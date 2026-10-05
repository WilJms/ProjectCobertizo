# Plan de ejecución

**Estado actualizado: entrega local completada y verificada (`publish_ready`).** El maestro se revisó espacialmente tras la observación del usuario. `progress.md` contiene evidencia y pendientes.

Reconstruir el patio, piscina y cierres, integrar los tres cobertizos y entregar una web recorrible para GitHub Pages. Maestro: `blender/patio_master.blend`; scripts: `blender/scripts/`; aplicación: `web/`.

`progress.md` registra la ejecución; `decisions.md`, las decisiones; `assumptions.md`, las estimaciones. Se siguen `AGENTS.md`, `PROMPT_INICIAL.md`, `docs/REFERENCIAS.md`, `docs/PIPELINE.md` y `docs/VALIDACION.md`. Las fuentes técnicas están en `docs/FUENTES.md`.

No solicitar fotografías ni medidas adicionales. Estimar con trazabilidad y continuar sin aprobaciones ordinarias entre etapas. Corregir errores y buscar alternativas compatibles. Reservar `blocked` para impedimentos reales de ejecución, acceso o credenciales; continuar las tareas independientes.

## S00 — Auditar entorno y referencias

**Estado:** `pass`. **Dependencias:** ninguna.

- **Trabajo:** localizar tres fotografías, tres diseños y video; usar la orientación técnica ya incorporada en `docs/PIPELINE.md`. Comprobar archivos, Blender, Node, herramientas de video, navegador y capacidad de render. Registrar versiones utilizadas.
- **Entregables:** inventario en `config/references.json`, referencias identificadas y fotogramas con tiempos en `outputs/`; diagnóstico del entorno en `progress.md`.
- **Aceptación:** referencias inspeccionadas y herramientas esenciales ejecutables.
- **Corrección:** buscar copias autorizadas de archivos faltantes y documentar limitaciones. No fingir inspecciones ni convertir dimensiones ausentes en bloqueos.

## S01 — Reconstruir distribución y cámaras

**Estado:** `pass`. **Dependencias:** S00.

- **Trabajo:** estimar escala, planta, alturas, piscina, pavimento, césped, cierres y deck. Resolver el límite hacia la casa sin modelarla en detalle. Registrar confianza y fundamento de cada estimación en `assumptions.md` y `config/scene-parameters.json`.
- **Entregables:** maestro preliminar, scripts reproducibles y cámaras `CAM01_GENERAL`, `CAM02_MURO_AZUL`, `CAM03_CERCO`, `CAM04_BAJO_CUBIERTA`, `CAM05_PISCINA`.
- **Aceptación:** distribución consistente entre las referencias; piscina y perímetro completos; proporciones coherentes desde varios puntos. Las dos últimas cámaras son revisiones sintéticas.
- **Corrección:** ajustar geometría y cámara. No compensar errores mediante materiales, encuadres engañosos o iluminación.

## S02 — Probar calidad de Blender a navegador

**Estado:** `pass`. **Dependencias:** S01.

- **Trabajo:** crear una muestra con cerco, muro, pavimento, deck, cubierta, luminaria y agua, de día y noche. Probar materiales horneados, iluminación, UV y color en Cycles y Three.js antes de detallar todo.
- **Entregables:** exportación de prueba, visor funcional, comparaciones y primeras mediciones en `outputs/`; contrato inicial en `web/public/assets/scene-manifest.json`.
- **Aceptación:** canal UV y mapas de iluminación comprobados; diferencias de exportación explicadas; ausencia de luz/AO duplicados; ruta viable para agua y cubierta clara.
- **Corrección:** aislar material, iluminación, color y reflejos; corregir la causa. Fijar presupuestos por perfil a partir de esta prueba.

## S03 — Completar geometría, variantes y materiales

**Estado:** `pass`. **Dependencias:** S02.

- **Trabajo:** completar patio, piscina, cierres, mobiliario y detalles visibles. Crear `d1_madera_dos_aguas`, `d2_oscuro_cielo_madera` y `d3_oscuro_paneles_claros`, manteniendo identidad, estructura y proporciones de cada diseño. El material exacto de los paneles claros sigue siendo una estimación.
- **Entregables:** maestro editable, materiales PBR, UV, texturas y geometría web; variantes independientes sobre una base común.
- **Aceptación:** cada diseño se reconoce por su construcción; las superficies próximas conservan detalle; los espacios no observados se completan coherentemente.
- **Corrección:** resolver primero siluetas, encuentros y escala de texturas. Sustituir aproximaciones genéricas que perjudiquen el parecido.

