// Browser plugin not installed. Deterministic Playwright capture complements IAB visual inspection.
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:960,height:640},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
const report=[];
for(const time of ['day','night']){
 await page.goto('http://127.0.0.1:5173/ProjectCobertizo/pilot.html?time='+time);await page.waitForFunction(()=>window.__pilot?.ready);
 await page.locator('#status').evaluate(e=>e.style.display='none');await page.screenshot({path:`../outputs/pilot/web-${time}.png`});
 report.push(await page.evaluate(()=>{const p=window.__pilot,r=p.renderer,gl=r.getContext();return {time:new URLSearchParams(location.search).get('time'),meshes:p.meshes,uv1:p.uv1,drawCalls:r.info.render.calls,triangles:r.info.render.triangles,textures:r.info.memory.textures,gpu:gl.getParameter(gl.RENDERER),webgl:gl.getParameter(gl.VERSION)};}));
}
await writeFile('../outputs/pilot/browser-report.json',JSON.stringify({errors,report},null,2));await browser.close();
