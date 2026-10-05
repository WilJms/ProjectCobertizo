"""Update lighting in the opened editable master, preserving all geometry and UVs."""
import sys, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
s=bpy.context.scene
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
master=Path(bpy.data.filepath)
assert master==ROOT/'blender/patio_master.blend'
archive=ROOT/'blender/history';archive.mkdir(exist_ok=True)
shutil.copy2(master,archive/f'patio_master_before_sunny_{int(time.time())}.blend')
for im in bpy.data.images:
    if im.filepath and Path(bpy.path.abspath(im.filepath)).name=='sky_day.jpg':im.reload()
s['config_json']=json.dumps(CONFIG)
state(CONFIG['designs'][0]['id'],'day')
for im in bpy.data.images:
    if im.filepath:im.filepath=bpy.path.relpath(bpy.path.abspath(im.filepath),start=str(ROOT/'blender'))
bpy.ops.wm.save_as_mainfile(filepath=str(master))
print('SUNNY_MASTER',hashlib.sha256(master.read_bytes()).hexdigest(),flush=True)
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=48;s.camera=bpy.data.objects['CAM01_GENERAL']
s.render.filepath=str(ROOT/'outputs/revision-2026-10-04/sunny-preview.png')
bpy.ops.render.render(write_still=True)
