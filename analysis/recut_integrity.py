"""Deterministic recut manifests and preservation checks; does not certify runtime results."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={".git","__pycache__",".pytest_cache","outputs",".validate-work","node_modules"}
EDITABLE={".gitignore",".zenodo.json","CITATION.cff","README.md","CHANGELOG.md","analysis/verify_archive.py","analysis/test_safeguards.py"}
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def files(root=ROOT):
    found=[]
    for directory, dirs, names in os.walk(root):
        dirs[:]=[name for name in dirs if name not in EXCLUDED and not name.startswith(".verify-")]
        for name in names:
            path=Path(directory)/name
            if path.relative_to(root).as_posix() not in {"SOURCE_SHA256.json","PROGRESS.md"}:found.append(path)
    return sorted(found)
def hashes(paths,root): return {p.relative_to(root).as_posix():sha(p) for p in paths}
def write(path,value): path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def flatten(x,prefix="",out=None):
    if out is None: out={}
    if isinstance(x,list):
        out[prefix+".length"]=len(x)
        for i,value in enumerate(x): flatten(value,prefix+"."+str(i),out)
    elif isinstance(x,dict):
        for k,value in x.items():flatten(value,(prefix+"." if prefix else "")+k,out)
    else:out[prefix]=x
    return out
def verify_preserved():
    old=read(ROOT/"validation-original/SOURCE_SHA256-v1.0.0.json")
    checked=0
    for name,value in old.items():
        if name in EDITABLE or name.startswith("app/"): continue
        assert sha(ROOT/name)==value,"Original evidence changed: "+name
        checked+=1
    for name,value in read(ROOT/"INPUT_SHA256.json").items():
        assert sha(ROOT/name)==value,"Original R input changed: "+name
    return checked
def verify_plus():
    upstream=read(ROOT/"validation-plus/UPSTREAM_SHA256.json")
    for name,value in upstream.items():
        assert sha(ROOT/"validation-plus"/name)==value,"Upstream extras changed: "+name
    manifest=read(ROOT/"validation-plus/MANIFEST-plus.json")
    for item in manifest["files"]:
        relative=Path(item["path"]).relative_to("validate")
        for p in [ROOT/"validation-plus"/relative,ROOT/"app/meta-regression"/item["path"]]:
            assert p.stat().st_size==item["bytes"] and sha(p)==item["sha256"],"Extras pin mismatch: "+str(p)
            assert b"\r" not in p.read_bytes(),"Pinned extras bytes must remain LF"
    corpus=read(ROOT/"validation-plus/plus/corpus.json")
    refs=read(ROOT/"validation-plus/plus/reference.json")
    assert [x["id"] for x in corpus]==[x["id"] for x in refs],"Extras ID/order mismatch"
    assert len({x["id"] for x in corpus})==len(corpus)==manifest["configurations"]==194
    count=sum(len(flatten(x["result"]))+1 for x in refs)
    assert count==manifest["numericChecks"]==52573
    assert count+len(corpus)==manifest["checks"]==52767
    assert manifest["versions"]["metafor"]=="5.2-1"
    for rel in ["contract.js","plus-pins.js","plus-adapter.js"]:
        assert (ROOT/"validation-plus"/rel).read_bytes()==(ROOT/"app/meta-regression/validate"/rel).read_bytes()
    return manifest
def verify_assets(candidate=None):
    app=ROOT/"app"; pins=read(app/"app-sha256.json")
    actual=hashes([p for p in app.rglob("*") if p.is_file() and p.name!="app-sha256.json"],app)
    assert pins and pins==actual,"App inventory/hash mismatch"
    provenance=read(ROOT/"RECUT_PROVENANCE.json")
    assert sorted(pins)==provenance["app_assets"],"App provenance inventory mismatch"
    for edge in provenance["dependency_edges"]:
        assert edge["target"] in pins,"Unarchived dependency"
    class PageAssets(HTMLParser):
        def handle_starttag(self,tag,attrs):
            a=dict(attrs); value=a.get("src") if tag=="script" else a.get("href") if tag=="link" else None
            if not value or re.match(r"(?:[a-z]+:|//|#)",value):return
            target=(app/"meta-regression"/value.split("?")[0].split("#")[0]).resolve()
            assert target.is_relative_to(app.resolve()) and target.is_file(),"Missing page dependency: "+value
    PageAssets().feed((app/"meta-regression/index.html").read_text(encoding="utf-8"))
    if candidate:
        for name,value in pins.items():
            assert sha(candidate/name)==value,"Candidate copy differs: "+name
        for name,value in read(ROOT/"validation-plus/UPSTREAM_SHA256.json").items():
            assert sha(candidate/"meta-regression/validate"/name)==value,"Candidate extras differ: "+name
    return len(pins)
def verify(executed=False,candidate=None):
    assert read(ROOT/"SOURCE_SHA256.json")==hashes(files(),ROOT),"Source inventory/hash mismatch"
    preserved=verify_preserved()
    n=verify_assets(candidate); m=verify_plus()
    if executed:
        root=ROOT/"outputs/recut"; stamp=sha(ROOT/"SOURCE_SHA256.json")
        a=read(root/"original-comparison.json")
        assert a["identical_configurations"]==a["configurations"]==1742
        assert (a["passed"],a["checks"],a["documented"],a["unexpected"])==(129867,129903,36,0)
        assert a["journal_sha256"]==sha(root/"original-app.jsonl")
        for name,want in [("plus-numeric.json",m["numericChecks"]),("plus-browser.json",m["checks"])]:
            result=read(root/name)
            assert result["passed"]==result["checks"]==want and result["failed"]==[]
            assert result["source_manifest_sha256"]==stamp,"Stale execution evidence"
        assert a["source_manifest_sha256"]==stamp,"Stale original replay"
        ui=read(root/"ui-smoke.json")
        assert len(ui)==4 and all(x["pass"] is True for x in ui)
        print("EXECUTED REPLAY GATES PASS: 1742/1742; 129867/129903; 52573/52573; 52767/52767; UI 4/4")
    print(f"RECUT INTEGRITY PASS: {n} app files; {preserved} original files unchanged; extras pins and coverage verified")
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["regenerate","verify"])
    parser.add_argument("--executed",action="store_true")
    parser.add_argument("--candidate",type=Path)
    args=parser.parse_args()
    if args.command=="regenerate":
        verify_preserved();verify_plus()
        app=ROOT/"app"
        actual=hashes([p for p in app.rglob("*") if p.is_file() and p.name!="app-sha256.json"],app)
        assert sorted(actual)==read(ROOT/"RECUT_PROVENANCE.json")["app_assets"]
        write(app/"app-sha256.json",actual)
        write(ROOT/"SOURCE_SHA256.json",hashes(files(),ROOT))
        print("Regenerated app/app-sha256.json and SOURCE_SHA256.json; original and extras pins unchanged")
    else:verify(args.executed,args.candidate)
if __name__=="__main__":main()