## S04 — Construir seis estados de iluminación

**Estado:** `pass`. **Dependencias:** S03.

- **Trabajo:** preparar `day` y `night` para cada diseño. Vincular geometría, luminarias, entorno, reflejos y horneados a su estado. Incluir todas las superficies compartidas cuya iluminación cambie.
- **Entregables:** seis estados completos en el manifiesto, mapas de iluminación y renders Cycles identificados por diseño, estado y cámara.
- **Aceptación:** luces apagadas de día y encendidas de noche; sombras coherentes con cada estructura; agua y cubierta correctas; contrato de composición sin duplicar aportaciones.
- **Corrección:** regenerar únicamente los recursos afectados por geometría o luces modificadas. No reutilizar mapas de otro diseño sin demostrar equivalencia.

## S05 — Implementar recorrido e interfaz

**Estado:** `pass`. **Dependencias:** S03; completar integración tras S04.

- **Trabajo:** movimiento libre con teclado/ratón y controles táctiles; colisiones, reinicio y vistas guardadas; selectores de diseño, iluminación y calidad. Resolver cambios rápidos y carga de recursos.
- **Entregables:** aplicación navegable con perfiles `high`, `balanced`, `low`; cambio de estado coherente y recuperación ante errores.
- **Aceptación:** recorrer todo el espacio accesible; cambiar de diseño conservando cámara cuando sea válido; reubicar de forma mínima si aparece un obstáculo; controles legibles y operables en pantalla pequeña.
- **Corrección:** reproducir cada fallo de interacción y comprobar el caso corregido, incluidas carreras de carga y recursos ausentes.

## S06 — Comparar y optimizar

**Estado:** `pass`. **Dependencias:** S04 y S05.

- **Trabajo:** ejecutar `docs/VALIDACION.md`; comparar referencias, Cycles y navegador con cámaras equivalentes. Medir carga, memoria estimada, tiempos de cuadro, geometría y texturas.
- **Entregables:** capturas reales, registro de discrepancias y resultados por perfil en `outputs/` y `progress.md`.
- **Aceptación:** seis estados coherentes; errores visuales relevantes corregidos; `high` disponible y preferido si el equipo lo permite. Metas iniciales: 60 FPS en escritorio capaz y 30 FPS en móvil representativo, sujetas a medición.
- **Corrección:** optimizar los costes medidos preservando fidelidad. No afirmar validación en dispositivos físicos ausentes.

## S07 — Preparar compilación y GitHub Pages

**Estado:** `pass`. **Dependencias:** S06.

- **Trabajo:** fijar dependencias, compilar, preparar el workflow de GitHub Actions y probar el resultado con la ruta base de un sitio de proyecto. Comprobar modelos, texturas, decodificadores y licencias.
- **Entregables:** `web/dist/`, workflow y comandos reproducibles; documentación del destino configurado o pendiente.
- **Aceptación:** compilación limpia y recorrido servido desde archivos de producción; rutas y recursos correctos bajo subdirectorio.
- **Corrección:** resolver fallos de carga y configuración. Si faltan destino o credenciales, entregar `publish_ready` con instrucciones precisas y declarar que todavía no está desplegado. Publicar solo con destino y autorización aplicables.

## S08 — Entregar y cerrar

**Estado:** `pass`. **Dependencias:** S07.

- **Entregables:** maestro Blender, scripts, recursos necesarios, código web, compilación, instrucciones y evidencias; documentación actualizada y lista exacta de limitaciones.
- **Aceptación:** otra sesión puede abrir, modificar, regenerar y servir el proyecto. Distinguir modelado, probado, listo para publicar y publicado.
- **Corrección:** completar archivos y pasos reproducibles que falten. Ninguna tarea esencial se considera terminada por tener una maqueta, un marcador o una promesa. Ante bloqueo real, conservar el trabajo recuperable y especificar la acción mínima pendiente.

## Revisión v3 — 2026-10-04

- [x] S03: planta A/B, paso izquierdo, muebles y luces 3+3+3+0; revisar arriba/general/cerca.
- [x] S04: regenerar seis estados desde el maestro y validar apagado completo/estabilidad.
- [x] S05: selector compacto por espacio, controles por entrada, Caminar/Salir táctil, resize conservando pose.
- [x] S06: pruebas temporales quieto/movimiento Alta/Auto; emulación retrato/paisaje y comparación Cycles/web.
- [x] S07–S08: producción con prefijo, documentación y copia local verificadas.
