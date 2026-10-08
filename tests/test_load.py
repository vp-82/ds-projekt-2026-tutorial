import datetime
from pathlib import Path

import polars as pl

from ds_projekt_2026_tutorial.load import load, parse_counts

FIXTURE = Path(__file__).parent / "fixtures" / "counts_small.csv"


def test_parse_counts_makes_datum_a_timestamp():
    raw = pl.read_csv(FIXTURE)
    counts = parse_counts(raw)
    assert counts.schema["DATUM"] == pl.Datetime
    assert counts.height == raw.height
    assert counts["DATUM"].min() == datetime.datetime(2019, 3, 1, 8, 0)
    assert counts["DATUM"].max() == datetime.datetime(2020, 3, 1, 8, 15)


def test_load_writes_then_skips(tmp_path, capsys):
    raw_path = tmp_path / "raw.parquet"
    pl.read_csv(FIXTURE).write_parquet(raw_path)
    out_path = tmp_path / "derived" / "counts.parquet"

    load(raw_path, out_path)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0] and "2019-03-01 to 2020-03-01" in out[0]

    load(raw_path, out_path)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "skipped" in out[0]

    load(raw_path, out_path, force=True)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0]
