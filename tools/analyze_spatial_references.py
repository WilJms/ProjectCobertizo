"""Reproducible visual reconstruction notes, projections and inferred plan.

Pixel landmarks are manually interpreted, NOT a survey or a camera calibration.
The long wall/ground lines are more stable than extrapolating one small tile.
Run with .venv/bin/python tools/analyze_spatial_references.py [--apply].
"""
from pathlib import Path
import json, math, sys
import numpy as np
from scipy.optimize import least_squares
from scipy.interpolate import CubicSpline
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/spatial-analysis'; OUT.mkdir(parents=True,exist_ok=True)
REF=ROOT/'references'
font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(size): return ImageFont.truetype(font_path,size) if Path(font_path).exists() else ImageFont.load_default(size)

# R03: transverse vanishing point is constrained by the terrace front and wall
# cap. The lawn's rounded corner is NOT used as a straight-line intersection.
vx=np.array([900.,515.,1.]); vy=np.array([-260.,535.,1.]); principal=np.array([480.,640.])
f=float(np.sqrt(-np.dot(vx[:2]-principal,vy[:2]-principal)))
K=np.array([[f,0,480],[0,f,640],[0,0,1.]])
rx=np.linalg.inv(K)@vx;rx/=np.linalg.norm(rx)
ry=-np.linalg.inv(K)@vy;ry/=np.linalg.norm(ry)
rz=-np.cross(rx,ry) # plan X,Y,Z has Y towards the house
eye=1.32 # arbitrary absolute scale, compatible with a phone below eye level
ray=np.linalg.inv(K)@np.array([414.,594.,1.]); translation=ray*(-eye/np.dot(rz,ray))
H=K@np.column_stack([rx,ry,translation]); inv=np.linalg.inv(H)
def unproject(pixel):
    v=inv@np.array([*pixel,1]);return v[:2]/v[2]+[7.4,0]
def project_ground(xy):
    v=H@np.array([xy[0]-7.4,xy[1],1]);return v[:2]/v[2]
camera03=np.array([-rx@translation+7.4,-ry@translation,eye])
forward03=np.array([rx[2],ry[2],rz[2]])

anchors={
 'blue_fence_ground':[414,594], 'terrace_front_right':[489,619],
 'terrace_back_right':[344,602], 'walkway_lawn_middle':[430,976],
 'walkway_lawn_near':[870,1260], 'house_ground_visible':[83,1150],
 'pool_far_water':[844,662], 'pool_inflexion_water':[837,713],
 'pool_left_bulb_water':[820,771], 'pool_left_side_water':[960,815],
}
readings={key:{'pixel':p,'plan_m':unproject(p).round(3).tolist()} for key,p in anchors.items()}

def project(points,pars):
    x,y,z,yaw,pitch,roll,fl=pars
    fw=np.array([math.sin(yaw)*math.cos(pitch),-math.cos(yaw)*math.cos(pitch),-math.sin(pitch)])
    right=np.array([math.cos(yaw),math.sin(yaw),0]);up=np.cross(right,fw)*-1
    right,up=right*math.cos(roll)+up*math.sin(roll),up*math.cos(roll)-right*math.sin(roll)
    q=np.array(points)-[x,y,z];depth=q@fw
    return np.column_stack([480+fl*(q@right)/depth,640-fl*(q@up)/depth])

# Fit an independent R02 pose to shared 3D points, with a small residual expected
# from uncalibrated phone distortion, imprecise contours and irregular construction.
p02=np.array([[7.4,0,0],[7.4,0,1.55],[7.4,0,2.48],[3.65,0,1.55],[5.9,2.85,0],[5.9,.3,0]])
q02=np.array([[827,598],[848,475],[868,394],[474,478],[904,710],[690,610]])
initial=np.array([3.7,6.8,1.5,0,.2,0,540.])
def error02(p):
    return np.r_[(project(p02,p)-q02).ravel(),(p[2]-1.45)*10,p[5]*80]
