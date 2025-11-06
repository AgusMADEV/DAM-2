En un entorno digital complejo, **programar en paralelo** permite aprovechar mejor la CPU y mantener la **interfaz fluida**. Los **Web Workers** son hilos ligeros que se ejecutan **fuera del hilo principal** del navegador. Así, podemos delegar cálculos pesados al worker mientras el UI sigue respondiendo (scroll, clicks, animaciones), algo clave en cualquier SPA o app web con procesos intensivos.

---

El worker realiza una operación matemática intensiva sin bloquear el hilo principal. El código está bien formado y usa la API de mensajería (`postMessage`/`onmessage`).

### `index.html` (hilo principal)
```html
<!doctype html>
<html>
  <body>
    <div id="output">Calculando...</div>

    <script>
      let worker = new Worker("004worker.js");
      let output = document.getElementById("output");

      worker.onmessage = (e) => {
        console.log(e.data);
        output.textContent = `El worker ha terminado.\nResultado: ${e.data}`;
      };

      worker.postMessage("start");
    </script>
  </body>
</html>
```

### `004worker.js` (worker)
```js
self.onmessage = function () {
  let numero = 1.000000000054;
  
  for (let i = 0; i < 2000000000; i++) {
    numero *= 1.000000000043;
  }
  postMessage(numero);
};
```

**Puntos clave técnicos**
- El worker **no accede al DOM**; se comunica con el main thread por mensajes.
- El cálculo se ejecuta **en paralelo** al hilo principal (UI no bloqueada).
- `postMessage` devuelve el **resultado final** al terminar el bucle.

> Nota: el bucle de 2.000 millones de iteraciones es deliberadamente costoso para evidenciar el beneficio del worker.

---

**Uso desde la interfaz principal**
1. Se **instancia** el worker con `new Worker("004worker.js")`.
2. Se **inicia** el trabajo con `worker.postMessage("start")`.
3. El worker realiza el cálculo y **responde** con `postMessage(numero)`.
4. El hilo principal **recibe** el mensaje en `worker.onmessage` y actualiza la UI.

---

Este ejercicio demuestra cómo **aplicar programación paralela en el navegador** con Web Workers para **mejorar el rendimiento** de operaciones intensivas y mantener una UI fluida. Este patrón es útil en proyectos de **desarrollo web** (preprocesado de imágenes, parsers pesados, cifrado) y se conecta con la unidad sobre **concurrencia y acceso a datos** porque fomenta el **diseño no bloqueante** y el **paso de mensajes** entre hilos.
