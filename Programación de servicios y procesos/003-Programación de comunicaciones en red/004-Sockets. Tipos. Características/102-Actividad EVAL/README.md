# Actividad EVAL: Cliente y Servidor de Chat

## 📋 Descripción

Esta actividad consiste en desarrollar un sistema completo de chat multiusuario utilizando sockets en Python. El sistema permite la comunicación bidireccional entre múltiples clientes a través de un servidor central.

## 🎯 Objetivos de Aprendizaje

- Comprender el funcionamiento de sockets TCP en Python
- Implementar comunicación cliente-servidor
- Gestionar múltiples conexiones concurrentes con threading
- Manejar codificación UTF-8 y mensajes con emojis
- Implementar protocolos de comunicación personalizados

## 📁 Archivos del Proyecto

- **004-servidor de chat.py**: Servidor de chat multiusuario
- **005-cliente de chat.py**: Cliente de chat para conectarse al servidor

## 🚀 Instrucciones de Ejecución

### 1. Iniciar el Servidor

Abre una terminal en la carpeta `102-Actividad EVAL` y ejecuta:

```bash
python "004-servidor de chat.py"
```

Verás el banner del servidor y el mensaje:
```
Escuchando en 0.0.0.0:5000 ...
```

### 2. Conectar Clientes

Abre **nuevas terminales** (tantas como clientes quieras probar) y ejecuta en cada una:

```bash
python "005-cliente de chat.py"
```

Se te pedirá un apodo. Escríbelo y presiona Enter.

### 3. Enviar Mensajes

- Escribe mensajes en cualquier cliente y presiona Enter
- Los mensajes se enviarán al servidor
- El servidor distribuirá los mensajes a todos los demás clientes conectados
- Cada cliente verá los mensajes de los demás en tiempo real

### 4. Desconectar

Escribe `/salir` en un cliente para desconectarte del chat.

## 🔍 Conceptos Implementados

### En el Servidor (004-servidor de chat.py)

#### 1. **Función `manejar_cliente(conn, addr)`**

Esta función gestiona cada cliente conectado:

```python
def manejar_cliente(conn: socket.socket, addr) -> None:
    # 1. Solicita el apodo al cliente
    conn.sendall("🟢 Bienvenido. Escribe tu apodo: ".encode("utf-8"))
    apodo_bytes = conn.recv(64)
    
    # 2. Registra al cliente en el diccionario
    with lock_clientes:
        clientes[conn] = apodo
    
    # 3. Notifica a todos de la nueva conexión
    enviar_a_todos(mensaje_union)
    
    # 4. Bucle para recibir mensajes
    while True:
        datos = conn.recv(1024)
        if not datos:
            break
        # Procesar y redistribuir mensaje
        enviar_a_todos(mensaje, sock_remitente=conn)
```

**Características clave:**
- Usa `conn.recv(1024)` para recibir hasta 1024 bytes
- Decodifica los datos con `decode("utf-8")`
- Gestiona el comando `/salir` para desconectar
- Usa un lock (threading.Lock) para acceso seguro al diccionario de clientes

#### 2. **Función `main()` del Servidor**

Acepta nuevas conexiones y crea hilos:

```python
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        
        while True:
            conn, addr = servidor.accept()  # Espera nueva conexión
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()  # Inicia hilo para este cliente
```

**Características clave:**
- `socket.AF_INET`: Familia de direcciones IPv4
- `socket.SOCK_STREAM`: Socket TCP (orientado a conexión)
- `SO_REUSEADDR`: Permite reutilizar el puerto inmediatamente
- `listen()`: Pone el socket en modo escucha
- `accept()`: Bloquea hasta que llega una conexión
- Cada cliente se gestiona en un hilo separado (`daemon=True`)

### En el Cliente (005-cliente de chat.py)

#### 1. **Función `manejar_mensajes(sock)`**

Recibe mensajes del servidor constantemente:

```python
def manejar_mensajes(sock: socket.socket) -> None:
    while True:
        datos = sock.recv(1024)
        if not datos:
            break
        mensaje = datos.decode("utf-8")
        print(mensaje)
```

