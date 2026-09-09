"""Minimal renderer for diagram-design-style SVG (editorial skin, light).

Tokens follow skills/diagram-design/references/style-guide.md. Every coordinate
this module emits is a multiple of 4 as long as callers pass multiples of 4.
"""

PAPER = "#f5f5f5"
INK = "#2d3142"
MUTED = "#4f5d75"
SOFT = "#7a8399"
ACCENT = "#eb6c36"
LINK = "#2e5aa8"

SANS = "'Geist', sans-serif"
MONO = "'Geist Mono', monospace"

KIND = {  # fill, stroke, tag colour
    "focal":    ("rgba(235,108,54,0.08)", ACCENT, ACCENT),
    "backend":  ("#ffffff", INK, MUTED),
    "store":    ("rgba(45,49,66,0.05)", MUTED, MUTED),
    "external": ("rgba(45,49,66,0.03)", "rgba(45,49,66,0.30)", SOFT),
    "input":    ("rgba(79,93,117,0.10)", SOFT, SOFT),
    "optional": ("rgba(45,49,66,0.02)", "rgba(45,49,66,0.20)", SOFT),
    "security": ("rgba(235,108,54,0.05)", "rgba(235,108,54,0.50)", ACCENT),
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def node(x, y, w, h, name, sub=None, kind="backend", tag=None, lines=None):
    """A component box. `lines` replaces name/sub with a stack of mono rows."""
    fill, stroke, tagc = KIND[kind]
    dash = ' stroke-dasharray="4,3"' if kind in ("optional", "security") else ""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="1"{dash}/>']
    cx = x + w // 2
    if tag:
        tw = 8 * len(tag) + 12
        o.append(f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="12" rx="2" fill="none" '
                 f'stroke="{tagc}" stroke-opacity="0.4" stroke-width="0.8"/>')
        o.append(f'<text x="{x+8+tw//2}" y="{y+17}" fill="{tagc}" font-size="7" '
                 f'font-family="{MONO}" text-anchor="middle" letter-spacing="0.08em">{esc(tag)}</text>')
    if lines:
        top = y + h // 2 - (len(lines) - 1) * 7
        for i, ln in enumerate(lines):
            o.append(f'<text x="{cx}" y="{top + i*14}" fill="{MUTED}" font-size="9.5" '
                     f'font-family="{MONO}" text-anchor="middle">{esc(ln)}</text>')
        return "\n".join(o)
    ny = y + h // 2 + (0 if not sub else -4)
    if tag:
        ny += 6
    o.append(f'<text x="{cx}" y="{ny}" fill="{INK}" font-size="12" font-weight="600" '
             f'font-family="{SANS}" text-anchor="middle">{esc(name)}</text>')
    if sub:
        o.append(f'<text x="{cx}" y="{ny+16}" fill="{MUTED}" font-size="9" '
                 f'font-family="{MONO}" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(o)


def zone(x, y, w, h, label):
    lw = 8 * len(label) + 16
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(45,49,66,0.02)" '
        f'stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
        f'<rect x="{x+16}" y="{y+4}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>',
        f'<text x="{x+16+lw//2}" y="{y+13}" fill="rgba(45,49,66,0.40)" font-size="7" '
        f'font-family="{MONO}" text-anchor="middle" letter-spacing="0.14em">{esc(label)}</text>',
    ])


def _stroke(style):
    if style == "accent":
        return ACCENT, 1.4, "url(#arrow-accent)", ""
    if style == "link":
        return LINK, 1.2, "url(#arrow-link)", ""
    if style == "dashed":
        return MUTED, 1.0, "url(#arrow)", ' stroke-dasharray="4,3"'
    return MUTED, 1.2, "url(#arrow)", ""


def arrow(x1, y1, x2, y2, style="plain", label=None, lx=None, ly=None):
    """Straight connector; endpoints must share x or y."""
    c, w, m, d = _stroke(style)
    o = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} '
         f'marker-end="{m}"/>']
    if label:
        o.append(_lab(label, lx if lx is not None else (x1 + x2) // 2,
                      ly if ly is not None else y1 - 8, c))
    return "\n".join(o)


