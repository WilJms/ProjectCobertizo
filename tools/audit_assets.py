"""Check every state URI, GLB compression/UV contract, EXR channel precision and sizes."""
import json,struct,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'web/public';m=json.loads((P/'assets/scene-manifest.json').read_text());models=[];maps=[];missing=[]
config=json.loads((R/'config/scene-parameters.json').read_text());assert m['spatialRevision']==config['spatial_revision']
assert len(m['states'])==6
assert hashlib.sha256((R/m['source']).read_bytes()).hexdigest()==m['sourceSha256'], 'Master does not match manifest'
assert m['navigation']['pool']==config['geometry']['pool_outline_xy_m']
assert m['navigation']['deck']==config['geometry']['deck_footprint_xy_m']
mesh_contract={}
def cstring(data,offset):
 end=data.index(0,offset);return data[offset:end].decode(),end+1
for path in sorted((P/'assets/models').glob('*.glb')):
 b=path.read_bytes();assert b[:4]==b'glTF';n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);primitives=[p for mesh in g['meshes'] for p in mesh['primitives']];models.append({'path':str(path.relative_to(R)),'bytes':len(b),'extensions':g.get('extensionsUsed',[]),'primitives':len(primitives),'uv1_primitives':sum('TEXCOORD_1' in p['attributes'] for p in primitives),'meshIds':[n.get('extras',{}).get('meshId') for n in g['nodes'] if n.get('extras',{}).get('meshId')]})
 assert 'EXT_meshopt_compression' in g.get('extensionsUsed',[])
 for node in g['nodes']:
  mesh_id=node.get('extras',{}).get('meshId')
  if mesh_id and 'mesh' in node:mesh_contract[mesh_id]=g['meshes'][node['mesh']]['primitives']
for key,state in m['states'].items():
 uris=[m['commonModel'],state['model'],state['environment']['uri'],state['render']]
 for lm in state['lightmaps']:
  assert lm['meshId'] in mesh_contract,lm['meshId']
  assert all('TEXCOORD_1' in p['attributes'] for p in mesh_contract[lm['meshId']])
  for q in ['high','balanced','low']:
   uri=lm['uri'] if q=='high' else lm['uri'].replace('.exr','--'+q+'.exr');uris.append(uri);p=P/uri
   if not p.exists():continue
   data=p.read_bytes();assert data[:4]==b'v/1\x01';offset=8;header={}
   while data[offset]:
    name,offset=cstring(data,offset);typ,offset=cstring(data,offset);size=struct.unpack_from('<I',data,offset)[0];offset+=4;header[name]=(typ,data[offset:offset+size]);offset+=size
   channels=[];raw=header['channels'][1];i=0
   while raw[i]:
    name,i=cstring(raw,i);pixel_type=struct.unpack_from('<I',raw,i)[0];i+=16;channels.append({'channel':name,'pixelType':pixel_type})
   assert all(c['pixelType']==1 for c in channels),f'EXR is not half float: {p}'
   assert header['compression'][1][0]==3,f'Expected lossless ZIP EXR: {p}'
   a,b,c,d=struct.unpack('<4i',header['dataWindow'][1]);maps.append({'state':key,'meshId':lm['meshId'],'quality':q,'width':c-a+1,'height':d-b+1,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'channels':channels})
   assert c-a+1==d-b+1==lm['size']//{'high':1,'balanced':2,'low':4}[q]
 for uri in uris:
  if not (P/uri).is_file():missing.append(uri)
assert not missing,missing
assert len(maps)==sum(len(s['lightmaps'])*3 for s in m['states'].values())
assert len({r['sha256'] for r in maps if r['meshId']=='MESH_SURFACES' and r['quality']=='high'})==6
report={'states':len(m['states']),'models':models,'lightmaps':maps,'missing':missing,'total_distributable_bytes':sum(p.stat().st_size for p in (P/'assets').rglob('*') if p.is_file()),'exr_encoding_verified':'HALF channels, ZIP compression, no PNG masquerading as EXR'}
(R/'outputs/validation/assets-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'states':len(m['states']),'model_bytes':sum(x['bytes'] for x in models),'maps':len(maps),'missing':missing,'total_bytes':report['total_distributable_bytes']},indent=2))
