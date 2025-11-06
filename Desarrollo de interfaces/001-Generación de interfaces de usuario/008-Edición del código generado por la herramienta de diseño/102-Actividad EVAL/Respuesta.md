En esta práctica parto de un diseño inicial (tarjetas circulares con título) y **edito el código generado** para convertirlo en **gráficas de tarta dinámicas** sin librerías externas. He integrado:
- **Fondo con `conic-gradient`** para pintar los sectores.
- **Capa SVG superpuesta** para etiquetas y líneas guía (leader lines).
- **Parámetros de configuración** (formateo de etiquetas, radios interiores/exteriores, umbral para etiquetas internas).

El objetivo es demostrar cómo, desde el código que entrega una herramienta de diseño (estructura y estilos base), puedo **refactorizar y ampliar** comportamiento visual y datos, manteniendo una separación clara entre **presentación (CSS)** y **lógica (JS)**.

---

### Estructura y buenas prácticas
- **Datos**: cuatro arrays (`datos1..datos4`) con pares `Etiqueta`/`Valor`.
- **Lógica reusable**: función `amdev_tarta(selector, datos, colorBase, titulo, opciones)` que construye cada gráfica.
- **Estilos**: tarjeta circular, sombra, `:hover` con transición; tipografía del sistema; etiquetas SVG legibles con contorno (stroke) para contraste.
- **Sin dependencias**: uso exclusivo de **HTML + CSS + JS**.

### Puntos clave del código
1. **Cálculo del gradiente cónico**
   ```js
   const suma = datos.reduce((acc, d) => acc + d.Valor, 0);
   const colores = datos.map(() => randomLightnessVariation(colorBase));
   let cursor = 0, grad = "";
   for (let i=0;i<datos.length;i++){
     const inicio = (cursor * 100).toFixed(6) + "%";
     cursor += datos[i].Valor / suma;
     const fin = (cursor * 100).toFixed(6) + "%";
     grad += `${colores[i]} ${inicio} ${fin},`;
   }
   grafica.style.background = `conic-gradient(${grad.slice(0,-1)})`;
   ```
   - Recorro fracciones acumuladas para definir **paradas exactas** del gradiente.
   - `randomLightnessVariation` genera **variaciones de luminosidad** sobre `colorBase` para distinguir sectores sin una paleta fija.

2. **Capa SVG para interacción y etiquetado**
   ```js
   overlay = document.createElementNS("http://www.w3.org/2000/svg","svg");
   overlay.setAttribute("class","overlay");
   overlay.setAttribute("viewBox", `0 0 ${size} ${size}`);
   // Grupos semánticos
   const gSlices = document.createElementNS("http://www.w3.org/2000/svg","g");
   const gLeaders = document.createElementNS("http://www.w3.org/2000/svg","g");
   const gLabels  = document.createElementNS("http://www.w3.org/2000/svg","g");
   overlay.append(gSlices, gLeaders, gLabels);
   ```
   - Aunque el color de sectores lo da el gradiente, **dibujo paths de sector** (invisibles) para tener **superficie interactiva** si más adelante queremos tooltips/hover.
   - **Etiquetas internas** si la fracción supera un umbral; en caso contrario, **línea guía externa** y texto fuera.

3. **Geometría de sectores y líneas guía**
   ```js
   function arcoPath(cx, cy, r, angInicio, angFin){
     const a1 = angInicio - Math.PI/2, a2 = angFin - Math.PI/2;
     const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
     const x2 = cx + r * Math.cos(a2), y2 = cy + r * Math.sin(a2);
     const largeArc = (angFin - angInicio) > Math.PI ? 1 : 0;
     return `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} Z`;
   }
   ```
   - Alineo el ángulo 0º hacia **arriba** restando `π/2` (convención visual habitual).
   - `largeArc` gestiona arcos > 180° para un path correcto.

