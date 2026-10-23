# BRYAN.STL STUDIO — Blender v0.4 (experimental)

El motor experimental conserva el renderizador v0.3 sin cambios.

## Ejecutar con Blender 4.x

Desde la raíz del repositorio:

```bash
blender -b -t 4 --python blender/festival_scene.py -- --preview
```

Genera `output/blender-preview.png` a 25 % de resolución para comprobar iluminación, encuadre y compatibilidad, y guarda `output/festival-v04.blend` para inspección. El modo sin argumentos genera un fotograma a resolución nativa 1080×1920 con Cycles, que puede ser costoso.

Solo después de aprobar el fotograma:

```bash
blender -b -t 4 --python blender/festival_scene.py -- --full
```

El modo full escribe secuencia de 240 PNG en `output/blender/`. **Todavía no compone MP4 ni integra audio; no confundir secuencia de fotogramas con entrega audiovisual final.** Se deben evaluar tiempo de render y cuotas antes de automatizar 240 fotogramas en GitHub Actions.

## Verificación actual

Código publicado. No se completó un render con Blender en el entorno de ChatGPT: el ejecutable `blender` y `bpy` no están instalados, y la tentativa de acceder a los paquetes del sistema agotó el tiempo disponible. Pendientes la verificación de compatibilidad Blender 4.x, prueba visual, cálculo de coste y exportación a video.

La geometría de la multitud todavía es simplificada; no es rigging de personajes realista.
