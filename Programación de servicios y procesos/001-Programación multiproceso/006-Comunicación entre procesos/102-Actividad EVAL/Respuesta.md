**Qué son los WebSockets.** WebSocket es un protocolo full-duplex que mantiene un **canal TCP abierto** entre cliente y servidor, permitiendo **mensajería bidireccional y asíncrona** sin estar haciendo peticiones constantes (polling).  
**Por qué importa en multiproceso/servicios.** En Programación de Servicios y Procesos, necesitamos **coordinar procesos** y **reaccionar en tiempo real** (chats, juegos online, paneles en vivo). WebSockets encaja porque reduce latencia, evita sobrecarga de peticiones y simplifica la **comunicación continua** entre componentes.

---

**Servidor (Python + `websockets`).**  
- Escucha en `ws://127.0.0.1:8765`.  
- Gestiona cada conexión en `handler(ws)` y **responde** con un eco del mensaje recibido.

```py
import asyncio, websockets

async def handler(ws):
    async for msg in ws:
        await ws.send(f"echo: {msg}")  # respuesta inmediata

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        await asyncio.Future()  # servidor corriendo

if __name__ == "__main__":
    asyncio.run(main())
```

**Cliente (HTML + JS).**  
- Se **conecta** al puerto `8765`.  
- En `onopen` envía `"hello"`.  
- Muestra por consola los mensajes recibidos y gestiona cierre/errores.

```html
<!doctype html>
<html>
  <head><meta charset="utf-8"></head>
  <body>
    <script>
      const ws = new WebSocket("ws://127.0.0.1:8765");
      ws.onopen    = () => ws.send("hello"); // envío inicial
      ws.onmessage = e => console.log("he recibido un mensaje:", e.data);
      ws.onclose   = () => console.log("closed");
      ws.onerror   = e => console.error("ws error:", e);
    </script>
  </body>
</html>
```

**Verificación funcional.**  
1) Arranca el servidor: `python server.py` → queda a la escucha en `127.0.0.1:8765`.  
2) Abre el cliente en el navegador → consola debería mostrar algo como:  
```
he recibido un mensaje: echo: hello
```
Esto confirma **conexión**, **envío** y **eco** de respuesta.

---

Este ejercicio muestra de forma sencilla cómo cliente y servidor se comunican usando WebSockets.  
- El **servidor** recibe cualquier mensaje que el cliente envía y responde devolviendo el mismo texto con el prefijo `"echo:"`.  
- El **cliente**, al conectarse, envía el mensaje `"hello"` y muestra por consola la respuesta que le devuelve el servidor.  

**Ejemplo de flujo real de ejecución:**  
1. Arrancamos el servidor en Python (`python server.py`).  
2. Abrimos el archivo HTML del cliente en el navegador.  
3. En la consola del navegador aparece:  
   ```
   he recibido un mensaje: echo: hello
   ```  
   Esto confirma que la comunicación bidireccional funciona correctamente.  

Este mismo esquema puede aplicarse a pequeñas aplicaciones interactivas, como un chat básico, un marcador de resultados o la actualización en vivo de un juego.

---

Este ejemplo me permite **aterrizar** la comunicación entre procesos **en tiempo real**: abro un canal WebSocket, intercambio mensajes y gestiono conexiones activas. Lo aprendido se alinea con la unidad de **Programación de Servicios y Procesos** (asincronía, I/O no bloqueante, coordinación de tareas).  
En proyectos futuros (juegos con actualización de estado, chats de equipo, paneles de resultados) podré **integrar WebSockets** para ofrecer **interactividad inmediata**, menor latencia y un modelo de programación más **reactivo** y **escalable**.