4. **API de opciones con valores por defecto**
   ```js
   function amdev_tarta(selector, datos, colorBase, titulo = "", {
     labelFormatter = (d, fr) => `${d.Etiqueta} (${d.Valor})`,
     insideMinFraction = 0.08,
     innerRadiusRatio = 0.55,
     outerLineStart = 0.72,
     outerLineEnd   = 0.92,
     outerLabelRadius = 1.02
   } = {}) { /* ... */ }
   ```
   - Facilita **reutilización** y **control fino** sin tocar la función principal.
   - `labelFormatter` permite personalizar el texto de las etiquetas.

5. **Accesibilidad y legibilidad**
   - Etiquetas con **contorno** (stroke) para mejorar contraste.
   - Tamaño de fuente y **espaciado** adecuados en títulos y etiquetas.
   - Estructura **semántica** en grupos SVG.

---

### Instanciación básica (los cuatro gráficos del ejercicio)
```js
amdev_tarta(".grafica1", datos1, "#ae2e33", "Plataformas");
amdev_tarta(".grafica2", datos2, "#e5e7eb", "Sagas más jugadas");
amdev_tarta(".grafica3", datos3, "#00A398", "Géneros populares");
amdev_tarta(".grafica4", datos4, "#334155", "Personajes favoritos");
```

### Personalizar etiquetas y umbrales
```js
amdev_tarta(".grafica1", datos1, "#ae2e33", "Plataformas (personalizado)", {
  labelFormatter: (d, fr) => `${d.Etiqueta}: ${(fr*100).toFixed(1)}%`,
  insideMinFraction: 0.10,      // solo etiquetas internas si el sector >=10%
  innerRadiusRatio: 0.58,       // separa un poco el texto del centro
  outerLabelRadius: 1.05        // aleja ligeramente las etiquetas externas
});
```

### Sustituir datos en caliente
```js
const nuevos = [
  {Etiqueta:"Consola A", Valor:50},
  {Etiqueta:"Consola B", Valor:30},
  {Etiqueta:"Consola C", Valor:20},
];
amdev_tarta(".grafica2", nuevos, "#2563eb", "Comparativa de consolas");
```
> Al volver a invocar `amdev_tarta` sobre el mismo `selector`, la función **reconstruye** la capa SVG y el título, manteniendo el gradiente y el layout actualizados al nuevo dataset.

---

- **Partir de un esqueleto visual** (tarjetas circulares con título) y **editar** el HTML/CSS para albergar un componente de datos real.
- **Encapsular la lógica** en una función reusable con **API de opciones**, separando datos, estilos y renderizado.
- **Ampliar capacidades** (etiquetas dinámicas, líneas guía, variación cromática) sin introducir dependencias.

Este patrón es transferible a otros casos de “código auto‑generado”: refactorizar, parametrizar y documentar para convertir un mockup en un **componente productivo**. Próximos pasos naturales serían añadir **tooltips**, **leyenda**, animaciones de entrada o una **API de eventos** para integrar las gráficas en cuadros de mando más grandes.

