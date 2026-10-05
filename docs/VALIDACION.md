# Validación visual, técnica y de uso

**Revisión ejecutada: 2026-10-04, v3 con día soleado.** Validación local completada con las limitaciones registradas al final. Dispositivo móvil físico y despliegue remoto: `not_run`. Las cifras objetivo siguen siendo metas, no garantías.

Registrar en `progress.md` fecha, versiones, procedimiento, evidencia en `outputs/`, resultado (`not_run`, `pass`, `fail`, `blocked`) y limitación. Declarar éxito solo tras ejecutar. Consultar `docs/PIPELINE.md` y `docs/FUENTES.md`.

## 1. Distinguir niveles de evidencia

| Evidencia | Qué demuestra | Qué no demuestra |
|---|---|---|
| Revisión de código | Contratos e implementación presentes | Que ejecuten correctamente |
| Comprobación estática/compilación | Tipos y paquete compilable | Calidad visual o navegación |
| Ejecución de Blender | Scripts y escena generados | Parecido o exportación correcta |
| Render Cycles inspeccionado | Apariencia del maestro desde esa cámara | Apariencia web |
| Navegador real automatizado o manual | Carga y funcionamiento en ese entorno | Funcionamiento en otro hardware |
| Emulación móvil | Diseño y eventos táctiles simulados | GPU, memoria o fluidez de un celular real |
| Dispositivo físico | Comportamiento del equipo probado | Compatibilidad con todos los dispositivos |
| URL publicada comprobada | Despliegue accesible observado | Que un build local ya estuviera publicado |

Sin teléfono físico, esa comprobación queda `not_run`; no bloquea entregar declarando el alcance probado.

## 2. Referencias y escala

- Verificar `config/references.json` y `docs/REFERENCIAS.md`. Distinguir fotografías, fotogramas y diseños conceptuales.
- Comparar distribución, piscina, cierres, pavimentos y mobiliario con las evidencias disponibles. Los diseños gobiernan la construcción nueva; no deben reemplazar accidentalmente materiales reales del patio.
- Contrastar dos vistas antes de corregir proporciones. Registrar estimaciones en `config/scene-parameters.json` y `assumptions.md`.
- Revisar contorno completo de piscina, continuidad del perímetro, cambios de nivel y cierre del lado de la casa. Identificar las zonas inferidas; no atribuirles exactitud medida.

## 3. Cámaras y comparaciones

Las tres cámaras `PHOTO_R01_CERCO`, `PHOTO_R02_TERRAZA` y `PHOTO_R03_GENERAL` comparan la reconstrucción con las fotografías verticales. `CAM01_GENERAL`, `CAM02_MURO_AZUL` y `CAM03_CERCO` conservan IDs y contenido relacionado, con encuadres prácticos para el recorrido. `CAM04_BAJO_CUBIERTA` y `CAM05_PISCINA` inspeccionan zonas críticas; no representan observaciones adicionales del sitio.

Para cada par Cycles/web guardar cámara, proyección, resolución, aspecto, recorte, estado, exposición y tiempo de animación del agua. Comprobar la transformación de Blender Z-up a glTF/Three.js Y-up con puntos conocidos; no aplicar dos veces una conversión ya hecha por el exportador. Igualar la proyección, no solo copiar un número de distancia focal.

Comparar fotografías con el maestro para evaluar reconstrucción; comparar maestro con navegador para evaluar exportación. Capturar una vista general equivalente de los seis estados, cada cubierta de cerca y agua de día/noche. Añadir vistas cuando una discrepancia concreta lo necesite.

Inspeccionar siluetas, perspectiva, texturas, sombras, brillo, reflejos y color. No exigir igualdad píxel a píxel ni inventar porcentajes de fidelidad. Usar capturas de Blender y navegador; ninguna mejora generativa, retoque o imagen de diseño puede sustituirlas.

## 4. Matriz obligatoria de estados

| Diseño | Día | Noche |
|---|---|---|
| `d1_madera_dos_aguas` | `day`: `pass` | `night`: `pass` |
| `d2_oscuro_cielo_madera` | `day`: `pass` | `night`: `pass` |
| `d3_oscuro_paneles_claros` | `day`: `pass` | `night`: `pass` |

Verificar estructura, cubierta, luminarias, sombras, mapas de iluminación, entorno, reflejos y colisiones. De día, emisión y aportación de luminarias apagadas; de noche, ambas coherentes. La noche es una simulación, no una observación del lugar.

## 5. Materiales, iluminación y exportación

