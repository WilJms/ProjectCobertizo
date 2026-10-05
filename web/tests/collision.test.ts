import {test} from 'node:test';
import assert from 'node:assert/strict';
import {CollisionWorld,pointInPolygon} from '../src/collision.ts';
const config={bounds:[.2,.2,10.3,10.3] as [number,number,number,number],pool:[[6,3],[9,3],[9,8],[6,8]],deck:[[.2,.2],[5,.2],[5,2],[3,2],[3,5],[.2,5]],deckHeight:.22,eyeHeight:1.65,radius:.2,commonCollisions:[{id:'table',type:'box' as const,min:[1,1] as [number,number],max:[2,2] as [number,number]}]};
test('pool interior and edge clearance are impassable',()=>{const w=new CollisionWorld(config);w.setVariant([]);assert.equal(w.valid(7,4),false);assert.equal(w.valid(5.9,4),false);assert.equal(w.valid(5.6,4),true);});
test('fast movement cannot tunnel through pool or fence',()=>{const w=new CollisionWorld(config);w.setVariant([]);const [x,y]=w.move(5,5,5,0);assert(x<5.8);assert(w.valid(x,y));const p=w.move(.4,6,-5,0);assert(p[0]>=.2);});
test('changing variant retains valid pose and finds nearby free pose for a new post',()=>{const w=new CollisionWorld(config);w.setVariant([]);assert.deepEqual(w.nearest(4,3),[4,3]);w.setVariant([{id:'post',type:'circle',x:4,y:3,radius:.12}]);const [x,y]=w.nearest(4,3);assert(w.valid(x,y));assert(Math.hypot(x-4,y-3)<.4);});
test('box clearance and sliding along a face',()=>{const w=new CollisionWorld(config);w.setVariant([]);assert.equal(w.valid(2.1,1.4),false);const [x,y]=w.move(2.4,1.3,-1,1.5);assert(w.valid(x,y));assert(y>2);});
test('deck elevation is continuous in the L footprint and absent from lawn',()=>{const w=new CollisionWorld(config);assert.equal(w.height(1,4),.22);assert.equal(w.height(4,1),.22);assert.equal(w.height(4,4),0);assert.equal(pointInPolygon(7,7,config.deck),false);});
