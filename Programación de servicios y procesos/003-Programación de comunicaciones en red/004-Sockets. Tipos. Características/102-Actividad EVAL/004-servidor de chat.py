#!/usr/bin/env python3
"""
SERVIDOR DE CHAT MULTIUSUARIO
==============================
Este servidor permite múltiples conexiones simultáneas de clientes.
Cada cliente puede enviar mensajes que se distribuyen a todos los demás.

Características:
- Comunicación bidireccional mediante sockets TCP
- Múltiples clientes concurrentes usando threading
- Gestión de apodos y mensajes
- Soporte para emojis y UTF-8
- Comando /salir para desconectar
"""

import socket
import threading

HOST = "0.0.0.0"   # Escuchar en todas las interfaces
PORT = 5000

# Códigos ANSI para colores en terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

FG_CYAN = "\033[36m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_RED = "\033[31m"
FG_MAGENTA = "\033[35m"

# Diccionario para almacenar clientes conectados (socket -> apodo)
clientes = {}
# Lock para acceso seguro al diccionario desde múltiples hilos
lock_clientes = threading.Lock()


def imprimir_banner():
    """Muestra el banner de bienvenida del servidor."""
    banner = f"""
{FG_CYAN}{BOLD}╔═══════════════════════════════════════════════╗
║              💬  SERVIDOR DE CHAT PYTHON        ║
║        Multiusuario · UTF-8 · Emojis 🙂        ║
╚═══════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def enviar_a_todos(mensaje: str, sock_remitente: socket.socket | None = None) -> None:
    """
    Envía un mensaje a todos los clientes excepto al remitente.
    
    Args:
        mensaje: Texto del mensaje a enviar
        sock_remitente: Socket del cliente que envió el mensaje (no recibirá el mensaje)
    """
    datos = mensaje.encode("utf-8", errors="ignore")
    with lock_clientes:
        desconectados = []
        for s in clientes:
            if s is sock_remitente:
                continue
            try:
                s.sendall(datos)
            except OSError:
                desconectados.append(s)

        # Eliminar clientes desconectados
        for s in desconectados:
            apodo = clientes.get(s, "Desconocido")
            del clientes[s]
            print(f"{FG_RED}[DESCONECTADO]{RESET} {apodo} (error de socket)")


def manejar_cliente(conn: socket.socket, addr) -> None:
    """
    Gestiona la conexión de un cliente individual.
    Esta función se ejecuta en un hilo separado para cada cliente.
    
    Flujo:
    1. Solicita el apodo al cliente
    2. Registra al cliente en el diccionario
    3. Notifica a todos de la nueva conexión
    4. Recibe y distribuye los mensajes del cliente
    5. Gestiona la desconexión limpiamente
    
    Args:
        conn: Socket de conexión con el cliente
        addr: Dirección (IP, puerto) del cliente
    """
    try:
        # 1. Solicitar apodo al cliente
        conn.sendall("🟢 Bienvenido. Escribe tu apodo: ".encode("utf-8"))
        apodo_bytes = conn.recv(64)
        if not apodo_bytes:
            conn.close()
            return

        apodo = apodo_bytes.decode("utf-8", errors="ignore").strip()
        if not apodo:
            apodo = f"{addr[0]}:{addr[1]}"

        # 2. Registrar cliente
        with lock_clientes:
            clientes[conn] = apodo

        # 3. Notificar unión
        mensaje_union = f"👤 {apodo} se ha unido al chat.\n"
        print(f"{FG_GREEN}[UNIÓN]{RESET} {apodo} desde {addr}")
        enviar_a_todos(mensaje_union)

        conn.sendall("✅ Ya estás conectado. Escribe /salir para desconectarte.\n".encode("utf-8"))

        # 4. Bucle de recepción de mensajes
        while True:
            datos = conn.recv(1024)
            if not datos:
                break

            texto = datos.decode("utf-8", errors="ignore").strip()
            if texto == "":
                continue

            if texto.lower() == "/salir":
                break

            # Distribuir mensaje a todos los demás clientes
            mensaje = f"💬 {apodo}: {texto}\n"
            print(f"{FG_MAGENTA}[MENSAJE]{RESET} {apodo}: {texto}")
            enviar_a_todos(mensaje, sock_remitente=conn)

    except ConnectionResetError:
        # El cliente cerró la conexión abruptamente
        pass
    finally:
        # 5. Limpieza: eliminar cliente y notificar salida
        with lock_clientes:
            apodo = clientes.pop(conn, "Desconocido")
        conn.close()

        mensaje_salida = f"🚪 {apodo} ha salido del chat.\n"
        print(f"{FG_YELLOW}[SALIDA]{RESET} {apodo}")
        enviar_a_todos(mensaje_salida)


def main():
    """
    Función principal del servidor.
    
    Crea un socket de escucha, acepta conexiones entrantes
    y crea un hilo nuevo para cada cliente conectado.
    """
    imprimir_banner()
    print(f"{DIM}Escuchando en {HOST}:{PORT} ...{RESET}")

    # Crear socket servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Permitir reutilizar el puerto inmediatamente
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincular socket a la dirección y puerto
        servidor.bind((HOST, PORT))
        
        # Comenzar a escuchar conexiones entrantes
        servidor.listen()

        # Bucle principal: aceptar nuevas conexiones
        while True:
            try:
                conn, addr = servidor.accept()
            except KeyboardInterrupt:
                print(f"\n{FG_RED}Cerrando servidor...{RESET}")
                break

            # Crear un hilo para gestionar este cliente
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()


if __name__ == "__main__":
    main()
