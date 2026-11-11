"""Loopback-only preview of exactly the public expedition app and research archive."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,unquote
ROOT=Path(__file__).resolve().parents[2]
ALLOWED=[ROOT/'apps/earth-science-expedition',ROOT/'docs/research/world-science-expedition']
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT),**kw)
    def do_GET(self):
        if self.path=='/':
            self.send_response(302);self.send_header('Location','/apps/earth-science-expedition/index.html');self.end_headers();return
        p=(ROOT/unquote(urlparse(self.path).path).lstrip('/')).resolve()
        if not any(p.is_relative_to(x) for x in ALLOWED) or any(part.startswith('.') for part in p.relative_to(ROOT).parts):
            self.send_error(404);return
        super().do_GET()
    def do_HEAD(self):
        p=(ROOT/unquote(urlparse(self.path).path).lstrip('/')).resolve()
        if not any(p.is_relative_to(x) for x in ALLOWED):self.send_error(404);return
        super().do_HEAD()
    def list_directory(self,path):self.send_error(404);return None
if __name__=='__main__':
    print('Local preview: http://127.0.0.1:8896/apps/earth-science-expedition/index.html',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8896),Handler).serve_forever()
