# Contrato de producción Blender → web

Contrato del proyecto y criterios de implementación. El sistema efectivo usa el difuso estático de Cycles sin albedo, EXR HALF lineal y especular/agua en tiempo real; el código y los informes de `outputs/validation/` precisan el alcance probado. Consultar `docs/FUENTES.md` para las versiones comprobadas.

## 1. Organización y fuente maestra

| Ruta prevista | Responsabilidad |
| --- | --- |
| `config/scene-parameters.json` | Escala, geometría estimada, variantes y decisiones de escena. |
| `blender/patio_master.blend` | Maestro editable con cámaras y estados. |
| `blender/scripts/` | Construcción/actualización, render, horneado y exportación. |
| `web/src/` | Carga de escena, materiales adaptados, navegación y estados. |
| `web/public/assets/` | Recursos distribuidos en web y `scene-manifest.json`. |
| `web/dist/` | Resultado de producción generado por Vite. |
| `outputs/` | Renders, evidencias, comparaciones y registros. |

Las rutas contienen archivos generados por Blender y Vite. El estado de ejecución y de revisión visual se registra en `progress.md`.

Parametrizar los componentes regulares y conservar los ajustes manuales mediante un mecanismo explícito: capas de detalle, colecciones preservadas o scripts de actualización. No reconstruir destructivamente el maestro en cada modificación. Mantener una semilla reproducible para variaciones de materiales/vegetación.

Blender usa metros de trabajo estimados y Z vertical. glTF/Three.js usan Y vertical en esta ruta. Definir origen y orientación, dejar que el exportador haga su conversión y verificar puntos/cámaras: no sumar otra rotación automática por costumbre. Las colisiones y metadatos deben usar el mismo sistema que la geometría web.

## 2. Variantes y cámaras

IDs de diseño: `d1_madera_dos_aguas`, `d2_oscuro_cielo_madera`, `d3_oscuro_paneles_claros`. Estados: `day`, `night`. Clave de estado sugerida: `<design_id>__<time_id>`. Perfiles: `high`, `balanced`, `low`.

Separar geometría permanente, elementos de proyecto compartidos y geometría de cada alternativa. `KHR_materials_variants` solo resuelve sustituciones de materiales sobre geometría compartida; este proyecto requiere cambiar también objetos.

Cámaras: `CAM01_GENERAL` sobre R03, `CAM02_MURO_AZUL` sobre R02, `CAM03_CERCO` sobre R01; `CAM04_BAJO_CUBIERTA` y `CAM05_PISCINA` son vistas de inspección creadas para el modelo. Guardar pose, proyección, aspecto y recorte. Mantener una cámara de navegación separada y evitar confundir focal con FOV sin considerar sensor/aspecto.

## 3. Geometría y materiales

GLB es el formato principal, pero no impone un archivo monolítico que duplique seis patios. Exportar recursos compartidos y variantes con IDs estables. Mallas, materiales y primitivas que reciben mapas distintos deben conservar una correspondencia después de optimizar.

Hornear o adaptar nodos procedurales no exportables. Convertir curvas, modificadores o instancias cuando sea necesario en la representación derivada, conservando el maestro. Mantener geometría para siluetas, juntas profundas y huecos; transferir microdetalle adecuado a normales.

Albedo libre de iluminación, rugosidad y normales coherentes con la escala. El acabado oscuro pintado no se convierte automáticamente en metal desnudo. El cerco existente y la madera nueva pueden necesitar acabados diferentes. Documentar todo recurso externo y su licencia en un registro de assets del proyecto.

El segundo UV de iluminación requiere islas sin solapamiento indebido y márgenes adecuados al filtrado. Evitar instanciar objetos con el mismo lightmap si reciben iluminación distinta; elegir atlas por instancia, un atributo adicional compatible o geometría independiente según el caso. La optimización no debe eliminar UVs, normales, tangentes o IDs necesarios.

## 4. Composición de iluminación

La hipótesis inicial favorece **difuso estático horneado por estado y respuesta dependiente de la vista en tiempo real**. La prueba S02 decide si conviene ese reparto o una combinación con indirecto horneado y algunas luces directas dinámicas. Registrar la decisión antes de producir todos los estados.

