"""Denoise scene-linear diffuse atlases through Blender's compositor.

The first run archives raw EXR files. Subsequent runs always use those originals.
Use -- --probe to process only the D1 night structure into outputs/validation.
"""
import bpy, sys, json, shutil, hashlib
from pathlib import Path
R = Path(__file__).resolve().parents[2]
assets = R/'web/public/assets/lightmaps'
raw = R/'outputs/lightmaps-raw'
probe = '--probe' in sys.argv
paths = [assets/'d1_madera_dos_aguas__night__MESH_D1_MADERA_DOS_AGUAS.exr'] if probe else sorted(p for p in assets.glob('*.exr') if '--' not in p.name)
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.engine = 'CYCLES'
s.cycles.samples = 1
s.cycles.device = 'CPU'
s.render.image_settings.file_format = 'OPEN_EXR'
s.render.image_settings.color_depth = '16'
s.render.image_settings.exr_codec = 'ZIP'
cam = bpy.data.objects.new('CompositorCamera', bpy.data.cameras.new('CompositorCamera'))
s.collection.objects.link(cam)
s.camera = cam
tree = bpy.data.node_groups.new('LinearDiffuseDenoise','CompositorNodeTree')
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
s.compositing_node_group = tree
source = tree.nodes.new('CompositorNodeImage')
denoise = tree.nodes.new('CompositorNodeDenoise')
output = tree.nodes.new('NodeGroupOutput')
tree.links.new(source.outputs['Image'],denoise.inputs['Image'])
tree.links.new(denoise.outputs['Image'],output.inputs['Image'])
report_path=R/'outputs/validation/denoising.json'
previous={row['path']:row for row in json.loads(report_path.read_text())} if report_path.exists() and not probe else {}
records=[]
for path in paths:
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    earlier=previous.get(str(path.relative_to(R)))
    if earlier and earlier['outputSha256']==digest:
        records.append(earlier)
        continue
    original = raw/digest/path.name
    if not original.exists():
        original.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,original)
    source.image=bpy.data.images.load(str(original),check_existing=False)
    source.image.colorspace_settings.name='Linear Rec.709'
    w,h=source.image.size
    s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
    target=R/'outputs/validation/denoise-probe.exr' if probe else path
    s.render.filepath=str(target)
    bpy.ops.render.render(write_still=True)
    if not probe:
        filtered=bpy.data.images.load(str(target),check_existing=False)
        for quality,divisor in [('balanced',2),('low',4)]:
            lower=path.with_stem(path.stem+'--'+quality)
            archived=raw/digest/lower.name
            if not archived.exists():shutil.copy2(lower,archived)
            filtered.scale(w//divisor,h//divisor)
            filtered.save_render(str(lower),scene=s)
        bpy.data.images.remove(filtered)
    records.append({'path':str(target.relative_to(R)),'sourceSha256':hashlib.sha256(original.read_bytes()).hexdigest(),'outputSha256':hashlib.sha256(target.read_bytes()).hexdigest(),'method':'Blender compositor Denoise; scene-linear irradiance, no display transform, color-only guide','width':w,'height':h})
    bpy.data.images.remove(source.image)
if not probe:
    (R/'outputs/validation/denoising.json').write_text(json.dumps(records,indent=2)+'\n')
    manifest_path=R/'web/public/assets/scene-manifest.json'
    manifest=json.loads(manifest_path.read_text())
    manifest['lightingContract']['lightmap']['denoising']='Blender compositor Denoise on scene-linear irradiance; texture albedo remains separate'
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('DENOISE_COMPLETE',len(records),flush=True)
