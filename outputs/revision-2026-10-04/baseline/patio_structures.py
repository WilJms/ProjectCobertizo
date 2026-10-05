"""Structures follow the corrected transverse terrace and right-hand return."""
from scene_lib import *

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
    points=[(x,3.08,'front') for x in [1.0,2.4,3.8,5.2]]+[(5.83,y,'side') for y in [3.8,4.8,5.8]]+[(x,6.18,'front') for x in [6.25,7.0]]
    for idx,(x,y,direction) in enumerate(points):
        size=(.12,.014,.045) if direction=='front' else (.014,.12,.045)
        box(f'RISER_HOUSING_{idx}',(x,y,.12),(size[0]+.024,size[1]+.024,.066),'paint',.003)
        box(f'RISER_LENS_{idx}',(x-.013 if direction=='side' else x,y+.013 if direction=='front' else y,.12),size,'lamp',.002)
        target=(x,y+.45,-.02) if direction=='front' else (x-.45,y,-.02)
        area_light(f'RISER_LIGHT_{idx}',(x-.025 if direction=='side' else x,y+.025 if direction=='front' else y,.12),target,3.4,.10)
    for idx,(x,y) in enumerate(g['planter_positions_xy_m']):
        cyl(f'UPLIGHT_BODY_{idx}',(x,y+.2,.25),.05,.10,'paint')
        area_light(f'PLANT_UPLIGHT_{idx}',(x,y+.22,.32),(x,y,1.8),20,.09)

def design(design_id):
    group(design_id);iswood=design_id.startswith('d1');panel=design_id.startswith('d3');m='wood_new' if iswood else 'paint'
    d=next(d for d in CONFIG['designs'] if d['id']==design_id);params=d['parameters'];posts=params['post_positions_xy_m']
    for idx,(x,y) in enumerate(posts):
        h=2.72 if x<5.8 else 2.53
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
      ('winginner',(5.99,.25,2.47),(5.99,6.10,2.47)),
      ('wingouter',(7.08,.25,2.47),(7.08,6.10,2.47)),
      ('wingend',(5.85,5.96,2.47),(7.22,5.96,2.47))]:
        beam(design_id+'_'+name,a,b,.16,.21,m)
    if iswood:
        ridge=params['ridge_height_m'];cx=2.995
        for idx,y in enumerate([.35,1.6,2.86]):
            for x in [.15,5.84]:beam(f'{design_id}_RAFTER_{idx}_{x}',(x,y,2.77),(cx,y,ridge),.115,.17,'wood_new')
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
    # Narrow return follows the tall fence, stopping before the observed pool arc.
    for i in range(9):beam(f'{design_id}_WING_RAFTER_{i}',(5.86,.18+i*.73,2.57),(7.30,.18+i*.73,2.61),.06,.11,m)
    if panel:
        for i in range(8):box(f'{design_id}_WING_PANEL_{i}',(6.58,.55+i*.73,2.635),(1.43,.66,.04),'panel',.004)
    else:
        for i in range(41):box(f'{design_id}_WING_SLAT_{i}',(6.58,.14+i*.148,2.635),(1.47,.142,.045),'wood_new',.002)
        box(f'{design_id}_WING_WEATHER',(6.58,3.13,2.675),(1.52,6.18,.04),'roof')
    beam(f'{design_id}_WING_FRONT_FASCIA',(5.81,.04,2.65),(5.81,6.24,2.65),.10,.16,'roof')
    beam(f'{design_id}_WING_END',(5.81,6.24,2.65),(7.35,6.24,2.65),.1,.16,'roof')
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
