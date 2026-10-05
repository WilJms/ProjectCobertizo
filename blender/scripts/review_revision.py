"""Inspect and validate v3 against the preserved v2 and the user's explicit rules."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_lib import *
from patio_geometry import inside
s=bpy.context.scene;g=CONFIG['geometry'];out=ROOT/'outputs/revision-2026-10-04'
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
for n in json.loads(s['receiver_ids']):bpy.data.objects[n].hide_render=True
old=json.loads((out/'baseline/scene-parameters.json').read_text())['geometry']
checks={}
for key in ['main_deck_rect_m','pool_outline_xy_m','pool_border_width_m','fence_segments']:
    checks[key+'_preserved']=g[key]==old[key];assert checks[key+'_preserved']
counts={f['id']:len([o for o in GROUPS['fixtures'].objects if o.name.startswith('RISER_LENS') and o.get('riserFace')==f['id']]) for f in g['deck_riser_faces']}
assert counts=={'dining':3,'lounger':3,'walkway':3,'diagonal':0}
checks['riser_counts']=counts
checks['diffuser_housing_clearance_m']=.061-.005-(.040+.011)
assert checks['diffuser_housing_clearance_m']>.004
A,B=g['wing_end_corners_xy_m'].values();assert A[1]==old['wing_deck_rect_m'][3] and B[1]>A[1]
checks['corners']={'A':A,'B':B};checks['wing_width_m']=B[0]-A[0]
checks['walkway_to_deck_clearance_m']=g['main_deck_rect_m'][0]-g['walkway_rect_m'][2]
checks['walkway_outside_main_roof']=g['walkway_rect_m'][2]<-.09
assert checks['walkway_outside_main_roof']
for d in CONFIG['designs']:
    for x,y in d['parameters']['post_positions_xy_m'][-2:]:
        assert all(inside((x+dx,y+dy),g['deck_footprint_xy_m']) for dx in [-.125,.125] for dy in [-.125,.125]),'Foot extends beyond diagonal'
    for t in ['day','night']:
        state(d['id'],t);active=[o for o in bpy.data.objects if o.type=='LIGHT' and o.data.energy>0 and not o.get('naturalLight')]
        natural=[o for o in bpy.data.objects if o.type=='LIGHT' and o.data.energy>0 and o.get('naturalLight')]
        assert len(natural)==(1 if t=='day' else 0)
        assert not natural or natural[0].data.type=='SUN'
        assert len(active)==(0 if t=='day' else 35),(d['id'],t,len(active))
        assert MAT['lamp'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value==(0 if t=='day' else 5)
        checks[d['id']+'__'+t]={'activeArtificialLights':len(active),'activeNaturalSuns':len(natural),'emission':0 if t=='day' else 5}
for i in range(101):
    p=Vector(A).lerp(Vector(B),i/100);assert not inside(p,g['pool_outline_xy_m']), 'Diagonal enters water'
checks['diagonal_enters_water']=False
closed=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not (o.name.startswith('DECK_') or '_WING_' in o.name or o.name=='EGG_CUSHION'):continue
    directions={};me=o.data;me.calc_loop_triangles()
    for p in me.polygons:
        ids=list(p.vertices)
        for a,b in zip(ids,ids[1:]+ids[:1]):
            key=tuple(sorted((a,b)));directions[key]=directions.get(key,0)+(1 if a<b else -1)
    assert all(n==0 for n in directions.values()),'Inconsistent face winding: '+o.name
    volume=sum(me.vertices[t.vertices[0]].co.dot(me.vertices[t.vertices[1]].co.cross(me.vertices[t.vertices[2]].co)) for t in me.loop_triangles)/6
    assert volume>0,'Reversed solid: '+o.name
    closed.append(o.name)
checks['closed_solids_with_outward_faces']=len(closed)
seat=bpy.data.objects['LOUNGER_SEAT'];back=bpy.data.objects['LOUNGER_BACK']
joint_seat=seat.matrix_world@Vector((0,-.71,0));joint_back=back.matrix_world@Vector((0,.38,0))
checks['lounger_joint_error_m']=(joint_seat-joint_back).length
assert checks['lounger_joint_error_m']<1e-5
table=Vector((g['table_position_xy_m'][0],-g['table_position_xy_m'][1],0))
for idx in range(4):
    def center(name):
        o=bpy.data.objects[name];return sum((o.matrix_world@v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
    seat_center=center(f'CHAIR_RED_SEAT_{idx}');back_center=center(f'CHAIR_RED_BACK_{idx}')
    facing=(seat_center-back_center);facing.z=0;to_table=table-seat_center;to_table.z=0
    assert facing.dot(to_table)>0,'Chair faces away from table'
checks['all_four_chairs_face_table']=True
from mathutils.bvhtree import BVHTree
state(CONFIG['designs'][0]['id'],'day')
bpy.context.view_layer.update()
depsgraph=bpy.context.evaluated_depsgraph_get()
def tree(obj):
    evaluated=obj.evaluated_get(depsgraph);me=evaluated.to_mesh()
    result=BVHTree.FromPolygons([evaluated.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])
    evaluated.to_mesh_clear();return result
d1=CONFIG['designs'][0]['id']
skins=[(o.name,tree(o)) for o in GROUPS[d1].objects if '_ROOF_OUTER_' in o.name]
roof_crossings=[]
for obj in GROUPS[d1].objects:
    if obj.name.startswith(d1+'_RAFTER_'):
        rafter=tree(obj)
        for name,skin in skins:
            if rafter.overlap(skin):roof_crossings.append([obj.name,name])
checks['rafter_roof_skin_intersections']=roof_crossings
assert not roof_crossings, 'Rafters pierce the outer roof: '+str(roof_crossings)
checks['foliage_pruning']=json.loads((out/'foliage-intersections.json').read_text())
(out/'geometry-checks.json').write_text(json.dumps(checks,indent=2))
if '--check-only' in sys.argv:sys.exit(0)
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=40;s.render.resolution_x=1200;s.render.resolution_y=800
selection=next((a.split('=',1)[1].split(',') for a in sys.argv if a.startswith('--views=')),None)
def view(name,pos,target,fov=66,design=0,time='day',top=False,hide_roof=False):
    if selection and not any(name.startswith(key) for key in selection):return
    state(CONFIG['designs'][design]['id'],time);s.camera=camera(name,(pos[0],-pos[1],pos[2]),(target[0],-target[1],target[2]),fov)
    s.render.resolution_x=1000 if top else 1200;s.render.resolution_y=1200 if top else 800
    if top:s.camera.data.type='ORTHO';s.camera.data.ortho_scale=10.0
    if hide_roof:GROUPS[CONFIG['designs'][design]['id']].hide_render=True
    s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
view('furniture-chairs',[2.9,4.1,2.7],[2.9,1.68,.85],72)
view('furniture-lounger',[4.45,4.4,1.55],[6.47,4.05,.69],61)
view('furniture-egg',[6.35,3.65,1.70],[6.48,1.11,1.35],67)
view('left-fascia-night',[-.93,4.4,1.12],[.15,1.65,.40],69,time='night')
view('diagonal-night',[3.85,7.3,2.65],[6.55,6.6,1.0],80,time='night')
for d in range(3):
    view('top-roof-d'+str(d+1),[3.1,5.9,15],[3.1,5.9,0],57,design=d,top=True)
    view('top-deck-d'+str(d+1),[3.1,5.9,15],[3.1,5.9,0],57,design=d,top=True,hide_roof=True)
view('general-night',CONFIG['comparison_cameras'][0]['position_plan'],CONFIG['comparison_cameras'][0]['target_plan'],88,time='night')
print('REVISION_GEOMETRY_PASS',flush=True)