fit=least_squares(error02,initial,bounds=([-2,3,.9,-1,-.4,-.15,280],[7,15,2.1,1,.7,.15,1100]))
p=fit.x;forward02=[math.sin(p[3])*math.cos(p[4]),-math.cos(p[3])*math.cos(p[4]),-math.sin(p[4])]

# Trace the visible far arc. Only the return towards the unseen house is completed.
# Counterclockwise outline; periodic cubic interpolation makes one continuous rim.
pool_controls=[[6.92,7.95],[6.50,7.35],[5.78,7.00],[5.19,6.91],[4.57,6.97],[4.16,7.07],
 [3.73,7.03],[3.36,7.00],[3.08,7.08],[2.92,7.28],[2.93,7.85],[3.02,9.70],
 [3.60,10.85],[4.70,11.25],[5.93,10.95],[6.75,10.00],[6.92,7.95]]
cp=np.array(pool_controls);ts=np.r_[0,np.cumsum(np.linalg.norm(np.diff(cp,axis=0),axis=1))]
curve=CubicSpline(ts,cp,bc_type='periodic');pool=curve(np.linspace(0,ts[-1],112,endpoint=False))
area=np.sum(pool[:,0]*np.roll(pool[:,1],-1)-np.roll(pool[:,0],-1)*pool[:,1])/2
if area<0:pool=pool[::-1]
footprint=[[.12,.14],[7.25,.14],[7.25,6.15],[5.86,6.15],[5.86,3.05],[.12,3.05]]
posts=[[.30,.35],[.30,2.86],[5.70,.35],[5.70,2.86],[7.08,.35],[5.99,5.96],[7.08,5.96]]
photo_cameras=[
 {'id':'PHOTO_R03_GENERAL','reference':'r03_general','position_plan':camera03.round(5).tolist(),'target_plan':(camera03+forward03*6).round(5).tolist(),'horizontal_fov_degrees':float(np.degrees(2*np.arctan(480/f))),'aspect':.75},
 {'id':'PHOTO_R02_TERRAZA','reference':'r02_terraza','position_plan':p[:3].round(5).tolist(),'target_plan':(p[:3]+np.array(forward02)*6).round(5).tolist(),'horizontal_fov_degrees':float(np.degrees(2*np.arctan(480/p[6]))),'aspect':.75},
 {'id':'PHOTO_R01_CERCO','reference':'r01_cerco','position_plan':[3.15,5.35,1.5],'target_plan':[7.4,5.35,-.75],'horizontal_fov_degrees':94.0,'aspect':.75},
]
report={'status':'inferred_visual_reconstruction_not_survey','reference_size':[960,1280],
 'method':'long ground/wall directions, shared corners across R02/R03, paving module counts, independent R01 check',
 'r03_vanishing_points_px':[vx[:2].tolist(),vy[:2].tolist()], 'r03_focal_px':f,
 'scale':'0.45 m provisional tile module; inferred eye height 1.32 m for R03 is not measured',
 'readings':readings,'r02_shared_landmarks':{'world':p02.tolist(),'pixels':q02.tolist(),'projected':project(p02,p).round(2).tolist(),'rms_px':float(np.sqrt(np.mean((project(p02,p)-q02)**2)))},
 'pool_controls_m':pool_controls,'pool_unobserved':'near return after the visible left arc, basin and depth',
 'limitations':['Not a calibrated reconstruction. Pinhole fit ignores residual phone lens distortion.',
 'Small four-point tile homographies were rejected: distant extrapolation is unstable.',
 'The near patio boundary and near pool cap are conservative completions; they are not visible in supplied media.'],
 'photo_cameras':photo_cameras}
