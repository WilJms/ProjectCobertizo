# Operación y regeneración

El maestro es `blender/patio_master.blend`. Las longitudes están estimadas; la noche y el lado oculto de la piscina son interpretaciones. La aplicación no necesita Blender ni un servidor de backend.

## Abrir el recorrido

Desde la raíz:

```sh
npm ci --prefix web
npm run dev --prefix web
```

Abrir `http://127.0.0.1:5173/ProjectCobertizo/`. Arrastrar para mirar, W A S D para desplazarse; la palanca táctil y las vistas guardadas son complementos. El selector Automática comienza en Alta y reduce calidad si los tiempos medidos de cuadro lo requieren. Una elección manual suspende ese ajuste.

## Build de producción bajo un subdirectorio

```sh
npm run build --prefix web
python3 tools/serve_production.py
```

Abrir `http://127.0.0.1:4173/ProjectCobertizo/`. Para otro nombre, compilar con `BASE_PATH=/NombreRepositorio/ npm run build --prefix web` y servir con `--base /NombreRepositorio/`. No abrir el HTML con `file://`: los modelos y mapas requieren peticiones HTTP.

El workflow de `.github/workflows/pages.yml` construye únicamente `web/` y publica únicamente `web/dist/`. Deduce la base del nombre del repositorio. Al trasladar la carpeta a GitHub, elegir GitHub Actions en la configuración de Pages y usar la rama `main` (o adaptar el workflow). El workflow se entrega preparado; no se ha ejecutado un despliegue remoto.

## Abrir y editar Blender

Se comprobó Blender 5.2.1 LTS en macOS con Metal. En otras plataformas ajustar la ruta del ejecutable; el código admite CPU si Metal no está disponible.

Las colecciones `surfaces`, `furniture`, `vegetation`, `fixtures` y las tres `d*` contienen fuentes editables. `WEB_DERIVED` es la representación preparada para exportación; sus nombres y UV son el vínculo del manifiesto. `LIGHTING` contiene fuentes luminosas; las cámaras conservan los IDs del encargo. Añadir detalles propios a `USER_DETAILS`.

Tras editar geometría fuente en Blender, guardar y actualizar solo la copia derivada:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b blender/patio_master.blend --python-exit-code 1 --python blender/scripts/refresh_derived.py
/Applications/Blender.app/Contents/MacOS/Blender -b blender/patio_master.blend -t 6 --python-exit-code 1 --python blender/scripts/export_scene.py
/Applications/Blender.app/Contents/MacOS/Blender -b -t 4 --python-exit-code 1 --python blender/scripts/denoise_lightmaps.py
.venv/bin/python tools/prepare_renders.py
npm run build --prefix web
```

`refresh_derived.py` conserva las fuentes y archiva una copia del maestro. Añade `USER_DETAILS` a los receptores si contiene mallas. Si cambian obstáculos o cámaras, actualizar también los metadatos de colisiones/cámaras de la escena y la configuración: las colisiones no se infieren automáticamente de cualquier modificación manual.

`export_scene.py` abre el maestro ya cargado, exporta GLB, hornea todas las superficies para los seis estados y genera renders. `-- --no-bake` sirve para regenerar exportación/manifiesto únicamente cuando UV, geometría e iluminación no han cambiado. `-- --quick` genera solo D1 día y no es una entrega completa. No publicar mapas antiguos después de modificar UV o fuentes de luz.

## Reconstrucción reproducible desde scripts

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/inspect_references.py
.venv/bin/python tools/make_textures.py
.venv/bin/python tools/water_normal.py
/Applications/Blender.app/Contents/MacOS/Blender -b -t 6 --python-exit-code 1 --python blender/scripts/build_scene.py
/Applications/Blender.app/Contents/MacOS/Blender -b blender/patio_master.blend -t 6 --python-exit-code 1 --python blender/scripts/export_scene.py
/Applications/Blender.app/Contents/MacOS/Blender -b -t 4 --python-exit-code 1 --python blender/scripts/denoise_lightmaps.py
.venv/bin/python tools/prepare_renders.py
```

`build_scene.py` crea una nueva reconstrucción de los scripts y guarda el maestro anterior en `blender/history/`. Para conservar ediciones manuales activas, utilizar `refresh_derived.py`, no la reconstrucción total. Las constantes de detalle están en `patio_geometry.py` y `patio_structures.py`; los parámetros de planta, postes y cámaras están en `config/scene-parameters.json`. La semilla es 7321. No hay descarga de recursos de terceros en esta generación.

