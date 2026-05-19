#!/usr/bin/env python3
"""
CLIENTE DE CHAT
===============
Cliente sencillo para conectarse al servidor de chat.
Permite enviar y recibir mensajes en tiempo real.

Características:
- Conexión a servidor remoto mediante socket TCP
- Recepción de mensajes en un hilo separado
- Envío de mensajes desde la entrada estándar
- Soporte para emojis y UTF-8
- Comando /salir para desconectar
"""

import socket
import threading
import sys

HOST = "127.0.0.1"  # Cambia a la IP del servidor si es remoto
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


def imprimir_banner():
    """Muestra el banner de bienvenida del cliente."""
    banner = f"""
{FG_CYAN}{BOLD}╔═══════════════════════════════════════════════╗
║                💬  CLIENTE DE CHAT PYTHON       ║
║         Escribe /salir para abandonar el chat   ║
╚═══════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def manejar_mensajes(sock: socket.socket) -> None:
    """
    Función para recibir y mostrar mensajes del servidor.
    
    Esta función se ejecuta en un hilo separado y está constantemente
    esperando mensajes desde el servidor. Cuando recibe un mensaje,
    lo muestra en pantalla de forma limpia.
    
    Args:
        sock: Socket conectado al servidor
    """
    try:
        while True:
            # Recibir datos del servidor
            datos = sock.recv(1024)
            
            # Si no hay datos, el servidor se ha desconectado
            if not datos:
                print(f"\n{FG_RED}[El servidor se ha desconectado]{RESET}")
                break

            # Decodificar el mensaje
            texto = datos.decode("utf-8", errors="ignore")

            # Limpia línea actual y muestra el mensaje
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.write(texto)
            sys.stdout.flush()

            # Reponer el prompt para el usuario
            sys.stdout.write(f"{FG_GREEN}> {RESET}")
            sys.stdout.flush()
            
    except OSError:
        # Error de conexión
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass
        salida_segura()


def salida_segura():
    """
    Salir del proceso de forma segura desde cualquier hilo.
    """
    try:
        sys.exit(0)
    except SystemExit:
        import os
        os._exit(0)


def main():
    """
    Función principal del cliente.
    
    Flujo:
    1. Solicita el apodo al usuario
    2. Conecta al servidor
    3. Crea un hilo para recibir mensajes
    4. Lee mensajes del usuario y los envía al servidor
    5. Gestiona la desconexión
    """
    imprimir_banner()
    
    # 1. Solicitar apodo
    apodo = input(f"{FG_YELLOW}Elige un apodo: {RESET}").strip()
    if not apodo:
        apodo = "Anónimo"

    # 2. Conectar al servidor
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except OSError as e:
        print(f"{FG_RED}No se pudo conectar a {HOST}:{PORT} → {e}{RESET}")
        return

    # 3. Crear hilo receptor para manejar mensajes entrantes
    receptor = threading.Thread(target=manejar_mensajes, args=(sock,), daemon=True)
    receptor.start()

    # Enviar apodo al servidor
    sock.sendall((apodo + "\n").encode("utf-8"))

    print(f"{FG_GREEN}Conectado. Escribe tus mensajes. /salir para salir.{RESET}")
    
    # 4. Bucle principal: leer y enviar mensajes
    try:
        while True:
            msg = input(f"{FG_GREEN}> {RESET}")
            
            # Comando para salir
            if msg.strip().lower() == "/salir":
                sock.sendall("/salir".encode("utf-8"))
                break
                
            # Enviar mensaje al servidor
            try:
                sock.sendall(msg.encode("utf-8"))
            except OSError:
                print(f"{FG_RED}Conexión perdida.{RESET}")
                break
                
    except KeyboardInterrupt:
        # Ctrl+C: cerrar limpiamente
        try:
            sock.sendall("/salir".encode("utf-8"))
        except OSError:
            pass

    # 5. Cerrar conexión
    try:
        sock.close()
    except OSError:
        pass
    print(f"{FG_YELLOW}Cerrando cliente...{RESET}")


if __name__ == "__main__":
    main()
