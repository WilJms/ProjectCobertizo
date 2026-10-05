"""Inventory original bytes and extract sparse, correctly rotated video evidence."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image, ImageOps, ImageDraw
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'outputs/references'
out.mkdir(parents=True, exist_ok=True)
inventory = json.loads((ROOT / 'config/references.json').read_text())
mapping = {
    'r01_cerco': 'WhatsApp Image 2026-10-01 at 21.35.57 (1).jpeg',
    'r02_terraza': 'WhatsApp Image 2026-10-01 at 21.35.57 (2).jpeg',
    'r03_general': 'WhatsApp Image 2026-10-01 at 21.35.57.jpeg',
    'v01_recorrido': 'WhatsApp Video 2026-09-26 at 21.01.22.mp4',
    'd1_madera_dos_aguas': 'Nueve luces cálidas en la terraza.png',
    'd2_oscuro_cielo_madera': 'Unknown-2.png',
    'd3_oscuro_paneles_claros': 'Unknown.png',
    'r04_detalle_deck': 'WhatsApp Image 2026-09-26 at 21.06.39.jpeg',
}
if not any(r['id']=='r04_detalle_deck' for r in inventory['references']):
    inventory['references'].append({'id':'r04_detalle_deck','role':'supplementary_design_detail','provenance':'Supplied image; deck and lighting match proposals. Not evidence of existing built deck.'})
for ref in inventory['references']:
    path = ROOT / 'references' / mapping[ref['id']]
    ref.update(resolved_relative_path=str(path.relative_to(ROOT)), location_status='located_and_inspected', sha256=hashlib.sha256(path.read_bytes()).hexdigest(), size_bytes=path.stat().st_size)
    if path.suffix != '.mp4':
        im = ImageOps.exif_transpose(Image.open(path))
        ref.update(image_width_px=im.width,image_height_px=im.height)
        im.thumbnail((768,1024))
        im.convert('RGB').save(out / (ref['id']+'.jpg'), quality=92)
inventory.update(status='originals_located',original_media_included=True,inspected_on='2026-10-03')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = ROOT / 'references' / mapping['v01_recorrido']
probe = subprocess.run([ffmpeg,'-i',str(video)],capture_output=True,text=True)
(out / 'video-metadata.txt').write_text(probe.stderr)
times = [0.5,3,6,9,12,15,18.5]
sheet = Image.new('RGB',(7*230,450),'#e9e8e4')
draw = ImageDraw.Draw(sheet)
for idx,t in enumerate(times):
    target = out / f'video-{t:04.1f}s.jpg'
    subprocess.run([ffmpeg,'-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(target)],check=True,capture_output=True)
    im=Image.open(target); im.thumbnail((224,405))
    sheet.paste(im,(idx*230,25)); draw.text((idx*230+6,6),f'{t:.1f} s',fill='black')
sheet.save(out/'video-contact-sheet.jpg',quality=94)
inventory['video_extraction']={'ffmpeg': imageio_ffmpeg.get_ffmpeg_version(),'timestamps_seconds':times,'rotation':'container autorotation applied','frames':'outputs/references/video-*.jpg'}
(ROOT/'config/references.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(mapping),'ffmpeg':imageio_ffmpeg.get_ffmpeg_version(),'frames':times}))
