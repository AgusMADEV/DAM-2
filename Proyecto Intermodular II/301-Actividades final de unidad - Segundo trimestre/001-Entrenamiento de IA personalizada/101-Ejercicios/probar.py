#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║       GastroBotChef - Comparativa ANTES vs DESPUÉS          ║
║   Demuestra el diferencial del modelo antes y tras el        ║
║       fine-tuning sobre gastronomía española                 ║
╚══════════════════════════════════════════════════════════════╝

MODIFICACIONES FUNCIONALES respecto al ejercicio de clase:
  1. Modo ANTES/DESPUÉS: lanza el mismo modelo base y el fine-tuned
     con las mismas preguntas y compara las respuestas en pantalla.
  2. Exporta la comparativa completa a un fichero JSON para
     documentación del proyecto.
  3. Calcula y muestra la longitud de respuesta (nº de tokens) de
     cada modelo como métrica objetiva de mejora.
"""

import os
import sys
import json
import time
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

try:
    from peft import PeftModel
    PEFT_DISPONIBLE = True
except ImportError:
    PEFT_DISPONIBLE = False

# ─────────────────────────────────────────────
# COLORES ANSI
# ─────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERDE    = "\033[92m"
AMARILLO = "\033[93m"
ROJO     = "\033[91m"
CYAN     = "\033[96m"
MAGENTA  = "\033[95m"
AZUL     = "\033[94m"

def c(color, texto):
    return f"{color}{texto}{RESET}"


# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
MODEL_NAME     = "Qwen/Qwen2.5-0.5B-Instruct"
LORA_DIR       = "./gastrobot-chef-model"
MAX_NEW_TOKENS = 300
TEMPERATURE    = 0.7
TOP_P          = 0.9

EXPORTAR_JSON  = "./comparativa_antes_despues.json"

# Preguntas de prueba que demuestran el diferencial
PREGUNTAS_TEST = [
    "¿Cómo se hace el sofrito perfecto para una paella valenciana?",
    "¿Qué diferencia hay entre el gazpacho y el salmorejo?",
    "Explícame la técnica del pil-pil del bacalao paso a paso.",
    "¿Cuáles son las variedades de aceite de oliva más importantes en España?",
    "¿Cómo se consigue el socarrat en la paella?",
]


def banner():
    print(c(MAGENTA, BOLD + """
