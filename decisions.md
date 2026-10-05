# Decisiones

Estas decisiones recogen el encargo y la estrategia inicial. Se pueden refinar con evidencia durante el desarrollo. Un cambio debe incluir motivo, efectos y documentos o recursos que deban actualizarse.

| ID | Decisión | Motivo / autoridad | Estado |
| --- | --- | --- | --- |
| D-001 | Trabajar con los recursos visuales aportados (8 originales localizados), sin nuevas medidas ni capturas. | Restricción expresa del usuario. | Fijada. |
| D-002 | Reconstrucción visual con escala estimada, común y editable. | Los adjuntos no ofrecen dimensiones verificadas. | Fijada. |
| D-003 | Patio completo, piscina y cierres; casa fuera del modelado detallado. | Alcance solicitado. | Fijada. |
| D-004 | Fotos/video gobiernan lo existente y diseños gobiernan la construcción nueva. | Los conceptos alteran algunas superficies existentes. | Fijada. |
| D-005 | Escena maestra Blender/Cycles y derivación optimizada Three.js/TypeScript/Vite. | Fidelidad editable y recorrido web estático. | Estrategia inicial. |
| D-006 | Probar una muestra Blender/web antes de completar toda la escena. | Resolver pronto luz, agua, materiales y color. | Fijada. |
| D-007 | Tres variantes geométricas con IDs estables, dos estados de luz por variante. | Cambian cubiertas, estructura y efectos sobre el entorno. | Fijada. |
| D-008 | Manifiesto explícito por estado, con iluminación en receptores comunes y variantes. | glTF no conserva por sí solo el resultado de Cycles. | Fijada. |
| D-009 | Evaluar primero difuso estático horneado y especular/reflejos en runtime; confirmar reparto en S02. | La escena tiene seis estados definidos y cámara móvil. | Validada en piloto; refinada en D-021. |
| D-010 | AgX como candidato de visualización, calibrado con referencias. | Nombres de transform iguales no prueban igualdad visual. | Validada en piloto; refinada en D-021. |
| D-011 | Navegación libre y táctil, colisiones, vistas guardadas auxiliares. | Requisito funcional. | Fijada. |
| D-012 | Calidad alta como objetivo, perfiles adaptables según medición. | Prioridad visual del usuario y diversidad de dispositivos. | Fijada. |
| D-013 | GitHub Pages para distribución estática; ninguna dependencia de servidor Blender en producción. | Destino solicitado. | Fijada. |
| D-014 | La publicación se realiza solo con destino, acceso y autorización aplicables; en su ausencia entregar `publish_ready`. | Evitar afirmar una URL inexistente o elegir una cuenta ajena. | Fijada. |
| D-015 | No duplicar los originales en el build web. | Son material de trabajo, no dependencias del recorrido. | Fijada. |

## Decisiones por cerrar mediante trabajo, sin pedir nuevos recursos al usuario

- Escala final estimada y geometría de zonas fuera de cámara.
- Material equivalente de la cubierta clara y su transmisión difusa aproximada.
- Número y posición de luces parcialmente ocultas.
- Reparto de luz horneada/runtime y formato de lightmaps.
- Método de reflejos del agua por perfil de calidad.
- Versiones de herramientas, estrategia de recursos y presupuestos de rendimiento.

## Plantilla de nueva decisión

### D-0XX — Título

- Fecha:
- Problema y evidencia:
- Decisión:
- Alternativas relevantes consideradas:
- Consecuencias visuales/técnicas:
- Archivos/estados que cambian:
- Revisión realizada o pendiente:

Conservar el historial de decisiones sustituidas indicando cuál las reemplaza.

### D-016 — Entrega exclusivamente local

- Fecha: 2026-10-03.
- Autoridad: el usuario indicó que trasladará los archivos a Git y gestionará la publicación.
- Decisión: preparar `entrega-repositorio/` al finalizar, sin crear repositorio remoto ni solicitar destino. Incluir fuentes y workflow, excluir entornos instalados y cachés. Estado final de publicación: `publish_ready`, nunca `deployed`.

### D-017 — Referencias efectivas y herramientas verificadas

