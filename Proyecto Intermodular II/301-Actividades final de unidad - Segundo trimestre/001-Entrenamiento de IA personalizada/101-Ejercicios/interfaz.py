#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║         GastroBotChef - Interfaz conversacional              ║
║  Chat interactivo con el modelo fine-tuned de gastronomía    ║
╚══════════════════════════════════════════════════════════════╝

MODIFICACIONES FUNCIONALES:
  - Historial de conversación en memoria durante la sesión
  - Comandos especiales: /ayuda, /historial, /limpiar, /exportar, /salir
  - Exportación del historial a JSON con fecha y hora
  - Tiempo de respuesta mostrado tras cada generación
"""

import os
import sys
import json
import time
import torch
from datetime import datetime
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
MAX_NEW_TOKENS = 350
TEMPERATURE    = 0.7
TOP_P          = 0.9

SYSTEM_PROMPT = (
    "Eres GastroBotChef, un chef virtual experto en gastronomía española. "
    "Tienes un profundo conocimiento sobre recetas tradicionales, técnicas culinarias "
    "(sofrito, escabeche, pil-pil, etc.), denominaciones de origen, vinos, quesos, "
    "embutidos y la cultura gastronómica de todas las comunidades autónomas de España. "
    "Respondes siempre en español, de forma amigable, detallada y apasionada por la cocina."
)

COMANDOS = {
    "/ayuda":     "Muestra este mensaje de ayuda.",
    "/historial": "Muestra el historial de la conversación.",
    "/limpiar":   "Limpia el historial y empieza una conversación nueva.",
    "/exportar":  "Guarda el historial en un fichero JSON.",
    "/salir":     "Cierra GastroBotChef.",
}


def banner():
    print(c(MAGENTA, BOLD + """
╔══════════════════════════════════════════════════════════════╗
║         GastroBotChef - Interfaz conversacional              ║
║  Chat interactivo con el modelo fine-tuned de gastronomía    ║
╚══════════════════════════════════════════════════════════════╝
""" + RESET))
    print(c(CYAN, "  Escribe tu pregunta sobre gastronomía española."))
    print(c(AMARILLO, "  Escribe /ayuda para ver los comandos disponibles.\n"))


def mostrar_ayuda():
    print(c(CYAN, "\n📖 Comandos disponibles:"))
    for cmd, desc in COMANDOS.items():
        print(c(VERDE, f"  {cmd:<12}") + f"  {desc}")
    print()


def mostrar_historial(historial):
    if not historial:
        print(c(AMARILLO, "  El historial está vacío.\n"))
        return
    print(c(CYAN, f"\n📜 Historial ({len(historial)} mensajes):"))
    print("─" * 62)
    for msg in historial:
        if msg["role"] == "user":
            print(c(AZUL,  f"  Tú    : {msg['content']}"))
        elif msg["role"] == "assistant":
            print(c(VERDE, f"  Chef  : {msg['content']}"))
    print("─" * 62 + "\n")


def exportar_historial(historial):
    if not historial:
        print(c(AMARILLO, "  No hay historial para exportar.\n"))
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"./historial_gastrobot_{ts}.json"
    datos = {
        "sesion": ts,
        "modelo": MODEL_NAME,
        "lora_dir": LORA_DIR,
        "mensajes": historial,
    }
    with open(nombre, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(c(VERDE, f"  ✅ Historial exportado: {nombre}\n"))


def detectar_dispositivo():
    if torch.cuda.is_available():
        print(c(VERDE, "💻 GPU detectada (CUDA). Usando float16."))
        return "cuda", torch.float16
    print(c(AMARILLO, "💻 No hay GPU. Usando CPU con float32."))
    return "cpu", torch.float32


def cargar_tokenizer():
    print(c(CYAN, f"✅ Cargando tokenizer de {MODEL_NAME}..."))
    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


def cargar_modelo(device, dtype):
    print(c(CYAN, f"✅ Cargando modelo base ({MODEL_NAME})..."))
    base = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
    )
    if device == "cpu":
        base.to(device)

    if not os.path.isdir(LORA_DIR):
        print(c(AMARILLO, f"⚠️  No se encontró '{LORA_DIR}'. Usando modelo base sin fine-tuning."))
        return base

    adapter_path = os.path.join(LORA_DIR, "adapter_config.json")
    if os.path.exists(adapter_path) and PEFT_DISPONIBLE:
        print(c(CYAN, f"✅ Cargando adaptadores LoRA desde '{LORA_DIR}'..."))
        model = PeftModel.from_pretrained(
            base, LORA_DIR,
            device_map="auto" if device == "cuda" else None,
        )
        try:
            model = model.merge_and_unload()
            print(c(VERDE, "✅ LoRA fusionado con el modelo base."))
        except Exception as e:
            print(c(AMARILLO, f"ℹ️  No se fusionó el LoRA: {e}"))
        return model

    return base


def construir_prompt(tokenizer, historial_actual):
    """Construye el prompt completo con el historial de la conversación."""
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}] + historial_actual
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            mensajes, tokenize=False, add_generation_prompt=True
        )
    # Fallback sin plantilla
    partes = [f"Sistema: {SYSTEM_PROMPT}"]
    for msg in historial_actual:
        rol = "Tú" if msg["role"] == "user" else "Chef"
        partes.append(f"{rol}: {msg['content']}")
    partes.append("Chef:")
    return "\n".join(partes)


def generar_respuesta(tokenizer, model, device, historial_actual):
    prompt = construir_prompt(tokenizer, historial_actual)
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


def main():
    banner()

    device, dtype = detectar_dispositivo()
    tokenizer     = cargar_tokenizer()
    model         = cargar_modelo(device, dtype)

    print(c(VERDE, "\n✅ GastroBotChef listo. ¡Pregúntame sobre gastronomía española!\n"))
    print("─" * 62)

    historial = []

    while True:
        try:
            entrada = input(c(AZUL, BOLD + "\n  Tú: " + RESET)).strip()
        except (KeyboardInterrupt, EOFError):
            print(c(AMARILLO, "\n\n  ¡Hasta pronto! 🍽️\n"))
            break

        if not entrada:
            continue

        # ── COMANDOS ESPECIALES ───────────────────────────────────
        if entrada.lower() == "/salir":
            print(c(AMARILLO, "\n  ¡Hasta pronto! 🍽️\n"))
            break
        elif entrada.lower() == "/ayuda":
            mostrar_ayuda()
            continue
        elif entrada.lower() == "/historial":
            mostrar_historial(historial)
            continue
        elif entrada.lower() == "/limpiar":
            historial = []
            print(c(VERDE, "\n  ✅ Historial limpiado. Nueva conversación iniciada.\n"))
            continue
        elif entrada.lower() == "/exportar":
            exportar_historial(historial)
            continue

        # ── GENERACIÓN ────────────────────────────────────────────
        historial.append({"role": "user", "content": entrada})

        print(c(CYAN, "  ⏳ GastroBotChef está pensando..."), end="\r")
        t0 = time.time()
        respuesta, n_tokens = generar_respuesta(tokenizer, model, device, historial)
        t_total = time.time() - t0

        historial.append({"role": "assistant", "content": respuesta})

        print(c(VERDE, BOLD + "\n  Chef: " + RESET) + respuesta)
        print(c(AMARILLO, f"        ↳ {n_tokens} tokens generados en {t_total:.1f}s"))


if __name__ == "__main__":
    main()
