"""Shared Blender authoring and explicit diffuse-only export pipeline."""
import bpy, math, random, json, time, shutil
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'web/public/assets'
TEX=ROOT/'blender/textures'
CONFIG=json.loads((ROOT/'config/scene-parameters.json').read_text())
RNG=random.Random(7321)
MAT={}; GROUPS={}; LIGHTS=[]; COLLISIONS=[]
CURRENT='surfaces'

def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.samples=48; s.cycles.use_denoising=True
    s.cycles.max_bounces=8; s.cycles.diffuse_bounces=4; s.cycles.glossy_bounces=4; s.cycles.transmission_bounces=6
    s.render.resolution_x=1200; s.render.resolution_y=800; s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG'; s.view_settings.view_transform='AgX'; s.view_settings.look='AgX - Medium High Contrast'
    s.view_settings.look='None'; s.view_settings.exposure=math.log2(1.2)
    s.unit_settings.system='METRIC'; s.unit_settings.scale_length=1
    prefs=bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type='METAL'; prefs.get_devices()
        for d in prefs.devices: d.use=d.type=='METAL'
        s.cycles.device='GPU'
    except Exception: s.cycles.device='CPU'
    s.world=bpy.data.worlds.new('Patio_environment'); s.world.use_nodes=True
    return s

def group(name):
    global CURRENT
    CURRENT=name
    if name not in GROUPS:
        coll=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(coll); GROUPS[name]=coll
    return GROUPS[name]

def register(obj,name,mat=None):
    obj.name=name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    GROUPS[CURRENT].objects.link(obj)
    obj['meshId']=name; obj['sourceGroup']=CURRENT
    if mat: obj.data.materials.append(MAT[mat])
    return obj

def srgb(x): return ((x/255+.055)/1.055)**2.4 if x/255>.04045 else x/255/12.92

def material(name,color,rough=.7,metal=0,texture=None,normal=.3,transmission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; l=m.node_tree.links
    p=n.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*[srgb(x) for x in color],1)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    p.inputs['Transmission Weight'].default_value=transmission
    if texture:
        uv=n.new('ShaderNodeUVMap'); uv.uv_map='UVMap'
        for suffix,socket,cs in [('color','Base Color','sRGB'),('normal','Normal','Non-Color'),('roughness','Roughness','Non-Color')]:
            node=n.new('ShaderNodeTexImage'); node.image=bpy.data.images.load(str(TEX / (f'{texture}_{suffix}.'+('jpg' if suffix=='color' else 'png'))),check_existing=True)
            node.image.colorspace_settings.name=cs; l.new(uv.outputs[0],node.inputs['Vector'])
            if suffix=='normal':
                norm=n.new('ShaderNodeNormalMap'); norm.inputs['Strength'].default_value=normal; l.new(node.outputs['Color'],norm.inputs['Color']); l.new(norm.outputs['Normal'],p.inputs[socket])
            else: l.new(node.outputs['Color'],p.inputs[socket])
    MAT[name]=m
    return m

def materials():
    for name,col,tex in [('wood_new',(153,101,57),'wood_new'),('wood_old',(110,77,46),'wood_old'),('blue',(18,64,101),'stucco_blue'),('aggregate',(151,144,129),'aggregate'),('coping',(184,174,145),'coping'),('grass',(65,88,32),'grass'),('artificial',(43,87,50),'artificial'),('pot',(113,117,113),'concrete'),('red',(172,19,33),'fabric_red'),('grey',(67,72,77),'fabric_grey')]:
        material(name,col,texture=tex,normal=.4 if name in ['blue','aggregate','grass'] else .24)
    for name,col,rough,metal in [('paint',(34,37,39),.52,0),('steel',(112,122,125),.32,.7),('bolt',(46,48,47),.35,.65),('wicker',(66,52,38),.82,0),('soil',(50,40,25),1,0),('leaf',(50,76,25),.73,0),('leaf_light',(79,101,37),.74,0),('pool',(78,170,189),.48,0),('grout',(82,82,72),1,0),('roof',(48,52,55),.65,.05),('neutral',(158,154,141),.93,0)]: material(name,col,rough,metal)
    material('glass',(165,194,190),.13,0,transmission=.65)
    material('water',(137,213,217),.09,0,transmission=.93)
    MAT['water'].node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.333
    # Diffusor: opaque frosted-looking panel with a controlled diffuse transmission component in Cycles.
    m=material('panel',(213,213,195),.5)
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF'); o=n.get('Material Output')
    trans=n.new('ShaderNodeBsdfTranslucent'); trans.inputs['Color'].default_value=(.75,.76,.68,1)
    mix=n.new('ShaderNodeMixShader'); mix.inputs[0].default_value=.28; l.new(p.outputs[0],mix.inputs[1]); l.new(trans.outputs[0],mix.inputs[2]); l.new(mix.outputs[0],o.inputs['Surface'])
    material('lamp',(235,216,170),.32)

