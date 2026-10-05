# Progreso del proyecto

Actualización: 2026-10-04. Trabajo local autorizado; el usuario se encargará del repositorio remoto y publicación.

## Revisión solicitada el 4 de octubre — completada y entregada localmente

Encargo íntegro conservado en `outputs/revision-2026-10-04/encargo.txt` y `PromptModificacion.rtf`. S03–S08 cerradas para v3: ala diagonal, paso izquierdo, nueve luces, muebles, controles compactos/táctiles y día soleado. Maestro, seis estados, comparaciones, pruebas temporales, producción y copia local comprobados. Estado: `publish_ready` local; publicación a cargo del usuario.

## Estado histórico de v2 (antes de PromptModificacion)

| Fase | Estado | Evidencia |
|---|---|---|
| S00 entorno y referencias | pass | Ocho originales, inventario SHA-256, siete fotogramas, prueba bpy/Metal real. |
| S01 base y cámaras | pass con escala inferida | Revisión espacial v2, tres comparaciones verticales y planta trazada. |
| S02 piloto Cycles/web | pass | Pares día/noche ejecutados; UV/EXR/canales comprobados. |
| S03 geometría y variantes | pass | Maestro revisado, cuatro GLB y siete receptores validados. |
| S04 seis estados | pass | 90 EXR y seis renders generales más cinco vistas de inspección. |
| S05–S06 recorrido y comparación | pass con límites documentados | Nueve comprobaciones, seis pares Cycles/web y emulación táctil. |
| S07 producción | pass | Build y seis estados probados desde `/ProjectCobertizo/`, sin fallos HTTP/JS. |
| S08 entrega local | pass | `entrega-repositorio/` creada, archivos verificados por SHA-256 y maestro abierto desde esa copia. |

## Comprobaciones realizadas

- Blender 5.2.1 LTS, Apple M2 GPU 8 núcleos, RAM 16 GB, macOS 26.6.2. `blender/scripts/check_environment.py`: render Cycles GPU y archivo .blend real; imagen inspeccionada. `outputs/environment/blender.json` y `blender-test.log`.
- Node 26.5.1, npm 11.17.0, Python 3.14.6. Dependencias Python aisladas en `.venv/`, fijadas en `requirements.txt`.
- `tools/inspect_references.py`: FFmpeg 7.1, video 19,70 s, rotación respetada. `outputs/references/video-contact-sheet.jpg` inspeccionada junto a los siete originales de imagen.
- No hay `.git` ni remoto. Por instrucción posterior del usuario se preparará `entrega-repositorio/`, sin publicación.

## Evidencia e incertidumbres

Los parámetros son estimaciones editables. Los puntos ocultos de piscina y perímetro no son medidos. Se añadió una referencia suplementaria de detalle de propuesta; no se usa para afirmar estado construido.

## Siguiente acción

Cerrar la regeneración final, observar las luces en ejecución, revisar las capturas compactas/táctiles y volver a verificar producción y copia local. `entrega-repositorio/` todavía conserva la entrega v2 hasta que esas comprobaciones terminen. Los apartados siguientes conservan el historial de ejecución.

## Hito S01/S02/S03

- Maestro real `blender/patio_master.blend` generado y abierto por Blender. Cinco cámaras estables, geometría de tres variantes, piscina cerrada con vaso/borde/agua, suelo, muros, deck, cuatro sillas rojas, mesa, silla de trama abierta, tumbona, plantas y luminarias.
- Render general `outputs/renders/base-day.png` inspeccionado; se corrigieron planta espejada, encuadre recortado, luz diurna insuficiente y vegetación escasa. Se archivó el maestro anterior antes de cada regeneración.
- Piloto real en `blender/pilot.blend`, `outputs/pilot/` y recursos derivados. EXR/UV corregidos por comparación visual. Prueba automatizada Chromium: sin errores, WebGL2 y segundo canal UV presente en todos los receptores. Revisión adicional en navegador integrado.
- `web/` compila con Three.js 0.186.1, Vite 8.3.2 y TypeScript 6.0.2. Build inicial comprobado; no equivale a prueba de recorrido completo todavía.
- En curso: horneado de las seis combinaciones y capturas Cycles; después pruebas de navegación, cambios rápidos, errores de carga y producción.

