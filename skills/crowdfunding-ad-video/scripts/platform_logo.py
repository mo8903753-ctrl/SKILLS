#!/usr/bin/env python3
"""Get the OFFICIAL platform logo as a transparent PNG — never redraw a platform logo by hand.

Two modes, both rasterise in a real browser (ego-browser) because KS / Indiegogo / zeczec sit behind
Cloudflare and curl only gets a challenge page:

  # A) element on the live page (inline <svg>, <img src=…svg/png>, or a container holding several)
  platform_logo.py --page URL --selector CSS [--parent N] --out logo.png [--height 400]
  platform_logo.py --page URL --find                     # list logo-like elements + sprite symbols

  # B) inline SVG <symbol> sprite (e.g. Makuake)
  platform_logo.py --page URL --symbol makuakelogo_pc --out logo.png

Known selectors (verified 2026-10-19; copies in assets/platform_logos/ — re-run with --find if a site redesigns):
  Kickstarter   --page https://www.kickstarter.com/  --selector 'svg.valign-middle'            (green wordmark)
  Indiegogo     --page https://www.indiegogo.com/    --selector 'img.gfu-header-logo__full'     (magenta wordmark)
  zeczec 嘖嘖    --page https://www.zeczec.com/       --selector 'svg.logo' --parent 2          (dark icon + 嘖嘖)
  Makuake       --page https://www.makuake.com/      --symbol makuakelogo_pc                  (colour icon + black wordmark)
Network is flaky: on ERR_CONNECTION_CLOSED just re-run.
Prints the first transparent column gap so the icon alone can be cropped if needed."""
import argparse, base64, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--page", required=True)
ap.add_argument("--selector"); ap.add_argument("--parent", type=int, default=0)
ap.add_argument("--symbol"); ap.add_argument("--find", action="store_true")
ap.add_argument("--out"); ap.add_argument("--height", type=int, default=400)
a = ap.parse_args()

PRELUDE = f"""
const fs = await import("node:fs/promises");
const task = await taskSpace("platform logo");
const page = task.page("p1");
try {{ await page.goto({json.dumps(a.page)}, {{ timeout: 45000 }}); }} catch (e) {{ console.log("goto-warning", String(e).slice(0, 120)); }}
await page.waitForTimeout(4000);
"""
FINISH = "await task.finish({ keep: [] });\n"

def run_js(js):
    r = subprocess.run(["ego-browser", "nodejs"], input=js, capture_output=True, text=True, timeout=240)
    return r.stdout + r.stderr

if a.find:
    js = PRELUDE + """
const r = await page.evaluate(() => {
  const syms = [...document.querySelectorAll('symbol[id]')].map(s => s.id).filter(i => /logo/i.test(i));
  const els = [...document.querySelectorAll('svg, img')].filter(el => {
    const s = (el.outerHTML.slice(0, 400) + (el.closest('a')?.getAttribute('aria-label') || '')).toLowerCase();
    return /logo|kickstarter|indiegogo|zeczec|makuake|嘖嘖/.test(s) && el.getBoundingClientRect().top < 200;
  }).map(el => { const b = el.getBoundingClientRect();
    return {tag: el.tagName.toLowerCase(), cls: el.getAttribute('class'), alt: el.getAttribute('alt'),
            aria: el.closest('a')?.getAttribute('aria-label'), src: el.getAttribute('src'),
            box: [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]}; });
  return {syms, els};
});
console.log(JSON.stringify(r, null, 1));
""" + FINISH
    print(run_js(js)); sys.exit(0)

if not a.out:
    sys.exit("--out required")

