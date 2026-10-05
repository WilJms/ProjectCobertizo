import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { PoolWater } from './water';
import { assetUrl, bakedMaterial, loadEnvironment, loadLightmap } from './lighting';
const t=new URLSearchParams(location.search).get('time')||'day';
const manifest=await (await fetch(assetUrl('assets/pilot/manifest.json'))).json();
const state=manifest.states[t];const c=manifest.camera;
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setSize(960,640);renderer.setPixelRatio(1);renderer.toneMapping=THREE.AgXToneMapping;renderer.outputColorSpace=THREE.SRGBColorSpace;document.body.append(renderer.domElement);
const scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(c.verticalFov,c.aspect,.05,100);camera.position.fromArray(c.position);camera.lookAt(new THREE.Vector3().fromArray(c.target));
const [gltf,lm,env]=await Promise.all([new GLTFLoader().loadAsync(assetUrl(state.model)),loadLightmap(state.lightmap),loadEnvironment(state.environment,renderer)]);
scene.background=env.background;scene.environment=env.reflection;scene.environmentIntensity=state.environmentIntensity;
let meshes=0;let uv1=0;
gltf.scene.traverse(o=>{if(o instanceof THREE.Mesh){meshes++;if(o.geometry.attributes.uv1)uv1++;if(!o.name.startsWith('WATER')){const mats=Array.isArray(o.material)?o.material:[o.material];o.material=mats.map(m=>bakedMaterial(m,lm));if(o.material.length===1)o.material=o.material[0];} }});scene.add(gltf.scene);
let pool:PoolWater|undefined;gltf.scene.updateMatrixWorld(true);gltf.scene.traverse(o=>{if(o instanceof THREE.Mesh&&o.name.startsWith('WATER')){pool=new PoolWater(o,512,.085);o.visible=false;}});if(pool){scene.add(pool.mesh);if(t==='night')pool.mesh.material.uniforms.waterColor.value.multiplyScalar(.01);}

renderer.setAnimationLoop(()=>{pool?.update(0);renderer.render(scene,camera);});document.querySelector('#status')!.textContent=`${t} · ${meshes} mallas · ${uv1} con TEXCOORD_1`;
Object.assign(window,{__pilot:{renderer,scene,camera,lm,ready:true,meshes,uv1}});
