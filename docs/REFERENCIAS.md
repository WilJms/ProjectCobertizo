# Lectura inicial de las referencias

Estas notas provienen de la revisión de las seis imágenes y de fotogramas a lo largo del video realizada al preparar el paquete. Sirven de orientación; el agente de implementación debe localizar e inspeccionar los archivos efectivamente presentes antes de afirmar que los ha procesado.

Los siete originales son suficientes para iniciar una reconstrucción visual. No se pedirán nuevos recursos. El inventario legible por código es `config/references.json` y las incertidumbres están en `assumptions.md`.

## Inventario

| ID | Nombre original | Tipo y aportación |
| --- | --- | --- |
| `r01_cerco` | `WhatsApp Image 2026-10-01 at 21.35.57 (1)(1).jpeg` | Foto real: cerco alto, tablillas, postes, apliques, pasto y porción del borde de piscina. |
| `r02_terraza` | `WhatsApp Image 2026-10-01 at 21.35.57 (2)(1).jpeg` | Foto real: terraza de baldosas, muro azul, cierre bajo de madera y esquina con el cerco alto. |
| `r03_general` | `WhatsApp Image 2026-10-01 at 21.35.57(1).jpeg` | Foto real: relación general de terraza, césped central, cerco y piscina a la derecha. |
| `v01_recorrido` | `WhatsApp Video 2026-09-26 at 21.01.22(1).mp4` | Video real: detalles de pavimento, muebles, maceteros y lateral de madera. |
| `d1_madera_dos_aguas` | `Nueve luces cálidas en la terraza.png` | Diseño: estructura de madera y cubierta principal a dos aguas, ala derecha baja. |
| `d2_oscuro_cielo_madera` | `Unknown-2.png` | Diseño: estructura oscura, cubierta baja en L y cielo de madera. |
| `d3_oscuro_paneles_claros` | `Unknown(1).png` | Diseño: estructura oscura, paños claros y travesaños vistos. |

Las fotografías disponibles tienen 960 × 1280 píxeles; los diseños, 1536 × 1024. Estos tamaños no son cotas físicas. Los acentos del nombre de D1 pueden estar codificados de formas Unicode distintas; normalizar para comparar, sin modificar los originales. Los hashes del manifiesto permiten identificar copias sin depender únicamente del nombre.

## Patio existente

El césped central presenta variación, zonas ralas y bordes irregulares. Las franjas junto al cerco y las tumbonas parecen artificiales y tienen algunas juntas visibles; conservar la distinción como hipótesis.

El pavimento son módulos cuadrados de árido visto, con juntas oscuras y variación. La superficie del muro azul tiene estuco rugoso. El remate de madera y la altura visible del muro cambian entre tramos.

El cerco alto tiene tablas horizontales, postes verticales, nudos y diferencias de color. Hay separaciones pequeñas por donde entra luz. Los apliques existentes se ven grises y apagados en las referencias reales.

La piscina tiene borde beige y contorno curvo parcialmente visible. No se documentan el contorno total, fondo, profundidad ni acceso completo. Se ve una pequeña pieza cuadrada junto al borde; reproducir su apariencia sin atribuirle una función no confirmada.

El video y las fotos no muestran exactamente la misma colocación del mobiliario. Las herramientas y mesa temporal de algunas fotos no forman parte de la propuesta final. Para objetos reconocibles, usar el video como detalle y las imágenes de diseño como disposición prevista.

## Diferencias entre los diseños

### D1 — Madera y techo principal a dos aguas

La estructura de madera es visible: postes, vigas, diagonales y cercha frontal. Hay un sector principal alto sobre el comedor y otro más bajo a la derecha. Bases y herrajes tienen acabado oscuro. Preservar silueta, espesores aparentes y encuentro de las cubiertas.

### D2 — Estructura oscura y cielo de madera

La cubierta forma una L baja, casi plana desde la cámara del concepto. Postes y vigas tienen acabado oscuro. El cielo muestra tablillas de madera. No afirmar pendiente cero; resolver una geometría coherente con la imagen.

### D3 — Estructura oscura y paños claros

Los paños claros se organizan entre perfiles oscuros visibles. Su apariencia puede sugerir difusión/translucidez, pero no identifica una composición material específica. Calibrar el equivalente visual con las referencias y documentarlo.

### Elementos que se repiten

Deck elevado en L, comedor con sillas rojas, silla colgante con soporte, tumbona, maceteros y varios tipos de iluminación. Compartir geometría únicamente cuando las variantes definitivas mantengan forma y posición.

## Información del video por tramos

Duración aproximada revisada: 19,70 s. Comprobar la duración del archivo local al procesarlo.

| Tiempo aproximado | Evidencia visual |
| --- | --- |
| 0–4 s | Baldosas y juntas, borde con pasto, maceteros y textura azul. |
| 6 s | Mesa de vidrio, sillas rojas y parasol. |
| 8–12 s | Silla colgante, esquina, pavimento y franja verde lateral. |
| 14–16 s | Encuentro del muro azul con el cerco, maceteros y franjas laterales. |
| 18–19,2 s | Tumbonas, parasol, cerco y porción pequeña de piscina a la derecha. |

El video no constituye un levantamiento completo del perímetro ni una vuelta a la piscina. Tampoco aporta referencia real nocturna. Extraer cuadros representativos con sus tiempos reales; ajustar el muestreo a la nitidez y al contenido.

## Conflictos visuales que resolver

- El pasto de los diseños parece de hojas más anchas y más uniforme que el real.
- Los dibujos del pavimento y borde de piscina están estilizados en los conceptos.
- Las vistas conceptuales tienen formato horizontal y las fotos, vertical. No exigir alineamiento de sus bordes de imagen como si fueran la misma cámara sin recorte.
- Puede haber encuentros de cubierta o espesores ambiguos en vistas únicas. Resolver continuidad 3D sin deformar las siluetas reconocibles.
- El nombre del archivo de luces no determina un inventario técnico de todas las categorías.

## Uso de los originales

Mantener los bytes de origen sin cambios. Escribir fotogramas, recortes de análisis y derivados en `outputs/`. No sustituir una referencia por un retoque generativo ni presentar una imagen de diseño como render generado por el proyecto.

## Inspección de archivos efectivos (2026-10-03)

Se inspeccionaron las siete imágenes y los siete cuadros representativos del video. El inventario actualizado contiene ocho originales. Los nombres efectivos y hashes están en `config/references.json`; D3 es `Unknown.png` y las fotos no llevan el sufijo adicional `(1)` del inventario preparatorio.

La imagen adicional `WhatsApp Image 2026-09-26 at 21.06.39.jpeg` aporta primer plano del deck, silla colgante, sillas rojas, mesa y luces. Su aspecto coincide con la propuesta y contradice el pavimento sin deck del video; se trata como detalle de diseño de procedencia no confirmada, no como constatación de deck construido. Los cuadros muestran claramente árido visto fino, pavimento en módulos, esquina azul, franjas artificiales, maceteros grises, mesa metálica con vidrio texturado, dos tumbonas y silla de trama abierta.
