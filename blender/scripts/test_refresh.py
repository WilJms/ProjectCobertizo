"""Exercise the editing workflow on a disposable copy, never on the real master."""
import bpy,sys,json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
testfile=ROOT/'blender/patio_refresh_test.blend'
assert Path(bpy.data.filepath)==testfile,'Run only on the explicit test copy'
source={o.name:list(map(list,o.matrix_basis)) for o in bpy.data.objects if o.type=='MESH' and o.get('sourceGroup')!='WEB_DERIVED'}
cams=sorted(o.name for o in bpy.data.objects if o.type=='CAMERA')
user=bpy.data.collections['USER_DETAILS'];bpy.ops.mesh.primitive_cube_add(size=.05,location=(1,-1,.5));obj=bpy.context.object;obj.name='TEST_MANUAL_DETAIL'
for c in list(obj.users_collection):c.objects.unlink(obj)
user.objects.link(obj);obj['sourceGroup']='USER_DETAILS';obj['meshId']=obj.name;obj.data.materials.append(bpy.data.materials['paint'])
runpy.run_path(str(ROOT/'blender/scripts/refresh_derived.py'),run_name='__main__')
differences=[]
for name,matrix in source.items():
    if name not in bpy.data.objects:differences.append({'name':name,'missing':True});continue
    # Hidden collections may have a stale evaluated matrix_world. Compare authored
    # local transforms, which must survive independently of visibility evaluation.
    delta=max(abs(bpy.data.objects[name].matrix_basis[i][j]-matrix[i][j]) for i in range(4) for j in range(4))
    if delta>1e-5:differences.append({'name':name,'maxTransformDelta':delta})
if differences:print('SOURCE_DIFFERENCES',json.dumps(differences[:10]),flush=True)
assert not differences
assert cams==sorted(o.name for o in bpy.data.objects if o.type=='CAMERA')
assert 'TEST_MANUAL_DETAIL' in bpy.data.objects and 'MESH_USER_DETAILS' in bpy.data.objects
report={'pass':True,'sourceMeshesPreserved':len(source),'camerasPreserved':cams,'manualDetailRetained':True,'derivedManualDetailCreated':True,'testFileOnly':str(testfile.relative_to(ROOT))}
(ROOT/'outputs/validation/refresh-report.json').write_text(json.dumps(report,indent=2)+'\n');print('REFRESH_TEST_PASS',flush=True)
