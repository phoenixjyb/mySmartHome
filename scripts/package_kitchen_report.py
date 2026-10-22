#!/usr/bin/env python3
"""Package the generated kitchen report for same-origin static hosting."""
from __future__ import annotations
import argparse, base64, hashlib, json, re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'exports/北京厨房电器选型_2026-10-22.html'
class Audit(HTMLParser):
 def __init__(self): super().__init__(); self.images=[]; self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='img' and a.get('src'):self.images.append(a['src'])
  if tag=='a':self.links.append(a.get('href',''))
def package(dst:Path):
 if dst.exists(): raise ValueError('Output directory exists; choose a new path to preserve existing files.')
 page=SOURCE.read_text()
 for bad in ('/Users/','file://','codex://','refrigerator_jd_handoff','chatgpt.com/c/'):
  if bad.lower() in page.lower(): raise ValueError('Forbidden private/local reference in HTML: '+bad)
 files={}
 def extract(m):
  fmt,payload=m.groups(); body=base64.b64decode(payload,validate=True)
  if fmt=='png' and not body.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG payload')
  if fmt=='jpeg' and not body.startswith(b'\xff\xd8\xff'):raise ValueError('Invalid JPEG payload')
  digest=hashlib.sha256(body).hexdigest(); name='images/'+digest[:24]+('.png' if fmt=='png' else '.jpg'); files[name]=body; return name
 page=re.sub(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)',extract,page)
 if len(files)!=8 or 'data:image/' in page:raise ValueError(f'Expected 8 embedded gallery assets; found {len(files)}')
 page=page.replace('<meta name="color-scheme" content="light">','<meta name="color-scheme" content="light"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">')
 if re.search(r'(?:href|src)=["\'](?:\.\.?/|/Users/|file:|codex:)',page,re.I):raise ValueError('Local or non-public link remains')
 audit=Audit(); audit.feed(page)
 if len(audit.images)!=8 or set(audit.images)!=set(files):raise ValueError('Gallery references do not match image manifest')
 for href in audit.links:
  if href.startswith('#'):
   if href[1:] and href[1:] not in audit.ids: raise ValueError('Broken anchor: '+href)
  elif not href.startswith('https://'):raise ValueError('Non-HTTPS public link: '+href)
 dst.mkdir(parents=True); (dst/'images').mkdir()
 files['index.html']=page.encode()
 entries=[]
 for name,body in sorted(files.items()):
  target=dst/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(body)
  entries.append({'path':name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
 (dst/'manifest.json').write_text(json.dumps({'format':1,'files':entries},ensure_ascii=False,indent=2)+'\n')
 return {'payloads':len(entries),'images':len(entries)-1,'bytes':sum(e['bytes'] for e in entries),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);a=p.parse_args();print(json.dumps(package(a.destination.resolve()),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
