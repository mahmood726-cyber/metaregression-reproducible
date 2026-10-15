# Random-effects meta-regression in the browser: validation against the R package metafor

Version 1.0.0. Creator: Mahmood Ahmad. MIT-licensed archive code.

This archive validates allmeta at **e47acf19f13d36feac52fc414d3c9782012155cc** (PR #89), included in allmeta [v1.2.1](https://doi.org/10.5281/zenodo.23288388) and [v1.3.0](https://doi.org/10.5281/zenodo.23330389). The reference environment is **R 4.6.0, metafor 5.2-1 and metadat 1.6-0** (R package-version strings 5.2.1 and 1.6.0). Release identifiers are supplied provenance; app bytes are verified against the specified local git objects.

Excluding experimental location-scale (LS), **129,867 of 129,903 checks pass**, versus **115,139** before the fixes. There are **36 documented conditioning differences across 14 configurations**, including eight using year as moderator. This is not an all-pass claim. The corpus screens **114 metadat datasets**, retaining **223 effect definitions and 1,742 configurations from 111 datasets**.

## Model and corpus

The exact primary reference is:

```r
metafor::rma(yi, vi, mods = ~x, data = d, method = "PM", test = "adhoc",
             control = list(tol = 1e-12, threshold = 1e-12, maxiter = 1000))
# For every configuration with 4 <= k <= 7:
metafor::permutest(fit, exact = TRUE)
```

The browser implements an intercept and **one numeric moderator**, Paule–Mandel heterogeneity, and floored Knapp–Hartung inference, `q=max(1,RSS/(k-2))`. The matching metafor test is `adhoc`, not `knha`. Main fitting accepts k≥3; permutation and LS are offered at k≥4. Alternate estimators, multiple moderators, factors and dependence models are outside this validation.

All metadat catalogue entries were screened. Inputs come from supplied effects/variances, documented escalc recipes and schema-checked supplements. Each resulting effect frame considers every eligible varying numeric column; known identifiers and yi/vi/sei outputs are excluded. Complete cases must have finite yi, vi and moderator values, positive variances and at least three rows. Numeric-looking strings are converted only when the whole nonmissing column is numeric. `data/effect-recipes.json`, `dataset-audit-final.json`, `moderator-exclusions.json` and `configuration-exclusions.json` preserve mappings and every exclusion reason; `bench/docs/` preserves package documentation/examples.

The final source audit removes duplicate complete-case triples, an incomplete percentage conversion, a documentation variant overwriting an observed outcome and generated labels. Raw journals contain 1,808 unique candidates; the final corpus retains 1,742. `results/raw/` preserves journals before filtering; comparison inputs must have exactly the final ID set with no duplicates. All five permutation journals are retained and merged into 365 unique exact-test records.

This deliberately broad **computational stress test is not a recommendation to use every numeric variable as a moderator**. It includes outcome-related predictors, numerical encodings and dependent/multi-arm rows. It does not validate clinical interpretations or independence assumptions. Labels such as `dat.bcg:1` are frame row addresses, not source trial identifiers. The archive validates installed-package values and recipes, without re-extracting publications.

## Comparisons and remaining differences

| Group | Passed after | Checks |
|---|---:|---:|
| Model quantities | 34,818 | 34,840 |
| Bubble plot | 86,986 | 87,000 |
| Exact permutation (365 configurations) | 1,095 | 1,095 |
| Structural | 6,968 | 6,968 |
| Non-LS total | 129,867 | 129,903 |
| Experimental LS, separate | 82,680 | 91,515 |

Estimates, SEs, confidence/prediction limits and statistics use `abs(app-reference)/max(1,abs(reference)) <= 1e-9`. P-values use absolute differences; displayed slope p-values must match the reference rounded to three decimals exactly. Intercept t/p, I², H² and QM are retained in R evidence but are not counted as exposed app outputs. Structural checks cover record presence, page errors, fit status and parsed rows.

Bubble checks cover the number of circles, every radius and the first/middle/last fitted-line and both confidence-band edges. SVG y coordinates are inverted using the original plotting transform. Radius is `4+10*(1/vi)/max(1/vi)`; bubble area is not proportional to inverse variance and random-effects weights do not set size. Plot-count checks are exact; other plot quantities use 1e-9.

The 36 differences range from approximately **1.0e-9 to 1.1e-7**. `outputs/table2_differences.csv` identifies each configuration, quantity and vector index, retains app/reference/difference values, and adds the centered-refit difference. Centered/scaled refits use `z=(x-mean(x))/sd(x)` and `tol=threshold=1e-15`, mapping coefficients and covariance back to the original scale. All recorded centered diagnostics agree within **3e-11**. Bubble diagnostics reconstruct bands from those fitted coefficients, tau², q and the design. Centered results diagnose conditioning; they do not replace the prespecified raw reference or erase its failures.

LS is experimental and **does not agree with metafor**: for example, alpha coefficients pass 1,893/3,280 checks. Its estimates/SEs/CIs, log likelihood and variances use 1e-6, with displayed scale-slope p checked at three decimals. The historical LS oracle uses ML and `scale=~x`; 91 offered configurations have R errors/refusals, including one timeout. Local/boundary optima, identifiability and curvature remain limitations. Explicit undefined SE values can match explicit nulls; missing keys, NaN, Infinity, wrong types and unmatched nulls cannot pass. The page's literal `--` p display is recognized only for its undefined experimental scale inference.

The measured fresh R run reports 82,672/89,671 experimental LS checks passing. It has 92 errors/refusals versus 91 historically: dat.moura2021/e1/ri (reached elapsed time limit). This additional execution timeout changes the LS denominator; it does not indicate improved agreement. The paper tables retain the historical 82,680/91,515 result. See outputs/validate_R_LS_review.json and validate_R_LS_errors.csv. The primary gate remains 129,867/129,903, with 36 documented and zero unexpected failures.

Monte Carlo permutation p-values are not compared because the app and R use different RNGs. Exact permutations alone are compared, for every k=4–7 configuration. R can collapse repeated permutations; equal multiplicities preserve the p-value.

## Five faults corrected in PR #89

1. Coarse t-quantile bisection and incomplete-beta convergence caused interval and band inaccuracies; tolerances were tightened.
2. Raw cross-product subtraction lost precision for large-offset moderators; centered weighted sums, centered prediction variance and tighter relative PM convergence were introduced, including the permutation helper.
3. Exported R used `knha` despite the implemented floor; it now uses `adhoc`. The unsupported extra-covariates hint was corrected.
4. LS optimization omitted outside contraction, used an unscaled location design and converted negative covariance diagonals into zero SEs; these were corrected without claiming full LS parity.
5. Refused main fits left stale prediction intervals and permutation results; both caches are now cleared.

`bench/fix.patch` and `bench/RESULTS.md` preserve the evidence. Table 1 regenerates every quantity's before/after count; the non-LS total improves from 115,139 to 129,867. The historical UI contract improved from 2/3 to 3/3; it is distinct from the numerical denominator.

For **dat.bcg, log RR on absolute latitude**, the R slope is **−0.0286 (95% CI −0.0485 to −0.0086; p=0.009)**, tau² **0.142**, R² **55.3%**, and QE **30.73 (11 df, p=0.001)**. These rounded values are checked against full-precision source records, not inserted as computed outputs.

## Reproduce

From this archive root, using already installed R packages metafor, metadat, jsonlite and digest:

```text
Rscript validate.R
```

Set standard `R_LIBS_USER`/`R_LIBS` variables to existing libraries if needed. The validator prioritizes `R_LIBS_USER` and fails loudly unless the paper's R and package versions load. No packages are installed and no network is used. It SHA-256-checks an exact input manifest before fitting every main configuration and running all 365 exact permutation tests. Model quantities, predictions, bubble reference values and exact p-values are freshly computed; archived app outputs, SVG coordinates and structural evidence are replayed. Experimental LS fits are also freshly recomputed with the original ML model, maxiter=10000 and 60-second per-fit limit; they are reported separately and their numerical discrepancies never affect the primary exit status. Three local R worker processes perform the fresh fits; progress is recorded in outputs/validate_R_workers.log. Historical publication LS totals remain tied to the archived run, since fresh timeout or optimizer behavior can differ. A browser is not run by this command.

It prints a per-quantity table and `129867/129903 checks pass`, followed by `129,867/129,903 pass; 36 documented, 0 unexpected`, and writes `outputs/validate_R_table.csv`, `validate_R_LS_table.csv`, `validate_R_fresh.rds` and `validate_R_runtime.json`. Success requires exactly the documented failing keys in `expected/documented_differences.json`; any unexpected failure, vanished/changed documented failure, duplicate or coverage mismatch exits nonzero. The measured runtime and command outcome are in `REPORT.md` outside this archive.

With Python and the packages listed in `analysis/requirements.txt`:

```text
python analysis/make_outputs.py
python -m pytest -q analysis/test_safeguards.py
python analysis/verify_archive.py
```

Output generation recreates both tables, agreement and visual-abstract PNG/TIFF pairs, `sizes.json`, evidence-linked `numbers.json` and `reproduction_report.md`. Figures are 300 dpi, 170 mm wide, with text ≥8 pt. Expected paper values are assertions only. The verifier checks source inventory/hashes, exact journal filtering, input coverage, tables, reproducibility, paired image pixels, metadata and fresh R results when present. It permits `.git` metadata.

`app/` contains byte-identical git objects for every page dependency, including all four fetchable glossary languages, with `app-sha256.json`. Serve it at `http://127.0.0.1:8000` and open `/meta-regression/index.html`. `bench/` retains the historical scripts with local paths replaced and exact R field access; see its README for replay instructions. `node bench/ui_smoke.cjs` replays the original browser E2E contract on absolute local file URLs, using an installed Playwright (set PLAYWRIGHT_MODULE if it is not locally resolvable). Four checks cover k=3 and k=4 fit/plot behavior, refusal-cache clearing, and absence of page errors; HTTP(S) requests are blocked. The BCG screenshot is retained. All glossary files are separately covered by the static asset and hash checks. Nothing was committed, pushed or deployed.

| Content | Static or dynamic | Evidence / transformation |
|---|---|---|
| Model, scope, tolerances and figure style | Static protocol/presentation | Inspected original scripts and archive code |
| Expected counts and release identifiers | Static assertions/provenance | Task specification, pinned commit and metadata |
| Study values and moderators | Recorded package evidence | Corpus, recipes, exclusions and package help |
| Counts, errors, use-case numbers, tables and figures | Dynamic | Strict comparisons of full-precision records |
| Fresh R primary references and exact tests | Dynamic | All configurations refitted by validate.R |
| Browser outputs in R command | Historical replay | Archived result records, clearly labelled |
| Hashes | Dynamic integrity evidence | Assembled source bytes; not scientific certification |

MIT covers archive code and does not replace upstream data/documentation rights. Package documentation and original attribution remain with the evidence. No manuscript drafts, machine-specific paths, secrets or release-certification claims are included.
