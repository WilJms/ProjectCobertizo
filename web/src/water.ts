import * as THREE from 'three';
import { Water } from 'three/addons/objects/Water.js';
import { assetUrl } from './lighting';
export class PoolWater {
 mesh: Water; normal: THREE.Texture; base: THREE.BufferGeometry;
 constructor(source:THREE.Mesh,public resolution=512, public level=-.14){
  source.updateWorldMatrix(true,false);this.base=source.geometry.clone().applyMatrix4(source.matrixWorld);
  // glTF geometry is world Y-up. Water's reflection plane is local +Z.
  this.base.translate(0,-this.level,0).rotateX(Math.PI/2);
  this.normal=new THREE.TextureLoader().load(assetUrl('assets/water-normal.png'));
  this.normal.wrapS=this.normal.wrapT=THREE.RepeatWrapping;this.normal.colorSpace=THREE.NoColorSpace;
  this.mesh=this.make(resolution);
 }
 private make(resolution:number){
  const water=new Water(this.base,{textureWidth:resolution,textureHeight:resolution,waterNormals:this.normal,sunDirection:new THREE.Vector3(0,1,0),sunColor:0x000000,waterColor:0x467c80,distortionScale:.19,alpha:.58,side:THREE.DoubleSide});
  water.rotation.x=-Math.PI/2;water.position.y=this.level;water.material.transparent=true;water.material.depthWrite=false;
  water.material.uniforms.size.value=3;water.name='WATER_RUNTIME';return water;
 }
 update(time:number){this.mesh.material.uniforms.time.value=time*.23;}
 dispose(){this.normal.dispose();this.base.dispose();this.mesh.material.dispose();}
}
