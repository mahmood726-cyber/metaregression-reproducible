# Runner contract and observed release results

Run RUN_PLAN.cmd from the archive root in Windows cmd. It stops at the first
nonzero exit code. The run dated 2026-10-21 on allmeta v1.8.0
1cb3f8409c7af75ed41f7e1811f9c502f900fc79 passed these gates; see
provenance/run_plan-2026-10-21-release.log. The protocol expectations below
are preserved unchanged; the observed-results table separates the measured run.

Prerequisites: Python packages in analysis/requirements.txt; Node supporting
--test-isolation=none; desktop R 4.6.0 with metafor 5.2.1, metadat 1.6.0,
jsonlite 2.0.0 and digest; Edge and Playwright; linkedom for the extras DOM tests.
No clubSandwich dependency is used here. The runner consumes environment
variables supplied by the caller; it installs nothing and fails preflight if
a required executable, package or module is absent.
Port 127.0.0.1:8000 must be free during browser steps.

| Label / command | Expected result |
|---|---|
| Archive working directory, environment, dependency resolution | Exit 0; use this archive, supplied R libraries, Playwright and linkedom |
| Verify prepared integrity: python analysis/recut_integrity.py verify | Exact source/app inventories, original evidence unchanged, all upstream extras hashes and four pinned JSONs match |
| Preserve prior outputs: python analysis/preserve_recut_attempt.py | Existing outputs, recut scratch stage and pytest base directory renamed into .validate-work/previous/ as NAME.prev-N; no prior outputs deleted |
| Prepare clean stage: python analysis/recut.py prepare | Fresh stage, generated path-only browser wrappers, no original evidence overwritten |
| Fresh original browser: python analysis/recut.py original | 1,742 newly recorded configurations; no resumed journal |
| Original replay gate: python analysis/recut.py compare-original | 1,742/1,742 extracted records identical; 129,867/129,903 primary checks, same 36 documented differences and zero unexpected; experimental LS 82,680/91,515 separately |
| Original UI: python analysis/recut.py ui | 4/4 contracts: k=3, k=4, refusal cache clearing and no page errors |
| Fresh original R: python bench/launch.py outputs/recut/validate_R.log Rscript validate.R | 129867/129903 checks pass; 36 documented, 0 unexpected. All 1,742 primary fits and 365 exact tests recomputed. Experimental LS is separate; timeouts may change its denominator, so no new LS count is prescribed |
| Extras numeric: python analysis/recut.py numeric | 52,573/52,573; 194 configurations, zero failures |
| Extras DOM/negative probes: python analysis/recut.py dom | All 5 Node tests pass; 52,573 positive numeric, 104,952 negative numeric, 356 positive DOM, 251 negative DOM, 162 positive plot-value and 4 negative plot-value probes. Three documented divergence designs have 874/874 gate-disabled comparisons, outside the panel denominator |
| Extras browser: python analysis/recut.py browser | 52,767/52,767; zero failures, input/result state restored, no page errors or missing resources |
| Historical outputs: python analysis/make_outputs.py | 129867/129903 primary checks; all 40 expected paper values reproduced, including the historical PR #89 commit; no relabelling as fresh release findings |
| Safeguards: python -m pytest -q analysis/test_safeguards.py analysis/test_recut.py | All 51 tests pass, including 3 R-dependent tests unavailable in the preparation sandbox |
| R safeguard plant: python analysis/check_r_guard_plant.py | Helper exits 0 only when the unchanged-table R snippet reaches the target assertion and exits nonzero with "negative test did not reject"; R startup or unrelated errors fail the stage |
| Archive verification: python analysis/verify_archive.py | Historical-evidence PASS; source hashes, app assets, original journals, reproducible outputs, metadata and fresh R table verified |
| Executed replay gates: python analysis/recut_integrity.py verify --executed | Current source-manifest stamp matches the fresh original, numeric and browser results; all expected totals and UI results match |
| Final success message | Execution plan complete; allmeta v1.8.0 1cb3f84 replay gates passed |

The 129,867/129,903 primary result intentionally includes 36 documented failures.
It is not 129,903/129,903. The 52,767 browser count includes the 52,573 numerical
checks and must not be added to it as an independent numerical denominator.

New runner evidence is under outputs/recut/. validate.R also replaces its normal
outputs/validate_R_* reports with the fresh R run. Original results/, expected/,
data/, bench/ and INPUT_SHA256.json remain unchanged.

## Environment variables

Set these in the calling shell when the dependencies are not already resolvable.
No machine-specific defaults are embedded in RUN_PLAN.cmd.

| Variable | Meaning |
|---|---|
| PATH | Existing Python, Node and Rscript executable search path |
| R_BIN | Optional installed R binary directory prepended to PATH |
| R_LIBS_USER | Existing user R library directories, using the platform separator |
| R_LIBS | Additional existing R library directories |
| PLAYWRIGHT_MODULE | Optional path to the installed Playwright module; otherwise require('playwright') |
| LINKEDOM_MODULE | Optional path to linkedom's esm/index.js; otherwise import('linkedom') |
| PW_CHANNEL | Browser channel; defaults to msedge |

The runner sets PYTHONUTF8=1, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and
R_ENVIRON_USER=NUL for repeatability. Python/Node/R dependencies must already
be installed at the required versions.

## Observed release run: 2026-10-21, allmeta 1cb3f84

| Gate | Observed |
|---|---|
| Original equality / primary result | 1,742/1,742; 129,867/129,903; 36 documented, 0 unexpected |
| Original UI | 4/4 |
| Exact permutation record, status and p-value | 365/365 each |
| Extras numeric / browser | 52,573/52,573 and 52,767/52,767 |
| Extras Node suite | 5/5; zero failures |
| Positive / negative numeric probes | 52,573 / 104,952 |
| Positive / negative DOM probes | 356 / 251 |
| Positive / negative plot-value probes | 162 / 4 |
| Safeguards / paper assertions | 51/51 and 40/40 |
| R uncorrupted-table negative-test plant | PASS |
| Historical experimental LS | 82,680/91,515 |
| Fresh experimental LS | 88,194/95,203; outside the primary gate |
| Fresh R runtime | 1,537.890 seconds |

The raw preserved log retains the old runner's final metadata-reminder wording
and historical verifier wording. Those are recorded messages, not current status.

## Exact release blobs and final manifests

Run FINAL_BLOBS.cmd from the containing workspace (or the archive's copy).
It uses COPY_MAP.json and finalize_blobs.py to fetch bytes with Git cat-file
from the pinned release, validates all targets before writing, compares bytes
after writing, prints BLOB PASS with the verified count, then calls:

    python analysis/recut_integrity.py regenerate
    python analysis/recut_integrity.py verify
    python analysis/verify_archive.py

This final manifest verification is distinct from a fresh browser/R rerun.
The preserved release receipts retain the source-manifest digest of that run.
Metadata edits or blob line-ending changes make verify --executed reject those
old receipts. RUN_PLAN.cmd can generate fresh evidence for the final manifest;
never alter old execution stamps to make the freshness check pass.
