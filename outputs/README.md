# Evidencias del proyecto

| Carpeta | Evidencia |
| --- | --- |
| `environment/` | Prueba real de bpy, .blend, Cycles y Metal. |
| `references/` | Inventario, fotogramas temporizados y miniaturas de originales. |
| `spatial-analysis/` | Planta revisada, lecturas de perspectiva y renders sin obra propuesta. Los ensayos `test` y copias `before/obsolete` son descartados, no pruebas finales. |
| `pilot/` | Muestra y pares Cycles/navegador de día y noche. |
| `renders/` | Renders Cycles de los estados y cámaras de inspección. |
| `browser/` | Capturas reales de Chromium y emulación táctil. |
| `comparisons/` | Láminas de referencia/maestro y maestro/web. |
| `validation/` | Informes de geometría, UV, exportación, recursos, navegador y producción. |
| `revision-2026-10-04/` | Encargo RTF transcrito, 19 capturas del usuario, geometría A/B, vistas superiores/detalles y observación temporal. Los archivos `baseline`, `before` y `preview` son diagnóstico previo, no resultado final. |

El maestro anterior a la revisión espacial no es evidencia de aceptación. Los logs `*-spatial-final*` corresponden a v2; los logs `*-sunny*` y los informes actuales con hash del maestro documentan v3 soleado. `progress.md` indica qué comandos y revisiones se han completado; la mera existencia de un script no significa que se haya ejecutado.

Las láminas `PHOTO_*` documentan la inferencia fotográfica v2 previa al encargo de modificación. Los pares `cycles-vs-web` y capturas finales generales se regeneran para v3. La modificación posterior del paso izquierdo está indicada en `docs/REVISION_2026-10-04.md`.

`browser/probe-*`, los EXR crudos de `lightmaps-raw/` y diagnósticos de ensayos se conservan en el proyecto original, pero no forman parte de las capturas finales de la entrega. `validation/denoising.json` registra el tratamiento de los atlas distribuidos.

La prueba temporal final completada queda en `validation/revision-report.json` y `revision-2026-10-04/temporal-high-auto.webm`. Los archivos `in-progress` nunca cuentan como aceptación. El cielo nocturno y 30 mapas de materiales conservan su SHA-256 anterior; los atlas de iluminación sí se regeneraron, por lo que no se promete identidad binaria de los EXR.
