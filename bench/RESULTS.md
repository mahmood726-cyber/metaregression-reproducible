# Meta-regression validation against metafor

**Validation completed with discrepancies. This is not an all-pass certification.** Upstream allmeta was read-only; every generated artifact and patched file is in this job folder.

Final corpus: **1742 configurations**, **111 of 114 metadat datasets**, **223 effect definitions/data subsets**; k ranges from 3 to 1828. The source audit removed 66 candidates from 1808. No simulated study values were used.

## Runtime and actual page contract

Initial source HEAD: `39f172b00233d072bdce5cfe4c7137f79167708a`. R version 4.6.0 (2026-04-24 ucrt); metafor 5.2.1; metadat 1.6.0. Chrome was driven through Playwright using local file URLs, with HTTP(S) requests blocked. `source-manifest.json` verifies byte-identical original page/dependency copies against upstream. Unrelated copied modules changed upstream during this audit; these were not edited by this job and are not loaded by this page. The manifest marks them explicitly.

The shipped page fits one numeric moderator plus an intercept, with PM heterogeneity and **floored** Knapp–Hartung inference (`q=max(1,RSS/(k−2))`). The matching R test is `adhoc`, not `knha`. There are no selectable alternate main-model tau estimators or inference tests. Main fitting and the bubble plot accept k≥3; the note recommends k≥4. Permutation and optional ML location-scale fitting are enabled for k≥4. Text factors and multiple-moderator designs are not supported. Numeric-looking strings are converted only when the entire nonmissing column is numeric.

Compared main outputs: both coefficients, SEs and confidence limits; slope t (arithmetic on exposed coefficients and SEs), displayed slope p, PM tau², q, residual df, R², QE and its p, prediction/SE/95% prediction interval at mean x. The app does **not** expose/display intercept t/p, I², H², or QM/F and its p. These are retained in the R reference but are not invented as app outputs or counted as missing-app failures. Slope and scale-slope p-values are private to the page; their cards show three decimals, so those checks compare the displayed rounding, not a claimed full-precision p-value.

The SVG is read from the actual rendered page. Every bubble radius and bubble count are checked. The fitted line and both confidence-band edges are checked at the first, middle, and last sampled x positions. Bubble radius is `4 + 10*(1/vi)/max(1/vi)`; bubble **area** is not proportional to inverse variance and RE weights are not used for bubble size. No such area-weighting equivalence is claimed.

The location-scale option profiles ML with log tau²=alpha0+alpha1*x, normal location CIs, alpha SEs, approximate normal scale-slope p, and a tau² range. The runner reads `__almLocScale()` from the actual page, not a reimplementation. Beta/alpha estimates and SEs, beta CIs, log likelihood, every per-row tau² and its range, and the displayed alpha1 p are checked.

## Corpus selection and traceability

All datasets were enumerated using `data(package="metadat")`. The package documentation is archived under `docs/`. Precomputed yi/vi, documented escalc/model inputs, documented pairwise transformations, and schema-checked supplements are recorded in `effect-recipes.json`, `supplemental.R`, and `dataset-audit-final.json`. Supplements include RR for standard 2×2 schemas, MD/SMD for documented mean/SD/sample-size schemas, Fisher-z correlations, named effect/SE pairs, and explicitly named endpoints. This is a defined, finite effect-recipe corpus, not every mathematically possible effect-size transformation.

Every numeric column in each resulting effect frame is considered, including sample sizes and numeric outcome-related fields. Known identifiers and yi/vi/sei output fields are excluded; constant columns and configurations with fewer than three finite complete rows or nonpositive variances are excluded. All categorical exclusions and moderator-level reasons are in `moderator-exclusions.json`. No hand-picked moderator subset is used. This deliberately broad computational stress test includes endogenous outcome-related predictors, correlated/multi-arm rows, and numerical encodings. It does not endorse those regressions as scientific analyses or validate dependence modeling.

