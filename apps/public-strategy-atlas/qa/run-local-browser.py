"""Keep localhost server and browser checks in one bounded execution lifetime."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import subprocess, sys, threading
APP=Path(__file__).resolve().parents[1]
allowed={'csoi-browser.py','system-browser.py','e0-browser.py','deep-browser.py','merge-browser.py','discovery-browser.py','integration-browser.py','intake-access-browser.py','run-browser-suite.py'}
scripts=sys.argv[1:] or ['csoi-browser.py']
if any(s not in allowed for s in scripts):raise SystemExit('UNRECOGNISED_LOCAL_BROWSER_SUITE')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8877),partial(Quiet,directory=str(APP)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 for script in scripts:
  result=subprocess.run([sys.executable,str(APP/'qa'/script)])
  if result.returncode:raise SystemExit(result.returncode)
finally:server.shutdown();server.server_close()