- Ocho originales encontrados e inventariados con SHA-256; D3 se llama `Unknown.png`. Se conservan bytes originales.
- Siete fotogramas representativos a 0,5; 3; 6; 9; 12; 15 y 18,5 s; FFmpeg 7.1 respeta la rotación −90° del video. Duración 19,70 s.
- Blender 5.2.1 LTS ejecutó bpy, guardó y renderizó con Metal en Apple M2 de 16 GB. Evidencia: `outputs/environment/`.
- La geometría y las texturas se crearán localmente de forma reproducible. No se generan imágenes sustitutivas de las referencias ni se compra material.
- La interfaz se limita al visor y controles pedidos; la guía frontend se aplica subordinada al encargo de fidelidad 3D y a sus referencias existentes.

### D-018 — Resultado del piloto: difuso Cycles y reflejos móviles

- Se generaron y revisaron pares Cycles/web de día y noche a 960 × 640. Se corrigieron dos defectos reales: inversión vertical de EXR y luminarias ocultas por pertenecer a la colección del receptor.
- Horneado `DIFFUSE`, directo e indirecto activados, `COLOR` desactivado. Representa E/π para albedo unitario; se multiplica una vez por el albedo. El shader reemplaza todo el difuso de runtime, también el del ambiente. No AO ni SSAO adicionales.
- El EXR se guarda ZIP de 16 bits flotantes, escena lineal Rec.709, sin AgX. El piloto nocturno conserva valores hasta 2,83; la exportación inicial de 32 bits sin compresión se descartó. `Texture.channel = 1` usa `uv1 / TEXCOORD_1`. `flipY = true` es el resultado comprobado para EXRLoader y esta exportación; las texturas glTF normales conservan su configuración propia.
- Especular PBR y reflexión planar del agua en runtime. Los paneles transmiten de forma difusa en Cycles (mezcla 28%); esa luz recibida queda horneada. En web son paños opacos de aspecto difusor, no una simulación volumétrica de policarbonato.
- AgX en ambos, exposición explícita. El cielo procedural de 8 bits no tiene calibración radiométrica; la intensidad de iluminación diurna se ajustó a 7, con intensidad de fondo visible 1,2. No se afirma hora ni orientación real.
- Perfiles: mapas completos / mitad / cuarto de resolución por dimensión; resolución de pantalla y frecuencia de reflexión adaptables. La geometría y los límites transitables se conservan.

### D-019 — Plano y cámaras tras contraste visual

- R02 y R03 muestran muro azul perpendicular al cerco alto. Se corrigió la primera hipótesis colineal antes del horneado final.
- Parámetros de planta: X a la derecha de la vista general, Y hacia casa. Blender convierte a `(X, -Y, Z)`; glTF/Three.js a `(X, Z, Y)`. Las cámaras guardan coordenadas de planta explícitas y exportan la pose real en el manifiesto.
- Se conserva el aspecto de las superficies reales. Las cubiertas ocupan una L: comedor en ala izquierda y tumbona en ala de fondo. Los cambios ocultos se simplifican; no hay vivienda detallada.

## D020 — Rehacer la planta desde las referencias

La observación del usuario invalida la aceptación espacial previa. Se sustituye D019 en su interpretación de la planta: muro azul transversal y cerco alto lateral; terraza principal ancha y poco profunda, con ala estrecha siguiendo el cerco. Se trazó el arco de piscina con una proyección aproximada de R03 y puntos compartidos de R02, y se conservaron cámaras verticales independientes. Se revisará el patio sin obra propuesta antes de repetir las seis iluminaciones. Gráficos, controles y funciones se conservan conforme a la indicación del usuario.

Los ensayos de homografía de una sola baldosa se descartan por inestabilidad. Las lecturas, incertidumbres, planta y superposiciones quedan guardadas; no se presentan como medidas reales. La configuración anterior y el script anterior se conservaron en `outputs/spatial-analysis/`, además del historial de maestros.


### D-021 — Correspondencia final y pruebas locales

