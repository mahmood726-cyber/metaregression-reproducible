# Reproduction report

Values below are recomputed; expected values are assertions.

| Claim | Expected | Reproduced | Verdict |
|---|---|---|---|
| datasets_screened | 114 | 114 | PASS |
| datasets_used | 111 | 111 | PASS |
| effect_definitions | 223 | 223 | PASS |
| configurations | 1742 | 1742 | PASS |
| checks | 129903 | 129903 | PASS |
| passed | 129867 | 129867 | PASS |
| before_passed | 115139 | 115139 | PASS |
| model_checks | 34840 | 34840 | PASS |
| model_passed | 34818 | 34818 | PASS |
| bubble_checks | 87000 | 87000 | PASS |
| bubble_passed | 86986 | 86986 | PASS |
| permutation_checks | 1095 | 1095 | PASS |
| permutation_passed | 1095 | 1095 | PASS |
| structural_checks | 6968 | 6968 | PASS |
| structural_passed | 6968 | 6968 | PASS |
| permutation_configurations | 365 | 365 | PASS |
| documented_checks | 36 | 36 | PASS |
| documented_configurations | 14 | 14 | PASS |
| year_configurations | 8 | 8 | PASS |
| LS_checks | 91515 | 91515 | PASS |
| LS_passed | 82680 | 82680 | PASS |
| LS_alpha_checks | 3280 | 3280 | PASS |
| LS_alpha_passed | 1893 | 1893 | PASS |
| version_R | R version 4.6.0 (2026-04-24 ucrt) | R version 4.6.0 (2026-04-24 ucrt) | PASS |
| version_metafor | 5.2.1 | 5.2.1 | PASS |
| version_metadat | 1.6.0 | 1.6.0 | PASS |
| commit | e47acf19f13d36feac52fc414d3c9782012155cc | e47acf19f13d36feac52fc414d3c9782012155cc | PASS |
| pull_request | 89 | 89 | PASS |
| usecase_slope | -0.0286 | -0.0286 | PASS |
| usecase_ci_lower | -0.0485 | -0.0485 | PASS |
| usecase_ci_upper | -0.0086 | -0.0086 | PASS |
| usecase_slope_p | 0.009 | 0.009 | PASS |
| usecase_tau2 | 0.142 | 0.142 | PASS |
| usecase_R2_percent | 55.3 | 55.3 | PASS |
| usecase_QE | 30.73 | 30.73 | PASS |
| usecase_df | 11 | 11 | PASS |
| usecase_QE_p | 0.001 | 0.001 | PASS |
| difference_min | 1e-09 | 1e-09 | PASS |
| difference_max | 1.1e-07 | 1.1e-07 | PASS |
| centered_max | 3e-11 | 3e-11 | PASS |

Centered refits diagnose conditioning; they do not replace the prespecified raw reference. Figures are 300 dpi, nominal 170 mm wide, text at least 8 pt. The browser UI is replayed historical evidence in the R command; main and experimental LS references and exact permutations are freshly computed. Publication LS totals here remain the historical run. No manuscript draft is distributed.

PASS: 40/40 paper-value assertions; 129867/129903 non-LS checks; 36 documented differences; LS 82680/91515 (experimental).
