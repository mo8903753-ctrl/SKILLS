#!/usr/bin/env python3
"""
Build the self-contained single-file Wix Custom Element bundle for Sweetmyo Gen2 (v4 Signal Edition).
Inlines GSAP 3, ScrollTrigger, Lenis, scoped CSS, templates, and SweetmyoLanding.
Outputs:
  - wix/sweetmyo-gen2-landing.js        (production bundle driven by media-map JSON or assets/ fallback)
  - wix/sweetmyo-gen2-landing.local.js  (for wix/host.html & wix/host-split.html using ../assets/)
  - wix/sweetmyo-gen2-landing.root.js   (for root index.html using assets/)
  - wix/media-map.template.json         (list of all media paths for Wix upload)
  - wix/host.html                       (single-element Wix 980px host test fixture with 3 large 680px external forms)
  - wix/host-split.html                 (4-section Wix split test fixture with part=a/b/c/d)
"""
import os
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
VENDOR = os.path.join(ROOT, "vendor")
ASSETS = os.path.join(ROOT, "assets")
WIX = os.path.join(ROOT, "wix")
os.makedirs(WIX, exist_ok=True)


def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def verify_css_scoping(css):
    for m in re.finditer(r"@keyframes\s+([a-zA-Z0-9_-]+)", css):
        name = m.group(1)
        assert name.startswith("sw-"), f"Unprefixed @keyframes: {name}"
    assert ".sw-white-root" in css, "Missing .sw-white-root root class"


def strip_esm(src_text):
    out = re.sub(r"^\s*import\s+[^;]+;\s*\n?", "", src_text, flags=re.M)
    out = re.sub(r"^\s*export\s+(?=(?:class|function|const|let|var)\b)", "", out, flags=re.M)
    return out


css_text = read(os.path.join(SRC, "styles.css"))
verify_css_scoping(css_text)

tpl_js = strip_esm(read(os.path.join(SRC, "template.js")))
elem_js = strip_esm(read(os.path.join(SRC, "element.js")))

vendor_files = [
    ("gsap", "gsap.min.js", "window.gsap"),
    ("ScrollTrigger", "ScrollTrigger.min.js", "window.ScrollTrigger"),
    ("Lenis", "lenis.min.js", "window.Lenis"),
]

vendor_blocks = []
for label, fname, check_expr in vendor_files:
    code = read(os.path.join(VENDOR, fname))
    vendor_blocks.append(
        f"  /* ── Inline Vendor: {label} ── */\n"
        f"  if (!{check_expr}) {{\n"
        f"    (function () {{\n"
        f"      var exports, module, define;\n"
        f"{code}\n"
        f"    }}).call(window);\n"
        f"  }}"
    )

tpl_src = read(os.path.join(SRC, "template.js"))
media_keys = sorted(set(re.findall(r"A\('([^']+)'\)", tpl_src)))
missing = [k for k in media_keys if not os.path.exists(os.path.join(ASSETS, k))]
if missing and not os.environ.get("SW_SKIP_ASSET_CHECK"):
    raise SystemExit(f"Missing assets (set SW_SKIP_ASSET_CHECK=1 to build anyway): {missing}")
media_keys.sort()

template_map = {
    "__folder": "",
    **{k: "" for k in media_keys}
}
map_tpl_path = os.path.join(WIX, "media-map.template.json")
with open(map_tpl_path, "w", encoding="utf-8") as f:
    json.dump(template_map, f, indent=2)

prod_map_path = os.path.join(WIX, "media-map.production.json")
prod_map = {}
if os.path.exists(prod_map_path):
    prod_map = {k: v for k, v in json.load(open(prod_map_path, encoding="utf-8")).items() if not k.startswith("__") and v}


def make_bundle(asset_map_dict, fallback_prefix, banner_note):
    return f"""/* Sweetmyo Gen2 Landing Page — Single-File Wix Custom Element ({banner_note})
 * Tag: <sweetmyo-gen2-landing> | Root Class: .sw-white-root
 * Generated automatically by scripts/build_wix.py — edit files in src/ instead.
 */
(function () {{
  var MEDIA_MAP = {json.dumps(asset_map_dict, ensure_ascii=False)};
  var FALLBACK_PREFIX = {json.dumps(fallback_prefix)};
  window.__SW_ASSET_FN = function (rel) {{
    return MEDIA_MAP[rel] || (FALLBACK_PREFIX + rel);
  }};
  window.__SW_CSS_TEXT = {json.dumps(css_text, ensure_ascii=False)};

{chr(10).join(vendor_blocks)}

  /* ── Source Modules (Strict Mode) ── */
  (function () {{
    'use strict';
{tpl_js}

{elem_js}

    window.SweetmyoLanding = SweetmyoLanding;
    window.syncSweetmyoWixForms = function () {{
      [].forEach.call(document.querySelectorAll('sweetmyo-gen2-landing'), function (el) {{
        if (typeof el.syncWixForms === 'function') el.syncWixForms();
      }});
    }};
    registerSweetmyoElement();
  }})();
}})();
"""


prod_bundle = make_bundle(prod_map, "assets/", "Production / Self-Contained")
local_bundle = make_bundle({}, "../assets/", "Local Wix Host Test")
root_bundle = make_bundle({}, "assets/", "Local Root Preview")

with open(os.path.join(WIX, "sweetmyo-gen2-landing.js"), "w", encoding="utf-8") as f:
    f.write(prod_bundle)
