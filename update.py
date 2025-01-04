from build import exec, MAIN_DIR
from pathlib import Path


def update_services(repo_dir: Path):
    exec(
        "docker compose -f ./docker-compose.yml up",
        cwd=repo_dir,
    )


def main():
    update_services(MAIN_DIR.parent)


if __name__ == "__main__":
    main()