╔══════════════════════════════════════════════════════════════╗
║       GastroBotChef - Comparativa ANTES vs DESPUÉS          ║
╚══════════════════════════════════════════════════════════════╝
""" + RESET))


def detectar_dispositivo():
    if torch.cuda.is_available():
        print(c(VERDE, "💻 GPU detectada (CUDA). Usando float16."))
        return "cuda", torch.float16
    print(c(AMARILLO, "💻 No hay GPU. Usando CPU con float32."))
    return "cpu", torch.float32


def cargar_tokenizer(nombre_modelo):
    print(c(CYAN, f"✅ Cargando tokenizer de {nombre_modelo}..."))
    tok = AutoTokenizer.from_pretrained(nombre_modelo)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


def cargar_modelo_base(nombre_modelo, device, dtype):
    print(c(CYAN, f"✅ Cargando modelo base ({nombre_modelo})..."))
    modelo = AutoModelForCausalLM.from_pretrained(
        nombre_modelo,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
    )
    if device == "cpu":
        modelo.to(device)
    return modelo


def cargar_modelo_finetuned(modelo_base, lora_dir, device):
    """
    Carga los adaptadores LoRA sobre el modelo base.
    Si no existe la carpeta, avisa al usuario y devuelve None.
    """
    if not os.path.isdir(lora_dir):
        print(c(ROJO, f"⚠️  La carpeta '{lora_dir}' no existe."))
        print(c(AMARILLO, "   Ejecuta primero entrenar.py para generar el modelo fine-tuned."))
        return None

    adapter_path = os.path.join(lora_dir, "adapter_config.json")

    if os.path.exists(adapter_path):
        if not PEFT_DISPONIBLE:
            print(c(ROJO, "❌ 'peft' no instalado. Ejecuta: pip install peft"))
            return None
        print(c(CYAN, f"✅ Cargando adaptadores LoRA desde '{lora_dir}'..."))
        modelo = PeftModel.from_pretrained(
            modelo_base,
            lora_dir,
            device_map="auto" if device == "cuda" else None,
        )
        try:
            modelo = modelo.merge_and_unload()
            print(c(VERDE, "✅ LoRA fusionado con el modelo base."))
        except Exception as e:
            print(c(AMARILLO, f"ℹ️  No se fusionó el LoRA: {e}"))
        return modelo

    # Fallback: intentar cargar como modelo completo
    print(c(AMARILLO, "⚠️  No se encontró adapter_config.json. Intentando cargar como modelo completo..."))
    try:
        modelo = AutoModelForCausalLM.from_pretrained(lora_dir)
        if device == "cpu":
            modelo.to(device)
        return modelo
    except Exception as e:
        print(c(ROJO, f"❌ No se pudo cargar el modelo fine-tuned: {e}"))
        return None


def construir_prompt(tokenizer, pregunta: str) -> str:
    """Construye el prompt usando la plantilla de chat de Qwen."""
    mensajes = [
        {
            "role": "system",
            "content": (
                "Eres GastroBotChef, un experto en gastronomía española con profundos "
                "conocimientos sobre recetas tradicionales, técnicas culinarias, "
                "denominaciones de origen y cultura gastronómica de España. "
                "Respondes siempre en español de forma detallada y precisa."
            ),
        },
        {"role": "user", "content": pregunta},
    ]
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            mensajes, tokenize=False, add_generation_prompt=True
        )
    return f"Sistema: Eres GastroBotChef, experto en gastronomía española.\nUsuario: {pregunta}\nAsistente:"


def generar_respuesta(tokenizer, model, device, prompt: str) -> tuple[str, int]:
    """
    Genera una respuesta y devuelve (texto, nº_tokens_generados).
    """
    model.eval()
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    generados = output_ids[0][inputs["input_ids"].shape[-1]:]
    texto = tokenizer.decode(generados, skip_special_tokens=True).strip()
    return texto, len(generados)


def separador(titulo=""):
    linea = "─" * 62
    if titulo:
        espacio = (62 - len(titulo) - 2) // 2
        print(c(CYAN, f"{'─'*espacio} {titulo} {'─'*espacio}"))
    else:
        print(c(CYAN, linea))


def main():
    banner()

    device, dtype = detectar_dispositivo()
    tokenizer     = cargar_tokenizer(MODEL_NAME)
    modelo_base   = cargar_modelo_base(MODEL_NAME, device, dtype)
    modelo_ft     = cargar_modelo_finetuned(modelo_base, LORA_DIR, device)

    if modelo_ft is None:
        print(c(AMARILLO, "\n⚠️  Solo se probará el modelo BASE (sin fine-tuning)."))
        solo_base = True
    else:
        solo_base = False

    resultados = []

    for i, pregunta in enumerate(PREGUNTAS_TEST, 1):
        separador(f"Pregunta {i}/{len(PREGUNTAS_TEST)}")
        print(c(BOLD, f"❓ {pregunta}\n"))

        # ── ANTES (modelo base) ───────────────────────────────────
        prompt = construir_prompt(tokenizer, pregunta)
        print(c(AZUL, "📌 ANTES (modelo base sin entrenar):"))
        t0 = time.time()
        resp_antes, tok_antes = generar_respuesta(tokenizer, modelo_base, device, prompt)
        t_antes = time.time() - t0
        print(f"   {resp_antes}")
        print(c(AMARILLO, f"   ↳ {tok_antes} tokens | {t_antes:.1f}s\n"))

        # ── DESPUÉS (modelo fine-tuned) ───────────────────────────
        if not solo_base:
            print(c(VERDE, "✅ DESPUÉS (GastroBotChef fine-tuned):"))
            t0 = time.time()
            resp_despues, tok_despues = generar_respuesta(tokenizer, modelo_ft, device, prompt)
            t_despues = time.time() - t0
            print(f"   {resp_despues}")
            print(c(VERDE, f"   ↳ {tok_despues} tokens | {t_despues:.1f}s\n"))
        else:
            resp_despues, tok_despues, t_despues = None, 0, 0

        resultados.append({
            "pregunta": pregunta,
            "antes": {
                "respuesta": resp_antes,
                "tokens": tok_antes,
                "tiempo_s": round(t_antes, 2),
            },
            "despues": {
                "respuesta": resp_despues,
                "tokens": tok_despues,
                "tiempo_s": round(t_despues, 2),
            } if not solo_base else None,
        })

    # ── EXPORTAR JSON ─────────────────────────────────────────────
    separador("Exportando resultados")
    with open(EXPORTAR_JSON, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(c(VERDE, f"✅ Comparativa exportada a '{EXPORTAR_JSON}'"))

    # ── RESUMEN DE MÉTRICAS ───────────────────────────────────────
    if not solo_base:
        separador("Resumen de métricas")
        total_antes   = sum(r["antes"]["tokens"]   for r in resultados)
        total_despues = sum(r["despues"]["tokens"]  for r in resultados)
        print(c(AZUL,  f"  Tokens generados (antes)   : {total_antes}"))
        print(c(VERDE, f"  Tokens generados (después)  : {total_despues}"))
        diferencial = total_despues - total_antes
        signo = "+" if diferencial >= 0 else ""
        print(c(AMARILLO, f"  Diferencial                 : {signo}{diferencial} tokens"))

    print(c(MAGENTA, "\n🍽️  GastroBotChef - Comparativa completada.\n"))


if __name__ == "__main__":
    main()
