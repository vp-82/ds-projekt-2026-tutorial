from pathlib import Path

import polars as pl

# Rules for the first answer, see docs/one-pager.md and docs/log.md (2026-10-09).
FIRST_YEAR = 2019
LAST_YEAR = 2025
MIN_DAYS = 300
BAND_PERCENT = 5.0


def place_change_table(place_year: pl.DataFrame) -> pl.DataFrame:
    """One row per place: bikes per day in both years, the change in percent and a status.

    A place is comparable when it has bike data on at least MIN_DAYS days in both years.
    It grew or shrank when the change is more than BAND_PERCENT, else it is unchanged.
    Places that are not comparable get a reason and no change.
    """

    def year(y: int) -> pl.DataFrame:
        return place_year.filter(pl.col("year") == y).select(
            "OST",
            "NORD",
            pl.col("days_with_bikes").alias(f"days_{y}"),
            pl.col("bikes_per_day").alias(f"bikes_per_day_{y}"),
        )

    def reason(y: int) -> pl.Expr:
        days = pl.col(f"days_{y}")
        return (
            pl.when(days.is_null())
            .then(pl.lit(f"{y}: no data"))
            .when(days < MIN_DAYS)
            .then(pl.format(f"{y}: fewer than {MIN_DAYS} days ({{}})", days))
        )

    first, last = pl.col(f"bikes_per_day_{FIRST_YEAR}"), pl.col(f"bikes_per_day_{LAST_YEAR}")
    reasons = pl.concat_str([reason(FIRST_YEAR), reason(LAST_YEAR)], separator=" and ", ignore_nulls=True)
    return (
        place_year.select("OST", "NORD")
        .unique()
        .join(year(FIRST_YEAR), on=["OST", "NORD"], how="left")
        .join(year(LAST_YEAR), on=["OST", "NORD"], how="left")
        .with_columns(reason=pl.when(reasons != "").then(reasons))
        .with_columns(change_percent=pl.when(pl.col("reason").is_null()).then((last - first) / first * 100))
        .with_columns(
            status=pl.when(pl.col("reason").is_not_null())
            .then(pl.lit("not comparable"))
            .when(pl.col("change_percent") > BAND_PERCENT)
            .then(pl.lit("grew"))
            .when(pl.col("change_percent") < -BAND_PERCENT)
            .then(pl.lit("shrank"))
            .otherwise(pl.lit("unchanged"))
        )
        .select("OST", "NORD", first, last, "change_percent", "status", "reason")
        .sort("OST", "NORD")
    )


def city_sentence(table: pl.DataFrame) -> str:
    """The answer for the city: yes when more than half of the comparable places grew."""
    n = {status: (table["status"] == status).sum() for status in ["grew", "shrank", "unchanged", "not comparable"]}
    comparable = n["grew"] + n["shrank"] + n["unchanged"]
    yes_no = "yes" if n["grew"] > comparable / 2 else "no"
    is_are = "is" if n["unchanged"] == 1 else "are"
    places = "place" if n["not comparable"] == 1 else "places"
    return (
        f"For the city: {yes_no}. {n['grew']} of {comparable} comparable places grew, {n['shrank']} shrank, "
        f"{n['unchanged']} {is_are} unchanged, {n['not comparable']} {places} cannot be compared."
    )


def answer(place_year_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write the place change table to out_path, unless it is already there. Prints the city sentence."""
    if out_path.exists() and not force:
        print(f"answer: skipped, {out_path} already exists. {city_sentence(pl.read_parquet(out_path))}")
        return out_path

    table = place_change_table(pl.read_parquet(place_year_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a .part file first so an interrupted run never looks complete.
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    print(f"answer: wrote {out_path}. {city_sentence(table)}")
    return out_path
