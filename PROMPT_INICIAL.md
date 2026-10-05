# Encargo: reconstrucción del patio en Blender y recorrido web fiel

Trabaja como responsable de este proyecto en Codex con Astra. Quiero que implementes una reconstrucción 3D del patio de mis referencias, con tres propuestas de cobertizo, y una aplicación web para recorrerlo libremente. Desarrolla, ejecuta, revisa visualmente y corrige el proyecto hasta alcanzar los criterios de entrega. Usa los archivos de esta carpeta como documentación de trabajo y mantén el progreso actualizado.

## 1. Resultado que quiero

Una escena maestra editable en Blender que represente todo el patio, la piscina, los suelos, los cierres y los elementos visibles relevantes, junto con las tres propuestas de construcción. La casa no se incluye en el modelado detallado.

De esa escena debe derivarse una web con Three.js, TypeScript y Vite, preparada para GitHub Pages. Debe permitir caminar por las zonas transitables, mirar libremente, elegir cualquiera de los tres diseños y alternar entre día con luces apagadas y noche con luces encendidas.

La prioridad es el realismo y la fidelidad visual: proporciones, espacio, geometría, materiales, detalles, iluminación y agua. La versión web debe acercarse lo más posible a los renders de referencia de Blender manteniendo una interacción utilizable. Conservar una versión de calidad alta y adaptar la calidad a dispositivos menos capaces.

## 2. Restricción definitiva de referencias

**Estas imágenes y este video son todos los recursos del lugar que tengo. No dispongo de más fotografías, planos ni dimensiones. No me pidas que los consiga y no bloquees el proyecto por esa ausencia.**

Localiza las referencias en `references/`; si las dejé en otra carpeta dentro del proyecto, localízalas allí y actualiza las rutas. No accedas a archivos externos al proyecto sin una razón autorizada. Conserva los originales.

Tienes autorización para estimar dimensiones, ajustar perspectivas y completar de manera conservadora lo que no se ve. Debes registrar qué es observado, inferido o supuesto. El resultado tendrá una escala estimada coherente y editable; no afirmes precisión métrica medida ni inventes medidas como hechos.

La autoridad visual se reparte así:

- Fotografías y video: estado existente del patio, materiales y relaciones espaciales.
- Tres diseños: intención de la construcción nueva, deck, mobiliario y luces.
- Proporciones inferidas: se contrastan entre todas las vistas compatibles.
- Zonas ocultas: se resuelven con continuidad razonable, sin añadir elementos llamativos que no tengan referencia.

Los diseños modifican visualmente algo del pasto, el pavimento y el borde de la piscina. Conserva la identidad real de esas superficies donde la obra propuesta no las sustituya. Las imágenes conceptuales no son planos y pueden tener inconsistencias de perspectiva o encuentros.

## 3. Identidad del patio y de las alternativas

Conserva el cerco de tablillas horizontales de madera y sus postes, el muro azul con relieve, las baldosas de árido visto y sus juntas, el césped central con variaciones, las franjas laterales diferenciadas, el borde beige curvo de piscina y la relación entre terraza, pasto y agua.

Reconstruye el contorno completo de la piscina y el resto del patio a partir de lo visible. Donde no haya información, utiliza la solución más sencilla y compatible con las vistas; registra esa parte como estimada. No hay referencia suficiente para confirmar fondo, escalones o profundidad de piscina: resuelve lo necesario para un resultado plausible sin presentarlo como observado.

Mantén estos identificadores de diseño:

| ID | Referencia e interpretación |
| --- | --- |
| `d1_madera_dos_aguas` | `Nueve luces cálidas en la terraza.png`: madera vista, cubierta principal a dos aguas, cercha y diagonales visibles, ala derecha de cubierta baja, herrajes oscuros. |
| `d2_oscuro_cielo_madera` | `Unknown-2.png`: postes y vigas oscuros, cubierta baja en L y cielo de tablillas de madera. |
| `d3_oscuro_paneles_claros` | `Unknown(1).png`: estructura oscura, cubierta baja en L y paños claros entre travesaños. Apariencia translúcida por aproximar, sin afirmar un material comercial concreto. |

Las tres propuestas tienen una organización parecida con deck elevado, comedor de sillas rojas, silla colgante, tumbona y maceteros. Comparte los elementos que coincidan realmente y separa lo que cambie. Cada alternativa debe tener geometría propia, no solo otro color.

No derives el número total de luminarias del nombre «Nueve luces». Haz un inventario de los puntos visibles y una distribución coherente de los no visibles. No añadas luces interiores de piscina como si su existencia estuviera confirmada.

Resuelve de manera sencilla el límite del lado de la casa y la vegetación visible sobre los cierres. Mantén la navegación dentro del patio modelado; no desarrolles una vivienda ni un entorno ajeno al encargo.

## 4. Método de reconstrucción y precisión visual

