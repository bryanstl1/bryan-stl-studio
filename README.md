# BRYAN.STL STUDIO

Estudio experimental de animación narrativa para BRYAN.STL.

## Estado

Prototipos v0.1, v0.2 y v0.3 producidos localmente con render geométrico por software. La v0.3 NO representa aún animación cinematográfica de calidad final. La resolución del MP4 es 1080x1920, pero parte de un render interno de menor resolución.

## Reproducir

Instala Python 3, numpy, Pillow y FFmpeg. Ejecuta `python src/render_v03.py` desde la raíz del repositorio. Inspecciona las dependencias del script antes de ejecutar. La salida se guarda en `output/`.

## Objetivo

Arquitectura modular para guion, storyboard, escenas 3D, motion graphics, audio, render, QA y publicación previa aprobación. No se publica automáticamente.

## Limitaciones

No hay integración con Blender, TTS, subtítulos automáticos ni publicación. El código actual es una prueba técnica, no el estudio completo.

## Piloto «24 horas sin música»

La producción de 15 s está en `productions/musica-24h/`. `src/music_24h_pilot.py` crea movimiento cuadro por cuadro, una mezcla original y un MP4 de revisión. Tiene voz sintética local de guía, no locución LATAM final, y arte 540×960 escalado; leer el estado y los criterios de QA antes de considerarlo publicable.
