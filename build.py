from __future__ import annotations
import subprocess, os, sys
from pathlib import Path
from exceptions import EnvFileValidationError, MissingEnvTemplateFileError

MAIN_DIR = Path(__file__).parent / "main"
MAIN_DIR.mkdir(exist_ok=True, parents=True)


# REPOS = ["ta2-minmod-dashboard", kg, kd - data, editor]
REPOS = [
    "ta2-minmod-dashboard",
    "ta2-minmod-kg",
]


def exec(cmd: str, cwd: Path = MAIN_DIR):
    subprocess.check_call(
        cmd, cwd=str(cwd), shell=True, env={"PATH": os.environ["PATH"]}
    )


def update_repo(repo_name: str) -> bool:
    repo_dir = MAIN_DIR / repo_name

    # Clone the repo if it does not exist
    if not repo_dir.exists():
        exec(
            f"git clone --depth 1 https://github.com/DARPA-CRITICALMAAS/{repo_name}.git",
            cwd=MAIN_DIR,
        )
        return True

    # pull changes
    try:
        exec("git pull", cwd=repo_dir)
        return True  # Repository updated
    except subprocess.CalledProcessError as e:
        print(f"Error during 'git pull': {e}")
        # retry with clean
        try:
            exec("git clean -fd", cwd=repo_dir)
            exec("git pull", cwd=repo_dir)
            return True
        except subprocess.CalledProcessError as retry_error:
            print(f"Error during retry 'git pull': {retry_error}")
            return False


def read_env_vars(envfile_path: Path) -> list[str]:

    env_vars = {}

    if envfile_path.exists():
        with open(envfile_path, "r") as file:
            env_vars = [
                line.replace("export ", "").split("=")[0].strip()
                for line in file
                if "=" in line
            ]
    else:
        raise MissingEnvTemplateFileError("No env template file present!")

    return env_vars


def process_env_file(env_dir: Path):
    all_envs = set()

    for repo in REPOS:
        envfile_path = MAIN_DIR / repo / "env.template"
        all_envs.update(read_env_vars(envfile_path))

    envfile_path = env_dir / ".env"
    if envfile_path.exists():
        current_envs = set()

        current_envs.update(read_env_vars(envfile_path))

        ## validate current envs and all envs

        # Update envs
        update_envs = all_envs - current_envs
        # Delete envs
        delete_envs = current_envs - all_envs

        # add_comments
        if not update_envs or not delete_envs:
            create_or_add_comments(envfile_path, update_envs, delete_envs)

            # log
            print(
                "Found missing envs in .env file, please update and remove the comments"
            )

        # log
        print("Env file processed : No Changes")

    else:

        # Update envs
        update_envs = all_envs
        # add comments
        create_or_add_comments(envfile_path, update_envs)

        # log
        print("Created .env file, please update and remove the comments")


def create_or_add_comments(
    envfile_path: Path, update_envs: set, delete_envs: set = None
):

    processed_lines = []

    if envfile_path.exists():
        with open(envfile_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("#"):
                key = stripped_line.split("=")[0].strip()
                if delete_envs and key in delete_envs:
                    processed_lines.append(f"#delete variable\n{line}")
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)

    # Add new variables in update_envs at the end
    if update_envs:
        for update_var in update_envs:
            processed_lines.append(f"#update variable :\n{update_var}=\n")

    # Write back to the .env file
    with open(envfile_path, "w") as file:
        file.writelines(processed_lines)


def validate_envfile(envfile_path: Path):

    with open(envfile_path, "r") as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            raise EnvFileValidationError(
                f"Comment found on line {line_num}: {line.strip()}"
            )

    print("Validation passed: No comments found in the .env file.")


def build_repo(repo_dir: Path):
    exec("docker compose build dashboard nginx api", cwd=repo_dir)


def build():
    is_updated = {}
    for repo in REPOS:
        is_updated[repo] = update_repo(repo)

    # setup the other directories.
    kgdata = MAIN_DIR / "kgdata"
    config = MAIN_DIR / "config"
    certs = MAIN_DIR / "certs"

    kgdata.mkdir(exist_ok=True, parents=True)
    config.mkdir(exist_ok=True, parents=True)
    certs.mkdir(exist_ok=True, parents=True)

    # setup env variables
    process_env_file(MAIN_DIR.parent)

    # Validate envfile
    validate_envfile(MAIN_DIR.parent / ".env")

    # build the docker images
    build_repo(MAIN_DIR.parent)


def main():
    build()


if __name__ == "__main__":
    main()
