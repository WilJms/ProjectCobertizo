import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
const base='http://127.0.0.1:4173/ProjectCobertizo/';
const browser=await chromium.launch({headless:true,channel:'chromium'});const page=await browser.newPage({viewport:{width:1200,height:800}});
const failures=[],errors=[],urls=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failures.push({url:r.url(),status:r.status()});urls.push(r.url());});
await page.goto(base+'?quality=balanced');await page.waitForFunction(()=>window.__patio?.ready,undefined,{timeout:90000});
const manifest=await page.evaluate(()=>window.__patio.manifest);
assert.equal(manifest.spatialRevision,'2026-10-04-detail-corrections-v3');assert(manifest.navigation.bounds[2]<7.5);
for(const d of manifest.designs){for(const t of ['day','night']){
 await page.evaluate(({d,t})=>window.__patio.request(d,t),{d:d.id,t});
 await page.waitForFunction(({d,t})=>window.__patio.scene.active.state.designId===d&&window.__patio.scene.active.state.timeId===t&&document.getElementById('loading').hidden,{d:d.id,t},{timeout:90000});
}}
await page.getByLabel('Vista guardada').selectOption('CAM05_PISCINA');await page.screenshot({path:'../outputs/browser/production-prefixed.png'});
const initial=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());await page.locator('canvas').click({position:{x:800,y:300}});await page.keyboard.down('KeyA');await page.waitForTimeout(350);await page.keyboard.up('KeyA');
const after=await page.evaluate(()=>window.__patio.scene.camera.position.toArray());assert(Math.hypot(after[0]-initial[0],after[2]-initial[2])>.1);
assert.equal(failures.length,0);assert.equal(errors.length,0);const httpUrls=urls.filter(u=>/^https?:/.test(u));const inMemory=urls.filter(u=>!/^https?:/.test(u));assert(inMemory.every(u=>u.startsWith('blob:')||u.startsWith('data:')));assert(httpUrls.every(u=>u.startsWith(base)),JSON.stringify(httpUrls.filter(u=>!u.startsWith(base))));
await writeFile('../outputs/validation/production-report.json',JSON.stringify({base,spatialRevision:manifest.spatialRevision,sourceSha256:manifest.sourceSha256,statesChecked:6,prefixChecked:true,movement:{initial,after},errors,failures,resources:urls.length,httpResources:httpUrls.length,inMemoryResources:inMemory.length,inMemoryNote:'Embedded GLB textures use blob/data URLs and are not remote path requests'},null,2));await browser.close();console.log('Production prefix, six states, keyboard movement and resource requests passed.');
