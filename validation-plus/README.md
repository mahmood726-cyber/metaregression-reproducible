# Extras validation for archive v1.1.0

This is a byte-preserved copy of allmeta v1.8.0's entire meta-regression/validate
directory, including helpers whose filenames do not contain "plus".
UPSTREAM_SHA256.json inventories those original files. README-plus.md is the
upstream protocol and historical PR #149 evidence, not a new execution report.

It checks two- and three-moderator ML meta-regression, optional interaction,
likelihood-ratio comparisons, AIC/BIC, coefficient inference, ML weights and
bubble fitted-mean confidence bands. The reference uses desktop R 4.6.0,
metafor 5.2-1 (packageVersion: 5.2.1), metadat 1.6.0 and jsonlite 2.0.0,
with the original non-default controls and tolerances preserved.

The 2026-10-21 release run on allmeta 1cb3f84 recorded 52,573/52,573
numerical/structural checks across 194 configurations; the panel recorded
52,767/52,767 including 194 render checks. All 5 DOM/negative-probe tests passed.
See ../provenance/run_plan-2026-10-21-release.log. Counts match MANIFEST-plus.json. Three documented synthetic mixed-scale
divergences are outside that denominator; they remain explicitly labelled in
plus/divergences.json and are exercised by numeric.test.mjs.

From the archive root, with Node, desktop R and installed dependencies available:

    python analysis/recut.py prepare
    python analysis/recut.py numeric
    python analysis/recut.py dom
    python analysis/recut.py browser

The wrappers stage the copied validation files under
.validate-work/recut/app/meta-regression/validate beside the archived app files.
This preserves every relative import without editing the upstream scripts.
Numerical and DOM evidence is written in that disposable stage; collected results
and logs are in outputs/recut/. Browser replay serves the real archive app at
http://127.0.0.1:8000/meta-regression/index.html and blocks off-origin requests.
Set PLAYWRIGHT_MODULE to the installed Playwright module if needed; PW_CHANNEL
defaults to msedge. The DOM suite needs linkedom (LINKEDOM_MODULE may name its
esm/index.js). Nothing is installed or downloaded by these commands.

Optional fresh desktop corpus/reference generation:

    python analysis/recut.py generate-plus

Run prepare first. The original generate-plus.R runs with its expected working
directory, inside the disposable stage only. Review the new corpus, references
and candidate ledger against the pinned evidence. Do not run pin-plus.mjs on
the archive or overwrite its references to turn a failure into a pass. Run
prepare again to restore the pinned stage before the standard replay.

The optional desktop live-script protocol can be exercised after prepare:

    node .validate-work/recut/app/meta-regression/validate/check-live-script.mjs build
    python bench/launch.py .validate-work/recut/app/meta-regression/validate/plus/live-protocol.log Rscript .validate-work/recut/app/meta-regression/validate/plus/live-protocol.R
    node .validate-work/recut/app/meta-regression/validate/check-live-script.mjs

Upstream expected result: 1,301/1,301 checks; this is not webR execution.
The copied app includes lazy webR 0.5.5 assets and pinned metafor 4.8-0
dependencies. Its live tier has a different package version from the desktop
reference. The standard recut runner tests corpus replay and the DOM suite;
it does not claim to rerun the upstream seven-test browser suite, accessibility
suite, live webR tier, or every interactive export.

| Content | Static or dynamic | Evidence |
|---|---|---|
| Controls, tolerances, expected counts | Static preserved protocol | MANIFEST-plus.json and original scripts |
| Corpus, R references and divergences | Recorded upstream evidence | Four SHA-256-pinned JSON files |
| Release numerical/browser results | Observed 2026-10-21 | Preserved release log and runtime receipts |
| Copy and source integrity | Dynamic | analysis/recut_integrity.py |
