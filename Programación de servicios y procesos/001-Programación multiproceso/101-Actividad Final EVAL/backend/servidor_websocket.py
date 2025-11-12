"""
Servidor WebSocket para comunicación en tiempo real
Permite que el frontend reciba actualizaciones en tiempo real del procesamiento
"""

import asyncio
import websockets
import json
import os
import threading
from pathlib import Path
from procesador import ProcesadorImagenes, obtener_imagenes_directorio


class ServidorWebSocket:
    """
    Servidor WebSocket que gestiona la comunicación en tiempo real
    con el cliente web y coordina el procesamiento de imágenes
    """
    
    def __init__(self, host='localhost', puerto=8765):
        """
        Inicializa el servidor WebSocket
        
        Args:
            host: Host del servidor (default: localhost)
            puerto: Puerto del servidor (default: 8765)
        """
        self.host = host
        self.puerto = puerto
        self.clientes = set()
        self.procesador = None
        self.procesando = False
        
    async def registrar_cliente(self, websocket):
        """
        Registra un nuevo cliente conectado
        
        Args:
            websocket: Conexión del cliente
        """
        self.clientes.add(websocket)
        print(f"✅ Cliente conectado. Total clientes: {len(self.clientes)}")
        
        # Enviar mensaje de bienvenida
        await self.enviar_mensaje(websocket, {
            'tipo': 'conexion',
            'mensaje': 'Conectado al servidor de procesamiento',
            'estado': 'conectado'
        })
    
    async def desregistrar_cliente(self, websocket):
        """
        Desregistra un cliente desconectado
        
        Args:
            websocket: Conexión del cliente
        """
        self.clientes.discard(websocket)
        print(f"❌ Cliente desconectado. Total clientes: {len(self.clientes)}")
    
    async def enviar_mensaje(self, websocket, datos):
        """
        Envía un mensaje JSON a un cliente específico
        
        Args:
            websocket: Conexión del cliente
            datos: Diccionario con los datos a enviar
        """
        try:
            mensaje = json.dumps(datos, ensure_ascii=False)
            await websocket.send(mensaje)
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def broadcast(self, datos):
        """
        Envía un mensaje a todos los clientes conectados
        
        Args:
            datos: Diccionario con los datos a enviar
        """
        if self.clientes:
            mensaje = json.dumps(datos, ensure_ascii=False)
            await asyncio.gather(
                *[cliente.send(mensaje) for cliente in self.clientes],
                return_exceptions=True
            )
    
    def callback_progreso(self, info):
        """
        Callback para reportar progreso del procesamiento
        Se ejecuta desde el procesador y envía actualizaciones a los clientes
        
        Args:
            info: Diccionario con información del progreso
        """
        # Crear tarea asíncrona para enviar el mensaje
        asyncio.run(self.broadcast({
            'tipo': 'progreso',
            'datos': info
        }))
    
    async def procesar_comando(self, websocket, comando):
        """
        Procesa comandos recibidos del cliente
        
        Args:
            websocket: Conexión del cliente
            comando: Diccionario con el comando y parámetros
        """
        tipo = comando.get('tipo', '')
        
        if tipo == 'listar_filtros':
            await self.comando_listar_filtros(websocket)
            
        elif tipo == 'listar_imagenes':
            await self.comando_listar_imagenes(websocket)
            
        elif tipo == 'procesar':
            await self.comando_procesar(websocket, comando)
            
        elif tipo == 'estado':
            await self.comando_estado(websocket)
            
        elif tipo == 'cancelar':
            await self.comando_cancelar(websocket)
            
        else:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': f'Comando desconocido: {tipo}'
            })
    
    async def comando_listar_filtros(self, websocket):
        """
        Envía la lista de filtros disponibles al cliente
        """
        from filtros import FiltrosImagen
        filtros = list(FiltrosImagen.obtener_filtros_disponibles().keys())
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'filtros',
            'datos': filtros
        })
    
    async def comando_listar_imagenes(self, websocket):
        """
        Envía la lista de imágenes disponibles en el directorio de entrada
        """
        dir_entrada = "../input_images"
        imagenes = obtener_imagenes_directorio(dir_entrada)
        
        nombres = [os.path.basename(img) for img in imagenes]
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'imagenes',
            'datos': {
                'cantidad': len(nombres),
                'imagenes': nombres
            }
        })
    
    async def comando_procesar(self, websocket, comando):
        """
        Inicia el procesamiento de imágenes
        
        Args:
            comando: Diccionario con parámetros del procesamiento
                - filtros: Lista de filtros a aplicar
                - modo: 'threads' o 'procesos'
                - imagenes: Lista de imágenes específicas (opcional)
        """
        if self.procesando:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': 'Ya hay un procesamiento en curso'
            })
            return
        
        self.procesando = True
        
        # Obtener parámetros
        filtros = comando.get('filtros', ['grises'])
        modo = comando.get('modo', 'procesos')
        
        # Obtener imágenes
        dir_entrada = "../input_images"
        dir_salida = "../output_images"
        imagenes = obtener_imagenes_directorio(dir_entrada)
        
        if not imagenes:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': 'No se encontraron imágenes para procesar'
            })
            self.procesando = False
            return
        
        # Notificar inicio
        await self.broadcast({
            'tipo': 'inicio_procesamiento',
            'datos': {
                'imagenes': len(imagenes),
                'filtros': filtros,
                'modo': modo
            }
        })
        
        # Ejecutar procesamiento en thread separado
        def ejecutar_procesamiento():
            # Crear procesador con callback adaptado
            def callback_async(info):
                try:
                    # Crear nuevo event loop para este thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.broadcast({
                        'tipo': 'progreso',
                        'datos': info
                    }))
                    loop.close()
                except Exception as e:
                    print(f"Error en callback: {e}")
            
            procesador = ProcesadorImagenes(callback_progreso=callback_async)
            
            try:
                resultados = procesador.procesar_batch(imagenes, filtros, dir_salida, modo)
                
                # Enviar resultados finales
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.broadcast({
                    'tipo': 'finalizado',
                    'datos': {
                        'resultados': resultados,
                        'mensaje': 'Procesamiento completado exitosamente'
                    }
                }))
                loop.close()
                
            except Exception as e:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.broadcast({
                    'tipo': 'error',
                    'mensaje': f'Error en el procesamiento: {str(e)}'
                }))
                loop.close()
            
            finally:
                self.procesando = False
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=ejecutar_procesamiento, daemon=True)
        thread.start()
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'aceptado',
            'mensaje': 'Procesamiento iniciado'
        })
    
    async def comando_estado(self, websocket):
        """
        Envía el estado actual del servidor
        """
        await self.enviar_mensaje(websocket, {
            'tipo': 'estado',
            'datos': {
                'procesando': self.procesando,
                'clientes_conectados': len(self.clientes)
            }
        })
    
    async def comando_cancelar(self, websocket):
        """
        Cancela el procesamiento actual (funcionalidad futura)
        """
        await self.enviar_mensaje(websocket, {
            'tipo': 'info',
            'mensaje': 'Funcionalidad de cancelación no implementada'
        })
    
    async def handler(self, websocket):
        """
        Manejador principal de conexiones WebSocket
        
        Args:
            websocket: Conexión del cliente
        """
        await self.registrar_cliente(websocket)
        
        try:
            async for mensaje in websocket:
                try:
                    comando = json.loads(mensaje)
                    await self.procesar_comando(websocket, comando)
                except json.JSONDecodeError:
                    await self.enviar_mensaje(websocket, {
                        'tipo': 'error',
                        'mensaje': 'Formato de mensaje inválido'
                    })
                except Exception as e:
                    await self.enviar_mensaje(websocket, {
                        'tipo': 'error',
                        'mensaje': f'Error al procesar comando: {str(e)}'
                    })
        finally:
            await self.desregistrar_cliente(websocket)
    
    async def iniciar(self):
        """
        Inicia el servidor WebSocket
        """
        print("="*60)
        print("🚀 SERVIDOR WEBSOCKET DE PROCESAMIENTO DE IMÁGENES")
        print("="*60)
        print(f"🌐 Host: {self.host}")
        print(f"🔌 Puerto: {self.puerto}")
        print(f"📡 Esperando conexiones...")
        print("="*60)
        
        async with websockets.serve(self.handler, self.host, self.puerto):
            await asyncio.Future()  # Ejecutar indefinidamente
    
    def ejecutar(self):
        """
        Método de conveniencia para ejecutar el servidor
        """
        try:
            asyncio.run(self.iniciar())
        except KeyboardInterrupt:
            print("\n\n👋 Servidor detenido por el usuario")


def main():
    """
    Función principal para iniciar el servidor
    """
    # Crear directorios si no existen
    Path("../input_images").mkdir(parents=True, exist_ok=True)
    Path("../output_images").mkdir(parents=True, exist_ok=True)
    
    # Crear y ejecutar servidor
    servidor = ServidorWebSocket(host='localhost', puerto=8765)
    servidor.ejecutar()


if __name__ == "__main__":
    main()