(OUT/'spatial-inference.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

# Reference overlay: geometry projections, with points actually used identified.
im=Image.open(REF/'WhatsApp Image 2026-10-01 at 21.35.57.jpeg').convert('RGB');draw=ImageDraw.Draw(im)
for pts,col in [([[0,0],[7.4,0],[7.4,11.6]],'#ffcd47'),([[.9,11.6],[.9,3.3],[1.15,2.95],[5.9,2.85],[5.9,.3]],'#64ed9b'),(pool.tolist()+[pool[0].tolist()],'#f884d4')]:
    for a,b in zip(pts,pts[1:]):
        segment=[]
        for t in np.linspace(0,1,180):
            xy=np.array(a)*(1-t)+np.array(b)*t;v=H@np.array([xy[0]-7.4,xy[1],1])
            if v[2]>.25:
                u,vv=v[:2]/v[2]
                if -200<u<1160 and -200<vv<1480:segment.append((u,vv))
        if len(segment)>1:draw.line(segment,fill=col,width=4)
for idx,(key,row) in enumerate(readings.items(),1):
    x,y=row['pixel'];draw.ellipse((x-5,y-5,x+5,y+5),fill='#ffe247',outline='black',width=1);draw.text((x+7,y-18),str(idx),font=font(20),fill='white',stroke_width=2,stroke_fill='black')
draw.rectangle((12,12,948,96),fill='#102123');draw.text((28,23),'R03 · Relaciones inferidas y arco visible de piscina',font=font(24),fill='white');draw.text((28,60),'Amarillo: cierres | Verde: suelo | Rosa: agua · Escala estimada',font=font(19),fill='white')
im.save(OUT/'r03-spatial-overlay.png')
im=Image.open(REF/'WhatsApp Image 2026-10-01 at 21.35.57 (2).jpeg').convert('RGB');draw=ImageDraw.Draw(im)
for a,b in zip(q02,project(p02,p)):
    x,y=a;u,v=b;draw.ellipse((x-6,y-6,x+6,y+6),outline='#ffce54',width=3);draw.line((u-7,v,u+7,v),fill='#57e7d1',width=3);draw.line((u,v-7,u,v+7),fill='#57e7d1',width=3)
im.save(OUT/'r02-shared-landmarks.png')

# A separate top view explicitly labels the unobserved completion.
im=Image.new('RGB',(1000,1460),'#f1eee5');draw=ImageDraw.Draw(im);scale=96;ox=135;oy=130
def plan(points):return [(ox+x*scale,oy+y*scale) for x,y in points]
draw.text((50,28),'Planta reconstruida · proporciones inferidas',font=font(30),fill='#253e37')
draw.text((50,70),'No es un levantamiento métrico. Fotos y video gobiernan el patio.',font=font(20),fill='#536058')
draw.polygon(plan([[0,0],[7.4,0],[7.4,12.3],[0,12.3]]),fill='#9eae79')
draw.polygon(plan([[0,0],[5.9,0],[5.9,2.95],[.9,2.95],[.9,12.3],[0,12.3]]),fill='#c2bba9')
draw.polygon(plan([[5.9,0],[7.4,0],[7.4,12.3],[5.9,12.3]]),fill='#59825a')
tangent=np.roll(pool,-1,axis=0)-np.roll(pool,1,axis=0);normal=np.column_stack([tangent[:,1],-tangent[:,0]]);normal/=np.linalg.norm(normal,axis=1)[:,None]
draw.polygon(plan(pool+normal*.38),fill='#e3d3ad');draw.polygon(plan(pool),fill='#5bbfc9')
draw.polygon(plan(footprint),fill='#b88759',outline='#78552f',width=3)
draw.line(plan([[0,0],[7.4,0]]),fill='#176f97',width=12);draw.line(plan([[7.4,0],[7.4,12.3]]),fill='#67412e',width=10)
for x,y in posts:draw.rectangle((ox+x*scale-5,oy+y*scale-5,ox+x*scale+5,oy+y*scale+5),fill='#323735')
for xy,label in [((1,1.15),'Comedor'),((5.98,3.9),'Ala'),((1.45,4.25),'Césped'),((3.65,8.25),'Piscina'),((1.2,11.8),'Cierre próximo inferido')]:
    x,y=plan([xy])[0];draw.text((x,y),label,font=font(23),fill='#153d39')
draw.text((ox,oy-36),'Muro azul: ancho de trabajo 7,40 m',font=font(21),fill='#176f97')
draw.text((50,1370),'Módulo provisional: 0,45 m · terraza ~13 × 6 módulos · paso ~2 módulos',font=font(20),fill='#364b3f')
draw.text((50,1400),'El extremo próximo de piscina y patio se completa por continuidad.',font=font(20),fill='#364b3f')
im.save(OUT/'inferred-plan.png')

if '--apply' in sys.argv:
    path=ROOT/'config/scene-parameters.json';config=json.loads(path.read_text())
    archive=OUT/'scene-parameters-before-spatial-correction.json'
    if not archive.exists():archive.write_text(path.read_text())
    config['spatial_revision']='2026-10-03-reference-reconstruction-v2'
    config['notes']='Escala inferida, no medida. Muro azul en Y=0; cerco alto en X=7.4. Evidencia y límites: outputs/spatial-analysis/spatial-inference.json.'
    config['scale_anchor'].update(used_value_m=.45,status='reestimated_visual_module',confidence='low_absolute_medium_relative')
    g=config['geometry'];g.update(patio_boundary_xy_m=[[0,0],[7.4,0],[7.4,12.3],[0,12.3]],pool_outline_xy_m=pool.round(5).tolist(),pool_border_width_m=.38,
      paving_polygons_xy_m=[[[0,.25],[5.9,.25],[5.9,2.95],[.9,2.95],[.9,12.3],[0,12.3]]],
      grass_polygons_xy_m=[[[.9,2.95],[5.9,2.95],[5.9,6.25],[7.0,6.25],[7.0,12.3],[.9,12.3]]],
      side_strip_polygons_xy_m=[[[5.9,0],[7.4,0],[7.4,12.3],[5.9,12.3]]],
      deck_footprint_xy_m=footprint,
      fence_segments=[{'id':'blue_wall','from':[0,0],'to':[7.4,0],'height':1.55},
       {'id':'low_slats','from':[3.65,0],'to':[7.4,0],'bottom':.89,'height':.69},
       {'id':'high_slats','from':[7.4,0],'to':[7.4,12.3],'height':2.48}],
      house_side_boundary_solution='Plano azul simple X=0; límite próximo Y=12.3 inferido. Sin casa detallada.',
      site_width_m=7.4,site_depth_m=12.3,main_deck_rect_m=[.12,.14,5.86,3.05],wing_deck_rect_m=[5.86,.14,7.25,6.15],
      pool_marker_position_xy_m=[3.88,6.68],stepping_stones_xy_m=[[2.18,8.0],[2.05,8.85],[2.12,9.75]],
      planter_positions_xy_m=[[.65,.72],[5.23,.74]],table_position_xy_m=[2.90,1.68],egg_chair_position_xy_m=[6.48,1.11],lounger_position_xy_m=[6.47,4.13])
    for d in config['designs']:
        d['status']='modeled_spatial_revision_in_progress';d['parameters'].update(post_positions_xy_m=posts,eave_heights_m=[2.72,2.53],ridge_height_m=3.91 if d['id'].startswith('d1') else 2.84,roof_outline_xy_m=footprint)
    cams=[([.38,8.65,1.9],[4.1,2.7,1.45],80),([3.50,6.0,1.75],[3.7,.3,1.4],76),([2.05,5.5,1.72],[7.2,5.55,1.0],78),([2.0,2.58,1.89],[4.1,.85,2.65],76),([1.70,8.30,1.73],[5.00,8.00,-.1],72)]
    for c,(pos,target,fov) in zip(config['comparison_cameras'],cams):
        c.update(position_plan=pos,target_plan=target,horizontal_fov_degrees=fov,aspect=1.5,accuracy='content_match_inspection; separate PHOTO cameras preserve portrait reference projection')
    config['photo_comparison_cameras']=photo_cameras
    path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':str(OUT/'spatial-inference.json'),'r02_rms_px':report['r02_shared_landmarks']['rms_px'],'photo_cameras':photo_cameras},ensure_ascii=False))
