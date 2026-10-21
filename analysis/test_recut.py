"""Integration guards for preserved evidence and candidate-only execution."""
import importlib.util
from pathlib import Path
import sys
import pytest
import recut_integrity as integrity
import recut

def test_preserved_protocol_and_extras_pins():
    assert integrity.verify_preserved()>0
    assert integrity.verify_plus()["checks"]==52767

def test_all_page_assets_and_copy_provenance():
    assert integrity.verify_assets()>0

def test_upstream_extras_mutation_is_rejected(monkeypatch,tmp_path):
    import shutil
    shutil.copytree(integrity.ROOT/"validation-plus",tmp_path/"validation-plus")
    target=tmp_path/"validation-plus/contract.js"
    target.write_bytes(target.read_bytes()+b"\n// mutation\n")
    monkeypatch.setattr(integrity,"ROOT",tmp_path)
    with pytest.raises(AssertionError,match="Upstream extras changed"):
        integrity.verify_plus()

def test_unexpected_original_file_mutation_is_rejected(monkeypatch):
    original=integrity.sha
    def changed(path):
        return "0"*64 if path.as_posix().endswith("/data/corpus.json") else original(path)
    monkeypatch.setattr(integrity,"sha",changed)
    with pytest.raises(AssertionError,match="Original evidence changed"):
        integrity.verify_preserved()

def test_wrapper_anchor_must_be_unique():
    with pytest.raises(ValueError):recut.replace_once("absent","needle","replacement")
    with pytest.raises(ValueError):recut.replace_once("xx","x","y")

def test_stale_stage_is_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(recut,"OUT",tmp_path)
    (tmp_path/"stage.json").write_text('{"source_manifest_sha256":"stale"}',encoding="utf-8")
    with pytest.raises(AssertionError,match="Source changed"):recut.require_stage()
