"""Conservative image-assisted patio reconstruction; all metres are estimates."""
from scene_lib import *
from plan_geometry import prism, wing_clip, strip

def inside(point,poly):
    x,y=point; odd=False
    for i,(a,b) in enumerate(poly):
        c,d=poly[(i+1)%len(poly)]
        if ((b>y)!=(d>y)) and x<(c-a)*(y-b)/(d-b)+a:odd=not odd
    return odd

def shell():
    group('surfaces')
    g=CONFIG['geometry'];pool=g['pool_outline_xy_m'];width=g['site_width_m'];depth=g['site_depth_m'];left=g.get('site_left_x_m',0)
    # Outdoor ground mosaic, hidden below the accurately modelled coping at its cut edge.
    vs=[];fs=[]
    step=.125
    for i in range(math.ceil((width-left)/step)):
        for j in range(math.ceil(depth/step)):
            x,y=left+i*step,j*step
            if any(inside(p,pool) for p in [(x,y),(x+step,y),(x+step,y+step),(x,y+step),(x+step/2,y+step/2)]):continue
            x2,y2=min(x+step,width),min(y+step,depth)
            k=len(vs);vs.extend([(x,y,-.035),(x2,y,-.035),(x2,y2,-.035),(x,y2,-.035)]);fs.append((k,k+1,k+2,k+3))
    mesh('GROUND_LAWN',vs,fs,'grass')
    # Existing exposed-aggregate paving; no procedural concept pattern.
    module=CONFIG['scale_anchor']['used_value_m']
    for ix in range(math.ceil((width-left)/module)):
        for iy in range(math.ceil((depth-.25)/module)):
            x,y=left+(ix+.5)*module,.25+(iy+.5)*module
            if any(inside((x,y),p) for p in g['paving_polygons_xy_m']):
                box(f'PAVER_{ix:02}_{iy:02}',(x,y,-.012),(module-.012,module-.012,.052),'aggregate',.007)
    # The lawn turns through a small rounded corner, visible in R02 and R03.
    path_right=g['walkway_rect_m'][2]
    arc=[(path_right+.35+.35*math.cos(-math.pi/2-i*math.pi/48),3.30+.35*math.sin(-math.pi/2-i*math.pi/48)) for i in range(25)]
    poly('PAVER_ROUNDED_CORNER',[(path_right,2.95)]+arc,.014,'aggregate')
    vs=[];fs=[]
    for i in range(math.ceil(width/step)):
        for j in range(math.ceil(depth/step)):
            x,y=i*step,j*step;mid=(x+step/2,y+step/2)
            if any(inside(p,pool) for p in [(x,y),(x+step,y),(x+step,y+step),(x,y+step),mid]) or not any(inside(mid,p) for p in g['side_strip_polygons_xy_m']):continue
            k=len(vs);vs.extend([(x,y,-.014),(min(width,x+step),y,-.014),(min(width,x+step),min(depth,y+step),-.014),(x,min(depth,y+step),-.014)]);fs.append((k,k+1,k+2,k+3))
    mesh('ARTIFICIAL_STRIP_RIGHT',vs,fs,'artificial')
    box('BLUE_STUCCO',((width+left)/2,0,.775),(width-left,.16,1.55),'blue',.008)
    box('HOUSE_LIMIT',(left-.055,depth/2,1.25),(.12,depth,2.5),'blue',.006)
    box('NEAR_BOUNDARY',((width+left)/2,depth+.045,.62),(width-left,.12,1.24),'neutral')
    # One tall return, along the right side. The blue wall is the transverse end.
    bay_width=1.30
    for bay in range(math.ceil(depth/bay_width)+1):
        y=min(depth,bay*bay_width)
        box(f'FENCE_POST_0_{bay}',(width,y,1.24),(.09,.09,2.48),'wood_old',.005)
        length=min(bay_width,depth-y)
        if length<=.02:continue
        for row in range(27):
            box(f'FENCE_SLAT_0_{bay:02}_{row:02}',(width+.038,y+length/2,.044+row*.092),(.042,length-.04,.086),'wood_old',.002)
    for bay in range(3):
        x=3.65+bay*1.25
        box(f'LOW_POST_{bay}',(x,.085,1.24),(.085,.09,.71),'wood_old',.004)
        for row in range(8):box(f'LOW_SLAT_{bay}_{row}',(x+.615,.10,.93+row*.086),(1.20,.055,.078),'wood_old',.003)
    # Irregular natural-stone stepping pieces seen beside pool.
    for i,(x,y) in enumerate(g['stepping_stones_xy_m']):
        points=[(x+.35*math.cos(a)*(1+.12*math.sin(a*3)),y+.26*math.sin(a)) for a in [k*2*math.pi/7 for k in range(7)]]
        poly(f'STEPPING_STONE_{i}',points,.012,'coping')
    # Pool coping normal offset, wall, bottom, and water all share the same contour.
    outer=[];inner=[];center=Vector((sum(p[0] for p in pool)/len(pool),sum(p[1] for p in pool)/len(pool)))
    for i,(x,y) in enumerate(pool):
        prev=Vector(pool[i-1]);nxt=Vector(pool[(i+1)%len(pool)]);t=(nxt-prev).normalized();normal=Vector((t.y,-t.x));outer.append((x+normal.x*g['pool_border_width_m'],y+normal.y*g['pool_border_width_m']));inner.append((center.x+(x-center.x)*.85,center.y+(y-center.y)*.9))
    verts=[];faces=[]
    for i,(a,b) in enumerate(zip(pool,outer)):verts.extend([(a[0],a[1],.045),(b[0],b[1],.045),(a[0],a[1],-.08),(b[0],b[1],-.08)])
    for i in range(len(pool)):
        k=i*4;n=((i+1)%len(pool))*4;faces.extend([(k,n,n+1,k+1),(k+2,n+2,n,k),(k+1,n+1,n+3,k+3)])
    coping=mesh('POOL_COPING',verts,faces,'coping');mod=coping.modifiers.new('Rounded coping edge','BEVEL');mod.width=.026;mod.segments=3
    for p in coping.data.polygons:p.use_smooth=True
    verts=[];faces=[]
    for (x,y),(bx,by) in zip(pool,inner):verts.extend([(x,y,.025),(x,y,-.18),(bx,by,-1.4)])
    for i in range(len(pool)):
        k=i*3;n=((i+1)%len(pool))*3;faces.extend([(k,k+1,n+1,n),(k+1,k+2,n+2,n+1)])
    mesh('POOL_BASIN_WALL',verts,faces,'pool');poly('POOL_BASIN_BOTTOM',inner,-1.4,'pool')
    # Mosaic waterline joints are actual geometry, not white specular baked into albedo.
    for i,(x,y) in enumerate(pool):
        x2,y2=pool[(i+1)%len(pool)];rod(f'POOL_TILE_JOINT_{i}',(x,y,-.06),(x,y,-.18),.0025,'grout',4)
    mx,my=g['pool_marker_position_xy_m']
    box('POOL_EDGE_SQUARE',(mx,my,.18),(.32,.33,.31),'pot',.03)
    box('POOL_EDGE_SQUARE_LID',(mx,my,.352),(.35,.35,.045),'coping',.035)
    group('water');poly('WATER_SURFACE',pool,-.14,'water')
    # Water micro-normal in Blender: world-space ripples. Web uses the same scale in its animated shader.
    m=MAT['water'];nodes=m.node_tree.nodes;links=m.node_tree.links;noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=32;noise.inputs['Detail'].default_value=2
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.045;links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs[0],nodes.get('Principled BSDF').inputs['Normal'])
    return pool

