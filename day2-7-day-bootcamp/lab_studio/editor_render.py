"""Render real source code into an IDE-style PNG (VS Code "Dark+" look).

A title bar with traffic-light dots and a filename tab, a line-number gutter,
syntax highlighting via Pygments, the target line(s) highlighted, and the rest
of the code visually dimmed — so it reads like a live editor, not a slide.

Supports line-by-line walkthroughs: a step is a sequence of "beats", each
highlighting just the line(s) currently being narrated, with the viewport held
steady across the step so only the highlight moves.
"""

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename, TextLexer
from pygments.token import Token

DOTS = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]

# --- Themes: each maps base UI colors + a Pygments token color map ---------- #
# "Vibrant" is a Dracula-style high-saturation palette (default). "Dark+" is the
# muted VS Code default. Token colors fall back to a parent token, then `text`.
THEMES = {
    "Vibrant": {
        "bg": (30, 31, 38),
        "titlebar": (44, 46, 58),
        "tab_bg": (30, 31, 38),
        "tab_text": (248, 248, 242),
        "gutter": (120, 126, 158),
        "text": (248, 248, 242),
        "band": (49, 54, 78),
        "accent": (189, 147, 249),
        "tokens": {
            Token.Keyword: (255, 121, 198),            # pink
            Token.Keyword.Namespace: (255, 121, 198),
            Token.Keyword.Constant: (189, 147, 249),   # purple
            Token.Operator: (255, 121, 198),
            Token.Operator.Word: (255, 121, 198),
            Token.Name.Function: (255, 216, 102),      # yellow
            Token.Name.Function.Magic: (255, 216, 102),
            Token.Name.Decorator: (255, 216, 102),
            Token.Name.Class: (139, 233, 253),         # cyan
            Token.Name.Builtin: (139, 233, 253),
            Token.Name.Builtin.Pseudo: (189, 147, 249),
            Token.Name.Namespace: (139, 233, 253),
            Token.Name.Variable: (248, 248, 242),
            Token.Name.Attribute: (102, 217, 239),
            Token.String: (195, 232, 141),             # green
            Token.String.Doc: (195, 232, 141),
            Token.String.Affix: (255, 121, 198),
            Token.String.Escape: (255, 216, 102),
            Token.String.Interpol: (255, 216, 102),
            Token.Number: (189, 147, 249),             # purple
            Token.Comment: (98, 114, 164),             # muted blue
            Token.Comment.Single: (98, 114, 164),
            Token.Punctuation: (248, 248, 242),
        },
    },
    "Dark+": {
        "bg": (30, 30, 30),
        "titlebar": (60, 60, 61),
        "tab_bg": (30, 30, 30),
        "tab_text": (212, 212, 212),
        "gutter": (133, 133, 133),
        "text": (212, 212, 212),
        "band": (40, 49, 71),
        "accent": (0, 122, 204),
        "tokens": {
            Token.Keyword: (86, 156, 214),
            Token.Keyword.Namespace: (197, 134, 192),
            Token.Keyword.Constant: (86, 156, 214),
            Token.Name.Function: (220, 220, 170),
            Token.Name.Class: (78, 201, 176),
            Token.Name.Decorator: (220, 220, 170),
            Token.Name.Builtin: (78, 201, 176),
            Token.Name.Builtin.Pseudo: (86, 156, 214),
            Token.Name.Namespace: (78, 201, 176),
            Token.Name.Variable: (156, 220, 254),
            Token.Name.Attribute: (156, 220, 254),
            Token.String: (206, 145, 120),
            Token.String.Doc: (206, 145, 120),
            Token.String.Escape: (215, 186, 125),
            Token.String.Interpol: (215, 186, 125),
            Token.Number: (181, 206, 168),
            Token.Comment: (106, 153, 85),
            Token.Operator: (212, 212, 212),
            Token.Operator.Word: (86, 156, 214),
            Token.Punctuation: (212, 212, 212),
        },
    },
}
DEFAULT_THEME = "Vibrant"

MONO_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Supplemental/Menlo.ttc",
    "/Library/Fonts/Courier New.ttf",
    "/System/Library/Fonts/Monaco.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
]


def _find_font(candidates, override=None):
    if override and Path(override).exists():
        return override
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def _load_font(size, font_path=None):
    p = _find_font(MONO_CANDIDATES, font_path)
    try:
        return ImageFont.truetype(p, size) if p else ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()


def _color_for(tok, tokens, default):
    t = tok
    while t is not None:
        if t in tokens:
            return tokens[t]
        t = t.parent
    return default


def _dim(color, bg, factor=0.42):
    return tuple(int(b + (c - b) * factor) for c, b in zip(color, bg))


