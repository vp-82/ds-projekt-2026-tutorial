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

## Hypothesis · 2026-10-09 · Cycling grew at the comparable places

**Expected:** at least 6 of the 10 comparable places grew from 2019 to 2025.

**Test:** the answer step of `uv run build` applies the rules for the first answer to `data/derived/place_year.parquet` and counts the places that grew, shrank, are unchanged or cannot be compared.

**Result:** 8 of the 10 comparable places grew, against the expected 6; 2 shrank (−7.4 and −20.4 percent) and none is unchanged. The growth ranges from +5.4 to +89.5 percent; the smallest, place 2682375/1247055, lies just above the 5 percent band. For the city: yes. 34 places cannot be compared.

**Decision:** the first answer stands. Yes, cycling grew from 2019 to 2025 at 8 of the 10 places that can be compared. The answer covers these 10 places only. It says nothing about the 34 places that cannot be compared, and whether the counting places stand for the whole city stays an untested assumption. Loop one is done. Loop two asks whether the answer holds on dry weekdays.

## AI use · 2026-10-09 · the first answer

**Delegated:** the answer step of `uv run build` (`place_change_table`, `city_sentence`, `answer`), the tests in `tests/test_answer.py` and the README update.

**Mine:** the rules, the fixture `tests/fixtures/place_year_small.csv` and the expected results for its five places and for the city, the wording of the reasons and that two reasons are joined with " and ", the hypothesis and the decision that follows from it.

**Checks passed:**
- Seven tests green.
- Outside the tests, a one-off run confirmed that exactly 5 percent counts as unchanged and that two reasons are joined with " and ".
- On the real data: 44 places, 10 comparable, as in the hypothesis of 2026-10-09 on comparable places. Place 2681319/1248665 checked by hand: 863.835616 bikes per day in 2019 (365 days) and 1240.101648 in 2025 (364 days) give +43.56 percent.

## Decision · 2026-10-09 · repository settings that are not files

Two settings live on GitHub, not in the repository, and are recorded here.

- Ruleset "protect main" (id 24737527, Settings → Rules → Rulesets): changes reach main only through a pull request; the `tests` check from GitHub Actions must pass; nobody can bypass it, including the owner; main cannot be deleted or force-pushed; no approvals are required, because I work alone. A branch does not need to be up to date with main before merging. GitHub added `require_extra_approval_for_unattributed_changes: true` on its own; its effect here is unknown and it has not blocked a merge so far.
- Head branches are deleted automatically after a pull request is merged (Settings → General → Pull Requests). Local copies are deleted by hand.

Checked on 2026-10-08 with PR #4: a failing `tests` check blocked the merge.

## Decision · 2026-10-14 · rules for a dry weekday

These rules are fixed before any comparison on dry weekdays is computed.

- Weekday: Monday to Friday. Known limit: public holidays count as weekdays.
- Dry: a day with zero minutes of rain, parameter `RainDur` with daily values, at the station `Zch_Stampfenbachstrasse`. A weekday without a known `RainDur` value at that station is not dry. Known limit: one station stands for the whole city.
- Source: the city's daily weather data, one CSV per year at `https://data.stadt-zuerich.ch/dataset/ugz_meteodaten_tagesmittelwerte/download/ugz_ogd_meteo_d1_<year>.csv`.
- Places and years: the same 10 comparable places and the same years, 2019 and 2025, as the first answer. The 5 percent band and the majority rule stay.

## Hypothesis · 2026-10-14 · Enough dry weekdays with bike data remain at the comparable places

**Expected:** at least 80 dry weekdays with bike data per place in each of the two years, at all 10 places.

**Test:** for each of the 10 comparable places in `data/derived/answer.parquet` and each of the two years, count the days that are a dry weekday and have bike data in `data/derived/counts.parquet`. The two weather files were downloaded once for this count, outside `data/raw`, and are not part of the pipeline. Only this count was run; no change between the years was computed.

**Result:** all 10 places have at least 80 dry weekdays with bike data in both years, against the expected 80: 117 to 120 in 2019 and 119 to 130 in 2025. Both years have 261 weekdays, of which 120 (2019) and 130 (2025) are dry; no weekday lacks a known `RainDur` value, so 0 weekdays count as not dry for that reason. Per place (OST/NORD: 2019, 2025):

- 2681319/1248665: 120, 130
- 2681339/1248647: 120, 130
- 2682296/1248311: 120, 130
- 2682375/1247055: 120, 119
- 2682731/1247708: 119, 130
- 2682873/1245891: 117, 130
- 2682881/1246549: 120, 130
- 2682933/1248821: 120, 130
- 2683457/1247065: 120, 130
- 2684006/1246566: 120, 128

