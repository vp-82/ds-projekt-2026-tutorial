# Assumptions

These are what must be true for the steps in How (`docs/one-pager.md`) to produce the table in What. They come from the one-pager, before any data was opened. Importance and evidence are the project owner's ratings.

Sorted by importance (high first), then by evidence (low first), so important assumptions with little evidence come first. # is the original number.

| # | Assumption | Importance | Evidence |
|---|---|---|---|
| 1 | **Stable counting:** each site counts bikes with the same error in every year, with no new sensor, recalibration or change of method in between. | high | low |
| 2 | **Same place:** a counter ID means the same physical place in every year, so a site that moved never keeps its old ID. | high | low |
| 7 | **Enough sites:** enough sites have comparable data in both the first year and later years to support a sentence about the whole city. | high | low |
| 8 | **Sites stand for the city:** the set of counting sites is a fair enough basis for the planner to answer yes or no for Zurich as a whole. | high | low |
| 11 | **Weather comparable across years:** weather is comparable across years, so a wet year does not look like a decline in cycling. | high | low |
| 12 | **Not answered already:** nobody has answered this already, for example the city itself in a yearly report. | high | low |
| 4 | **Gaps are visible:** a quarter hour with no count shows up as missing in the files, not as a zero, so complete days can be told apart from incomplete ones. | high | medium |
| 3 | **Bikes separable:** the files label which counts are bikes and which are pedestrians, so bikes can be kept and pedestrians dropped. | high | high |
| 5 | **Raw values:** the counts are raw measurements, or any values the city filled in or corrected are marked as such. | medium | low |
| 6 | **Same file structure:** the yearly files share column names, IDs and units, so they can be joined into one series without guessing. | medium | low |
| 9 | **Changes are real, not detours:** a site's change over the years comes from cycling changing, not from bikes being rerouted past the counter or away from it, for example by roadworks. | medium | low |
| 10 | **Weather fits (loop two):** the city's daily weather data covers the same days as the counts and can say whether a day was dry at every site. | medium | medium |
