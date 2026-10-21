# Preparation environment blockers

TASK.md explicitly requires deferring Node, Git, R/Rscript and PowerShell because
these programs cannot start in the sandbox (Windows 0xC0000142). No Node, Git or R
execution was attempted after reading that instruction. Initial PowerShell
discovery calls failed before the task was readable; cmd plus Python works.

Python module preflight also found:
- matplotlib: DLL initialization failure importing _c_internal_utils.
- scipy: extension modules cannot be imported.
- Pillow: DLL initialization failure importing _imaging.
- An unrelated auto-loaded pytest plugin imports _ssl, which also fails to initialize. The runner disables plugin auto-loading; neither requested suite needs external pytest plugins.

Consequently figure regeneration, the full historical archive verifier, three
R-backed safeguard tests, browser/E2E checks and extras Node/DOM tests required
the human-side runner during preparation. The recorded 2026-10-21 release run
subsequently passed those gates; these sandbox restrictions still apply to
local finalization verification. This is an environment limitation, not a numerical PASS.
RUN_PLAN.cmd performs dependency preflight and all deferred checks, stopping on
any failure. No references, expected counts or tolerances were weakened.

The archive verifier now imports figure-building dependencies only when its main
routine runs, so the independent Python safeguards remain executable here.

Pytest's default temporary directory also produced a sandbox ACL denial. The
local preparation run used a pytest tmp_path fixture with normal inherited
workspace permissions and disabled the built-in tmpdir plugin. All test bodies
and assertions were unchanged. The human runner uses the ordinary pytest suite.


## Finalization blockers (2026-10-21)

1. Privacy versus exact-copy requirements: three pinned upstream extras logs
   contain local installation paths; protected upstream documents and libraries
   contain public contacts and virtual runtime paths. Sanitizing all would alter
   required upstream/historical bytes. User clarification is pending. Every
   scan hit and the completed runner/hostname redactions are in RECUT_NOTES.md.
2. The archive v1.0.0 DOI is absent from supplied and checked public metadata.
   The existing older allmeta DOI is preserved without mislabelling it. User
   clarification is pending; the required archive-version DOI relation cannot
   be fabricated.
3. Full local archive verification exits 1 while importing Matplotlib's native
   extension (DLL initialization failure). The 64 available Python tests and
   integrity checks pass; 3 R-backed tests remain delegated. FINAL_BLOBS.cmd
   includes full verification for the human runner after exact blob copying.

No publication clearance, fresh R/Node execution, or Git-blob PASS is claimed
for this sandbox finalization. No source pin was relaxed to hide these blockers.
