"""Render named inspection views from the saved master, without rebuilding."""
import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
for n in json.loads(s['receiver_ids']):bpy.data.objects[n].hide_render=True
s.render.resolution_x=1200;s.render.resolution_y=800;s.cycles.samples=48
for d in [d['id'] for d in CONFIG['designs']]:
 state(d,'night');s.camera=bpy.data.objects['CAM04_BAJO_CUBIERTA'];s.render.filepath=str(ROOT/'outputs/renders'/f'{d}__night__CAM04_BAJO_CUBIERTA.png');bpy.ops.render.render(write_still=True)
for t in ['day','night']:
 state('d3_oscuro_paneles_claros',t);s.camera=bpy.data.objects['CAM05_PISCINA'];s.render.filepath=str(ROOT/'outputs/renders'/f'd3_oscuro_paneles_claros__{t}__CAM05_PISCINA.png');bpy.ops.render.render(write_still=True)
