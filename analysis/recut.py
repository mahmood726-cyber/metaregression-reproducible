"""Archive-local recut wrappers. Upstream scripts and pinned evidence stay unchanged."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".validate-work/recut"
OUT = ROOT / "outputs/recut"
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8", newline="\n")
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def replace_once(text, old, new):
    if text.count(old) != 1: raise ValueError("Upstream wrapper anchor changed: "+old)
    return text.replace(old, new, 1)
def prepare():
    from recut_integrity import verify
    verify()
    WORK.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    stage = WORK / "app"
    if stage.exists():
        assert stage.resolve().is_relative_to((ROOT/".validate-work").resolve())
        shutil.rmtree(stage)
    shutil.copytree(ROOT/"app",stage)
    shutil.copytree(ROOT/"validation-plus",stage/"meta-regression/validate",dirs_exist_ok=True)
    text = (ROOT/"bench/run_app.cjs").read_text(encoding="utf-8")
    text = replace_once(text,"require('<PLAYWRIGHT_MODULE>')","require(process.env.PLAYWRIGHT_MODULE||'playwright')")
    text = replace_once(text,"fs.readFileSync('corpus.json','utf8')","fs.readFileSync('data/corpus.json','utf8')")
    text = replace_once(text,"channel:'chrome'","channel:process.env.PW_CHANNEL||'msedge'")
    text = replace_once(text,"await page.route('https://**/*',r=>r.abort());await page.route('http://**/*',r=>r.abort());",
                        "await page.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8000'?r.continue():r.abort());")
    text = replace_once(text,"require('url').pathToFileURL(path.resolve(root,'meta-regression/index.html')).href",
                        "'http://127.0.0.1:8000/meta-regression/index.html'")
    text = replace_once(text,"const browser=await chromium.launch","browser=await chromium.launch")
    text = replace_once(text,"(async()=>{","let browser;\n(async()=>{")
    text = replace_once(text,"})().catch(e=>{console.error(e);process.exit(1)});",
                        "})().catch(async e=>{console.error(e);if(browser)await browser.close();process.exitCode=1;});")
    (WORK/"run-original.cjs").write_text(text,encoding="utf-8",newline="\n")
    smoke=(ROOT/"bench/ui_smoke.cjs").read_text(encoding="utf-8")
    smoke=replace_once(smoke,"channel:'chrome'","channel:process.env.PW_CHANNEL||'msedge'")
    smoke=replace_once(smoke,"'outputs/ui-smoke.png'","'outputs/recut/ui-smoke.png'")
    smoke=replace_once(smoke,"'results/ui-smoke.json'","'outputs/recut/ui-smoke.json'")
    smoke=replace_once(smoke,"await page.route('https://**/*',r=>r.abort());await page.route('http://**/*',r=>r.abort());",
                       "await page.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8000'?r.continue():r.abort());")
    smoke=replace_once(smoke,"require('url').pathToFileURL(path.resolve(root,'meta-regression/index.html')).href",
                       "'http://127.0.0.1:8000/meta-regression/index.html'")
    smoke=replace_once(smoke,"const root=process.argv[2]||'app';const browser=","const root=process.argv[2]||'app';browser=")
    smoke=replace_once(smoke,"(async()=>{","let browser;\n(async()=>{")
    smoke=replace_once(smoke,"})().catch(e=>{console.error(e);process.exit(1)});",
                       "})().catch(async e=>{console.error(e);if(browser)await browser.close();process.exitCode=1;});")
    (WORK/"ui-smoke.cjs").write_text(smoke,encoding="utf-8",newline="\n")
    dump(OUT/"stage.json",{"source_manifest_sha256":digest(ROOT/"SOURCE_SHA256.json")})
    print("Prepared clean wrappers and extras stage; original evidence preserved.")
def require_stage():
    record=json.loads((OUT/"stage.json").read_text())
    assert record["source_manifest_sha256"]==digest(ROOT/"SOURCE_SHA256.json"),"Source changed: prepare again"
    pins=json.loads((ROOT/"app/app-sha256.json").read_text())
    for name,value in pins.items():
        assert digest(WORK/"app"/name)==value,"Staged app/input changed: prepare again: "+name
def run(label, command, cwd=ROOT, serve=False):
    require_stage()
    server=None; thread=None
    if serve:
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self,*args): pass
        server=ThreadingHTTPServer(("127.0.0.1",8000),partial(QuietHandler,directory=str(ROOT/"app")))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with (OUT/(label+".log")).open("w",encoding="utf-8",newline="\n") as log:
            proc=subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                  text=True,encoding="utf-8",errors="replace")
            for line in proc.stdout:
                print(line,end="",flush=True);log.write(line);log.flush()
            status=proc.wait()
        if status: raise subprocess.CalledProcessError(status,command)
    finally:
        if server:
            server.shutdown();server.server_close();thread.join(timeout=5)
def compare_original():
    from checks import read, loads, indexed, inputs, compare, documented
    c,b,old,r,p=inputs(ROOT)
    fresh=indexed([loads(line) for line in (OUT/"original-app.jsonl").read_text(encoding="utf-8").splitlines()],len(c),c)
    changed=[key for key in c if fresh[key]!=old[key]]
    assert not changed, f"Original records changed ({len(changed)}): {changed[:10]}"
    rows=compare(c,fresh,r,p);documented(rows,read(ROOT/"expected/documented_differences.json"))
    primary=[x for x in rows if x["group"]!="LS experimental"]
    ls=[x for x in rows if x["group"]=="LS experimental"]
    result={"identical_configurations":len(c),"configurations":len(c),"checks":len(primary),
            "passed":sum(x["passed"] for x in primary),"documented":sum(not x["passed"] for x in primary),
            "unexpected":0,"LS_checks":len(ls),"LS_passed":sum(x["passed"] for x in ls),
            "source_manifest_sha256":digest(ROOT/"SOURCE_SHA256.json"),
            "journal_sha256":digest(OUT/"original-app.jsonl")}
    dump(OUT/"original-comparison.json",result)
    print(f'{len(c)}/{len(c)} original configurations identical; {result["passed"]}/{result["checks"]} primary checks; {result["documented"]} documented, 0 unexpected')
    print(f'{result["LS_passed"]}/{result["LS_checks"]} experimental LS checks (separate)')
def numeric_result():
    manifest=json.loads((ROOT/"validation-plus/MANIFEST-plus.json").read_text())
    path=WORK/"app/meta-regression/validate/plus/numeric-evidence.json"
    result=json.loads(path.read_text())
    assert result["configurations"]==manifest["configurations"]
    assert result["checks"]==result["passed"]==manifest["numericChecks"] and result["failed"]==[]
    dump(OUT/"plus-numeric.json",dict(result,source_manifest_sha256=digest(ROOT/"SOURCE_SHA256.json")))
    print(f'{result["passed"]}/{result["checks"]} extras numerical checks pass')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["prepare","original","compare-original","ui","numeric","dom","browser","generate-plus"])
    args=parser.parse_args()
    if args.command=="prepare":prepare();return
    require_stage()
    if args.command=="original":
        (OUT/"original-app.jsonl").unlink(missing_ok=True)
        (OUT/"original-comparison.json").unlink(missing_ok=True)
        run("original-browser",["node",str(WORK/"run-original.cjs"),"app","outputs/recut/original-app.jsonl"],serve=True)
    elif args.command=="compare-original":compare_original()
    elif args.command=="ui":
        (OUT/"ui-smoke.json").unlink(missing_ok=True)
        run("ui-smoke",["node",str(WORK/"ui-smoke.cjs"),"app"],serve=True)
    elif args.command=="numeric":
        (OUT/"plus-numeric.json").unlink(missing_ok=True)
        (WORK/"app/meta-regression/validate/plus/numeric-evidence.json").unlink(missing_ok=True)
        run("plus-numeric",["node",str(WORK/"app/meta-regression/validate/check-numeric.mjs")])
        numeric_result()
    elif args.command=="dom":
        run("plus-dom",["node","--test-isolation=none","--test",str(WORK/"app/meta-regression/validate/numeric.test.mjs")])
    elif args.command=="browser":
        (OUT/"plus-browser.json").unlink(missing_ok=True)
        run("plus-browser",["node","analysis/recut_browser.cjs"],serve=True)
    else:
        run("plus-generate",["Rscript","meta-regression/validate/generate-plus.R"],cwd=WORK/"app")
        print("Generated staged R files only. Review against pinned files; do not replace archive references or pins.")
if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