**Decision:** the rules for loop two stand. Every comparable place has at least 117 dry weekdays with bike data in each year, so the comparison on dry weekdays rests on about 120 days per place and year instead of 300 or more. The answer for loop two names that.

## AI use · 2026-10-14 · rules for a dry weekday

**Delegated:** writing the rules into `docs/one-pager.md` and `docs/log.md`, the one-off download of the two weather files and the count for the hypothesis.

**Mine:** the rules, including that a weekday without a known `RainDur` value is not dry, the hypothesis and its expected value.

**Checks passed:**
- Each weather file has exactly one `RainDur` row per day for `Zch_Stampfenbachstrasse` (365 in 2019, 365 in 2025), all in minutes and with status "bereinigt".
- A day has bike data under the same test as `place_year_table` (VELO_IN or VELO_OUT not null); the 10 places are the ones not marked "not comparable" in `answer.parquet`.

## Decision · 2026-10-15 · reading the weather files

The date of a day is the first 10 characters of `Datum`, the local date as the file gives it. Every `Datum` in the 2019 and 2025 files carries the offset +0100, also in summer, so converting to UTC would move every day back by one. Missing values are written as `NA` in the real files, and the fixture (`tests/fixtures/weather_small.csv`) pins this with its 2020-03-06 row; an empty field also counts as missing. When a day has more than one `RainDur` value at `Zch_Stampfenbachstrasse`, the days step stops with an error instead of picking one; the 2019 and 2025 files have none.

## AI use · 2026-10-15 · the days step

**Delegated:** the weather downloads in `uv run build`, the days step (`read_weather`, `day_table`, `days`), the tests in `tests/test_days.py`, including the two `RainDur` rows for one day written inside the test, and the README update.

**Mine:** the step and its columns, the fixture `tests/fixtures/weather_small.csv` and the six expected rows, and the decision that two `RainDur` values for one day stop the step.

**Checks passed:**
- Ten tests green.
- `uv run build` downloaded the two weather files into `data/raw` with one manifest line each, and a second run skipped them.
- `days.parquet` has 365 days per year and 120 dry weekdays in 2019 and 130 in 2025, the same as the one-off count in the hypothesis of 2026-10-14; no day lacks a rain value.

## AI use · 2026-10-15 · refactor of the answer step

**Delegated:** moving the 5 percent band of `place_change_table` into `status_expr`, so loop two can use the same rule, and making the opening of the city sentence a parameter of `city_sentence`, with "For the city" as the default. No change in behaviour.

**Mine:** the split of this refactor from the answer on dry weekdays.

**Checks passed:**
- The seven loop-one tests pass unchanged; ten tests green in all.
- `place_change_table` on `data/derived/place_year.parquet` gives a table identical to `data/derived/answer.parquet`, with the same sentence for the city.

## Hypothesis · 2026-10-15 · The answer holds on dry weekdays

**Expected:** at least 6 of the 10 comparable places grew on dry weekdays, and the answer for the city stays yes.

**Test:** the answer_dry step of `uv run build` keeps only the rows of `data/derived/counts.parquet` whose date is a dry weekday in `data/derived/days.parquet`, builds the table per place and year from them with `place_year_table`, and applies the rules for loop two: a place is comparable when it is comparable in `data/derived/answer.parquet`, and the 5 percent band and the majority rule stay.

**Result:** 6 of the 10 comparable places grew on dry weekdays, as expected (at least 6); 2 shrank and 2 are unchanged. For the city on dry weekdays: yes. On all days it was 8 grew, 2 shrank, 0 unchanged. The two places that grew on all days and are unchanged on dry weekdays are 2681339/1248647 (+9.2 percent on all days, +4.6 on dry weekdays) and 2682375/1247055 (+5.4, −1.3). Place 2682933/1248821 grew by +5.4 percent on dry weekdays, just above the 5 percent band. Each place has 117 to 120 dry weekdays with bike data in 2019 and 119 to 130 in 2025. Per place (OST/NORD: all days, dry weekdays):

- 2681319/1248665: grew +43.6, grew +34.6
- 2681339/1248647: grew +9.2, unchanged +4.6
- 2682296/1248311: shrank −7.4, shrank −14.0
- 2682375/1247055: grew +5.4, unchanged −1.3
- 2682731/1247708: shrank −20.4, shrank −24.5
- 2682873/1245891: grew +32.3, grew +25.5
- 2682881/1246549: grew +31.5, grew +23.2
- 2682933/1248821: grew +13.0, grew +5.4
- 2683457/1247065: grew +89.5, grew +64.6
- 2684006/1246566: grew +38.9, grew +28.3

