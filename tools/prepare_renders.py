from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json
r=Path(__file__).resolve().parents[1];m=json.loads((r/'web/public/assets/scene-manifest.json').read_text());sheet=Image.new('RGB',(1200,3*430),'#202722');d=ImageDraw.Draw(sheet)
for row,design in enumerate(m['designs']):
 for col,t in enumerate(['day','night']):
  key=design['id']+'__'+t;p=r/'outputs/renders'/f'{key}__CAM01_GENERAL.png';im=Image.open(p).convert('RGB');im.save(r/'web/public'/m['states'][key]['render'],quality=91)
  im=ImageOps.fit(im,(600,400));sheet.paste(im,(col*600,row*430+30));d.text((col*600+12,row*430+8),design['label']+' / '+t,fill='#ffffff')
sheet.save(r/'outputs/renders/six-states.jpg',quality=93)
