# Supuestos e incertidumbres

No existen medidas reales ni se solicitarán nuevas capturas. Este registro permite inferir y avanzar sin confundir inferencias con observaciones. La confianza describe la evidencia, no una garantía de precisión.

## Registro inicial

| ID | Asunto | Evidencia disponible | Resolución inicial | Confianza / revisión |
| --- | --- | --- | --- | --- |
| A-001 | Escala absoluta | No hay cota conocida ni tamaño confirmado de baldosas. | La configuración ofrece **0,50 m por módulo de baldosa únicamente como semilla de trabajo no medida**. Reestimar con proporciones entre vistas; registrar si se usa y cambiar si resulta incoherente. | Baja; resolver en S01. |
| A-002 | Perímetro completo | Se observan sobre todo terraza, esquina azul y cerco lateral. | Completar lados ausentes con la extensión mínima compatible con el patio y la piscina inferidos. | Baja en zonas ocultas. |
| A-003 | Piscina | Forma curva y parte del borde visibles; contorno total/fondo no documentados. | Inferir contorno coherente, vaso y profundidad visual. No incorporar escalones, lámparas u otros detalles como si fueran observados. | Media en borde visible, baja en resto. |
| A-004 | Alturas y desniveles | Relación visual entre cierres, muebles y proyecto de deck. | Estimar con una única escala y parametrizar. No derivar exactitud de perspectivas amplias. | Baja a media. |
| A-005 | Cubierta clara | Paños claros en D3, apariencia posiblemente translúcida. | Material visualmente difusor y ajustable; no afirmar policarbonato o vidrio real. Comparar luz de día y lámparas de noche. | Baja sobre composición; media sobre apariencia. |
| A-006 | Iluminación nocturna | Propuestas con luces encendidas; no foto real nocturna. | Simular iluminación cálida consistente con las luminarias y las superficies. Intensidades/temperatura son parámetros artísticos estimados. | Baja sobre equivalencia física. |
| A-007 | Recuento de luminarias | Varios puntos visibles y zonas ocultas. | Inventario por categoría y diseño; completar solo lo necesario. El título «Nueve luces» no determina el total. | Variable; resolver en S03/S04. |
| A-008 | Superficies verdes | Césped central irregular y franjas laterales con aspecto de césped artificial. | Materiales separados, preservando juntas y variación. Especie y composición no confirmadas. | Media. |
| A-009 | Mobiliario y maceteros | Se repiten objetos entre video y conceptos con posiciones distintas. | Usar las propuestas para colocación del proyecto y el video para forma/detalle de objetos reconocibles. | Media. |
| A-010 | Apariencia del pavimento en conceptos | Los diseños estilizan el pavimento y el pasto. | Conservar materiales reales salvo superficies sustituidas por la obra nueva. | Alta como regla del proyecto. |
| A-011 | Lado de la casa | Alcance excluye la vivienda; referencias parciales. | Resolver límite sencillo del área recorrible. Si requiere un cerramiento técnico discreto, identificarlo como decisión visual. | Baja para fidelidad de ese encuadre. |
| A-012 | Sol, norte y hora | Cielo nublado en referencias, sin orientación confirmada. | Día de referencia nublado. Cualquier dirección solar usada será una decisión de escena, no dato geográfico. | Baja. |
| A-013 | Detalles posteriores/superiores de cubiertas | Tres vistas conceptuales frontales. | Construcción geométricamente coherente que respete siluetas visibles; componentes ocultos simplificados. | Baja a media. |
| A-014 | Cámara de recorrido | No es una medida del lugar. | Altura inicial de ojos 1,65 m y FOV inicial de 60° como valores de interacción ajustables. | Parámetros de experiencia, no observaciones. |

## Cómo actualizar

Para una medida inferida, registrar valor/unidad, referencia de origen, método, efecto sobre el conjunto y confianza. Una inferencia no cambia a «medida» por haberse usado durante varias sesiones.

Las zonas ocultas pueden permanecer estimadas al final; describirlas brevemente en la entrega. La ausencia de nuevos datos no impide terminar una reconstrucción visual coherente.

Si se cambia escala, hacerlo mediante parámetros comunes y regenerar dependencias pertinentes: alturas, piscina, deck, cámaras, luces y colisiones. Evitar corregir cada diseño a una escala diferente.

## Plantilla de actualización

- ID:
- Valor o hipótesis anterior:
- Valor o hipótesis nueva:
- Origen: observado / inferido / convención / desconocido.
- Referencia y razonamiento breve:
- Confianza:
- Dependencias que se actualizaron:
- Evidencia de revisión:

## Inferencias aplicadas — 2026-10-03

- **A-001 / A-004:** módulo de pavimento adoptado 0,50 m; patio de trabajo 10,5 × 10,5 m, deck 0,22 m, cierres alto 2,65 m y azul 1,70 m. La proporción surge de contar juntas y tramos visibles en R02/R03 y contrastar mobiliario en video. Son convenciones métricas de confianza baja, no cotas medidas.
- **A-002 / A-003:** la parte no visible continúa como cierre sencillo. Piscina curva cerrada, aproximadamente 3,8 × 5,3 m, profundidad 1,4 m y agua a −0,14 m. Borde 0,38 m. Se preserva la inflexión del borde visible; lado lejano y fondo son supuestos. Sin escaleras ni luces sumergidas inventadas.
- **A-004 / A-013:** ala comedor de 5,2 × 3,7 m y ala lateral de 4,9 × 2,1 m. Aleros 2,9/2,7 m; cumbrera D1 4,02 m. Se regularizan encuentros inconsistentes de los conceptos. Confianza media en siluetas, baja en dimensiones.
- **A-007:** inventario propuesto por diseño: 10 focos de techo (6+4), 6 apliques de cerco, 9 luces de contrahuella y 2 luces de maceteros. No se deriva del nombre del archivo. Posiciones y potencias se estiman; no es proyecto eléctrico.
- **A-015:** el archivo adicional de septiembre muestra deck y luminarias coherentes con los conceptos, mientras el video muestra baldosas y césped. Se usa como referencia suplementaria de detalles propuestos, sin atribuirle prueba de obra existente.
- **A-016:** cámaras foto-match aproximadas por contenido y perspectiva. Se registra una pose reproducible, no una calibración fotogramétrica ni ajuste métrico exacto. Las comparaciones Cycles/web sí compartirán proyección y pose.

