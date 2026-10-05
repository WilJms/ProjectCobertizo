import './style.css';
import {PatioScene} from './scene';
import {CollisionWorld} from './collision';
import {Navigation} from './navigation';
import {assetUrl} from './lighting';
import type {Manifest,Quality,TimeId} from './types';
const app=document.querySelector<HTMLDivElement>('#app')!;
const icon=(kind:string)=>`<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${({sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4L19 5"/>',moon:'<path d="M20.7 13A9 9 0 0 1 11 3.3 9 9 0 1 0 20.7 13Z"/>',walk:'<circle cx="14" cy="4" r="2"/><path d="m7 12 3-4 4 1 3 4h3M12 9l-2 7-4 5m4-5 5 1 1 4"/>',reset:'<path d="M3 10a9 9 0 1 1 2 8M3 4v6h6"/>',help:'<circle cx="12" cy="12" r="9"/><path d="M9.5 8.5a2.6 2.6 0 0 1 5 1c0 2-2.5 2-2.5 4m0 3h.01"/>',close:'<path d="m6 6 12 12M6 18 18 6"/>'} as Record<string,string>)[kind]||''}</svg>`;
app.innerHTML=`<main id="viewer" aria-label="Recorrido tridimensional del patio"><canvas id="scene" tabindex="0" aria-label="Patio 3D. Arrastra para mirar y usa W A S D para caminar."></canvas><img id="fallback-image" alt="Render Cycles del patio" hidden>
<header><div class="brand"><h1>Patio</h1><span>Tres propuestas de cobertizo</span></div><div class="time-controls" role="group" aria-label="Momento del día"><button data-time="day" aria-pressed="true">${icon('sun')}<span>Día</span></button><button data-time="night" aria-pressed="false">${icon('moon')}<span>Noche</span></button></div></header>
<section class="design-panel" data-open="false" aria-label="Propuesta de cobertizo"><button id="design-toggle" aria-expanded="false" aria-controls="designs"><span id="design-summary">Madera · 1/3</span><span aria-hidden="true">⌄</span></button><div class="panel-heading">Elige una propuesta <span id="state-number">01 / 03</span></div><div id="designs"></div></section>
<div id="tools-menu" class="top-tools" data-open="false"><button id="tools-toggle" aria-label="Opciones de imagen y ayuda" aria-expanded="false" aria-controls="tools-content">···</button><div class="tools-content" id="tools-content"><label class="select-control">Calidad <select id="quality" aria-label="Calidad de imagen"><option value="auto">Automática</option><option value="high">Alta</option><option value="balanced">Equilibrada</option><option value="low">Ligera</option></select></label><button id="help" class="icon-button" aria-label="Ver controles">${icon('help')}</button></div></div>
<div class="bottom-controls"><div class="view-control"><label for="camera">Vista</label><select id="camera" aria-label="Vista guardada"><option value="CAM01_GENERAL">General</option><option value="CAM02_MURO_AZUL">Muro azul</option><option value="CAM03_CERCO">Cerco</option><option value="CAM04_BAJO_CUBIERTA">Bajo cubierta</option><option value="CAM05_PISCINA">Piscina</option></select></div><button id="reset" class="icon-button" aria-label="Reiniciar recorrido">${icon('reset')}</button><button id="walk" aria-pressed="false">${icon('walk')}<span>Caminar</span></button></div>
<div id="joystick" aria-label="Control táctil de movimiento"><span class="joystick-knob"></span></div><div class="touch-look">Mueve la palanca · Arrastra para mirar</div>
<footer><span id="hint">Arrastra para mirar · W A S D para caminar</span><span id="quality-note">Escala estimada</span></footer>
<div id="loading" role="status"><span class="spinner"></span><span id="loading-text">Preparando el patio…</span><button id="retry" hidden>Reintentar</button></div><p id="toast" role="status" hidden></p>
<dialog id="help-dialog"><button class="close icon-button" aria-label="Cerrar controles">${icon('close')}</button><h2>Recorre el patio</h2><p>Arrastra sobre la escena para mirar alrededor. Puedes caminar por el césped, el pavimento y el deck.</p><dl><dt>W A S D</dt><dd>Avanzar, retroceder y moverte a los lados</dd><dt>Flechas</dt><dd>Avanzar y girar</dd><dt>Shift</dt><dd>Caminar más rápido</dd><dt>Esc</dt><dd>Soltar el ratón en modo Caminar</dd><dt>Pantalla táctil</dt><dd>Pulsa Caminar para mostrar la palanca izquierda. Arrastra la escena para mirar y pulsa Salir para terminar.</dd></dl><p class="muted">Las dimensiones son estimadas a partir de las referencias. La noche simula la iluminación propuesta. Las vistas guardadas complementan el recorrido libre.</p><button id="metrics-toggle">Mostrar rendimiento</button><pre id="metrics" hidden></pre></dialog>
<div id="fallback-note" hidden><strong>Modo imágenes</strong><p>Este navegador no pudo iniciar el recorrido 3D. Puedes comparar los renders de las seis propuestas y momentos del día.</p></div>
</main>`;
const $=<T extends HTMLElement=HTMLElement>(id:string)=>document.getElementById(id) as T;
let manifest:Manifest;let patio:PatioScene|undefined;let nav:Navigation|undefined;
let design='d1_madera_dos_aguas',time:TimeId='day',quality:Quality='high',automatic=true,fallback=false,initial=true;
let frames:number[]=[],last=performance.now(),clockTime=0,measureAt=last,adjustAt=last,frameCount=0,loadStart=last,qualityCooldown=0;
const query=new URLSearchParams(location.search),frozen=query.has('capture');let ready=false;
let toastTimer:number;
let touchInput=matchMedia('(any-pointer: coarse)').matches||navigator.maxTouchPoints>0,walking=false;
const toolsMenu=$('tools-menu');
function setToolsOpen(value:boolean){toolsMenu.dataset.open=String(value);$('tools-toggle').setAttribute('aria-expanded',String(value));pauseForMenus();}
function syncInput(){
 document.documentElement.dataset.input=touchInput?'touch':'mouse';document.documentElement.dataset.walking=String(walking);
 $('walk').setAttribute('aria-pressed',String(walking));$('walk').querySelector('span')!.textContent=walking?'Salir':'Caminar';
 $('hint').textContent=touchInput?(walking?'Palanca para caminar · Arrastra para mirar':'Arrastra para mirar · Caminar activa la palanca'):(document.pointerLockElement?'W A S D para caminar · Esc para salir':'Arrastra para mirar · W A S D para caminar');
 $('scene').setAttribute('aria-label',touchInput?'Patio 3D. Arrastra para mirar. Pulsa Caminar para usar la palanca.':'Patio 3D. Arrastra para mirar y usa W A S D para caminar.');
}
function pauseForMenus(){const open=$('design-toggle').getAttribute('aria-expanded')==='true'||toolsMenu.dataset.open==='true'||$<HTMLDialogElement>('help-dialog').open;document.documentElement.dataset.menuOpen=String(open);nav?.setPaused(open);}
function closeDesign(){document.querySelector<HTMLElement>('.design-panel')!.dataset.open='false';$('design-toggle').setAttribute('aria-expanded','false');pauseForMenus();}
$('design-toggle').addEventListener('click',()=>{const open=$('design-toggle').getAttribute('aria-expanded')!=='true';setToolsOpen(false);document.querySelector<HTMLElement>('.design-panel')!.dataset.open=String(open);$('design-toggle').setAttribute('aria-expanded',String(open));pauseForMenus();});
$('tools-toggle').addEventListener('click',()=>{const open=toolsMenu.dataset.open!=='true';closeDesign();setToolsOpen(open);});
document.addEventListener('pointerdown',e=>{if(e.pointerType==='touch'&&!touchInput){touchInput=true;syncInput();}else if(e.pointerType==='mouse'&&touchInput&&!walking){touchInput=false;syncInput();}
 const target=e.target as Element;if(!target.closest('.design-panel'))closeDesign();if(!target.closest('.top-tools'))setToolsOpen(false);
});
document.addEventListener('keydown',e=>{if(e.code==='Escape'){closeDesign();setToolsOpen(false);if(walking){walking=false;nav?.stop();syncInput();}}});
syncInput();
function toast(message:string){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=window.setTimeout(()=>$('toast').hidden=true,3500);}
function setStatus(message:string,error=false){$('loading').hidden=!message;$('loading-text').textContent=message;$<HTMLButtonElement>('retry').hidden=!error;$('loading').classList.toggle('error',error);if(error&&!patio?.active)enableFallback();}
function updateSelection(){
 document.querySelectorAll<HTMLButtonElement>('[data-design]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.design===design)));
 document.querySelectorAll<HTMLButtonElement>('button[data-time]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.time===time)));
 const index=manifest.designs.findIndex(d=>d.id===design);$('state-number').textContent=`0${index+1} / 03`;$('design-summary').textContent=`${['Madera','Oscuro · Madera','Oscuro · Claro'][index]} · ${index+1}/3`;
 document.documentElement.dataset.time=time;
}
function requestState(){if(fallback){$<HTMLImageElement>('fallback-image').src=assetUrl(manifest.states[design+'__'+time].render);updateSelection();return;}patio?.request(design+'__'+time,quality);}
function enableFallback(){fallback=true;$('scene').hidden=true;$('fallback-image').hidden=false;$('fallback-note').hidden=false;$('loading').hidden=true;$('walk').hidden=true;$('joystick').hidden=true;document.documentElement.classList.add('fallback');if(manifest)requestState();else $<HTMLImageElement>('fallback-image').src=assetUrl('assets/renders/d1_madera_dos_aguas__day.jpg');ready=true;}
let resizeFrame=0;
function resize(){cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{
 document.documentElement.style.setProperty('--viewport-height',`${window.visualViewport?.height??innerHeight}px`);
 const rect=$('viewer').getBoundingClientRect();if(rect.width&&rect.height)patio?.resize(rect.width,rect.height,patio.active?.quality??quality);
 nav?.stop();
});}
function updateQualityNote(){const shown=patio?.active?.quality??quality;$('quality-note').textContent=`${({high:'Alta',balanced:'Equilibrada',low:'Ligera'})[shown]}${automatic?' · Auto':''} · Escala estimada`;}
function changeQuality(next:Quality){if(next===quality)return;quality=next;frames=[];qualityCooldown=performance.now()+12000;requestState();}
try{
 const response=await fetch(assetUrl('assets/scene-manifest.json'));if(!response.ok)throw Error('No se encontró el manifiesto');manifest=await response.json();
 if(manifest.schemaVersion!=='1.0'||Object.keys(manifest.states).length!==6)throw Error('Manifiesto no compatible');
 $('designs').innerHTML=manifest.designs.map((d,i)=>`<button class="design-option" data-design="${d.id}" aria-pressed="${i===0}"><span class="design-index">0${i+1}</span><span><strong>${d.label.split(' · ')[0]}</strong><small>${d.label.split(' · ')[1]}</small></span><span class="selection-mark" aria-hidden="true"></span></button>`).join('');
 if(query.has('design')&&manifest.designs.some(d=>d.id===query.get('design')))design=query.get('design')!;
 if(query.get('time')==='night')time='night';
 if(['high','balanced','low'].includes(query.get('quality')||'')){quality=query.get('quality') as Quality;automatic=false;$<HTMLSelectElement>('quality').value=quality;}
 document.querySelectorAll<HTMLButtonElement>('[data-design]').forEach(b=>b.addEventListener('click',()=>{design=b.dataset.design!;closeDesign();requestState();}));
 document.querySelectorAll<HTMLButtonElement>('button[data-time]').forEach(b=>b.addEventListener('click',()=>{time=b.dataset.time as TimeId;closeDesign();requestState();}));
 if(query.has('fallback'))enableFallback();else{
  patio=new PatioScene(manifest,$<HTMLCanvasElement>('scene'));const world=new CollisionWorld(manifest.navigation);nav=new Navigation(patio.camera,world,$('scene'));nav.attachJoystick($('joystick'));
  patio.onStatus=setStatus;
  patio.onState=(state,activeQuality)=>{design=state.designId;time=state.timeId;quality=activeQuality;world.setVariant(state.collisions);
   if(initial){loadStart=performance.now()-loadStart;const pose=manifest.cameras.find(c=>c.id===(query.get('camera')||'CAM01_GENERAL'))!;nav!.pose(pose||manifest.cameras[0]);initial=false;$<HTMLSelectElement>('camera').value=pose?.id||'CAM01_GENERAL';}
   else if(nav!.reconcile())toast('Te hemos movido un poco para evitar un poste.');
   ready=true;updateSelection();resize();updateQualityNote();
  };
  requestState();window.addEventListener('resize',resize);window.visualViewport?.addEventListener('resize',resize);new ResizeObserver(resize).observe($('viewer'));resize();
  const canvas=$<HTMLCanvasElement>('scene');canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();setStatus('Restaurando el contexto 3D…');});canvas.addEventListener('webglcontextrestored',()=>setStatus(''));
  patio.renderer.setAnimationLoop(now=>{
   const raw=now-last,dt=Math.min(raw/1000,.05);last=now;if(document.hidden)return;
   if(!frozen)clockTime+=dt;nav!.update(dt);patio!.render(clockTime,patio!.active?.quality??quality);
   if(ready){frameCount++;frames.push(raw);if(frames.length>300)frames.shift();}
   if(now-measureAt>1000){const sorted=frames.slice().sort((a,b)=>a-b),average=frames.reduce((a,b)=>a+b,0)/Math.max(frames.length,1);const telemetry={...patio!.diagnostics(),fps:Number((1000/average).toFixed(1)),frameMsP50:sorted[Math.floor(sorted.length*.5)]||0,frameMsP95:sorted[Math.floor(sorted.length*.95)]||0,firstReadyMs:Math.round(loadStart),frames:frameCount,physicalDevice:'macOS host; touch viewport emulation is not a phone benchmark'};$('metrics').textContent=JSON.stringify(telemetry,null,2);$('viewer').dataset.ready=String(ready);$('viewer').dataset.state=telemetry.state;
    Object.assign(window,{__patioDiagnostics:telemetry});measureAt=now;
    if(automatic&&now-adjustAt>8000&&now>qualityCooldown&&frames.length>=180){adjustAt=now;if(telemetry.frameMsP50>25&&quality==='high')changeQuality('balanced');else if(telemetry.frameMsP50>38&&quality==='balanced')changeQuality('low');else if(telemetry.frameMsP95<17.7&&quality==='low')changeQuality('balanced');}
   }
  });
 }
}catch(error){console.error(error);enableFallback();}
$('quality').addEventListener('change',()=>{const value=$<HTMLSelectElement>('quality').value;automatic=value==='auto';if(!automatic)changeQuality(value as Quality);else{qualityCooldown=performance.now()+8000;changeQuality('high');}updateQualityNote();});
$('camera').addEventListener('change',()=>{const pose=manifest.cameras.find(c=>c.id===$<HTMLSelectElement>('camera').value);if(pose&&nav){nav.pose(pose);nav.reconcile();}});
$('reset').addEventListener('click',()=>{if(nav){nav.pose(manifest.cameras[0]);nav.reconcile();$<HTMLSelectElement>('camera').value='CAM01_GENERAL';}});
$('walk').addEventListener('click',async()=>{
 closeDesign();setToolsOpen(false);walking=!walking;nav?.stop();syncInput();
 if(!walking){if(document.pointerLockElement)document.exitPointerLock();return;}
 if(!touchInput){try{await $<HTMLCanvasElement>('scene').requestPointerLock();}catch{walking=false;syncInput();toast('Arrastra para mirar y usa W A S D para caminar.');}}
});
document.addEventListener('pointerlockchange',()=>{if(!touchInput)walking=!!document.pointerLockElement;nav?.stop();syncInput();});
$('help').addEventListener('click',()=>{setToolsOpen(false);closeDesign();$<HTMLDialogElement>('help-dialog').showModal();pauseForMenus();});
document.querySelector('#help-dialog .close')!.addEventListener('click',()=>$<HTMLDialogElement>('help-dialog').close());$('help-dialog').addEventListener('close',pauseForMenus);
$('metrics-toggle').addEventListener('click',()=>{$('metrics').hidden=!$('metrics').hidden;});
$('retry').addEventListener('click',()=>requestState());
// Test hooks expose authored navigation and state APIs, not alternate geometry or simulated pass results.
Object.assign(window,{__patio:{get ready(){return ready;},get manifest(){return manifest;},get navigation(){return nav;},get scene(){return patio;},request:(d:string,t:TimeId)=>{design=d;time=t;requestState();}}});
if(query.has('capture'))document.documentElement.classList.add('capture');