def elbow(x1, y1, x2, y2, style="plain", label=None, mid=None, ly=None):
    """Two-bend horizontal-first elbow with r=8 corners."""
    c, w, m, d = _stroke(style)
    mx = mid if mid is not None else (x1 + x2) // 2
    s = 8 if y2 > y1 else -8
    p = (f"M {x1},{y1} H {mx-8} Q {mx},{y1} {mx},{y1+s} V {y2-s} "
         f"Q {mx},{y2} {mx+8},{y2} H {x2}")
    o = [f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{w}"{d} marker-end="{m}"/>']
    if label:
        o.append(_lab(label, mx, ly if ly is not None else (y1 + y2) // 2, c))
    return "\n".join(o)


def drop(x1, y1, x2, y2, style="plain", label=None):
    """Single-bend L: run horizontally from the source, then into the target's face."""
    c, w, m, d = _stroke(style)
    s = 8 if y2 > y1 else -8
    p = f"M {x1},{y1} H {x2-8} Q {x2},{y1} {x2},{y1+s} V {y2}"
    o = [f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{w}"{d} marker-end="{m}"/>']
    if label:
        o.append(_lab(label, (x1 + x2) // 2, y1 - 8, c))
    return "\n".join(o)


def _lab(text, cx, cy, colour):
    w = 8 * len(text) + 8
    return (f'<rect x="{cx-w//2}" y="{cy-10}" width="{w}" height="12" rx="2" fill="{PAPER}"/>'
            f'<text x="{cx}" y="{cy-1}" fill="{colour}" font-size="8" font-family="{MONO}" '
            f'text-anchor="middle" letter-spacing="0.08em">{esc(text)}</text>')


def caption(x, y, text, anchor="start", colour=None, size=9):
    return (f'<text x="{x}" y="{y}" fill="{colour or SOFT}" font-size="{size}" '
            f'font-family="{MONO}" text-anchor="{anchor}">{esc(text)}</text>')


def note(x, y, text, anchor="start"):
    """Caption under a diagram — sans, muted, the only non-mono annotation."""
    return (f'<text x="{x}" y="{y}" fill="{MUTED}" font-size="11.5" '
            f'font-family="{SANS}" text-anchor="{anchor}">{esc(text)}</text>')


DEFS = f'''<defs>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
<circle cx="1" cy="1" r="0.9" fill="rgba(45,49,66,0.10)"/></pattern>
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
<polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
<polygon points="0 0, 8 3, 0 6" fill="{ACCENT}"/></marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
<polygon points="0 0, 8 3, 0 6" fill="{LINK}"/></marker>
</defs>'''


def svg(slug, title, desc, width, height, body, dots=True):
    bg = f'<rect width="100%" height="100%" fill="{PAPER}"/>'
    if dots:
        bg += '\n<rect width="100%" height="100%" fill="url(#dots)" opacity="0.55"/>'
    return (f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-labelledby="{slug}-title {slug}-desc">\n'
            f'<title id="{slug}-title">{esc(title)}</title>\n'
            f'<desc id="{slug}-desc">{esc(desc)}</desc>\n{DEFS}\n{bg}\n{body}\n</svg>')


PAGE = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--paper:#f5f5f5;--ink:#2d3142;--muted:#4f5d75}}
body{{font-family:'Geist',system-ui,sans-serif;background:var(--paper);color:var(--ink);
min-height:100vh;display:flex;align-items:center;justify-content:center;padding:3rem 2rem}}
.frame{{max-width:1200px;width:100%}}
.eyebrow{{font-family:'Geist Mono',monospace;font-size:.66rem;font-weight:500;
letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:.5rem}}
h1{{font-family:'Geist',sans-serif;font-size:1.5rem;font-weight:600;
letter-spacing:-.01em;line-height:1.2;margin-bottom:1.5rem}}
svg{{width:100%;display:block}}
</style></head>
<body><div class="frame"><p class="eyebrow">{eyebrow}</p><h1>{heading}</h1>
{svg}
</div></body></html>
'''


def write(path, slug, eyebrow, heading, title, desc, width, height, body, dots=True):
    s = svg(slug, title, desc, width, height, body, dots)
    path.write_text(PAGE.format(title=esc(title), eyebrow=esc(eyebrow),
                                heading=esc(heading), svg=s), encoding="utf-8")
    return s


def oval(x, y, w, h, name, kind="input"):
    fill, stroke, _ = KIND[kind]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{PAPER}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1"/>'
            f'<text x="{x+w//2}" y="{y+h//2+4}" fill="{INK}" font-size="12" font-weight="600" '
            f'font-family="{SANS}" text-anchor="middle">{esc(name)}</text>')


def diamond(cx, cy, w, h, name, sub=None, kind="backend"):
    fill, stroke, _ = KIND[kind]
    hw, hh = w // 2, h // 2
    pts = f"{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
    o = [f'<polygon points="{pts}" fill="{PAPER}"/>',
         f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>']
    dy = -4 if sub else 4
    o.append(f'<text x="{cx}" y="{cy+dy}" fill="{INK}" font-size="11" font-weight="600" '
             f'font-family="{SANS}" text-anchor="middle">{esc(name)}</text>')
    if sub:
        o.append(f'<text x="{cx}" y="{cy+12}" fill="{MUTED}" font-size="8.5" '
                 f'font-family="{MONO}" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(o)


def dot(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>'


def band(x, y, w, h, idx, name, sub, focal=False):
    """One row of a layer stack."""
    fill = "rgba(235,108,54,0.08)" if focal else "#ffffff"
    stroke = ACCENT if focal else "rgba(45,49,66,0.12)"
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="{1.2 if focal else 0.8}"/>',
         f'<text x="{x+20}" y="{y+h//2+4}" fill="{ACCENT if focal else SOFT}" font-size="8.5" '
         f'font-family="{MONO}" letter-spacing="0.14em">{esc(idx)}</text>',
         f'<text x="{x+88}" y="{y+h//2+5}" fill="{INK}" font-size="14" font-weight="600" '
         f'font-family="{SANS}">{esc(name)}</text>',
         f'<text x="{x+w-20}" y="{y+h//2+4}" fill="{MUTED}" font-size="9.5" '
         f'font-family="{MONO}" text-anchor="end">{esc(sub)}</text>']
    return "\n".join(o)
