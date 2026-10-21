"""Human-runner preflight. This intentionally starts Node and R; do not run in the preparation sandbox."""
import importlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
assert not sys.flags.optimize,"Run validation without Python -O"
for name in ["pytest","matplotlib","matplotlib.pyplot","PIL.Image","scipy.stats","yaml"]:
    importlib.import_module(name)
for name in ["node","Rscript"]:
    if not shutil.which(name):raise RuntimeError("Missing executable: "+name)
for name in ["data/corpus.json","results/patched-app.json","validate.R","bench/run_app.cjs",
             "bench/ui_smoke.cjs","validation-plus/MANIFEST-plus.json","analysis/recut_browser.cjs"]:
    assert (ROOT/name).is_file(),"Missing command target: "+name
subprocess.run(["node","--test-isolation=none","--version"],check=True)
node=r"""
const {pathToFileURL}=require('node:url');
(async()=>{
 const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
 await import(process.env.LINKEDOM_MODULE?pathToFileURL(process.env.LINKEDOM_MODULE).href:'linkedom');
 const browser=await chromium.launch({channel:process.env.PW_CHANNEL||'msedge',headless:true});
 try{console.log('Browser preflight: '+browser.version());}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
"""
subprocess.run(["node","-e",node],check=True)
r=r"""
stopifnot(as.character(getRversion())=='4.6.0')
for(p in c('metafor','metadat','jsonlite','digest'))stopifnot(requireNamespace(p,quietly=TRUE))
stopifnot(as.character(packageVersion('metafor'))=='5.2.1',
          as.character(packageVersion('metadat'))=='1.6.0',
          as.character(packageVersion('jsonlite'))=='2.0.0')
cat('R 4.6.0; metafor 5.2.1; metadat 1.6.0; jsonlite 2.0.0; digest available\n')
"""
script=tempfile.NamedTemporaryFile(suffix=".R",delete=False,mode="w",encoding="utf-8",newline="")
try:
    with script:
        script.write(r)
    subprocess.run(["Rscript",script.name],check=True)
finally:
    Path(script.name).unlink()
print("Preflight PASS: command targets, Python, Node, browser, linkedom and R packages")
