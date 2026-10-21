# Rscript multiline-call fix

Changed:
- `analysis/recut_preflight.py`: added `tempfile`; the package/version preflight now writes its existing R code to a UTF-8 temporary `.R` file.
- `analysis/test_safeguards.py`: the multiline `test_r_guards` code uses the same temporary-file pattern.

The files close before Rscript runs and are deleted in `finally`, including failure paths. `newline=""` preserves the R payload bytes on Windows.

| File | Before call | After call |
|---|---|---|
| `analysis/recut_preflight.py` | `subprocess.run(["Rscript","-e",r],check=True)` | `subprocess.run(["Rscript",script.name],check=True)` |
| `analysis/test_safeguards.py` | `proc=subprocess.run(['Rscript','-e',code],cwd=ROOT,capture_output=True,text=True)` | `proc=subprocess.run(['Rscript',script.name],cwd=ROOT,capture_output=True,text=True)` |

The single-line `test_version_guards` call remains unchanged.

| Content | Static or dynamic | Validation |
|---|---|---|
| R source | Preserved static content | Original source text and UTF-8 payload bytes match exactly |
| Temporary-file transport | Dynamic Python checks | 8 passed: success, nonzero exit, launch error and write error for each helper |
| Existing Python safeguards | Dynamic pytest results | 47 passed, 1 failed, 3 R-dependent cases deselected |
| Real R execution | Pending external runner | Not attempted, per TASK.md |

Python transport check: `python -X utf8 outputs/recut/rcall_verify.py`.

The pytest failure is `test_preserved_protocol_and_extras_pins`: the original historical manifest pins `analysis/test_safeguards.py` as immutable. The archive's own `python analysis/recut_integrity.py regenerate` fails with the same preservation assertion before writing manifests.

Awaiting approval for the precise extra edit: add `"analysis/test_safeguards.py"` to `EDITABLE` in `analysis/recut_integrity.py`. Historical manifest bytes remain untouched. After approval, regenerate `SOURCE_SHA256.json` with that script, run its `verify`, and repeat the Python safeguards.

Local check artifacts are under `outputs/recut/`, already excluded from the source inventory. Pytest uses a workspace temporary-directory fixture and disables unrelated plugin autoloading and the built-in tmpdir plugin because of the sandbox limitations documented in `STUCK_FAILURES.md`. Test bodies and assertions are unchanged.