- **Corrección A-002/A-004 (dos vistas):** muro azul en X=0 y cerco alto en Y=0 del plano; son perpendiculares. Ala izquierda del deck 3,45 × 5,10 m y ala de fondo 6,50 × 1,98 m. Cumbrera D1 ajustada a 3,72 m. Sustituye las cifras provisionales de las alas anteriores. El modelo conserva una única escala.
- **A-017:** cielo y vegetación de continuidad creados proceduralmente. No representan especies, orientación geográfica ni edificios vecinos confirmados. Panel claro: aproximación difusora, con transmisión estática incluida en GI. El agua web aproxima absorción y ondulación; no hay simulación hidrodinámica.

## Revisión espacial prioritaria — sustituye las cotas anteriores

- **A-018 / corrección A-001–A-004:** se descarta la planta cuadrada de 10,5 m y el comedor estrecho/profundo. El muro azul queda transversal en Y=0; el cerco alto retorna por X=7,40. La afirmación anterior de que aquella orientación estaba contrastada fue incorrecta.
- **Escala:** módulo provisional 0,45 m, no medido. Terraza existente ~13 × 6 módulos y paso lateral ~2 módulos. La precisión absoluta es baja; las relaciones visibles tienen mayor apoyo.
- **Deck:** comedor transversal ~5,74 × 2,91 m; ala de 1,39 m de ancho junto al cerco hasta Y=6,15. Derivado de la organización de las tres propuestas sobre la planta real.
- **Piscina:** arco visible trazado sobre R03 con proyección de suelo y contrastado espacialmente con R01. Extremo próximo, fondo y profundidad continúan siendo supuestos. No se usa una elipse aislada colocada por conveniencia.
- **Perímetro:** ancho de trabajo 7,40 m; cierre próximo a 12,30 m por continuidad. La longitud completa no está observada. No se atribuye al video evidencia de una vuelta al patio.
- **Cámaras:** tres cámaras PHOTO conservan el formato vertical; las cinco cámaras del recorrido mantienen sus IDs. La proyección aproximada no corrige distorsión de lente y no equivale a calibración fotogramétrica.
- **A-007 revisado:** seis apliques sobre el cerco alto y dos sobre la pantalla baja se leen en fotos distintas; el inventario pasa a ocho apliques existentes modelados. Se conservan diez focos de cubierta, nueve de contrahuella y dos de maceteros como propuesta.
- Evidencia: `docs/RECONSTRUCCION_ESPACIAL.md` y `outputs/spatial-analysis/`. Maestro y derivados se regeneran juntos para mantener colisiones, cámara e iluminación coherentes.


## Límites conservados al cerrar la revisión

- **A-019:** la escala absoluta continúa sin ancla métrica. Los valores de 7,40 × 12,30 m describen el modelo de trabajo, no una medición del inmueble. La franja visible, los encuentros y el arco observado tienen más apoyo que el cierre próximo y el extremo completo de piscina.
- La cámara pinhole aproximada no corrige distorsión del teléfono. Vegetación sobre el cerco y cielo se simplifican; muebles temporales de las fotos no se añaden al proyecto de cobertizo. Las láminas de comparación muestran estas diferencias explícitamente.
- El agua web conserva una reflexión planar y aproximación de absorción; el acabado de paneles claros no prueba una marca o material. El filtrado del bake y la reflexión PBR pueden diferir de Cycles en sombras pequeñas, brillo y saturación.

### A-020 — Ajustes de proyecto solicitados, no nuevas medidas

- Ala ensanchada 0,30 m de trabajo hacia césped (1,69 m frente a 5,74 m del cuerpo aprobado). A=(5,56;6,15); B=(7,25;7,75786), intersección del lateral con el contorno exterior del borde existente. La diagonal encuentra la franja seca curva, sin entrar en el vaso; el borde y el agua no se alteran.
- Paso de baldosas de 0,90 m desplazado a X=[−1,28;−0,38], dejando 0,50 m hasta la tarima. Acompañan el límite sencillo de casa y la continuidad del muro azul; no es un nuevo levantamiento del patio.
- Son elecciones moderadas de diseño para concretar la instrucción del usuario. Conservan escala, texturas y bloque principal; pueden editarse en configuración.

## A-021 — Día soleado solicitado el 4 de octubre

El usuario sustituye el día nublado de las fotografías por un día soleado. Cielo despejado y dirección solar oblicua desde el frente izquierdo se eligen para leer cubierta, postes, muebles y piscina. No se dispone de orientación geográfica ni hora solar: no se atribuyen a esta iluminación. La geometría sigue siendo la reconstrucción estimada registrada en A-020 y las hipótesis anteriores.
