import argparse
from pathlib import Path

from ds_projekt_2026_tutorial.download import URL, download

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"


def main() -> None:
    parser = argparse.ArgumentParser(prog="build", description="Build the project's data from nothing.")
    parser.add_argument("--force", action="store_true", help="fetch files again even if they are already there")
    args = parser.parse_args()

    download(URL, RAW_DIR, force=args.force)
