# Reglas del proyecto

## Objetivo

Reconstruir el patio de las referencias en Blender y derivar una web Three.js/Vite para GitHub Pages: tres cobertizos, día/noche, recorrido libre y máxima fidelidad visual viable. El encargo completo está en `PROMPT_INICIAL.md`.

## Reglas permanentes

- Solo existen las referencias aportadas. No solicitar más fotos, planos o medidas. Inferir lo necesario y registrarlo en `assumptions.md`; nunca presentar una escala estimada como levantamiento métrico.
- Fotos/video gobiernan el patio existente; diseños gobiernan la obra nueva. Conservar identidad, proporciones y materiales del lugar. La casa queda fuera del modelado detallado.
- Blender es la fuente maestra. Validar pronto una muestra Cycles/web y conservar correspondencia entre ambas versiones.
- Mantener IDs de diseños, cámaras y mallas. Las seis combinaciones de diseño/iluminación incluyen sombras y rebotes correctos sobre superficies compartidas.
- No duplicar contribuciones horneadas y dinámicas, incluida la luz difusa del ambiente. No tratar AO como GI ni un render con tone mapping como lightmap lineal.
- El recorrido es libre; vistas guardadas y renders son complementos. Preservar cámara y colisiones coherentes al cambiar diseño.
- Priorizar fidelidad con calidad adaptable y medir en dispositivos realmente disponibles. Diferenciar pruebas físicas, emulación y comprobaciones estáticas.
- Continuar trabajo local reversible y pruebas pertinentes dentro de los permisos disponibles, sin pedir aprobación al usuario entre fases ordinarias. Respetar accesos y conservar trabajo existente.
- Informar únicamente bloqueos reales. No comprar recursos o servicios ni afirmar publicación sin destino, acceso y autorización aplicables.
- Mantener `progress.md` al cerrar hitos o interrumpir: evidencia real, pendientes y siguiente acción. No inventar resultados de Blender, navegador o despliegue.

## Dónde consultar

- Inicio/reanudación: `progress.md` y la fase correspondiente de `plan.md`.
- Referencias y decisiones espaciales: `docs/REFERENCIAS.md`, `assumptions.md`, `config/scene-parameters.json`.
- Exportación, materiales, iluminación o web: `docs/PIPELINE.md`.
- Cierre de un riesgo o fase: comprobaciones pertinentes de `docs/VALIDACION.md`.
- Cambios de criterio: `decisions.md`. Fuentes técnicas: `docs/FUENTES.md`.

Consultar según la tarea; no releer todos los documentos antes de cada edición. Estas reglas no sustituyen las instrucciones del usuario ni los permisos del entorno.
