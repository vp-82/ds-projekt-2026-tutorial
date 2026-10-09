from pathlib import Path

import polars as pl
from polars.testing import assert_frame_equal

from ds_projekt_2026_tutorial.derive import place_year_table
from ds_projekt_2026_tutorial.load import parse_counts

FIXTURE = Path(__file__).parent / "fixtures" / "counts_small.csv"


def test_place_year_table_on_fixture():
    table = place_year_table(parse_counts(pl.read_csv(FIXTURE)))
    expected = pl.DataFrame(
        {
            "OST": [1000, 1000, 3000],
            "NORD": [2000, 2000, 4000],
            "year": [2019, 2020, 2020],
            "days_with_bikes": [2, 1, 1],
            "bikes_per_day": [5.0, 7.0, 15.0],
        }
    )
    assert_frame_equal(table, expected, check_dtypes=False)