def deck():
    group('surfaces')
    g=CONFIG['geometry'];a,b,c,d=g['main_deck_rect_m'];e,f,h,j=g['wing_deck_rect_m']
    footprint=g['deck_footprint_xy_m'];A=g['wing_end_corners_xy_m']['A'];B=g['wing_end_corners_xy_m']['B']
    prism('DECK_FOUNDATION_MAIN',footprint,.016,.170,'paint')
    # Split at the inside corner before clipping: no overhanging row or coplanar fascia cap.
    cuts=sorted(set([b,d,j]+[min(j,b+i*.148) for i in range(1,math.ceil((j-b)/.148))]))
    for i,(y0,y1) in enumerate(zip(cuts,cuts[1:])):
        start=a if y1<=d else e;count=3 if y1<=d else 1;length=(h-start)/count
        for k in range(count):
            x0=start+k*length+.003;x1=start+(k+1)*length-.003
            points=[(x0,y0+.003),(x1,y0+.003),(x1,y1-.003),(x0,y1-.003)]
            if y1>d:points=wing_clip(points)
            if len(points)>=3:prism(f'DECK_BOARD_{i}_{k}',points,.174,.220,'wood_new',.002)
    for name,p,q in [('FRONT',(a,d),(e,d)),('INNER',(e,d),A),('WING',A,B),('LEFT',(a,b),(a,d)),('BACK',(a,b),(h,b)),('OUTER',(h,b),B)]:
        strip('DECK_FASCIA_'+name,p,q,.045,.008,.173,'wood_new')


