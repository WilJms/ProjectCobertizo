"""Render the existing ground/walls without the proposals, from portrait references."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
s=bpy.context.scene
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
state('d1_madera_dos_aguas','day')
for o in bpy.data.objects:
    if o.type=='MESH' and (o.get('sourceGroup','') in ['furniture','fixtures','WEB_DERIVED'] or o.get('sourceGroup','').startswith('d') or o.name.startswith(('DECK_','PLANT_','UPLIGHT_'))):o.hide_render=True
s.cycles.samples=32;s.render.resolution_x=960;s.render.resolution_y=1280
out=ROOT/'outputs/spatial-analysis'
for c in CONFIG['photo_comparison_cameras']:
    s.camera=bpy.data.objects[c['id']]
    # The reference's house lies outside the modeled detail; avoid a proxy wall
    # occluding the fitted camera, which is just outside its nominal X=0 plane.
    bpy.data.objects['HOUSE_LIMIT'].hide_render=c['id']=='PHOTO_R03_GENERAL'
    s.render.filepath=str(out/(c['id']+'__existing.png'));bpy.ops.render.render(write_still=True)
print('SPATIAL_REVIEW_RENDERED',flush=True)
