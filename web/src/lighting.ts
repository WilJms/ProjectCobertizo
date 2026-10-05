import * as THREE from 'three';
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';
export const assetUrl = (path: string) => import.meta.env.BASE_URL + path;
const exrLoader = new EXRLoader().setDataType(THREE.HalfFloatType);
/** Cycles DIFFUSE without COLOR = outgoing diffuse for unit albedo, i.e. E / π.
 * Preserve all view-dependent specular; replace every diffuse contribution.
 * No runtime diffuse, AO, hemisphere, or second environment diffuse is added.
 */
export function bakedMaterial(source: THREE.MeshStandardMaterial, map: THREE.Texture) {
  const mat = source.clone();
  mat.lightMap = map; mat.lightMapIntensity = Math.PI;
  mat.aoMap = null;
  mat.onBeforeCompile = shader => {
    shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_end>', `
      #include <lights_fragment_end>
      #ifdef USE_LIGHTMAP
        reflectedLight.directDiffuse = vec3(0.0);
        reflectedLight.indirectDiffuse = texture2D(lightMap, vLightMapUv).rgb * diffuseColor.rgb * (1.0 - metalnessFactor);
      #endif
    `);
  };
  mat.customProgramCacheKey = () => 'cycles-static-diffuse-v1';
  return mat;
}
export async function loadLightmap(path: string) {
 const map=await exrLoader.loadAsync(assetUrl(path));
 map.colorSpace=THREE.LinearSRGBColorSpace;map.channel=1;map.flipY=true;
 map.minFilter=THREE.LinearFilter;map.magFilter=THREE.LinearFilter;map.generateMipmaps=false;
 return map;
}
export async function loadEnvironment(path:string, renderer:THREE.WebGLRenderer) {
 const tex=await new THREE.TextureLoader().loadAsync(assetUrl(path));tex.colorSpace=THREE.SRGBColorSpace;tex.mapping=THREE.EquirectangularReflectionMapping;
 const pmrem=new THREE.PMREMGenerator(renderer);const rt=pmrem.fromEquirectangular(tex);pmrem.dispose();
 return {background:tex,reflection:rt.texture,dispose:()=>{rt.dispose();tex.dispose();}};
}
