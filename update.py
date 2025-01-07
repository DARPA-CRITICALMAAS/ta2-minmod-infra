import argparse
import sys
from pathlib import Path

from build import MAIN_DIR, exec


def build_kg(test: bool = False):
    data_repo = "ta2-minmod-data" if not test else "ta2-minmod-data-sample"
    exec(
        f"ta2-minmod-kg/.venv/bin/python -m statickg ta2-minmod-kg/etl.yml ./kgdata {data_repo} --overwrite-config --no-loop",
        cwd=MAIN_DIR,
        env={
            "CFG_FILE": str(MAIN_DIR / "config/config.yml"),
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test", action="store_true", help="Run the script in test mode."
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    build_kg(args.test)
