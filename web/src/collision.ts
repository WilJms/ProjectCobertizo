import type {Collision,Manifest} from './types';
export function pointInPolygon(x:number,y:number,points:number[][]){
 let inside=false;for(let i=0,j=points.length-1;i<points.length;j=i++){
 const [xi,yi]=points[i],[xj,yj]=points[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)inside=!inside;
 }return inside;
}
export function segmentDistance(x:number,y:number,a:number[],b:number[]){
 const dx=b[0]-a[0],dy=b[1]-a[1];const t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy||1)));return Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);
}
export class CollisionWorld {
 obstacles:Collision[]=[];
 config:Manifest['navigation'];
 constructor(config:Manifest['navigation']){this.config=config;}
 setVariant(collisions:Collision[]){this.obstacles=[...this.config.commonCollisions,...collisions];}
 valid(x:number,y:number){
 const {bounds:b,radius:r,pool}=this.config;
 if(x<b[0]||y<b[1]||x>b[2]||y>b[3])return false;
 if(pointInPolygon(x,y,pool)||pool.some((a,i)=>segmentDistance(x,y,a,pool[(i+1)%pool.length])<r+.04))return false;
 for(const c of this.obstacles){
  if(c.type==='circle'&&Math.hypot(c.x-x,c.y-y)<c.radius+r)return false;
  if(c.type==='box'){const cx=Math.max(c.min[0],Math.min(x,c.max[0])),cy=Math.max(c.min[1],Math.min(y,c.max[1]));if(Math.hypot(x-cx,y-cy)<r)return false;}
 }return true;
 }
 nearest(x:number,y:number):[number,number]{
 if(this.valid(x,y))return [x,y];
 for(let r=.04;r<15;r+=.04){const n=Math.ceil(2*Math.PI*r/.04);for(let i=0;i<n;i++){const a=i/n*Math.PI*2,nx=x+Math.cos(a)*r,ny=y+Math.sin(a)*r;if(this.valid(nx,ny))return[nx,ny];}}
 throw new Error('No se encontró una posición transitable');
 }
 move(x:number,y:number,dx:number,dy:number):[number,number]{
 const steps=Math.max(1,Math.ceil(Math.hypot(dx,dy)/.07));
 for(let i=0;i<steps;i++){const nx=x+dx/steps,ny=y+dy/steps;if(this.valid(nx,ny)){x=nx;y=ny;}else{if(this.valid(nx,y))x=nx;if(this.valid(x,ny))y=ny;}}
 return[x,y];
 }
 height(x:number,y:number){return pointInPolygon(x,y,this.config.deck)?this.config.deckHeight:0;}
}
