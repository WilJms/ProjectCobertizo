import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {assetUrl,bakedMaterial,loadEnvironment,loadLightmap} from './lighting';
import {PoolWater} from './water';
import type {Manifest,Quality,SceneState} from './types';
type Loaded={key:string;root:THREE.Group;maps:THREE.Texture[];mats:THREE.Material[];state:SceneState;quality:Quality};
export class PatioScene {
 scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(55,1,.06,150);renderer:THREE.WebGLRenderer;water?:PoolWater;
 active?:Loaded;private loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);private geometry=new Map<string,Promise<THREE.Group>>();private environments=new Map<string,ReturnType<typeof loadEnvironment>>();private cache=new Map<string,Loaded>();private serial=0;private pending?:{key:string,quality:Quality,serial:number};private loading=false;private reflect?:THREE.Object3D['onBeforeRender'];private frame=0;
 onState?:(state:SceneState,quality:Quality)=>void;onStatus?:(status:string,error?:boolean)=>void;
 private reflectedPosition=new THREE.Vector3(Infinity,Infinity,Infinity);private reflectedRotation=new THREE.Quaternion();private forceReflection=true;private commits=0;
 constructor(public manifest:Manifest,canvas:HTMLCanvasElement){
  this.renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance',preserveDrawingBuffer:false});
  this.renderer.toneMapping=THREE.AgXToneMapping;this.renderer.outputColorSpace=THREE.SRGBColorSpace;this.renderer.info.autoReset=false;
 }
 async model(uri:string){let task=this.geometry.get(uri);if(!task){task=this.loader.loadAsync(assetUrl(uri)).then(g=>g.scene);this.geometry.set(uri,task);task.catch(()=>this.geometry.delete(uri));}return task;}
 async environment(state:SceneState){let task=this.environments.get(state.timeId);if(!task){task=loadEnvironment(state.environment.uri,this.renderer);this.environments.set(state.timeId,task);task.catch(()=>this.environments.delete(state.timeId));}return task;}
 request(key:string,quality:Quality){if(!this.loading&&this.active?.key===key+'__'+quality)return;this.pending={key,quality,serial:++this.serial};void this.run();}
 private release(item:Loaded){item.mats.forEach(m=>m.dispose());item.maps.forEach(m=>m.dispose());}
 private async prepare(key:string,quality:Quality){
  const cacheKey=key+'__'+quality;const cached=this.cache.get(cacheKey);if(cached){this.cache.delete(cacheKey);this.cache.set(cacheKey,cached);return cached;}
  const state=this.manifest.states[key];if(!state)throw Error('Estado desconocido');const maps:THREE.Texture[]=[];const mats:THREE.Material[]=[];
  try{
   const [common,variant]=await Promise.all([this.model(this.manifest.commonModel),this.model(state.model)]);
   // allSettled guarantees cleanup even if one of the independent texture downloads fails.
   const results=await Promise.allSettled(state.lightmaps.map(m=>loadLightmap(quality==='high'?m.uri:m.uri.replace('.exr',`--${quality}.exr`))));
   for(const r of results)if(r.status==='fulfilled')maps.push(r.value);
   const failure=results.find(r=>r.status==='rejected');if(failure?.status==='rejected')throw failure.reason;
   const lookup=new Map(state.lightmaps.map((m,i)=>[m.meshId,maps[i]]));
   const root=new THREE.Group();root.add(common.clone(true),variant.clone(true));root.updateMatrixWorld(true);
   root.traverse(object=>{
    if(!(object instanceof THREE.Mesh))return;
    if(object.name.startsWith('WATER')){if(!this.water){this.water=new PoolWater(object);this.scene.add(this.water.mesh);this.reflect=this.water.mesh.onBeforeRender;}object.visible=false;return;}
    let parent:THREE.Object3D|null=object;let meshId='';while(parent){if(parent.userData.meshId){meshId=parent.userData.meshId;break;}parent=parent.parent;}
    const lightmap=lookup.get(meshId)||state.lightmaps.map(m=>m.meshId).filter(id=>object.name.startsWith(id)).map(id=>lookup.get(id))[0];
    if(!lightmap||!object.geometry.attributes.uv1)throw new Error(`Falta luz o TEXCOORD_1: ${object.name}`);
    const source=Array.isArray(object.material)?object.material:[object.material];
    const adapted=source.map(material=>{
      const m=bakedMaterial(material,lightmap);
      if(m.name==='lamp'){m.emissive.setRGB(1,.53,.18);m.emissiveIntensity=state.emissionStrength;}
      if(m.name==='panel'){m.side=THREE.DoubleSide;/* Diffuse transmission to other surfaces is already baked in Cycles. */}
      for(const tex of [m.map,m.normalMap,m.roughnessMap])if(tex)tex.anisotropy=Math.min(quality==='high'?8:4,this.renderer.capabilities.getMaxAnisotropy());
      mats.push(m);return m;
    });object.material=Array.isArray(object.material)?adapted:adapted[0];
   });return {key:cacheKey,root,maps,mats,state,quality};
  }catch(error){mats.forEach(m=>m.dispose());maps.forEach(m=>m.dispose());throw error;}
 }
 private async run(){
  if(this.loading)return;this.loading=true;
  while(this.pending){const request=this.pending;this.pending=undefined;this.onStatus?.('Preparando escena…');
   let prepared:Loaded|undefined;
   try{
    const item=await this.prepare(request.key,request.quality);prepared=item;const env=await this.environment(item.state);
    if(request.serial!==this.serial){if(!this.cache.has(item.key))this.release(item);continue;}
    if(this.active)this.scene.remove(this.active.root);
    this.active=item;this.scene.add(item.root);this.forceReflection=true;this.commits++;this.scene.background=env.background;this.scene.backgroundIntensity=item.state.environment.backgroundIntensity??1;this.scene.environment=env.reflection;this.scene.environmentIntensity=item.state.environment.intensity;this.renderer.toneMappingExposure=item.state.exposure;
    if(this.water)this.water.mesh.material.uniforms.waterColor.value.set(0x467c80).multiplyScalar(item.state.timeId==='day'?.9:.007);
    // Diffuse luminaires are baked; glossy response uses the environment and
    // planar water reflection. Unshadowed point surrogates incorrectly lit
    // the outside of roofs and leaves through the structure.
    this.cache.set(item.key,item);
    while(this.cache.size>2){const oldest=this.cache.keys().next().value!;if(oldest===item.key)break;this.release(this.cache.get(oldest)!);this.cache.delete(oldest);}
    this.onState?.(item.state,item.quality);this.onStatus?.('');
   }catch(error){if(prepared&&!this.cache.has(prepared.key)&&prepared!==this.active)this.release(prepared);console.warn('No se pudo cargar el estado solicitado',error);if(request.serial===this.serial)this.onStatus?.('No se pudo cargar la escena. La vista anterior sigue disponible.',true);}
  }
  this.loading=false;
 }
 render(time:number,quality:Quality){
  if(this.water){this.water.update(time);const interval=this.manifest.profiles[quality].reflectionEvery;
   // Never reuse a reflection from a different pose, viewport or light state.
   const moved=this.camera.position.distanceToSquared(this.reflectedPosition)>1e-10||1-Math.abs(this.camera.quaternion.dot(this.reflectedRotation))>1e-10;
   const refresh=this.forceReflection||moved||this.frame%interval===0;
   this.water.mesh.onBeforeRender=refresh&&this.reflect?this.reflect:()=>{};
   if(refresh){this.reflectedPosition.copy(this.camera.position);this.reflectedRotation.copy(this.camera.quaternion);this.forceReflection=false;}
  }
  this.renderer.info.reset();this.renderer.render(this.scene,this.camera);this.frame++;
 }
 resize(width:number,height:number,quality:Quality){this.renderer.setPixelRatio(Math.min(devicePixelRatio,this.manifest.profiles[quality].pixelRatio));this.renderer.setSize(width,height,false);this.camera.aspect=width/height;this.camera.updateProjectionMatrix();this.forceReflection=true;}
 diagnostics(){const r=this.renderer,gl=r.getContext(),extension=gl.getExtension('WEBGL_debug_renderer_info');const item=this.active;
  let lightmapGpuBytes=0;if(item)for(const map of item.maps){const im=map.image as {width:number,height:number};lightmapGpuBytes+=im.width*im.height*8;}
  return {state:item?.state.designId+'__'+item?.state.timeId,quality:item?.quality,commits:this.commits,drawCalls:r.info.render.calls,triangles:r.info.render.triangles,textures:r.info.memory.textures,geometries:r.info.memory.geometries,lightmapGpuBytesActive:lightmapGpuBytes,cachedStates:this.cache.size,modelCache:this.geometry.size,renderer:extension?gl.getParameter(extension.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),version:gl.getParameter(gl.VERSION),size:r.getSize(new THREE.Vector2()).toArray(),dpr:r.getPixelRatio(),position:this.camera.position.toArray()};
 }
}
