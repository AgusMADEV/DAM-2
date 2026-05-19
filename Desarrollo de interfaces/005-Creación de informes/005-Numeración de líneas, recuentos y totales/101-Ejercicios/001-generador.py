#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
code_to_image.py
Render a code file into a transparent PNG "editor window" image.

Dependencies:
  - pillow
Optional (for syntax highlighting):
  - pygments

Install:
  pip install pillow
  pip install pygments   # optional
"""

from __future__ import annotations

import os
import sys
import math
import textwrap
from pathlib import Path
from typing import List, Tuple, Optional

from PIL import Image, ImageDraw, ImageFont

# -----------------------------
# CONFIG (edit these)
# -----------------------------
OUT_W = 800
OUT_H = 400
PADDING = 24

# Editor window box
BOX_RADIUS = 22
BOX_BG = (10, 10, 12, 235)        # near-black, slightly translucent
BOX_STROKE = (255, 255, 255, 28)  # subtle border

# Title bar
TITLEBAR_H = 44
TITLE_TEXT_COLOR = (235, 235, 235, 220)
TITLE_FONT_SIZE = 16

# Code area
CODE_FONT_SIZE = 16
LINE_SPACING = 6
CODE_TEXT_COLOR = (230, 230, 235, 235)
LINENO_COLOR = (170, 170, 175, 140)
LINENO_BG = None  # e.g. (255,255,255,10) if you want a subtle strip

# Layout
INNER_PAD_X = 18
INNER_PAD_Y = 14
GUTTER_GAP = 14           # gap between line numbers and code
MAX_LINES = None          # set e.g. 200 to hard-limit

# Mac buttons
BTN_R = 7
BTN_GAP = 8
BTN_LEFT = 18
BTN_Y = 22  # relative to titlebar top

MAC_RED = (255, 95, 86, 235)
MAC_YELLOW = (255, 189, 46, 235)
MAC_GREEN = (39, 201, 63, 235)

# Fonts (provide paths if you want exact fonts)
# If None, the script tries common monospace fonts.
MONO_FONT_PATH = None
TITLE_FONT_PATH = None

# Tabs/spaces
TAB_SIZE = 4

# Wrapping: set True to wrap long lines to fit the image
WRAP_LONG_LINES = True

# -----------------------------
# Optional Pygments highlighting
# -----------------------------
USE_PYGMENTS_IF_AVAILABLE = True


# -----------------------------
# Helpers
# -----------------------------
def load_font(preferred_path: Optional[str], size: int, monospace: bool = False) -> ImageFont.FreeTypeFont:
    """
    Try to load a TTF/OTF font. Falls back to PIL default if needed.
    """
    candidates = []
    if preferred_path:
        candidates.append(preferred_path)

    if monospace:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/Library/Fonts/Menlo.ttc",
            "C:\\Windows\\Fonts\\consola.ttf",
        ]
    else:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/Library/Fonts/Arial.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]

    for p in candidates:
        try:
            if p and os.path.exists(p):
                return ImageFont.truetype(p, size=size)
        except Exception:
            pass

    # Last resort
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], r: int, fill, outline=None, width: int = 1):
    """
    Draw a rounded rectangle with Pillow.
    """
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def ellipsize(text: str, font: ImageFont.FreeTypeFont, max_w: int, draw: ImageDraw.ImageDraw) -> str:
    """
    Truncate text with ellipsis to fit width.
    """
    if draw.textlength(text, font=font) <= max_w:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        candidate = text[:mid] + ell
        if draw.textlength(candidate, font=font) <= max_w:
            lo = mid + 1
        else:
            hi = mid
    return text[: max(0, lo - 1)] + ell


def expand_tabs(s: str, tab_size: int) -> str:
    return s.expandtabs(tab_size)


def split_and_wrap_lines(lines: List[str], font: ImageFont.FreeTypeFont, max_text_w: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """
    Wrap long lines to fit max_text_w. Keeps indentation visually.
    """
    if not WRAP_LONG_LINES:
        return lines

    wrapped: List[str] = []
    for line in lines:
        # Keep newline-free
        raw = line.rstrip("\n")
        if not raw:
            wrapped.append("")
            continue

        # If it already fits, keep it
        if draw.textlength(raw, font=font) <= max_text_w:
            wrapped.append(raw)
            continue

        # Preserve leading spaces as indentation for wrapped segments
        leading = len(raw) - len(raw.lstrip(" "))
        indent = " " * leading
        rest = raw.lstrip(" ")

        # We wrap by measuring words, but code often has long tokens.
        # So we do a character-based greedy wrap.
        current = ""
        for ch in rest:
            test = (current + ch)
            if draw.textlength(indent + test, font=font) <= max_text_w:
                current = test
            else:
                wrapped.append(indent + current)
                current = ch
        if current:
            wrapped.append(indent + current)

    return wrapped


# -----------------------------
# Pygments integration (optional)
# -----------------------------
def try_get_pygments():
    if not USE_PYGMENTS_IF_AVAILABLE:
        return None
    try:
        import pygments  # noqa
        from pygments import lex
        from pygments.lexers import guess_lexer_for_filename, get_lexer_by_name, TextLexer
        from pygments.token import Token
        return {
            "lex": lex,
            "guess_lexer_for_filename": guess_lexer_for_filename,
            "get_lexer_by_name": get_lexer_by_name,
            "TextLexer": TextLexer,
            "Token": Token,
        }
    except Exception:
        return None


def token_color_map():
    """
    A simple dark-theme-ish palette.
    """
    return {
        "comment": (120, 160, 130, 210),
        "string": (180, 220, 160, 230),
        "keyword": (140, 190, 255, 235),
        "name": (230, 230, 235, 235),
        "number": (255, 210, 140, 235),
        "operator": (210, 210, 220, 235),
        "punct": (210, 210, 220, 235),
        "builtin": (255, 170, 240, 235),
        "decorator": (255, 170, 240, 235),
        "other": (230, 230, 235, 235),
    }


def classify_token(ttype) -> str:
    """
    Reduce Pygments token types to a small set.
    """
    s = str(ttype)
    # Examples: 'Token.Comment.Single', 'Token.Literal.String', 'Token.Keyword'
    if "Comment" in s:
        return "comment"
    if "String" in s or "Char" in s:
        return "string"
    if "Keyword" in s:
        return "keyword"
    if "Number" in s:
        return "number"
    if "Operator" in s:
        return "operator"
    if "Punctuation" in s:
        return "punct"
    if "Name.Builtin" in s:
        return "builtin"
    if "Name.Decorator" in s:
        return "decorator"
    if "Name" in s:
        return "name"
    return "other"


def render_with_optional_highlighting(
    draw: ImageDraw.ImageDraw,
    code_lines: List[str],
    filename: str,
    font: ImageFont.FreeTypeFont,
    start_x: int,
    start_y: int,
    line_h: int,
    max_w: int,
):
    """
    Draw code lines either as plain text or token-colored segments (pygments).
    """
    pyg = try_get_pygments()
    palette = token_color_map()

    if pyg is None:
        # Plain text
        y = start_y
        for line in code_lines:
            draw.text((start_x, y), line, font=font, fill=CODE_TEXT_COLOR)
            y += line_h
        return

    # Build one string for lexing, but render line by line.
    from pygments.lexers import TextLexer  # type: ignore

    # Guess lexer by filename + content
    code_text = "\n".join(code_lines)
    try:
        lexer = pyg["guess_lexer_for_filename"](filename, code_text)
    except Exception:
        lexer = TextLexer()

    # Tokenize full text, then split tokens by lines
    tokens = list(pyg["lex"](code_text, lexer))

    # Convert token stream to per-line segments
    lines_segments: List[List[Tuple[str, Tuple[int, int, int, int]]]] = [[]]
    for ttype, value in tokens:
        # split by newlines while keeping color
        parts = value.split("\n")
        cls = classify_token(ttype)
        color = palette.get(cls, palette["other"])

        for i, part in enumerate(parts):
            if i > 0:
                lines_segments.append([])
            if part:
                lines_segments[-1].append((part, color))

    # Render each line as segments
    y = start_y
    for segs in lines_segments:
        x = start_x
        for text, color in segs:
            draw.text((x, y), text, font=font, fill=color)
            x += draw.textlength(text, font=font)
            if x > start_x + max_w:
                break
        y += line_h


# -----------------------------
# Main
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 code_to_image.py path/to/file.py [output.png]")
        sys.exit(1)

    in_path = Path(sys.argv[1]).expanduser().resolve()
    if not in_path.exists():
        print(f"File not found: {in_path}")
        sys.exit(1)

    out_path = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) >= 3 else in_path.with_suffix(".png")

    raw = in_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if MAX_LINES is not None:
        raw = raw[:MAX_LINES]

    # Expand tabs for consistent rendering
    lines = [expand_tabs(l, TAB_SIZE) for l in raw]

    # Create transparent canvas
    img = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fonts
    mono_font = load_font(MONO_FONT_PATH, CODE_FONT_SIZE, monospace=True)
    title_font = load_font(TITLE_FONT_PATH, TITLE_FONT_SIZE, monospace=False)

    # Editor window box area
    x0 = PADDING
    y0 = PADDING
    x1 = OUT_W - PADDING
    y1 = OUT_H - PADDING

    # Draw rounded editor window
    rounded_rect(draw, (x0, y0, x1, y1), BOX_RADIUS, fill=BOX_BG, outline=BOX_STROKE, width=1)

    # Title bar separator (subtle line)
    sep_y = y0 + TITLEBAR_H
    draw.line([(x0 + 1, sep_y), (x1 - 1, sep_y)], fill=(255, 255, 255, 22), width=1)

    # Mac buttons
    btn_cy = y0 + BTN_Y
    btn_cx = x0 + BTN_LEFT
    for color in (MAC_RED, MAC_YELLOW, MAC_GREEN):
        draw.ellipse((btn_cx - BTN_R, btn_cy - BTN_R, btn_cx + BTN_R, btn_cy + BTN_R), fill=color)
        btn_cx += (BTN_R * 2 + BTN_GAP)

    # Title (filename) centered in title bar
    title = in_path.name
    max_title_w = (x1 - x0) - 2 * 120  # leave room for buttons and margins
    title = ellipsize(title, title_font, max_title_w, draw)
    title_w = draw.textlength(title, font=title_font)
    title_x = x0 + ((x1 - x0) - title_w) / 2
    title_y = y0 + (TITLEBAR_H - TITLE_FONT_SIZE) / 2 - 2
    draw.text((title_x, title_y), title, font=title_font, fill=TITLE_TEXT_COLOR)

    # Compute code layout
    inner_left = x0 + INNER_PAD_X
    inner_top = y0 + TITLEBAR_H + INNER_PAD_Y
    inner_right = x1 - INNER_PAD_X
    inner_bottom = y1 - INNER_PAD_Y

    # Line height
    ascent, descent = mono_font.getmetrics()
    base_line_h = ascent + descent
    line_h = base_line_h + LINE_SPACING

    # Determine visible lines
    available_h = inner_bottom - inner_top
    max_visible_lines = max(1, available_h // line_h)

    # We will wrap BEFORE line numbers width calculation, because wrapping increases line count
    # But line numbers should correspond to original lines; for wrapped continuations, we show blank lineno.
    # So we keep a structure: display_lines = [(lineno_or_None, text)]
    # First, wrapping each original line into 1..n display lines
    tmp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp_img)

    # Compute gutter width from original line count
    total_lines = max(1, len(lines))
    lineno_digits = len(str(total_lines))
    lineno_sample = "9" * lineno_digits
    gutter_w = math.ceil(tmp_draw.textlength(lineno_sample, font=mono_font)) + 6

    code_area_w = (inner_right - inner_left) - gutter_w - GUTTER_GAP
    if code_area_w < 50:
        raise RuntimeError("Image too small for the chosen padding/font sizes; increase OUT_W or reduce sizes.")

    display: List[Tuple[Optional[int], str]] = []
    # Wrap each original line; wrapped continuations have lineno None
    for i, line in enumerate(lines, start=1):
        if not WRAP_LONG_LINES or tmp_draw.textlength(line, font=mono_font) <= code_area_w:
            display.append((i, line))
        else:
            wrapped = split_and_wrap_lines([line], mono_font, code_area_w, tmp_draw)
            for j, wline in enumerate(wrapped):
                display.append((i if j == 0 else None, wline))

    # Clip to visible
    display = display[:max_visible_lines]

    # Optional: draw a faint lineno strip
    if LINENO_BG is not None:
        draw.rectangle((inner_left, inner_top, inner_left + gutter_w + 6, inner_bottom), fill=LINENO_BG)

    # Draw line numbers + collect code lines for highlighting render
    code_x = inner_left + gutter_w + GUTTER_GAP
    y = inner_top

    # Build a “code-only” list for pygments rendering *in display order*
    # For wrapped continuation lines, we still render their text.
    display_code_lines = [t for (_, t) in display]

    # First draw line numbers
    for ln, text in display:
        if ln is not None:
            s = str(ln).rjust(lineno_digits)
            draw.text((inner_left, y), s, font=mono_font, fill=LINENO_COLOR)
        y += line_h

    # Then draw code content (plain or highlighted)
    render_with_optional_highlighting(
        draw=draw,
        code_lines=display_code_lines,
        filename=in_path.name,
        font=mono_font,
        start_x=code_x,
        start_y=inner_top,
        line_h=line_h,
        max_w=code_area_w,
    )

    img.save(out_path, "PNG")
    print(f"OK: {out_path}")


if __name__ == "__main__":
    main()

