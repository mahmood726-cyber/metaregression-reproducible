"""Prove the documented-difference negative test fails without its mutation."""
import ast
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MUTATION = "tab$index[1]<-99;"
TARGET = "reject(check_documented(tab,pins))"
MARKER = "R_GUARD_PLANT_TARGET"


def plant_code(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "test_r_guards"]
    if len(functions) != 1:
        raise ValueError("Expected one test_r_guards")
    values = [n.value for n in functions[0].body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "code" for t in n.targets)]
    if len(values) != 1:
        raise ValueError("Expected one embedded R snippet")
    code = ast.literal_eval(values[0])
    if code.count(MUTATION + TARGET) != 1:
        raise ValueError("Expected exactly one documented-index mutation")
    # Keep the actual reject call, and mark entry so an earlier R error cannot pass.
    return code.replace(MUTATION + TARGET, "cat('" + MARKER + "\\n');" + TARGET, 1)


def check_result(proc):
    if proc.returncode == 0:
        raise AssertionError("Plant check incorrectly accepted the uncorrupted table")
    if MARKER not in proc.stdout or "negative test did not reject" not in proc.stderr:
        raise AssertionError("Plant check failed before the intended negative assertion")
    if "R safeguard negative tests PASS" in proc.stdout:
        raise AssertionError("Plant check continued past the intended failure")


def main():
    out = ROOT / "outputs/recut"
    out.mkdir(parents=True, exist_ok=True)
    script = out / "r-guard-plant.R"
    script.write_text(plant_code(ROOT / "analysis/test_safeguards.py"), encoding="utf-8", newline="\n")
    proc = subprocess.run(["Rscript", str(script)], cwd=ROOT, capture_output=True, text=True)
    (out / "r-guard-plant.log").write_text(
        "R exit code: " + str(proc.returncode) + "\n" + proc.stdout + proc.stderr,
        encoding="utf-8", newline="\n")
    check_result(proc)
    print("R GUARD PLANT PASS: uncorrupted table triggers the expected negative-test failure")


if __name__ == "__main__":
    main()
