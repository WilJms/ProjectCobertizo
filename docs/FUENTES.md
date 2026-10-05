# Fuentes técnicas y decisiones aplicadas

Fuentes primarias revisadas al preparar el paquete, 2026-10-03. Consultar las páginas pertinentes con la versión instalada antes de copiar APIs; esta lista no obliga a releer toda la documentación en cada tarea.

## Contexto aportado por el usuario

Los ocho originales localizados se describen en `REFERENCIAS.md`. El texto adjunto `Texto pegado(5).txt`, de otro modelo, se usó como orientación y se contrastó con documentación oficial. Su contenido útil ya está incorporado; no es una dependencia necesaria de ejecución.

Se conservaron su arquitectura Blender/glTF/Three.js/Vite/Pages, materiales PBR, conversión de procedimientos a texturas, compresión y calibración de color. Se precisaron los aspectos de luz horneada, UV, seis estados, carga por recursos y comprobación temprana. Sus cifras ilustrativas de reducción de peso no se adoptaron como garantía. Usar AgX en ambos motores tampoco se considera garantía de igualdad.

## Fuentes

| ID | Fuente oficial | Uso en este proyecto |
| --- | --- | --- |
| F1 | [OpenAI — Architectural visualization with Astra](https://developers.openai.com/blog/architectural-visualization-with-astra) | Ejemplo de escena Blender mediante `bpy`, revisión de renders e iteración con Astra. No prueba reconstrucción exacta de este patio. |
| F2 | [OpenAI — Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Instrucciones breves, documentación consultada según tarea y definición de finalización. |
| F3 | [Khronos — Documentación del exportador glTF de Blender](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/docs/blender_docs/scene_gltf2.rst) | Mallas, materiales reconocidos, texturas, luces y límites de exportación. |
| F4 | [Blender — Render Baking](https://docs.blender.org/manual/en/5.0/render/cycles/baking.html) | Horneado a texturas y separación de contribuciones. Referencia versionada; verificar interfaz instalada. |
| F5 | [Three.js — MeshStandardMaterial](https://threejs.org/docs/pages/MeshStandardMaterial.html) | PBR, mapas de normales, ambiente y lightmaps. |
| F6 | [Three.js — Texture](https://threejs.org/docs/pages/Texture.html) | Canal UV, espacios de color, filtrado y ciclo de vida. |
| F7 | [Three.js — Color Management](https://threejs.org/manual/pages/color-management.html) | Texturas de color/datos, espacio lineal y salida. |
| F8 | [Three.js — Water](https://threejs.org/docs/pages/Water.html) | Efecto básico reflectante y coste de resolución; punto de partida, no piscina físicamente completa. |
| F9 | [Three.js — GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html) | Extensiones soportadas y conexión de decodificadores. |
| F10 | [Three.js — KTX2Loader](https://threejs.org/docs/pages/KTX2Loader.html) | Transcodificación de texturas Basis a formatos GPU compatibles. |
| F11 | [Three.js — WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html) | Ruta WebGL 2, capacidades, salida y métricas de render. |
| F12 | [Three.js — EffectComposer](https://threejs.org/docs/pages/EffectComposer.html) | Postprocesado cuando sea útil. |
| F13 | [Vite — Deploying a Static Site](https://vite.dev/guide/static-deploy.html) | Build estático, ruta base y publicación en GitHub Pages. |
| F14 | [GitHub — What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | Alojamiento estático y direcciones de sitios de proyecto. |
| F15 | [GitHub — GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | Restricciones del sitio y uso; revisar al publicar. |
| F16 | [GitHub — About large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) | Restricciones de archivos en Git y alternativas para fuentes pesadas. |
| F17 | [GitHub — Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) | Flujo de construcción y despliegue autorizado. |
| F18 | [Khronos — KHR_materials_variants](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_variants/README.md) | Variantes de materiales; no sustituyen las variantes de geometría de este encargo. |

## Alcance de las decisiones propias

Los IDs, fases, organización de archivos, cámaras de inspección, seed de escala y objetivos de rendimiento son decisiones de este proyecto. No proceden de mediciones del patio ni de promesas de las herramientas.

La propuesta de hornear difuso por estado y mantener reflejos dinámicos es una decisión de ingeniería para esta escena. Debe confirmarse con la prueba temprana. No se afirma que una sola opción reproduzca Cycles de manera idéntica en todos los navegadores.

## Verificación durante la implementación

- Three.js 0.186.1: documentación oficial de `MeshStandardMaterial` y `Texture`, y código instalado de `lights_fragment_maps`, `lights_fragment_end`, `EXRLoader`, `Water` y `GLTFLoader`. Se verificó el contrato de color/canal y se compararon imágenes reales; los shaders locales están en `web/src/lighting.ts`.
- Blender 5.2.1: RNA inspeccionado en ejecución. Se comprobó soporte de `export_meshopt_compression_enable`, `EXT_meshopt_compression` y exportación WebP. El manual web de baking devolvió error de acceso 402; se usó la API local y pruebas reales de horneado.
- [Vite: despliegue estático](https://vite.dev/guide/static-deploy.html), consultado para `base` y workflow de Pages. Dependencias fijadas por versión, con lockfile; la versión inicial Vite 8.0.2 se sustituyó por 8.3.2 tras `npm audit`. Auditoría posterior: cero vulnerabilidades.
- Biblioteca Water/Three.js y decodificador Meshopt: fuentes de la dependencia npm instalada, licencias incluidas en la entrega. No CDN necesario en runtime.

- Compositor de Blender 5.2.1: API RNA local (`Scene.compositing_node_group`, nodo `CompositorNodeDenoise`) verificada con una prueba EXR y ejecución de 30 atlas. No se interpretan las estimaciones de las referencias como una fuente métrica externa.