Para cada familia de materiales, declarar una tabla de contribuciones:

| Contribución | Dónde se calcula | Riesgo a comprobar |
| --- | --- | --- |
| Difuso directo | Bake o runtime, según decisión | No sumar dos veces las mismas lámparas/sol. |
| Difuso indirecto y ambiente | Bake o runtime, según decisión | Un HDRI puede aportar difuso además de reflejos. |
| Albedo | Material o bake de color, según semántica | No multiplicar dos veces el color. |
| Especular/reflejos | Runtime o aproximación por estado | Debe responder al ángulo de cámara. |
| Emisión visible | Material activo por estado | Su brillo visible no sustituye la luz sobre otras superficies. |
| Oclusión/contacto | Bake, AO o efecto elegido | No ennegrecer contactos mediante acumulación de AO/SSAO. |

Si se usa un lightmap que contiene iluminación difusa completa, un material estándar con todas las luces y `scene.environment` activados puede añadir de nuevo difuso. Preparar una adaptación de material pequeña y comprobable que preserve la parte especular necesaria. Si no es viable con calidad y coste adecuados, cambiar el reparto documentadamente. No imponer un shader enorme sin comparar sus resultados.

Conservar semántica y unidades del horneado: distinguir irradiancia/contribución de luz, radiancia difusa final y albedo. Un bake de color final no puede conectarse como si fuera irradiancia pura. Un mapa de AO no contiene iluminación global. No asumir que los canales sin albedo carecen de color de luz: conservar la cromaticidad de las contribuciones cuando corresponda.

La luz sobre el suelo, cercos y muros depende del diseño activo. Regenerar los receptores afectados al modificar estructura, material de cubierta o luminarias. Reutilizar mapas solo tras comprobar equivalencia, no porque la geometría del receptor sea común.

## 5. Manifiesto de escena y asignación de lightmaps

Crear `web/public/assets/scene-manifest.json` con un contrato versionado y validar sus referencias al cargar. Cada estado contiene al menos:

- `designId`, `timeId`, versión/hash de recursos.
- Recursos de geometría común y de variante.
- Asignación por ID estable de malla/primitiva/material a lightmaps.
- Canal UV, orientación de textura, formato, decodificación, espacio/rango de color y factor de escala del mapa.
- Cielo/ambiente, orientación/intensidad, reflexión global o local.
- Luces y emisivos con parámetros explícitos.
- Configuración de agua/reflejos y exposición/visualización.
- Colisiones y áreas transitables correspondientes.
- Recursos disponibles por perfil de calidad.

glTF no exporta automáticamente el contrato de `lightMap` de Three.js. Transportar el vínculo mediante metadatos o manifiesto propio y aplicarlo explícitamente tras cargar.

Verificar el canal UV real de la versión instalada. La documentación consultada de Three.js asigna `Texture.channel`: 0 a `uv`, 1 a `uv1`, 2 a `uv2`, 3 a `uv3`. No copiar instrucciones antiguas que llamen siempre `uv2` al segundo canal. Comprobar además `flipY`, tangentes y correspondencia de `TEXCOORD_n` después de exportar/optimizar.

## 6. Color, HDR y postprocesado

Registrar espacios de entrada, espacio lineal de trabajo y transformación de salida. Albedo/emisivo ordinarios suelen ser sRGB; rugosidad, normales y metalness son datos. Los mapas de luz deben interpretarse conforme al formato elegido, no asignarse por extensión a ciegas.

Mantener rango dinámico suficiente en los horneados. No convertir una imagen lineal EXR en PNG de 8 bits con AgX aplicado y después tratarla como luz física. Si se elige una codificación compacta, documentar su decodificación y comparar rango, bandas, color y brillo antes de adoptarla. KTX2 para materiales no resuelve automáticamente todos los requisitos de lightmaps HDR.

AgX es un candidato de visualización, no una prueba de paridad. Comparar exposición, blancos, sombras y altas luces. Aplicar tone mapping/conversión de salida una sola vez en el pipeline efectivo. Si se usa compositor, revisar el pase de salida y su compatibilidad con la versión elegida.

