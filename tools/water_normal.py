from pathlib import Path
import numpy as np
from PIL import Image
n=256;y,x=np.mgrid[0:n,0:n]/n
h=np.sin(x*6*np.pi+y*4*np.pi)+.35*np.sin(x*18*np.pi-y*10*np.pi)+.2*np.cos(y*24*np.pi)
dy,dx=np.gradient(h);v=np.stack([-dx*2,-dy*2,np.ones_like(h)],-1);v/=np.linalg.norm(v,axis=-1)[...,None]
r=Path(__file__).resolve().parents[1];Image.fromarray(np.uint8((v*.5+.5)*255)).save(r/'web/public/assets/water-normal.png')
