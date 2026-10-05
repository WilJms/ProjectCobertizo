import * as THREE from 'three';
import {CollisionWorld} from './collision';
import type {CameraPose} from './types';
export class Navigation {
 keys=new Set<string>();yaw=0;pitch=0;touchMove={x:0,y:0};private drag?:{id:number;x:number;y:number};private moving=false;
 constructor(public camera:THREE.PerspectiveCamera,public world:CollisionWorld,public canvas:HTMLCanvasElement){
  camera.rotation.order='YXZ';
  window.addEventListener('keydown',e=>{if((e.target as HTMLElement)?.matches('input,select,textarea'))return;if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','ShiftLeft'].includes(e.code)){this.keys.add(e.code);e.preventDefault();}});
  window.addEventListener('keyup',e=>this.keys.delete(e.code));window.addEventListener('blur',()=>this.keys.clear());
  document.addEventListener('visibilitychange',()=>{if(document.hidden)this.keys.clear();});
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0||document.pointerLockElement)return;this.drag={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',e=>{if(document.pointerLockElement===canvas)this.look(e.movementX,e.movementY);else if(this.drag?.id===e.pointerId){this.look(e.clientX-this.drag.x,e.clientY-this.drag.y);this.drag.x=e.clientX;this.drag.y=e.clientY;}});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(event,()=>{this.drag=undefined;});
 }
 look(dx:number,dy:number){this.yaw-=dx*.0025;this.pitch=THREE.MathUtils.clamp(this.pitch-dy*.0025,-1.2,1.2);this.camera.rotation.set(this.pitch,this.yaw,0);}
 pose(p:CameraPose){this.camera.position.fromArray(p.position);this.camera.lookAt(new THREE.Vector3().fromArray(p.target));this.yaw=this.camera.rotation.y;this.pitch=this.camera.rotation.x;this.camera.fov=p.verticalFov;this.camera.updateProjectionMatrix();this.moving=false;}
 reconcile(){const [x,z]=this.world.nearest(this.camera.position.x,this.camera.position.z);const moved=Math.hypot(x-this.camera.position.x,z-this.camera.position.z)>.001;this.camera.position.x=x;this.camera.position.z=z;return moved;}
 update(dt:number){
  const forward=Number(this.keys.has('KeyW')||this.keys.has('ArrowUp'))-Number(this.keys.has('KeyS')||this.keys.has('ArrowDown'))-this.touchMove.y;
  const sideways=Number(this.keys.has('KeyD'))-Number(this.keys.has('KeyA'))+this.touchMove.x;
  const turn=Number(this.keys.has('ArrowLeft'))-Number(this.keys.has('ArrowRight'));if(turn){this.yaw+=turn*dt*1.2;this.camera.rotation.set(this.pitch,this.yaw,0);}
  if(forward||sideways){const speed=(this.keys.has('ShiftLeft')?2.8:1.7)*dt/Math.max(1,Math.hypot(forward,sideways));const dx=(-Math.sin(this.yaw)*forward+Math.cos(this.yaw)*sideways)*speed;const dz=(-Math.cos(this.yaw)*forward-Math.sin(this.yaw)*sideways)*speed;
   const [x,z]=this.world.move(this.camera.position.x,this.camera.position.z,dx,dz);this.camera.position.x=x;this.camera.position.z=z;this.moving=true;
  }
  if(this.moving){const target=this.world.height(this.camera.position.x,this.camera.position.z)+this.world.config.eyeHeight;this.camera.position.y=THREE.MathUtils.damp(this.camera.position.y,target,9,dt);}
 }
 attachJoystick(el:HTMLElement){
  let active:number|undefined;const knob=el.querySelector<HTMLElement>('.joystick-knob')!;
  const update=(e:PointerEvent)=>{const rect=el.getBoundingClientRect(),x=(e.clientX-rect.left-rect.width/2)/35,y=(e.clientY-rect.top-rect.height/2)/35,n=Math.max(1,Math.hypot(x,y));this.touchMove={x:x/n,y:y/n};knob.style.transform=`translate(${x/n*29}px,${y/n*29}px)`;};
  el.addEventListener('pointerdown',e=>{active=e.pointerId;el.setPointerCapture(active);update(e);e.preventDefault();});el.addEventListener('pointermove',e=>{if(e.pointerId===active)update(e);});
  const stop=()=>{active=undefined;this.touchMove={x:0,y:0};knob.style.transform='';};for(const event of ['pointerup','pointercancel','lostpointercapture'])el.addEventListener(event,stop);
 }
}