The final audit (`finalize_corpus.R`, `configuration-exclusions.json`) removes identical complete-case numeric triples within a dataset/moderator, regardless of row ordering; the incomplete OBrien percentage-conversion state; the Dorn documentation variant that manually overwrites one observed effect; and generated study labels. R and JS consume the identical exported numbers. Row labels such as `dat.bcg:1` are analysis-frame row addresses, not asserted original-dataset row identifiers or trial identifiers. Installed-package data and documented recipes are the evidence; this audit does not independently re-extract the underlying publications.

| Item | Static / dynamic disclosure |
|---|---|
| Method, numeric tolerances, eligible schemas, exclusion rules | Static inspected rules; explicit in scripts |
| Study values and covariates | Dynamic installed metadat reads |
| Effect sizes and variances | Dynamic metafor::escalc / documented calculations; no fitted-output literals |
| App/reference estimates, counts, discrepancies | Dynamic actual Chrome and R runs |
| App built-in toy example | Page initializes it, then every audited run replaces it with the corpus; not counted |

## Comparison rules and totals

Main closed-form quantities use 1e−9. PM is solved tightly in R (`tol=threshold=1e−12`, maxiter=1000); PM outputs are also checked at 1e−9. All ML estimates, SEs, likelihoods and variance components use 1e−6; no flat-likelihood 1e−4 relaxation was used. Differences are `abs(app−ref)/max(1,abs(ref))`, except p-values use absolute error. Display-only p checks require the same three-decimal rounded value. Matching null/NA values check missingness, not numeric precision. Both refusals match; one-sided refusals fail. Plot and structural checks are separately named so the large number of bubble checks cannot hide coefficient failures.

Main numeric totals: original 29805/34840; patched 34818/34840.

Verbatim final comparison lines:
```text
197780/221418 checks pass
212547/221418 checks pass
```

| Quantity | Original pass/checks | Original maximum | Patched pass/checks | Patched maximum | Tolerance |
|---|---:|---:|---:|---:|---:|
| record_present | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| no_page_error | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| fit_status | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| beta | 3474/3484 | 1.86049274839e-08 | 3483/3484 | 2.10347562794e-09 | 1e-09 |
| se | 3474/3484 | 4.54610636893e-08 | 3484/3484 | 2.70337818752e-10 | 1e-09 |
| ci_lb | 1141/3484 | 2.2401819022e-06 | 3484/3484 | 2.52262763625e-10 | 1e-09 |
| ci_ub | 1142/3484 | 1.0854732113e-06 | 3484/3484 | 2.88075549463e-10 | 1e-09 |
| tau2 | 1742/1742 | 9.32049784574e-11 | 1742/1742 | 5.49767106839e-11 | 1e-09 |
| R2 | 1632/1742 | 7.96306559292e-06 | 1736/1742 | 4.46476967064e-08 | 1e-09 |
| QE | 1735/1742 | 1.08274862612e-07 | 1735/1742 | 1.08274887081e-07 | 1e-09 |
| QE_p | 1740/1742 | 5.09330780468e-08 | 1740/1742 | 5.09330897042e-08 | 1e-09 |
| q | 1682/1742 | 7.09418703115e-07 | 1741/1742 | 3.49613559102e-09 | 1e-09 |
| df | 1742/1742 | 0 | 1742/1742 | 0 | 1e-09 |
| pred | 1740/1742 | 4.31657554145e-09 | 1740/1742 | 2.40140707319e-09 | 1e-09 |
| pred_se | 1741/1742 | 2.65028288204e-09 | 1742/1742 | 5.11817144222e-10 | 1e-09 |
| pi_lb | 1699/1742 | 1.70703571833e-08 | 1740/1742 | 1.79075041093e-09 | 1e-09 |
| pi_ub | 1698/1742 | 1.68857259286e-08 | 1742/1742 | 7.74990258793e-10 | 1e-09 |
| parsed_rows | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| slope_t | 1681/1742 | 4.01656275338e-07 | 1741/1742 | 2.91113753636e-09 | 1e-09 |
| slope_p_display | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| bubble_count | 1742/1742 | 0 | 1742/1742 | 0 | 0 |
| bubble_line | 5221/5226 | 7.9077153714e-09 | 5221/5226 | 2.41698216996e-09 | 1e-09 |
| bubble_ci | 729/10452 | 2.26900149335e-06 | 10443/10452 | 5.27129335869e-09 | 1e-09 |
| bubble_radius | 69580/69580 | 4.4167953332e-16 | 69580/69580 | 4.4167953332e-16 | 1e-09 |
| LS_fit_status | 1640/1731 | 1 | 1640/1731 | 1 | 0 |
| LS_beta | 3126/3280 | 1.06551308468 | 3129/3280 | 1.06551308654 | 1e-06 |
| LS_betaSE | 3140/3280 | 0.138211337244 | 3145/3280 | 0.138211337244 | 1e-06 |
| LS_alpha | 1895/3280 | 450.733951552 | 1893/3280 | 450.733951552 | 1e-06 |
| LS_alphaSE | 2154/3280 | inf | 2157/3280 | inf | 1e-06 |
| LS_logLik | 1571/1640 | 1.10438055273 | 1573/1640 | 1.10438055273 | 1e-06 |
| LS_tau2 | 58498/63544 | 63.389817275 | 58506/63544 | 63.3898243343 | 1e-06 |
| LS_beta_lb | 3128/3280 | 1.02814638426 | 3132/3280 | 1.02814638665 | 1e-06 |
| LS_beta_ub | 3128/3280 | 6.05947190069 | 3132/3280 | 6.05947175329 | 1e-06 |
| LS_alpha_p_display | 1290/1640 | inf | 1300/1640 | inf | 0 |
| LS_tau2_min | 1593/1640 | 0.449669305724 | 1594/1640 | 0.449669355084 | 1e-06 |
| LS_tau2_max | 1478/1640 | 40.9036494804 | 1479/1640 | 40.9036541461 | 1e-06 |
| exact_permutation_record | 365/365 | 0 | 365/365 | 0 | 0 |
| exact_permutation_status | 365/365 | 0 | 365/365 | 0 | 0 |
| exact_permutation_p | 364/365 | 0.00277777777778 | 365/365 | 0 | 1e-09 |

