"""Serve only the built site under the same project prefix as GitHub Pages."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit, unquote
import argparse
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=4173);p.add_argument('--base',default='/ProjectCobertizo/');p.add_argument('--directory',default='web/dist');a=p.parse_args()
root=Path(a.directory).resolve();base='/'+a.base.strip('/')+'/'
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  path=unquote(urlsplit(path).path)
  if not path.startswith(base):return str(root/'__outside_prefix__')
  relative=path[len(base):];resolved=(root/relative).resolve()
  if not resolved.is_relative_to(root):return str(root/'__outside_prefix__')
  return str(resolved)
print(f'Producción local: http://127.0.0.1:{a.port}{base}',flush=True)
ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
