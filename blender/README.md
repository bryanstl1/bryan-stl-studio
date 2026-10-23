# Motor Blender experimental

`blender -b -t 4 --python blender/festival_scene.py` genera una imagen de prueba a resolución nativa 1080×1920. Con `-- --full` intenta renderizar 240 fotogramas PNG en `output/blender/`. Se utiliza Cycles, materiales de nodos, iluminación animada, cámara 3D y personajes geométricos articulados de manera básica.

**Estado:** código publicado y sintaxis Python comprobada, pero **no ejecutado en Blender** en el entorno actual, que carece de Blender. No existe todavía MP4 de este motor. El código puede necesitar ajustes de compatibilidad al ejecutarse en Blender 4.x. La prueba no incluye por ahora onda sonora volumétrica, audio ni composición final. No ejecutar render completo en GitHub Actions sin medir primero duración y consumo de recursos.

Se conserva `src/render_v03.py` como renderizador alternativo.
