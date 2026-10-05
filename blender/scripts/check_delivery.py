"""Read-only check: a copied master resolves all file textures inside its delivery."""
import bpy,json,sys
from pathlib import Path
root=Path(bpy.data.filepath).resolve().parents[1]
images=[]
for im in bpy.data.images:
    if im.source!='FILE' or not im.filepath:continue
    path=Path(bpy.path.abspath(im.filepath)).resolve()
    assert path.is_file(),f'Missing copied texture: {im.name}'
    assert path.is_relative_to(root),f'Texture outside delivery: {im.name}'
    images.append(str(path.relative_to(root)))
revision=json.loads(bpy.context.scene['config_json'])['spatial_revision']
assert revision==json.loads((root/'config/scene-parameters.json').read_text())['spatial_revision']
report={'masterOpened':True,'spatialRevision':revision,'fileImages':len(images),'allImagesInsideDelivery':True,'images':images}
destination=next(a.split('=',1)[1] for a in sys.argv if a.startswith('--report='))
Path(destination).write_text(json.dumps(report,indent=2)+'\n')
print('DELIVERY_MASTER_PASS',len(images),revision)
