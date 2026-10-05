// Regression checks for the user's 2026-10-04 geometry, temporal and phone report.
import {chromium} from '@playwright/test';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='../outputs/revision-2026-10-04';await mkdir(out,{recursive:true});
const interfaceOnly=process.argv.includes('--interface-only');
const config=JSON.parse(await readFile('../config/scene-parameters.json','utf8'));
const url=process.env.TEST_URL||'http://127.0.0.1:5173/ProjectCobertizo/';
const browser=await chromium.launch({headless:true,channel:'chromium'});
const errors=[],report={date:'2026-10-04',spatialRevision:config.spatial_revision,physicalHost:'Apple M2 macOS; no physical phone available',checks:[],temporal:[],viewports:[],errors};
const ready=async p=>p.waitForFunction(()=>window.__patio?.ready&&document.getElementById('loading').hidden,undefined,{timeout:90000});
const state=async(p,d,t,q)=>p.waitForFunction(({d,t,q})=>{const a=window.__patio.scene.active;return a.state.designId===d&&a.state.timeId===t&&(!q||a.quality===q)&&document.getElementById('loading').hidden;},{d,t,q},{timeout:90000});
const pose=p=>p.evaluate(()=>{const s=window.__patio.scene;return [...s.camera.position.toArray(),...s.camera.quaternion.toArray()];});
const distance=(a,b)=>Math.max(...a.map((v,i)=>Math.abs(v-b[i])));
const selectDesign=async(p,id,method='click')=>{await p.locator('#design-toggle')[method]();await p.locator(`[data-design="${id}"]`)[method]();};
const qselect=async(p,q)=>{if(!await p.locator('#quality').isVisible())await p.locator('#tools-toggle').click();await p.locator('#quality').selectOption(q);if(await p.locator('#tools-toggle').isVisible()&&await p.locator('#tools-toggle').getAttribute('aria-expanded')==='true')await p.locator('#tools-toggle').click();};
const ds=config.designs.map(d=>d.id);
const page=await browser.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1,...(interfaceOnly?{}:{recordVideo:{dir:out+'/temporal-video',size:{width:1200,height:800}}})});page.on('pageerror',e=>errors.push(e.message));
await page.goto(url+'?quality=high');await ready(page);
assert.equal(await page.evaluate(()=>window.__patio.manifest.spatialRevision),config.spatial_revision);
report.sourceSha256=await page.evaluate(()=>window.__patio.manifest.sourceSha256);
// Each commit contains exactly one common/variant root and two lamp materials.
for(const d of ds)for(const t of ['day','night']){
 await selectDesign(page,d);await page.locator(`button[data-time="${t}"]`).click();await state(page,d,t);
 const info=await page.evaluate(()=>{const s=window.__patio.scene,a=s.active;return {state:a.state.designId+'__'+a.state.timeId,roots:s.scene.children.filter(o=>o===a.root).length,children:s.scene.children.length,lamps:a.mats.filter(m=>m.name==='lamp').map(m=>m.emissiveIntensity),lights:a.state.lights.length,natural:a.state.naturalLight};});
 assert.equal(info.roots,1);assert.equal(info.children,2);assert.equal(info.lamps.length,2);assert(info.lamps.every(v=>v===(t==='day'?0:5)));assert.equal(info.lights,t==='day'?0:35);
 if(t==='day'){assert.equal(info.natural.id,'SUN_DAY');assert.equal(info.natural.type,'sun');assert.equal(info.natural.baked,true);}else assert.equal(info.natural,null);
 assert.equal(await page.locator('#design-toggle').getAttribute('aria-expanded'),'false');
}
report.checks.push({name:'Six coherent states, no duplicated roots/lamps, artificial emission 0/5, baked lamps 0/35 and natural sun day only',pass:true});
// Actual collision model: a visitor can reach the dining perimeter and terminal
// diagonal from the walkway, and cannot cross pool water or walk through furniture.
const paths=await page.evaluate(()=>{const n=window.__patio.navigation,w=n.world,start=[-1,9.8],goals=[[.6,4],[1.1,2.5],[4.7,2.5],[5.0,4.5],[5.1,6.1],[6.2,6.4],[6.85,7.0]],step=.12,b=w.config.bounds;
 const key=(x,y)=>`${x},${y}`,index=p=>[Math.round((p[0]-b[0])/step),Math.round((p[1]-b[1])/step)],world=p=>[b[0]+p[0]*step,b[1]+p[1]*step];let queue=[index(start)],seen=new Set([key(...queue[0])]);
 for(let i=0;i<queue.length;i++){const p=queue[i];for(const d of [[1,0],[-1,0],[0,1],[0,-1]]){const q=[p[0]+d[0],p[1]+d[1]],k=key(...q);if(!seen.has(k)&&w.valid(...world(q))){seen.add(k);queue.push(q);}}}
 return {reachable:goals.map(g=>({goal:g,valid:w.valid(...g),reachable:seen.has(key(...index(g)))})),poolBlocked:!w.valid(5,8.8),tableBlocked:!w.valid(2.9,1.68),visited:seen.size};});