if a.symbol:
    js = PRELUDE + f"""
const svg = await page.evaluate((id) => {{
  const s = document.getElementById(id); if (!s) return null;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${{s.getAttribute('viewBox')}}">${{s.innerHTML}}</svg>`;
}}, {json.dumps(a.symbol)});
console.log("PARTS" + JSON.stringify(svg ? [{{kind: "svg", markup: svg, x: 0, y: 0, w: 0, h: 0}}] : []));
""" + FINISH
else:
    js = PRELUDE + f"""
const parts = await page.evaluate(({{sel, up}}) => {{
  let root = document.querySelector(sel); if (!root) return [];
  for (let i = 0; i < up; i++) root = root.parentElement;
  const R = root.getBoundingClientRect();
  const els = root.matches('svg, img') ? [root] : [...root.querySelectorAll('svg, img')].filter(e => !e.parentElement.closest('svg'));
  const out = [];
  for (const el of els) {{
    const b = el.getBoundingClientRect(); if (!b.width || !b.height) continue;
    const box = {{x: b.left - R.left, y: b.top - R.top, w: b.width, h: b.height}};
    if (el.tagName.toLowerCase() === 'img') {{ out.push({{kind: "img", src: el.currentSrc || el.src, ...box}}); continue; }}
    const cl = el.cloneNode(true);
    const o = [el, ...el.querySelectorAll('*')], c = [cl, ...cl.querySelectorAll('*')];
    o.forEach((n, i) => {{ const cs = getComputedStyle(n);
      if (cs.display === 'none') c[i].setAttribute('display', 'none');
      if (cs.fill) c[i].setAttribute('fill', cs.fill);
      if (cs.stroke && cs.stroke !== 'none') c[i].setAttribute('stroke', cs.stroke); }});
    cl.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    cl.setAttribute('width', b.width); cl.setAttribute('height', b.height);
    out.push({{kind: "svg", markup: new XMLSerializer().serializeToString(cl), ...box}});
  }}
  return out;
}}, {{sel: {json.dumps(a.selector)}, up: {a.parent}}});
console.log("PARTS" + JSON.stringify(parts));
""" + FINISH

out = run_js(js)
line = next((l for l in out.splitlines() if l.startswith("PARTS")), None)
parts = json.loads(line[5:]) if line else []
if not parts:
    sys.exit("no logo element found — run with --find\n" + out[-1500:])

for p in parts:   # <img>: download with curl (no canvas CORS taint) → data URL
    if p["kind"] == "img":
        data = subprocess.run(["curl", "-sL", "--max-time", "40", p["src"]], capture_output=True).stdout
        svgish = p["src"].split("?")[0].endswith(".svg") or data[:300].lstrip().startswith(b"<")
        p["data"] = ("data:image/svg+xml;base64," if svgish else "data:image/png;base64,") + base64.b64encode(data).decode()
    else:
        p["data"] = "data:image/svg+xml;base64," + base64.b64encode(p["markup"].encode()).decode()

js2 = f"""
const fs = await import("node:fs/promises");
const task = await taskSpace("platform logo raster");
const page = task.page("p1");
await page.goto("about:blank");
const png = await page.evaluate(async ({{parts, H}}) => {{
  const imgs = [];
  for (const p of parts) {{ const im = new Image(); im.src = p.data; await im.decode(); imgs.push(im); }}
  if (parts.length === 1 && !parts[0].w) {{
    const vb = (atob(parts[0].data.split(',')[1]).match(/viewBox="([^"]+)"/) || [])[1];
    const v = vb ? vb.split(/[ ,]+/).map(Number) : [0, 0, imgs[0].naturalWidth || 200, imgs[0].naturalHeight || 40];
    parts[0].w = v[2]; parts[0].h = v[3];
  }}
  const maxX = Math.max(...parts.map(p => p.x + p.w)), maxY = Math.max(...parts.map(p => p.y + p.h));
  const s = H / maxY;
  const c = document.createElement('canvas'); c.width = Math.ceil(maxX * s); c.height = H;
  const ctx = c.getContext('2d');
  parts.forEach((p, i) => ctx.drawImage(imgs[i], p.x * s, p.y * s, p.w * s, p.h * s));
  return c.toDataURL('image/png');
}}, {{parts: {json.dumps([{k: p[k] for k in ("data", "x", "y", "w", "h")} for p in parts])}, H: {a.height}}});
await fs.writeFile({json.dumps(os.path.abspath(a.out))}, Buffer.from(png.split(",")[1], "base64"));
""" + FINISH
if os.path.exists(a.out):
    os.remove(a.out)
log = run_js(js2)
if not os.path.exists(a.out):
    sys.exit("rasterise failed:\n" + log[-1500:])
from PIL import Image
import numpy as np
im = Image.open(a.out).convert("RGBA")
im = im.crop(im.getbbox()); im.save(a.out)
cols = (np.asarray(im.getchannel("A")) > 10).any(axis=0)
x = 0
while x < len(cols) and cols[x]:
    x += 1
print(f"saved {a.out} {im.size}; first transparent gap at x={x}")
print("CHECK IT: Read the PNG on light and dark backgrounds — some header logos are white-on-transparent.")