- Revisar `web/public/assets/scene-manifest.json`: seis estados, identificadores estables, recursos existentes, superficies afectadas y correspondencias de UV. Comprobar el `TEXCOORD_n` exportado y el canal utilizado por la versión instalada de Three.js; no asumir nombres equivalentes.
- Verificar UV de materiales y de iluminación, márgenes, ausencia de solapamientos indebidos y costuras. Los elementos compartidos reciben el mapa del estado activo cuando cambia su iluminación.
- Registrar si cada horneado contiene iluminación directa, indirecta, albedo o AO. Comprobar su composición con luz dinámica, entorno y oclusión para impedir duplicaciones.
- Confirmar espacios de color, rango dinámico, decodificación y exposición. No hornear AgX dentro de mapas físicos ni aplicar transformaciones de visualización dos veces. Tener AgX en ambos motores no prueba equivalencia automática.
- Inspeccionar veta, árido, rugosidad, juntas, normales, bordes y repetición cercana. Confirmar que geometría necesaria para siluetas no se sustituyó por un mapa plano.
- En agua, comprobar profundidad aparente, fondo, borde, reflejos y transición nocturna desde distintos ángulos. En paneles claros, comprobar caras, espesor, sombras y transmisión estimada sin suponer vidrio confirmado.

## 6. Interacciones y estabilidad

Recorrer el perímetro y las zonas bajo cubierta; probar teclado/ratón, reinicio, vistas y controles táctiles. Comprobar muros, postes, muebles, escalones y límite de piscina. La cámara no atraviesa obstáculos ni queda atrapada.

Cambiar entre todos los diseños y estados desde ubicaciones distintas, incluyendo una ocupada por un poste del diseño entrante. Mantener pose cuando sea válida y reubicar solo lo necesario cuando no lo sea. Probar cambios rápidos, recursos en carga, error de descarga y retorno a un estado válido. Nunca mezclar geometría de una variante con iluminación de otra.

Revisar orientación, legibilidad y áreas táctiles; evitar desplazamiento accidental de página al caminar. Inspeccionar consola y red. Repetir cambios para detectar crecimiento persistente de memoria, sin confundir caché deliberada con una fuga.

## 7. Calidad y rendimiento

Medir primero en S02 y fijar presupuestos revisables por `high`, `balanced`, `low` en la configuración. Registrar equipo, navegador, resolución, DPR, FPS/tiempos de cuadro, carga inicial, bytes transferidos, texturas, triángulos, llamadas de dibujo y memoria estimada. Separar memoria calculada de memoria realmente observada.

Objetivos iniciales: 60 FPS en escritorio capaz y 30 FPS en móvil representativo. Mantener `high` cuando el equipo lo permita y conservar selector manual. Optimizar costes identificados; no degradar materiales o geometría para cumplir cifras arbitrarias. Probar texturas y geometría comprimidas contra las originales antes de aceptarlas.

## 8. Producción y cierre

Comprobar instalación reproducible, compilación y recorrido desde `web/dist/` servido bajo una ruta de proyecto. Verificar rutas base, GLB, mapas, decodificadores, licencias y límites vigentes de Pages. El workflow debe corresponder a la estructura real.

Guardar resultados y discrepancias. La entrega local validada, con build y workflow preparados, puede marcarse `publish_ready`; una publicación ejecutada y comprobada permite afirmar que la web es accesible. Entregar comandos, ubicación del maestro y límites de las pruebas; no presentar verificaciones pendientes como éxitos.


## Resultado ejecutado de v3 soleado

Todos los informes de navegador, regresión y producción identifican el mismo maestro `ca9df64c8d2134e8b27b01cdc38b623411fca929a3e99c11b3c7feb9ebca6592`. La revisión fotográfica v2 sigue siendo antecedente de la reconstrucción, y las modificaciones posteriores están en `docs/REVISION_2026-10-04.md`.