with open(os.path.join(WIX, "sweetmyo-gen2-landing.local.js"), "w", encoding="utf-8") as f:
    f.write(local_bundle)
with open(os.path.join(WIX, "sweetmyo-gen2-landing.root.js"), "w", encoding="utf-8") as f:
    f.write(root_bundle)


# ── Build Wix 980px Grid Host Simulators with Enlarged 680px x 68px Forms ──
BTN_LABELS = {0: "Notify Me", 1: "Lock In 50% OFF", 2: "Notify Me"}
MOCK_FORM_HTML = lambda idx, margin_css, title: f"""
<div class="wxw" data-mock-wix-form="{idx}" style="margin:{margin_css}">
  <div class="wx-comp-inner">
    <form class="wxform" onsubmit="event.preventDefault(); this.querySelector('button').textContent='50% OFF Locked';">
      <input type="email" required placeholder="Enter your email" aria-label="{title}">
      <button type="submit">{BTN_LABELS.get(idx, 'Notify Me')}</button>
    </form>
  </div>
</div>"""

HOST_STYLES = """
  html, body { margin: 0; padding: 0; background: #F6F5F2; font-family: 'Inter Tight', Arial, sans-serif; }
  .wxsec { position: relative; width: 100%; min-width: 0; overflow-x: clip; }
  .wxgrid { display: grid; grid-template-rows: 1fr; grid-template-columns: 100%; position: relative; }
  .wxgrid > * { grid-area: 1 / 1 / 2 / 2; place-self: start; position: relative; }
  .wxcomp { width: 980px; max-width: 100%; margin-left: calc(50% - 490px); min-height: 120px; }
  @media (max-width: 980px) { .wxcomp { width: 100%; margin-left: 0; } }
  .wxw { width: 560px; max-width: calc(100vw - 40px); z-index: 35; }
  .wxform { display: flex; align-items: center; gap: 8px; padding: 6px; border-radius: 999px; background: #0E0F0C; width: 100%; box-sizing: border-box; }
  .wxform input { flex: 1 1 auto; min-width: 0; height: 52px; border: 0; outline: none; background: transparent; color: #F6F5F2; font-size: 16px; padding: 0 18px; }
  .wxform input::placeholder { color: #A9ACA3; }
  .wxform button { flex: none; height: 52px; padding: 0 26px; border: 0; border-radius: 999px; background: #CBF23A; color: #0E0F0C; font-size: 15px; font-weight: 600; cursor: pointer; white-space: nowrap; }
  [data-mock-wix-form="1"] .wxform, [data-mock-wix-form="2"] .wxform { background: #F6F5F2; }
  [data-mock-wix-form="1"] .wxform input, [data-mock-wix-form="2"] .wxform input { color: #0E0F0C; }
  [data-mock-wix-form="1"] .wxform button, [data-mock-wix-form="2"] .wxform button { background: #0E0F0C; color: #F6F5F2; }
"""

host_single = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sweetmyo Gen2 — Wix Custom Element 980px Host Verification</title>
  <style>{HOST_STYLES}</style>
</head>
<body>
  <section class="wxsec">
    <div class="wxgrid">
      <div class="wxcomp">
        <sweetmyo-gen2-landing></sweetmyo-gen2-landing>
      </div>
      <!-- Deliberately scattered external Wix native forms that MUST snap cleanly into the 3 centered 680px placeholders -->
      {MOCK_FORM_HTML(0, "140px 0 0 380px", "Hero VIP Email")}
      {MOCK_FORM_HTML(1, "40px 0 0 110px", "Mid Banner VIP Email")}
      {MOCK_FORM_HTML(2, "320px 0 0 440px", "Final Launch VIP Email")}
    </div>
  </section>
  <script src="sweetmyo-gen2-landing.local.js"></script>
</body>
</html>
"""

host_split = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sweetmyo Gen2 — Wix Multi-Section Custom Element Verification</title>
  <style>{HOST_STYLES}</style>
</head>
<body>
  <section class="wxsec"><div class="wxgrid"><div class="wxcomp"><sweetmyo-gen2-landing part="a"></sweetmyo-gen2-landing></div>{MOCK_FORM_HTML(0, "90px 0 0 340px", "Hero VIP Email")}</div></section>
  <section class="wxsec"><div class="wxgrid"><div class="wxcomp"><sweetmyo-gen2-landing part="b"></sweetmyo-gen2-landing></div>{MOCK_FORM_HTML(1, "60px 0 0 120px", "Mid Banner VIP Email")}</div></section>
  <section class="wxsec"><div class="wxgrid"><div class="wxcomp"><sweetmyo-gen2-landing part="c"></sweetmyo-gen2-landing></div></div></section>
  <section class="wxsec"><div class="wxgrid"><div class="wxcomp"><sweetmyo-gen2-landing part="d"></sweetmyo-gen2-landing></div>{MOCK_FORM_HTML(2, "120px 0 0 320px", "Final Launch VIP Email")}</div></section>
  <script src="sweetmyo-gen2-landing.local.js"></script>
</body>
</html>
"""

with open(os.path.join(WIX, "host.html"), "w", encoding="utf-8") as f:
    f.write(host_single)
with open(os.path.join(WIX, "host-split.html"), "w", encoding="utf-8") as f:
    f.write(host_split)

print(f"Built wix/sweetmyo-gen2-landing.js ({os.path.getsize(os.path.join(WIX, 'sweetmyo-gen2-landing.js')) / 1024:.1f} KB)")
print(f"Media assets indexed: {len(media_keys)}")
