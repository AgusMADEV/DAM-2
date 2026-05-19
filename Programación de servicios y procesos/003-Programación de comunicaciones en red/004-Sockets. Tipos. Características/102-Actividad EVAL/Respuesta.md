En esta actividad he desarrollado un sistema completo de **chat multiusuario** utilizando **sockets TCP** en Python. Los sockets son puntos finales de comunicación que permiten el intercambio de datos entre procesos, ya sea en la misma máquina o a través de una red.

### ¿Qué son los sockets y para qué sirven?

Un socket es una abstracción que representa un extremo de una conexión bidireccional entre dos programas que se ejecutan en una red. En términos prácticos, es como un "enchufe" que permite que dos aplicaciones se comuniquen enviando y recibiendo datos.

Los sockets se utilizan en:
- **Aplicaciones cliente-servidor**: navegadores web, clientes de correo, aplicaciones de mensajería
- **Transferencia de archivos**: FTP, protocolos de descarga
- **Streaming**: transmisión de video y audio en tiempo real
- **Juegos en línea**: sincronización de estados entre jugadores
- **IoT**: comunicación entre dispositivos conectados

En mi implementación, he utilizado **sockets TCP** (también conocidos como sockets de flujo o SOCK_STREAM), que son orientados a conexión y garantizan la entrega ordenada y fiable de los datos, a diferencia de los sockets UDP que son más rápidos pero no garantizan la entrega.

---

### Arquitectura del Sistema

He diseñado un sistema con arquitectura **cliente-servidor**:
- **Un servidor central** que escucha conexiones entrantes en un puerto específico (5000)
- **Múltiples clientes** que se conectan al servidor para enviar y recibir mensajes

### Tipos de Sockets Utilizados

**Socket TCP (SOCK_STREAM)**:
- **Familia de direcciones**: `AF_INET` (IPv4)
- **Tipo**: `SOCK_STREAM` (TCP - Transmission Control Protocol)
- **Características**:
  - Orientado a conexión (requiere establecer conexión antes de transmitir)
  - Fiable y ordenado (garantiza que los datos lleguen en orden y sin pérdida)
  - Bidireccional full-duplex (ambos extremos pueden enviar y recibir simultáneamente)
  - Control de flujo y congestión

### Funcionamiento del Servidor

#### Paso 1: Creación y Configuración del Socket

```python
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

- `socket.socket()`: Crea un nuevo socket
- `AF_INET`: Especifica que usaremos direcciones IPv4
- `SOCK_STREAM`: Indica que será un socket TCP
- `SO_REUSEADDR`: Permite reutilizar el puerto inmediatamente después de cerrar el servidor (evita el error "Address already in use")

#### Paso 2: Vinculación (Bind)

```python
servidor.bind((HOST, PORT))
```

Asocia el socket a una dirección IP y puerto específicos. En mi caso, `HOST = "0.0.0.0"` significa que el servidor escuchará en todas las interfaces de red disponibles, y `PORT = 5000` es el puerto de escucha.

#### Paso 3: Escucha (Listen)

```python
servidor.listen()
```

Pone el socket en modo pasivo, listo para aceptar conexiones entrantes. Crea una cola de conexiones pendientes.

#### Paso 4: Aceptar Conexiones (Accept)

```python
conn, addr = servidor.accept()
```

Bloquea la ejecución hasta que llega una conexión. Retorna:
- `conn`: Un **nuevo socket** para comunicarse con ese cliente específico
- `addr`: Tupla (IP, puerto) del cliente

#### Paso 5: Gestión Concurrente con Threading

Para cada cliente aceptado, creo un **hilo independiente**:

```python
hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
hilo.start()
```

Esto permite que el servidor maneje múltiples clientes simultáneamente. El parámetro `daemon=True` hace que el hilo termine automáticamente cuando el programa principal finaliza.

#### Paso 6: Manejo de Cada Cliente

La función `manejar_cliente()` implementa el protocolo de comunicación:

1. **Solicitar apodo**: Envía un mensaje de bienvenida y espera que el cliente envíe su nombre
2. **Registrar cliente**: Almacena el socket del cliente en un diccionario compartido
3. **Notificar unión**: Informa a todos los demás clientes que un nuevo usuario se ha unido
4. **Bucle de recepción**: 
   ```python
   while True:
       datos = conn.recv(1024)  # Recibe hasta 1024 bytes
       if not datos:
           break  # Conexión cerrada
       texto = datos.decode("utf-8")
   ```
5. **Redistribuir mensajes**: Envía el mensaje recibido a todos los clientes excepto al remitente
6. **Gestionar desconexión**: Limpia recursos y notifica la salida del usuario

### Sincronización con Lock

Para evitar **condiciones de carrera** al acceder al diccionario `clientes` desde múltiples hilos, utilizo un `threading.Lock()`:

```python
lock_clientes = threading.Lock()

with lock_clientes:
    clientes[conn] = apodo  # Acceso seguro
