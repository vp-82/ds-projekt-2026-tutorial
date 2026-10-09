from pathlib import Path

import polars as pl


def place_year_table(counts: pl.DataFrame) -> pl.DataFrame:
    """One row per place (OST, NORD) and year: days with bike data and average bikes per day.

    Rows without any bike count drop out. A missing direction counts as 0.
    Site IDs at the same coordinates form one place. Rows of the same site ID
    for the same quarter hour add up (the hour repeats when the clocks go back).
    When several site IDs record the same quarter hour at a place, it counts
    once, with the highest total.
    """
    return (
        counts.filter(pl.col("VELO_IN").is_not_null() | pl.col("VELO_OUT").is_not_null())
        .with_columns(bikes=pl.col("VELO_IN").fill_null(0) + pl.col("VELO_OUT").fill_null(0))
        # Rows of one site ID add up; across site IDs only the highest counts.
        .group_by("OST", "NORD", "DATUM", "FK_STANDORT")
        .agg(pl.col("bikes").sum())
        .group_by("OST", "NORD", "DATUM")
        .agg(pl.col("bikes").max())
        .with_columns(date=pl.col("DATUM").dt.date())
        .group_by("OST", "NORD", "date")
        .agg(pl.col("bikes").sum())
        .group_by("OST", "NORD", pl.col("date").dt.year().alias("year"))
        .agg(
            pl.len().alias("days_with_bikes"),
            pl.col("bikes").mean().alias("bikes_per_day"),
        )
        .sort("OST", "NORD", "year")
    )


def derive(counts_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write the place-year table to out_path, unless it is already there."""
    if out_path.exists() and not force:
        print(f"derive: skipped, {out_path} already exists")
        return out_path

    table = place_year_table(pl.read_parquet(counts_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a .part file first so an interrupted run never looks complete.
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    n_places = table.select("OST", "NORD").unique().height
    print(f"derive: wrote {out_path} ({table.height} place-years, {n_places} places)")
    return out_path
