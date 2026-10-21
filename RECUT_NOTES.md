# v1.1.0 recut and finalization notes

Archive v1.1.0 for paper 8, meta-regression. The release run dated 2026-10-21
on allmeta v1.8.0 1cb3f84 passed the recorded runtime gates. TASK_finalize.md
supplies the release identity and date; provenance/run_plan-2026-10-21-release.log
preserves the observed results. Earlier preparation and re-sync history follows;
the Finalize section records the current changes. Git/Node/R execution remains
with the human-side runner.

## Build and historical identity

- The initial SOURCE_SHA256.json had 554 entries; every recorded file matched
  before editing. Its exact records are preserved in
  validation-original/SOURCE_SHA256-v1.0.0.json.
- The v1.0.0 corpus, original/post-fix browser journals, R references and
  before/after counts live in data/, results/, expected/ and bench/.
  analysis/checks.py performs strict keyed comparisons; analysis/make_outputs.py
  regenerates tables, figures, evidence-linked numbers and the paper report.
- validate.R verifies the six INPUT_SHA256.json files, requires R 4.6.0,
  metafor 5.2.1 and metadat 1.6.0, freshly refits 1,742 primary models and
  365 exact permutation tests, and compares them with historical browser data.
  Experimental LS is separate and may have run-dependent timeouts.
