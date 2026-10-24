# Método de producción y dirección visual

## Objetivo de lenguaje

Referencias aportadas por Bryan: video vertical explicativo con objeto o diagrama protagonista, tipografía precisa, cortes motivados por la frase y elementos que cambian frente a cámara. Adaptar el método al universo de música electrónica de BRYAN.STL sin copiar diseños, marcas, voces o escenas específicas de terceros.

La imagen principal de este piloto debe sentirse diseñada y animada en 3D. No usar un montaje de fotos, un animatic de imágenes fijas o zooms como sustituto. Preferir un objeto grande y claro por plano; el festival geométrico previo no es el estándar final.

## Reglas de producción

1. **Guion → acciones.** Cada verbo importante provoca una acción visible. «Desapareciera» detiene físicamente el cono y colapsa la onda; «avanza» mueve el contador; «falta» deja un gesto sin respuesta.
2. **Storyboard y assets.** Dibujar encuadres y puntos de transición antes de construir. Modelar solo altavoces, línea/partículas, teléfono, sala y cabina necesarios para los 15 segundos. Planear continuidad de luz y cámara entre escenas.
3. **Escenas parametrizadas.** Mantener tiempos, textos, cámara, material, luces y eventos sonoros en datos o funciones inspeccionables. No incrustar todo en un único render monolítico. Reutilizar el código existente únicamente cuando resuelva una necesidad comprobada.
4. **Movimiento.** Animar geometría, luces, cámara e interfaz sobre una línea de tiempo común. Usar curvas de aceleración y pausas intencionales. El evento de corte de música debe tener el mismo tiempo en imagen, subtítulo y mezcla.
5. **Voz y sonido.** Grabar o generar una voz con uso autorizado, revisar pronunciación de «BRYAN.STL» solo si se menciona (no en este piloto). Crear un pulso musical original y efectos libres o propios. Después del corte mantener ambiente sin música. Evitar materiales de terceros sin licencia.
6. **Texto.** Sans serif clara y con jerarquía. Blanco dominante, acento violeta muy medido. Subtítulos en fragmentos legibles sincronizados con voz. Crédito pequeño `@bryan.stl` abajo a la izquierda, dentro de zona segura. La composición del piloto no hereda automáticamente la exposición fija ni el formato 1:1 de las series fotográficas.
7. **Render y composición.** Previsualizar primero planos clave y una prueba temporal de baja resolución. Tras aprobación visual, renderizar secuencia completa a resolución nativa, componer voz/ambiente/subtítulos y exportar MP4. Conservar secuencia y proyecto editables.
8. **Iteración.** Revisar fotogramas de inicio, corte, teléfono y club, además del video continuo con audio. Corregir timing, legibilidad y movimientos antes de ampliar a 55 segundos.

## Implementación compatible con el estado actual

El repo contiene un renderer OpenCV `src/render_v03.py` y scripts Blender experimentales bajo `blender/`. Este paquete es especificación, no afirmación de que esas piezas ya produzcan el nuevo piloto. La ruta propuesta es aprovechar Blender para objetos, materiales, luces y cámara, y FFmpeg para composición de audio y exportación; validar primero el entorno y el costo/tiempo de render. Si se usa Three.js para preview, no sustituye por sí mismo al render final. No contratar servicios ni activar consumo facturable por este documento.

## Criterio para expandir

Solo escribir/renderizar los 40 segundos restantes del reel después de ver el piloto de 15 segundos con movimiento real, sonido y subtítulos aprobados. Mantener estructura de curiosidad → consecuencias concretas → remate emocional, con hechos presentados como ficción y sin atribuir efectos sociales o científicos como certezas.
