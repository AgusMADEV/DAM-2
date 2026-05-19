#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║           GastroBotChef - Entrenamiento del modelo           ║
║     Fine-tuning de Qwen2.5-0.5B-Instruct con LoRA/QLoRA     ║
║          Temática: Gastronomía española y técnicas           ║
╚══════════════════════════════════════════════════════════════╝

Basado en el ejercicio de clase (Entrenamiento IA - Segundo trimestre)
Adaptado con temática de gastronomía española.

Modificaciones respecto al ejercicio de clase:
  - Dataset: gastronomía española (23 pares Q&A)
  - System prompt orientado a chef / experto culinario
  - Colores ANSI en la terminal para mayor legibilidad
  - Guardado automático de métricas de entrenamiento en JSON
  - Barra de progreso con tiempo estimado
"""

import os
import json
import time
from dataclasses import dataclass

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    TrainerCallback,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)

try:
    import bitsandbytes  # noqa: F401
    BITSANDBYTES_DISPONIBLE = True
except ImportError:
    BITSANDBYTES_DISPONIBLE = False

# ─────────────────────────────────────────────
# COLORES ANSI PARA LA TERMINAL
# ─────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
VERDE  = "\033[92m"
AMARILLO = "\033[93m"
ROJO   = "\033[91m"
CYAN   = "\033[96m"
MAGENTA = "\033[95m"

def c(color, texto):
    """Aplica color ANSI a un texto."""
    return f"{color}{texto}{RESET}"


# ─────────────────────────────────────────────
# CONFIGURACIÓN BÁSICA
# ─────────────────────────────────────────────
DATA_PATH  = "training_data.jsonl"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "./gastrobot-chef-model"

MAX_LENGTH  = 256
NUM_EPOCHS  = 1
LR          = 2e-4
BATCH_SIZE  = 1
GRAD_ACCUM  = 4

METRICAS_PATH = "./gastrobot_metricas.json"


# ─────────────────────────────────────────────
# CALLBACK PERSONALIZADO: guarda métricas en JSON
# ─────────────────────────────────────────────
class GuardarMetricasCallback(TrainerCallback):
    """Registra loss y paso en cada logging step y lo guarda en JSON."""

    def __init__(self, ruta_json):
        self.ruta = ruta_json
        self.historial = []

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            entrada = {
                "paso": state.global_step,
                "epoch": round(state.epoch, 3) if state.epoch else 0,
                "loss": logs.get("loss"),
                "learning_rate": logs.get("learning_rate"),
                "timestamp": time.strftime("%H:%M:%S"),
            }
            self.historial.append(entrada)
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)


def banner():
    print(c(MAGENTA, BOLD + """