| Comprobación | Resultado | Evidencia y alcance |
| --- | --- | --- |
| Geometría y conservación | pass | Rectángulo principal, 112 vértices de piscina, borde y cerco idénticos al estado aprobado. Ala de 1,69, A/B y dos bases interiores; 273 sólidos coherentes, cuatro sillas orientadas hacia la mesa, respaldo unido y cabios sin atravesar la cubierta. `revision-2026-10-04/geometry-checks.json`. |
| Luces bajas | pass | Exactamente 3+3+3+0, centros al 25/50/75 %, nueve difusores separados de carcasa. |
| UV y exportación | pass | Siete atlas sin degenerados ni solapamientos detectados en raster 512 px; cuatro GLB Meshopt, UV1 y 90 EXR HALF/ZIP presentes. 30 atlas filtrados con trazabilidad. |
| Sol y luces artificiales | pass | Un SUN natural de día, cero de noche; 0/35 fuentes artificiales y emisión 0/5. Directa e indirecta solares horneadas por propuesta, sin segundo difuso web. |
| Cámaras y vistas | pass | Seis pares generales Cycles/web con posición, FOV, aspecto 1,5 y agua t=0 verificados; vistas cercanas y superiores inspeccionadas. |
| Página y controles | pass | Identidad, contenido, ausencia de overlay, WASD, arrastre, cambios rápidos, pose conservada, reubicación junto a poste, Reintentar, caché de dos estados y fallback. Nueve comprobaciones generales. |
| Temporal | pass | Ocho intervalos de 18 s en D2: Alta/Auto × día/noche × quieto/caminando. Estado, raíces y emisivos estables; las nueve muestras de difusores no variaron con cámara quieta. `revision-report.json` y `temporal-high-auto.webm`. |
| Recorrido | pass | Movimiento real y ausencia de posiciones inválidas durante los intervalos; siete destinos accesibles alrededor de mesa, reposera y extremo de piscina en el modelo de colisión. Agua y mesa bloqueadas. |
| Interfaz de teléfono | pass emulado | 390×844 → 844×390 → 390×844 conserva pose, estado, tamaño y aspecto. Caminar/Salir, tacto, menú que bloquea movimiento, seis cambios repetidos y entrada mixta. La ventana 844×390 con ratón también se compacta. |
| Compilación y producción | pass | TypeScript/Vite; seis estados y movimiento en `/ProjectCobertizo/`, 41 respuestas HTTP bajo prefijo y 36 imágenes embebidas. Cero errores JS/HTTP en producción. |
| Navegador integrado | pass | Día → noche → día accionado y capturado; selector compacto, carga completada y consola sin errores/avisos. `iab-report.json` y capturas `iab-final-*.jpg`. |
| Copia local y portabilidad | pass | Todos los archivos verificados por SHA-256; maestro abierto desde `entrega-repositorio/`, 31 imágenes resueltas dentro de la copia. `delivery-report.json`. |
| Teléfono físico y Safari iOS | not_run | No se dispuso de un teléfono físico. La emulación no prueba su GPU, memoria ni barras reales de Safari. |
| Despliegue remoto | not_run por alcance | El usuario gestionará el repositorio y la publicación. |

La prueba general inyecta deliberadamente el fallo de cinco EXR del perfil Ligera: genera cinco `net::ERR_FAILED` y un aviso de carga esperados. Se conserva el estado anterior y Reintentar recupera el solicitado. No hubo otros errores JS ni fallos HTTP. Las pruebas temporal y de producción no registraron errores.

### Mediciones y presupuestos

MacBook Air M2, 16 GB, macOS 26.6.2; Chromium 153.0.8010.12, ANGLE Metal Apple M2. Browser plugin ausente: Playwright con Chromium completo y revisión adicional en navegador integrado. Headless Shell/SwiftShader no se usa como medición de GPU. Blender terminó sus trabajos antes de las mediciones.

Ventana 1200×800: 60 FPS en los tres perfiles a DPR 1 en la muestra nocturna D3. Día D1 en contexto DPR 2: 46,8 / 60 / 60 FPS con DPR efectivo 1,75 / 1,25 / 0,85. P95 Alta Retina: 33,4 ms. Son ventanas de 6,5 s después de carga; no garantizan 60 FPS durante todo recorrido ni en otros dispositivos. Se conserva Alta y el selector permite Equilibrada.

Primera disponibilidad: 1.010 ms en localhost (935 ms en el contexto Retina posterior). Resource Timing inicial: 37.654.559 bytes transferidos y 37.651.559 bytes de cuerpos para diez recursos. No se extrapola a Internet. Recursos distribuibles de escena: 230.104.435 bytes.

Memoria estimada de mapas activos: 58 / 14,5 / 3,625 MiB; máximo dos conjuntos en caché. No es memoria GPU total medida. Hasta 777.790 triángulos y 137 llamadas en las vistas medidas, incluida reflexión planar. Automática permaneció en Alta durante las ocho observaciones a DPR 1 porque ese equipo sostuvo la cadencia; no se fuerza un descenso ficticio.

### Diferencias y límites visuales

- La escala absoluta, profundidad y partes no observadas conservan los supuestos de `assumptions.md`. La revisión no demuestra exactitud de un levantamiento ni aprobación posterior del usuario.
- El cielo soleado es una elección solicitada; dirección e intensidad no representan una hora u orientación geográfica medida.
- Cycles y Three.js conservan siluetas y sombras principales, con diferencias de fondo, color, especular y oclusión. El cielo web es más saturado y el entorno especular ilumina más uniformemente algunos materiales bajo cubierta.
- El agua usa reflexión planar y absorción aproximada, sin refracción trazada. El borde de piscina aparece más oscuro en web que en Cycles; esa diferencia de representación preexistente no cambia su geometría. No se afirma equivalencia píxel a píxel.
- Los paneles claros usan transmisión difusa en el bake y acabado difusor opaco en web. El filtrado lineal suaviza detalle de iluminación pequeño; juntas finas y follaje conservan aliasing a distancia, sobre todo en perfiles menores.
- Las observaciones temporales descartan alternancias de estado/emisión y parpadeo de los difusores en los intervalos ejecutados. No constituyen una garantía para cualquier GPU, navegador o duración.

La observación temporal acumuló 8,648 cuadros y 144.09 s; en los cuatro recorridos hubo desplazamientos superiores a 9,3 unidades del modelo sin atravesar obstáculos.
