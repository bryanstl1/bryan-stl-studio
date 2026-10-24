# QA del piloto — lista verificable

Este documento define condiciones para la revisión. **Ninguna prueba se considera pasada hasta generar el piloto y registrar evidencia.**

## Técnica

- [ ] `ffprobe`: 15.0 s (tolerancia de montaje ±0.15 s), 1080 × 1920, 30 fps, H.264 y pista AAC.
- [ ] 450 fotogramas útiles, sin cuadros negros accidentales, congelamiento no intencional ni saltos de geometría.
- [ ] Audio sin clipping; voz inteligible en altavoz de teléfono, con pulso inicial y ausencia de música posterior al corte.
- [ ] Subtítulos coinciden con la voz, con revisión manual de inicio y fin por frase; ninguna palabra queda cortada.
- [ ] Crédito y texto legibles con la interfaz típica de Reels sobrepuesta, sin invadir controles.

## Dirección

- [ ] El altavoz vibra y se detiene visiblemente alrededor de «desapareciera».
- [ ] El contador del teléfono avanza aunque la canción no produce audio.
- [ ] Luz, cámara, interfaz y figuras cambian dentro de los planos; no es una secuencia de imágenes fijas.
- [ ] El club comunica ausencia de música sin convertir el mundo en silencio absoluto.
- [ ] No aparecen rostros deformados, manos extrañas, geometría rota ni texto ilegible.
- [ ] El color y la tipografía sostienen una identidad propia de BRYAN.STL, sin calcar la marca de las referencias.

## Evidencia a adjuntar cuando exista

Guardar un contacto de fotogramas en 0, 3.15, 6.5, 10 y 13 s, un extracto de mezcla alrededor del corte, la salida de `ffprobe`, el comando de render y el MP4 final. Registrar tiempo de render y versión de Blender/FFmpeg. Si falla una condición, anotar la falla y corregirla antes de llamar al piloto «listo».
