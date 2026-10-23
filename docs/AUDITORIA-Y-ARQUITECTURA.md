# BRYAN.STL STUDIO — Estado auditado (2026-10-23)

## Confirmado por inspección de main
- `src/render_v03.py`: proyección procedural 3D a imágenes OpenCV, audio sintetizado, FFmpeg H.264/AAC, 240 cuadros internos 540x960 escalados a 1080x1920.
- `requirements.txt`: numpy, opencv-python-headless.
- `.github/workflows/verify.yml`: render en Ubuntu y comprobación de duración, dimensiones, fps y códecs.
- No hay Blender, aplicación Safari, TTS, IA de guion, storyboard estructurado ni motor de personajes en los archivos auditados.

## Decisión arquitectónica
Conservar `src/render_v03.py` como motor legacy/preview. Introducir escenas JSON con esquema validable, motor WebGL/Three.js para vista previa en Safari y Blender en CI/servidor para render final (no en iPhone). Audio y subtítulos con herramientas locales; exportación con FFmpeg. La publicación requiere aprobación humana.

## Prioridades
1. Asegurar CI y pruebas de audio; comprobar resultado real de Actions.
2. Escenas parametrizadas y pruebas automatizadas de contrato.
3. Escena 3D con geometría/materiales/cámara real, sin imágenes estáticas.
4. Safari: interfaz de control y preview WebGL; exportación híbrida.
5. TTS y alineación temporal; composición final de 55 segundos.

## Presupuesto
Implementación inicial sin servicios de pago. GitHub Actions puede estar sujeto a cuotas; no activar servicios facturables sin autorización. No afirmar coste total cero sin comprobar el plan.

## Puertas de calidad
No aprobar producción final sin MP4 reproducible, 1650 fotogramas a 30 fps, 1080x1920, audio y subtítulos sincronizados, continuidad, revisión humana de animación y materiales.