Empieza comprobando el entorno de ejecución: Blender, herramientas de Python, Node, procesamiento de video y navegador disponibles. Verifica la capacidad de ejecutar `bpy` dentro de Blender y generar un archivo e imagen de prueba. Identifica si el render puede usar GPU; si no, utiliza una ruta CPU viable y registra sus límites. No presupongas herramientas o capacidades que no hayas probado.

Inspecciona las imágenes y extrae fotogramas útiles del video, evitando tratar muchos fotogramas casi iguales como evidencia independiente. La reconstrucción principal será paramétrica y asistida por imágenes. Usa fotogrametría únicamente si una prueba concreta aporta información; no dependas de ella para continuar.

Construye una base sencilla con terreno, piscina, pavimento, cierres y volúmenes de los cobertizos. Usa un sistema de coordenadas y una escala comunes. Estima proporciones con las juntas del pavimento, muebles y relaciones entre vistas; no des por conocido el tamaño de un objeto reconocible.

`config/scene-parameters.json` contiene una semilla opcional de escala y campos pendientes. Los valores `null` representan trabajo de inferencia para ti, no solicitudes de datos al usuario. Completa los campos necesarios antes de generar el modelo correspondiente y registra la procedencia de cada estimación relevante.

Crea cámaras de comparación para las fotografías. Distingue focal, posición y distorsión de cámara de las dimensiones del patio. También revisa el modelo desde vistas no coincidentes con las referencias para comprobar que sea coherente en 3D. Las vistas de diseño tienen otro encuadre y no deben forzar deformaciones del patio ya coherente con las fotos.

## 5. Prueba temprana de fidelidad Blender/web

En cuanto exista la base geométrica, realiza una escena piloto con madera, muro azul, pavimento, deck, una luminaria, paños claros de cubierta y un sector de piscina. Produce pares Cycles/navegador con cámara, encuadre y estado equivalentes, de día y noche.

Utiliza esa prueba para elegir el reparto de iluminación horneada y dinámica, la representación del agua, el formato de lightmaps y el tratamiento de color. Corrige las diferencias importantes antes de extender el método al patio completo. No esperes a terminar una escena pesada en Blender para comprobar por primera vez su adaptación al navegador.

Mantén Blender como fuente maestra durante todo el proyecto. La versión optimizada se deriva de ella; cualquier simplificación o shader especial debe conservar una correspondencia documentada.

## 6. Materiales, detalle y agua

Modela con geometría lo que afecte a contornos, encuentros, huecos y sombras: vigas, postes, diagonales, espesores de cubierta, bordes del deck, herrajes visibles y muebles relevantes. Usa texturas y normales para el detalle fino que no necesite volumen propio.

Presta atención a escala de veta, juntas, separación de tablillas, variación entre piezas, acabado de madera nueva frente a cerco existente, rugosidad de pintura oscura, relieve del estuco, tamaño del árido y diferencias entre las superficies verdes. Evita materiales uniformes que borren la identidad del patio.

Los materiales procedurales de Blender se hornean o adaptan a representaciones compatibles con glTF/Three.js. El color base debe estar libre de sombras o reflejos de una única fotografía. Conserva color, rugosidad, normales y los canales necesarios sin sobredimensionar todas las texturas de forma indiscriminada.

Puedes usar recursos externos adecuados y con licencia compatible si el entorno permite obtenerlos. Registra su procedencia y licencia. No compres recursos ni contrates servicios. Si una descarga falla, prepara una alternativa local razonable y documenta el efecto visual.

La piscina necesita vaso, borde, nivel de agua, profundidad aparente, ondulación discreta y reflejos del entorno y las luminarias. Desarrolla una solución de agua adecuada a cada perfil de calidad y verifica su aspecto al mover la cámara. No congeles reflejos de una cámara dentro del albedo.

## 7. Seis estados de iluminación coherentes

Implementa los modos `day` y `night` para cada diseño. El día puede partir de la luz nublada visible en las referencias. La noche será una simulación visual del proyecto, ya que no hay una captura nocturna real.

Para cada combinación guarda geometría activa, materiales afectados, lightmaps, ambiente, luces/emisivos, reflejos, exposición y colisiones. Comparte recursos comunes cuando sea correcto. Cambiar un poste o una cubierta también cambia iluminación sobre pavimentos y muros que conservan su geometría.

El manifiesto previsto es `web/public/assets/scene-manifest.json`. Debe asociar explícitamente los mapas de iluminación a identificadores estables de malla y al canal UV correcto. No supongas que glTF exporta automáticamente los lightmaps de Cycles ni que AO equivale a iluminación global.

Como hipótesis inicial, estudia hornear en Cycles la iluminación difusa estática de cada estado y mantener reflejos/especular y agua en tiempo real. La prueba temprana puede justificar otro reparto. Declara qué contribuciones están horneadas y cuáles se añaden en el navegador, incluyendo la iluminación difusa del HDRI. Evita duplicar luz, color base, oclusión y tone mapping.