def furniture():
    group('furniture')
    # Four red textile chairs with tubular dark frames, open backs and arms.
    tx,ty=CONFIG['geometry']['table_position_xy_m']
    for idx,(x,y,a) in enumerate([(tx-1.13,ty,math.pi/2),(tx+1.13,ty,-math.pi/2),(tx-.22,ty+.88,0),(tx+.22,ty-.88,math.pi)]):
        def p(u,v,z):return (x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a),z+.22)
        mesh(f'CHAIR_RED_SEAT_{idx}',[p(-.255,-.24,.48),p(.255,-.24,.48),p(.255,.24,.48),p(-.255,.24,.48)],[(0,1,2,3)],'red')
        mesh(f'CHAIR_RED_BACK_{idx}',[p(-.255,.22,.49),p(.255,.22,.49),p(.255,.39,1.05),p(-.255,.39,1.05)],[(0,1,2,3)],'red')
        for sign in [-1,1]:
            rod(f'CHAIR_FRAME_A_{idx}_{sign}',p(sign*.28,-.31,0),p(sign*.28,.4,1.08),.018,'paint')
            rod(f'CHAIR_FRAME_B_{idx}_{sign}',p(sign*.28,.40,0),p(sign*.28,-.25,.68),.018,'paint')
            rod(f'CHAIR_ARM_{idx}_{sign}',p(sign*.29,-.3,.7),p(sign*.29,.32,.75),.022,'paint')
        for z,v in [(1.06,.4),(.48,-.24)]:rod(f'CHAIR_CROSS_{idx}_{z}',p(-.28,v,z),p(.28,v,z),.018,'paint')
        COLLISIONS.append({'id':f'chair_{idx}','type':'circle','x':x,'y':y,'radius':.45})
    # Glass-topped oval rectangular table; high-frequency etched finish inferred from video.
    table=box('TABLE_GLASS',(tx,ty,1.00),(1.5,.94,.035),'glass',.12)
    for sign in [-1,1]:
        rod(f'TABLE_LEG_A_{sign}',(tx+sign*.65,ty-.38,.23),(tx+sign*.48,ty-.29,.985),.022,'steel')
        rod(f'TABLE_LEG_B_{sign}',(tx+sign*.65,ty+.38,.23),(tx+sign*.48,ty+.29,.985),.022,'steel')
    for y in [ty-.46,ty+.46]:rod(f'TABLE_RIM_{y}',(tx-.65,y,1.0),(tx+.65,y,1.0),.018,'steel')
    COLLISIONS.append({'id':'table','type':'box','min':[tx-.78,ty-.5],'max':[tx+.78,ty+.5]})
    for i,x in enumerate([tx-.17,tx+.17]):cyl(f'TABLE_POT_{i}',(x,ty,1.10),.073,.16,'coping',16,radius2=.058)
    # Chaise silhouette with tilted back and stretched grey fabric.
    for idx,(x,y) in enumerate([CONFIG['geometry']['lounger_position_xy_m']]):
        angle=math.radians(42);hinge=Vector((x,y-.54,.64));head=hinge+Vector((0,-.76*math.cos(angle),.76*math.sin(angle)))
        box('LOUNGER_SEAT',(x,y+.17,.64),(.67,1.42,.075),'grey',.025)
        back=box('LOUNGER_BACK',(hinge+head)/2,(.67,.76,.075),'grey',.025);back.rotation_euler.x=-angle
        for dx in [-.37,.37]:
            rod(f'LOUNGER_SIDE_{dx}',(x+dx,hinge.y,.58),(x+dx,y+.85,.58),.025,'paint')
            rod(f'LOUNGER_BACK_FRAME_{dx}',(x+dx,hinge.y,.60),(x+dx,head.y,head.z-.04),.023,'paint')
            rod(f'LOUNGER_STAY_{dx}',(x+dx,y-.30,.56),(x+dx,y-.89,.92),.018,'paint')
            for dy in [-.46,.67]:rod(f'LOUNGER_LEG_{dx}_{dy}',(x+dx,y+dy,.22),(x+dx,y+dy,.58),.023,'paint')
        for idx,yy in enumerate([hinge.y,y+.84]):rod(f'LOUNGER_CROSS_{idx}',(x-.37,yy,.58),(x+.37,yy,.58),.023,'paint')
        rod('LOUNGER_HINGE',(x-.385,hinge.y,.615),(x+.385,hinge.y,.615),.030,'steel')
        COLLISIONS.append({'id':'lounger','type':'box','min':[x-.41,head.y-.07],'max':[x+.41,y+.94]})
    # Open wicker egg chair, standing arc, chain and ring base. No opaque egg proxy.
    cx,cy=CONFIG['geometry']['egg_chair_position_xy_m']
    tube('EGG_BASE',[(cx+.54*math.cos(i*2*math.pi/48),cy+.50*math.sin(i*2*math.pi/48),.25) for i in range(48)],.025,'paint',True,8)
    tube('EGG_SUPPORT',[(cx+.50-.40*(i/23)**3,cy-.08, .25+2.27*i/23) for i in range(24)],.027,'paint',False,10)
    rod('EGG_CHAIN',(cx+.10,cy-.08,2.52),(cx,cy-.08,2.27),.011,'steel')
    tube('EGG_HOOK',[(cx+.043*math.cos(a),cy-.08,2.28+.043*math.sin(a)) for a in [i*math.tau/24 for i in range(24)]],.009,'steel',True)
    # Front opening looks toward +Y, ellipsoidal basket from lower bowl to narrow top.
    for j in range(24):
        phi=math.pi*.75+j/23*math.pi*1.5;pts=[]
        for k in range(20):
            t=.12+(math.pi-.24)*k/19;r=.54*math.sin(t)
            pts.append((cx+r*math.cos(phi),cy-.08+r*.82*math.sin(phi),1.43+.83*math.cos(t)))
        tube(f'EGG_VERTICAL_{j}',pts,.009,'wicker',False,5)
    for j in range(15):
        t=.17+(math.pi-.30)*j/14;r=.54*math.sin(t)
        z=1.43+.83*math.cos(t);closed=z<.87 or z>2.16
        angles=[k/32*math.tau for k in range(32)] if closed else [math.pi*.75+k/31*math.pi*1.5 for k in range(32)]
        pts=[(cx+r*math.cos(a),cy-.08+r*.82*math.sin(a),z) for a in angles]
        tube(f'EGG_WEAVE_{j}',pts,.008,'wicker',closed,5)
    # Diagonal weave, visible through the open basket.
    for j in range(13):
        pts=[]
        for k in range(22):
            t=.25+(math.pi-.5)*k/21;r=.545*math.sin(t);phi=math.pi*.80+j/12*math.pi*1.38+.06*math.sin(k*.4)
            pts.append((cx+r*math.cos(phi),cy-.08+r*.82*math.sin(phi),1.43+.83*math.cos(t)))
        tube(f'EGG_DIAGONAL_{j}',pts,.007,'wicker',False,5)
    cushion=prism('EGG_CUSHION',[(cx+.36*math.cos(a),cy-.08+.255*math.sin(a)) for a in [i*math.tau/48 for i in range(48)]],.85,.96,'grey',.035)
    COLLISIONS.append({'id':'egg_chair','type':'circle','x':cx,'y':cy,'radius':.62})


