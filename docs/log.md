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