En día deben apagarse emisivos y aportaciones de las luminarias. En noche deben iluminar de forma consistente las superficies cercanas, además de verse encendidas. La cubierta clara debe afectar la iluminación conforme a la hipótesis material elegida.

Usa un pipeline de color explícito. AgX puede ser un punto de partida, pero no asegura igualdad entre motores. Calibra exposición, entorno, espacios de color y salida. Preserva el rango y la interpretación de los lightmaps; no trates una imagen final con tone mapping como iluminación lineal.

## 8. Interacción, rendimiento y web

Implementa desplazamiento y mirada libres en computador y controles táctiles en móvil/tablet. Añade colisiones con cierres, postes y mobiliario principal, tratamiento de desniveles y límite de piscina. Las vistas guardadas complementan el recorrido libre y permiten comparar; no lo sustituyen.

Al cambiar de diseño o momento del día, carga primero los recursos necesarios y activa el nuevo estado de forma coherente. Conserva la cámara. Si una nueva colisión ocupa la posición del visitante, reubícalo en un punto transitable próximo. Evita luces, sombras o reflejos residuales del estado anterior.

Ofrece perfiles `high`, `balanced` y `low`, con selección manual y ajuste automático fundamentado en rendimiento. Prioriza la mejor fidelidad que el equipo pueda sostener. Establece presupuestos de descarga, memoria y complejidad después de medir el prototipo. Como objetivos de referencia, aspira a 60 FPS en escritorio capaz y 30 FPS en un móvil representativo; no los presentes como resultados medidos antes de comprobarlos.

Usa carga por estados, reutilización y liberación de recursos. Evalúa KTX2/Basis para texturas y Meshopt o Draco para geometría, con decodificadores compatibles. Comprueba aparte el formato y la precisión de lightmaps HDR.

La ruta inicial es Three.js/WebGL 2. Otras rutas solo se incorporan si aportan una mejora comprobada sin comprometer la entrega. Ante falta de soporte 3D, permite ver renders de referencia y describe honestamente esa modalidad; no afirmes que ofrece la misma navegación.

La interfaz debe ser discreta, en español, con selectores de diseño, día/noche, calidad, controles y reinicio. Evita que una interfaz decorativa o efectos de postprocesado excesivos resten atención al patio. Mantén profundidad de campo desactivada durante la navegación normal.

## 9. Entregables y publicación

Entrega el archivo `blender/patio_master.blend`, scripts de construcción/exportación y configuración, recursos necesarios, aplicación completa en `web/`, build de producción en `web/dist/`, preparación de GitHub Pages, renders Cycles, capturas de navegador y comparaciones visuales.

Incluye documentación con comandos realmente comprobados para regenerar, hornear, exportar, ejecutar y construir. Fija versiones y archivo de bloqueo de dependencias.

Comprueba la aplicación con el prefijo de ruta de un sitio de proyecto de GitHub Pages. Las rutas de modelos, texturas y decodificadores deben respetar la base de despliegue. No publiques los originales de trabajo ni el `.blend` como dependencias del recorrido.

Si existe un repositorio/destino configurado, con acceso y autorización para publicar, completa el despliegue y verifica la URL. Si faltan esos datos, termina la entrega local y el workflow, registra `publish_ready` y pide únicamente lo imprescindible para publicar. No inventes una URL ni marques publicación como completada sin verificarla.

## 10. Forma de trabajar y criterio de finalización

Lee inicialmente `AGENTS.md`, `progress.md`, el plan y la guía de referencias. Consulta los documentos técnicos pertinentes cuando los necesites. Adapta el plan con criterio si una prueba lo justifica y registra las decisiones; las fases sirven para organizar la ejecución, no para detenerte a pedirme aprobación entre tareas ordinarias.

Puedes crear y corregir archivos del proyecto, ejecutar renders/pruebas locales y mejorar lo necesario para completar este encargo dentro de los permisos disponibles. Conserva trabajo existente y respeta las restricciones del entorno. Las fotografías faltantes y las medidas desconocidas son incertidumbres aceptadas, no bloqueos. Un permiso o una herramienta realmente inaccesible se informa con precisión y con lo que sí pudiste completar.

Actualiza `progress.md` al cerrar un hito o antes de una interrupción: archivos existentes, comandos ejecutados, evidencia visual, defectos pendientes, bloqueos reales y siguiente acción concreta. No marques un render como revisado si solo generaste código; no confundas una pantalla emulada de móvil con una prueba de rendimiento en un teléfono real.

La entrega debe superar las comprobaciones pertinentes de `docs/VALIDACION.md`: coherencia espacial estimada, identidad de las tres propuestas, seis estados, calidad de materiales y agua, comparación Blender/web, navegación y carga de producción. Una vez cubiertos los riesgos concretos y corregidos los defectos importantes, entrega los resultados sin prolongar pruebas que ya no cambian la conclusión.

**Empieza ahora por localizar e inspeccionar las referencias y verificar el entorno. Después ejecuta las fases de `plan.md` y continúa hasta la entrega completa que permitan los recursos y accesos disponibles.**