## Corrección prioritaria solicitada por el usuario

El usuario observa que las dimensiones y el espacio no corresponden a las referencias. La planta actual no supera la aceptación espacial de S01. Se suspende la validación final y se prioriza un análisis profundo de juntas, esquinas, proporciones y cámaras en todas las referencias. El maestro actual queda como versión previa, no como reconstrucción espacial aceptada. No se deben cerrar S03–S08 sobre esta geometría sin corregirla.

### Revisión de planta en ejecución

- Analizados nuevamente los ocho originales, con recortes de juntas, líneas de fuga, puntos compartidos R02/R03 y trazado del arco de piscina. Generados `spatial-inference.json`, `r03-spatial-overlay.png`, `r02-shared-landmarks.png` e `inferred-plan.png`. Las imágenes de análisis fueron inspeccionadas.
- Configuración corregida y archivada la anterior. Sustituidas orientación, huella del deck, piscina, cierres, posiciones de muebles/luces y límites de navegación. El maestro se está regenerando; todavía no se afirma aceptación visual de esa regeneración.
- Siguiente acción: inspeccionar renders del patio existente sin cobertizo y las tres propuestas; resolver discrepancias espaciales antes de hornear de nuevo.

### Hito de corrección espacial del maestro

- Maestro revisado generado por `build_scene.py`; render general inspeccionado. Tres renders `PHOTO_*__existing.png` inspeccionados frente a R01/R02/R03. Se corrigieron también ancho continuo de franja artificial, esquina redondeada del césped y recorte del suelo en piscina.
- `validate_master.py` ejecutado: siete receptores, UV en [0,1], cero triángulos UV degenerados y cero píxeles solapados en la prueba raster a 512 px. Esa resolución no es una prueba analítica de ausencia de cualquier solapamiento.
- Cinco pruebas de colisiones y compilación TypeScript/Vite pasan. Se conserva la apariencia y la interfaz; los cambios de geometría se trasladan al contrato de navegación.
- Horneado completo de la planta revisada en ejecución. Pendientes: terminar seis estados, capturas web, pruebas de recorrido/producción, comparación y empaquetado local.

### Hito de exportación revisada

- Seis estados completos exportados desde el maestro revisado. `assets-report.json`: cuatro GLB Meshopt, 90 EXR HALF/ZIP con dimensiones verificadas, todos los recursos presentes y seis mapas distintos para superficies comunes.
- Once renders Cycles finales generados: seis generales, tres interiores de cubierta y dos de piscina. La lámina general y las vistas D3 de cubierta/piscina se inspeccionaron; continúa la comparación con navegador.
- `test_refresh.py` ejecutado en una copia descartable: `REFRESH_TEST_PASS`. Conserva transformaciones locales de fuentes y cámaras y deriva `USER_DETAILS`. El test compara transformaciones autoradas, no matrices evaluadas de objetos ocultos.
- `npm ci --prefix web` completado. La prueba web inicial detectó un selector ambiguo de día/noche y el uso de SwiftShader en Chromium Headless Shell; se corrige el alcance del selector y se comprueba un navegador con aceleración real antes de registrar rendimiento.
- Pendientes actuales: QA web final, build bajo prefijo, comparaciones y carpeta de entrega. No hay despliegue remoto solicitado.


### Validación final de la revisión