def apply_uv(obj,wood=False):
    me=obj.data
    if not me.uv_layers: me.uv_layers.new(name='UVMap')
    me.uv_layers[0].name='UVMap'; uv=me.uv_layers[0].data
    dims=obj.dimensions
    for face in me.polygons:
        n=face.normal; axis=max(range(3),key=lambda k:abs(n[k])); axes=[i for i in range(3) if i!=axis]
        if wood: axes.sort(key=lambda i:dims[i],reverse=True)
        for li in face.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co
            if wood: uv[li].uv=(co[axes[0]]/2+RNG.random()*.0001,co[axes[1]]/.23)
            else:
                scale=.5 if any(m.name in ['aggregate','coping'] for m in me.materials) else 1.2
                uv[li].uv=(co[axes[0]]/scale,co[axes[1]]/scale)

def box(name,pos,size,mat,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos); o=register(bpy.context.object,name,mat); o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); apply_uv(o,'wood' in mat)
    if bevel:
        mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=bevel; mod.segments=2
    return o

def mesh(name,verts,faces,mat,uv=True):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update(); o=bpy.data.objects.new(name,me); GROUPS[CURRENT].objects.link(o)
    o['meshId']=name; o['sourceGroup']=CURRENT; o.data.materials.append(MAT[mat])
    if uv: apply_uv(o,'wood' in mat)
    return o

def beam(name,a,b,width,depth,mat,bevel=.006):
    a,b=Vector(a),Vector(b); o=box(name,(a+b)/2,(width,depth,(b-a).length),mat,bevel)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o

def cyl(name,pos,radius,depth,mat,vertices=16,radius2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=radius,radius2=radius if radius2 is None else radius2,depth=depth,location=pos)
    o=register(bpy.context.object,name,mat)
    for f in o.data.polygons: f.use_smooth=len(f.vertices)==4
    return o

def rod(name,a,b,radius,mat,vertices=8):
    a,b=Vector(a),Vector(b); o=cyl(name,(a+b)/2,radius,(b-a).length,mat,vertices); o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

def tube(name,points,radius,mat,closed=False,sides=6):
    verts=[];faces=[]; pts=[Vector(p) for p in points]
    for i,p in enumerate(pts):
        t=pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]; t.normalize()
        up=Vector((0,0,1)) if abs(t.z)<.95 else Vector((0,1,0)); u=t.cross(up).normalized();v=t.cross(u).normalized()
        for j in range(sides): verts.append(p+radius*(math.cos(j*2*math.pi/sides)*u+math.sin(j*2*math.pi/sides)*v))
    for i in range(len(pts) if closed else len(pts)-1):
        for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,((i+1)%len(pts))*sides+(j+1)%sides,((i+1)%len(pts))*sides+j))
    o=mesh(name,verts,faces,mat)
    for f in o.data.polygons:f.use_smooth=True
    return o

def poly(name,points,z,mat):
    verts=[(x,y,z) for x,y in points]; coords=[Vector(v) for v in verts]; tris=tessellate_polygon([coords]); faces=[tuple(v if isinstance(v,int) else coords.index(v) for v in t) for t in tris]
    return mesh(name,verts,faces,mat)

def area_light(name,pos,target,power,size=.16,group_id='common'):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.color=(1,.61,.30); data.shape='DISK'; data.size=size
    o=bpy.data.objects.new(name,data)
    if 'LIGHTING' not in GROUPS:
        coll=bpy.data.collections.new('LIGHTING');bpy.context.scene.collection.children.link(coll);GROUPS['LIGHTING']=coll
    GROUPS['LIGHTING'].objects.link(o); o.location=pos; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o['power_night']=power; o['designId']=group_id
    LIGHTS.append({'id':name,'position':list(pos),'target':list(target),'power_w':power,'size_m':size,'group':group_id})
    return o

