#!/usr/bin/env python3
"""Build the Wix custom-element bundle from the standalone site.
   out: wix/dist/gx-genesis.js (Wix media URLs) + wix/dist/gx-genesis.local.js + wix/dist/host.html (local mock of the Wix page)"""
import re, json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(R + "/index.html", encoding="utf-8").read()
css = open(R + "/css/style.css", encoding="utf-8").read()
js = open(R + "/js/main.js", encoding="utf-8").read()
MAP = json.load(open(os.environ.get("GX_MEDIA_MAP", R + "/wix/media-map.production.json")))
OUT = os.environ.get("GX_DIST_DIR", R + "/wix/dist-production")

def must(s, a, b, n=1):
    assert s.count(a) >= 1, "missing: " + a[:70]
    return s.replace(a, b, n)
def between(s, a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

# ───────── HTML → four parts ─────────
body = between(html, '<div class="aura"', '<script src="https://cdnjs')
layers = '<div class="aura" aria-hidden="true"></div><div class="grain" aria-hidden="true"></div>'
hero_to_plates = between(body, '<!-- ───────────── HERO + PAIN', '<!-- ───────────── MID CTA')
sw_to_scenes = between(body, '<!-- ───────────── 04 SWITCH', '<!-- ───────────── FINAL CTA')
end = between(body, '<!-- ───────────── FINAL CTA', '</main>')
foot = between(body, '<footer class="foot">', '</footer>') + '</footer>'
form_re = re.compile(r'\s*<form class="form" novalidate>.*?</form>', re.S)

# hero: copy leaves the pinned layer so it scrolls with the page; the native Wix form sits in .slot
copy = between(hero_to_plates, '    <div class="hero__copy">', '    <div class="pain"')
hero_to_plates = hero_to_plates.replace(copy, '')
copy, n = form_re.subn('\n        <div class="slot" data-slot="hero"></div>', copy); assert n == 1
hero_to_plates = must(hero_to_plates, '  <div class="hero__pin">', copy.replace('    <div class="hero__copy">', '  <div class="hero__copy">') + '  <div class="hero__pin">')
nav = '<header class="nav"><span class="nav__logo"><img src="assets/logo-white.png" alt="biaXbew" width="1660" height="427"></span><p class="nav__status mono"><i class="dot"></i>Launching soon on <img class="ks" src="assets/ks.png" alt="Kickstarter" width="1200" height="183"></p><span class="nav__sp"></span></header>'
part_a = layers + nav + hero_to_plates
part_c = ('<section class="strip"><div class="strip__in"><div><p class="cta__line mono">Launching Soon on <img class="ks" src="assets/ks.png" alt="Kickstarter" width="1200" height="183"></p>'
          '<p class="strip__offer">Sign up now and enjoy <strong>over 30% OFF</strong></p></div><div class="slot" data-slot="mid"></div></div></section>')
part_b = layers + sw_to_scenes
end, n = form_re.subn('\n      <div class="slot" data-slot="end"></div>', end); assert n == 1
part_d = layers + end + foot
PARTS = {"a": part_a, "c": part_c, "b": part_b, "d": part_d}
for k, v in PARTS.items():
    assert '<form class="form"' not in v, k
    PARTS[k] = re.sub(r"<!--.*?-->", "", v, flags=re.S)

# ───────── CSS → scoped under .gxg ─────────
KF = ["pulse", "grain", "drip", "hue", "nudge"]
def scope_sel(sel):
    s = sel.strip()
    if not s: return None
    if s.startswith("html") or s.startswith(".lenis"): return None
    if s == ":root" or s == "body": return ".gxg"
    if s in ("main", ".foot"): return ".gxg > section, .gxg > .foot" if s == "main" else ".gxg .foot"
    return ".gxg " + s
def scope(block):
    out = []; i = 0; n = len(block)
    while i < n:
        j = block.find("{", i)
        if j < 0: break
        head = block[i:j].strip()
        d = 1; k = j + 1
        while d: 
            c = block[k]; d += (c == "{") - (c == "}"); k += 1
        inner = block[j + 1:k - 1]
        head_clean = re.sub(r"/\*.*?\*/", "", head, flags=re.S).strip()
        if head_clean.startswith("@media"): out.append(head_clean + " {\n" + scope(inner) + "}\n")
        elif head_clean.startswith("@keyframes"):
            name = head_clean.split()[1]; out.append("@keyframes gx-%s {%s}\n" % (name, inner))
        elif head_clean.startswith("@property"): out.append(head_clean + " {" + inner + "}\n")
        else:
            sels = [scope_sel(x) for x in head_clean.split(",")]
            sels = [x for x in sels if x]
            if sels: out.append(", ".join(dict.fromkeys(sels)) + " {" + inner + "}\n")
        i = k
    return "".join(out)
scoped = scope(css)
for k in KF:
    scoped = re.sub(r"(animation:\s*)%s\b" % k, r"\1gx-%s" % k, scoped)
scoped = scoped.replace("overflow-x: clip;", "")

WIX_CSS = r"""
/* ── Wix host adaptations ── */
html.gx-on body, html.gx-on #site-root, html.gx-on #masterPage, html.gx-on #PAGES_CONTAINER { background-color: #050506 !important; }
.gxg { display: block; position: relative; flex: none; min-width: 0; max-width: none; width: var(--gxw, 100vw) !important; margin-left: var(--gxl, calc((980px - var(--gxw, 100vw)) / 2)); background: #050506; clip-path: inset(0); isolation: isolate; text-align: left; }
.gxg[data-part="a"]:not(.is-ready) { background: transparent; }
.gxg[data-part="a"]:not(.is-ready) .kb { opacity: 0; }
.gxg.gxg-float { width: 0 !important; height: 0; margin: 0; clip-path: none; background: none; position: static; }
.gxg > section, .gxg > .foot { position: relative; z-index: 1; }
.gxg .slot { height: 60px; width: 100%; }
.gxg .nav { position: absolute; }
.gxg .nav__logo img { height: 26px; width: auto; }
.gxg .nav__sp { width: 120px; }
.gxg .hero__copy { position: absolute; z-index: 3; top: 50vh; bottom: auto; left: clamp(56px, 8vw, 240px); width: min(42vw, 760px); transform: translateY(-50%); }
.gxg .hero .h1 { font-size: clamp(40px, 4.6vw, 96px); }
.gxg .kb:not(.is-js) { transform: translate(-50%, -50%) translate(16vw, 5.5vh) rotateX(48deg) rotateZ(-24deg) scale(1.06); }
.gxg .hero__sub { margin: 18px 0 26px; }
.gxg .hero .cta__offer { margin-bottom: 14px; }
.gxg .strip__in { width: 980px; max-width: calc(100% - 40px); margin-inline: auto; height: 160px; display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; gap: 30px; padding: 0; }
.gxg .strip .slot { width: 450px; flex: none; }
.gxg .strip__offer { font-size: 25px; white-space: nowrap; }
.gxg .end { min-height: 0; height: 820px; padding: 0; margin-top: 0; display: block; }
.gxg .end__in { position: absolute; left: var(--gut); top: 0; height: 710px; width: min(60vw, 820px); padding: 0; display: flex; flex-direction: column; justify-content: flex-end; }
.gxg .end .lede { margin: 20px 0 26px; }
.gxg .end .cta__offer { margin-bottom: 14px; }
.gxg .end__h { font-size: clamp(36px, 4vw, 76px); }
@media (min-width: 901px) and (max-width: 1799px) {
  .gxg .kb:not(.is-js) { transform: translate(-50%, -50%) translate(22vw, 5.5vh) rotateX(48deg) rotateZ(-24deg) scale(1.06); }
}
@media (max-width: 900px) {
  .gxg .kb:not(.is-js) { transform: translate(-50%, -50%) translate(10vw, -25vh) rotateX(58deg) rotateZ(-27deg) scale(1.5); }
  .gxg .hero__copy { left: var(--gut); right: var(--gut); width: auto; top: 31vh; bottom: auto; transform: none; }
  .gxg .hero .h1 { font-size: 27px; }
  .gxg .hero .eyebrow { margin-bottom: 10px; }
  .gxg .hero__sub { margin: 10px 0 14px; font-size: 14px; }
  .gxg .hero .cta__offer { font-size: 16px; margin-bottom: 10px; }
  .gxg .nav { padding: 12px var(--gut); }
  .gxg .nav__sp { display: none; }
  .gxg .strip__in { height: auto; flex-direction: column; align-items: flex-start; padding: 28px 0 20px; }
  .gxg .strip .slot { width: 100%; height: 52px; }
  .gxg .strip__in { max-width: none; width: auto; margin-inline: var(--gut); }
  .gxg .strip__offer { white-space: normal; font-size: 20px; }
  .gxg .end__in { left: var(--gut); right: var(--gut); width: auto; }
  .gxg .slot { height: 52px; }
  .gxg .end { height: 640px; }
  .gxg .end__in { height: 560px; }
}
"""
CSS = scoped + WIX_CSS

# ───────── JS → mount inside custom elements ─────────
j = js
j = must(j, "(() => {\n  const $ = (s, c = document) => c.querySelector(s);", "function GX_INIT(A) {\n  const $ = (s, c = document) => c.querySelector(s);")
assert j.rstrip().endswith("})();"); j = j.rstrip()[:-5] + "}\n"
# no smooth-scroll library, no anchors, no nav logic, no custom forms on Wix
blk = between(j, "  /* ───────── smooth scroll ───────── */", "  /* ───────── the page glow follows")
j = j.replace(blk, "  const lenis = null;\n\n")
blk = between(j, "  /* ───────── nav ───────── */", "  /* ───────── numbers roll up")
j = j.replace(blk, "")
j = must(j, "    if (lenis) lenis.on('scroll', (e) => { vel = e.velocity; });", "    let ly = scrollY; addEventListener('scroll', () => { vel = clamp(-40, 40, (scrollY - ly) * 0.25); ly = scrollY; }, { passive: true });")
j = must(j, "      .to('.hero__copy', { autoAlpha: 0, y: -50, duration: 0.14 }, 0.02)\n", "")
j = must(j, "      gsap.from('.nav', { yPercent: -120, duration: 1, delay: 0.5, ease: 'expo.out', clearProps: 'transform' });\n", "")
j = must(j, "  zone('.strip', () => { cycleOn = true; });\n", "")
j = must(j, "const refresh = () => { clearTimeout(rT); rT = setTimeout(() => ScrollTrigger.refresh(), 250); };", "const refresh = () => { clearTimeout(rT); rT = setTimeout(() => { if (window.__gxLayout) window.__gxLayout(); ScrollTrigger.refresh(); }, 250); };")
j = j.replace("`assets/seq/a-${n}${suf}.webp`", "A(`seq/a-${n}${suf}.webp`)")
assert "assets/" not in j, [m.start() for m in re.finditer("assets/", j)]
# cursor lives outside the clipped roots
j = must(j, "    const cur = $('.cursor'), ring = $('.cursor b');", "    const fl = document.createElement('div'); fl.className = 'gxg gxg-float'; fl.innerHTML = '<div class=\"cursor\" aria-hidden=\"true\"><i></i><b></b></div>'; document.body.appendChild(fl);\n    const cur = $('.cursor', fl), ring = $('.cursor b', fl);")
j = must(j, "      const hot = t.closest('a,button,input,[role=tab],.pos__p,.pos__title span,.game__tok li');", "      const hot = t.closest('a,button,input,[role=tab],.pos__p,.pos__title span,.game__tok li') || !t.closest('.gxg');")
j = must(j, "    addEventListener('mousemove', (e) => { x(e.clientX); y(e.clientY); cur.style.opacity = 1; }, { passive: true });", "    addEventListener('mousemove', (e) => { x(e.clientX); y(e.clientY); cur.style.opacity = e.target.closest && e.target.closest('.gxg') ? 1 : 0; }, { passive: true });")
# the typing demo must not swallow keys typed into Wix inputs
j = must(j, "if (e.target.closest && e.target.closest('input,textarea,[role=slider]')) return;", "if (e.target.closest && e.target.closest('input,textarea,select,[contenteditable],[role=slider]')) return;")

VENDOR = [open(R + '/wix/vendor/%s.min.js' % n, encoding='utf-8').read().replace('%', '%%') and open(R + '/wix/vendor/%s.min.js' % n, encoding='utf-8').read() for n in ('gsap', 'ScrollTrigger')]
def bundle(amap, tag):
    parts = {k: re.sub(r'(src|href)="assets/([^"]+)"', lambda m: '%s="%s"' % (m.group(1), amap(m.group(2))), v) for k, v in PARTS.items()}
    for v in parts.values(): assert '="assets/' not in v
    seq = {k: amap(k) for k in MAP if k.startswith("seq/")}
    return """/* biaXbew Genesis01 landing — Wix custom element. Generated by wix/build_wix.py — do not edit by hand. */
(function () {
  if (window.__gxGenesis) return; window.__gxGenesis = true;
  var CSS = %s;
  var PARTS = %s;
  var SEQ = %s;
  var ORDER = ['a', 'c', 'b', 'd'];
  var LIBS = [];
  if (!window.gsap) { (function () { var exports, module, define; %s
 }).call(window); }
  if (!window.ScrollTrigger) { (function () { var exports, module, define; %s
 }).call(window); }
  function A(p) { return SEQ[p] || SEQ[p.replace('@m', '')]; }
  function head() {
    if (document.getElementById('gxg-css')) return;
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = 'https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,300..800;1,62..125,300..800&family=JetBrains+Mono:wght@400;500&display=swap'; document.head.appendChild(l);
    var s = document.createElement('style'); s.id = 'gxg-css'; s.textContent = CSS; document.head.appendChild(s);
    document.documentElement.classList.add('gx-on');
    var w = function () { document.documentElement.style.setProperty('--gxw', document.documentElement.clientWidth + 'px'); layout(); };
    w(); addEventListener('resize', w);
    [300, 1200, 3000, 6000].forEach(function (t) { setTimeout(layout, t); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  }
  function load(i, done) { if (i >= LIBS.length) return done(); if ((i === 0 && window.gsap) || (i === 1 && window.ScrollTrigger)) return load(i + 1, done); var s = document.createElement('script'); s.src = LIBS[i]; s.onload = function () { load(i + 1, done); }; document.head.appendChild(s); }
  function layout() {
    [].forEach.call(document.querySelectorAll('%s'), function (host) {
      var wrap = host.parentElement; if (!wrap) return;
      host.style.setProperty('--gxl', '0px');
      host.style.setProperty('--gxl', (-host.getBoundingClientRect().left) + 'px');
      var slot = host.querySelector('.slot'), grid = wrap.parentElement; if (!slot || !grid) return;
      var form = [].filter.call(grid.querySelectorAll('form'), function (f) { return !f.closest('.gxg'); })[0]; if (!form) return;
      var t = form; while (t.parentElement && t.parentElement !== grid) t = t.parentElement; if (t.parentElement !== grid) return;
      t.style.transform = 'none';
      var a = slot.getBoundingClientRect(), b = t.getBoundingClientRect();
      t.style.transform = 'translate(' + Math.round(a.left - b.left) + 'px,' + Math.round(a.top - b.top) + 'px)';
      t.style.zIndex = 5;
    });
  }
  window.__gxLayout = layout;
  var started = false;
  function start() {
    if (started) return;
    var els = [].slice.call(document.querySelectorAll('%s'));
    if (els.length < ORDER.length || els.some(function (e) { return !e.__gx; })) return;
    started = true;
    load(0, function () { try { GX_INIT(A); } catch (e) { console.error('[gx-genesis]', e); } });
  }
  var El = function () { return Reflect.construct(HTMLElement, [], El); };
  El.prototype = Object.create(HTMLElement.prototype); El.prototype.constructor = El; Object.setPrototypeOf(El, HTMLElement);
  El.prototype.connectedCallback = function () {
    if (this.__gx) return;
    head();
    var all = [].slice.call(document.querySelectorAll('%s'));
    var part = this.getAttribute('part') || ORDER[all.indexOf(this)] || 'a';
    this.classList.add('gxg'); this.setAttribute('data-part', part);
    this.innerHTML = PARTS[part] || '';
    this.__gx = true;
    if (part === 'a') {            // a native Wix background still shows first; swap to the live keyboard once its image is in
      var self = this, img = this.querySelector('.kb__top'), done = false;
      var ready = function () { if (done) return; done = true; self.classList.add('is-ready'); var sec = self.closest('section'); var bg = sec && sec.querySelector('[data-testid="bgLayers"], [id^="bgLayers"]'); if (bg) bg.style.visibility = 'hidden'; };
      if (img && img.complete && img.naturalWidth) ready(); else if (img) { img.addEventListener('load', ready); img.addEventListener('error', ready); }
      setTimeout(ready, 8000);
    }
    setTimeout(start, 0); setTimeout(start, 400); setTimeout(start, 1500);
  };
  customElements.define('%s', El);

%s
})();
""" % (json.dumps(CSS), json.dumps(parts, ensure_ascii=False), json.dumps(seq), VENDOR[0], VENDOR[1], tag, tag, tag, tag, j)

os.makedirs(OUT, exist_ok=True)
open(OUT + "/gx-genesis.js", "w", encoding="utf-8").write(bundle(lambda p: MAP[p], "gx-genesis"))
open(OUT + "/gx-genesis.local.js", "w", encoding="utf-8").write(bundle(lambda p: "../../assets/" + p, "gx-genesis"))
FORM = '<div class="wxw" style="margin:%s 0 0 calc(50%% - 490px + %dpx)"><div><form class="wxform" onsubmit="return false"><input placeholder="Email"><button>Sign up</button></form></div></div>'
sec = lambda part, form="": '<section class="wxsec"><div class="wxgrid"><div class="wxcomp"><gx-genesis part="%s"></gx-genesis></div>%s</div></section>' % (part, form)
open(OUT + "/host.html", "w", encoding="utf-8").write("""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wix host mock</title>
<style>body{margin:0;background:#fff;overflow-y:scroll;font-family:Helvetica}.wxsec{position:relative;width:100%%;min-width:980px}.wxgrid{display:grid;grid-template-rows:1fr;grid-template-columns:100%%}
.wxgrid>*{grid-area:1/1/2/2;place-self:start;position:relative}.wxcomp{margin-left:calc(50%% - 490px);min-height:100px}
.wxform{display:flex;gap:8px;z-index:5}.wxform input{width:330px;height:54px;border-radius:999px;border:1px solid #fff3;background:#ffffff14;color:#fff;padding:0 22px;font-size:16px;box-sizing:border-box}.wxform button{width:150px;height:54px;border-radius:999px;border:0;background:#f2f1ec;font-weight:700}</style>
%s%s%s%s<script src="gx-genesis.local.js"></script>""" % (sec("a", FORM % ("588px", 0)), sec("c", FORM % ("50px", 530)), sec("b"), sec("d", FORM % ("650px", 0))))
print("ok", {k: len(v) for k, v in PARTS.items()}, "css", len(CSS), "bundle", os.path.getsize(OUT + "/gx-genesis.js"))