## Console endings

| Log | Verbatim last nonempty line |
|---|---|
| corpus-final.log | `1808 configurations; 111 / 114 datasets used` |
| corpus-audit.log | `1742 final configurations; 66 source-audit exclusions` |
| reference-resume.log | `1808 reference configurations recorded` |
| app.log | `1798 app configurations recorded (original)` |
| app-extra.log | `1808 app configurations recorded (original)` |
| patched-app.log | `1798 app configurations recorded (patched)` |
| patched-extra.log | `1808 app configurations recorded (patched)` |
| permutation-0.log | `92 exact permutation configurations recorded` |
| permutation-1.log | `91 exact permutation configurations recorded` |
| permutation-2.log | `91 exact permutation configurations recorded` |
| permutation-3.log | `91 exact permutation configurations recorded` |
| centered-reference.log | `14 centered-reference diagnostics recorded` |

## Permutation and location-scale limitations

Exact permutation tests: 365 configurations with 4≤k≤7, tested against actual `metafor::permutest(rma(...,method='PM',test='adhoc'),exact=TRUE)`. The page enumerates k! permutations; R collapses duplicate permutations. Equal multiplicity gives the same p-value. R's default comparison tolerance is sqrt(machine epsilon); the app uses 1e−10. Every exact result is in the reference journals and final `reference.json`.

The original app passes 364/365 exact p checks; the patch passes 365/365. In `dat.hart1999/e1/year`, original p=0.39166666666666666, R/patched p=0.39444444444444443. `diagnose_permutation.cjs` calls the shipped original and patched `_slopeT` helpers on every permutation. It finds 2 lost ties out of 720 permutations: original cancellation shifts the tied absolute t by about −3.30e−10, beyond the page's 1e−10 comparison tolerance; centering reduces that difference to about −1.11e−16. Full precision evidence is in `permutation-diagnostic.json`.

The page's fixed-seed LCG Monte Carlo results for 1366 configurations are recorded but **not numerically comparable** with R's different random generator. For 11 configurations with k=3 the page offers no permutation test.

