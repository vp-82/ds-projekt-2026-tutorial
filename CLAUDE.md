# Working rules

## Workflow
- Plan before changing files, and wait for my go. (I decide what changes.)
- One package per pull request: one purpose, under about 200 changed lines; propose a split when larger. (Small PRs stay reviewable.)
- Never commit to main; work on a branch, and commit and push only when I say so. (main holds reviewed work only.)
- After a pull request is merged, switch to main and pull before starting anything new. (New work starts from reviewed main.)
- An @claude comment from me on a pull request counts as my go to commit and push to that pull request's branch. (The comment is the go.)

## Pipeline
- Only the download step writes to data/raw, with one manifest line per download. (Raw data stays traceable.)
- Every step prints one line, skips when its output exists and rebuilds with --force. (Reruns are cheap and visible.)
- Logic lives in functions that take a table and return a table. (Testable without files.)

## Tests
- Tests run on fixtures in tests/fixtures and never read data/. (Fast and independent of downloads.)
- Fixtures and expected values are mine: do not change them, and tell me when code and fixture disagree. (They are the specification.)

## Notebooks
- Notebook cells you create have visible code. (I read what ran.)

## Documentation
- Decisions, hypotheses and AI use go into docs/log.md, in the form of the entries already there. (One traceable record.)
- Where I have not decided something, ask or mark it as open; do not fill the gap. (Gaps stay visible.)
