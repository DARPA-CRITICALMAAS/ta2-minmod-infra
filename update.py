from build import exec, MAIN_DIR
from pathlib import Path


def build_kg():
    minmod_kg_path = MAIN_DIR / "ta2-minmod-kg"
    # install dependencies
    exec("python -m venv .venv", cwd=minmod_kg_path)
    exec("poetry lock --no-update", cwd=minmod_kg_path)
    exec("poetry install --only main", cwd=minmod_kg_path)

    # activate venv and build
    exec("source ta2-minmod-kg/.venv/bin/activate", cwd=MAIN_DIR)
    exec("cp ./config/config.yml ./ta2-minmod-kg", cwd=MAIN_DIR)
    exec(
        "ta2-minmod-kg/.venv/bin/python -m statickg ta2-minmod-kg/etl.yml ./kgdata ta2-minmod-data --overwrite-config --refresh 20",
        cwd=MAIN_DIR,
    )


def update_services(repo_dir: Path):
    exec(
        "docker compose -f ./docker-compose.yml up -d",
        cwd=repo_dir,
    )


def main():
    # update and run services
    update_services(MAIN_DIR.parent)
    # build kg
    build_kg()


if __name__ == "__main__":
    main()