Location-scale R errors/timeouts: 91 of 1731 offered cases. Errors and warnings are retained by configuration. Remaining long-running LS calls were limited to 60 seconds; timeouts are execution limits, not mathematical refusals. Timeout IDs: dat.moura2021/e1/ni. The first reference run was resumed after a long large-k fit, retaining completed records. No completed result was replaced to improve agreement.

Patched likelihood comparison: {"app_higher_likelihood": 39, "likelihood_agrees_within_1e-6": 1573, "reference_error_or_timeout": 91, "reference_higher_likelihood": 28}. Agreement in likelihood does not establish agreement or identifiability of scale coefficients. Either implementation can find a higher local/boundary likelihood; these are discrepancies, not automatic proof that R or JS found a global optimum.

## Root causes and local patch

Line references below refer to unchanged `original/` files.

1. `meta-regression/index.html:360–369`: t critical-value bisection stops at 1e−6, causing CI and confidence-band errors. The patch tightens it to 1e−13 and incomplete-beta convergence to 1e−14.
2. `meta-regression/index.html:206–223`, `:251–273`, `:431–435`, `:524`; `shared/permutest.js:23–39`: raw cross-product subtraction cancels for large-offset moderators, prediction/band variance repeats that subtraction, and PM uses an absolute tau stopping threshold. The patch centers the WLS sums and uses centered prediction variance with tighter relative PM convergence.
3. `meta-regression/index.html:164`, `:603`: the exported R code uses `test="knha"` despite the implemented floor at `:282`. The patch exports `test="adhoc"`; `reference.json` retains separate knha SE/CIs. The two R tests produce SE differences exceeding 1e−9 in 523 retained configurations. The extra-covariates hint at `:111` is also misleading: the engine fits one scalar moderator, and the tail-based parser at `:192–197` does not implement multivariable regression. The patch corrects the hint.
4. `shared/location-scale.js:61–75`: the Nelder–Mead routine omits outside contraction. `:34–41` uses an unscaled location design while only Z is standardized at `:107–116`. `:139–146` uses a finite-difference profile Hessian and turns negative variance diagonals into zero SEs. The patch adds outside contraction, scales the one-moderator location design and maps coefficients/covariance back, and returns undefined SE for nonpositive covariance diagonals. It does not establish global convergence or solve boundary identifiability. Finite-difference curvature and absence of a reliable convergence/Hessian validity gate remain blockers for blanket LS parity.
5. `meta-regression/index.html:549–550`: failed main fits clear some caches but retain PI and permutation results. The patch clears both; the original UI contract fails and the patched contract passes.
6. Residual main-model differences against raw R are numerically diagnosed separately. `centered-reference.R` fits an algebraically equivalent centered/scaled moderator and maps estimates/SEs back, tightening R root tolerance to 1e−15. `centered-diagnostics.json` records those diagnostic checks; they do not replace the prespecified raw-reference results or erase failures. This isolates raw R conditioning/root tolerance from app error for the tested configurations.

The patch is `fix.patch`, against allmeta paths, and is applied only under `patched/`. The numerical changes received a full corpus rerun; subsequent cache and wording changes received targeted UI checks. Unresolved discrepancy instances remain in `results-original.json`, `results-patched.json` and `STUCK_FAILURES.md`. There is no all-pass or release claim.

## UI verification and exact commands

Verbatim UI contract lines:
```text
2/3 UI contracts pass (original)
3/3 UI contracts pass (patched)
```

`ui-original.png` and `ui-patched.png` show the real BCG/latitude plot with explicit effect and moderator labels. The patched screenshot was visually inspected. Syntax checks passed for patched permutation and location-scale JS. The directory is not a Git repository; nothing was committed, pushed, or deployed.

