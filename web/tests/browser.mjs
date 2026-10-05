// Reproducible browser QA; IAB is also inspected visually through the app's browser tools.
import {chromium} from '@playwright/test';
import {writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
const origin=process.env.TEST_URL||'http://127.0.0.1:5173/ProjectCobertizo/';
const out='../outputs/browser';await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chromium'});
const context=await browser.newContext({viewport:{width:1200,height:800},deviceScaleFactor:1});
const page=await context.newPage();const errors=[],warnings=[],failures=[];
page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());if(m.type()==='warning')warnings.push(m.text());});page.on('response',r=>{if(r.status()>=400)failures.push({url:r.url(),status:r.status()});});
const waitState=async(d,t,q)=>page.waitForFunction(({d,t,q})=>{const s=window.__patio?.scene;return !!s?.active&&s.active.state.designId===d&&s.active.state.timeId===t&&(!q||s.active.quality===q)&&document.getElementById('loading').hidden;},{d,t,q},{timeout:90000});
await page.goto(origin+'?quality=high');await page.waitForFunction(()=>window.__patio?.ready,undefined,{timeout:90000});
assert.equal(await page.title(),'Patio · Tres cobertizos');assert(await page.getByRole('heading',{name:'Patio',exact:true}).isVisible());assert.equal(await page.locator('vite-error-overlay').count(),0);
const designs=await page.evaluate(()=>window.__patio.manifest.designs.map(d=>d.id));
const report={origin,spatialRevision:await page.evaluate(()=>window.__patio.manifest.spatialRevision),sourceSha256:await page.evaluate(()=>window.__patio.manifest.sourceSha256),browser:await browser.version(),viewports:[],checks:[],states:[],comparisons:[],metrics:[],errors,warnings,failures};
console.log('Renderer:',await page.evaluate(()=>window.__patio.scene.diagnostics().renderer));
report.initialTransfer=await page.evaluate(()=>{const resources=performance.getEntriesByType('resource').filter(r=>r.name.includes('/assets/'));return {transferBytes:resources.reduce((n,r)=>n+r.transferSize,0),decodedBodyBytes:resources.reduce((n,r)=>n+r.decodedBodySize,0),resources:resources.length};});
report.checks.push({name:'Identity, meaningful DOM, no framework error overlay',pass:true});
const selectDesign=async(d)=>{await page.locator('#design-toggle').click();await page.locator(`[data-design="${d}"]`).click();};
await page.screenshot({path:out+'/desktop-ui.png'});
for(const d of designs){for(const t of ['day','night']){
 await selectDesign(d);await page.locator(`button[data-time="${t}"]`).click();await waitState(d,t,'high');
 const position=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());
 await page.screenshot({path:out+`/${d}__${t}__ui.png`});
 report.states.push({design:d,time:t,position,...await page.evaluate(()=>window.__patio.scene.diagnostics())});console.log('State checked:',d,t);
}}
// Screenshot comparison uses an independently opened exact-aspect frozen camera, no post-capture edits.
const capture=await context.newPage();
for(const d of designs){for(const t of ['day','night']){
 await capture.goto(origin+`?capture=1&quality=high&design=${d}&time=${t}`);await capture.waitForFunction(()=>window.__patio?.ready,undefined,{timeout:90000});await capture.waitForTimeout(150);
 await capture.screenshot({path:out+`/${d}__${t}__CAM01_GENERAL.png`});
 const comparison=await capture.evaluate(()=>{const s=window.__patio.scene,p=window.__patio.manifest.cameras[0];return {state:s.active.key,cameraId:p.id,position:s.camera.position.toArray(),expectedPosition:p.position,verticalFov:s.camera.fov,expectedVerticalFov:p.verticalFov,aspect:s.camera.aspect,width:innerWidth,height:innerHeight,waterTime:s.water.mesh.material.uniforms.time.value,exposure:s.renderer.toneMappingExposure};});
 assert(comparison.position.every((v,i)=>Math.abs(v-comparison.expectedPosition[i])<1e-6));assert.equal(comparison.verticalFov,comparison.expectedVerticalFov);assert.equal(comparison.aspect,1.5);assert.equal(comparison.waterTime,0);report.comparisons.push(comparison);
}}
await capture.close();
// Saved views including all three roof undersides and both water states.
for(const d of designs){await selectDesign(d);await waitState(d,'night');await page.getByLabel('Vista guardada').selectOption('CAM04_BAJO_CUBIERTA');await page.screenshot({path:out+`/${d}__roof.png`});}
await page.getByLabel('Vista guardada').selectOption('CAM05_PISCINA');await page.screenshot({path:out+'/water-night.png'});await page.locator('button[data-time="day"]').click();await waitState(designs[2],'day');await page.screenshot({path:out+'/water-day.png'});
// Real keyboard and mouse events: movement and free look are separately checked.
await page.getByRole('button',{name:'Reiniciar recorrido',exact:true}).click();
let before=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());await page.locator('canvas').click({position:{x:750,y:500}});await page.keyboard.down('KeyW');await page.waitForTimeout(850);await page.keyboard.up('KeyW');let after=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());assert(Math.hypot(after[0]-before[0],after[2]-before[2])>.5);
const yaw=await page.evaluate(()=>window.__patio.navigation.yaw);await page.mouse.move(800,420);await page.mouse.down();await page.mouse.move(920,465,{steps:10});await page.mouse.up();assert(Math.abs(await page.evaluate(()=>window.__patio.navigation.yaw)-yaw)>.1);
report.checks.push({name:'WASD movement and pointer-drag free look',pass:true,before,after});
// Camera does not move on a valid variant/time change.
before=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());await selectDesign(designs[1]);await waitState(designs[1],'day');after=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());assert(Math.hypot(after[0]-before[0],after[2]-before[2])<.001);
report.checks.push({name:'Valid camera preserved across design change',pass:true});
// Nearest-valid-position handles a visitor at an incoming support, using the authored controller.
const relocation=await page.evaluate(()=>{const n=window.__patio.navigation;const post=window.__patio.scene.active.state.collisions[0];n.camera.position.set(post.x,1.87,post.y);const moved=n.reconcile();return {moved,valid:n.world.valid(n.camera.position.x,n.camera.position.z),position:n.camera.position.toArray()};});assert(relocation.moved&&relocation.valid);report.checks.push({name:'Post overlap resolved nearby',pass:true,...relocation});
await page.getByRole('button',{name:'Reiniciar recorrido',exact:true}).click();
// Rapid requests must leave one coherent final state.
await page.evaluate(ds=>{for(let i=0;i<9;i++)window.__patio.request(ds[i%3],i%2?'day':'night');window.__patio.request(ds[2],'night');},designs);await waitState(designs[2],'night');report.checks.push({name:'Rapid requests commit only the final requested state',pass:true});
// A deliberately failed uncached map must preserve the old root; retry recovers.
const activeBeforeError=await page.evaluate(()=>window.__patio.scene.active.key);
await page.route('**/*--low.exr',route=>route.abort('failed'));
await page.getByLabel('Calidad de imagen').selectOption('low');await page.getByRole('button',{name:'Reintentar',exact:true}).waitFor({state:'visible',timeout:90000});assert.equal(await page.evaluate(()=>window.__patio.scene.active.key),activeBeforeError);
await page.unroute('**/*--low.exr');await page.getByRole('button',{name:'Reintentar',exact:true}).click();await waitState(designs[2],'night','low');report.checks.push({name:'Download failure preserves old scene; retry recovers',pass:true});
// Measured at a fixed view after load/compilation, with Cycles jobs stopped by the caller.
for(const q of ['high','balanced','low']){
 await page.getByLabel('Calidad de imagen').selectOption(q);await waitState(designs[2],'night',q);await page.waitForTimeout(6500);
 report.metrics.push(await page.evaluate(()=>window.__patioDiagnostics));
}
await page.getByLabel('Calidad de imagen').selectOption('high');await waitState(designs[2],'night','high');
const memory=[];
for(let i=0;i<9;i++){const d=designs[i%3],t=i%2?'day':'night';await page.evaluate(({d,t})=>window.__patio.request(d,t),{d,t});await waitState(d,t);memory.push(await page.evaluate(()=>window.__patio.scene.diagnostics()));}
assert(memory.every(m=>m.cachedStates<=2));report.memory=memory;report.checks.push({name:'At most two state lightmap sets retained',pass:true});
// UI touch emulation, explicitly not a physical-phone performance result.
const mobile=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,hasTouch:true,isMobile:true});const phone=await mobile.newPage();
await phone.goto(origin+'?quality=balanced');await phone.waitForFunction(()=>window.__patio?.ready,undefined,{timeout:90000});
await phone.locator('button[data-time="night"]').tap();await phone.waitForFunction(()=>window.__patio?.scene.active.state.timeId==='night');
await phone.getByRole('button',{name:'Caminar',exact:true}).tap();assert(await phone.getByLabel('Control táctil de movimiento').isVisible());assert(await phone.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
const start=await phone.evaluate(()=>window.__patio.scene.camera.position.toArray());
const joystick=phone.getByLabel('Control táctil de movimiento');const bounds=await joystick.boundingBox();
const cdp=await mobile.newCDPSession(phone);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:bounds.x+50,y:bounds.y+20}]});await phone.waitForTimeout(600);await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
const end=await phone.evaluate(()=>window.__patio.scene.camera.position.toArray());assert(Math.hypot(end[0]-start[0],end[2]-start[2])>.25);
await phone.screenshot({path:out+'/mobile-390x844.png'});report.viewports.push({width:390,height:844,type:'touch emulation on Mac, not physical phone',movement:{start,end}});
await phone.setViewportSize({width:844,height:390});
const touchLayout=await phone.evaluate(()=>{const a=document.getElementById('joystick').getBoundingClientRect(),b=document.querySelector('.design-panel').getBoundingClientRect();return {overlap:a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top};});assert(!touchLayout.overlap);report.checks.push({name:'Landscape joystick does not overlap design choices',pass:true});await phone.screenshot({path:out+'/mobile-landscape.png'});report.viewports.push({width:844,height:390,type:'landscape emulation'});
await mobile.close();
// Retina desktop rendering uses the real host GPU at the specified DPR; it is not a phone test.
await page.goto(origin+'?fallback=1');
const retina=await browser.newContext({viewport:{width:1200,height:800},deviceScaleFactor:2});const perf=await retina.newPage();
await perf.goto(origin+'?quality=high');await perf.waitForFunction(()=>window.__patio?.ready,undefined,{timeout:90000});
report.retinaMetrics=[];
for(const q of ['high','balanced','low']){
 await perf.getByLabel('Calidad de imagen').selectOption(q);await perf.waitForFunction(q=>window.__patio?.scene.active.quality===q,q,{timeout:90000});await perf.waitForTimeout(6500);
 report.retinaMetrics.push(await perf.evaluate(()=>window.__patioDiagnostics));
}
await retina.close();
const fb=await context.newPage();await fb.goto(origin+'?fallback=1');await fb.getByText('Modo imágenes',{exact:true}).waitFor();await fb.locator('button[data-time="night"]').click();assert((await fb.locator('#fallback-image').getAttribute('src')).includes('__night.jpg'));await fb.screenshot({path:out+'/fallback-renders.png'});await fb.close();report.checks.push({name:'Fallback explicitly offers renders instead of navigation',pass:true});
report.viewports.push({width:1200,height:800,type:'desktop Chromium on physical Mac host'});
report.expectedNetworkErrors='Deliberate abort of --low.exr during error recovery test; no HTTP error is expected otherwise.';
await writeFile('../outputs/validation/browser-report.json',JSON.stringify(report,null,2));await browser.close();
assert.equal(failures.length,0,'unexpected HTTP failures');const unexpectedErrors=errors.filter(e=>!e.includes('net::ERR_FAILED'));assert.equal(unexpectedErrors.length,0,unexpectedErrors.join('\n'));
console.log(JSON.stringify({checks:report.checks,metrics:report.metrics,errors:unexpectedErrors,networkFailures:failures},null,2));
