"""docs/*.html fragments + diagrams/*.html  ->  pdf/*.pdf

A fragment writes {{diagram-slug}} where a diagram goes; the build inlines that
diagram's <svg>, so every diagram has exactly one source file.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SHELL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
@page {{ size: A4; margin: 18mm 16mm 16mm; }}
*,*::before,*::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --ink:#2d3142; --muted:#4f5d75; --soft:#7a8399; --accent:#eb6c36;
         --rule:rgba(45,49,66,0.12); --paper:#f5f5f5; }}
body {{ font-family:'Geist',system-ui,sans-serif; color:var(--ink);
        font-size:10.5pt; line-height:1.55; background:#fff; }}
.eyebrow {{ font-family:'Geist Mono',monospace; font-size:7.5pt; letter-spacing:.18em;
            text-transform:uppercase; color:var(--muted); }}
h1 {{ font-family:'Instrument Serif',serif; font-weight:400; font-size:30pt;
      line-height:1.1; letter-spacing:-.02em; margin:.2em 0 .35em; }}
h2 {{ font-family:'Instrument Serif',serif; font-weight:400; font-size:17pt;
      margin:1.6em 0 .5em; letter-spacing:-.01em; break-after:avoid; }}
h3 {{ font-size:10.5pt; font-weight:600; margin:1.3em 0 .3em; break-after:avoid; }}
p {{ margin:0 0 .75em; max-width:38em; }}
.lede {{ font-size:12pt; line-height:1.5; color:var(--muted); max-width:34em; margin-bottom:1.4em; }}
ul {{ margin:0 0 .9em 1.1em; max-width:38em; }}
li {{ margin-bottom:.3em; }}
code, .m {{ font-family:'Geist Mono',monospace; font-size:9pt; }}
figure {{ margin:1.5em 0 1.6em; break-inside:avoid; }}
figure svg {{ width:100%; height:auto; display:block; margin:0 auto;
              border:1px solid var(--rule); border-radius:6px; background:var(--paper); }}
figure.tall svg {{ width:auto; height:148mm; }}
figcaption {{ font-family:'Geist Mono',monospace; font-size:7.5pt; color:var(--soft);
              letter-spacing:.06em; margin-top:.5em; }}
.rule {{ border:0; border-top:1px solid var(--rule); margin:2em 0 0; }}
.aside {{ font-family:'Instrument Serif',serif; font-style:italic; font-size:12pt;
          color:var(--muted); border-left:2px solid var(--accent); padding-left:.9em;
          margin:1.2em 0; max-width:34em; }}
table {{ border-collapse:collapse; font-size:9.5pt; margin:.6em 0 1.1em; width:100%;
         max-width:38em; break-inside:avoid; }}
th {{ font-family:'Geist Mono',monospace; font-size:7.5pt; letter-spacing:.12em;
      text-transform:uppercase; color:var(--muted); text-align:left;
      border-bottom:1px solid var(--rule); padding:.35em .6em .35em 0; }}
td {{ border-bottom:1px solid var(--rule); padding:.4em .6em .4em 0; vertical-align:top; }}
td:first-child {{ font-weight:600; white-space:nowrap; }}
footer {{ font-family:'Geist Mono',monospace; font-size:7.5pt; color:var(--soft);
          margin-top:1.2em; }}
a {{ color:var(--ink); }}
</style></head><body>
{body}
<hr class="rule">
<footer>{footer}</footer>
</body></html>
"""

FOOTER = ('Sarvesh Singh · github.com/Starfish124/agentic-architecture · '
          'diagrams built from source, not drawn by hand')


def svg_of(slug):
    html = (ROOT / "diagrams" / f"{slug}.html").read_text(encoding="utf-8")
    m = re.search(r"<svg\b.*?</svg>", html, re.S)
    if not m:
        sys.exit(f"no <svg> in {slug}.html")
    return m.group(0)


def build(frag_path):
    src = frag_path.read_text(encoding="utf-8")
    title = re.search(r"<h1>(.*?)</h1>", src, re.S).group(1).strip()
    body = re.sub(r"\{\{([\w-]+)\}\}", lambda m: svg_of(m.group(1)), src)
    page = ROOT / "pdf" / f"{frag_path.stem}.html"
    page.write_text(SHELL.format(title=title, body=body, footer=FOOTER), encoding="utf-8")
    pdf = ROOT / "pdf" / f"{frag_path.stem}.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", page.as_uri()],
                   check=True, capture_output=True)
    page.unlink()
    return pdf


if __name__ == "__main__":
    (ROOT / "pdf").mkdir(exist_ok=True)
    for f in sorted((ROOT / "docs").glob("*.html")):
        p = build(f)
        print(f"{p.name}  {p.stat().st_size // 1024} KB")
