"""Validate real derived UVs and correspondence, using a conservative raster overlap check."""
import bpy, json, numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[2];s=bpy.context.scene;report=[]
for name in json.loads(s['receiver_ids']):
 o=bpy.data.objects[name];me=o.data;me.calc_loop_triangles();layer=me.uv_layers.get('LightmapUV')
 uv=np.array([tuple(v.uv) for v in layer.data]);n=512;cover=np.zeros((n,n),dtype=np.uint16);degenerate=0
 for tri in me.loop_triangles:
  p=uv[list(tri.loops)]*n;a,b,c=p;area=np.cross(b-a,c-a)
  if abs(area)<1e-7:degenerate+=1;continue
  lo=np.maximum(0,np.floor(p.min(axis=0)).astype(int));hi=np.minimum(n-1,np.ceil(p.max(axis=0)).astype(int))
  if np.any(lo>hi):continue
  yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
  e1=(b[0]-a[0])*(yy-a[1])-(b[1]-a[1])*(xx-a[0]);e2=(c[0]-b[0])*(yy-b[1])-(c[1]-b[1])*(xx-b[0]);e3=(a[0]-c[0])*(yy-c[1])-(a[1]-c[1])*(xx-c[0]);sign=np.sign(area)
  mask=(e1*sign>1e-5)&(e2*sign>1e-5)&(e3*sign>1e-5);cover[lo[1]:hi[1]+1,lo[0]:hi[0]+1]+=mask.astype('uint16')
 report.append({'meshId':name,'uv_min':uv.min(axis=0).tolist(),'uv_max':uv.max(axis=0).tolist(),'triangle_count':len(me.loop_triangles),'zero_area_triangles':degenerate,'raster_resolution':n,'covered_pixels':int((cover>0).sum()),'overlapped_pixels':int((cover>1).sum()),'interpretation':'Raster test detects overlaps at 512 px, not an analytic proof at arbitrary resolution.'})
(R/'outputs/validation/uv-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
assert all(r['zero_area_triangles']==0 and r['overlapped_pixels']==0 for r in report),'Degenerate or overlapping lightmap triangles'
assert all(min(r['uv_min'])>=-1e-6 and max(r['uv_max'])<=1+1e-6 for r in report),'Lightmap UV outside atlas'