Run from this folder. `launch.py` sets R_LIBS_USER to the supplied sibling library and captures UTF-8 logs:
```powershell
$env:R_LIBS_USER=(Resolve-Path ..\re\Rlib_dta).Path
Rscript inspect.R
python launch.py corpus-final.log Rscript corpus.R
python launch.py corpus-audit.log Rscript finalize_corpus.R
python launch.py reference.log Rscript reference.R
# Resume, if interrupted: python launch.py reference-resume.log Rscript reference.R
python launch.py app.log node run_app.cjs original app.jsonl
python make_patch.py
node --check patched/shared/permutest.js
node --check patched/shared/location-scale.js
python launch.py patched-app.log node run_app.cjs patched patched-app.jsonl
# The actual expanded-corpus resumes used app-extra.log and patched-extra.log.
python launch.py permutation.log Rscript permutation.R
# The initial exact run was stopped and resumed in four disjoint batches:
python launch.py permutation-0.log Rscript permutation.R permutation-0.jsonl 0 4
python launch.py permutation-1.log Rscript permutation.R permutation-1.jsonl 1 4
python launch.py permutation-2.log Rscript permutation.R permutation-2.jsonl 2 4
python launch.py permutation-3.log Rscript permutation.R permutation-3.jsonl 3 4
python launch.py ui-original.log node test_ui.cjs original
python launch.py ui-patched-final.log node test_ui.cjs patched
python launch.py centered-reference.log Rscript centered-reference.R
python launch.py permutation-diagnostic.log node diagnose_permutation.cjs
python launch.py compare-original.log python compare.py app.jsonl results-original
python launch.py compare-patched.log python compare.py patched-app.jsonl results-patched
python report.py
python launch.py verification.log python verify_artifacts.py
```

The corpus expanded during coverage review and was then reduced by source audit. Raw JSONL journals preserve all executed candidate configurations; final `app.json`, `patched-app.json`, `reference.json`, and totals select only IDs in the final corpus. The resume routines skip completed IDs; delete local output journals before an intentional completely fresh run.

## Every dataset: final disposition

