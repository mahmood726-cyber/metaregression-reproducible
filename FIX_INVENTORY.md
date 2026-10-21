# Inventory regeneration attempt

Status: BLOCKED. Regeneration and verification both exited 1. No manifest or source code was changed; hashes were not hand-edited.

## Commands and outputs

Working directory: archive. -B prevents bytecode cache writes. Output excerpts:

    > python -B analysis/recut_integrity.py --help
    usage: recut_integrity.py [-h] [--executed] [--candidate CANDIDATE] {regenerate,verify}
    Exit code: 0

    > python -B analysis/recut_integrity.py regenerate
    AssertionError: Original evidence changed: analysis/test_safeguards.py
    Exit code: 1

    > python -B analysis/recut_integrity.py verify
    AssertionError: Source inventory/hash mismatch
    Exit code: 1

Regeneration fails inside verify_preserved() before either manifest write.

## Before/after entries

Stored hashes were unchanged by the attempted regeneration. Computed on-disk hashes below reflect the existing Rscript-call fix and were NOT written into the inventory.

| File | Stored before AND after attempt | Computed on disk |
|---|---|---|
| analysis/recut_preflight.py | db1f018aadf91c8c80723920d435f606683a12c44b6ef3a87e04dd66356c526b | 9c65e2a2ea66555913ccc5461745d9f3992a831af5eb1bb1be9d2b23945cdf8d |
| analysis/test_safeguards.py | 3ae7678294d168ba92a129457d6b6ad97ab8f90257f5a97e4fd4e843a942cdca | 35d55be2971a303fbacb7a726d5f1375d7ce8ef808d46b75049ac7a1fc017bb6 |

Read-only audit: imported recut_integrity.py with bytecode disabled; compared hashes(files(), ROOT) against SOURCE_SHA256.json. Exactly these two existing entries differ; the other 732 match. No inventoried files are missing. FIX_RCALL.md was the only unlisted path before this report. FIX_INVENTORY.md is also unlisted now; future regeneration must include both reports.

## Manifest hashes before and after the attempt

| Manifest | SHA-256 |
|---|---|
| SOURCE_SHA256.json | f93cbc00c75190e0d1f31fe868df89065b3cced8b579b6eff063ff9acd74e95b |
| app/app-sha256.json | c192d27eb6bae69585fb15ba5c14a2c3230d018eff1549108bbfd246b9b5b1c5 |
| validation-original/SOURCE_SHA256-v1.0.0.json | f2dfb6a531f0ce4a8100b4e565ea19e1625cd187a75fbacac179303b3d03bff1 |

## Required scope change

FIX_RCALL.md already documents this blocker: analysis/test_safeguards.py is historically pinned and absent from EDITABLE in analysis/recut_integrity.py. The proposed repair is adding that path to EDITABLE, then regenerating and verifying normally. It changes a third source hash (recut_integrity.py), contrary to the current two-file restriction; the historical manifest would stay untouched. This additional edit needs scope authorization.

No guard bypass, assertion disabling, historical-pin rewrite, code edit, or .git write was performed.

| Content | Static or dynamic | Evidence |
|---|---|---|
| Allowed helper paths | Static scope | TASK.md and FIX_RCALL.md |
| Command outcomes | Dynamic | Actual CLI exit codes and exceptions |
| Digests and entry counts | Dynamic | File reads using archive hashing functions |
| EDITABLE change | Unapplied proposal | Preservation check and FIX_RCALL.md |

Final read-only audit: PASS. All three manifests retain their initial hashes; the two previously changed helper hashes are unchanged; all 732 other entries still match; only FIX_INVENTORY.md was added by this task. The report is UTF-8 without BOM. Regeneration and verification remain FAIL.

INVENTORY_FIX_DONE