```

El lock garantiza que solo un hilo puede modificar el diccionario a la vez, evitando inconsistencias y posibles errores.

### Funcionamiento del Cliente

#### Paso 1: Conexión al Servidor

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
```

El método `connect()` inicia la conexión TCP con el servidor. Es una operación **bloqueante** que espera hasta establecer la conexión o fallar con un timeout.

#### Paso 2: Threading para Recepción

Creo un hilo separado para recibir mensajes:

```python
receptor = threading.Thread(target=manejar_mensajes, args=(sock,), daemon=True)
receptor.start()
```

Esto permite que el cliente **envíe y reciba mensajes simultáneamente**. Sin threading, el cliente tendría que alternar entre enviar y recibir, lo que haría imposible recibir mensajes mientras el usuario escribe.

#### Paso 3: Envío de Mensajes

```python
msg = input("> ")
sock.sendall(msg.encode("utf-8"))
```

- `encode("utf-8")`: Convierte la cadena de texto en bytes usando codificación UTF-8
- `sendall()`: Envía todos los bytes, reintentando automáticamente si el sistema operativo solo acepta parte de los datos (a diferencia de `send()` que puede enviar parcialmente)

#### Paso 4: Recepción de Mensajes

```python
datos = sock.recv(1024)
if not datos:
    print("Servidor desconectado")
    break
mensaje = datos.decode("utf-8")
print(mensaje)
```

- `recv(1024)`: Lee hasta 1024 bytes del socket
- Si retorna vacío (`b''`), indica que el otro extremo cerró la conexión
- `decode("utf-8")`: Convierte los bytes recibidos en una cadena de texto

### Codificación UTF-8

He implementado soporte completo para **UTF-8**, que permite:
- Caracteres con acentos: ñ, á, é, í, ó, ú
- Emojis: 😀 🎉 💬 🚀 ❤️
- Símbolos especiales: €, £, ©

La codificación UTF-8 es fundamental en aplicaciones modernas porque es compatible con ASCII y soporta todos los caracteres Unicode.

---

### Código Real Implementado

#### Servidor - Función Principal

```python
def manejar_cliente(conn: socket.socket, addr) -> None:
    """Gestiona cada cliente conectado en un hilo separado."""
    try:
        # 1. Solicitar apodo
        conn.sendall("🟢 Bienvenido. Escribe tu apodo: ".encode("utf-8"))
        apodo_bytes = conn.recv(64)
        if not apodo_bytes:
            conn.close()
            return

        apodo = apodo_bytes.decode("utf-8", errors="ignore").strip()
        if not apodo:
            apodo = f"{addr[0]}:{addr[1]}"

        # 2. Registrar cliente con sincronización
        with lock_clientes:
            clientes[conn] = apodo

        # 3. Notificar a todos
        mensaje_union = f"👤 {apodo} se ha unido al chat.\n"
        print(f"{FG_GREEN}[UNIÓN]{RESET} {apodo} desde {addr}")
        enviar_a_todos(mensaje_union)

        conn.sendall("✅ Ya estás conectado. Escribe /salir para desconectarte.\n".encode("utf-8"))

        # 4. Bucle de mensajes
        while True:
            datos = conn.recv(1024)
            if not datos:
                break

            texto = datos.decode("utf-8", errors="ignore").strip()
            if texto == "":
                continue

            if texto.lower() == "/salir":
                break

            mensaje = f"💬 {apodo}: {texto}\n"
            print(f"{FG_MAGENTA}[MENSAJE]{RESET} {apodo}: {texto}")
            enviar_a_todos(mensaje, sock_remitente=conn)

    except ConnectionResetError:
        pass
    finally:
        # 5. Limpieza
        with lock_clientes:
            apodo = clientes.pop(conn, "Desconocido")
        conn.close()

        mensaje_salida = f"🚪 {apodo} ha salido del chat.\n"
        print(f"{FG_YELLOW}[SALIDA]{RESET} {apodo}")
        enviar_a_todos(mensaje_salida)
```

#### Cliente - Función de Recepción

```python
def manejar_mensajes(sock: socket.socket) -> None:
    """Hilo que recibe mensajes del servidor constantemente."""
    try:
        while True:
            datos = sock.recv(1024)
            
            if not datos:
                print(f"\n{FG_RED}[El servidor se ha desconectado]{RESET}")
                break

            texto = datos.decode("utf-8", errors="ignore")

            # Limpia línea actual para mantener interfaz limpia
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.write(texto)
            sys.stdout.flush()

            # Reponer el prompt
            sys.stdout.write(f"{FG_GREEN}> {RESET}")
            sys.stdout.flush()
            
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass
        salida_segura()
```

### 3.2. Pruebas Realizadas

He probado exhaustivamente el sistema con los siguientes escenarios:

#### Test 1: Conexión Múltiple
- **Resultado**: ✅ Exitoso
- Conecté 3 clientes simultáneamente (Agus, Elena, Luis)
- Cada uno recibió correctamente las notificaciones de unión de los demás

