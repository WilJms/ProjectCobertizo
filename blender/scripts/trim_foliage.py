"""Prune only leaf faces that physically intersect the union of the three roofs.
Triangle BVH overlap is recorded before deletion; view-dependent overlap alone
does not qualify. Pruned geometry remains identical in all lighting states.
"""
from scene_lib import *
from mathutils.bvhtree import BVHTree
import bmesh

def trim_foliage():
    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
    structure=[]
    for d in CONFIG['designs']:
        for o in GROUPS[d['id']].objects:
            if o.type!='MESH' or any(t in o.name for t in ['DOWNLIGHT','BOLT','BRACKET','FOOT']):continue
            evaluated=o.evaluated_get(deps);me=evaluated.to_mesh();vs=[o.matrix_world@v.co for v in me.vertices]
            bounds=[(min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3)]
            tree=BVHTree.FromPolygons(vs,[list(p.vertices) for p in me.polygons]);structure.append((o.name,bounds,tree));evaluated.to_mesh_clear()
    records=[]
    for o in GROUPS['vegetation'].objects:
        if not any(t in o.name for t in ['LEAVES','TREE']):continue
        vs=[o.matrix_world@v.co for v in o.data.vertices];bounds=[(min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3)]
        tree=BVHTree.FromPolygons(vs,[list(p.vertices) for p in o.data.polygons]);cut=set();hits={}
        for name,box,other in structure:
            if any(bounds[k][1]<box[k][0] or bounds[k][0]>box[k][1] for k in range(3)):continue
            overlap=tree.overlap(other)
            if overlap:hits[name]=len(overlap);cut.update(a for a,b in overlap)
        if cut:
            # Leaves have four triangles sharing one raised centre: remove the
            # whole individual leaf rather than leaving floating triangle tips.
            leaves={i//4 for i in cut};bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index//4 in leaves],context='FACES');bm.to_mesh(o.data);bm.free()
            records.append({'object':o.name,'intersectingLeafCount':len(leaves),'triangleIntersections':hits})
    (ROOT/'outputs/revision-2026-10-04/foliage-intersections.json').write_text(json.dumps(records,indent=2))