- Se completó `npm run qa` con Chromium 153.0.8010.12 y ANGLE Metal Apple M2. Nueve comprobaciones funcionales pasan; cero errores JS inesperados y cero respuestas HTTP fallidas. El único fallo de descarga fue inyectado deliberadamente para probar recuperación.
- Se inspeccionaron los tres pares fotografía/patio existente, seis pares Cycles/web, cubiertas, piscina y capturas táctiles. Los seis pares generales verifican misma posición, FOV, aspecto y agua detenida. Las diferencias de brillo, reflejos, cielo, vegetación y zonas inferidas permanecen explícitas en `docs/VALIDACION.md`.
- Correcciones de cierre: selector día/noche limitado a sus botones; filtrado de 30 atlas lineales y regeneración de 90 EXR; retirada de luces especulares puntuales sin sombras; separación de palanca y opciones en pantalla horizontal.
- `npm test --prefix web`: cinco pruebas pasan. `npm run build --prefix web`: TypeScript y Vite pasan. `tools/audit_assets.py`: hash de maestro, cuatro GLB y 90 mapas presentes/verificados.
- `node tests/production.mjs`: seis estados, movimiento y prefijo correctos, cero errores. Las 36 imágenes embebidas GLB usan URLs blob; las 41 respuestas HTTP están dentro del prefijo. El build excluye referencias, `.blend` y recursos del piloto.
- Rendimiento local medido a 1200×800: 60 FPS en los tres perfiles a DPR 1 para la muestra nocturna; D1 diurno en contexto DPR 2: 43,5 / 60 / 60 FPS, con DPR efectivo 1,75 / 1,25 / 0,85. No se extrapola a Internet ni a teléfono físico. `browser-report.json` conserva muestras y estimaciones de memoria.
- Navegador integrado: vista revisada cargada, día/noche accionado, consola limpia. Viewport temporal restablecido y vista general diurna conservada.
- Publicación remota: no ejecutada por instrucción del usuario. Entrega `publish_ready` local; teléfono físico `not_run`.


### Entrega local completada

- `entrega-repositorio/` contiene el maestro, scripts, configuración, referencias, web, `web/dist/`, workflow y evidencias. Se verificaron todos los archivos de la copia contra su manifiesto SHA-256.
- El maestro copiado se abrió con Blender: todas sus 31 imágenes de archivo resuelven dentro de la carpeta de entrega y la revisión espacial es v2. No necesita rutas del proyecto original para esas texturas.
- Se excluyeron entornos virtuales, dependencias instaladas, historial de maestros, copia descartable del test y capturas de diagnóstico. Las versiones anteriores siguen conservadas en el proyecto de trabajo.
- Estado final: `publish_ready` local, sin publicación remota. No hay errores funcionales conocidos pendientes de esta revisión. Precisión métrica, teléfono físico y diferencias Cycles/web mantienen los límites descritos en `docs/VALIDACION.md`.

## Hito v3: maestro y encuentros corregidos

- `PromptModificacion.rtf` leído: mismo encargo que el adjunto, con formato RTF. Rectángulo principal, 112 puntos de piscina, borde y cerco comprobados sin cambios respecto a la copia v2.
- Ala 1,39 → 1,69 m de trabajo; A conserva Y=6,15 y B alcanza el borde seco a Y=7,75786. Bases de ambos postes dentro de la tarima; cubierta, tablas y remates recortados. Escala estimada.
- Luces bajas: 3 comedor + 3 reposera + 3 baldosas; cero diagonal. Difusores separados 5 mm de la cara de carcasa; tapas del faldón sin coplanaridad con tablas.
- Sillas giradas hacia la mesa; reposera con respaldo unido, bisagra y soportes; apertura frontal y cojín interior de colgante. Renders cercanos revisados.
- Cruces reales de triángulos del follaje con las tres estructuras detectados por BVH y hojas afectadas retiradas; registro `foliage-intersections.json`.
- `geometry-checks.json` comprueba nueve luces, apoyos, piscina y 0/35 luces artificiales activas de día/noche en Blender.
- En curso: seis horneados completos; interfaz compacta/táctil implementada, todavía pendiente QA final con nuevos recursos.

### Validación geométrica v3 completada

- Siete receptores con cero degenerados y cero píxeles de solapamiento en prueba UV a 512 px. El comprobador ahora termina con error ante solapamientos.
- 273 sólidos nuevos revisados con caras orientadas consistentemente; cuatro sillas mirando a la mesa y diferencia numérica de unión de la reposera inferior a 0,000001 m del modelo. Es tolerancia de cálculo, no precisión métrica real.
- La muestra de 480 cuadros de v2 no encontró cambios de intensidad programados. Se preserva como diagnóstico, no como aceptación de aquella geometría.
- Fuente final reconstruida y conservada en Blender; todas las iluminaciones se regeneran desde esa misma fuente.

### Hito v3: inspección superior e interfaz

- Corregidos los cabios de D1 que asomaban por la cubierta. Prueba BVH sin cruces contra la piel exterior y render ortográfico inspeccionado con superficie continua.
- Primera QA general de navegador superada y conservada como diagnóstico previo al último ajuste de cabios. La prueba independiente de interfaz pasó con ratón, tacto, entradas mixtas, menús y rotación; no se usa como medición final de rendimiento.
- Los seis estados finales se han exportado y filtrado; build TypeScript/Vite completado. Se generan capturas de inspección y se repetirá la QA general con el mismo hash final del maestro.
- Continúan pendientes: ocho observaciones temporales, prueba de producción, comparación final y actualización de la copia local.

