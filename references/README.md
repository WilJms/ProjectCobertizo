# Añade aquí tus referencias

Copia los tres JPG/JPEG reales, las tres imágenes PNG de diseño y el MP4 en esta carpeta. Los nombres originales pueden mantenerse. El inventario de nombres y hashes está en `../config/references.json` y la lectura visual inicial en `../docs/REFERENCIAS.md`.

No hacen falta fotografías nuevas ni dimensiones. Los parámetros ausentes serán estimados por el agente y quedarán documentados.

Si has cambiado los nombres, el agente debe identificarlos por contenido y, cuando coincidan los bytes, por hash. Los nombres con acentos pueden usar distintas normalizaciones Unicode. Registrar las rutas encontradas sin alterar originales.

Los originales no se incluyen en este paquete ni deben copiarse automáticamente al build público. El `.gitignore` inicial conserva este README y excluye el resto de esta carpeta del seguimiento ordinario; los archivos siguen disponibles localmente para Blender y Codex.