Bloom discreto solo donde mejore la representación de luces intensas. Mantener profundidad de campo desactivada al caminar. Evitar filtros que escondan errores de materiales o diferencias entre motores.

## 7. Agua, cubierta y reflejos

El agua combina geometría del vaso, nivel, fondo, normales animadas y reflejos adecuados a la vista. Probar reflexión planar en calidad alta y alternativas de menor coste por perfil. Capturas de ambiente locales pueden ser útiles, pero documentar sus límites de paralaje.

Actualizar reflejos al cambiar diseño o luz. No hornear un reflejo de cámara en el albedo. Para comparar imágenes, fijar tiempo de animación del agua; para validar el recorrido, inspeccionarlo en movimiento.

La cubierta clara se aproxima por su apariencia. Evaluar espesor, caras, transmisión/difusión y sombras. Si la transmisión del material web no reproduce el paso de luz al suelo, incorporar esa aportación estática en el horneado coherente. No asumir que transparencia alfa equivale al comportamiento del panel.

## 8. Estado de aplicación y memoria

Gestionar selección de diseño, hora y calidad como un estado coherente. Cargar dependencias, verificar que pertenecen a la selección vigente y realizar el cambio atómico. Descartar respuestas de cargas antiguas para evitar carreras al pulsar rápido. Conservar el estado anterior si falla la nueva carga y mostrar una opción de reintento.

La cámara mantiene pose cuando es válida; resolver colisiones nuevas moviéndola al punto transitable próximo. Controles de teclado/ratón y táctiles comparten el mismo controlador espacial.

Medir descarga, memoria estimada, llamadas de dibujo y tiempos de cuadro. Los bytes del JPEG/GLB descargado no representan su consumo GPU. Compartir, cargar bajo demanda y liberar recursos con una política de caché explícita. Elegir KTX2/Basis y Meshopt o Draco después de medir y comprobar las versiones de sus decodificadores.

Conservar `high`, `balanced`, `low`. Fijar presupuestos a partir del prototipo; no imponer un número universal de polígonos o megabytes que obligue a degradar el parecido sin motivo. Diferenciar rendimiento físico de emulación de pantalla.

## 9. GitHub Pages

Aplicación estática, sin backend necesario para renderizar el patio. Blender produce recursos antes del despliegue. La visita no requiere cuenta de Codex ni Blender instalado.

Configurar Vite y todas las rutas de recursos/decodificadores para la base de Pages; usar `import.meta.env.BASE_URL` o un mecanismo equivalente correcto. El ejemplo `'/models/escena.glb'` no es una ruta segura para un proyecto publicado bajo `/nombre-repositorio/`.

Fijar dependencias y comprobar build de producción servido bajo ese prefijo. El workflow se sitúa en la raíz del repositorio (`.github/workflows/`) y construye la aplicación de `web/`. Seleccionar versiones vigentes de acciones al implementarlo, respetando los permisos del repositorio.

Publicar los archivos de `web/dist/`; conservar fuentes Blender y originales por separado del build. Si se usa Git LFS para fuentes pesadas, no asumir que sus punteros son assets web utilizables: la distribución debe contener bytes reales. Revisar límites vigentes de GitHub Pages y del repositorio.

Entregar `publish_ready` cuando falte destino/acceso de publicación, después de terminar y verificar la versión local. Solo registrar `deployed` al ejecutar y comprobar el despliegue autorizado.

## Implementación efectiva

