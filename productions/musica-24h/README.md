# Música durante 24 horas — piloto de 15 segundos

**Estado:** paquete de preproducción, pendiente de producción y revisión visual. No hay MP4 de este piloto todavía.

Este piloto prueba si BRYAN.STL STUDIO puede producir una narración visual explicativa con objetos animados, cámara, voz y diseño sonoro sincronizados. El mundo de la historia conserva voces y sonidos ambientales; solo desaparece la música. El corte en el momento del drop es el centro de la pieza.

## Documentos

- [GUION-TECNICO.md](GUION-TECNICO.md): frase, acción, cámara y audio por tramo.
- [METODO-Y-DIRECCION.md](METODO-Y-DIRECCION.md): cómo producirlo con la arquitectura existente.
- [QA.md](QA.md): pruebas y criterios de aprobación.

## Relación con el repositorio

Conservar `src/render_v03.py` como prototipo legacy de ocho segundos. Puede servir para comparar el efecto de corte, pero su render a resolución interna menor y su festival geométrico no cumplen el objetivo visual de este piloto. `blender/festival_scene.py` y `blender/festival_v05.py` son experimentos reutilizables por partes, sujetos a inspección y prueba. No asumir que Blender, TTS o render completo ya están integrados o verificados.

El objetivo final es vertical 1080 × 1920, 30 fps y 15 s (450 fotogramas) con H.264/AAC. Para pruebas rápidas se permiten previsualizaciones de menor resolución, identificadas como tales. La voz real determina los tiempos finales: los rangos de este documento son objetivos de montaje, no alineación automática verificada. No publicar sin revisión humana.
