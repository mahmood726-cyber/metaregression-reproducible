"""Run a local command with UTF-8 logs, without shell redirection."""
import os, subprocess, sys
from pathlib import Path
env=os.environ.copy()
# R_LIBS_USER is supplied by the caller.
with open(sys.argv[1],'w',encoding='utf-8') as log:
 p=subprocess.Popen(sys.argv[2:],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 Path(sys.argv[1]+'.pid').write_text(str(p.pid),encoding='utf-8')
 for line in iter(p.stdout.readline,b''):
  text=line.decode('utf-8',errors='replace');log.write(text);log.flush();print(text,end='',flush=True)
 sys.exit(p.wait())