---
```
<!doctype html>
<html>
  <head>
    <title>Gráficas</title>
    <meta charset="utf-8">
    <style>
      body {
        margin: 0;
        padding: 40px;
        background: #f9fafb;
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, Ubuntu, sans-serif;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 32px;
      }

      .grafica1, .grafica2, .grafica3, .grafica4 {
        position: relative;
        width: 260px;
        aspect-ratio: 1;
        border-radius: 50%;
        display: inline-block;
        background: #f1f5f9;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
        margin-bottom: 48px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
      }

      .grafica1:hover, .grafica2:hover, .grafica3:hover, .grafica4:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.12);
      }

      .overlay {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
      }

      /* Etiquetas dentro de los gráficos */
      .label {
        font: 12px/1.3 "Segoe UI", system-ui, sans-serif;
        fill: #1f2937;
        paint-order: stroke;
        stroke: #f9fafb;
        stroke-width: 3px;
        stroke-linejoin: round;
        text-anchor: middle;
        pointer-events: none;
      }

      .leader {
        stroke: rgba(0, 0, 0, 0.35);
        stroke-width: 1;
        fill: none;
        pointer-events: none;
      }

      /* Título de la gráfica */
      .chart-title {
        position: absolute;
        left: 50%;
        bottom: -28px;
        transform: translateX(-50%);
        font: 600 15px/1.2 "Segoe UI", system-ui, sans-serif;
        color: #111827;
        text-align: center;
        letter-spacing: -0.4px;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div class="grafica1"></div>
    <div class="grafica2"></div>
    <div class="grafica3"></div>
    <div class="grafica4"></div>  
    <script>
      let datos1 = [
        {"Etiqueta":"PlayStation 5","Valor":34},
        {"Etiqueta":"PC","Valor":78},
        {"Etiqueta":"Xbox Series","Valor":76},
        {"Etiqueta":"Nintendo Switch","Valor":87},
        {"Etiqueta":"Dispositivos móviles","Valor":127}
      ];
      let datos2 = [
        {"Etiqueta":"The Legend of Zelda","Valor":56},
        {"Etiqueta":"Super Mario","Valor":102},
        {"Etiqueta":"Pokémon","Valor":88},
        {"Etiqueta":"Final Fantasy","Valor":74},
        {"Etiqueta":"Call of Duty","Valor":61}
      ];
      let datos3 = [
        {"Etiqueta":"RPG","Valor":120},
        {"Etiqueta":"Acción / Aventura","Valor":98},
        {"Etiqueta":"Shooter","Valor":77},
        {"Etiqueta":"Mundo abierto","Valor":110},
        {"Etiqueta":"Indie","Valor":45}
      ];
      let datos4 = [
        {"Etiqueta":"Mario","Valor":34},
        {"Etiqueta":"Link","Valor":52},
        {"Etiqueta":"Pikachu","Valor":46},
        {"Etiqueta":"Lara Croft","Valor":29},
        {"Etiqueta":"Master Chief","Valor":67}
      ];

      function randomLightnessVariation(hex, min = 0.7, max = 1.3) {
        let r = parseInt(hex.slice(1, 3), 16) / 255;
        let g = parseInt(hex.slice(3, 5), 16) / 255;
        let b = parseInt(hex.slice(5, 7), 16) / 255;
        let maxC = Math.max(r, g, b), minC = Math.min(r, g, b);
        let l = (maxC + minC) / 2;
        let s, h;
        if (maxC === minC) { s = h = 0; }
        else {
          let d = maxC - minC;
          s = l > 0.5 ? d / (2 - maxC - minC) : d / (maxC + minC);
          switch (maxC) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
          }
          h /= 6;
        }
        let L = l * (min + Math.random() * (max - min));
        L = Math.max(0, Math.min(1, L));
        function hue2rgb(p, q, t) {
          if (t < 0) t += 1;
          if (t > 1) t -= 1;
          if (t < 1/6) return p + (q - p) * 6 * t;
          if (t < 1/2) return q;
          if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
          return p;
        }
        let q = L < 0.5 ? L * (1 + s) : L + s - L * s;
        let p = 2 * L - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
        return "#" +
          Math.round(r * 255).toString(16).padStart(2, "0") +
          Math.round(g * 255).toString(16).padStart(2, "0") +
          Math.round(b * 255).toString(16).padStart(2, "0");
      }

      const defaultLabelFormatter = (d) => `${d.Etiqueta} (${d.Valor})`;

      function amdev_tarta(selector, datos, colorBase, titulo = "", {
        labelFormatter = defaultLabelFormatter,
        insideMinFraction = 0.08,
        innerRadiusRatio = 0.55,
        outerLineStart = 0.72,
        outerLineEnd = 0.92,
        outerLabelRadius = 1.02
      } = {}){
        const suma = datos.reduce((acc, d) => acc + d.Valor, 0);
        const colores = datos.map(() => randomLightnessVariation(colorBase));
        let cursor = 0, grad = "";
        for (let i=0;i<datos.length;i++){
          const inicio = (cursor * 100).toFixed(6) + "%";
          cursor += datos[i].Valor / suma;
          const fin = (cursor * 100).toFixed(6) + "%";
          grad += `${colores[i]} ${inicio} ${fin},`;
        }
        grad = grad.slice(0,-1);

        const grafica = document.querySelector(selector);
        grafica.style.background = `conic-gradient(${grad})`;

        let titleEl = grafica.querySelector(".chart-title");
        if(!titleEl){
          titleEl = document.createElement("div");
          titleEl.className = "chart-title";
          grafica.appendChild(titleEl);
        }
        titleEl.textContent = titulo || "";

        let overlay = grafica.querySelector("svg.overlay");
        if(overlay) overlay.remove();

        const size = grafica.clientWidth || 240;
        const cx = size/2, cy = size/2, r = size/2;

        overlay = document.createElementNS("http://www.w3.org/2000/svg","svg");
        overlay.setAttribute("class","overlay");
        overlay.setAttribute("viewBox", `0 0 ${size} ${size}`);
        overlay.setAttribute("preserveAspectRatio","xMidYMid meet");

        const gLeaders = document.createElementNS("http://www.w3.org/2000/svg","g");
        const gLabels  = document.createElementNS("http://www.w3.org/2000/svg","g");
        overlay.appendChild(gLeaders);
        overlay.appendChild(gLabels);

        let angAcum = 0;
        for (let i=0;i<datos.length;i++){
          const fr = datos[i].Valor / suma;
          const angInicio = angAcum;
          const angFin = angAcum + fr * Math.PI * 2;
          const angMid = (angInicio + angFin) / 2;
          angAcum = angFin;

          const text = document.createElementNS("http://www.w3.org/2000/svg","text");
          text.setAttribute("class","label");
          text.textContent = labelFormatter(datos[i], fr);
          const a = angMid - Math.PI/2;

          if (fr >= insideMinFraction){
            const rx = r * innerRadiusRatio;
            const x = cx + rx * Math.cos(a);
            const y = cy + rx * Math.sin(a);
            text.setAttribute("x", x);
            text.setAttribute("y", y);
            gLabels.appendChild(text);
          } else {
            const x1 = cx + r * outerLineStart * Math.cos(a);
            const y1 = cy + r * outerLineStart * Math.sin(a);
            const x2 = cx + r * outerLineEnd   * Math.cos(a);
            const y2 = cy + r * outerLineEnd   * Math.sin(a);
            const line = document.createElementNS("http://www.w3.org/2000/svg","path");
            line.setAttribute("class","leader");
            const side = Math.cos(a) >= 0 ? 1 : -1;
            const x2b = x2 + side * 8;
            line.setAttribute("d", `M ${x1} ${y1} L ${x2} ${y2} L ${x2b} ${y2}`);
            gLeaders.appendChild(line);

            const xText = cx + r * outerLabelRadius * Math.cos(a) + side * 14;
            const yText = cy + r * outerLabelRadius * Math.sin(a);
            text.setAttribute("x", xText);
            text.setAttribute("y", yText);
            text.setAttribute("text-anchor", side === 1 ? "start" : "end");
            gLabels.appendChild(text);
          }
        }
        grafica.appendChild(overlay);
      }

      amdev_tarta(".grafica1", datos1, "#ae2e33", "Plataformas");
      amdev_tarta(".grafica2", datos2, "#e5e7eb", "Sagas más jugadas");
      amdev_tarta(".grafica3", datos3, "#00A398", "Géneros populares");
      amdev_tarta(".grafica4", datos4, "#334155", "Personajes favoritos");
    </script>
  </body>
</html>
```
