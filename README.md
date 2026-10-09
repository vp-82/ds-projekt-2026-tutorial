# Is cycling in Zurich growing?

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Run `uv sync` to create the virtual environment.
3. Run `uv run build` to build everything from nothing.

## What `uv run build` produces

| Step | Output | What it holds |
|---|---|---|
| download | `data/raw/verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet` | the all-years file from the city's open data portal; each download adds a line to `data/raw/manifest.csv` |
| load | `data/derived/counts.parquet` | the raw counts, with a real timestamp |
| derive | `data/derived/place_year.parquet` | one row per place and year: days with bike data and average bikes per day |
| answer | `data/derived/answer.parquet` | one row per place: bikes per day in 2019 and 2025, the change in percent, a status (grew, shrank, unchanged or not comparable) and the reason for places that cannot be compared |

Each step prints one line and skips when its output already exists. Add `--force` to rebuild every step, including the download. The last line is the sentence for the city: yes or no, and how many places grew, shrank, are unchanged or cannot be compared. The rules behind it are in `docs/one-pager.md`.

`uv run pytest` runs the tests.
