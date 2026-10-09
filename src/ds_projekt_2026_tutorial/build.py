import argparse
from pathlib import Path

from ds_projekt_2026_tutorial.answer import answer
from ds_projekt_2026_tutorial.derive import derive
from ds_projekt_2026_tutorial.download import URL, download
from ds_projekt_2026_tutorial.load import load

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
DERIVED_DIR = ROOT / "data" / "derived"


def main() -> None:
    parser = argparse.ArgumentParser(prog="build", description="Build the project's data from nothing.")
    parser.add_argument("--force", action="store_true", help="rebuild every step even if its output is already there")
    args = parser.parse_args()

    raw = download(URL, RAW_DIR, force=args.force)
    counts = load(raw, DERIVED_DIR / "counts.parquet", force=args.force)
    place_year = derive(counts, DERIVED_DIR / "place_year.parquet", force=args.force)
    answer(place_year, DERIVED_DIR / "answer.parquet", force=args.force)