def leaves(name,center,radius,count,mat='leaf',height=1.0):
    vs=[];fs=[];cx,cy,cz=center
    for _ in range(count):
        theta=RNG.uniform(0,math.tau);phi=RNG.uniform(-1,1);r=RNG.random()**.45
        c=Vector((cx+radius*r*math.cos(theta)*math.sqrt(1-phi*phi),cy+radius*r*math.sin(theta)*math.sqrt(1-phi*phi),cz+height*phi))
        direction=Vector((math.cos(theta),math.sin(theta),RNG.uniform(-.25,.65))).normalized();side=direction.cross(Vector((0,0,1))).normalized();lng=RNG.uniform(.055,.145);w=lng*.29;k=len(vs)
        vs.extend([c-direction*lng,c+side*w,c+direction*lng,c-side*w,c+Vector((0,0,.015))]);fs.extend([(k,k+1,k+4),(k+1,k+2,k+4),(k+2,k+3,k+4),(k+3,k,k+4)])
    return mesh(name,vs,fs,mat)

def landscaping():
    group('vegetation')
    for idx,(x,y) in enumerate(CONFIG['geometry']['planter_positions_xy_m']):
        cyl(f'PLANT_POT_{idx}',(x,y,.49),.28,.54,'pot',8,radius2=.37)
        cyl(f'PLANT_RIM_{idx}',(x,y,.755),.382,.055,'pot',8)
        cyl(f'PLANT_SOIL_{idx}',(x,y,.786),.34,.025,'soil',16)
        rod(f'PLANT_TRUNK_{idx}',(x,y,.78),(x+.08,y,1.9),.035,'wood_old')
        leaves(f'PLANT_LEAVES_{idx}',(x,y,1.72),.47,650,'leaf',.81)
        leaves(f'PLANT_LEAVES_LIGHT_{idx}',(x+.07,y+.08,1.73),.48,180,'leaf_light',.74)
        COLLISIONS.append({'id':f'planter_{idx}','type':'circle','x':x,'y':y,'radius':.41})
    # Sparse visible vegetation above fences, not invented buildings or scenery.
    for idx,(x,y,z,r) in enumerate([(-.6,1,2.5,.9),(3,-.8,3.35,1.1),(6.7,-.75,3.0,1),(8.1,2,3,1.05),(8.1,7.4,2.8,1)]):
        rod(f'BACKGROUND_TRUNK_{idx}',(x,y,1.5),(x+.08,y,3.4),.045,'wood_old')
        leaves(f'BACKGROUND_TREE_{idx}',(x,y,z),r,2700,'leaf',.95)
        leaves(f'BACKGROUND_TREE_LIGHT_{idx}',(x,y,z+.1),r,650,'leaf_light',.9)
    # Physical grass blades supplement the varied fine texture in the exposed lawn.
    verts=[];faces=[];g=CONFIG['geometry'];pool=g['pool_outline_xy_m']
    for i in range(12000):
        x=RNG.uniform(.98,g['site_width_m']-.3);y=RNG.uniform(3.08,g['site_depth_m']-.1)
        if inside((x,y),g['deck_footprint_xy_m']) or inside((x,y),pool) or any(inside((x,y),p) for p in g['side_strip_polygons_xy_m']):continue
        if min((Vector((x,y))-Vector(p)).length for p in pool)<.43:continue
        h=RNG.uniform(.016,.047);w=RNG.uniform(.002,.006);theta=RNG.random()*math.tau;dx=w*math.cos(theta);dy=w*math.sin(theta);k=len(verts)
        verts.extend([(x-dx,y-dy,-.03),(x+dx,y+dy,-.03),(x+dx*.6,y+dy*.6,h-.03)]);faces.append((k,k+1,k+2))
    mesh('LAWN_BLADES',verts,faces,'leaf_light')



from patio_structures import lights_common, design