def camera(name,pos,target,hfov=72,aspect=1.5):
    data=bpy.data.cameras.new(name); data.type='PERSP'; data.sensor_fit='HORIZONTAL'; data.lens=36/(2*math.tan(math.radians(hfov)/2)); data.sensor_width=36
    o=bpy.data.objects.new(name,data); bpy.context.scene.collection.objects.link(o); o.location=pos; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); o['aspect']=aspect
    return o

def daylight_settings():
    # Exports use the saved master's lighting. Editing the parameter file alone
    # must never silently change a bake attributed to an unchanged source hash.
    saved=bpy.context.scene.get('config_json')
    config=json.loads(saved) if saved else CONFIG
    return config['lighting'].get('day',{'environment_intensity':7.0,'background_intensity':1.2})

def configure_daylight():
    """One natural sun shared by all designs, independent of artificial fixtures."""
    sun=daylight_settings().get('sun')
    if not sun:return
    obj=bpy.data.objects.get('SUN_DAY')
    if obj is None:
        obj=bpy.data.objects.new('SUN_DAY',bpy.data.lights.new('SUN_DAY','SUN'))
        group('LIGHTING').objects.link(obj)
    direction=sun['direction_to_sun_plan']
    toward_sun=Vector((direction[0],-direction[1],direction[2])).normalized()
    obj.location=Vector((3.7,-5,0))+toward_sun*12
    obj.rotation_euler=(-toward_sun).to_track_quat('-Z','Y').to_euler()
    obj.data.color=sun['color_linear'];obj.data.angle=math.radians(sun['angular_diameter_degrees'])
    obj['naturalLight']=True;obj['power_day']=sun['energy'];obj['designId']='common'
    obj['direction_is_design_choice']=True
    return obj