assert(paths.reachable.every(p=>p.valid&&p.reachable),JSON.stringify(paths));assert(paths.poolBlocked&&paths.tableBlocked);report.checks.push({name:'Walkable routes around dining, lounger and pool terminal; water and furniture blocked',pass:true,...paths});
// Temporal observation: real animated scene, not capture=1. Material/state/roots
// are sampled after every rendered frame; pixels at authored diffuser centres
// are read every 250 ms immediately after that same render (no fake draw path).
const probes=config.geometry.deck_riser_faces.filter(f=>f.count).flatMap(f=>[.25,.5,.75].map(t=>[f.start[0]+(f.end[0]-f.start[0])*t+f.normal[0]*.067,.09,f.start[1]+(f.end[1]-f.start[1])*t+f.normal[1]*.067]));
for(const quality of interfaceOnly?[]:['high','auto'])for(const time of ['day','night'])for(const moving of [false,true]){
 await qselect(page,quality);await page.evaluate(({d,t})=>window.__patio.request(d,t),{d:ds[1],t:time});await state(page,ds[1],time);
 await page.locator('#reset').click();await page.waitForTimeout(400);
 const observation=page.evaluate(async({duration,moving,probes})=>{
  const s=window.__patio.scene,n=window.__patio.navigation,original=s.render,started=performance.now();let lastPixels=0,frames=0,invalidPositions=0,maxHorizontalDisplacement=0;const signatures=new Map(),pixels=[];const startPosition=s.camera.position.toArray(),startYaw=n.yaw,startPitch=n.pitch;
  await new Promise(resolve=>{
   s.render=function(...args){
    const age=performance.now()-started;if(moving){n.yaw=startYaw+.10*Math.sin(age/1800);n.pitch=startPitch+.04*Math.sin(age/2200);n.camera.rotation.set(n.pitch,n.yaw,0);}
    original.apply(this,args);frames++;if(!n.world.valid(s.camera.position.x,s.camera.position.z))invalidPositions++;
    maxHorizontalDisplacement=Math.max(maxHorizontalDisplacement,Math.hypot(s.camera.position.x-startPosition[0],s.camera.position.z-startPosition[2]));
    const a=s.active,sig=JSON.stringify({state:a.state.designId+'__'+a.state.timeId,quality:a.quality,lamps:a.mats.filter(m=>m.name==='lamp').map(m=>m.emissiveIntensity),root:a.root.uuid,roots:s.scene.children.length});signatures.set(sig,(signatures.get(sig)||0)+1);
    if(age-lastPixels>=250){lastPixels=age;const gl=s.renderer.getContext(),w=gl.drawingBufferWidth,h=gl.drawingBufferHeight;
     const samples=probes.map(p=>{const v=s.camera.position.clone().fromArray(p).project(s.camera),x=Math.round((v.x+1)*w/2),y=Math.round((v.y+1)*h/2);if(x<4||y<4||x>w-4||y>h-4||Math.abs(v.z)>1)return null;
      const data=new Uint8Array(7*7*4);gl.readPixels(x-3,y-3,7,7,gl.RGBA,gl.UNSIGNED_BYTE,data);let sum=0;for(let i=0;i<data.length;i+=4)sum+=(data[i]+data[i+1]+data[i+2])/3;return sum/49;});pixels.push({age,samples,quality:a.quality});}
    if(age>=duration){s.render=original;resolve();}
   };
  });
  return {durationMs:performance.now()-started,frames,moving,invalidPositions,maxHorizontalDisplacement,signatures:[...signatures].map(([s,count])=>({...JSON.parse(s),frames:count})),pixels,startPosition,endPosition:s.camera.position.toArray(),waterTime:s.water.mesh.material.uniforms.time.value};
 },{duration:18000,moving,probes});
 if(moving){
  await page.locator('canvas').focus();
  for(const [key,ms] of [['KeyW',5500],['KeyD',2000],['KeyS',5500],['KeyA',2000]]){await page.keyboard.down(key);await page.waitForTimeout(ms);await page.keyboard.up(key);}
 }
 const result=await observation;
 assert.equal(result.invalidPositions,0);if(moving)assert(result.maxHorizontalDisplacement>.3);
 assert(result.frames>100);assert(result.waterTime>0);assert(result.signatures.every(s=>s.state===ds[1]+'__'+time&&s.roots===2&&s.lamps.length===2&&s.lamps.every(v=>v===(time==='day'?0:5))));
 if(quality==='high')assert.equal(result.signatures.length,1);
 assert(result.signatures.length<=2,'Unexpected repeated automatic-quality/state changes');
 if(!moving){const groups=new Map();for(const p of result.pixels){if(!groups.has(p.quality))groups.set(p.quality,[]);groups.get(p.quality).push(p.samples);}
  result.stationaryRanges=[...groups].map(([quality,rows])=>({quality,ranges:probes.map((_,i)=>{const v=rows.map(r=>r[i]).filter(v=>v!==null);return v.length?Math.max(...v)-Math.min(...v):null;})}));
  assert(result.stationaryRanges.every(g=>g.ranges.every(v=>v===null||v<=1)),'Static diffuser pixels are unstable');
 }
 await page.screenshot({path:`${out}/temporal-${quality}-${time}-${moving?'moving':'still'}.png`});
 report.temporal.push({quality,time,...result});console.log('Temporal passed',quality,time,moving?'moving':'stationary',result.frames);
 await writeFile(out+'/temporal-in-progress.json',JSON.stringify(report,null,2));
}
if(!interfaceOnly)report.checks.push({name:'Eight 18-second observations: day/night, High/Auto, stationary/moving; frame state and stationary diffuser pixels stable',pass:true});
// Pure mouse in a short landscape window: size compaction cannot depend on coarse input.
await page.setViewportSize({width:844,height:390});await page.waitForTimeout(250);assert(await page.locator('#design-toggle').isVisible());assert(!await page.locator('#designs').isVisible());assert(!await page.locator('#joystick').isVisible());
await page.screenshot({path:out+'/landscape-mouse.png'});report.viewports.push({width:844,height:390,input:'mouse, no touch emulation'});
const recording=page.video();await page.close();if(recording){await recording.saveAs(out+'/temporal-high-auto.webm');await recording.delete();report.temporalRecording='outputs/revision-2026-10-04/temporal-high-auto.webm';}
// Touch portrait -> landscape -> portrait, then mixed touch and mouse input.
const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,deviceScaleFactor:2});const phone=await context.newPage();phone.on('pageerror',e=>errors.push(e.message));
await phone.goto(url+'?quality=balanced');await ready(phone);await phone.getByRole('button',{name:'Caminar',exact:true}).tap();assert(await phone.getByRole('button',{name:'Salir',exact:true}).isVisible());assert(await phone.locator('#joystick').isVisible());
const cdp=await context.newCDPSession(phone),box=await phone.locator('#joystick').boundingBox(),before=await pose(phone);
await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2-28}]});await phone.waitForTimeout(750);await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await phone.waitForTimeout(400);const after=await pose(phone);assert(distance(before,after)>.3);
await phone.getByRole('button',{name:'Salir',exact:true}).tap();assert(!await phone.locator('#joystick').isVisible());assert.deepEqual(await phone.evaluate(()=>window.__patio.navigation.touchMove),{x:0,y:0});
await phone.locator('button[data-time=night]').tap();await state(phone,ds[0],'night');
const stable=await pose(phone);
for(const viewport of [{width:390,height:844},{width:844,height:390},{width:390,height:844}]){
 await phone.setViewportSize(viewport);await phone.waitForTimeout(300);const size=await phone.evaluate(()=>{const s=window.__patio.scene,r=document.getElementById('scene').getBoundingClientRect();return {aspect:s.camera.aspect,canvas:[r.width,r.height],renderer:s.diagnostics().size,state:s.active.state.designId+'__'+s.active.state.timeId,overflow:document.documentElement.scrollWidth>innerWidth};});
 assert(!size.overflow);assert.equal(size.aspect,size.canvas[0]/size.canvas[1]);assert.deepEqual(size.canvas,size.renderer);assert(distance(stable,await pose(phone))<1e-8);assert.equal(size.state,ds[0]+'__night');
 await phone.screenshot({path:`${out}/touch-${viewport.width}x${viewport.height}.png`});report.viewports.push({...viewport,input:'touch emulation; DPR 2',...size});
 await phone.locator('#design-toggle').tap();const menu=await phone.locator('#designs').boundingBox();assert(menu.y>=0&&menu.y+menu.height<=viewport.height);const prev=await pose(phone);await phone.locator(`[data-design="${ds[0]}"]`).tap();assert(distance(prev,await pose(phone))<1e-8);
}
await phone.setViewportSize({width:844,height:390});await phone.waitForTimeout(250);await phone.getByRole('button',{name:'Caminar',exact:true}).tap();
for(let i=0;i<6;i++){const prev=await pose(phone),d=ds[i%3],t=i%2?'day':'night';await selectDesign(phone,d,'tap');await phone.locator(`button[data-time=${t}]`).tap();await state(phone,d,t);assert(distance(prev,await pose(phone))<1e-8);}
await phone.screenshot({path:out+'/touch-landscape-walking.png'});
const p0=await pose(phone);await phone.locator('#design-toggle').tap();await phone.screenshot({path:out+'/touch-landscape-menu.png'});assert.equal(await phone.evaluate(()=>window.__patio.navigation.paused),true);await phone.keyboard.down('KeyW');await phone.waitForTimeout(350);await phone.keyboard.up('KeyW');assert(distance(p0,await pose(phone))<1e-8);await phone.locator(`[data-design="${ds[2]}"]`).tap();
await phone.getByRole('button',{name:'Salir',exact:true}).tap();await phone.mouse.click(720,210);assert.equal(await phone.locator('html').getAttribute('data-input'),'mouse');await phone.locator('#design-toggle').tap();assert.equal(await phone.locator('html').getAttribute('data-input'),'touch');await phone.locator(`[data-design="${ds[2]}"]`).tap();
report.checks.push({name:'Portrait-landscape-portrait preserves camera/state/aspect; compact mouse UI; touch Caminar/Salir; menus block navigation; mixed inputs switch correctly',pass:true});
await context.close();await browser.close();assert.equal(errors.length,0);await writeFile(interfaceOnly?out+'/interface-preview-report.json':'../outputs/validation/revision-report.json',JSON.stringify(report,null,2));console.log(interfaceOnly?'Interface preview QA passed (temporal checks not run)':'Revision QA passed');
