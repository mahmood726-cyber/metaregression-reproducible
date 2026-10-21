"""Materialize pinned upstream Git blobs and run the archive's integrity scripts."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

COMMIT = "1cb3f8409c7af75ed41f7e1811f9c502f900fc79"
TAG = "v1.8.0"
ROOT = Path(__file__).resolve().parents[1]


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120
    ).stdout


def safe_relative(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Empty/non-string copy path")
    path = PurePosixPath(value)
    if (path.is_absolute() or path.as_posix() != value
            or any(part.casefold() in {"..", ".git"} for part in path.parts)
            or "\\" in value or ":" in value):
        raise ValueError("Unsafe copy path: " + value)
    return path


def load_map(root):
    entries = json.loads((root / "COPY_MAP.json").read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        raise ValueError("Copy map must be a nonempty list")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"archive_path", "allmeta_path"}:
            raise ValueError("Invalid copy-map entry")
        target = safe_relative(entry["archive_path"])
        source = safe_relative(entry["allmeta_path"])
        key = target.as_posix().casefold()
        if key in seen:
            raise ValueError("Duplicate copy target")
        seen.add(key)
        if not (root / target).resolve().is_relative_to(root.resolve()):
            raise ValueError("Copy target escapes archive")
        if target.parts[0] not in {"app", "validation-plus"}:
            raise ValueError("Copy target is outside current upstream-copy directories")
        if target.parts[0] == "app":
            if source.as_posix() != target.relative_to("app").as_posix():
                raise ValueError("App source mapping differs")
        elif source.as_posix() != "meta-regression/validate/" + target.relative_to("validation-plus").as_posix():
            raise ValueError("Extras source mapping differs")
    assets = json.loads((root / "RECUT_PROVENANCE.json").read_text())["app_assets"]
    extras = json.loads((root / "validation-plus/UPSTREAM_SHA256.json").read_text())
    expected = {"app/" + name for name in assets} | {"validation-plus/" + name for name in extras}
    if {entry["archive_path"] for entry in entries} != expected:
        raise ValueError("Copy map does not cover the exact current upstream inventory")
    return entries


def blob_id(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def collect_blobs(root, repo, entries, read_git=git):
    # Resolve both identifiers independently. No trust in checkout bytes/autocrlf.
    for ref in [TAG + "^{commit}", COMMIT + "^{commit}"]:
        resolved = read_git(repo, "rev-parse", "--verify", ref).decode("ascii").strip()
        if resolved != COMMIT:
            raise ValueError("Release identity mismatch")
    blobs = []
    for entry in entries:
        spec = COMMIT + ":" + entry["allmeta_path"]
        raw = read_git(repo, "cat-file", "blob", spec)
        expected = read_git(repo, "rev-parse", "--verify", spec).decode("ascii").strip()
        if blob_id(raw) != expected:
            raise ValueError("Git blob hash mismatch: " + entry["allmeta_path"])
        path = root / entry["archive_path"]
        if not path.is_file():
            raise ValueError("Missing archive copy target: " + entry["archive_path"])
        before = path.read_bytes()
        # This finalizer is only a checkout-to-blob conversion. Semantic drift
        # requires a new validation run, not an automatic source repin.
        if before != raw and before.replace(b"\r\n", b"\n") != raw:
            raise ValueError("Non-line-ending source change: " + entry["archive_path"])
        blobs.append((path, raw))
    return blobs


def materialize(blobs):
    # Every source and destination has already passed preflight.
    for path, raw in blobs:
        if path.read_bytes() != raw:
            path.write_bytes(raw)
    for path, raw in blobs:
        if path.read_bytes() != raw:
            raise RuntimeError("Post-write blob mismatch: " + path.name)
    print(f"BLOB PASS {len(blobs)}/{len(blobs)}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allmeta", type=Path, default=ROOT.parent / "allmeta")
    parser.add_argument("--check-only", action="store_true",
                        help="Verify all mapped copies already equal pinned Git blobs; do not write")
    args = parser.parse_args(argv)
    repo = args.allmeta.resolve()
    entries = load_map(ROOT)
    blobs = collect_blobs(ROOT, repo, entries)
    if args.check_only:
        if any(path.read_bytes() != raw for path, raw in blobs):
            raise ValueError("Archive still contains checkout bytes; run without --check-only")
        print(f"BLOB PASS {len(blobs)}/{len(blobs)}", flush=True)
        return
    materialize(blobs)
    for command in [
        ["analysis/recut_integrity.py", "regenerate"],
        ["analysis/recut_integrity.py", "verify"],
        ["analysis/verify_archive.py"],
    ]:
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True, timeout=300)
    print("FINAL BLOBS AND ARCHIVE MANIFESTS PASS", flush=True)


if __name__ == "__main__":
    main()