**Decision:** the answer holds on dry weekdays, and it is weaker. Yes, cycling grew from 2019 to 2025 at 6 of the 10 comparable places on dry weekdays, against 8 of 10 on all days. The margin is one place at +5.4 percent, just above the band. Every one of the 10 places grew less, or shrank more, on dry weekdays than on all days. Why is not part of this project. The answer for the city reports both sentences. Loop two is done.

## AI use · 2026-10-15 · the answer on dry weekdays

**Delegated:** the answer_dry step of `uv run build` (`dry_counts`, `dry_place_change_table`, `answer_dry`), using `status_expr` and `city_sentence` from the refactor of the answer step, the tests in `tests/test_answer_dry.py`, including the small inputs written inside them, and the README update.

**Mine:** the rules for loop two, the fixture `tests/fixtures/place_year_dry_small.csv` and its expected results with `tests/fixtures/place_year_small.csv` as the loop-one side, the wording of the sentence, that places that cannot be compared keep their bikes per day, that a comparable place without dry-weekday data in one year stops the step, the hypothesis and its expected value.

**Checks passed:**
- Fourteen tests green.
- On the real data: 44 places, 10 comparable as in `answer.parquet`, 34 with the reason "not comparable on all days". The dry-weekday days with bike data per place (117 to 120 in 2019, 119 to 130 in 2025) match the count in the hypothesis of 2026-10-14.
- The final check ran `uv run build --force`, which downloaded the counts file again: the portal's copy now runs to 12 October 2026 (61421788 bytes, sha256 04c8c75d5715…). Both sentences and the change and status of all 10 places are the same as above; 367 place-years and 44 places as before.

## Decision · 2026-10-15 · --force leaves the raw files as they are

`--force` rebuilds every derived step and leaves the files in `data/raw` as they are. A new option `--force-download` fetches the raw files again as well and rebuilds every derived step. Before, `--force` also downloaded again, so there was no way to rebuild only the derived tables, and in #18 a forced rebuild pulled a newer counts file in the middle of a package. The rule in `CLAUDE.md` changes to match: "--force rebuilds every derived step; only --force-download fetches the raw files again" (issue #21).

## AI use · 2026-10-15 · --force and --force-download

