# Recursos y procedencia

- Fotografías, video y conceptos: aportados por el usuario, preservados sin alterar en `references/` con inventario SHA-256. No se copian al build de producción. No se presupone una licencia de redistribución de esos originales.
- Geometría: creada por los scripts del proyecto y editable en Blender. Dimensiones visualmente inferidas; no es documentación de cálculo estructural.
- Texturas: generadas proceduralmente por `tools/make_textures.py`, semilla reproducible. Madera, estuco, árido, césped, telas, hormigón y cielo no proceden de bibliotecas comerciales. Véase `blender/textures/LICENSE.txt`.
- Normal de agua: generada por `tools/water_normal.py`. Agua web basada en el módulo Water de Three.js; datos de vaso y contorno derivados del maestro.
- Aplicación: Three.js y sus decodificadores Meshopt y fflate bajo licencia MIT. Se incluyen avisos completos en `web/public/THIRD_PARTY_NOTICES.txt`, copiados también a producción. Vite, TypeScript y Playwright son herramientas de desarrollo fijadas en `package-lock.json`.
- No se compraron ni descargaron recursos gráficos externos.
