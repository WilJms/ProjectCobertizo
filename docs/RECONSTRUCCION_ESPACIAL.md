# Revisión espacial de las referencias

Revisión 2026-10-03 motivada por el rechazo espacial del usuario. Se conservan los materiales, controles y funciones, y se sustituye la planta anterior. Todas las cotas siguen siendo inferidas.

## Error anterior

La planta de 10,5 × 10,5 m puso el muro azul en un lateral y extendió el cerco alto por dos lados. El comedor quedó en un brazo de 3,45 × 5,10 m y el ala se extendió transversalmente. Esa interpretación no respetaba la terraza ancha frente al muro azul ni la franja que continúa junto al cerco alto. Las anteriores anotaciones que daban por contrastadas esas proporciones quedan sustituidas por esta revisión.

## Lectura conjunta

- R02 muestra el muro azul transversal, la pantalla baja sobre su mitad derecha y el cerco alto que retorna hacia la cámara. La terraza existente termina antes del cerco, dejando una franja verde lateral.
- R03 muestra esa misma esquina, el paso junto a la casa, la terraza, el césped y el arco de piscina. Se separó la esquina redondeada del césped de las direcciones rectas usadas para estimar la perspectiva.
- R01 mira casi perpendicularmente al cerco y confirma la franja estrecha entre piscina y madera, además de la inflexión del borde visible.
- El video confirma el módulo de pavimento, el ancho de la franja de tumbonas y silla colgante, y el encuentro a escuadra de ambos cierres. No muestra el extremo próximo completo de la piscina.
- D1/D2/D3 y el detalle suplementario gobiernan el deck y las estructuras propuestas. El ala principal se dispone transversalmente; el brazo estrecho continúa junto al cerco. Se preservan las diferencias de las tres cubiertas.

## Método y evidencia

`tools/analyze_spatial_references.py` conserva puntos de lectura en píxeles y genera `outputs/spatial-analysis/spatial-inference.json`, una superposición de R03, un contraste independiente de puntos comunes en R02 y una planta. La reconstrucción usa direcciones largas del suelo/cierres y una cámara pinhole aproximada. No tiene calibración de lente ni medición física.

La proyección se ajusta a relaciones del conjunto. Se descartaron homografías locales de cuatro esquinas de una sola baldosa: pequeñas imprecisiones en las juntas producían errores grandes al extrapolar hasta el muro. No se presentan esos ensayos como calibración válida.

El módulo provisional pasa a 0,45 m. La terraza equivale aproximadamente a 13 módulos de ancho por 6 de fondo; el paso lateral a unos 2 módulos. Son recuentos e interpretación visual con juntas parcialmente tapadas, no dimensiones certificadas. La escala absoluta se puede cambiar conjuntamente.

La planta de trabajo tiene 7,40 m de ancho y 12,30 m hasta el cierre próximo inferido. El deck principal ocupa aproximadamente 5,74 × 2,91 m; el brazo derecho, 1,39 m de ancho hasta 6,15 m desde el fondo. El contorno de agua se traza a partir del arco visible en R03 y se completa hacia la parte no fotografiada. La anchura y longitud completas no tienen la misma certeza que el arco observado.

## Comprobación

Las cámaras `PHOTO_R01_CERCO`, `PHOTO_R02_TERRAZA` y `PHOTO_R03_GENERAL` conservan el formato vertical de las fotografías. Las cinco cámaras existentes mantienen sus IDs y sirven como vistas prácticas del recorrido. `render_spatial_review.py` oculta temporalmente la obra propuesta para comprobar el suelo y los cierres sin ocultaciones de cubierta; no altera el maestro guardado. La pared simplificada de la casa se oculta solo en la cámara R03 para no tapar una pose situada en su borde.

El ajuste de puntos no constituye un porcentaje de fidelidad. Las diferencias de lente, mobiliario temporal, vegetación y cierre próximo no observado se registran por separado de los errores de planta.
