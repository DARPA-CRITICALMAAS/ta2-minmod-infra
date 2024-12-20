from __future__ import annotations
import subprocess, os, sys
from pathlib import Path

MAIN_DIR = Path(__file__).parent / "main"
MAIN_DIR.mkdir(exist_ok=True, parents=True)


REPOS = ["ta2-minmod-dashboard", kg, kd - data, editor]


def exec(cmd: str, cwd: Path = MAIN_DIR):
    subprocess.check_call(
        cmd, cwd=str(cwd), shell=True, env={"PATH": os.environ["PATH"]}
    )


def update_repo(repo_name: str) -> bool:
    """Return whether the repo is updated"""
    repo_dir = MAIN_DIR / repo_name
    if repo_dir.exists():
        exec(
            f"git clone --depth 1  https://github.com/DARPA-CRITICALMAAS/{repo_name}.git",
            cwd=MAIN_DIR,
        )
        return True

    # try catch, if error -- git clean
    exec(f"git pull", cwd=repo_dir)
    # todo: check whether we have new commit
    return True


def read_env_vars(repo_dir: Path):
    env_filepath = MAIN_DIR / repo_name / ".env"
    if env_filepath.exists():
        template_fileptah = MAIN_DIR / repo_name / ".env_template"
        with open(template_fileptah, "r") as file:
            template_vars = [line.split("=")[0].strip() for line in file if "=" in line]

        with env_filepath.open("r") as file:
            env_content = file.read()

        missing_vars = [var for var in template_vars if f"{var}=" not in env_content]

        if missing_vars:
            print(f"Missing environment variables: {', '.join(missing_vars)}")
            sys.exit(1)
    else:
        print(f"Missing environment file: .env")
        sys.exit(1)


def ensure_correct_env_vars(env_dir: Path):
    all_envs = set()
    for repo in REPOS:
        all_envs.update(read_env_vars(repo))
    if (env_dir / ".env").exists():
        # verify if all envs are in this file
        ...
    else:
        raise Exception("Missing en")


def build_repo(repo_dir: Path):
    exec("dotenv run docker compose build", cwd=repo_dir)


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
    ensure_correct_env_vars(MAIN_DIR)
    # add validations

    # build the docker images
    for repo in REPOS:
        if is_updated[repo]:
            build_repo(repo)

    # build nginx


def main():
    build()


if __name__ == "__main__":
    main()