**Delegated:** the issue text (#21), the change to `build.py`, the test in `tests/test_build.py` and the README update.

**Mine:** the decision, the wording of the rule in `CLAUDE.md`, and that the test must fail before the change.

**Checks passed:**
- Before the change, `tests/test_build.py` failed in two of its three cases: with `--force` the download step got force (True instead of False), and `--force-download` was an unknown option. After the change, all three pass; seventeen tests green.
- The test replaces the steps with stand-ins, so it downloads nothing and reads no `data/`.
- `uv run build --force` skipped the three downloads and rebuilt the five derived steps. `data/raw/manifest.csv` has 10 lines before and after, and both sentences for the city are unchanged.

## AI use · 2026-10-16 · the hypothesis skill

**Delegated:** the issue text (#23), the skill `.claude/skills/hypothesis/SKILL.md` and the README line.

**Mine:** that the routine becomes a skill and not a rule in `CLAUDE.md`, its steps, that the expected result and the Decision are mine and written in my words, the AI use entry after each Hypothesis entry, the branch `hypothesis-<slug>` when on main, and `disable-model-invocation: true`.

**Checks passed:**
- The skill's entry template has the same headings as the Hypothesis entries of 2026-10-07, 2026-10-09, 2026-10-14 and 2026-10-15.
- The skill has not been run yet; the first run is mine.

## Hypothesis · 2026-10-16 · Public holidays make no difference to the sentence on dry weekdays

**Expected:** the sentence for the city on dry weekdays stays the same when the canton of Zurich's ten public holidays per year (New Year, Berchtoldstag, Good Friday, Easter Monday, 1 May, Ascension, Whit Monday, 1 August, Christmas, St Stephen's Day; no half-days) no longer count as dry weekdays: yes, 6 grew, 2 shrank, 2 unchanged. Places may move within the counts.

**Test:** in a copy of `data/derived/days.parquet` held in memory, `dry_weekday` is set to false on the 20 holidays of 2019 and 2025 (all fall on Monday to Friday). On that copy, the existing functions `dry_counts`, `place_year_table`, `dry_place_change_table` (with `data/derived/answer.parquet`) and `city_sentence` give the sentence on dry weekdays, which is compared with the current one. No file in `data/` was written, the rules and the pipeline were not changed, and no comparison with all days was computed.

**Result:** the sentence changes, against the expected same sentence. For the city on dry weekdays: yes. 7 of 10 comparable places grew, 2 shrank, 1 is unchanged, 34 places cannot be compared (before: 6 grew, 2 shrank, 2 unchanged). 10 of the 20 holidays were dry weekdays, 3 in 2019 and 7 in 2025, so the dry weekdays go from 120 to 117 in 2019 and from 130 to 123 in 2025. Place 2681339/1248647 goes from unchanged (+4.6 percent) to grew (+6.8); no place moves the other way. The change rises at all 10 places, by 1.5 to 2.9 percentage points; place 2682933/1248821, the one just above the band, goes from +5.4 to +7.6. The answer for the city stays yes.

**Decision:** Rule stays. The holiday rule moves one place, 2681339, across the band and not the answer for the city. It is a known limit with a measured size, not a reason to change loop two. The one-pager gets the limit as a line in this package.

## AI use · 2026-10-16 · public holidays on dry weekdays

**Delegated:** the test, writing the entry and the line in `docs/one-pager.md`.

**Mine:** the hypothesis, the list of holidays and their dates, the expected result and the decision.

**Checks passed:**
- Second route: the same script on the day table without any holiday removed gives a table identical to `data/derived/answer_dry.parquet`.
- The 20 dates were checked by me; the script asserts that all of them fall on Monday to Friday.

## Hypothesis · 2026-10-16 · Someone else can rebuild the result from a fresh clone

**Expected:** yes: a fresh clone of the repository in a new folder, `uv sync` and `uv run build` give both sentences identical, and `answer.parquet` and `answer_dry.parquet` identical row for row, to my working copy. The test also reports whether the sha256 of the three raw files in the clone's manifest are the same as in my working copy.

**Test:** `git clone` of the GitHub repository (`main` at f73481d) into a new folder outside the working copy, then `uv sync` and `uv run build`, which downloaded the three raw files fresh from the portal. The last two lines of the build were compared with `city_sentence` on my `answer.parquet` and `answer_dry.parquet`; both tables were compared with exact values, same rows, order, columns and types; and the clone's manifest sha256 per raw file was compared with the latest line for that file in my `data/raw/manifest.csv`. The other derived tables were not compared, no tests were run in the clone, and nothing in my working copy's `data/` was written.

**Result:** yes, as expected. Both sentences are identical (8 of 10 grew on all days, 6 of 10 on dry weekdays), and `answer.parquet` and `answer_dry.parquet` are identical row for row (44 rows, 7 columns each). The two weather files have the same sha256 as in my working copy. The counts file does not: the portal moved again, from 61421788 bytes (sha256 04c8c75d5715…, downloaded 2026-10-15, data to 12 October 2026) to 61430196 bytes (sha256 8a26ffc8505d…, downloaded 2026-10-16, data to 13 October 2026). So the result was rebuilt from a newer counts file, not from the same raw files, and the answers for 2019 and 2025 did not change. Both builds used polars 2.0.0 from `uv.lock`.

**Decision:** Loop two is done. A fresh clone gives the same two sentences and the same tables from a counts file one day newer than mine, so the result holds when the source moves. Known limit: the clone ran on my machine, with the same Python and the same uv cache, the build has not run on another machine. The one-pager gets the check as a line under Done in this package.

## AI use · 2026-10-16 · rebuild from a fresh clone

**Delegated:** the test, writing the entry and the line in `docs/one-pager.md`.

**Mine:** the hypothesis, the expected result, that the test reports the sha256 of the raw files, and the decision.

**Checks passed:**
- The sentences of my working copy were taken from `city_sentence` on my answer tables, not from the clone's build output, so the two sides were computed separately.
- The clone started without a `data/` folder, so every raw file was downloaded and every table built inside the clone.

## Decision · 2026-10-23 · a package starts as an issue

From now on every package starts as an issue that a person writes before the branch exists, with the "Package" form in `.github/ISSUE_TEMPLATE/package.yml`. Its five required fields are what exists at the end, which question it serves, done when, kind and size, and out of scope. `CLAUDE.md` gets the rule in its Workflow section: a package starts as an issue that a person writes with the Package form before the branch exists, and its pull request closes that issue. Known limit: this package itself started before the form existed, so its pull request (#29) closes no issue.

Open:
- The reason for the decision.
- The form says that more than about 200 lines needs a reason; `CLAUDE.md` says to propose a split when larger. Whether a reason is enough.
- Whether blank issues stay possible (no `.github/ISSUE_TEMPLATE/config.yml`); `gh issue create` cannot fill the form.
- Whether package issues get a label; the title prefix can be edited away.
- Whether GitHub shows the form under New issue after the merge.

## AI use · 2026-10-23 · package issue form

**Delegated:** the issue form, the line in `README.md`, the wording of the line in `CLAUDE.md` and writing the entry.

**Mine:** the decision, that `CLAUDE.md` gets the rule, the form's name, title prefix, the five fields, their order and their descriptions.

**Checks passed:**
- The form parses as YAML and its title prefix is "Package: ".
