"""Tests of binary copying and fail-closed release identity/inventory checks."""
import hashlib
import json
import pytest
import finalize_blobs as final


def fixture_tree(tmp_path, initial=b"alpha\r\nbeta\r\n"):
    (tmp_path / "app").mkdir()
    (tmp_path / "validation-plus").mkdir()
    (tmp_path / "app/asset.bin").write_bytes(initial)
    (tmp_path / "RECUT_PROVENANCE.json").write_text(json.dumps({"app_assets": ["asset.bin"]}))
    (tmp_path / "validation-plus/UPSTREAM_SHA256.json").write_text("{}")
    entries = [{"archive_path": "app/asset.bin", "allmeta_path": "asset.bin"}]
    (tmp_path / "COPY_MAP.json").write_text(json.dumps(entries))
    return entries


def fake_git(raw, tag=final.COMMIT):
    def run(repo, *args):
        if args == ("rev-parse", "--verify", final.TAG + "^{commit}"):
            return (tag + "\n").encode()
        if args == ("rev-parse", "--verify", final.COMMIT + "^{commit}"):
            return (final.COMMIT + "\n").encode()
        if args[:2] == ("cat-file", "blob"):
            return raw
        if args[:2] == ("rev-parse", "--verify"):
            return (final.blob_id(raw) + "\n").encode()
        raise AssertionError(args)
    return run


def test_binary_identity_and_crlf_conversion(tmp_path):
    raw = b"alpha\nbeta\n\x00\xff\x80"
    entries = fixture_tree(tmp_path, b"alpha\r\nbeta\r\n\x00\xff\x80")
    final.load_map(tmp_path)
    blobs = final.collect_blobs(tmp_path, tmp_path, entries, fake_git(raw))
    final.materialize(blobs)
    assert (tmp_path / "app/asset.bin").read_bytes() == raw


def test_tag_mismatch_does_not_write(tmp_path):
    entries = fixture_tree(tmp_path)
    before = (tmp_path / "app/asset.bin").read_bytes()
    with pytest.raises(ValueError, match="Release identity"):
        final.collect_blobs(tmp_path, tmp_path, entries, fake_git(b"alpha\nbeta\n", "0" * 40))
    assert (tmp_path / "app/asset.bin").read_bytes() == before


def test_semantic_change_does_not_write(tmp_path):
    entries = fixture_tree(tmp_path)
    before = (tmp_path / "app/asset.bin").read_bytes()
    with pytest.raises(ValueError, match="Non-line-ending"):
        final.collect_blobs(tmp_path, tmp_path, entries, fake_git(b"changed source\n"))
    assert (tmp_path / "app/asset.bin").read_bytes() == before


def test_bad_git_object_hash_rejected(tmp_path):
    entries = fixture_tree(tmp_path)
    real = fake_git(b"alpha\nbeta\n")
    def bad(repo, *args):
        result = real(repo, *args)
        return b"0" * 40 if args[-1].endswith(":asset.bin") and args[0] == "rev-parse" else result
    with pytest.raises(ValueError, match="blob hash"):
        final.collect_blobs(tmp_path, tmp_path, entries, bad)


@pytest.mark.parametrize("path", ["../escape", "/absolute", "app/../../escape", ".git/config",
                                   "app/.GIT/config", "app\\asset.bin", "C:/asset", "", "app//asset.bin"])
def test_unsafe_paths_rejected(path):
    with pytest.raises(ValueError):
        final.safe_relative(path)


def test_missing_map_entry_rejected(tmp_path):
    fixture_tree(tmp_path)
    (tmp_path / "RECUT_PROVENANCE.json").write_text(json.dumps({"app_assets": ["asset.bin", "other.bin"]}))
    with pytest.raises(ValueError, match="exact current upstream inventory"):
        final.load_map(tmp_path)


def test_duplicate_target_rejected(tmp_path):
    entries = fixture_tree(tmp_path)
    (tmp_path / "COPY_MAP.json").write_text(json.dumps(entries + entries))
    with pytest.raises(ValueError, match="Duplicate"):
        final.load_map(tmp_path)


def test_no_write_until_all_sources_checked(tmp_path):
    entries = fixture_tree(tmp_path)
    other = tmp_path / "app/other.bin"
    other.write_bytes(b"original")
    entries.append({"archive_path": "app/other.bin", "allmeta_path": "other.bin"})
    before = (tmp_path / "app/asset.bin").read_bytes()
    with pytest.raises(ValueError, match="Non-line-ending"):
        final.collect_blobs(tmp_path, tmp_path, entries, fake_git(b"alpha\nbeta\n"))
    assert (tmp_path / "app/asset.bin").read_bytes() == before
    assert other.read_bytes() == b"original"
