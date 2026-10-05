"""Build master non-destructively to a new file; archive an existing master first.
Usage: Blender -b --python-exit-code 1 --python blender/scripts/build_scene.py [-- --all]
The generated source is editable; export_scene.py operates on the saved master.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from patio_geometry import *
import hashlib
s=setup();materials();shell();deck();furniture();landscaping();lights_common()
for d in CONFIG['designs']:design(d['id'])
from trim_foliage import trim_foliage
trim_foliage()
# Plan Y grows toward the house; Blender world Y points in the opposite direction.
from mathutils import Matrix
reflection=Matrix.Diagonal((1,-1,1,1))
for obj in list(bpy.data.objects):
    if obj.type=='MESH':obj.matrix_world=reflection @ obj.matrix_world
for info in LIGHTS:
    info['position'][1]*=-1;info['target'][1]*=-1
    obj=bpy.data.objects[info['id']];obj.location=info['position'];obj.rotation_euler=(Vector(info['target'])-obj.location).to_track_quat('-Z','Y').to_euler()
for c in CONFIG['comparison_cameras']+CONFIG.get('photo_comparison_cameras',[]):camera(c['id'],[c['position_plan'][0],-c['position_plan'][1],c['position_plan'][2]],[c['target_plan'][0],-c['target_plan'][1],c['target_plan'][2]],c['horizontal_fov_degrees'],c['aspect'])
s.camera=bpy.data.objects['CAM01_GENERAL']
# Stable derived receiver IDs. Every group has a private non-overlapping lightmap atlas.
receivers=[]
for name,size in [('surfaces',2048),('furniture',1024),('vegetation',1024),('fixtures',512)]+[(d['id'],1024) for d in CONFIG['designs']]:
    receivers.append(derive('MESH_'+name.upper(),name,size))
state(CONFIG['designs'][0]['id'],'day')
for o in receivers:o.hide_render=True;o.hide_set(True)
# An explicit hand-authored collection survives incremental exports; rebuild does not overwrite the prior file.
group('USER_DETAILS')
master=ROOT/'blender/patio_master.blend'
if master.exists():
    archive=ROOT/'blender/history';archive.mkdir(exist_ok=True);shutil.copy2(master,archive/f'patio_master_{int(time.time())}.blend')
# Make assets portable to the delivery directory.
for im in bpy.data.images:
    if im.filepath:im.filepath=bpy.path.relpath(im.filepath,start=str(ROOT/'blender'))
s['pipeline_version']='1.0';s['lengths_are_estimates']=True;s['collisions_json']=json.dumps(COLLISIONS);s['lights_json']=json.dumps(LIGHTS)
s['receiver_ids']=json.dumps([o.name for o in receivers]);s['config_json']=json.dumps(CONFIG)
bpy.ops.wm.save_as_mainfile(filepath=str(master))
report={'authored_objects':sum(len(c.objects) for key,c in GROUPS.items() if key!='WEB_DERIVED'),'derived_meshes':[{'meshId':o.name,'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'vertices':len(o.data.vertices),'uv_layers':[u.name for u in o.data.uv_layers]} for o in receivers],'camera_ids':[c['id'] for c in CONFIG['comparison_cameras']]}
(ROOT/'outputs/validation/geometry-report.json').write_text(json.dumps(report,indent=2))
s.cycles.samples=48;s.render.filepath=str(ROOT/'outputs/renders/base-day.png');bpy.ops.render.render(write_still=True)
print('MASTER_READY',master,flush=True)
