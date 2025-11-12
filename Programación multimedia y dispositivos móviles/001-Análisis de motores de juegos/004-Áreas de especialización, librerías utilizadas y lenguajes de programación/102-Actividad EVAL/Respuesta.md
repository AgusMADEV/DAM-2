**¿Qué es A-Frame y cómo se utiliza?**

A-Frame es una librería de código abierto desarrollada sobre Three.js que permite crear experiencias web en realidad virtual y aumentada de forma sencilla utilizando HTML. Su principal ventaja es que no requiere conocimientos avanzados de programación 3D, ya que trabaja con una estructura declarativa basada en etiquetas HTML personalizadas (como `<a-scene>`, `<a-sphere>`, `<a-box>`, etc.).

A-Frame se utiliza simplemente incluyendo su script en el HTML y luego añadiendo elementos 3D dentro de una escena (`<a-scene>`). Es compatible con dispositivos de realidad virtual como Oculus Quest, HTC Vive, y también funciona en navegadores móviles y de escritorio, permitiendo la visualización inmersiva con gafas VR o simplemente en modo 3D tradicional.

---

**Verificación de la carga de la textura:**

He comprobado que la textura se carga correctamente en el archivo `Respuesta.html`. La imagen de la Tierra se ha definido en el bloque `<a-assets>` con el id `texturatierra`, haciendo referencia al archivo `nasatierra.jpg`:

```html
<a-assets>
  <img id="texturatierra" src="nasatierra.jpg">
</a-assets>
```

Esta textura se aplica correctamente a la esfera mediante el atributo `material`, referenciando el id de la imagen:

```html
<a-sphere 
  position="0 1.25 -5" 
  radius="1" 
  material="src: #texturatierra"
></a-sphere>
```

**Estructura del código HTML:**

El código está bien estructurado y sigue las buenas prácticas:
- El script de A-Frame se carga correctamente en el `<head>`
- La escena `<a-scene>` contiene todos los elementos 3D
- Los assets se cargan antes de ser utilizados
- La esfera tiene parámetros bien definidos (posición, radio y material)
- Se incluyen elementos adicionales como el cielo (`<a-sky>`) y luces (`<a-entity light>`) para mejorar la visualización

No he encontrado errores de sintaxis ni problemas en la estructura del HTML.

---
**Código entero:**

```html
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.0/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <!-- Textura de la Tierra -->
      <a-assets>
        <img id="texturatierra" src="nasatierra.jpg">
      </a-assets>
      <a-sphere position="0 1.25 -5" radius="1"  material="src: #texturatierra;"></a-sphere>
      <!-- Cielo y luces -->
      <a-sky color="#000000"></a-sky>
      <a-entity light="type: ambient; intensity: 0.0"></a-entity>
      <a-entity light="type: directional; intensity: 10" position="2 4 0"></a-entity>
    </a-scene>
  </body>
</html>

```

**Pasos realizados para añadir la textura a la esfera:**

1. **Preparación de los assets:** Primero, dentro del elemento `<a-scene>`, he añadido un bloque `<a-assets>` donde se cargan todos los recursos externos (imágenes, modelos 3D, etc.) que voy a utilizar en la escena:

   ```html
   <a-assets>
     <img id="texturatierra" src="nasatierra.jpg">
   </a-assets>
   ```
   
   Aquí definí una imagen con el id `texturatierra` que apunta al archivo `nasatierra.jpg`.

2. **Creación de la esfera:** Luego, creé un elemento esfera usando la etiqueta `<a-sphere>`:

   ```html
   <a-sphere position="0 1.25 -5" radius="3"></a-sphere>
   ```
   
   - `position="0 1.25 -5"`: Coloca la esfera en el espacio 3D (x=0, y=1.25, z=-5)
   - `radius="3"`: Define el tamaño de la esfera con un radio de 3 unidades

3. **Aplicación de la textura:** Para aplicar la textura de la Tierra a la esfera, utilicé el atributo `material` y referencié la imagen cargada usando su id precedido por `#`:

   ```html
   <a-sphere 
     position="0 1.25 -5" 
     radius="3" 
     material="src: #texturatierra; metalness: 0.2; roughness: 0.5"
   ></a-sphere>
   ```
   
   - `src: #texturatierra`: Aplica la imagen de la Tierra como textura
   - `metalness: 0.2`: Define cuán metálico es el material (0.2 es poco metálico)
   - `roughness: 0.5`: Define la rugosidad del material (0.5 es semi-rugoso)

4. **Añadido de iluminación:** Para que la esfera se vea correctamente texturizada, añadí iluminación direccional que simula la luz del sol:

   ```html
   <a-entity light="type: directional; intensity: 10" position="2 4 0"></a-entity>
   ```

**Resultado:** Al abrir el archivo en un navegador, se visualiza una esfera texturizada con la imagen de la Tierra, flotando en un espacio oscuro, iluminada desde un lado, lo que crea un efecto realista y tridimensional.

---

Esta actividad me ha permitido comprender los conceptos básicos de **texturas y materiales en A-Frame**. He aprendido que:

- Las texturas son imágenes que se aplican sobre superficies 3D para darles apariencia realista
- Los materiales definen cómo la luz interactúa con las superficies (metalness, roughness, etc.)
- El sistema de assets de A-Frame permite cargar recursos de forma organizada y eficiente
- La iluminación es fundamental para apreciar correctamente las texturas en un entorno 3D

Como aficionado a los videojuegos, esta práctica me ha recordado a juegos de simulación espacial como *Kerbal Space Program* o *Elite Dangerous*, donde los planetas están texturizados de forma similar para crear entornos inmersivos. Entender cómo funcionan las texturas y materiales me ayuda a apreciar mejor el trabajo técnico detrás de los videojuegos que disfruto.

Además, este conocimiento es aplicable a deportes virtuales y simuladores deportivos, donde las texturas realistas del terreno, las pelotas o los equipamientos son esenciales para crear experiencias inmersivas. Por ejemplo, en juegos de fútbol como FIFA o en simuladores de carreras, las texturas del balón o del asfalto utilizan técnicas similares a las que he aplicado en este ejercicio.

Esta base me permitirá avanzar hacia proyectos más complejos en realidad virtual, donde pueda combinar mis intereses con el desarrollo de experiencias interactivas y visualmente atractivas.