## Validación

```sh
npm test --prefix web
/Applications/Blender.app/Contents/MacOS/Blender -b blender/patio_master.blend --python-exit-code 1 --python blender/scripts/validate_master.py
.venv/bin/python tools/audit_assets.py
```

Con la web en ejecución, desde `web/`: `npm run qa`. `TEST_URL` permite verificar un servidor de producción con su prefijo. Playwright Chromium debe estar instalado con `npx playwright install chromium`. Los tests guardan evidencia solicitada en `outputs/`. La emulación táctil no demuestra rendimiento de un teléfono físico.


## Evidencia espacial y reanudación

`tools/analyze_spatial_references.py` genera lecturas y superposiciones sin cambiar el modelo por defecto. Su opción `--apply` reemplaza parámetros inferidos y obliga a reconstruir y validar de nuevo; no ejecutarla para una simple consulta. `tools/configure_scene.py` comprueba la configuración actual sin restablecer la planta obsoleta.

`export_scene.py -- --resume-designs=d1_madera_dos_aguas` se utilizó para conservar los dos estados completos de D1 al reanudar el horneado del mismo maestro. Comprueba que mapas de los tres perfiles y renders son posteriores al maestro. Usar solo si no han cambiado geometría, UV o iluminación; el informe conserva el hash de la fuente y de cada mapa retomado.

Después de las capturas, `.venv/bin/python tools/prepare_comparisons.py` compone láminas con los archivos reales, sin retoque visual. `node tests/production.mjs`, desde `web/`, comprueba el servidor del puerto 4173. La QA usa el canal Chromium completo porque el Headless Shell disponible eligió SwiftShader; se registra el nombre real del renderizador.

`denoise_lightmaps.py` filtra únicamente la irradiancia lineal y vuelve a generar los perfiles menores; guarda los EXR crudos por hash en `outputs/lightmaps-raw/`. No modifica el albedo ni el maestro. El informe `denoising.json` enlaza los hashes de entrada y salida. Suprimir el ruido suaviza parte del detalle fino de iluminación, especialmente en islas UV pequeñas.

## Regresión de las correcciones del 4 de octubre

Con Vite iniciado, ejecutar desde `web/`:

```sh
node tests/browser.mjs
node tests/revision.mjs
```

`revision.mjs` usa Chromium completo con ANGLE/Metal en este Mac. Observa ocho intervalos de 18 segundos con escena animada (Alta/Auto, día/noche, cámara quieta/en movimiento), toma muestras de los difusores tras renderizar y comprueba controles táctiles, ratón, entradas combinadas y orientación. No sustituye una prueba en Safari/iPhone físico.

Para revisar geometría y generar vistas ortográficas/cercanas desde el maestro:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b blender/patio_master.blend --python-exit-code 1 --python blender/scripts/review_revision.py
```

`-- --check-only` ejecuta únicamente invariantes, montajes, luces y orientación de caras. `-- --views=top,furniture-egg` limita los renders a esos nombres. El directorio de evidencia conserva la configuración v2 necesaria para comprobar que piscina, cerco y bloque principal no se alteraron.

Para preparar y comprobar la copia local después de QA/producción:

```sh
python3 tools/prepare_delivery.py
python3 tools/check_delivery.py
```

El empaquetador exige informes del mismo hash de maestro, no solo la misma etiqueta de revisión. La comprobación verifica SHA-256 de cada archivo y abre la copia del maestro para resolver sus texturas dentro de la entrega. No publica en Internet. `revision.mjs --interface-only` sirve para diagnosticar controles durante la preparación; no genera el informe temporal requerido para entregar.

### Cambiar el ambiente diurno sin remodelar

Editar `lighting.day` en `config/scene-parameters.json`, ejecutar `.venv/bin/python tools/make_day_sky.py` si cambia el gradiente y abrir el maestro con `Blender -b blender/patio_master.blend --python-exit-code 1 --python blender/scripts/update_daylight.py`. Este paso guarda la fuente y un render de prueba. Después repetir exportación, filtrado, renders, auditoría, build y QA según los comandos anteriores. No mezclar el cielo nuevo con horneados anteriores.
