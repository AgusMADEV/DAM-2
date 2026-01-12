"""
Cliente para comunicación con Ollama
Gestiona las peticiones al servidor de Ollama
Basado en el código de la actividad 102 de PSP
"""

import requests
import json

class OllamaClient:
    """Cliente para interactuar con Ollama - Basado en código de PSP"""
    
    def __init__(self, base_url="http://localhost:11434", model="qwen2.5:7b-instruct-q4_0"):
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        
    def check_connection(self):
        """Verificar si Ollama está disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt, system_prompt=None, temperature=0.7):
        """
        Generar respuesta usando Ollama (código adaptado de consulta_blog.py)
        """
        try:
            # Construir el prompt completo
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            print(f"[IA] Consultando Ollama (modelo: {self.model})...")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"[ERROR] Ollama: {response.status_code}")
                return None
                
        except requests.Timeout:
            print("[ERROR] Timeout esperando respuesta de Ollama")
            return None
        except Exception as e:
            print(f"[ERROR] Error generando respuesta: {e}")
            return None


# Instancia global (patrón usado en clase)
_ollama_client = None

def get_ollama_client():
    """Obtener instancia global del cliente Ollama"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