- The original identity is results/provenance.json commit
  e47acf19f13d36feac52fc414d3c9782012155cc (PR #89). Original paper assertions
  also pin that commit; changing it would mislabel historical outputs. Those
  files remain unchanged. Current app identity is RECUT_PROVENANCE.json.
- The initial pre-release source d04b0a9 was replaced by release commit
  1cb3f8409c7af75ed41f7e1811f9c502f900fc79. Both local HEAD and the
  v1.8.0 tag record that exact commit; the Git executable cannot start here.
- No existing Python manifest-regeneration command was present: the original
  verifier only compared inventories. analysis/recut_integrity.py now supplies
  deterministic regeneration and verification. Original INPUT_SHA256.json and
  all upstream extras pins remain untouched.

## App dependency resolution

All 27 pre-existing app assets were copied from matching initial source paths.
The resulting inventory has 167 files: 27 changed existing files, 140 additions,
and no removals. Copy differences include initial checkout line endings;
Final release copies are checked against Git blobs by FINAL_BLOBS.cmd.

The dependency crawl parsed index.html script/link attributes, literal
import/fetch paths, new URL expressions in recursively loaded shared JS and
CSS url expressions. Dynamic cases were resolved from inspected source:

- tooltips.js language selection: all four glossary JSONs;
- plot-export.js: hub/shared/vendor/jspdf.min.js;
- plus-pins.js and MANIFEST-plus.json: all four hash-pinned extras JSONs;
- alm-validate.js: lazy webr-runner.js;
- webr-runner.js: local webR 0.5.5 loader, worker, WASM, R library data,
  shared libraries, lazy VFS files, and the metafor package dependency closure
  resolved from repo/manifest.json. Package archives were checked against
  their recorded hashes and byte sizes before copying.

RECUT_PROVENANCE.json contains the resolved dependency edges and per-app-file
old/new hashes. Browser devtools source maps, unrelated packages, webR tests
and backup files are not runtime dependencies and were not copied.
The original inline build stamp is preserved as source bytes, not treated as
the final allmeta release identity. The live webR metafor version is 4.8-0;
the extras desktop reference is 5.2-1. These scopes are documented separately.

## Extras and execution

The entire 27-file upstream validate/ directory is preserved in validation-plus/.
This includes contract.js, reference.R and DOM/numeric helpers without 'plus'
in their names. UPSTREAM_SHA256.json verifies exact copies. The copied
README-plus.md and evidence logs describe the upstream PR run only.

analysis/recut.py creates a clean disposable app/validate layout for those
unmodified scripts. It derives browser wrappers from the unchanged historical
bench runners, changing only resource/module paths, output paths, browser
selection and cleanup. The page.evaluate extraction body is preserved.
Original fresh results are stored separately and must match every archived
post-fix record before the original R command can be interpreted as release
validation. The same original comparator and tolerances then apply.

RUN_PLAN.cmd now consumes documented environment variables and uses existing
Playwright and linkedom modules, preflights dependencies, executes all required
replays and checks, and exits on failure. RUN_PLAN_EXPECTED.md distinguishes
preserved expected counts from the measured release results. Servers bind to 127.0.0.1:8000 and each
wrapper closes its own server/browser. No install, commit, push or deploy occurs.

Optional full extras R regeneration is confined to the disposable stage.
The original upstream pin-plus.mjs is preserved but never run on archived
references to absorb a discrepancy. Current-stage input hashes must still
match the archive before standard replays.

## Verification and limits

Local completed checks:

- 48 Python safeguards passed; 3 R-dependent tests were deselected because
  TASK.md prohibits starting R in this sandbox. Test assertions were unchanged.
  A preparation-only tmp_path fixture uses inherited workspace permissions
  because pytest's default Windows 0o700 directory was inaccessible to the
  sandbox. Unrelated pytest plugin auto-loading was disabled.
- Strict recomparison of historical evidence reproduced 129,867/129,903
  primary checks with precisely the same 36 documented differences.
- The existing historical R table passed arithmetic, exact coverage,
  tolerances and app-value checks. This was not a fresh R run.
- 520 protected original source/evidence files and all six original input
  hashes matched their baseline.
- All 167 app assets and 27 upstream extras copies matched the supplied
  initial source. The four extras JSON hashes/byte sizes, 194 ordered unique IDs,
  52,573 flattened numerical checks and 52,767 panel coverage matched.
- The preparation text scan checked only selected source extensions. Finalize
  extends the privacy review to every publishable file, including logs and
  binary assets, and removes machine-specific runner defaults.

Final manifest and wrapper-preparation results are recorded by the local
verification commands and outputs/recut/preparation-pytest.log. The later
release log records successful Node/browser, R, extras, figure regeneration
and full archive verification. Native-library limitations in the preparation
sandbox remain described in STUCK_FAILURES.md. No numerical result
was synthesized, no model/tolerance changed, and no failed runtime was re-pinned.

The original verifier imports plotting/image dependencies only inside the
functions that use them, allowing its independent safeguards to run locally.
Metadata checks now require 1.1.0, the requested release date and the added
allmeta v1.8.0 relation. Creators/authors are unchanged.

The release commit, DOI and runner results are now recorded. Initial environment
observations below remain historical: Playwright reported 1.59.1, whereas
upstream PR notes reported 1.64. The release runner explicitly preflighted its
installed browser and libraries; no version equivalence was inferred.

## Resolved release fields and retained notation

Release commit: 1cb3f8409c7af75ed41f7e1811f9c502f900fc79.
Release DOI: 10.5281/zenodo.23515177; concept DOI: 10.5281/zenodo.20516880.
Extras numerical count: 52,573; browser-panel count: 52,767.
All release metadata placeholders were replaced from TASK_finalize.md and
the release log. Historical redaction markers and documented command metavariables
are listed in the Finalize scan; they are not missing release identifiers.

| Content | Static or dynamic | Evidence / transformation |
|---|---|---|
| Model settings and tolerances | Static preserved protocol | Unchanged original scripts and extras manifest |
| Expected counts | Static assertions | APP.txt, original expected files, upstream extras manifest |
| Study/configuration values | Recorded package evidence | Unchanged corpora and R references |
| Initial app/extras | Recorded source bytes | Matching relative paths in supplied initial source |
| File inventories/hashes | Dynamic | Python SHA-256 and exact inventories |
| Release execution results | Observed 2026-10-21 | Preserved release log |
| Release SHA/DOI | Supplied provenance | TASK_finalize.md; commit cross-checked to local tag/HEAD |

## Files added or changed

All paths below are relative to archive/. No original source file was removed.
Local outputs, disposable stage and ignored recovery file are listed separately.

| Change | Path | Reason |
|---|---|---|
| Changed | .gitignore | Ignore local module dependencies and new runner outputs. |
| Changed | .zenodo.json | Version 1.1.0, release-run description and added release relation. |
| Added | analysis/recut.py | Stage/path wrappers; fresh original equality gate; extras replay commands. |
| Added | analysis/recut_browser.cjs | Run actual app extras panel and verify counts, state restoration and resource errors. |
| Added | analysis/recut_integrity.py | Deterministic regeneration and preservation/copy/pin checks. |
| Added | analysis/recut_preflight.py | Human-runner dependency and executable preflight. |
| Added | analysis/test_recut.py | Preservation and fail-closed integration/negative checks. |
| Changed | analysis/verify_archive.py | Current metadata/app inventory; lazy optional imports; preserved scientific checks. |
| Changed | app/app-sha256.json | Exact inventory and SHA-256 of copied initial assets. |
| Changed | app/hub/app-style.css | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/a11y-landmarks.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/hub/shared/analysis-lifecycle.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/axis-controls.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/csv-upload.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/glossary.ar.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/glossary.es.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/glossary.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/glossary.zh.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/hub/shared/plot-export.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/reset-undo.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/results-export.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/tooltips.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/hub/shared/url-state.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/hub/shared/vendor/jspdf.min.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/meta-regression/index.html | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/plus-engine.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/plus-ui.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/plus.css | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/contract.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus/candidates.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus/corpus.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus/divergences.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus/reference.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus-adapter.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/meta-regression/validate/plus-pins.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/library.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/library.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/libRblas.so | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/libRlapack.so | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/lattice/lattice_0.22-9.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/mathjaxr/mathjaxr_2.0-0.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/nlme/nlme_3.1-169.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/packages/pbapply/pbapply_1.7-4.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/R.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/R.wasm | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/repo/manifest.json | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-BoldItalic.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-BoldItalic.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Italic.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/gdal.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/gdal.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/proj.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/proj.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/udunits.data.gz | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/udunits.js.metadata | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/3830d5c3ddfd5cd38a049b759396e72e-le32d8.cache-9 | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/CACHEDIR.TAG | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/webr-worker.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/r-shiny/shinylive/webr/webr.mjs | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/shared/alm-validate.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/app-flow.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/autosave.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/build-info.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/canonical-datasets.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/citation.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/forced-colors.css | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/hero-examples.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/location-scale.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/ma-core.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/ma-studies-v1.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/permutest.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/toast.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/truthcert-export.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | app/shared/truthcert-ui.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Added | app/shared/webr-runner.js | Initial app dependency; exact source bytes (see provenance hashes). |
| Changed | CHANGELOG.md | Prepared 1.1.0 entry. |
| Changed | CITATION.cff | Version/date and added release reference; unchanged people. |
| Changed | README.md | Recut scope, historical distinction, release IDs and commands. |
| Added | RECUT_NOTES.md | This build, verification, scope and complete change inventory. |
| Added | RECUT_PROVENANCE.json | Initial source identity, resolved release IDs, asset changes and dependency graph. |
| Added | RUN_PLAN.cmd | Fail-closed Windows human-side execution commands and supplied environment. |
| Added | RUN_PLAN_EXPECTED.md | Expected result for each runner command; no unobserved pass claims. |
| Added | STUCK_FAILURES.md | Explicit preparation-environment blockers. |
| Added | validation-original/SOURCE_SHA256-v1.0.0.json | Retain the original source inventory before recut. |
| Added | validation-plus/baseline-dom.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/baseline.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/check-live-script.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/check-numeric.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/contract.js | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/dom-harness.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/generate-plus.R | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/inspect.R | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/MANIFEST-plus.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/numeric.test.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/pin-plus.mjs | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/after-dom.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/baseline-dom.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/candidates.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/corpus.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/divergences.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/generator.log | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/inventory.log | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/live-protocol.log | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/live-protocol.R | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/numeric-evidence.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/reference.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus/test-evidence.json | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus-adapter.js | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/plus-pins.js | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/README-plus.md | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/README.md | Archive-specific scope, versions, staging and rerun instructions. |
| Added | validation-plus/reference.R | Unmodified initial extras validation/support/evidence copy. |
| Added | validation-plus/UPSTREAM_SHA256.json | Pin all unmodified upstream validation support/evidence files. |
| Changed | SOURCE_SHA256.json | Regenerated exact source inventory, excluding itself and local outputs/caches. |

Removed app/source files: **none**.

Local verification/recovery: PROGRESS.md (ignored), outputs/recut/preparation-pytest.log,
outputs/recut/preparation_checks.json and outputs/recut/stage.json; generated
.validate-work/recut wrappers/app stage and preparation test directories are
excluded from source integrity. No .git contents were edited. No allmeta files
were edited. Portfolio index/workbook were read as required but not changed;
this task does not change project/submission/release status.


## Disclosed change to a historically pinned file: analysis/test_safeguards.py

On Windows, Rscript 4.6.0 crashes (exit 0xC0000005) when `-e` code contains literal newlines. The original `test_r_guards` passed its multiline R code with `Rscript -e`, so it could not run on the re-run hosts. In v1.1.0 only the transport changed: the same R code is written to a temporary UTF-8 `.R` file and run with `Rscript <file>`; the R code and every assertion are byte-for-byte unchanged (see FIX_RCALL.md). Because of this, `analysis/test_safeguards.py` was added to EDITABLE in `analysis/recut_integrity.py`. The historical v1.0.0 manifest still records the original hash and was not rewritten.


## Re-sync to allmeta v1.8.0 (1cb3f84)

Source: supplied allmeta checkout, identified by TASK_resync.md as
1cb3f8409c7af75ed41f7e1811f9c502f900fc79. Git cannot start here; this identity
is task-supplied, not a local Git verification. All 167 app assets and all
27 upstream extras files were compared byte-for-byte. Five app assets differed;
all five were recopied as raw bytes. No assets were added or removed. All
app-specific files and all extras are unchanged from the previous preparation.

| Archive path | SHA-256 before -> after | Why |
|---|---|---|
| app/shared/alm-validate.js | 3de6a685c77fa26d68ae39b1da9619c5ada49fd22ef5170237268e1401a09fb7 -> b451c1377164842466aa0d7ad4cb6dd7a1340456a61e891a01646b4375c4ed87 | Avoid duplicate R version prefix in live-validation display. |
| app/shared/build-info.js | f75a435e283d007883ce8fb2f66da7a1cf6132cd5a391a57419b137a69c9c238 -> 44c8a7d1e2cdad4d4b1c4806cffdd4f9817dc39161cd0de5374761a71bd19177 | Copy upstream v1.8.0 version/build stamp exactly. |
| app/shared/canonical-datasets.js | 24bfdb32183dd76ddfc18e02e16292156b4e47e899f3a1c48fb1ba62f963ab28 -> 32f5b35faff14429602f95a72d79ddc8b6864098e94c652a81cd537579770aca | Add effect/SE/label formatter; dataset rows unchanged. |
| app/shared/hero-examples.js | 624a76d249eb39f7fe6b1eaef2d82c60e7ee31b0ad456eff2c8292021d6bd3a5 -> 7b091e4f08184b069b9c649a2cf04f19f440c37bd2de86d49d453f16791307f3 | Add effect-se-label BCG adapter; forest adapter unchanged. |
| app/hub/shared/results-export.js | 8fd30b46fc6e0d09b98326f69edf14757659dbcf2cf1434ca8c5de60c057cc71 -> 16ffa76bc74275565214c2e142d7f0d0847a5a8eded2614efb04aa172acd71f4 | CSS export-bar wrapping and maximum width. |

The page's script/link attributes and recursive JS import/fetch/new URL and
CSS url paths were re-parsed. All 167 resolved dependency assets are present;
no unresolved literal local paths or missing assets were found. Dynamic
glossaries, pinned extras, PDF exporter and webR paths remain covered. The
nine-package metafor dependency closure was resolved from the current webR
manifest and each archive's SHA-256 and byte size checked. The existing
dependency inventory is unchanged. shared/stats-qt.js is neither copied nor
loaded by this app; its upstream accuracy change does not enter this archive.

Potential numerical impact: canonical-datasets.js adds an effect/SE formatter
using sqrt(vi) rounded to four decimals, and hero-examples.js exposes it through
the new effect-se-label adapter. Those two files can affect example-generated
inputs when that adapter is selected. This page still selects forest; its BCG
rows and numerical engines are byte-identical to the prior preparation.
The other three diffs concern CSS, a display label and build metadata. No
validated-number change was identified by source inspection. The runner's
fresh replays decide whether any validated number changes; no count, reference,
expected value or tolerance was relaxed.

The copied build-info.js reports version v1.8.0 but embeds build SHA
42a94da2110a02200d0b5bff4c56f636b9cbffa9 and builtAt 2026-10-20T20:32:27Z.
That embedded stamp is preserved verbatim and is not the supplied release
commit identity. The release commit and DOI were subsequently supplied in
TASK_finalize.md and are now filled in. The previous app_changes/candidate_commit provenance
records remain historical; the new resync record describes this transition.

### ADDENDUM safeguard correction and runner changes

Only the requested assignment in analysis/test_safeguards.py was changed:

- Line 92, old: `tab[['index',exact=TRUE]][1]<-99;reject(check_documented(tab,pins))`
- New: `tab$index[1]<-99;reject(check_documented(tab,pins))`
- Reason: data-frame replacement does not accept exact; preserve the index-corruption rejection test. Every other test-file byte is unchanged.


RUN_PLAN.cmd now invokes analysis/check_r_guard_plant.py immediately after the
pytest stage. It extracts the actual embedded R snippet using Python's AST,
removes only the corruption assignment, marks entry to the retained reject
call, and requires a nonzero R exit with "negative test did not reject".
A successful R exit, an early/startup/unrelated error, or reaching the original
PASS marker makes the helper fail. The generated R script and diagnostic log
are saved under outputs/recut/. This proves the negative test can fail on an
uncorrupted table when the human-side runner executes it.

Before preparing the stage, RUN_PLAN.cmd invokes
analysis/preserve_recut_attempt.py. Existing outputs/, .validate-work/recut/
and .verify-pytest/ are renamed into .validate-work/previous/ using names
outputs.prev-<attempt>, recut.prev-<attempt>, and .verify-pytest.prev-<attempt>.
The first unused common attempt number is selected. Resolved source and
destination paths must remain inside the archive; no outputs are deleted.
The previous-attempt directory is already excluded by the .validate-work/
manifest and ignore rules. All original runner commands, environment lines,
order, expected counts and failure gates are otherwise unchanged.

Added archive-local helpers (not upstream copies):

| Path | SHA-256 before -> after | Why |
|---|---|---|
| analysis/check_r_guard_plant.py | absent -> 578c8f3df388ca10cdc9f0170a9e016be26022dacca12e7a92bcac287d2cb499 | ADDENDUM negative-test plant check without editing the source R validation. |
| analysis/preserve_recut_attempt.py | absent -> f8aa870398108ea77a27c07b193f264c0b8a4715f095a91e73fd9446d1949fa1 | Preserve prior runner outputs and scratch folders on repeated runs. |


Other archive-local updates: RECUT_PROVENANCE.json records the supplied release
source and before/after copy hashes; RUN_PLAN_EXPECTED.md adds only expectations
for the two new stages; this section records the re-sync. app/app-sha256.json
and SOURCE_SHA256.json are regenerated by analysis/recut_integrity.py. No
upstream extras hash or original input pin needed regeneration.

Local preservation checks pass for 519 non-editable original files and all six
original R input pins. The separate exact-diff check confirms the safeguard
test changed only as directed. All 27 extras files and their expected counts,
references and tolerances remain unchanged. All 167 app files match the current
supplied release bytes, including identical files not recopied.

Python-only helper checks passed: the plant result evaluator accepts only the
intended failure pattern, and two isolated repeated rename attempts preserved
all six old output folders and their contents. These are harness unit checks,
not an R plant-check execution. Full Node/browser, R, R plant, figures and
executed-manifest gates subsequently passed in the release RUN_PLAN.cmd run.
That run's receipts retain their original manifest stamp; final metadata edits
do not make them evidence of a new execution. Available Python safeguards and manifest verification are recorded
in the local preparation logs and PROGRESS.md.

| Content | Static or dynamic | Evidence / transformation |
|---|---|---|
| Original corpus/R references/expected values/tolerances | Static preserved | Baseline hashes and six original input pins |
| Extras counts and references | Static preserved | Unchanged upstream manifest and all 27 copied files |
| Release app bytes and dependency inventory | Dynamic comparison | Current allmeta paths, SHA-256 and recursive path parsing |
| Helper and integrity checks | Dynamic local checks | Python guards and archive manifest script |
| Release numerical/browser/R verdicts | Observed PASS | Preserved release log; expected counts unchanged |
| Final SHA/DOI metadata | Supplied release provenance | 1cb3f8409c7af75ed41f7e1811f9c502f900fc79; 10.5281/zenodo.23515177 |

Final local verification: 48 Python safeguards passed; 3 R-dependent tests
were deselected as required by the sandbox task. Archive integrity verification
against ../allmeta passed; source text-safety checks passed. Evidence:
outputs/recut/resync-pytest.log and outputs/recut/resync-checks.json. The R plant
check subsequently passed in the recorded release run.

RUN_PLAN.cmd: the R_LIBS_USER / R_LIBS lines now use `if not defined ...` so the runner on [REDACTED HOST] can supply its library paths (same package versions: metafor 5.2-1, meta 8.5-0, clubSandwich 0.7.0, jsonlite 2.0.0). Coordinator, 2026-10-21.

## Finalize

Finalized release metadata for 1.1.0, dated 2026-10-21, using allmeta v1.8.0
1cb3f8409c7af75ed41f7e1811f9c502f900fc79 and DOI 10.5281/zenodo.23515177.
Creators and author order are unchanged. The concept DOI is recorded as
10.5281/zenodo.20516880. The local release tag and HEAD independently match
the supplied full commit.

### Observed release results and README corrections

Source: provenance/run_plan-2026-10-21-release.log, copied from the supplied
archive/../run_plan.log. The date is supplied by TASK_provfix.md because the
log has no independent wall-clock timestamp. No count is inferred from an
earlier preparation log.

| Measure | Release-log result |
|---|---|
| Original equality | 1,742/1,742 |
| Original primary, browser replay and fresh R | 129,867/129,903; 36 documented, 0 unexpected |
| UI contracts | 4/4 |
| Exact permutation record/status/p-value | 365/365 in each group |
| Extras numerical; configurations | 52,573/52,573; 194 |
| Extras browser panel | 52,767/52,767 |
| Extras Node tests | 5/5 |
| Positive/negative numerical probes | 52,573/104,952 |
| Positive/negative DOM probes | 356/251 |
| Positive/negative plot-value probes | 162/4 |
| Safeguards; paper-value assertions | 51/51; 40/40 |
| R safeguard plant | PASS |
| Historical experimental LS | 82,680/91,515 |
| Fresh experimental LS | 88,194/95,203 |
| Fresh LS alpha coefficients | 1,898/3,284 |
| Fresh R elapsed seconds | 1,537.890 |

README correction: the obsolete earlier fresh LS result 82,672/89,671 is
replaced by the observed release result 88,194/95,203. Its earlier 92-refusal
and one-additional-timeout narrative is removed because the release log does
not provide that aggregate or narrative. The historical 82,680/91,515 and
historical alpha-coefficient 1,893/3,280 results retain their historical labels.
Primary/extras counts did not change. No original corpus, reference, expected
value, tolerance, or numerical test was changed. Browser-panel totals overlap
numerical totals and are not summed.

README, RUN_PLAN_EXPECTED and validation-plus/README now describe the completed
release run. CITATION.cff, .zenodo.json, CHANGELOG and RECUT_PROVENANCE carry
the supplied identifiers. The original metadata reminder at the end of the
raw runner log remains verbatim evidence of what that runner printed.

RUN_PLAN.cmd now takes R_BIN, R_LIBS_USER, R_LIBS, PLAYWRIGHT_MODULE and
LINKEDOM_MODULE from the calling environment, with defaults only for msedge
and deterministic runner flags. RUN_PLAN_EXPECTED documents their semantics.
The old hardcoded install locations and unrelated package comments were removed.

Release JSON receipts were copied into provenance/ without changing their
source-manifest stamps. Final manifest regeneration does not certify a fresh
execution. The existing --executed gate remains strict and will reject old
stamps after source changes. A new RUN_PLAN.cmd execution creates new receipts.

| Content | Static or dynamic | Evidence / transformation |
|---|---|---|
| Release date and DOI | Supplied provenance | TASK_finalize.md; no date inferred from file modification time |
| Release commit | Supplied and cross-checked | Task, local HEAD and v1.8.0 tag |
| Observed counts | Recorded dynamic execution | Preserved release log and JSON receipts |
| Protocol/expected values/tolerances | Static, preserved | Original and extras pins |
| Current inventories | Dynamic integrity checks | Archive manifest regeneration/verification |
| Exact blob equality | Human-runner check | COPY_MAP.json and FINAL_BLOBS.cmd |

### Privacy scan: findings and actions

The scan covered every existing publishable archive file, including tracked
outputs and otherwise unignored additions. Git index v2 was read without
invoking Git or modifying its metadata. The exact root .gitignore rules were
applied to untracked paths; ignored scratch, module dependencies, caches and
PROGRESS.md were excluded. Nested ignore files are absent. All file bytes,
including binary assets, were scanned; compressed payloads were not unpacked.
The final pre-report scan covered 763 files. Patterns included local
home/install paths, supplied account/host indicators, email shapes and credential
prefixes. Raw-byte coincidences in binary files were inspected separately from
actual contacts, runtime filesystem paths and credential material.

The release log itself contained none of those sensitive patterns, so its
preserved copy is byte-identical to the supplied log. RUN_PLAN.cmd installation
defaults were removed, and the coordinator hostname was redacted from these
notes. The following table uses **pre-finalization line numbers** so a reviewer
can locate every initial hit; repeated hits on the same line are counted.
Sensitive values are not reproduced in the audit table.

**Publication remains blocked on the requested redaction/identity decision.**
The three upstream extras logs contain real local installation paths. They
are among the 194 exact copies and have upstream SHA-256 pins. Public author
email addresses also occur in protected package documentation and vendor/runtime
files. Removing those bytes conflicts with the task's exact-copy requirement
and original-evidence preservation. No such content was silently changed and
no upstream or historical pin was weakened. The requested decision is to
sanitize local logs as explicit derived copies and retain public attribution
and virtual runtime paths, or authorize broader departures from byte identity.

Generic runtime labels, public X.509 trust certificates, ordinary words or
filenames matching a short credential prefix, and random binary coincidences
are not credentials. No private-key block or actual access token was identified.
This classification does not waive the unresolved blanket email/path instruction.

| File:line (before edit) | Category / occurrences | Finding and action |
|---|---|---|
| .zenodo.json:24 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| CHANGELOG.md:10 | placeholder; 2 | Release identifier/count field; resolved from task or release log. |
| CITATION.cff:33 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| CITATION.cff:34 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| README.md:10 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| README.md:11 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_NOTES.md:127 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_NOTES.md:130 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_NOTES.md:132 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_NOTES.md:135 | placeholder; 2 | Historical command/filename notation; retained or rewritten in current instructions. |
| RECUT_NOTES.md:395 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| RECUT_NOTES.md:430 | placeholder; 2 | Release identifier/count field; resolved from task or release log. |
| RECUT_NOTES.md:455 | placeholder; 3 | Historical command/filename notation; retained or rewritten in current instructions. |
| RECUT_NOTES.md:498 | placeholder; 2 | Release identifier/count field; resolved from task or release log. |
| RECUT_PROVENANCE.json:4 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_PROVENANCE.json:5 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RECUT_PROVENANCE.json:1187 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| RUN_PLAN.cmd:12 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:14 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:14 | username; 3 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:16 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:16 | username; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:20 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:20 | username; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:22 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:22 | username; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:26 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:26 | username; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:28 | local_path; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN.cmd:28 | username; 1 | Machine-specific installation/account text; removed; caller environment now supplies paths. |
| RUN_PLAN_EXPECTED.md:19 | placeholder; 2 | Historical command/filename notation; retained or rewritten in current instructions. |
| RUN_PLAN_EXPECTED.md:46 | placeholder; 3 | Release identifier/count field; resolved from task or release log. |
| SOURCE_SHA256.json:444 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| SOURCE_SHA256.json:561 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| analysis/recut.py:34 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| app/hub/shared/vendor/jspdf.min.js:7 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:9 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:10 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:54 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:89 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:112 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:129 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:138 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:163 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:203 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:275 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:335 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/hub/shared/vendor/jspdf.min.js:361 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.js:1823 | local_path; 2 | webR virtual filesystem path; upstream runtime constant, unchanged; explicit exception requested. |
| app/r-shiny/shinylive/webr/R.wasm:29467 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:29476 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/R.wasm:29885 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:30769 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:30770 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:30829 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:30841 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:36544 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:36545 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:36546 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:37320 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:37321 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:38082 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:38083 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:40425 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:41054 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:41055 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:42977 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:42978 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:42979 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:43297 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/R.wasm:43955 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/R.wasm:46793 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:46794 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52327 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52328 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52329 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52330 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52696 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:52697 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:54587 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/R.wasm:57849 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/R.wasm:60136 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:60137 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:60140 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:63801 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:63802 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:64419 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:64420 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:64433 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:64471 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:64474 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:73975 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:73976 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:74005 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:74153 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/R.wasm:79838 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:79839 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:79857 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/R.wasm:81345 | username; 2 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/library.data.gz:2397 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/library.data.gz:44924 | secret_prefix; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz:3169 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz:3630 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz:3003 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz:4740 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz:7775 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz:11206 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz:179 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz:127 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf:5 | local_path; 1 | webR virtual filesystem path; upstream runtime constant, unchanged; explicit exception requested. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:25 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:51 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:82 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:117 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:139 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:161 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:183 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:214 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:236 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:258 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:282 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:299 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:321 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:352 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:372 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:396 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:420 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:441 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:473 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:495 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:518 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:541 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:561 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:581 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:610 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:625 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:647 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:668 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:689 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:720 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:750 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:780 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:802 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:826 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:851 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:881 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:922 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:951 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:980 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1002 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1023 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1053 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1083 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1113 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1135 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1151 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1173 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1189 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1220 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1252 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1284 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1301 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1316 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1346 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1376 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1401 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1420 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1450 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1472 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1493 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1525 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1558 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1576 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1606 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1636 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1656 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1685 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1698 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1712 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1737 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1767 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1799 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1816 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1848 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1865 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1895 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1911 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1940 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:1970 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2004 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2026 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2042 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2063 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2078 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2110 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2126 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2157 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2173 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2202 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2234 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2250 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2267 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2298 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2314 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2344 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2359 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2389 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2421 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2437 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2468 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2499 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2530 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2546 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2579 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2594 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2624 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2639 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2669 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2683 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2713 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2743 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2758 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2773 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2803 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2821 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2839 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2854 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2884 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2913 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2927 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2943 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2973 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:2988 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3004 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3034 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3064 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3080 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3095 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3125 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3156 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3172 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3187 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3202 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3232 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3262 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3278 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3309 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3326 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3356 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3377 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3407 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3422 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3453 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3468 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3498 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem:3529 | secret_prefix; 1 | Public trust-certificate delimiter; retained, no private key. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz:4601 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz:8294 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz:8570 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz:245 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz:64 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz:622 | secret_prefix; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz:5485 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.data.gz:287 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz:8153 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION:5 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf:1262 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf:424 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf:427 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf:1134 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:360 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:363 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:549 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:790 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:904 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:1353 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:1621 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:1624 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf:1628 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf:1367 | placeholder; 2 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf:621 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf:1584 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf:1649 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf:983 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf:1395 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf:2896 | email; 1 | Raw binary pattern coincidence; unchanged. |
| app/r-shiny/shinylive/webr/webr-worker.js:2 | username; 1 | Generic runtime label, not a host account; unchanged. |
| app/r-shiny/shinylive/webr/webr-worker.js:35 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/webr-worker.js:36 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| app/r-shiny/shinylive/webr/webr.mjs:2 | local_path; 1 | webR virtual filesystem path; upstream runtime constant, unchanged; explicit exception requested. |
| bench/README.md:5 | placeholder; 2 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/docs/dat.aloe2013.txt:54 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.anand1999.txt:51 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.anker2025.txt:68 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.assink2016.txt:56 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.axfors2021.txt:44 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bakdash2021.txt:90 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bakdash2021.txt:91 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bakdash2021.txt:92 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bakdash2021.txt:93 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.baker2009.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bangertdrowns2004.txt:58 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bartos2023.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.baskerville2012.txt:64 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bassler2004.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bauer2002.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bcg.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.begg1989.txt:49 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.berkey1998.txt:66 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.besson2016.txt:99 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bonett2010.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bornmann2007.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.bourassa1996.txt:67 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.cannon2006.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.chiarito2020.txt:6 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.chiarito2020.txt:64 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.chiarito2020.txt:70 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.chiarito2020.txt:74 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.cohen1981.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.colditz1994.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.collins1985a.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.collins1985b.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.craft2003.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.crede2010.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.crisafulli2020.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.curtin2002.txt:38 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.curtis1998.txt:86 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.dagostino1998.txt:70 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.damico2009.txt:39 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.debruin2009.txt:53 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.demir2022.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.dogliotti2014.txt:41 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.dong2013.txt:44 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.dorn2007.txt:49 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.dumouchel1994.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.egger2001.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.feng2019.txt:43 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.fine1993.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.franchini2012.txt:51 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.frank2008.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.furukawa2003.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.gibson2002.txt:78 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.graves2010.txt:41 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.greb2008.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.greenland1992.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.gurusamy2011.txt:51 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hackshaw1998.txt:54 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hahn2001.txt:41 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hannum2020.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hart1999.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hartmannboyce2018.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hasselblad1998.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.higgins2008.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.hine1989.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.huber2000.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.ishak2007.txt:64 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.kalaian1996.txt:59 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.karner2014.txt:5 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.karner2014.txt:64 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.karner2014.txt:71 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.karner2014.txt:75 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.kearon1998.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.knapp2017.txt:74 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.konstantopoulos2011.txt:58 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.landenberger2005.txt:66 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.laopaiboon2015.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lau1992.txt:38 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lee2004.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lehmann2018.txt:89 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.li2007.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lim2014.txt:51 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.linde2005.txt:80 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.linde2015.txt:65 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.linde2016.txt:63 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lloyd2010.txt:39 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.lopez2019.txt:75 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.maire2019.txt:55 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.mccurdy2020.txt:89 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.mcdaniel1994.txt:62 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.meeker2017.txt:37 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.michael2013.txt:69 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.molloy2014.txt:32 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/dat.molloy2014.txt:61 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.moore1998.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.moura2021.txt:46 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.nakagawa2007.txt:35 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.nielweise2007.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.nielweise2008.txt:49 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.nissen2007.txt:67 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.normand1999.txt:41 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.obrien2003.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.pagliaro1992.txt:42 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.pignon2000.txt:49 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.poole2003.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.pritz1997.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.quan2000.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.raudenbush1985.txt:78 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.riley2003.txt:49 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.rivera2025.txt:52 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.roever2022.txt:41 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.senn2013.txt:47 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.spooner2002.txt:53 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.steurer2006.txt:45 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.stowe2010.txt:57 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.tannersmith2016.txt:57 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.thompson1999.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.tian2009.txt:52 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.ursino2021.txt:40 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.vanhowe1999.txt:50 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.viechtbauer2021.txt:36 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.white2020.txt:51 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.woods2010.txt:34 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/dat.yusuf1985.txt:48 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/datsearch.txt:94 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/docs/datsearch.txt:99 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/datsearch.txt:100 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/metadat-package.txt:101 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/metadat-package.txt:102 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/metadat-package.txt:103 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/metadat-package.txt:104 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/metadat-package.txt:105 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/docs/prep_dat.txt:32 | email; 1 | Public upstream author/maintainer contact; unchanged pending blanket-redaction/identity decision. |
| bench/original/shared/alm-task.css:37 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/alm-task.css:41 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/alm-task.css:42 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/benefit-risk-v1.js:1 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/evalue.js:4 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/glossary.js:52 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/ma-methods-v1.js:70 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/protocol-schema.js:92 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/original/shared/report-bundle.js:14 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:8 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:9 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:10 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:11 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:13 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:28 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:29 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/revman-reader.js:238 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/original/shared/rob-core.js:1 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/alm-task.css:37 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/alm-task.css:41 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/alm-task.css:42 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/benefit-risk-v1.js:1 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/evalue.js:4 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/glossary.js:52 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/ma-methods-v1.js:70 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/protocol-schema.js:92 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/patched/shared/report-bundle.js:14 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:8 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:9 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:10 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:11 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:13 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:28 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:29 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/revman-reader.js:238 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/patched/shared/rob-core.js:1 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| bench/run_app.cjs:2 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| bench/test_ui.cjs:2 | placeholder; 1 | Historical redaction marker, command metavariable or XML syntax; preserved. |
| outputs/validate_R_fresh.rds:18226 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| outputs/validate_R_fresh.rds:28172 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| outputs/validate_R_fresh.rds:29955 | placeholder; 1 | Upstream runtime marker or binary coincidence; preserved, not release metadata. |
| validation-original/SOURCE_SHA256-v1.0.0.json:297 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| validation-original/SOURCE_SHA256-v1.0.0.json:414 | secret_prefix; 1 | Short prefix inside ordinary text or filenames; inspected, not a credential; unchanged. |
| validation-plus/README.md:14 | placeholder; 1 | Release identifier/count field; resolved from task or release log. |
| validation-plus/plus/generator.log:3 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:3 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:12 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:12 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:13 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:13 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:14 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/generator.log:14 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:3 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:3 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:12 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:12 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:13 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:13 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:14 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:14 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:27 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:27 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:28 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:28 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:29 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:29 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:30 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:30 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:31 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:31 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:32 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/inventory.log:32 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:3 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:3 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:12 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:12 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:13 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:13 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:14 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:14 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:17 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:17 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:18 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:18 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:19 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:19 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:22 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:22 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:23 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:23 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:24 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:24 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:27 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:27 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:28 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:28 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:29 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:29 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:32 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:32 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:33 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:33 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:34 | local_path; 1 | Local installation path in pinned upstream log; unresolved redaction/byte-identity conflict. |
| validation-plus/plus/live-protocol.log:34 | username; 1 | Local account component in pinned upstream log; unresolved redaction/byte-identity conflict. |
| RECUT_NOTES.md:506 | hostname; 1 | Coordinator machine name; replaced with a redaction marker. |

### Other angle-bracket notation

The full documentation review also found executable/library metavariables in
validation-plus/README-plus.md:189, 190, 192 and 206; these are upstream example
instructions and are not unknown results. Historical bench redaction/module
markers, the report filename date template, XML element names, runtime missing
value markers and binary coincidences remain listed above. Release SHA, DOI
and extras-count placeholders are all resolved.

### Copy map and deterministic Git-blob handoff

COPY_MAP.json lists 167 current app assets and 27 upstream extras files (194
destinations). Historical bench/original and bench/patched snapshots are
preserved evidence from earlier commits; they are deliberately not replaced
by v1.8.0. The workspace and archive map copies are byte-identical.

FINAL_BLOBS.cmd invokes the Python helper, which checks the full commit and
v1.8.0 tag, validates the complete map and destination confinement, reads each
Git blob through subprocess byte pipes, verifies its Git object digest, and
allows only checkout line-ending differences. Every entry passes preflight
before any destination is written. It prints BLOB PASS with the exact verified
count, then regenerates and verifies manifests with the archive's own scripts.
Semantic changes, missing sources, unsafe/duplicate targets and digest failures
stop the command. The helper is also shipped in archive/analysis with an
archive-root command so the published archive carries its finalization tooling.

All 194 upstream files still match the pre-finalization bytes. Git-blob
materialization has not been executed in this Python-only sandbox. Resolving
the privacy conflict may require documented redacted derivatives and associated
map/integrity adjustments before the human runner uses this handoff.

### Unresolved archive v1.0.0 DOI

The archive's own v1.0.0 DOI was not supplied and was not found in local
metadata or the public GitHub v1.0.0 README, CITATION, Zenodo metadata or release
description. Existing relation 10.5281/zenodo.23288388 identifies allmeta
v1.2.1; it is retained and is not relabelled as this archive's v1.0.0 DOI.
The user was asked for the missing archive DOI. No identifier was invented.

Checked public source records:
- https://github.com/mahmood726-cyber/metaregression-reproducible/blob/v1.0.0/.zenodo.json
- https://github.com/mahmood726-cyber/metaregression-reproducible/blob/v1.0.0/README.md
- https://github.com/mahmood726-cyber/metaregression-reproducible/releases/tag/v1.0.0

### Finalization verification

- Python safeguards and blob-helper regression tests: **64 passed**, with the
  **3 R-dependent safeguards deselected** by the sandbox-only harness.
- Existing integrity regeneration and verification: PASS; 167 app assets,
  519 protected original files unchanged, all original input and extras pins.
- Second-pass review: PASS for version/date/creators, supplied commit/DOI,
  tag/HEAD consistency, release-log claims and fresh-R CSV totals, unchanged
  receipt stamps, complete copy map, UTF-8 without BOM and portable runner.
- Full archive verifier: BLOCKED locally at Matplotlib native-extension DLL
  initialization. No test was weakened; FINAL_BLOBS.cmd includes that verifier
  for the human-side runner. The recorded release run previously passed it.
- Current-manifest executed validation: not claimed; original run stamps remain
  unchanged and the strict freshness check is preserved.
- Publication: blocked by the unresolved redaction/identity decision and missing
  archive v1.0.0 DOI. No commit, push, deployment or external registry update.


## Upstream pin correction (coordinator, 2026-10-21)
validation-plus/UPSTREAM_SHA256.json had recorded hashes of CRLF working-tree copies (Windows autocrlf), not of the allmeta files. After the git-blob recopy, 19 entries were re-pinned to the sha256 of the allmeta 1cb3f84 git blob, each only after checking that the archive file is byte-identical to that blob; 8 entries were already correct; 0 could not be checked: [].
- baseline-dom.mjs: 3e40c85bb6dccf94d68a5ed15a9998b6aec73f3225ae4e5b9a5a51ccdb2b1045 -> 80124335f5c3453a2fadba69fe78e6666024d71ffee8963c93d1b5de6cbc10cc
- baseline.mjs: 0aaa6e078c5815cf869528c6dd20f53601274df903a8176db4839663260a9af3 -> 7de1448e8ebedde57b09638c38ba03ed89c31030e2f362573175e5c554b3764d
- check-live-script.mjs: 33ca1ecadb408b50c4fab49041fb0987ea0f812b3a88906e88f35e9e6d634feb -> fa9825fcb5c365ca3bc87d6671db5a2ece9bcaf21b71b00b221417bbc4f9dc53
- check-numeric.mjs: 286ddbcd356445a4cdd3955fa79e8f763b68eae22567b8ac80a77273d0c8d7b8 -> a60ffd6d531bb3ac79c96e9a14fc895d694c7c9894eaeed23bc13d775d970f4a
- contract.js: 603d66b91155cf2fe14964b0a49c9660913d2a02d065b5ea7e170daf9248d227 -> 5bb457e5824ffbc91b8aca4aa648d41b18d78c6e49f681dcf98df6ae4f951a74
- dom-harness.mjs: 3723cc3d1f4b9cb131593a65f0430a16f495dd577676932167b7a09bcd62de71 -> 79e04ae13ef3a80bac5ec5043b860826c67f009651fba0934bd8ef6438329c46
- generate-plus.R: b3aedb8df1f3184cb43548351499bcf3013c3c9ed41f6df1be6e68ed309e5597 -> d395a8c44c5710f5855368cac4e63716b8457ecd35432d8fbd281e8f1ace3108
- inspect.R: 4801d483042c58c93dadc4ca3730c4568f82462db18fcc4e6d3b4fe1cfe4ad82 -> 1c733b9d9852e45b4b080bf982e26d09f9d044e356e6b8fb7cf957892521b4b1
- MANIFEST-plus.json: 536cad0d734616c46251ee72f78846d5f8d233408056a787fa9d08d40298dfc7 -> 56c41acc2d29565e79bdae728e475cd43cc1af9f43ea0c8c583ae04eab953835
- numeric.test.mjs: 331959b2699d107329ea0fe2764d0159d1bc74c29fdd0ad8ff35d8786bd3caef -> 14bb16ffd423cc3c1fbc22c1c5b4678f8dd089816425fed02a994998df7c4148
- pin-plus.mjs: 289b7e1e91fce78bc1739f8870adb3056c41e549e483e43270cbd8f249cc96b1 -> e074933da30fd77a0bdd32b37b1d379f6f5052f4d170391317d41c99a8cfad22
- plus/generator.log: 25c1647df1102a43d659bce4f3bee1c9223628b6f2cc5555a14abfd1a0b3813c -> 9bab5bd0386e53bc3af2b7df4046294b0592bfb32a7711777257b5a3c9291562
- plus/inventory.log: 09a053e2202dcc3df85129b2df28706a4e592a59a1faefedf55e19af8d068662 -> cab553aad6f8c10abdd99ba261e08486494a0d33f2f4fd8d51105964e9364e37
- plus/live-protocol.log: 1743f18e913edc564347a767ba43cbb02a381dd661907a4b216b7c530b2c41b1 -> c3e904eb4d1a8886ad684f266275463501065c62cc038999e092b108aded82c6
- plus/live-protocol.R: f90478678c18604d8e81c864bc436d79e1c6dd0109bbc0b8ecee1f5d8a59443e -> ecd202e64be5335b0640f87e15340e1c25dd49e52333d2e7f4c66d90b169c37b
- plus-adapter.js: dcaecb299ea7169cb44cb395dc5cfef82aac8564b3408f7982d8a90ea7e183ec -> 9122b3ce481a385835883db4a0b266aafd0e524a7a4058d352cb1d5edd3c4c37
- plus-pins.js: 62b0e19d83f8ee87cbef1a72eccf026e47916d3a28032a6b6c864c2fd529f9cd -> 24e0ce97767fc3fc2c60323f660d68fd5d054d20da00856ce7ff5c22a96b61e3
- README-plus.md: 2a850bb179e70d4d134aaeed650621a21308ee12f770abe45dce708a57ab843f -> efe3c9c724c8743bc4ba834550cee03e704fcb25cb0c2fa3b204ad74ca495736
- reference.R: 1db73c17a432c35d858f3d4bad971babd9f809f5799e1d0dda41a6e0404271b8 -> 958e7580f554c90d2d4a86d102adf366e923dde79ae3eefea18036e1525a0c9a

## Provenance fix (2026-10-21)

The final coordinator-designated ../run_plan.log replaces the earlier archived log.
The coordinator reports this execution followed the Git-blob recopy and upstream-pin
correction and completed with RUN_EXIT 0. The log itself ends with the successful
execution-plan message; it has no independent wall-clock timestamp or RUN_EXIT line.

### Dates and provenance

- README.md:3: release date/reference 2026-10-20 -> 2026-10-21.
- README.md:7: release date/reference 2026-10-20 -> 2026-10-21.
- README.md:17: release date/reference 2026-10-20 -> 2026-10-21.
- README.md:102: release date/reference 2026-10-20 -> 2026-10-21.
- README.md:130: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_NOTES.md:3: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_NOTES.md:5: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_NOTES.md:143: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_NOTES.md:503: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_NOTES.md:511: release date/reference 2026-10-20 -> 2026-10-21.
- CHANGELOG.md:3: release date/reference 2026-10-20 -> 2026-10-21.
- .zenodo.json:29: release date/reference 2026-10-20 -> 2026-10-21.
- .zenodo.json:30: release date/reference 2026-10-20 -> 2026-10-21.
- CITATION.cff:9: release date/reference 2026-10-20 -> 2026-10-21.
- RUN_PLAN_EXPECTED.md:4: release date/reference 2026-10-20 -> 2026-10-21.
- RUN_PLAN_EXPECTED.md:6: release date/reference 2026-10-20 -> 2026-10-21.
- RUN_PLAN_EXPECTED.md:64: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_PROVENANCE.json:6: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_PROVENANCE.json:2070: release date/reference 2026-10-20 -> 2026-10-21.
- RECUT_PROVENANCE.json:2073: release date/reference 2026-10-20 -> 2026-10-21.
- STUCK_FAILURES.md:16: release date/reference 2026-10-20 -> 2026-10-21.
- validation-plus/README.md:14: release date/reference 2026-10-20 -> 2026-10-21.
- validation-plus/README.md:17: release date/reference 2026-10-20 -> 2026-10-21.
- validation-plus/README.md:65: release date/reference 2026-10-20 -> 2026-10-21.
- analysis/verify_archive.py:84: release date/reference 2026-10-20 -> 2026-10-21.

- Replaced the old dated provenance log with provenance/run_plan-2026-10-21-release.log and updated its SHA-256.
- Release receipt source-manifest digest: 7d8f93543a8a5be03ce428c6f0aa60c51c1a4591a11ec843c1f9ed2512d19533 -> 517a936b022343e774f44f8d96f8ee85a3e7e111ba9eb862901647aa8f7cd9e2. This is read from the final runtime receipt; no receipt was restamped.
- Preserved the upstream build timestamp and historical event dates.

### Counts checked against the final log

- README.md, RECUT_NOTES.md and RUN_PLAN_EXPECTED.md: fresh R runtime 1,561.780 -> 1,537.890 seconds.
- No quoted release-result count changed: original equality 1,742/1,742; primary 129,867/129,903 with 36 documented and 0 unexpected; UI 4/4; exact permutation 365/365 each; extras numerical 52,573/52,573 across 194 configurations; browser 52,767/52,767; Node suite 5/5; safeguards 51/51; paper assertions 40/40. Probe counts remain 52,573/104,952 numerical, 356/251 DOM and 162/4 plot-value.
- The task P8 note conflicts with the designated log: 82,680/91,515 is historical replay, while the explicit fresh-fit line reports 88,194/95,203 and LS_alpha reports 1,898/3,284. These distinct labels are retained in README, CHANGELOG, Zenodo metadata, runner documentation and these notes. Historical alpha 1,893/3,280 remains historical.
- Expected values, tolerances, corpus, original input pins and upstream pins are unchanged.

### Privacy rescan and unresolved instruction conflict

A fresh raw-byte scan covered all 763 publishable files (422,607,854 bytes before
this edit), including binaries and tracked outputs; Git metadata and ignored
scratch/dependencies were excluded using the existing Python inventory reader.
Compressed payloads were not unpacked. Results: 183 email-shaped matches, 34 local-path
matches, 44 account-word matches and 181 credential-prefix candidates; no hostname
match or actual access token/private key identified. The 64 angle-bracket markers
are existing redaction/notation, not credentials. The new release log has no
sensitive matches and is byte-identical to ../run_plan.log.

The task simultaneously requires redacting publishable files and never changing
pins. Thirty actual local installation paths (and their account components) occur
in three upstream-pinned logs. Contact-address hits also occur in protected original
documentation and upstream libraries. Redacting those would make the unchanged
pins fail verification. Clarification was requested; pending a response, these
protected bytes and pins remain unchanged. This is an incomplete privacy cleanup,
not publication clearance. Generic account words and virtual filesystem paths
are not automatically redacted from executable code. The following lists every
non-placeholder scan group with its pre-edit line numbers; no sensitive value is
reproduced. The earlier Finalize audit contains the detailed classifications.

| File | Category | Hits | Lines | Disposition |
|---|---|---:|---|---|
| RECUT_NOTES.md | secret_prefix | 3 | 388, 1030, 1048 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| SOURCE_SHA256.json | secret_prefix | 2 | 446, 563 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| STUCK_FAILURES.md | username | 2 | 36, 39 | Generic runtime/UI/documentation word; not an identified local account; preserved. |
| app/hub/shared/vendor/jspdf.min.js | email | 13 | 7, 9, 10, 54, 89, 112, 129, 138, 163, 203, 275, 335, 361 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/R.js | local_path | 2 | 1823 | Virtual runtime filesystem or font configuration; not a host account path; preserved. |
| app/r-shiny/shinylive/webr/R.wasm | email | 35 | 29885, 30769, 30770, 36544, 36545, 36546, 37320, 37321, 38082, 38083, 41054, 41055, 42977, 42978, 42979, 46793, 46794, 52327, 52328, 52329, 52330, 52696, 52697, 60136, 60137, 60140, 63801, 63802, 64419, 64420, 73975, 73976, 79838, 79839, 79857 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/R.wasm | username | 11 | 29467, 30829, 30841, 40425, 64433, 64471, 64474, 74005, 74153, 81345 | Generic runtime/UI/documentation word; not an identified local account; preserved. |
| app/r-shiny/shinylive/webr/library.data.gz | secret_prefix | 1 | 44924 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz | email | 1 | 179 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf | local_path | 1 | 5 | Virtual runtime filesystem or font configuration; not a host account path; preserved. |
| app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem | secret_prefix | 146 | 25, 51, 82, 117, 139, 161, 183, 214, 236, 258, 282, 299, 321, 352, 372, 396, 420, 441, 473, 495, 518, 541, 561, 581, 610, 625, 647, 668, 689, 720, 750, 780, 802, 826, 851, 881, 922, 951, 980, 1002, 1023, 1053, 1083, 1113, 1135, 1151, 1173, 1189, 1220, 1252, 1284, 1301, 1316, 1346, 1376, 1401, 1420, 1450, 1472, 1493, 1525, 1558, 1576, 1606, 1636, 1656, 1685, 1698, 1712, 1737, 1767, 1799, 1816, 1848, 1865, 1895, 1911, 1940, 1970, 2004, 2026, 2042, 2063, 2078, 2110, 2126, 2157, 2173, 2202, 2234, 2250, 2267, 2298, 2314, 2344, 2359, 2389, 2421, 2437, 2468, 2499, 2530, 2546, 2579, 2594, 2624, 2639, 2669, 2683, 2713, 2743, 2758, 2773, 2803, 2821, 2839, 2854, 2884, 2913, 2927, 2943, 2973, 2988, 3004, 3034, 3064, 3080, 3095, 3125, 3156, 3172, 3187, 3202, 3232, 3262, 3278, 3309, 3326, 3356, 3377, 3407, 3422, 3453, 3468, 3498, 3529 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz | secret_prefix | 1 | 622 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION | email | 1 | 5 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf | email | 3 | 424, 427, 1134 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf | email | 3 | 360, 363, 904 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf | email | 1 | 1584 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf | email | 1 | 2896 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/webr-worker.js | email | 2 | 35, 36 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| app/r-shiny/shinylive/webr/webr-worker.js | username | 1 | 2 | Generic runtime/UI/documentation word; not an identified local account; preserved. |
| app/r-shiny/shinylive/webr/webr.mjs | local_path | 1 | 2 | Virtual runtime filesystem or font configuration; not a host account path; preserved. |
| bench/docs/dat.aloe2013.txt | email | 1 | 54 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.anand1999.txt | email | 1 | 51 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.anker2025.txt | email | 1 | 68 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.assink2016.txt | email | 1 | 56 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.axfors2021.txt | email | 1 | 44 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bakdash2021.txt | email | 4 | 90, 91, 92, 93 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.baker2009.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bangertdrowns2004.txt | email | 1 | 58 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bartos2023.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.baskerville2012.txt | email | 1 | 64 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bassler2004.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bauer2002.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bcg.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.begg1989.txt | email | 1 | 49 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.berkey1998.txt | email | 1 | 66 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.besson2016.txt | email | 1 | 99 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bonett2010.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bornmann2007.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.bourassa1996.txt | email | 1 | 67 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.cannon2006.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.chiarito2020.txt | email | 1 | 74 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.chiarito2020.txt | secret_prefix | 3 | 6, 64, 70 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/docs/dat.cohen1981.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.colditz1994.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.collins1985a.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.collins1985b.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.craft2003.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.crede2010.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.crisafulli2020.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.curtin2002.txt | email | 1 | 38 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.curtis1998.txt | email | 1 | 86 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.dagostino1998.txt | email | 1 | 70 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.damico2009.txt | email | 1 | 39 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.debruin2009.txt | email | 1 | 53 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.demir2022.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.dogliotti2014.txt | email | 1 | 41 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.dong2013.txt | email | 1 | 44 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.dorn2007.txt | email | 1 | 49 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.dumouchel1994.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.egger2001.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.feng2019.txt | email | 1 | 43 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.fine1993.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.franchini2012.txt | email | 1 | 51 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.frank2008.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.furukawa2003.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.gibson2002.txt | email | 1 | 78 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.graves2010.txt | email | 1 | 41 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.greb2008.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.greenland1992.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.gurusamy2011.txt | email | 1 | 51 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hackshaw1998.txt | email | 1 | 54 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hahn2001.txt | email | 1 | 41 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hannum2020.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hart1999.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hartmannboyce2018.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hasselblad1998.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.higgins2008.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.hine1989.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.huber2000.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.ishak2007.txt | email | 1 | 64 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.kalaian1996.txt | email | 1 | 59 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.karner2014.txt | email | 1 | 75 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.karner2014.txt | secret_prefix | 3 | 5, 64, 71 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/docs/dat.kearon1998.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.knapp2017.txt | email | 1 | 74 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.konstantopoulos2011.txt | email | 1 | 58 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.landenberger2005.txt | email | 1 | 66 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.laopaiboon2015.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lau1992.txt | email | 1 | 38 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lee2004.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lehmann2018.txt | email | 1 | 89 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.li2007.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lim2014.txt | email | 1 | 51 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.linde2005.txt | email | 1 | 80 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.linde2015.txt | email | 1 | 65 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.linde2016.txt | email | 1 | 63 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lloyd2010.txt | email | 1 | 39 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.lopez2019.txt | email | 1 | 75 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.maire2019.txt | email | 1 | 55 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.mccurdy2020.txt | email | 1 | 89 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.mcdaniel1994.txt | email | 1 | 62 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.meeker2017.txt | email | 1 | 37 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.michael2013.txt | email | 1 | 69 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.molloy2014.txt | email | 1 | 61 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.molloy2014.txt | secret_prefix | 1 | 32 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/docs/dat.moore1998.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.moura2021.txt | email | 1 | 46 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.nakagawa2007.txt | email | 1 | 35 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.nielweise2007.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.nielweise2008.txt | email | 1 | 49 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.nissen2007.txt | email | 1 | 67 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.normand1999.txt | email | 1 | 41 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.obrien2003.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.pagliaro1992.txt | email | 1 | 42 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.pignon2000.txt | email | 1 | 49 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.poole2003.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.pritz1997.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.quan2000.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.raudenbush1985.txt | email | 1 | 78 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.riley2003.txt | email | 1 | 49 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.rivera2025.txt | email | 1 | 52 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.roever2022.txt | email | 1 | 41 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.senn2013.txt | email | 1 | 47 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.spooner2002.txt | email | 1 | 53 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.steurer2006.txt | email | 1 | 45 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.stowe2010.txt | email | 1 | 57 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.tannersmith2016.txt | email | 1 | 57 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.thompson1999.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.tian2009.txt | email | 1 | 52 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.ursino2021.txt | email | 1 | 40 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.vanhowe1999.txt | email | 1 | 50 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.viechtbauer2021.txt | email | 1 | 36 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.white2020.txt | email | 1 | 51 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.woods2010.txt | email | 1 | 34 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/dat.yusuf1985.txt | email | 1 | 48 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/datsearch.txt | email | 2 | 99, 100 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/datsearch.txt | secret_prefix | 1 | 94 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/docs/metadat-package.txt | email | 5 | 101, 102, 103, 104, 105 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/docs/prep_dat.txt | email | 1 | 32 | Unresolved blanket-email request: protected public contact or binary pattern; byte/pin preservation retained. |
| bench/original/shared/alm-task.css | secret_prefix | 3 | 37, 41, 42 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/benefit-risk-v1.js | secret_prefix | 1 | 1 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/evalue.js | secret_prefix | 1 | 4 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/glossary.js | secret_prefix | 1 | 52 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/ma-methods-v1.js | secret_prefix | 1 | 70 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/protocol-schema.js | secret_prefix | 1 | 92 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/original/shared/rob-core.js | secret_prefix | 1 | 1 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/alm-task.css | secret_prefix | 3 | 37, 41, 42 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/benefit-risk-v1.js | secret_prefix | 1 | 1 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/evalue.js | secret_prefix | 1 | 4 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/glossary.js | secret_prefix | 1 | 52 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/ma-methods-v1.js | secret_prefix | 1 | 70 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/protocol-schema.js | secret_prefix | 1 | 92 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| bench/patched/shared/rob-core.js | secret_prefix | 1 | 1 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| validation-original/SOURCE_SHA256-v1.0.0.json | secret_prefix | 2 | 297, 414 | Public certificate, ordinary text/filename or binary coincidence; no access token/private key identified. |
| validation-plus/plus/generator.log | local_path | 4 | 3, 12, 13, 14 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |
| validation-plus/plus/generator.log | username | 4 | 3, 12, 13, 14 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |
| validation-plus/plus/inventory.log | local_path | 10 | 3, 12, 13, 14, 27, 28, 29, 30, 31, 32 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |
| validation-plus/plus/inventory.log | username | 10 | 3, 12, 13, 14, 27, 28, 29, 30, 31, 32 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |
| validation-plus/plus/live-protocol.log | local_path | 16 | 3, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29, 32, 33, 34 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |
| validation-plus/plus/live-protocol.log | username | 16 | 3, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29, 32, 33, 34 | Unresolved: local installation/account data in upstream-pinned log; redaction would violate unchanged pins. |

### Python verification

The archive-owned regeneration and integrity verifier completed successfully.
The full verifier was attempted with both available Python environments: the
default lacks Matplotlib; the release runner environment has Matplotlib but its
native extension fails to initialize in this sandbox. No verifier was weakened.
Last output lines:

~~~text
Regenerated app/app-sha256.json and SOURCE_SHA256.json; original and extras pins unchanged
RECUT INTEGRITY PASS: 167 app files; 519 original files unchanged; extras pins and coverage verified
ImportError: DLL load failed while importing _c_internal_utils: A dynamic link library (DLL) initialization routine failed.
~~~