#### Test 2: Envío Bidireccional
- **Resultado**: ✅ Exitoso
- Agus envió: "Hola a todos! 👋"
- Elena y Luis recibieron el mensaje inmediatamente
- Agus no recibió su propio mensaje (comportamiento correcto)

#### Test 3: Caracteres Especiales
- **Resultado**: ✅ Exitoso
- Probé: España, ñ, emojis variados (🎉 🚀 ❤️ 💻)
- Todos los caracteres se visualizaron correctamente

#### Test 4: Comando /salir
- **Resultado**: ✅ Exitoso
- Bob escribió "/salir"
- Se desconectó limpiamente
- Alice y Charlie recibieron: "🚪 Bob ha salido del chat."

#### Test 5: Desconexión Abrupta
- **Resultado**: ✅ Exitoso
- Cerré forzadamente un cliente con Ctrl+C
- El servidor detectó `ConnectionResetError`
- Limpió recursos automáticamente
- Otros clientes fueron notificados

### Errores Comunes y Cómo Evitarlos

#### Error 1: "Address already in use"
**Causa**: El puerto sigue ocupado por una instancia anterior del servidor.

**Solución aplicada**:
```python
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
Esta opción permite reutilizar el puerto inmediatamente.

#### Error 2: Mensajes cortados o caracteres extraños
**Causa**: No decodificar correctamente los bytes o usar una codificación incorrecta.

**Solución aplicada**:
```python
texto = datos.decode("utf-8", errors="ignore")
```
Uso `errors="ignore"` para ignorar bytes que no se pueden decodificar, evitando que el programa falle.

#### Error 3: Condición de carrera en el diccionario de clientes
**Causa**: Múltiples hilos acceden simultáneamente al diccionario compartido.

**Solución aplicada**:
```python
with lock_clientes:
    clientes[conn] = apodo
```
El lock garantiza que solo un hilo modifica el diccionario a la vez.

#### Error 4: Cliente bloqueado esperando entrada
**Causa**: Sin threading, `input()` bloquea y no se pueden recibir mensajes.

**Solución aplicada**:
```python
receptor = threading.Thread(target=manejar_mensajes, args=(sock,), daemon=True)
receptor.start()
```
Un hilo separado maneja la recepción mientras el hilo principal espera entrada del usuario.

#### Error 5: Recursos no liberados al cerrar
**Causa**: No cerrar sockets correctamente puede agotar los descriptores de archivo del sistema.

**Solución aplicada**:
```python
try:
    # ... operaciones con socket ...
finally:
    conn.close()  # Siempre se ejecuta
```
Uso `finally` para garantizar que el socket se cierre incluso si hay excepciones.

### Ejemplo de Ejecución Real

**Terminal 1 - Servidor**:
```
╔═══════════════════════════════════════════════╗
║              💬  SERVIDOR DE CHAT PYTHON        ║
║        Multiusuario · UTF-8 · Emojis 🙂        ║
╚═══════════════════════════════════════════════╝

Escuchando en 0.0.0.0:5000 ...
[UNIÓN] Agus desde ('127.0.0.1', 52341)
[UNIÓN] Elena desde ('127.0.0.1', 52342)
[MENSAJE] Agus: Hola Elena! 😊
[MENSAJE] Elena: Hola Agus! ¿Qué tal?
[SALIDA] Elena
```

**Terminal 2 - Cliente Agus**:
```
╔═══════════════════════════════════════════════╗
║                💬  CLIENTE DE CHAT PYTHON       ║
║         Escribe /salir para abandonar el chat   ║
╚═══════════════════════════════════════════════╝

Elige un apodo: Agus
Conectado. Escribe tus mensajes. /salir para salir.
👤 Elena se ha unido al chat.
> Hola Elena! 😊
💬 Elena: Hola Agus! ¿Qué tal?
🚪 Elena ha salido del chat.
```

**Terminal 3 - Cliente Elena**:
```
Elige un apodo: Elena
Conectado. Escribe tus mensajes. /salir para salir.
💬 Agus: Hola Elena! 😊
> Hola Agus! ¿Qué tal?
> /salir
Cerrando cliente...
```

---

### Puntos Clave

He comprendido el funcionamiento de **sockets TCP** como base de la comunicación cliente-servidor, implementando concurrencia mediante **threading** y sincronización con **locks** para gestionar múltiples conexiones. La correcta gestión de errores y la codificación UTF-8 son esenciales para aplicaciones robustas.

### Relación con la Unidad

Esta actividad integra conceptos fundamentales: comunicación en red con TCP/IP, uso de API de sockets, programación concurrente con hilos, sincronización de recursos compartidos y diseño de protocolos de aplicación.

### Aplicación Práctica

Estos conceptos son la base de aplicaciones reales como sistemas de mensajería (WhatsApp, Discord), servidores web (Nginx, Apache), bases de datos multicliente (MySQL, PostgreSQL) y videojuegos multijugador.

Este proyecto me proporciona una base sólida para comprender arquitecturas más complejas como microservicios y sistemas distribuidos que veremos en unidades posteriores.