def _lex_lines(code, lexer):
    lines = [[]]
    for tok, val in lex(code, lexer):
        for i, part in enumerate(val.split("\n")):
            if i > 0:
                lines.append([])
            if part:
                lines[-1].append((part, tok))
    if lines and not lines[-1]:
        lines.pop()
    return lines


def _lexer_for(lang, filename, code):
    try:
        return get_lexer_by_name(lang) if lang else guess_lexer_for_filename(filename, code)
    except Exception:
        try:
            return guess_lexer_for_filename(filename, code)
        except Exception:
            return TextLexer()


# --- layout / viewport math (shared so beats line up) ---------------------- #

def _bar_h(font_size):
    return max(56, font_size + 28)


def visible_lines(font_size=28, height=1080):
    line_h = int(font_size * 1.55)
    top = _bar_h(font_size) + 14
    return max(1, (height - top - 14) // line_h)


def viewport_first(n_total, focus_lines, font_size=28, height=1080):
    """0-based first visible line: show all if it fits, else center on focus."""
    vis = visible_lines(font_size, height)
    if n_total <= vis:
        return 0
    if focus_lines:
        lo, hi = min(focus_lines), max(focus_lines)
        center = (lo + hi) // 2
        return max(0, min(center - vis // 2, n_total - vis))
    return 0


def resolve_highlight(code, spec, line_offset=0):
    """spec -> set of 1-based line numbers within `code`. Accepts:
       'a-b' range, a single line number, a quoted "substring", or a
       function/class/method name (whole def block).

    Numeric targets are interpreted as REAL file line numbers (what the gutter
    shows); `line_offset` maps them back to the snippet's own indexing."""
    if not spec:
        return set()
    spec = spec.strip()
    m = re.match(r"^(\d+)\s*-\s*(\d+)$", spec)
    if m:
        a, b = int(m.group(1)) - line_offset, int(m.group(2)) - line_offset
        return set(range(min(a, b), max(a, b) + 1))
    if spec.isdigit():
        return {int(spec) - line_offset}
    lines = code.split("\n")
    # quoted literal -> all lines containing the substring
    if (spec[0], spec[-1]) in (('"', '"'), ("'", "'")) and len(spec) >= 2:
        needle = spec[1:-1]
        return {i + 1 for i, ln in enumerate(lines) if needle in ln} or set()
    # function / class / method name -> its definition + indented body
    name = re.escape(spec)
    def_re = re.compile(rf"^(\s*)(?:async\s+def|def|class|func|function)\s+{name}\b")
    for i, line in enumerate(lines):
        m = def_re.match(line)
        if m:
            indent = len(m.group(1))
            end = i
            for j in range(i + 1, len(lines)):
                s = lines[j].strip()
                if s and (len(lines[j]) - len(lines[j].lstrip())) <= indent:
                    break
                end = j
            return set(range(i + 1, end + 2))
    # fallback: any line containing the text
    return {i + 1 for i, ln in enumerate(lines) if spec in ln}


def render_code_image(code, filename, out_path, lang=None, highlight=None,
                      width=1920, height=1080, font_size=28, font_path=None,
                      viewport=None, line_offset=0, theme=DEFAULT_THEME):
    code = code.replace("\t", "    ").rstrip("\n")
    lexer = _lexer_for(lang, filename, code)
    hl = resolve_highlight(code, highlight, line_offset) if isinstance(highlight, str) else (highlight or set())
    has_focus = bool(hl)

    th = THEMES.get(theme, THEMES[DEFAULT_THEME])
    BG, TITLEBAR, TAB_BG = th["bg"], th["titlebar"], th["tab_bg"]
    TAB_TEXT, GUTTER_TEXT, DEFAULT_TEXT = th["tab_text"], th["gutter"], th["text"]
    HILITE_BAND, HILITE_ACCENT, tokens = th["band"], th["accent"], th["tokens"]

    reg = _load_font(font_size, font_path)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)

    bar_h = _bar_h(font_size)
    d.rectangle([0, 0, width, bar_h], fill=TITLEBAR)
    cx = 26
    for col in DOTS:
        d.ellipse([cx, bar_h // 2 - 8, cx + 16, bar_h // 2 + 8], fill=col)
        cx += 26
    tab_x = cx + 18
    tab_w = int(d.textlength(filename, font=reg)) + 48
    d.rectangle([tab_x, 0, tab_x + tab_w, bar_h], fill=TAB_BG)
    d.rectangle([tab_x, bar_h - 3, tab_x + tab_w, bar_h], fill=HILITE_ACCENT)
    d.text((tab_x + 24, bar_h // 2), filename, font=reg, fill=TAB_TEXT, anchor="lm")

    char_w = d.textlength("M", font=reg)
    line_h = int(font_size * 1.55)
    top = bar_h + 14
    lines = _lex_lines(code, lexer)
    n = len(lines)
    digits = len(str(n + line_offset))
    gutter_w = int(char_w * (digits + 2)) + 20
    code_x0 = gutter_w + 16
    vis = (height - top - 14) // line_h

    first = viewport if viewport is not None else viewport_first(n, hl, font_size, height)
    first = max(0, min(first, max(0, n - vis)))
    last = min(n, first + vis)

    y = top
    for idx in range(first, last):
        snip_line = idx + 1
        disp_line = snip_line + line_offset
        focused = (not has_focus) or (snip_line in hl)
        if has_focus and snip_line in hl:
            d.rectangle([gutter_w, y - 2, width, y + line_h - 2], fill=HILITE_BAND)
            d.rectangle([gutter_w, y - 2, gutter_w + 4, y + line_h - 2], fill=HILITE_ACCENT)
        num_col = GUTTER_TEXT if focused else _dim(GUTTER_TEXT, BG)
        d.text((gutter_w - 10, y + line_h // 2), str(disp_line), font=reg,
               fill=num_col, anchor="rm")
        x = code_x0
        for text, tok in lines[idx]:
            col = _color_for(tok, tokens, DEFAULT_TEXT)
            if not focused:
                col = _dim(col, BG)
            d.text((x, y), text, font=reg, fill=col)
            x += char_w * len(text)
        y += line_h

    img.save(str(out_path))
    return out_path


# --------------------------------------------------------------------------- #
# Lab-file parser
# --------------------------------------------------------------------------- #

EXT_LANG = {".py": "python", ".js": "javascript", ".ts": "typescript",
            ".tsx": "tsx", ".jsx": "jsx", ".java": "java", ".go": "go",
            ".rb": "ruby", ".rs": "rust", ".c": "c", ".cpp": "cpp",
            ".cs": "csharp", ".php": "php", ".sql": "sql", ".sh": "bash"}


def _parse_beats(body, fallback_highlight, fallback_notes):
    """Parse a '**Walkthrough:**' section of '@ target' beats. Falls back to a
    single beat from **Notes:**/**Highlight:** when no walkthrough is present."""
    wt = re.search(r"\*\*Walkthrough:\*\*\s*(.*)$", body, re.S)
    if wt:
        section = wt.group(1)
        beats = []
        # split on lines beginning with '@'
        chunks = re.split(r"^@[ \t]*(.*)$", section, flags=re.MULTILINE)
        # chunks: [pre, target1, text1, target2, text2, ...]
        it = iter(chunks[1:])
        for target, text in zip(it, it):
            text = text.strip()
            if text:
                beats.append({"highlight": target.strip(), "text": text})
        if beats:
            return beats
    if fallback_notes:
        return [{"highlight": fallback_highlight, "text": fallback_notes}]
    return []


def parse_lab(md_text):
    """Parse a Lab-Mode markdown file into ordered steps, each with beats.

    Per step:
        ### Step 1 — Title
        **File:** app/services/llm_service.py
        **Lang:** python                      (optional)

        ```python
        ...full code to show...
        ```

        **Walkthrough:**
        @ send_request
        Inside this file we add a new function...

        @ 13-17
        Here we build the payload...

        @ "if response.status_code != 200:"
        This condition protects us from continuing when the request fails...

    Backward compatible: a step may instead use **Highlight:** + **Notes:**
    for a single full-function beat.
    """
    steps = []
    blocks = re.split(r"^###\s+Step\b[^\n]*\n", md_text, flags=re.MULTILINE)
    titles = re.findall(r"^###\s+Step\b([^\n]*)\n", md_text, flags=re.MULTILINE)
    for title, body in zip(titles, blocks[1:]):
        file_m = re.search(r"\*\*File:\*\*\s*(.+)", body)
        lang_m = re.search(r"\*\*Lang:\*\*\s*([\w-]+)", body)
        start_m = re.search(r"\*\*StartLine:\*\*\s*(\d+)", body)
        hi_m = re.search(r"\*\*Highlight:\*\*\s*(.+)", body)
        code_m = re.search(r"```[\w-]*\n(.*?)```", body, re.S)
        notes_m = re.search(r"\*\*Notes:\*\*\s*(.*?)\n```", body, re.S) \
            or re.search(r"\*\*Notes:\*\*\s*(.*)$", body, re.S)

        filename = file_m.group(1).strip() if file_m else "untitled.py"
        lang = lang_m.group(1).strip() if lang_m else EXT_LANG.get(Path(filename).suffix)
        start_line = int(start_m.group(1)) if start_m else 1
        code = code_m.group(1).rstrip("\n") if code_m else ""
        beats = _parse_beats(
            body,
            hi_m.group(1).strip() if hi_m else "",
            notes_m.group(1).strip() if notes_m else "",
        )
        steps.append({
            "title": title.strip(" —-").strip(),
            "file": filename,
            "lang": lang,
            "start_line": start_line,
            "code": code,
            "beats": beats,
        })
    return steps