### Cambio solicitado: día soleado

- Se sustituye el ambiente uniforme nublado por cielo azul despejado y un sol direccional en Blender. Intensidad y dirección son decisiones visuales, no una simulación geográfica o una hora medida.
- Permanecen las correcciones v3. El cielo nocturno y los mapas de materiales no se regeneran. La iluminación artificial sigue apagada de día; la contribución solar difusa llega a la web mediante los horneados.
- Prueba temporal anterior interrumpida para validar el estado diurno definitivo. Pendientes: inspección del nuevo día, seis estados consistentes, ocho intervalos temporales, producción y copia local.

### Hito v3: sol y exportación final comprobados

- Fuente solar guardada; hash `ca9df64c8d2134e8b27b01cdc38b623411fca929a3e99c11b3c7feb9ebca6592`. Seis estados exportados, 30 atlas filtrados y 90 EXR comprobados. Cuatro GLB y todos los recursos presentes.
- Siete receptores conservan su geometría/UV. El comprobador del maestro confirma un sol natural diurno y cero nocturno; 0/35 fuentes artificiales y emisión 0/5.
- Renders de las tres propuestas, vistas superiores y detalles regenerados e inspeccionados. Comparaciones Cycles/web desde la misma cámara inspeccionadas en las seis combinaciones.
- `npm test` y build pasan. QA general de Chromium sobre M2 pasa nueve comprobaciones; los cinco errores de descarga y el aviso registrados corresponden exclusivamente a la interrupción deliberada para probar Reintentar.
- Muestra actual: 60 FPS a DPR 1 en los tres perfiles; día D1 Retina: 46,8/60/60 FPS (Alta/Equilibrada/Ligera). No son resultados de un teléfono. Continúan prueba temporal, producción y copia final.

### QA final v3 soleado superada

- Nueve comprobaciones generales, cuatro grupos de regresión, cinco pruebas de colisión y seis estados de producción pasan con el mismo hash del maestro.
- Ocho intervalos de 18 s, 8.648 cuadros: sin alternancias de estado/emisión ni posiciones de cámara inválidas. Variación de las nueve muestras de difusor en quieto: cero dentro de la precisión de lectura. Grabación WebM conservada.
- 390×844 → 844×390 → 390×844 conserva pose, estado y aspecto; Caminar/Salir, menús, tacto, ratón y entrada mixta comprobados. Es emulación en Mac, no iPhone físico.
- Producción: 41 respuestas HTTP bajo `/ProjectCobertizo/`, 36 imágenes GLB en memoria, sin errores. Compilación final completada.
- Siguiente acción: comprobar la copia local, actualizar manifiesto y cerrar la documentación de entrega.

- Navegador integrado comprobado adicionalmente: día → noche → día, capturas reales guardadas y consola limpia. El visor queda en día soleado y calidad Alta.

### Entrega final v3 completada

- `entrega-repositorio/` actualizada con maestro, configuración, scripts, referencias, web, build, documentación y evidencias; la copia v2 se conserva en una carpeta anterior.
- `tools/check_delivery.py` abrió el maestro desde la copia: 31 imágenes de archivo encontradas dentro de ella. Verificación SHA-256 de todos los archivos incluida en el manifiesto.
- Informes finales `browser-report.json`, `revision-report.json` y `production-report.json` corresponden al mismo hash del maestro soleado. Los ensayos anteriores y las observaciones interrumpidas no se presentan como validación final.
- `plan.md`, `decisions.md`, `assumptions.md` y documentos de revisión/validación actualizados. Capturas diurna/nocturna del navegador integrado y grabación temporal conservadas.
- Pendientes del alcance solicitado: ninguno. Teléfono físico/Safari iOS y publicación remota no ejecutados; límites de escala y diferencias de representación explícitos en `docs/VALIDACION.md`.
- Siguiente acción del usuario: revisar el recorrido o trasladar `entrega-repositorio/` al repositorio que elija. No hace falta publicar para usar los servidores locales actuales.
