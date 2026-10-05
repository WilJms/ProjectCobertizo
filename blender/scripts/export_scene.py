"""Bake/render/export the currently opened editable master, without rebuilding it.
Use -- --quick for one state, -- --no-bake to re-export geometry/manifest only.
"""
import sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import scene_lib as lib
from scene_lib import *
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for device in prefs.devices:device.use=device.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
print('CYCLES_DEVICE',s.cycles.device,[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
if 'receiver_ids' not in s:raise RuntimeError('Open blender/patio_master.blend before export')
for c in bpy.data.collections:GROUPS[c.name]=c
for m in bpy.data.materials:MAT[m.name]=m
CONFIG=json.loads(s['config_json']);receivers=[bpy.data.objects[n] for n in json.loads(s['receiver_ids'])]
COLLISIONS=json.loads(s['collisions_json']);LIGHTS=json.loads(s['lights_json'])
for o in receivers:o.hide_render=True;o.hide_set(True)
for f in ['models','lightmaps','renders']: (ASSETS/f).mkdir(exist_ok=True,parents=True)
for t in ['day','night']:shutil.copy(TEX/f'sky_{t}.jpg',ASSETS/f'sky_{t}.jpg')
common=[o for o in receivers if not o['sourceGroup'].startswith('d')];variants={d['id']:next(o for o in receivers if o['sourceGroup']==d['id']) for d in CONFIG['designs']}
water=[o for o in GROUPS['water'].objects if o.type=='MESH']
state(CONFIG['designs'][0]['id'],'day')
export_glb(common+water,ASSETS/'models/common.glb')
for d,o in variants.items():export_glb([o],ASSETS/'models'/f'{d}.glb')
for o in water:o.hide_render=False;o.hide_set(False)
manifest={'schemaVersion':'1.0','spatialRevision':CONFIG.get('spatial_revision'),'sourceSha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'source':'blender/patio_master.blend','lengthsAreEstimates':True,'commonModel':'assets/models/common.glb','cameras':[camera_contract(bpy.data.objects[c['id']]) for c in CONFIG['comparison_cameras']],
 'designs':[{'id':d['id'],'label':label,'description':desc} for d,label,desc in zip(CONFIG['designs'],['Madera · Dos aguas','Oscuro · Cielo de madera','Oscuro · Paños claros'],['Cercha vista y ala lateral baja','Estructura oscura y tablillas cálidas','Travesaños vistos y cubierta difusora'])],
 'states':{},'lightingContract':{'diffuse':'Cycles DIFFUSE direct+indirect without COLOR: E/pi, multiplied once by albedo at runtime','specular':'Realtime PBR environment plus planar pool reflection; no unshadowed point-light surrogates','environmentDiffuse':'Included in Cycles; all runtime material diffuse overwritten','daySun':'SUN_DAY direct and indirect diffuse baked once; no runtime diffuse sun','ao':'None','toneMapping':'AgX once; output sRGB; exposure multiplier 1.2','lightmap':{'format':'OpenEXR ZIP half float','colorSpace':'Linear Rec.709 / linear-sRGB','channel':1,'gltfAttribute':'TEXCOORD_1','threeAttribute':'uv1','flipY':True,'scale':1}},
 'navigation':{'bounds':[CONFIG['geometry'].get('site_left_x_m',0)+.18,.18,CONFIG['geometry']['site_width_m']-.18,CONFIG['geometry']['site_depth_m']-.18],'pool':CONFIG['geometry']['pool_outline_xy_m'],'deck':CONFIG['geometry']['deck_footprint_xy_m'],'deckHeight':.22,'eyeHeight':1.65,'radius':.20,'commonCollisions':COLLISIONS},
 'profiles':{'high':{'pixelRatio':1.75,'reflectionSize':512,'reflectionEvery':1,'description':'Mayor nitidez y reflejos continuos'},'balanced':{'pixelRatio':1.25,'reflectionSize':512,'reflectionEvery':2,'description':'Nitidez media y reflejos alternos'},'low':{'pixelRatio':.85,'reflectionSize':512,'reflectionEvery':4,'description':'Menor resolución y reflejos espaciados'}},
 'provenance':{'dimensions':'inferred_not_measured','night':'design_simulation','day':'sunny_user_request; sun direction is an authored choice, not a measured orientation','poolFarEdgeAndDepth':'conservative_estimate','panel':'diffuse_translucent_approximation'},
 'assetsLicense':'Original geometry/textures generated locally; Three.js MIT; no external stock assets'}
records=[];quick='--quick' in sys.argv;no_bake='--no-bake' in sys.argv
resume_designs=set(next((a.split('=',1)[1] for a in sys.argv if a.startswith('--resume-designs=')),'').split(','))-{''}
assert resume_designs.issubset(variants),'Unknown resumed design ID'
for d in CONFIG['designs']:
 for t in ['day','night']:
    key=d['id']+'__'+t;state(d['id'],t)
    active=common+[variants[d['id']]];maps=[]
    for o in active:
        path=ASSETS/'lightmaps'/f'{key}__{o.name}.exr'
        if d['id'] in resume_designs:
            paths=[path,path.with_stem(path.stem+'--balanced'),path.with_stem(path.stem+'--low')]
            assert all(p.exists() and p.stat().st_mtime>Path(bpy.data.filepath).stat().st_mtime for p in paths),'Cannot resume maps older than the master'
            records.append({'meshId':o.name,'width':int(o['atlasSize']),'state':key,'resumed':True,'seconds':None,'sourceSha256':manifest['sourceSha256'],'evidence':'Completed state in export-spatial-first-pass.log; all three maps are newer than the unchanged master','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'encoding':'linear_rec709_half_float','pass':'DIFFUSE direct+indirect; COLOR excluded; no AO'})
        elif not no_bake and (not quick or key==CONFIG['designs'][0]['id']+'__day'):
            row=bake(o,path,int(o['atlasSize']),40);row['state']=key;records.append(row)
            (ROOT/'outputs/validation/bakes-in-progress.json').write_text(json.dumps(records,indent=2)+'\n')
            print('BAKED',key,o.name,flush=True)
        maps.append({'meshId':o.name,'uri':str(path.relative_to(ASSETS.parent)),'uvChannel':1,'flipY':True,'linear':True,'size':int(o['atlasSize'])})
    lights=[l for l in LIGHTS if l['group'] in ['common',d['id']]]
    manifest['states'][key]={'designId':d['id'],'timeId':t,'model':'assets/models/'+d['id']+'.glb','lightmaps':maps,'environment':{'uri':f'assets/sky_{t}.jpg','intensity':daylight_settings()['environment_intensity'] if t=='day' else 1.0,'backgroundIntensity':daylight_settings()['background_intensity'] if t=='day' else 1.0},'exposure':1.2,'emissionStrength':5 if t=='night' else 0,'lights':lights if t=='night' else [],'naturalLight':{'type':'sun','baked':True,**CONFIG['lighting']['day']['sun']} if t=='day' else None,'water':{'level':-.14,'reflection':'planar','time':0,'absorptionApproximation':True},'collisions':[{'id':d['id']+f'_post_{i}','type':'circle','x':xy[0],'y':xy[1],'radius':.13} for i,xy in enumerate(d['parameters']['post_positions_xy_m'])],'render':f'assets/renders/{key}.jpg'}
    if d['id'] in resume_designs:
        p=ROOT/'outputs/renders'/f'{key}__CAM01_GENERAL.png'
        assert p.exists() and p.stat().st_mtime>Path(bpy.data.filepath).stat().st_mtime,'Cannot resume a render older than the master'
    elif not no_bake and (not quick or key==CONFIG['designs'][0]['id']+'__day'):
        s.cycles.samples=64;s.camera=bpy.data.objects['CAM01_GENERAL'];s.render.filepath=str(ROOT/'outputs/renders'/f'{key}__CAM01_GENERAL.png');bpy.ops.render.render(write_still=True)
        print('RENDERED',key,flush=True)
(ASSETS/'scene-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
report=ROOT/'outputs/validation/bakes.json'
if records:report.write_text(json.dumps(records,indent=2)+'\n')
state(CONFIG['designs'][0]['id'],'day')
# Keep the master's source objects visible and derived preview disabled after export.
for o in receivers:o.hide_render=True;o.hide_set(True)
for o in water:o.hide_render=False;o.hide_set(False)
print('EXPORT_COMPLETE',flush=True)
