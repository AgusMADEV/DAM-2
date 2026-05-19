#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Render a code file as a slick macOS-style editor image (transparent PNG)
- Ubuntu Mono font
- Rounded black editor
- macOS window controls
- Line numbers
- Optional syntax highlighting (Pygments)
- High-quality antialiasing via 2x render + downscale
"""

from __future__ import annotations

import sys
import math
from pathlib import Path
from typing import List, Tuple, Optional

from PIL import Image, ImageDraw, ImageFont

# =============================
# RENDER SCALE (for antialias)
# =============================
SCALE = 2  # render at 2x and downscale

# =============================
# IMAGE CONFIG
# =============================
OUT_W = 800
OUT_H = 400
PADDING = 24

BOX_RADIUS = 22
BOX_BG = (10, 10, 12, 235)
BOX_STROKE = (255, 255, 255, 28)

TITLEBAR_H = 44
TITLE_TEXT_COLOR = (235, 235, 235, 220)

CODE_TEXT_COLOR = (230, 230, 235, 235)
LINENO_COLOR = (170, 170, 175, 140)

INNER_PAD_X = 18
INNER_PAD_Y = 14
GUTTER_GAP = 14

LINE_SPACING = 6
TAB_SIZE = 4
WRAP_LONG_LINES = True

# =============================
# MAC BUTTONS
# =============================
BTN_R = 7
BTN_GAP = 8
BTN_LEFT = 18
BTN_Y = 22

MAC_RED = (255, 95, 86, 235)
MAC_YELLOW = (255, 189, 46, 235)
MAC_GREEN = (39, 201, 63, 235)

# =============================
# FONTS (FORCED)
# =============================
UBUNTU_MONO = "UbuntuMono-R.ttf"
CODE_FONT_SIZE = 16
TITLE_FONT_SIZE = 16

# =============================
# OPTIONAL: PYGMENTS
# =============================
USE_PYGMENTS = True


# -----------------------------
# Helpers
# -----------------------------
def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size=size)
    except Exception:
        raise RuntimeError(f"Font not found: {path}")


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def expand_tabs(s: str) -> str:
    return s.expandtabs(TAB_SIZE)


def try_pygments():
    if not USE_PYGMENTS:
        return None
    try:
        from pygments import lex
        from pygments.lexers import guess_lexer_for_filename, TextLexer
        return lex, guess_lexer_for_filename, TextLexer
    except Exception:
        return None


def token_palette(ttype: str):
    if "Comment" in ttype:
        return (120, 160, 130, 220)
    if "String" in ttype:
        return (180, 220, 160, 235)
    if "Keyword" in ttype:
        return (140, 190, 255, 235)
    if "Number" in ttype:
        return (255, 210, 140, 235)
    if "Name.Builtin" in ttype:
        return (255, 170, 240, 235)
    return CODE_TEXT_COLOR


# -----------------------------
# Main
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 code_to_image.py file.py [out.png]")
        sys.exit(1)

    in_file = Path(sys.argv[1]).resolve()
    out_file = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else in_file.with_suffix(".png")
    )

    lines = in_file.read_text(encoding="utf-8", errors="replace").splitlines()
    lines = [expand_tabs(l) for l in lines]

    # ---------- 2x canvas ----------
    W, H = OUT_W * SCALE, OUT_H * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ---------- fonts ----------
    code_font = load_font(UBUNTU_MONO, CODE_FONT_SIZE * SCALE)
    title_font = load_font(UBUNTU_MONO, TITLE_FONT_SIZE * SCALE)

    # ---------- window ----------
    px = PADDING * SCALE
    x0, y0 = px, px
    x1, y1 = W - px, H - px

    rounded_rect(
        draw,
        (x0, y0, x1, y1),
        BOX_RADIUS * SCALE,
        BOX_BG,
        BOX_STROKE,
        width=1 * SCALE,
    )

    # ---------- mac buttons ----------
    cy = y0 + BTN_Y * SCALE
    cx = x0 + BTN_LEFT * SCALE
    for c in (MAC_RED, MAC_YELLOW, MAC_GREEN):
        draw.ellipse(
            (cx - BTN_R * SCALE, cy - BTN_R * SCALE,
             cx + BTN_R * SCALE, cy + BTN_R * SCALE),
            fill=c,
        )
        cx += (BTN_R * 2 + BTN_GAP) * SCALE

    # ---------- title ----------
    title = in_file.name
    tw = draw.textlength(title, font=title_font)
    tx = x0 + ((x1 - x0) - tw) / 2
    ty = y0 + (TITLEBAR_H * SCALE - TITLE_FONT_SIZE * SCALE) / 2
    draw.text((tx, ty), title, font=title_font, fill=TITLE_TEXT_COLOR)

    # ---------- code layout ----------
    inner_left = x0 + INNER_PAD_X * SCALE
    inner_top = y0 + (TITLEBAR_H + INNER_PAD_Y) * SCALE
    inner_right = x1 - INNER_PAD_X * SCALE
    inner_bottom = y1 - INNER_PAD_Y * SCALE

    ascent, descent = code_font.getmetrics()
    line_h = ascent + descent + LINE_SPACING * SCALE

    lineno_digits = len(str(len(lines)))
    gutter_w = int(draw.textlength("9" * lineno_digits, font=code_font)) + 8 * SCALE
    code_x = inner_left + gutter_w + GUTTER_GAP * SCALE
    max_code_w = inner_right - code_x

    pyg = try_pygments()

    y = inner_top
    if pyg:
        lex, guess_lexer, TextLexer = pyg
        try:
            lexer = guess_lexer(in_file.name, "\n".join(lines))
        except Exception:
            lexer = TextLexer()
        tokens = list(lex("\n".join(lines), lexer))

        line_tokens = [[]]
        for ttype, value in tokens:
            parts = value.split("\n")
            for i, p in enumerate(parts):
                if i > 0:
                    line_tokens.append([])
                if p:
                    line_tokens[-1].append((p, token_palette(str(ttype))))

        for i, segs in enumerate(line_tokens, start=1):
            if y + line_h > inner_bottom:
                break
            ln = str(i).rjust(lineno_digits)
            draw.text((inner_left, y), ln, font=code_font, fill=LINENO_COLOR)

            x = code_x
            for txt, col in segs:
                draw.text((x, y), txt, font=code_font, fill=col)
                x += draw.textlength(txt, font=code_font)
                if x > code_x + max_code_w:
                    break
            y += line_h
    else:
        for i, line in enumerate(lines, start=1):
            if y + line_h > inner_bottom:
                break
            ln = str(i).rjust(lineno_digits)
            draw.text((inner_left, y), ln, font=code_font, fill=LINENO_COLOR)
            draw.text((code_x, y), line, font=code_font, fill=CODE_TEXT_COLOR)
            y += line_h

    # ---------- downscale (antialias) ----------
    img = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    img.save(out_file, "PNG")
    print(f"OK → {out_file}")


if __name__ == "__main__":
    main()

