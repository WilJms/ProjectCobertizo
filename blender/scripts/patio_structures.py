"""Structures follow the corrected transverse terrace and right-hand return."""
from scene_lib import *
from plan_geometry import prism, wing_clip, wing_y, strip

def lights_common():
    group('fixtures');g=CONFIG['geometry'];w=g['site_width_m']
    # Six tall-fence fixtures plus the two separately visible on the low screen.
    for idx,y in enumerate([.75,2.05,3.35,4.65,5.95,7.25]):
        cyl(f'SCONCE_BODY_{idx}',(w-.075,y,1.78),.053,.20,'steel')
        cyl(f'SCONCE_LENS_{idx}',(w-.075,y,1.672),.046,.012,'lamp')
        area_light(f'SCONCE_DOWN_{idx}',(w-.13,y,1.655),(w-.06,y,.1),26,.085)
        area_light(f'SCONCE_UP_{idx}',(w-.13,y,1.895),(w-.035,y,2.46),7,.07)
    for idx,x in enumerate([4.55,6.10],6):
        cyl(f'SCONCE_BODY_{idx}',(x,.16,1.00),.045,.18,'steel')
        cyl(f'SCONCE_LENS_{idx}',(x,.16,.905),.039,.012,'lamp')
        area_light(f'SCONCE_DOWN_{idx}',(x,.19,.89),(x,.06,.15),13,.075)
    idx=0
    for face in g['deck_riser_faces']:
        if not face['count']:continue
        a,b=Vector(face['start']),Vector(face['end']);n=Vector(face['normal'])
        for fraction in [.25,.5,.75]:
            p=a.lerp(b,fraction);body=p+n*.040;lens=p+n*.061;light=p+n*.075
            front=abs(n.y)>.5
            housing=box(f'RISER_HOUSING_{idx}',(*body,.09),(.156,.022,.066) if front else (.022,.156,.066),'paint',.003)
            diffuser=box(f'RISER_LENS_{idx}',(*lens,.09),(.120,.010,.041) if front else (.010,.120,.041),'lamp',.002)
            emitter=area_light(f'RISER_LIGHT_{idx}',(*light,.09),(*(p+n*.50),-.025),3.4,.10)
            for obj in [housing,diffuser,emitter]:obj['riserFace']=face['id'];obj['faceFraction']=fraction
            idx+=1
    assert idx==9
    for idx,(x,y) in enumerate(g['planter_positions_xy_m']):
        cyl(f'UPLIGHT_BODY_{idx}',(x,y+.2,.25),.05,.10,'paint')
        area_light(f'PLANT_UPLIGHT_{idx}',(x,y+.22,.32),(x,y,1.8),20,.09)

