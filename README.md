# Patio · Tres cobertizos

Reconstrucción editable en Blender y recorrido Three.js/TypeScript/Vite. Tres estructuras distintas, día soleado/noche, movimiento libre, controles táctiles y calidad adaptable.

La planta fue revisada con las fotografías y el video: terraza ancha frente al muro azul, ala estrecha junto al cerco alto y piscina trazada sobre su arco visible. Las dimensiones son estimaciones visuales. El cierre próximo, el extremo no visible de piscina y la profundidad se completan por continuidad. Consulta `docs/RECONSTRUCCION_ESPACIAL.md` y `assumptions.md`.

La revisión del 4 de octubre mantiene el bloque principal y la piscina, corrige el extremo diagonal, distribuye las luces bajas como 3+3+3+0 y añade un selector compacto con navegación táctil explícita. Detalles y pruebas: `docs/REVISION_2026-10-04.md`.

## Ejecutar la web

```sh
npm ci --prefix web
npm run dev --prefix web
```

Abrir http://127.0.0.1:5173/ProjectCobertizo/. Arrastrar para mirar y usar W A S D para caminar; en pantalla táctil, pulsar Caminar y usar la palanca izquierda; Salir termina ese modo. Hay cinco vistas guardadas, tres propuestas, selector día/noche, calidad automática/manual y reinicio.

```sh
npm run build --prefix web
python3 tools/serve_production.py
```

Producción local: http://127.0.0.1:4173/ProjectCobertizo/. La carpeta `web/dist/` es el sitio estático; no se abre mediante `file://`.

## Archivos principales

| Ruta | Contenido |
| --- | --- |
| `blender/patio_master.blend` | Maestro editable, fuentes, variantes, luces y cámaras. |
| `blender/scripts/` | Construcción, actualización derivada, exportación, render y validación. |
| `blender/textures/` | Texturas originales generadas localmente. |
| `config/scene-parameters.json` | Dimensiones inferidas, planta, posiciones y cámaras. |
| `web/src/` | Aplicación, navegación, colisiones, carga y materiales web. |
| `web/public/assets/` | GLB Meshopt, mapas EXR lineales, entornos y renders. |
| `outputs/spatial-analysis/` | Lecturas, planta, superposiciones y vistas del patio existente. |
| `outputs/comparisons/` | Comparaciones entre referencias, Blender y navegador. |
| `outputs/validation/` | Informes ejecutados; alcance y límites de las pruebas. |
| `docs/OPERACION.md` | Comandos para editar, regenerar, ejecutar y validar. |
| `progress.md` | Estado real de la entrega y pendientes. |

## Entrega local y GitHub Pages

El usuario se encargará de crear el repositorio y publicar. Esta carpeta es la copia organizada para trasladar a un repositorio; no incluye entornos virtuales, `node_modules` ni el historial de pruebas descartadas. Los originales están fuera de los recursos de la web.

El workflow `.github/workflows/pages.yml` construye `web/`, deduce el prefijo del nombre del repositorio y publica solamente `web/dist/`. Al trasladarlo, seleccionar GitHub Actions como origen de Pages y conservar la rama `main` o adaptar el workflow. No se ha ejecutado publicación remota.

## Escala y correspondencia

Blender es la fuente maestra. Los parámetros de planta usan X hacia la derecha e Y hacia la casa; Blender recibe `(X, -Y, Z)` y la exportación glTF produce `(X, Z, Y)`. Las tres variantes conservan IDs y las superficies comunes tienen iluminación propia para cada uno de los seis estados.

El difuso directo e indirecto se hornea en Cycles sin albedo, en OpenEXR lineal de 16 bits flotantes. La web aplica ese difuso una vez y calcula especular y agua en tiempo real. El modo de imágenes ofrece renders cuando no se puede iniciar WebGL2.

Las pruebas de pantalla táctil son emulación sobre el Mac disponible, no mediciones de un teléfono físico. Los informes distinguen compilación, navegador, render y revisión visual.
