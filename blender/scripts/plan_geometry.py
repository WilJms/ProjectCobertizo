"""Shared polygon operations in authoring plan coordinates (estimated metres)."""
from scene_lib import *

def clip(poly, nx, ny, limit):
    """Keep nx*x + ny*y <= limit. Used to cut boards at the actual diagonal."""
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da=nx*a[0]+ny*a[1]-limit;db=nx*b[0]+ny*b[1]-limit
        if da<=1e-8:out.append(a)
        if (da<0)!=(db<0):
            t=da/(da-db);out.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
    return out

def prism(name,points,bottom,top,mat,bevel=0):
    n=len(points);coords=[Vector((x,y,top)) for x,y in points]
    tris=tessellate_polygon([coords]);faces=[tuple(v if isinstance(v,int) else coords.index(v) for v in t) for t in tris]
    faces += [tuple(i+n for i in reversed(f)) for f in faces[:]]
    faces += [(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    o=mesh(name,[(x,y,top) for x,y in points]+[(x,y,bottom) for x,y in points],faces,mat)
    if bevel:
        mod=o.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=2
    return o

def wing_clip(points,offset=0):
    a,b=CONFIG['geometry']['wing_end_corners_xy_m'].values()
    slope=(b[1]-a[1])/(b[0]-a[0])
    return clip(points,-slope,1,a[1]-slope*a[0]+offset)

def wing_y(x):
    a,b=CONFIG['geometry']['wing_end_corners_xy_m'].values()
    return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])

def strip(name,a,b,width,bottom,top,mat):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);nx=-dy/length*width/2;ny=dx/length*width/2
    return prism(name,[(a[0]-nx,a[1]-ny),(b[0]-nx,b[1]-ny),(b[0]+nx,b[1]+ny),(a[0]+nx,a[1]+ny)],bottom,top,mat,.002)
