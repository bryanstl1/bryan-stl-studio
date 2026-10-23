# Música durante 24 horas — piloto de 15 segundos

**Estado:** piloto v0.1 renderizado localmente. Pendiente de voz LATAM final y aprobación visual. El MP4 de revisión se entrega como artefacto separado, no se versiona en Git.

Este piloto prueba si BRYAN.STL STUDIO puede producir una narración visual explicativa con objetos animados, cámara, voz y diseño sonoro sincronizados. El mundo de la historia conserva voces y sonidos ambientales; solo desaparece la música. El corte en el momento del drop es el centro de la pieza.

## Documentos

- [GUION-TECNICO.md](GUION-TECNICO.md): frase, acción, cámara y audio por tramo.
- [METODO-Y-DIRECCION.md](METODO-Y-DIRECCION.md): cómo producirlo con la arquitectura existente.
- [QA.md](QA.md): pruebas y criterios de aprobación.

## Relación con el repositorio

Conservar `src/render_v03.py` como prototipo legacy de ocho segundos. Este piloto nuevo usa `src/music_24h_pilot.py`: altavoz, teléfono y club animados cuadro por cuadro con Pillow/NumPy y audio original, exportados por FFmpeg. La perspectiva y el sombreado se dibujan por código; **no es un render Blender 3D con materiales físicos**. `blender/festival_scene.py` y `blender/festival_v05.py` siguen siendo experimentos separados.

La exportación es vertical 1080 × 1920, 30 fps y 15 s (450 fotogramas) con H.264/AAC. Los dibujos se generan internamente a 540 × 960 y se amplían; esto limita la nitidez de la textura. La voz de la versión v0.1 procede del sintetizador local Flite con fonemas ingleses: solo marca el ritmo, **no es una voz LATAM publicable**. Sustituirla, ajustar sincronía y revisar antes de publicar.

## Reproducir

Desde la raíz, instalar `requirements.txt` y disponer de FFmpeg con el filtro `flite` habilitado. Ejecutar `python src/music_24h_pilot.py --render`. Los archivos van a `output/musica-24h/`: MP4, hoja de contacto, mezcla y voz guía. Ejecutar `python -m unittest tests.test_music_24h_pilot -v` para las pruebas de la animación.
