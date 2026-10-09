from pathlib import Path

import polars as pl
from polars.testing import assert_frame_equal

from ds_projekt_2026_tutorial.answer import answer, city_sentence, place_change_table

FIXTURE = Path(__file__).parent / "fixtures" / "place_year_small.csv"
SENTENCE = (
    "For the city: no. 1 of 3 comparable places grew, 1 shrank, 1 is unchanged, 2 places cannot be compared."
)


def test_place_change_table_on_fixture():
    table = place_change_table(pl.read_csv(FIXTURE))
    expected = pl.DataFrame(
        {
            "OST": [1000, 3000, 5000, 7000, 9000],
            "NORD": [2000, 4000, 6000, 8000, 1000],
            "bikes_per_day_2019": [100.0, 200.0, 100.0, 50.0, None],
            "bikes_per_day_2025": [120.0, 150.0, 103.0, 80.0, 60.0],
            "change_percent": [20.0, -25.0, 3.0, None, None],
            "status": ["grew", "shrank", "unchanged", "not comparable", "not comparable"],
            "reason": [None, None, None, "2019: fewer than 300 days (120)", "2019: no data"],
        }
    )
    assert_frame_equal(table, expected, check_dtypes=False)


def test_city_sentence_on_fixture():
    assert city_sentence(place_change_table(pl.read_csv(FIXTURE))) == SENTENCE


def test_answer_writes_skips_and_forces(tmp_path, capsys):
    place_year_path = tmp_path / "place_year.parquet"
    pl.read_csv(FIXTURE).write_parquet(place_year_path)
    out_path = tmp_path / "derived" / "answer.parquet"

    answer(place_year_path, out_path)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0] and out[0].endswith(SENTENCE)

    answer(place_year_path, out_path)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "skipped" in out[0] and out[0].endswith(SENTENCE)

    answer(place_year_path, out_path, force=True)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0]