**Características clave:**
- Se ejecuta en un hilo separado
- Bloquea en `recv()` esperando datos
- Si `recv()` devuelve vacío, el servidor se desconectó

#### 2. **Función `main()` del Cliente**

Conecta al servidor y gestiona el envío de mensajes:

```python
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))  # Conectar al servidor
    
    # Crear hilo para recibir mensajes
    receptor = threading.Thread(target=manejar_mensajes, args=(sock,), daemon=True)
    receptor.start()
    
    # Enviar apodo
    sock.sendall((apodo + "\n").encode("utf-8"))
    
    # Bucle de envío
    while True:
        msg = input("> ")
        if msg.lower() == "/salir":
            break
        sock.sendall(msg.encode("utf-8"))
```

**Características clave:**
- `connect()`: Establece conexión con el servidor
- `sendall()`: Envía todos los datos (maneja envíos parciales automáticamente)
- Usa threading para recibir y enviar simultáneamente

## 🧪 Pruebas Realizadas

### Test 1: Conexión de Múltiples Clientes
- [✓] Abrir el servidor
- [✓] Conectar 3 clientes con diferentes apodos
- [✓] Verificar que todos reciben las notificaciones de unión

### Test 2: Envío de Mensajes
- [✓] Cliente A envía mensaje
- [✓] Clientes B y C reciben el mensaje
- [✓] Cliente A no recibe su propio mensaje

### Test 3: Soporte UTF-8 y Emojis
- [✓] Enviar mensajes con emojis: 😀 🎉 ❤️
- [✓] Enviar mensajes con acentos: ñ, á, é, í
- [✓] Verificar correcta decodificación

### Test 4: Desconexión
- [✓] Cliente escribe `/salir`
- [✓] Otros clientes reciben notificación de salida
- [✓] Cliente se desconecta limpiamente

### Test 5: Desconexión Abrupta
- [✓] Cerrar terminal de un cliente (Ctrl+C)
- [✓] Servidor detecta desconexión
- [✓] Notifica a otros clientes

## 📚 Conceptos Técnicos

### Sockets TCP
- **Orientado a conexión**: Se establece una conexión antes de enviar datos
- **Fiable**: Garantiza la entrega ordenada de datos
- **Bidireccional**: Permite comunicación en ambas direcciones

### Threading
- **Concurrencia**: Permite gestionar múltiples clientes simultáneamente
- **Daemon threads**: Terminan automáticamente cuando el programa principal termina
- **Lock**: Sincroniza el acceso al diccionario compartido

### Codificación UTF-8
- **Universal**: Soporta todos los caracteres Unicode
- **Emojis**: Codifica correctamente emojis y símbolos
- **`errors="ignore"`**: Ignora caracteres que no se pueden decodificar

## 🔧 Posibles Mejoras

1. **Autenticación**: Agregar contraseñas para los usuarios
2. **Salas**: Implementar diferentes salas de chat
3. **Mensajes privados**: Permitir enviar mensajes directos entre usuarios
4. **Historial**: Guardar los mensajes en un archivo
5. **GUI**: Crear una interfaz gráfica con tkinter o PyQt
6. **Encriptación**: Implementar SSL/TLS para comunicación segura

## ❓ Preguntas de Reflexión

1. ¿Qué pasaría si no usáramos threading en el servidor?
2. ¿Por qué necesitamos un lock para el diccionario de clientes?
3. ¿Cuál es la diferencia entre `send()` y `sendall()`?
4. ¿Qué ocurre si `recv()` devuelve menos bytes de los solicitados?
5. ¿Por qué el cliente necesita un hilo separado para recibir mensajes?

## 📝 Conclusiones

Este proyecto demuestra los fundamentos de la programación de red en Python:

- Uso de sockets para comunicación TCP/IP
- Gestión de concurrencia con threading
- Manejo de codificación y decodificación de texto
- Implementación de un protocolo de comunicación simple
- Gestión de errores y desconexiones

La aplicación funciona correctamente y permite la comunicación en tiempo real entre múltiples usuarios, cumpliendo con todos los requisitos de la actividad.

---

**Autor**: Actividad EVAL - Programación de Servicios y Procesos  
**Fecha**: Febrero 2026  
**Lenguaje**: Python 3.10+
