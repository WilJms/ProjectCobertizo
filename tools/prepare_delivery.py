"""Create a local, self-contained repository copy after all validation passes."""
from pathlib import Path
import json,hashlib,shutil,time
R=Path(__file__).resolve().parents[1]
required=['blender/patio_master.blend','web/dist/index.html','outputs/validation/assets-report.json','outputs/validation/browser-report.json','outputs/validation/production-report.json','outputs/validation/revision-report.json']
for name in required:assert (R/name).is_file(),f'Missing required delivery evidence: {name}'
browser=json.loads((R/required[3]).read_text());production=json.loads((R/required[4]).read_text())
revision=json.loads((R/required[5]).read_text())
expected=json.loads((R/'config/scene-parameters.json').read_text())['spatial_revision']
assert all(report['spatialRevision']==expected for report in [browser,production,revision]),'Validation belongs to an older revision'
source=hashlib.sha256((R/'blender/patio_master.blend').read_bytes()).hexdigest()
assert all(report['sourceSha256']==source for report in [browser,production,revision]),'Validation does not match the final master'
assert not revision['errors'] and all(row['pass'] for row in revision['checks'])
assert len(revision['temporal'])==8 and all(row['durationMs']>=18000 for row in revision['temporal'])
assert not production['errors'] and not production['failures']
assert all(row['pass'] for row in browser['checks'])
assert not browser['failures']
assert not [e for e in browser['errors'] if 'net::ERR_FAILED' not in e]
stage=R/('outputs/delivery-staging-'+str(int(time.time())));stage.mkdir()
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for name in ['AGENTS.md','README.md','PROMPT_INICIAL.md','PROMPT_CONTINUAR.md','PromptModificacion.rtf','plan.md','progress.md','decisions.md','assumptions.md','requirements.txt','.gitignore','.nvmrc']:
 if (R/name).is_file():copy(R/name,stage/name)
for directory in ['.github','config','docs','tools','references','blender','web']:
 for src in (R/directory).rglob('*'):
  if not src.is_file():continue
  rel=src.relative_to(R)
  if any(part in {'node_modules','__pycache__','history'} for part in rel.parts):continue
  if src.name=='.DS_Store' or src.suffix in {'.blend1','.blend2','.pyc'} or src.name.startswith('patio_refresh_test'):continue
  copy(src,stage/rel)
for directory in ['environment','references','pilot','renders','browser','comparisons','revision-2026-10-04']:
 for src in (R/'outputs'/directory).rglob('*'):
  if src.is_file() and src.name!='.DS_Store' and not src.name.startswith('probe-') and 'in-progress' not in src.name and 'temporal-video' not in src.parts and not src.name.endswith('server.log'):copy(src,stage/src.relative_to(R))
final_spatial=['spatial-inference.json','inferred-plan.png','r03-spatial-overlay.png','r02-shared-landmarks.png','PHOTO_R01_CERCO__existing.png','PHOTO_R02_TERRAZA__existing.png','PHOTO_R03_GENERAL__existing.png','r02-paving.png','r03-ground.png','r01-fence-ground.png']
for name in final_spatial:
 src=R/'outputs/spatial-analysis'/name
 if src.is_file():copy(src,stage/src.relative_to(R))
for src in (R/'outputs/validation').glob('*'):
 if src.suffix=='.json' and 'in-progress' not in src.name or src.name in ['build-spatial-final.log','export-spatial-final.log','export-spatial-first-pass.log','spatial-review-final.log','uv-final.log','browser-final.log','production-final.log','refresh-test.log','inspection-renders.log','denoising.log','production-build.log','unit-final.log','delivery-blender.log']:
  copy(src,stage/src.relative_to(R))
copy(R/'outputs/README.md',stage/'outputs/README.md')
readme=stage/'README.md';readme.write_text(readme.read_text().replace('La copia organizada está en `entrega-repositorio/`; no incluye','Esta carpeta es la copia organizada para trasladar a un repositorio; no incluye'))
files=[]
for p in sorted(stage.rglob('*')):
 if p.is_file():files.append({'path':str(p.relative_to(stage)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'status':'publish_ready_local_delivery','remote_deployment':'not_requested_user_will_handle','spatialRevision':production['spatialRevision'],'fileCount':len(files),'bytes':sum(f['bytes'] for f in files),'files':files}
(stage/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
target=R/'entrega-repositorio'
if target.exists():target.rename(R/('entrega-repositorio-anterior-'+str(int(time.time()))))
stage.rename(target)
print(json.dumps({'directory':str(target),'files':manifest['fileCount'],'bytes':manifest['bytes']},ensure_ascii=False))
