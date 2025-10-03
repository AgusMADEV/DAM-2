#!/usr/bin/env python3
"""
coder.py — Codificador/decodificador de texto en imágenes RGB.

Este script permite convertir un texto (UTF-8) en una imagen cuadrada de píxeles RGB,
y posteriormente recuperar exactamente el texto original desde la imagen.

Formato de almacenamiento dentro de la imagen:
    [ MAGIC (4 bytes = "MSG1") ]
    [ LENGTH (4 bytes, entero big-endian) ]
    [ CRC32 (4 bytes, entero big-endian) ]
    [ PAYLOAD (bytes del texto en UTF-8) ]
    [ Relleno hasta múltiplo de 3 ]

Cada píxel almacena exactamente 3 bytes (R,G,B).
El relleno asegura que todos los píxeles estén completos.
El CRC32 permite detectar corrupción de datos.

Uso:
    # Codificar texto directo
    python coder.py encode -t "¡Hola mundo!" -o mensaje.png

    # Codificar desde archivo de texto
    python coder.py encode -f entrada.txt -o mensaje.png

    # Decodificar y mostrar texto
    python coder.py decode -i mensaje.png

    # Decodificar y guardar en archivo
    python coder.py decode -i mensaje.png -o salida.txt

    # Decodificar como bytes crudos
    python coder.py decode -i mensaje.png --raw-bytes -o datos.bin
"""

from PIL import Image
import math
import argparse
import zlib
import sys
from pathlib import Path

# Constante de identificación de nuestras imágenes
MAGIC = b"MSG1"  # 4 bytes


def bytes_to_pixels(payload: bytes):
    """
    Convierte un flujo de bytes en una cuadrícula de píxeles RGB.

    Args:
        payload (bytes): Secuencia de bytes a codificar.

    Returns:
        tuple:
            - payload_padded (bytes): Bytes con relleno para múltiplo de 3.
            - side (int): Dimensión del lado de la imagen cuadrada.
    """
    # Relleno a múltiplos de 3 (RGB)
    pad_len = (3 - (len(payload) % 3)) % 3
    payload_padded = payload + b"\x00" * pad_len

    # Calcular tamaño de imagen cuadrada
    num_pixels = len(payload_padded) // 3
    side = math.ceil(math.sqrt(num_pixels))
    return payload_padded, side


def encode_to_image(text_bytes: bytes, out_path: str, img_format: str = "PNG"):
    """
    Codifica bytes de texto en una imagen RGB cuadrada.

    Args:
        text_bytes (bytes): Contenido a codificar (en UTF-8).
        out_path (str): Ruta de salida para la imagen.
        img_format (str): Formato de imagen (PNG, BMP, etc.).
    """
    length = len(text_bytes)
    crc = zlib.crc32(text_bytes) & 0xFFFFFFFF

    # Cabecera: magic + longitud + CRC
    header = MAGIC + length.to_bytes(4, "big") + crc.to_bytes(4, "big")
    payload = header + text_bytes

    payload_padded, side = bytes_to_pixels(payload)

    img = Image.new("RGB", size=(side, side), color=(0, 0, 0))
    pixels = img.load()

    # Escribir secuencialmente bytes en los píxeles
    idx = 0
    total = len(payload_padded)
    for y in range(side):
        for x in range(side):
            if idx + 3 <= total:
                r = payload_padded[idx]
                g = payload_padded[idx + 1]
                b = payload_padded[idx + 2]
                pixels[x, y] = (r, g, b)
                idx += 3
            else:
                break

    img.save(out_path, format=img_format.upper())


def decode_from_image(in_path: str) -> bytes:
    """
    Decodifica bytes desde una imagen RGB con formato definido.

    Args:
        in_path (str): Ruta de la imagen de entrada.

    Returns:
        bytes: Texto original en bytes UTF-8.

    Raises:
        ValueError: Si la imagen no contiene cabecera válida o los datos están corruptos.
    """
    img = Image.open(in_path).convert("RGB")
    w, h = img.size
    pixels = img.load()

    # Recuperar todos los bytes en el mismo orden de escritura
    data = bytearray()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            data.extend((r, g, b))

    if len(data) < 12:
        raise ValueError("Imagen demasiado pequeña para contener cabecera.")

    if bytes(data[0:4]) != MAGIC:
        raise ValueError("Magic inválido: la imagen no contiene un mensaje válido (MSG1).")

    length = int.from_bytes(data[4:8], "big")
    crc_expected = int.from_bytes(data[8:12], "big")

    start = 12
    end = start + length
    if end > len(data):
        raise ValueError("La imagen no contiene todos los bytes anunciados por la longitud.")

    payload = bytes(data[start:end])
    crc_actual = zlib.crc32(payload) & 0xFFFFFFFF

    if crc_actual != crc_expected:
        raise ValueError(
            f"CRC no coincide: esperado {crc_expected:#010x}, obtenido {crc_actual:#010x}. Datos corruptos."
        )

    return payload


def main():
    """Punto de entrada principal: parsea argumentos y ejecuta encode/decode."""
    parser = argparse.ArgumentParser(
        description="Codifica/decodifica texto en una imagen RGB con cabecera y CRC."
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # Subcomando: encode
    p_enc = sub.add_parser("encode", help="Codifica texto en imagen")
    src = p_enc.add_mutually_exclusive_group(required=True)
    src.add_argument("-t", "--text", help="Texto directo a codificar (UTF-8)")
    src.add_argument("-f", "--text-file", help="Archivo de texto a codificar (se lee como UTF-8)")
    p_enc.add_argument("-o", "--output", required=True, help="Ruta de salida de la imagen (ej: salida.png)")
    p_enc.add_argument("--format", default=None, help="Formato de imagen (PNG por defecto si no se deduce por extensión)")

    # Subcomando: decode
    p_dec = sub.add_parser("decode", help="Decodifica imagen a texto")
    p_dec.add_argument("-i", "--input", required=True, help="Imagen de entrada")
    p_dec.add_argument("-o", "--output", help="Archivo de salida para el texto (si se omite, imprime por stdout)")
    p_dec.add_argument("--raw-bytes", action="store_true", help="Guardar bytes tal cual (sin decodificar UTF-8)")

    args = parser.parse_args()

    if args.mode == "encode":
        # Obtener texto
        if args.text is not None:
            text_bytes = args.text.encode("utf-8")
        else:
            text_bytes = Path(args.text_file).read_text(encoding="utf-8").encode("utf-8")

        # Detectar formato de imagen si no se especifica
        img_format = args.format
        if img_format is None:
            suffix = Path(args.output).suffix.lower()
            img_format = "PNG" if suffix == "" else suffix.lstrip(".").upper()

        encode_to_image(text_bytes, args.output, img_format=img_format)

    elif args.mode == "decode":
        payload = decode_from_image(args.input)
        if args.raw_bytes:
            # Guardar bytes en bruto
            if args.output:
                Path(args.output).write_bytes(payload)
            else:
                sys.stderr.write("Advertencia: mostrando bytes en bruto por stdout.\n")
                sys.stdout.buffer.write(payload)
        else:
            # Decodificar como UTF-8
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("Los datos no son UTF-8 válidos. Use --raw-bytes para extraerlos sin decodificar.")
            if args.output:
                Path(args.output).write_text(text, encoding="utf-8")
            else:
                print(text)


if __name__ == "__main__":
    main()

