import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
s=setup();materials();group('pilot')
for name,pos,size in [('left',(-1.1,0,-.08),(2.8,5,.16)),('right',(2.3,0,-.08),(.4,5,.16)),('back',(1.2,-1.1,-.08),(1.8,2.8,.16)),('front',(1.2,2.2,-.08),(1.8,.6,.16))]:box('pilot_paving_'+name,pos,size,'aggregate')
box('pilot_blue',(-2.45,0,1.2),(.12,5,2.4),'blue',.015)
for i in range(21):box(f'pilot_fence_{i}',(0,-2.4,.06+i*.115),(4.8,.07,.10),'wood_old',.003)
for i in range(22):box(f'pilot_deck_{i}',(-1.3+i*.15,-1.2,.15),(.143,2,.1),'wood_new',.004)
box('pilot_post',(1.4,-.2,1.5),(.15,.15,3),'paint',.01)
box('pilot_beam',(0,-.2,2.93),(3,.15,.22),'paint',.008)
box('pilot_panel',(0,-1.1,2.98),(3,1.8,.05),'panel',.006)
cyl('pilot_luminaire',(0,-1.1,2.86),.09,.05,'paint')
cyl('pilot_lens',(0,-1.1,2.824),.08,.01,'lamp')
area_light('pilot_light',(0,-1.1,2.8),(0,-1.1,0),110,.13)
box('pilot_pool_bottom',(1.2,1.1,-.28),(1.8,1.6,.08),'pool')
# Separate animated water; basin visible around it, no coincident floor.
group('pilot_water'); water=box('WATER',(1.2,1.1,.08),(1.65,1.45,.01),'water');water.hide_render=False
cam=camera('PILOT_CAMERA',(4,5,3.6),(-.25,-.65,1),65);s.camera=cam;s.render.resolution_x=960;s.render.resolution_y=640
obj=derive('PILOT_STATIC','pilot',1024);(ASSETS/'pilot').mkdir(parents=True,exist_ok=True)
manifest={'version':1,'stage':'pilot','camera':camera_contract(cam),'states':{}}
records=[]
for t in ['day','night']:
 state('pilot',t);s.view_settings.exposure=0; s.world.node_tree.nodes.get('Background').inputs[1].default_value=1 if t=='day' else .65;records.append(bake(obj,ASSETS/'pilot'/f'{t}.exr',1024,32))
 s.cycles.samples=48;s.render.filepath=str(ROOT/'outputs/pilot'/f'cycles-{t}.png');bpy.ops.render.render(write_still=True)
 manifest['states'][t]={'model':'assets/pilot/pilot.glb','lightmap':f'assets/pilot/{t}.exr','environment':f'assets/sky_{t}.jpg','environmentIntensity':1 if t=='day' else .65}
export_glb([obj,water],ASSETS/'pilot/pilot.glb')
for t in ['day','night']:shutil.copy(TEX/f'sky_{t}.jpg',ASSETS/f'sky_{t}.jpg')
(ASSETS/'pilot/manifest.json').write_text(json.dumps(manifest,indent=2));(ROOT/'outputs/pilot/bake-report.json').write_text(json.dumps(records,indent=2))
state('pilot','day');obj.hide_render=True;obj.hide_set(True);water.hide_render=False;water.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/pilot.blend'))
