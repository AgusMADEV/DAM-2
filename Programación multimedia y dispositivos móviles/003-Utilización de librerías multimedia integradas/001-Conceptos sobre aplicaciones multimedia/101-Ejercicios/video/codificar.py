#!/usr/bin/env python3
import subprocess
import json
import argparse
from pathlib import Path
import sys

# Resoluciones 16:9 más comunes (ancho, alto, etiqueta)
COMMON_16_9_RESOLUTIONS = [
    (3840, 2160, "2160p"),
    (2560, 1440, "1440p"),
    (1920, 1080, "1080p"),
    (1280, 720,  "720p"),
    (854,  480,  "480p"),
    (640,  360,  "360p"),
    (426,  240,  "240p"),
    (256,  144,  "144p"),
]

def run_cmd(cmd):
    """Ejecuta un comando y devuelve stdout como texto. Lanza excepción si falla."""
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Error ejecutando comando: {' '.join(cmd)}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout

def get_video_resolution(input_path: Path):
    """Obtiene resolución (ancho, alto) usando ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        str(input_path),
    ]
    out = run_cmd(cmd)
    data = json.loads(out)
    try:
        stream = data["streams"][0]
        width = int(stream["width"])
        height = int(stream["height"])
        return width, height
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"No se pudo obtener la resolución del vídeo: {e}")

def choose_target_resolutions(src_width: int, src_height: int):
    """
    Devuelve la lista de resoluciones destino (w, h, label)
    que son <= a la resolución de origen (por altura).
    """
    targets = [
        (w, h, label)
        for (w, h, label) in COMMON_16_9_RESOLUTIONS
        if h <= src_height
    ]
    # Por si el vídeo es muy pequeño y no coincide con ninguna altura estándar
    if not targets:
        targets = [(src_width, src_height, f"{src_height}p_custom")]
    return targets

def encode_video(input_path: Path, output_path: Path, width: int, height: int):
    """
    Codifica una versión del vídeo con ffmpeg reescalando a width x height.
    Ajusta la relación de aspecto manteniendo el contenido.
    """
    # Puedes ajustar crf/preset a tu gusto
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path),
    ]
    print(f"Codificando {output_path.name} ({width}x{height})...")
    run_cmd(cmd)
    print(f"✔ Generado: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Genera versiones 16:9 reescaladas de un vídeo (desde la resolución original hacia abajo) y crea un JSON con los nombres."
    )
    parser.add_argument("input", help="Ruta del vídeo de entrada")
    parser.add_argument(
        "-o", "--output-dir",
        help="Directorio de salida (por defecto, el mismo del vídeo)",
        default=None,
    )
    parser.add_argument(
        "-j", "--json-name",
        help="Nombre del archivo JSON (por defecto, <basename>_renditions.json)",
        default=None,
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"ERROR: El archivo de entrada no existe: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent

    base_name = input_path.stem

    if args.json_name:
        json_path = Path(args.json_name).expanduser().resolve()
    else:
        json_path = output_dir / f"{base_name}_renditions.json"

    print(f"Analizando resolución de: {input_path}")
    src_width, src_height = get_video_resolution(input_path)
    print(f"Resolución de origen: {src_width}x{src_height}")

    targets = choose_target_resolutions(src_width, src_height)
    print("Resoluciones destino:")
    for w, h, label in targets:
        print(f" - {label}: {w}x{h}")

    renditions = []

    for w, h, label in targets:
        # 1) Nombre estándar de vídeo independiente del nombre original
        out_name = f"video_{label}.mp4"
        out_path = output_dir / out_name
        encode_video(input_path, out_path, w, h)

        # 2) En el JSON solo guardamos el nombre del fichero, no la ruta completa
        renditions.append({
            "label": label,
            "width": w,
            "height": h,
            "filename": out_name,
        })

    # Guardar JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "input_file": str(input_path),
                "source_width": src_width,
                "source_height": src_height,
                "renditions": renditions,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n✔ JSON generado: {json_path}")
    print("Contenido de ejemplo:")
    print(json.dumps({"renditions": renditions}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

