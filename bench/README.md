# Historical validation scripts

These are the scripts used by the completed validation, plus original/patched page copies, source documentation and the patch. Raw journals are in `../results/raw/`; the final corpus and exclusions are in `../data/`. The current publication comparison is `../analysis/checks.py`, which adds strict shape, uniqueness and coverage guards to the historical `compare.py`.

Machine paths were replaced by `<LOCAL_PATH>` or `<PLAYWRIGHT_MODULE>` placeholders. Set the latter to an existing Playwright module when intentionally replaying the original browser runner. `launch.py` inherits standard R library environment variables. Historical R scripts use exact `[[..., exact=TRUE]]` field access; their model formulas and numerical settings are preserved. Package-help examples are unmodified source documents.

For a full historical replay, use a new working directory, copy the needed bench scripts and final corpus (`corpus.json`, `corpus.rds`) there, and provide the archived original/patched directories. Run reference.R and permutation.R with the paper versions, then run `node run_app.cjs patched patched-app.jsonl` and `python compare.py patched-app.jsonl results-patched`. The original runner resumes by ID: start from absent journals for an intentionally fresh run. Five permutation journals record the original disjoint batching. Corpus-building scripts require the original package dependencies including meta; rebuilding recipes is separate from refitting the pinned exported corpus.

`Rscript ../validate.R` must instead be run from the archive root as `Rscript validate.R`; it is the maintained single-command primary numerical validation and uses no browser, Python or Node. Its primary and experimental LS refits are fresh, while browser observations are labelled historical replay. refit_worker.R and compare_ls.R are maintained archive helpers, not historical scripts.

Original scripts are evidence, not a claim of strict input validation. Use the maintained archive checks for fail-closed comparisons. `RESULTS.md` preserves historical provenance, not current certification. Internal task/recovery notes are not distributed.