- Blender 5.2.1 LTS / Metal; Three.js 0.186.1, Vite 8.3.2 y TypeScript 6.0.2. Versiones fijadas en los archivos de dependencias.
- `UVMap` corresponde a textura material; `LightmapUV` se exporta como `TEXCOORD_1` y se asigna a `Texture.channel = 1`, `flipY = true`. Islas y ocupación se comprueban en `uv-report.json`.
- Bake `DIFFUSE`, directo + indirecto, sin `COLOR`, sin AO. EXR ZIP HALF, datos lineales Rec.709. `lighting.ts` sustituye todo el difuso del material, incluido el del ambiente, conservando el especular.
- Cielo procedural JPEG original, sin pretensión de calibración fotométrica. Intensidad ambiental diurna 7; brillo del fondo 1,2; noche 1. Exposición 1,2 y AgX una vez. Las lámparas se apagan de día.
- Geometría Meshopt y texturas WebP de calidad 92 dentro de GLB. No hay codificador `toktx` disponible en el entorno comprobado; KTX2/Basis no se implementa. La descarga se comprime con WebP, mientras que los lightmaps conservan precisión HDR. Esto no equivale a compresión GPU de las texturas.
- Perfiles de atlas 2048/1024/512 para superficies y escalas proporcionales para otros receptores. Caché de dos estados de luz; modelos compartidos conservados; mapas/materiales de estados retirados se liberan.
- Reflexión planar del agua a 512², actualización cada 1/2/4 cuadros según calidad. La absorción/translucidez web es una aproximación; el agua de Cycles usa transmisión e IOR 1,333. La ondulación se congela en capturas comparativas.
- Las tres cámaras PHOTO del maestro son verticales para comparar fotografías. Las cinco CAM del recorrido son encuadres prácticos con pose/proyección compartidas entre renders y web.


### Ajuste comprobado tras la revisión espacial

Los atlas finales se filtran con `blender/scripts/denoise_lightmaps.py` antes de producir los perfiles menores. El compositor trabaja con EXR lineal HALF/ZIP y no introduce AgX. `bakes.json` conserva la evidencia del horneado; `denoising.json` vincula cada entrada cruda con el archivo distribuido. El filtrado puede suavizar iluminación fina en islas pequeñas, sin alterar las texturas de albedo.

El especular web usa el entorno PBR y, en la piscina, el reflejo planar de geometría y emisivos activos. Se retiraron las luces puntuales auxiliares sin sombras porque su brillo atravesaba cubiertas y hojas. No hay luces difusas dinámicas. Las luminarias siguen iluminando muros, muebles y suelos mediante los seis horneados; la reflexión local sobre otros acabados es una aproximación pendiente de una futura solución con sombras especulares.

### Estabilidad y planta v3

Los polígonos de tarima y cubiertas se extruyen con normales exteriores; tablas y paneles se recortan contra la diagonal real A/B. `plan_geometry.py` comparte el recorte entre las tres variantes. El atlas y los seis horneados se regeneran tras cualquier modificación de esa planta o de las nueve luces bajas. El número 3+3+3+0 viene de `PromptModificacion.rtf` y sustituye la distribución anterior.

Los difusores están separados físicamente de sus carcasas. Las tapas del faldón quedan debajo de las tablas; no se usa polygonOffset para disimular piezas coincidentes. No se anima la intensidad de las luminarias. Día/Noche se activa con los materiales, entorno y mapas de un único estado.

La reflexión planar se actualiza en el primer cuadro de cada estado y cuando cambian pose o viewport. Solo con cámara quieta puede reutilizarse según el perfil. Así se conservan los reflejos al caminar sin mantener una matriz de proyección de una pose antigua.

## Día soleado de v3

`config/scene-parameters.json > lighting.day` gobierna el sol natural `SUN_DAY`, su diámetro angular, dirección elegida y energía, además del ambiente despejado. El sol existe en el maestro y se apaga en `night`; es independiente de los 35 emisores artificiales nocturnos. Luz directa, sombra y rebotes solares se incluyen una vez en el pase DIFFUSE sin COLOR de cada propuesta. No se añade luz solar difusa dinámica en Three.js. El entorno de cielo proporciona fondo y especular; su componente difusa sigue sustituida por la irradiancia horneada. El disco solar especular no se reconstruye de forma analítica en web.

`tools/make_day_sky.py` cambia únicamente `sky_day.jpg`. `blender/scripts/update_daylight.py`, ejecutado sobre el maestro abierto, archiva la versión anterior y conserva geometría y UV. Después se exportan, filtran y prueban los seis estados. Los cambios de iluminación posteriores deben actualizar fuente, manifiesto y horneados juntos.
