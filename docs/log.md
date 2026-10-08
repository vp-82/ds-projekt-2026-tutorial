# Log

## Hypothesis · 2026-10-07 · The counting sites are the same every year

**Expected:** at least 80% of all sites in the data report in every year.

**Test:** count the sites per year and how many appear in every year, using the all-years file from the city's open data portal.

**Result:** 0% of site IDs report in every year, against the expected 80%. The check showed why: the 85 bike site IDs sit on 44 places, and a place gets a new ID every few years. Counted by place, 5 of the 44 places (11%) report bikes in every complete year, 2010 to 2025.

**Decision:** the unit of the table is the place, identified by its coordinates, not the site ID.

Open:
- Two coordinate pairs lie one metre apart (2683405/1251617 and 2683406/1251617) and may be one place.

## Decision · 2026-10-08 · source and first table

The pipeline uses the single all-years file from the portal, not the yearly CSVs, because it is one download and the exploration already ran on it. Known limit: when we looked, its data ended on 6 June 2026. The first table has one row per place and year, with the number of days that have data and the average number of bikes per day on those days. Which place-years count as comparable stays open.

**Revisit:** when newer data or the yearly files are needed.

## Decision · 2026-10-08 · one-sided counts and data range

A row with only one of VELO_IN or VELO_OUT counts the missing side as 0, because some counters count one direction only. The fixture (`tests/fixtures/counts_small.csv`) has a row that pins this. The all-years file now runs to 5 October 2026, so the earlier limit of 6 June no longer holds. Known limit: at one ID switch a single quarter hour is recorded under two site IDs and therefore counted twice (place 2682278/1248325, 2017-09-08 00:00, site IDs 1997 and 2319). It stays as it is for now.

## AI use · 2026-10-08 · load and derive steps

**Delegated:** the load and derive steps of `uv run build`, the functions `parse_counts` and `place_year_table`, and the test code.

**Mine:** the fixture `tests/fixtures/counts_small.csv` and the expected table the test checks against.

**Checks passed:**
- Four tests green.
- The same table after deleting `data/derived` and rebuilding (367 place-years).
- 44 places, 5 of them reporting in every year from 2010 to 2025, as in the notebook.

## AI use · 2026-10-08 · CI workflow

**Delegated:** the workflow `.github/workflows/tests.yml`, set up as in the uv guide for GitHub Actions (setup-uv v9.0.0, uv 0.12.23, cache on, `uv sync --locked --dev`, `uv run pytest tests`).

**Mine:** tests run on every pull request and every push to main; CI does not run `uv run build`, because it downloads the full raw file; the setup-uv version follows the uv docs example; local uv stays at 0.7.12 and `uv.lock` is not regenerated for CI.

**Checks passed:**
- `uv sync --locked --dev` and `uv run pytest tests` locally with uv 0.7.12: four tests green.
- `uv sync --locked --dev` locally with uv 0.12.23 accepts the existing `uv.lock`.
