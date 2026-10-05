"""Refresh only WEB_DERIVED from editable source collections, preserving manual work.
Open the master with -b and run this after editing sources in Blender. Then export_scene.py.
"""
import bpy,sys,json,shutil,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
s=bpy.context.scene
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
master=Path(bpy.data.filepath);history=master.parent/'history';history.mkdir(exist_ok=True);shutil.copy2(master,history/f'patio_before_refresh_{int(time.time())}.blend')
specs=[]
for name in json.loads(s['receiver_ids']):
 old=bpy.data.objects[name];specs.append((name,old['sourceGroup'],int(old['atlasSize'])));bpy.data.objects.remove(old,do_unlink=True)
if GROUPS.get('USER_DETAILS') and len(GROUPS['USER_DETAILS'].objects) and not any(g=='USER_DETAILS' for _,g,_ in specs):specs.append(('MESH_USER_DETAILS','USER_DETAILS',1024))
for name,g,size in specs:
 GROUPS[g].hide_viewport=False;GROUPS[g].hide_render=False;derive(name,g,size)
s['receiver_ids']=json.dumps([n for n,_,_ in specs])
state(s.get('designId','d1_madera_dos_aguas'),s.get('timeId','day'))
bpy.ops.wm.save_as_mainfile(filepath=str(master))
print('Derived geometry refreshed; source collections and manual edits retained.')
