"""Verify every copied file, then open the copied Blender master without saving."""
from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path(__file__).resolve().parents[1]
target=R/'entrega-repositorio'
manifest=json.loads((target/'delivery-manifest.json').read_text())
for row in manifest['files']:
    p=target/row['path']
    assert p.stat().st_size==row['bytes'],row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
scene=json.loads((target/'web/public/assets/scene-manifest.json').read_text())
assert scene['sourceSha256']==hashlib.sha256((target/'blender/patio_master.blend').read_bytes()).hexdigest()
assert scene['spatialRevision']==manifest['spatialRevision']
blender=shutil.which('blender') or '/Applications/Blender.app/Contents/MacOS/Blender'
assert Path(blender).is_file(),'Blender is required to verify the copied master'
out=R/'outputs/revision-2026-10-04'
with (out/'delivery-blender.log').open('w') as log:
    subprocess.run([blender,'-b',str(target/'blender/patio_master.blend'),'--python-exit-code','1','--python',str(target/'blender/scripts/check_delivery.py'),'--','--report='+str(out/'delivery-blender.json')],stdout=log,stderr=subprocess.STDOUT,check=True)
opened=json.loads((out/'delivery-blender.json').read_text())
report={'status':'publish_ready','spatialRevision':scene['spatialRevision'],'sha256_copy_verification':'pass','files_verified':len(manifest['files']),'master_opened_from_delivery':opened['masterOpened'],'master_images_resolve_inside_delivery':opened['allImagesInsideDelivery'],'file_images':opened['fileImages'],'production_prefix':'/ProjectCobertizo/','remote_publication':'not_requested_user_will_handle','physical_phone':'not_run'}
(R/'outputs/validation/delivery-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