def design(design_id):
    group(design_id);iswood=design_id.startswith('d1');panel=design_id.startswith('d3');m='wood_new' if iswood else 'paint'
    d=next(d for d in CONFIG['designs'] if d['id']==design_id);params=d['parameters'];posts=params['post_positions_xy_m']
    g=CONFIG['geometry'];wx,wy,ex,ey=g['wing_deck_rect_m'];A=g['wing_end_corners_xy_m']['A'];B=g['wing_end_corners_xy_m']['B']
    for idx,(x,y) in enumerate(posts):
        h=2.72 if idx<4 else 2.53
        box(f'{design_id}_POST_{idx}',(x,y,(h+.22)/2),(.16,.16,h-.22),m,.007)
        box(f'{design_id}_FOOT_{idx}',(x,y,.26),(.25,.25,.06),'bolt',.004)
        for dx in [-.07,.07]:
            box(f'{design_id}_BRACKET_{idx}_{dx}',(x+dx,y,.37),(.017,.20,.20),'bolt',.003)
            b=cyl(f'{design_id}_BOLT_{idx}_{dx}',(x+dx,y+.102,.36),.014,.01,'steel',10);b.rotation_euler.x=math.pi/2
    for name,a,b in [
      ('mainfront',(.15,2.86,2.65),(5.84,2.86,2.65)),
      ('mainback',(.15,.35,2.65),(5.84,.35,2.65)),
      ('left',(.30,.17,2.65),(.30,3.05,2.65)),
      ('right',(5.70,.17,2.65),(5.70,3.05,2.65)),
      ('winginner',(posts[-2][0],3.04,2.47),(*posts[-2],2.47)),
      ('wingouter',(posts[-1][0],.25,2.47),(*posts[-1],2.47)),
      ('wingend',(*posts[-2],2.47),(*posts[-1],2.47))]:
        beam(design_id+'_'+name,a,b,.16,.21,m)
    if iswood:
        ridge=params['ridge_height_m'];cx=2.995
        for idx,y in enumerate([.35,1.6,2.86]):
            # Keep the complete rafter section below the boarded roof, including
            # its bevel and sloping end; the old centres pierced the left skin.
            for x in [.15,5.84]:beam(f'{design_id}_RAFTER_{idx}_{x}',(x,y,2.66),(cx,y,ridge-.11),.115,.17,'wood_new')
            beam(f'{design_id}_KING_{idx}',(cx,y,2.72),(cx,y,ridge),.12,.12,'wood_new')
            for x in [1.0,4.99]:beam(f'{design_id}_DIAGONAL_{idx}_{x}',(cx,y,2.79),(x,y,3.12),.105,.105,'wood_new')
        for i in range(21):
            y=.04+i*.151
            for sign in [-1,1]:
                beam(f'{design_id}_ROOF_BOARD_{sign}_{i}',(cx+sign*3.00,y,2.72),(cx,y,ridge+.04),.145,.046,'wood_new',.002)
        for sign in [-1,1]:
            roof=mesh(f'{design_id}_ROOF_OUTER_{sign}',[(cx,-.04,ridge+.07),(cx,3.20,ridge+.07),(cx+sign*3.04,3.20,2.74),(cx+sign*3.04,-.04,2.74)],[(0,1,2,3)],'roof')
            sol=roof.modifiers.new('Roof thickness','SOLIDIFY');sol.thickness=.045
            beam(f'{design_id}_FRONT_FASCIA_{sign}',(cx,3.20,ridge+.06),(cx+sign*3.04,3.20,2.74),.10,.12,'roof',.007)
        for x in [.3,5.7]:
            for y in [.35,2.86]:
                other=1 if x<1 else -1
                beam(f'{design_id}_KNEE_{x}_{y}',(x,y,2.11),(x+other*.52,y,2.60),.09,.11,'wood_new')
    else:
        for i in range(9):beam(f'{design_id}_CROSSBEAM_{i}',(.16+i*.71,.08,2.76),(.16+i*.71,3.14,2.71),.065,.11,'paint')
        if panel:
            for i in range(8):box(f'{design_id}_PANEL_{i}',(.515+i*.71,1.62,2.79),(.65,3.10,.045),'panel',.004)
        else:
            for i in range(21):box(f'{design_id}_CEILING_SLAT_{i}',(3.0,.09+i*.15,2.79),(5.91,.144,.047),'wood_new',.002)
        for x in [.06,5.94]:beam(f'{design_id}_EDGE_{x}',(x,.04,2.84),(x,3.17,2.78),.105,.17,'roof')
        beam(f'{design_id}_EDGE_FRONT',(.06,3.17,2.78),(5.96,3.17,2.78),.13,.13,'roof')
        if not panel:box(f'{design_id}_WEATHER_MAIN',(3.0,1.60,2.835),(5.94,3.14,.045),'roof')
    # Join the fixed main roof at x=5.99, then widen only its return beyond y=3.20.
    # Each board/panel is clipped against the same real diagonal as the deck.
    roof_segments=[(5.99,.04,ex+.04,3.20),(wx-.06,3.20,ex+.04,ey+.13)]
    for seg,(x0,y0,x1,y1) in enumerate(roof_segments):
        pitch=.73 if panel else .148
        for i in range(math.ceil((y1-y0)/pitch)):
            lo=y0+i*pitch;hi=min(y1,lo+pitch)
            points=wing_clip([(x0,lo+.003),(x1,lo+.003),(x1,hi-.003),(x0,hi-.003)],.10)
            if len(points)>=3:prism(f'{design_id}_WING_'+('PANEL' if panel else 'SLAT')+f'_{seg}_{i}',points,2.613,2.657,'panel' if panel else 'wood_new',.002)
        for i in range(math.ceil((y1-y0)/.73)):
            y=y0+.035+i*.73;points=wing_clip([(x0,y-.03),(x1,y-.03),(x1,y+.03),(x0,y+.03)],.10)
            if len(points)>=3:prism(f'{design_id}_WING_RAFTER_{seg}_{i}',points,2.505,2.612,m,.003)
        if not panel:
            points=wing_clip([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],.10)
            prism(f'{design_id}_WING_WEATHER_{seg}',points,2.661,2.70,'roof')
    rA=(wx-.06,wing_y(wx-.06)+.10);rB=(ex+.04,wing_y(ex+.04)+.10)
    strip(f'{design_id}_WING_FRONT_FASCIA',(wx-.06,3.20),rA,.10,2.55,2.71,'roof')
    strip(f'{design_id}_WING_END',rA,rB,.10,2.55,2.71,'roof')
    strip(f'{design_id}_WING_OUTER',(ex+.04,.04),rB,.10,2.55,2.71,'roof')
    strip(f'{design_id}_WING_SHOULDER',(wx-.06,3.20),(5.99,3.20),.10,2.55,2.71,'roof')
    points=[]
    for x in [1.1,2.98,4.86]:
        for y in [.9,2.28]:
            z=2.72+(params['ridge_height_m']-2.72)*(1-abs(x-2.995)/2.99)-.14 if iswood else 2.72
            points.append((x,y,z))
    points += [(6.60,y,2.575) for y in [.7,2.30,3.90,5.55]]
    for idx,(x,y,z) in enumerate(points):
        cyl(f'{design_id}_DOWNLIGHT_BODY_{idx}',(x,y,z),.061,.038,'paint')
        cyl(f'{design_id}_DOWNLIGHT_LENS_{idx}',(x,y,z-.023),.047,.012,'lamp')
        area_light(f'{design_id}_DOWNLIGHT_{idx}',(x,y,z-.04),(x,y,.22),40,.11,design_id)
    return posts