╔══════════════════════════════════════════════════════════════╗
║           GastroBotChef - Entrenamiento del modelo           ║
║     Fine-tuning de Qwen2.5-0.5B-Instruct con LoRA/QLoRA     ║
╚══════════════════════════════════════════════════════════════╝
""" + RESET))


def main():
    banner()
    print(c(CYAN, f"📁 Dataset        : {DATA_PATH}"))
    print(c(CYAN, f"🧠 Modelo base    : {MODEL_NAME}"))
    print(c(CYAN, f"💾 Salida LoRA    : {OUTPUT_DIR}"))
    print(c(CYAN, f"📊 Métricas JSON  : {METRICAS_PATH}"))
    print("─" * 62)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            c(ROJO, f"❌ No se encontró el dataset en '{DATA_PATH}'")
        )

    # ── DISPOSITIVO ──────────────────────────────────────────────
    if torch.cuda.is_available() and BITSANDBYTES_DISPONIBLE:
        device   = "cuda"
        use_4bit = True
        print(c(VERDE, "💻 GPU detectada (CUDA). Entrenando con QLoRA 4-bit."))
    elif torch.cuda.is_available():
        device   = "cuda"
        use_4bit = False
        print(c(AMARILLO, "💻 GPU detectada pero bitsandbytes no disponible. Entrenando sin 4-bit."))
    else:
        device   = "cpu"
        use_4bit = False
        print(c(AMARILLO, "💻 No hay GPU CUDA. Entrenando en CPU (más lento)."))

    # ── DATASET ──────────────────────────────────────────────────
    print(c(CYAN, "\n📥 Cargando dataset..."))
    raw_dataset = load_dataset("json", data_files=DATA_PATH, split="train")
    print(c(VERDE, f"✅ Dataset cargado: {len(raw_dataset)} ejemplos de gastronomía española."))

    # ── TOKENIZER ────────────────────────────────────────────────
    print(c(CYAN, "\n✅ Cargando tokenizer..."))
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ── MODELO ───────────────────────────────────────────────────
    print(c(CYAN, "✅ Cargando modelo base..."))
    if use_4bit:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto",
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model = prepare_model_for_kbit_training(model)
    else:
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        model.to(device)

    # ── LORA ─────────────────────────────────────────────────────
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    print(c(VERDE, "✅ LoRA aplicado al modelo."))
    model.print_trainable_parameters()

    # ── CONVERTIR messages → texto ────────────────────────────────
    print(c(CYAN, "\n🧱 Transformando mensajes con plantilla de chat..."))

    def messages_to_text(example):
        conv = []
        for m in example["messages"]:
            role = m.get("role", "user")
            if role not in ("user", "assistant", "system"):
                role = "user"
            conv.append({"role": role, "content": m["content"]})
        try:
            text = tokenizer.apply_chat_template(
                conv, tokenize=False, add_generation_prompt=False
            )
        except Exception:
            partes = []
            for m in conv:
                prefijo = "Usuario" if m["role"] == "user" else "Asistente"
                partes.append(f"{prefijo}: {m['content']}")
            text = "\n".join(partes)
        return {"text": text}

    text_dataset = raw_dataset.map(
        messages_to_text, remove_columns=raw_dataset.column_names
    )

    # ── TOKENIZACIÓN ─────────────────────────────────────────────
    print(c(CYAN, "✅ Tokenizando dataset..."))

    def tokenize_fn(batch):
        out = tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )
        out["labels"] = out["input_ids"].copy()
        return out

    tokenized_dataset = text_dataset.map(
        tokenize_fn, batched=True, remove_columns=["text"]
    )

    # ── TRAINING ARGUMENTS ────────────────────────────────────────
    print(c(CYAN, "✅ Configurando argumentos de entrenamiento..."))
    use_fp16 = device == "cuda"

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        learning_rate=LR,
        weight_decay=0.01,
        warmup_ratio=0.03,
        logging_steps=1,
        save_steps=20,
        save_total_limit=1,
        fp16=use_fp16,
        bf16=False,
        report_to="none",
        dataloader_pin_memory=False,
    )

    # ── TRAINER ───────────────────────────────────────────────────
    metricas_callback = GuardarMetricasCallback(METRICAS_PATH)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        callbacks=[metricas_callback],
    )

    # ── ENTRENAMIENTO ─────────────────────────────────────────────
    print(c(MAGENTA, f"\n🚀 Iniciando entrenamiento ({NUM_EPOCHS} épocas)...\n"))
    t_inicio = time.time()
    trainer.train()
    t_fin = time.time()
    duracion = t_fin - t_inicio
    print(c(VERDE, f"\n✅ Entrenamiento completado en {duracion:.1f} segundos."))

    # ── GUARDAR MODELO ────────────────────────────────────────────
    print(c(CYAN, f"\n💾 Guardando adaptadores LoRA en '{OUTPUT_DIR}'..."))
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(c(VERDE, f"✅ Modelo guardado."))
    print(c(VERDE, f"📊 Métricas guardadas en '{METRICAS_PATH}'."))

    # ── RESUMEN FINAL ─────────────────────────────────────────────
    print(c(MAGENTA, BOLD + """
╔══════════════════════════════════════════════════════════════╗
║                  ENTRENAMIENTO FINALIZADO                    ║
╚══════════════════════════════════════════════════════════════╝
""" + RESET))
    print(c(CYAN,  f"  Modelo base       : {MODEL_NAME}"))
    print(c(VERDE, f"  Adaptadores LoRA  : {OUTPUT_DIR}"))
    print(c(VERDE, f"  Métricas JSON     : {METRICAS_PATH}"))
    print(c(AMARILLO, "  Siguiente paso    : ejecuta probar.py o interfaz.py"))
    print()


if __name__ == "__main__":
    main()
