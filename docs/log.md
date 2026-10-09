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

## Decision · 2026-10-09 · one quarter hour under two site IDs

When a place has rows from more than one site ID for the same quarter hour, that quarter hour counts once, with the highest total (VELO_IN + VELO_OUT) of those site IDs. This resolves the known limit from 2026-10-08: at place 2682278/1248325 on 2017-09-08 00:00, site ID 2319 (40 bikes) counts and site ID 1997 (31 bikes) does not. The fixture pins it with a second site ID for place 1000/2000 at 2020-03-01 08:00 (issue #6). It is the only such quarter hour in the data; the 2017 row of that place goes from 4631.565714 to 4631.477143 bikes per day, and no other row of the table changes.

## Decision · 2026-10-09 · one quarter hour twice under the same site ID

Rows from the same site ID for the same quarter hour add up, because that hour really happens twice when the clocks go back. This covers 560 of the 604 such quarter hours, all at 02:00–02:45 on the last Sunday in October. Known limit: the other 44 (11 places, 2013-03-31 03:00–03:45) are unexplained, since the clocks go forward that night; they also add up and stay as they are.

## AI use · 2026-10-09 · one quarter hour under two site IDs

**Delegated:** the change to `place_year_table`, the issue text (#6) and the check against the real data.

**Mine:** both decisions, the fixture row and the expected value of 7 bikes per day for place 1000/2000 in 2020; later the fixture row `3,2020-03-01T08:00,2,0,,,3000,4000` and the expected value of 17 bikes per day for place 3000/4000 in 2020 (pins that rows of the same site ID add up).

**Delegated (later):** the test update and the docstring of `place_year_table`.

**Checks passed:**
- The test failed before the change (9.0 instead of 7.0) and passes after it; four tests green.
- After deleting `data/derived/place_year.parquet` and rebuilding: 367 place-years and 44 places as before, and only the 2017 row of place 2682278/1248325 differs from the old table.
- A first version took the highest count over all rows of a quarter hour and would also have collapsed the 604 same-ID repeats; it was narrowed to apply across site IDs only.

## Decision · 2026-10-09 · no review run for commits by claude[bot]

The Claude Code Review job skips when the run was started by `claude[bot]`, for example when @claude pushes a commit to a pull request. The action refuses runs started by a bot ("Workflow initiated by non-human actor: claude (type: Bot)"), so the check turned red on PR #7 and had to be ignored; a skipped check says what happened. The bot is not added to `allowed_bots` (issue #8). Commits pushed by @claude are read by a person before merging, because no review runs on them.

## AI use · 2026-10-09 · no review run for commits by claude[bot]

**Delegated:** the job condition in `.github/workflows/claude-code-review.yml` and the issue text (#8).

**Mine:** the decision to skip rather than allow the bot.

**Checks passed:**
- The two red runs on PR #7 (37901246364, 37908694827) had actor `claude[bot]` and failed with the non-human actor error.
- On this pull request, the commit pushed by @claude (01cdae6) shows Claude Code Review as skipped and Tests as green.

## Decision · 2026-10-09 · rules for the first answer

These rules are fixed before any comparison is computed, so they are not chosen after seeing the result.

- Years: compare 2025, the last full year, with 2019, the last full year before the pandemic.
- Days: a day counts when it has any bike data, as the place-year table does now. Known limit: a day with a partial outage counts as a full day and lowers the average.
- Comparable: a place counts in a year when it has bike data on at least 300 days of that year. A place is comparable when that holds in both years.
- Change: a place grew when its bikes per day rose by more than 5 percent, shrank when they fell by more than 5 percent, and is unchanged in between.
- Answer for the city: yes when more than half of the comparable places grew.

## Hypothesis · 2026-10-09 · Enough places are comparable to answer for the city

**Expected:** at least 20 of the 44 places are comparable.

**Test:** count the places with bike data on at least 300 days in both 2019 and 2025, in `data/derived/place_year.parquet`. Only this count was run; no change between the years was computed.

**Result:** 10 of the 44 places are comparable, against the expected 20. 14 places reach 300 days in 2019 and 19 in 2025.

**Decision:** the rules stay. 10 comparable places are fewer than expected, and they are enough for a first answer as long as the answer says so. The sentence for the city names the 10 comparable places and the 34 that cannot be compared. Finding a pair of years with more comparable places is a question for a later loop.

## AI use · 2026-10-09 · rules for the first answer

**Delegated:** writing the rules into `docs/one-pager.md` and `docs/log.md`, and the count for the hypothesis.

**Mine:** the rules, the hypothesis and its expected value, and the decision that follows from the count.

**Checks passed:**
- `place_year.parquet` was built after the last change to the derive logic (only the docstring changed since): 44 places, years 2009 to 2026.
