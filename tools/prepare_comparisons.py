"""Lay out unretouched reference/render/browser evidence with explicit labels."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

R = Path(__file__).resolve().parents[1]
out = R / 'outputs/comparisons'
out.mkdir(exist_ok=True)
references = {r['id']: r for r in json.loads((R/'config/references.json').read_text())['references']}

def pair(left, right, destination, labels, size):
    w, h = size
    sheet = Image.new('RGB', (w*2, h+32), '#202722')
    draw = ImageDraw.Draw(sheet)
    for i, (source, label) in enumerate(zip([left, right], labels)):
        im = Image.open(source).convert('RGB')
        assert abs(im.width/im.height - w/h) < .002, source
        sheet.paste(im.resize((w,h), Image.Resampling.LANCZOS), (i*w, 32))
        draw.text((i*w+12, 10), label, fill='white')
    sheet.save(destination, quality=94)

for camera, reference in [('PHOTO_R01_CERCO','r01_cerco'),('PHOTO_R02_TERRAZA','r02_terraza'),('PHOTO_R03_GENERAL','r03_general')]:
    pair(R/references[reference]['resolved_relative_path'], R/'outputs/spatial-analysis'/f'{camera}__existing.png',
         out/f'{camera}__reference-vs-blender.jpg', ['Referencia original', 'Base v2 / patio existente estimado'], (480,640))

manifest = json.loads((R/'web/public/assets/scene-manifest.json').read_text())
for key in manifest['states']:
    name = key+'__CAM01_GENERAL.png'
    web = R/'outputs/browser'/name
    if web.exists():
        pair(R/'outputs/renders'/name, web, out/(key+'__cycles-vs-web.jpg'), ['Cycles / '+key, 'Three.js / misma camara, agua t=0'], (600,400))
print('Comparison sheets generated from actual images; only proportional resizing and labels applied.')