- Fecha: 2026-10-03. La comparación real detectó ruido de muestreo en atlas nocturnos y brillo excesivo provocado por luces puntuales auxiliares sin sombras. Se filtra la irradiancia lineal con el nodo Denoise de Blender y se conservan los EXR crudos por hash. La textura de color no cambia. Se elimina aquella contribución especular puntual; ambiente PBR y reflexión planar del agua siguen respondiendo a la cámara. No se añade un segundo difuso.
- Se mantienen materiales, geometría revisada, agua y controles. El filtrado puede suavizar pequeñas sombras en islas UV reducidas. La reflexión de luminarias locales en otros materiales es aproximada; no se afirma igualdad píxel a píxel con Cycles.
- `flipY=true` se confirmó de nuevo por prueba A/B; invertirlo rompe la correspondencia del atlas y se descartó. No se cambia el canal de iluminación.
- Las capturas generales usan cámara, FOV, aspecto 1,5, resolución 1200×800 y agua en t=0 comprobados en ejecución. Las fotografías se comparan por separado con las cámaras PHOTO y el patio sin obra nueva.
- Chromium Headless Shell escogió SwiftShader; se usa el canal Chromium completo, cuyo renderizador real se identifica como ANGLE Metal Apple M2. La emulación táctil sigue sin equivaler a un teléfono físico.
- Se ajusta únicamente el punto de corte de la interfaz táctil horizontal para evitar que la palanca cubra las opciones de diseño. No hay rediseño de controles.

### D-022 — Correcciones explícitas del 4 de octubre

- Se aplica `PromptModificacion.rtf` sobre v2. Se preservan el cuerpo principal, piscina y cerco; el desplazamiento de baldosas y límite izquierdo responde a la instrucción posterior del usuario.
- Planta común con A retraída y B extendida; recorte geométrico de tablas/paneles, vigas y dos apoyos terminales en las tres variantes. Se regenera toda la iluminación porque cambian sombras y emisores compartidos.
- Diagnóstico geométrico: filas de tablas cruzaban el límite del bloque principal y sus caras superiores coincidían con tapas del faldón. Los difusores sobresalían solo 1 mm de un cuerpo sólido que los atravesaba. Se eliminan las caras superpuestas, con montaje y separación explícitos. No se atribuye una prueba temporal al mero diagnóstico.
- La reflexión del agua se fuerza inmediatamente al cambiar estado, cámara o viewport; solo se espacian actualizaciones con cámara quieta. Se evita mostrar reflejos del estado/pose anterior durante 1–3 cuadros en perfiles menores.
- Selector compacto según espacio disponible, entrada según capacidades y último puntero. Caminar/Salir controla la palanca táctil, los menús suspenden entrada de navegación, y ResizeObserver/visualViewport actualizan render sin rehacer pose. Pruebas temporales y táctiles pendientes al registrar esta decisión.

- Diagnóstico adicional en la copia anterior sin modificar: 480 cuadros observados durante dos intervalos de 6 s (día/noche). No hubo alternancia de estado, raíz ni intensidad; emisión estable 0/5 (`baseline-runtime.json`). Esto descarta una pulsación programada en esa muestra, sin afirmar que una vista fija reproduzca todo artefacto al moverse. La corrección se centra en profundidad de superficies y actualización del reflejo.
- La primera malla nueva presentó caras laterales invertidas en el extrusor de polígonos. La prueba UV encontró solapamientos y se detuvo aquel horneado. Se corrigió el orden de los vértices; los siete atlas vuelven a cero solapamientos detectados a 512 px. La validación ahora falla explícitamente si reaparece el defecto.

### D-023 — Revisión superior y trazabilidad del cierre

- La inspección desde arriba de D1 reveló tres cabios cruzando la piel del techo. Se bajó el conjunto de cabios dentro del espesor previsto, conservando silueta, cubierta, dimensiones y apoyos. Una prueba BVH comprueba ausencia de cruces con las dos vertientes.
- Se repite la derivación y el horneado después de esa corrección. Los informes de navegador, observación temporal y producción incluyen el hash del maestro; la entrega rechaza cualquier informe de una fuente previa aunque comparta la etiqueta v3.
- Las pruebas de interfaz pueden ejecutarse durante preparación de recursos, pero no cuentan como prueba visual final ni medición de rendimiento. Las medidas finales se ejecutan con los trabajos de Cycles terminados.

## D-024 — Sol diurno en la fuente maestra

Por petición del usuario se añade `SUN_DAY` natural, independiente de las luminarias artificiales. El cielo diurno pierde las nubes; `sky_night.jpg` y los albedos permanecen sin cambios. Cycles calcula luz solar directa, sombras y rebotes en cada diseño; la web consume una sola contribución difusa horneada y conserva entorno especular/reflejo de piscina. De noche el sol queda apagado. Se regeneran los seis estados para mantener una única procedencia del maestro y se repiten las pruebas finales.
