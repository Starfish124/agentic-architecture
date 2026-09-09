"""diagrams/*.html -> diagrams/png/*.png at 2x, sized from each diagram's own viewBox."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIN_W = 1264                      # 1200 frame + 2rem padding each side
CHROME_MIN_H = 200                # headless refuses to go much below this

out = ROOT / "diagrams" / "png"
out.mkdir(exist_ok=True)

for html in sorted((ROOT / "diagrams").glob("*.html")):
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', html.read_text(encoding="utf-8"))
    w, h = int(vb.group(1)), int(vb.group(2))
    svg_h = round(1200 * h / w)
    page_h = max(CHROME_MIN_H, svg_h + 96 + 96)   # header block + body padding
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={WIN_W},{page_h}", "--force-device-scale-factor=2",
                    f"--screenshot={out / (html.stem + '.png')}", html.as_uri()],
                   check=True, capture_output=True)
    print(f"{html.stem}.png  {WIN_W}x{page_h} @2")