| Dataset | Configurations | Reason/status |
|---|---:|---|
| dat.aloe2013 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.anand1999 | 32 | used; all eligible numeric moderators in recorded definitions |
| dat.anker2025 | 80 | used; all eligible numeric moderators in recorded definitions |
| dat.assink2016 | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.axfors2021 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.bakdash2021 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.baker2009 | 13 | used; all eligible numeric moderators in recorded definitions |
| dat.bangertdrowns2004 | 11 | used; all eligible numeric moderators in recorded definitions |
| dat.bartos2023 | 30 | used; all eligible numeric moderators in recorded definitions |
| dat.baskerville2012 | 15 | used; all eligible numeric moderators in recorded definitions |
| dat.bassler2004 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.bauer2002 | 18 | used; all eligible numeric moderators in recorded definitions |
| dat.bcg | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.begg1989 | 1 | used; all eligible numeric moderators in recorded definitions |
| dat.berkey1998 | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.berkey1998r | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.besson2016 | 26 | used; all eligible numeric moderators in recorded definitions |
| dat.bonett2010 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.bornmann2007 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.bourassa1996 | 18 | used; all eligible numeric moderators in recorded definitions |
| dat.cannon2006 | 98 | used; all eligible numeric moderators in recorded definitions |
| dat.chiarito2020 | 95 | used; all eligible numeric moderators in recorded definitions |
| dat.cohen1981 | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.colditz1994 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.collins1985a | 30 | used; all eligible numeric moderators in recorded definitions |
| dat.collins1985b | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.craft2003 | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.crede2010 | 9 | used; all eligible numeric moderators in recorded definitions |
| dat.crisafulli2020 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.curtin2002 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.curtis1998 | 29 | used; all eligible numeric moderators in recorded definitions |
| dat.dagostino1998 | 34 | used; all eligible numeric moderators in recorded definitions |
| dat.damico2009 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.debruin2009 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.demir2022 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.dogliotti2014 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.dong2013 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.dorn2007 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.dumouchel1994 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.egger2001 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.feng2019 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.fine1993 | 41 | used; all eligible numeric moderators in recorded definitions |
| dat.franchini2012 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.frank2008 | 24 | used; all eligible numeric moderators in recorded definitions |
| dat.furukawa2003 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.gibson2002 | 44 | used; all eligible numeric moderators in recorded definitions |
| dat.graves2010 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.greb2008 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.greenland1992 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.gurusamy2011 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.hackshaw1998 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.hahn2001 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.hannum2020 | 9 | used; all eligible numeric moderators in recorded definitions |
| dat.hart1999 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.hartmannboyce2018 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.hasselblad1998 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.higgins2008 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.hine1989 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.huber2000 | 0 | excluded: individual-participant recurrence records; no supplied study-level yi/vi or study-level moderator/variance combination |
| dat.ishak2007 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.kalaian1996 | 7 | used; all eligible numeric moderators in recorded definitions |
| dat.karner2014 | 192 | used; all eligible numeric moderators in recorded definitions |
| dat.kearon1998 | 25 | used; all eligible numeric moderators in recorded definitions |
| dat.knapp2017 | 7 | used; all eligible numeric moderators in recorded definitions |
| dat.konstantopoulos2011 | 1 | used; all eligible numeric moderators in recorded definitions |
| dat.landenberger2005 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.laopaiboon2015 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.lau1992 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.lee2004 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.lehmann2018 | 49 | used; all eligible numeric moderators in recorded definitions |
| dat.li2007 | 15 | used; all eligible numeric moderators in recorded definitions |
| dat.lim2014 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.linde2005 | 25 | used; all eligible numeric moderators in recorded definitions |
| dat.linde2015 | 50 | used; all eligible numeric moderators in recorded definitions |
| dat.linde2016 | 11 | used; all eligible numeric moderators in recorded definitions |
| dat.lloyd2010 | 16 | used; all eligible numeric moderators in recorded definitions |
| dat.lopez2019 | 23 | used; all eligible numeric moderators in recorded definitions |
| dat.maire2019 | 6 | used; all eligible numeric moderators in recorded definitions |
| dat.mccurdy2020 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.mcdaniel1994 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.meeker2017 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.metap | 0 | excluded: collections of p-values without paired study-level effect estimates and sampling variances |
| dat.michael2013 | 12 | used; all eligible numeric moderators in recorded definitions |
| dat.molloy2014 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.moore1998 | 9 | used; all eligible numeric moderators in recorded definitions |
| dat.moura2021 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.nakagawa2007 | 2 | used; all eligible numeric moderators in recorded definitions |
| dat.nielweise2007 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.nielweise2008 | 5 | used; all eligible numeric moderators in recorded definitions |
| dat.nissen2007 | 28 | used; all eligible numeric moderators in recorded definitions |
| dat.normand1999 | 18 | used; all eligible numeric moderators in recorded definitions |
| dat.obrien2003 | 29 | used; all eligible numeric moderators in recorded definitions |
| dat.pagliaro1992 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.pignon2000 | 9 | used; all eligible numeric moderators in recorded definitions |
| dat.poole2003 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.pritz1997 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.quan2000 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.raudenbush1985 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.riley2003 | 0 | excluded: effects and variances supplied, but remaining fields are identifiers, an SE, and a categorical outcome; no eligible varying numeric moderator |
| dat.rivera2025 | 32 | used; all eligible numeric moderators in recorded definitions |
| dat.roever2022 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.senn2013 | 9 | used; all eligible numeric moderators in recorded definitions |
| dat.spooner2002 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.steurer2006 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.stowe2010 | 14 | used; all eligible numeric moderators in recorded definitions |
| dat.tannersmith2016 | 3 | used; all eligible numeric moderators in recorded definitions |
| dat.thompson1999 | 8 | used; all eligible numeric moderators in recorded definitions |
| dat.tian2009 | 18 | used; all eligible numeric moderators in recorded definitions |
| dat.ursino2021 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.vanhowe1999 | 16 | used; all eligible numeric moderators in recorded definitions |
| dat.viechtbauer2021 | 20 | used; all eligible numeric moderators in recorded definitions |
| dat.white2020 | 4 | used; all eligible numeric moderators in recorded definitions |
| dat.woods2010 | 10 | used; all eligible numeric moderators in recorded definitions |
| dat.yusuf1985 | 4 | used; all eligible numeric moderators in recorded definitions |
