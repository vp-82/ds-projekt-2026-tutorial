# One-pager: Is cycling in Zurich growing?

## Why

**The question as it arrived:** "Is cycling in Zurich growing?"
Nothing else came with it: no time span, no definition of cycling, no place.

**Who reads the result:** a planner in the city's transport planning who has to answer this in public, for example in a yearly report on the bike strategy. They will say yes or no, name where, and must be able to defend the answer when someone doubts the numbers.

## What

**What the reader gets:** a table, with one sentence above it.

- The sentence gives yes or no for the city, plus how many places grew, shrank or cannot be compared.
- The table has the average number of bikes per day and the change against the first year.
- A chart is a view of the table, not the result.

**Unit of the result:** one row per place and year. Changed on 2026-10-08 from one row per counting site and year, because a place gets a new site ID every few years, so site IDs cannot be followed across years (see `docs/log.md`).

Open:
- Which years are covered.
- Which days of a place count as comparable.
- What makes the answer "yes" for the city. Must be decided before the first comparison is computed, so the rule is not chosen after seeing the result.
- When a place counts as grown or shrunk, for example whether a small change counts. Must be decided before the first comparison is computed, so the rule is not chosen after seeing the result.

## How

**Source:** the open data portal of the city of Zurich, dataset "Daten der automatischen Fussgänger- und Velozählung, Viertelstundenwerte". The pipeline uses the single all-years file (`verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet`) with counts per counter and quarter hour, not the yearly CSVs. Changed on 2026-10-08, because it is one download and the exploration already ran on it (see `docs/log.md`). Its data runs to 5 October 2026 (updated on 2026-10-08: the file on the portal had grown since the earlier limit of 6 June 2026).

**Loop one (all days):**
1. Download the all-years file.
2. Sum the quarter hours to bikes per place and day.
3. Decide which days of a place are complete.
4. Keep the places that can be compared across years.
5. Average per place and year, then compute the change against the first year.

**First table:** one row per place and year, with the number of days that have data and the average number of bikes per day on those days. Which place-years count as comparable stays open.

**Loop two (dry weekdays):** repeat the comparison on dry weekdays only. This needs a second source, the city's daily weather data.

Open:
- The rule for "comparable" stays open until the data has been seen.
- What counts as a dry weekday for loop two: what counts as "dry" and which days count as weekdays.

## Non-goals

- A city-wide number of cyclists. The counters sit at chosen sites and say nothing about the streets between them.
- Causes. Whether a new bike lane or a policy changed anything is a different project.
- Forecasts.
- Pedestrians. They are in the same dataset and stay out.
- Correcting the counts to true bike numbers. The result compares a place with itself over time, so the counting error matters less as long as it stays the same.

## Done

- Every place and year has either a value or a stated reason why it cannot be compared. Nothing is dropped silently.
- The sentence for the city exists, with the counts of places that grew, shrank or cannot be compared.
- The unknowns are written into the result: counting error, sites that moved or were added, the years covered.
- Someone else can rebuild the table from nothing with one command and gets the same numbers from the same raw files.
- Loop one is done when all of this holds for all days. Loop two is done when the same table exists for dry weekdays and the two tables are compared.