def state(design,time_id):
    configure_daylight()
    for name,c in GROUPS.items():
        if name.startswith('d') and name[1:2].isdigit(): c.hide_render=not name.startswith(design);c.hide_viewport=c.hide_render
    for o in bpy.data.objects:
        if o.type=='LIGHT':
            if o.get('naturalLight'):o.data.energy=o.get('power_day',0) if time_id=='day' else 0
            else:o.data.energy=o.get('power_night',0) if time_id=='night' and o.get('designId','common') in ['common',design] else 0
    n=bpy.context.scene.world.node_tree.nodes; l=bpy.context.scene.world.node_tree.links; n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');env=n.new('ShaderNodeTexEnvironment')
    env.image=bpy.data.images.load(str(TEX/f'sky_{time_id}.jpg'),check_existing=True); l.new(env.outputs['Color'],bg.inputs['Color']);l.new(bg.outputs[0],out.inputs[0]); bg.inputs[1].default_value=daylight_settings()['environment_intensity'] if time_id=='day' else 1.0
    # An 8-bit environment has no absolute photometric calibration. Separate camera display intensity.
    path=n.new('ShaderNodeLightPath'); camera_bg=n.new('ShaderNodeBackground');camera_bg.inputs[1].default_value=daylight_settings()['background_intensity'] if time_id=='day' else 1.0;l.new(env.outputs['Color'],camera_bg.inputs[0]);mix=n.new('ShaderNodeMixShader');l.new(path.outputs['Is Camera Ray'],mix.inputs[0]);l.new(bg.outputs[0],mix.inputs[1]);l.new(camera_bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    p=MAT['lamp'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.53,.18,1);p.inputs['Emission Strength'].default_value=5 if time_id=='night' else 0
    bpy.context.scene['designId']=design;bpy.context.scene['timeId']=time_id

def derive(name,source_group,atlas_size):
    """Explicit derived mesh; original authored objects stay editable and are not overwritten."""
    src=list(GROUPS[source_group].objects); copies=[]; coll=group('WEB_DERIVED')
    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
    for obj in src:
        if obj.type!='MESH':continue
        data=bpy.data.meshes.new_from_object(obj.evaluated_get(deps),depsgraph=deps)
        copy=bpy.data.objects.new(obj.name+'_derived',data);coll.objects.link(copy);copy.matrix_world=obj.matrix_world.copy();copies.append(copy)
    if not copies:return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in copies:o.select_set(True)
    bpy.context.view_layer.objects.active=copies[0]
    if len(copies)>1:bpy.ops.object.join()
    o=bpy.context.object;o.name=name;o['meshId']=name;o['sourceGroup']=source_group
    if not o.data.uv_layers:o.data.uv_layers.new(name='UVMap')
    o.data.uv_layers.new(name='LightmapUV');o.data.uv_layers.active_index=1
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.00005)
    bpy.ops.uv.smart_project(angle_limit=math.radians(20 if 'FURNITURE' in name else 66),island_margin=.00025 if 'VEGETATION' in name else .001,margin_method='FRACTION',area_weight=.7,correct_aspect=True,scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT');o.data.uv_layers.active_index=0
    o['atlasSize']=atlas_size;o.hide_render=True;o.hide_set(True)
    return o

def bake(o,path,size,samples=32):
    s=bpy.context.scene; start=time.monotonic(); s.cycles.samples=samples
    # Replace original members with the identical derived geometry during bake.
    src=GROUPS[o['sourceGroup']];src.hide_render=True
    o.hide_render=False;o.hide_set(False);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    image=bpy.data.images.new(path.stem,width=size,height=size,alpha=False,float_buffer=True)
    image.colorspace_settings.name='Linear Rec.709'
    for mat in o.data.materials:
        n=mat.node_tree.nodes; node=n.get('BAKE_TARGET') or n.new('ShaderNodeTexImage');node.name='BAKE_TARGET';node.image=image;n.active=node
    o.data.uv_layers.active_index=1
    s.render.bake.use_pass_direct=True;s.render.bake.use_pass_indirect=True;s.render.bake.use_pass_color=False;s.render.bake.margin=8;s.render.bake.use_clear=True
    bpy.ops.object.bake(type='DIFFUSE',use_clear=True,margin=1 if 'VEGETATION' in o.name else 3)
    image.filepath_raw=str(path);image.file_format='OPEN_EXR';s.render.image_settings.color_depth='16';s.render.image_settings.exr_codec='ZIP'
    s.render.image_settings.file_format='OPEN_EXR'
    image.save_render(str(path),scene=s)
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8'
    # EXR stores scene-linear values without the display transform.
    import numpy as np
    a=np.empty(size*size*4,dtype=np.float32);image.pixels.foreach_get(a);a=a.reshape(-1,4)[:,:3]
    record={'meshId':o.name,'width':size,'min':float(a.min()),'max':float(a.max()),'mean':float(a.mean()),'seconds':time.monotonic()-start,'uv_channel':1,'encoding':'linear_rec709_half_float','pass':'DIFFUSE direct+indirect; COLOR excluded; no AO'}
    for profile,divisor in [('balanced',2),('low',4)]:
        image.scale(size//divisor,size//divisor)
        s.render.image_settings.file_format='OPEN_EXR';s.render.image_settings.color_depth='16'
        image.save_render(str(path.with_stem(path.stem+'--'+profile)),scene=s)
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8'
    bpy.data.images.remove(image);o.data.uv_layers.active_index=0;o.hide_render=True;o.hide_set(True);src.hide_render=False
    return record

def export_glb(objects,path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.hide_set(False);o.hide_render=False;o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    # Translucent shader is not glTF; export its explicitly corresponding opaque PBR equivalent.
    m=MAT['panel'];out=m.node_tree.nodes.get('Material Output'); original=out.inputs[0].links[0].from_socket
    m.node_tree.links.new(m.node_tree.nodes.get('Principled BSDF').outputs[0],out.inputs[0])
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_texcoords=True,export_normals=True,export_materials='EXPORT',export_extras=True,export_yup=True,export_cameras=False,export_lights=False,export_meshopt_compression_enable=True,export_image_format='WEBP',export_image_quality=92)
    m.node_tree.links.new(original,out.inputs[0])
    for o in objects:o.hide_render=True;o.hide_set(True)

def to_web(v):return [v[0],v[2],-v[1]]

def camera_contract(cam):
    aspect=float(cam.get('aspect',1.5)); rot=cam.rotation_euler.to_quaternion();forward=rot@Vector((0,0,-1));target=cam.location+forward
    return {'id':cam.name,'position':to_web(cam.location),'target':to_web(target),'verticalFov':math.degrees(2*math.atan(math.tan(cam.data.angle_x/2)/aspect)),'aspect':aspect,'near':.06,'far':150}
