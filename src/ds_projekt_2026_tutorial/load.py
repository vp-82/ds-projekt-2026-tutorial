from pathlib import Path

import polars as pl


def parse_counts(raw: pl.DataFrame) -> pl.DataFrame:
    """Return the raw counts with DATUM as a real timestamp."""
    return raw.with_columns(pl.col("DATUM").str.to_datetime("%Y-%m-%dT%H:%M", strict=True))


def load(raw_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write a clean copy of the raw file to out_path, unless it is already there."""
    if out_path.exists() and not force:
        print(f"load: skipped, {out_path} already exists")
        return out_path

    counts = parse_counts(pl.read_parquet(raw_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a .part file first so an interrupted run never looks complete.
    part = out_path.with_name(out_path.name + ".part")
    counts.write_parquet(part)
    part.replace(out_path)

    first, last = counts["DATUM"].min(), counts["DATUM"].max()
    print(f"load: wrote {out_path} ({counts.height} rows, {first:%Y-%m-%d} to {last:%Y-%m-%d})")
    return out_path
