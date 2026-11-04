// Lucy AI Studio · Japan plan v2 — scroll engine, 3D choreography and page motion
import { createStage } from './stage.js';
import { NOTES } from './notes.js';

if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
const gsap = window.gsap, ScrollTrigger = window.ScrollTrigger, SplitText = window.SplitText;
gsap.registerPlugin(ScrollTrigger, SplitText);

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (p, a, b) => clamp((p - a) / (b - a));
const easeIO = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const easeO = t => 1 - Math.pow(1 - t, 3);
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const isMobile = () => innerWidth <= 820;
if (reduced) document.documentElement.classList.add('reduced');

const LABELS = [
  { zh: '判断', en: 'WHY LUCY', ch: 'CH 01 核心判断 · 02 受众与场景' },
  { zh: '市场', en: 'MARKET', ch: 'CH 03 市场与竞争' },
  { zh: '定价', en: 'MONEY', ch: 'CH 04 定价经济 · 05 资金转化' },
  { zh: '渠道', en: 'REACH', ch: 'CH 06 页面渠道 · 07 KOL 广告' },
  { zh: '执行', en: 'EXECUTE', ch: 'CH 08 时间执行 · 09 可行资产' },
];

/* ------------------------------------------------------------------ */
/* smooth scroll                                                       */
/* ------------------------------------------------------------------ */
let lenis = null;
if (!reduced && window.Lenis) {
  lenis = new window.Lenis({ lerp: 0.085, wheelMultiplier: 0.95, smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  lenis.stop();
}
const scrollY = () => lenis ? lenis.scroll : window.scrollY;
function scrollToY(y, immediate) {
  if (lenis) lenis.scrollTo(y, { duration: immediate ? 0 : 1.8, immediate, easing: t => 1 - Math.pow(1 - t, 4) });
  else window.scrollTo({ top: y, behavior: immediate ? 'auto' : 'smooth' });
}

/* ------------------------------------------------------------------ */
/* scenes (pinned, scroll-scrubbed)                                    */
/* ------------------------------------------------------------------ */
const sceneEls = $$('[data-scene]');
let scenes = [];
function measure() {
  const y = window.scrollY;
  scenes = sceneEls.map(el => {
    const top = el.getBoundingClientRect().top + y;
    return { el, type: el.dataset.scene, drive: +el.dataset.drive - 1, start: top, end: top + el.offsetHeight - innerHeight };
  });
}
const sceneById = id => scenes.find(s => s.el.id === id);
function goTo(sel) {
  if (sel === '#hero') return scrollToY(0);
  const s = sceneById(sel.slice(1));
  if (s && s.type === 'drive') return scrollToY(s.start + (s.end - s.start) * 0.64);
  const el = $(sel); if (el) scrollToY(el.getBoundingClientRect().top + scrollY());
}

/* ------------------------------------------------------------------ */
/* camera views                                                        */
/* ------------------------------------------------------------------ */
const V = {
  hero0: { az: -0.66, el: 0.30, dist: 1.05, sx: 0.22, sy: 0.03, ty: 0.108, tz: 0 },
  hero1: { az: -0.30, el: 0.20, dist: 0.92, sx: 0.16, sy: 0.02, ty: 0.108, tz: 0 },
  front: { az: 0.0, el: 0.10, dist: 0.74, sx: 0.0, sy: 0.0, ty: 0.108, tz: 0 },
  bay: { az: -0.16, el: 0.16, dist: 0.70, sx: 0.12, sy: 0, ty: 0.095, tz: 0.02 },
  outro: { az: -0.55, el: 0.24, dist: 1.2, sx: 0, sy: -0.15, ty: 0.108, tz: 0 },
};
const driveView = i => ({ az: -0.7 + i * 0.04, el: 0.42 - i * 0.02, dist: 0.84, sx: 0.19, sy: 0.06, ty: 0.075 + 0.012 * i, tz: 0.06 });
function mob(v) {
  if (!isMobile()) return v;
  return { ...v, sx: 0, sy: -0.2, dist: v.dist * 1.75 };
}
const mixV = (a, b, t) => { const o = {}; for (const k in a) o[k] = lerp(a[k], b[k] ?? a[k], t); return o; };

function baseState() {
  return { az: 0, el: 0, dist: 0.7, sx: 0, sy: 0, ty: 0.1, tz: 0, cover: 0, drives: [0, 0, 0, 0, 0], hover: [0, 0, 0, 0, 0], sleeve: 0, sleeveDrive: 0, idle: 0, spin: 0, ribA: 0, ribB: 0, interactive: 'none', drag: false };
}

function sceneState(s, p) {
  const S = baseState();
  if (s.type === 'hero') {
    Object.assign(S, mob(mixV(V.hero0, V.hero1, easeIO(p))));
    S.idle = 1 - p; S.drag = true;
  } else if (s.type === 'spin') {
    const sv = { az: -0.3, el: 0.16, dist: 1.0, sx: 0, sy: 0.0, ty: 0.11, tz: 0 };
    let v = mixV(V.hero1, sv, easeIO(seg(p, 0, 0.1)));
    v = mixV(v, V.hero1, easeIO(seg(p, 0.9, 1)));
    Object.assign(S, mob(v));
    S.spin = easeIO(seg(p, 0.04, 0.94)) * Math.PI * 2;
    S.ribB = easeIO(seg(p, 0.03, 0.55)); S.ribA = easeIO(seg(p, 0.82, 0.97));
  } else if (s.type === 'unbox') {
    let v = mixV(V.hero1, V.front, easeIO(seg(p, 0, 0.24)));
    v = mixV(v, V.bay, easeIO(seg(p, 0.5, 0.66)));
    v = mixV(v, driveView(0), easeIO(seg(p, 0.86, 1)));
    Object.assign(S, mob(v));
    S.cover = easeIO(seg(p, 0.16, 0.5));
    const w = seg(p, 0.6, 0.82);
    S.drives = S.drives.map((_, k) => 0.12 * Math.max(0, Math.sin(clamp(w * 1.6 - k * 0.15) * Math.PI)));
    S.drag = p < 0.15; S.interactive = p > 0.6 ? 'drives' : 'none';
  } else if (s.type === 'drive') {
    const i = s.drive, prev = i - 1;
    const from = i === 0 ? driveView(0) : driveView(prev);
    let v = mixV(from, driveView(i), easeIO(seg(p, 0.16, 0.46)));
    v.dist *= 1 - 0.1 * easeIO(seg(p, 0.8, 1));
    Object.assign(S, mob(v));
    S.cover = 1;
    if (prev >= 0) S.drives[prev] = 1 - seg(p, 0.1, 0.32);
    S.drives[i] = seg(p, 0.3, 0.58);
    if (prev >= 0 && p < 0.18) { S.sleeve = 1 - easeIO(seg(p, 0, 0.16)); S.sleeveDrive = prev; }
    if (p > 0.78) { S.sleeve = easeIO(seg(p, 0.8, 1)); S.sleeveDrive = i; }
    S.interactive = p > 0.2 && p < 0.8 ? 'drives' : 'none';
  } else if (s.type === 'outro') {
    let v = mixV(driveView(4), V.outro, easeIO(seg(p, 0.22, 0.7)));
    Object.assign(S, mob(v));
    S.cover = 1 - easeIO(seg(p, 0.3, 0.62));
    S.drives[4] = 1 - seg(p, 0.08, 0.3);
    if (p < 0.16) { S.sleeve = 1 - easeIO(seg(p, 0, 0.14)); S.sleeveDrive = 4; }
    S.idle = seg(p, 0.6, 1);
    S.ribB = easeIO(seg(p, 0.55, 0.95));
  }
  return S;
}

function currentScene(y) {
  let cur = null;
  for (const s of scenes) if (y >= s.start - 1) cur = s;
  if (!cur) return { s: scenes[0], p: 0 };
  return { s: cur, p: clamp((y - cur.start) / Math.max(1, cur.end - cur.start)) };
}

/* ------------------------------------------------------------------ */
/* stage + overlay                                                     */
/* ------------------------------------------------------------------ */
const canvas = $('#stage');
const loaderNum = $('#lcNum'), loaderBar = $('#lcBar');
let loadP = 0, shownP = 0;
const stage = createStage(canvas, { onProgress: p => { loadP = p; }, mobile: isMobile(), labels: LABELS });

const pointer = { x: innerWidth / 2, y: innerHeight / 2, nx: 0, ny: 0, sx: 0, sy: 0, down: false, lastX: 0, lastY: 0, moved: 0 };
const user = { yaw: 0, pitch: 0, vy: 0 };
const hoverS = [0, 0, 0, 0, 0];
let hoverDrive = -1;

// callouts
const ovCo = $('#ovCo'), ovSvg = $('#ovSvg');
const NS = 'http://www.w3.org/2000/svg';
function mkCo(html, cls = '') { const d = document.createElement('div'); d.className = 'co ' + cls; d.innerHTML = `<span class="pt"></span><span class="cb">${html}</span>`; ovCo.appendChild(d); return d; }
const coUnbox = {
  cover: mkCo('<b>FRONT COVER</b>斜纹前盖 · 可拆卸', 'l'),
  io: mkCo('<b>FRONT I/O</b>USB-A · 3.5mm · USB-C'),
  size: mkCo('<b>222.5 × 222.5 × 224</b>MM · REAL SCALE'),
};
const coDrives = LABELS.map((L, i) => {
  const d = mkCo(`<b>DRIVE 0${i + 1}</b>${L.zh} · ${L.en}`, 'drv');
  d.querySelector('.cb').addEventListener('click', () => goTo('#d' + (i + 1)));
  return d;
});
const coActive = mkCo('<b>DRIVE 01</b>—', 'l');
const pitchLine = document.createElementNS(NS, 'path'); ovSvg.appendChild(pitchLine);
const pitchLbl = mkCo('<b>27 MM PITCH</b>5 × 3.5" SATA', 'l');
const coLine = document.createElementNS(NS, 'path'); coLine.setAttribute('class', 'dash'); ovSvg.appendChild(coLine);

function placeCo(el, world, op) {
  if (!world || op <= 0.001) { el.style.opacity = 0; return null; }
  const s = stage.project(world);
  el.style.opacity = op;
  el.style.transform = `translate(${s.x}px,${s.y}px)`;
  return s;
}

// sleeve
const sleeve = $('#sleeve'), slIn = $('.sl-in', sleeve), slK = $('#slK'), slT = $('#slT');
let lastSleeveDrive = -1;
function drawSleeve(S) {
  if (S.sleeve <= 0.001) { sleeve.style.visibility = 'hidden'; return; }
  const r = stage.driveRect(S.sleeveDrive); if (!r) return;
  if (lastSleeveDrive !== S.sleeveDrive) { lastSleeveDrive = S.sleeveDrive; const L = LABELS[S.sleeveDrive]; slK.textContent = `DRIVE 0${S.sleeveDrive + 1} · ${L.en}`; slT.textContent = L.zh; }
  const t = S.sleeve, W = innerWidth, H = innerHeight;
  const x = lerp(r.x, 0, t), y = lerp(r.y, 0, t), w = lerp(r.w, W, t), h = lerp(r.h, H, t);
  sleeve.style.visibility = 'visible';
  sleeve.style.transform = `translate(${x}px,${y}px)`;
  sleeve.style.width = w + 'px'; sleeve.style.height = h + 'px';
  sleeve.style.borderRadius = lerp(6, 0, t) + 'px';
  sleeve.style.boxShadow = t > 0.98 ? 'none' : '';
  slIn.style.opacity = seg(t, 0.45, 0.85) * (1 - seg(t, 0.97, 1) * 0);
}

// backdrop giant type
const bd = Object.fromEntries($$('[data-bd]').map(e => [e.dataset.bd, e]));
const sbgs = $$('.sbg'), spinDeg = $('#spinDeg');
const SPIN_AT = [0.06, 0.28, 0.5, 0.72];
let spinDark = false;
function drawSpinBg(s, p) {
  const on = s.type === 'spin';
  const c = on && modelReady ? stage.project({ x: 0, y: 0.11, z: 0, clone() { return this; } }) : { x: innerWidth / 2, y: innerHeight / 2 };
  const R = Math.hypot(innerWidth, innerHeight);
  sbgs.forEach((b, i) => {
    const r = on ? easeIO(seg(p, SPIN_AT[i], SPIN_AT[i] + 0.1)) * R * (1 - easeIO(seg(p, 0.9, 0.99))) : 0;
    b.style.clipPath = `circle(${r}px at ${c.x}px ${c.y}px)`;
  });
  spinDark = on && p > SPIN_AT[0] + 0.05 && p < SPIN_AT[1] + 0.05;
  if (on && spinDeg) spinDeg.textContent = String(Math.round(easeIO(seg(p, 0.04, 0.94)) * 360)).padStart(3, '0') + '°';
}
function drawBackdrop(s, p) {
  for (const k in bd) bd[k].style.opacity = 0;
  drawSpinBg(s, p);
  const W = innerWidth;
  if (s.type === 'hero') {
    const e = bd.hero; e.style.opacity = 1 - seg(p, 0.75, 1);
    e.style.transform = `translate(${lerp(0.04, -0.42, p) * W}px,-52%)`;
  } else if (s.type === 'spin') {
    const sv = { az: -0.3, el: 0.16, dist: 1.0, sx: 0, sy: 0.0, ty: 0.11, tz: 0 };
    let v = mixV(V.hero1, sv, easeIO(seg(p, 0, 0.1)));
    v = mixV(v, V.hero1, easeIO(seg(p, 0.9, 1)));
    Object.assign(S, mob(v));
    S.spin = easeIO(seg(p, 0.04, 0.94)) * Math.PI * 2;
    S.ribB = easeIO(seg(p, 0.03, 0.55)); S.ribA = easeIO(seg(p, 0.82, 0.97));
  } else if (s.type === 'unbox') {
    const e = bd.unbox; e.style.opacity = seg(p, 0.08, 0.28) * (1 - seg(p, 0.82, 0.96));
    e.style.transform = `translate(${lerp(0.5, -0.6, p) * W}px,-50%)`;
  } else if (s.type === 'drive') {
    const e = bd['d' + (s.drive + 1)];
    e.style.opacity = seg(p, 0.22, 0.42) * (1 - seg(p, 0.76, 0.86));
    const sc = lerp(0.9, 1.05, p);
    e.style.left = (isMobile() ? 0.5 : 0.66) * W + 'px';
    e.style.transform = `translate(-50%,-52%) scale(${sc})`;
  } else if (s.type === 'outro') {
    const e = bd.outro; e.style.opacity = seg(p, 0.3, 0.5) * (1 - seg(p, 0.92, 1));
    e.style.transform = `translate(${lerp(0.3, -0.7, p) * W}px,-60%)`;
  }
}

/* ------------------------------------------------------------------ */
/* frame loop                                                          */
/* ------------------------------------------------------------------ */
let S = baseState(), modelReady = false, t0 = performance.now(), lastKey = '';
const hud = $('#hud'), hudLinks = $$('#hud a'), navLinks = $$('[data-drive-nav]'), sbar = $('#scrollbar i');
const chapters = $$('.chapter');
const themeBands = chapters.map(c => ({ c, bands: $$('[data-theme]', c), t: '' }));
function updateThemes() {
  const mid = innerHeight * 0.5;
  for (const tb of themeBands) {
    const r = tb.c.getBoundingClientRect();
    if (r.bottom < -200 || r.top > innerHeight + 200) continue;
    let t = 'white';
    for (const b of tb.bands) { const br = b.getBoundingClientRect(); if (br.top <= mid && br.bottom >= mid) t = b.dataset.theme; }
    if (t !== tb.t) { tb.t = t; tb.c.dataset.t = t; }
  }
  // header / HUD contrast: what colour is under the top bar?
  let hdr = '';
  const under = document.elementsFromPoint(innerWidth / 2, 40).find(e => e.closest && e.closest('.chapter,footer,.dcard'));
  if (under) {
    const host = under.closest('.dcard') || under.closest('footer') || under.closest('.chapter');
    if (host.matches('footer') || host.matches('.dcard.c-blue,.dcard.c-ink') || (host.matches('.chapter') && /blue|ink/.test(host.dataset.t || ''))) hdr = 'dark';
  }
  if (spinDark) hdr = 'dark';
  if (document.documentElement.dataset.hdr !== hdr) document.documentElement.dataset.hdr = hdr;
}

function frame(now) {
  const time = (now - t0) / 1000;
  const y = scrollY();
  const { s, p } = currentScene(y);
  if (!s) return;
  S = sceneState(s, p);

  // pointer parallax + drag
  pointer.sx += (pointer.nx - pointer.sx) * 0.06; pointer.sy += (pointer.ny - pointer.sy) * 0.06;
  if (!pointer.down) { user.yaw += user.vy; user.vy *= 0.92; if (!S.drag) user.yaw *= 0.94; user.pitch *= 0.94; }
  S.az += pointer.sx * 0.1 + user.yaw + Math.sin(time * 0.35) * 0.09 * S.idle;
  S.el = clamp(S.el - pointer.sy * 0.05 + user.pitch, 0.02, 1.2);

  // drive hover
  for (let i = 0; i < 5; i++) { hoverS[i] += ((S.interactive === 'drives' && hoverDrive === i ? 1 : 0) - hoverS[i]) * 0.15; S.hover[i] = hoverS[i]; }

  if (modelReady) {
    stage.apply(S, time);
    // skip GPU work while a chapter fully covers the viewport
    let covered = false;
    for (const c of chapters) { const r = c.getBoundingClientRect(); if (r.top <= 0 && r.bottom >= innerHeight) { covered = true; break; } }
    canvas.style.visibility = covered ? 'hidden' : 'visible';
    if (!covered) stage.render();
    drawSleeve(S);
    drawOverlay(s, p, S);
    drawDisc(s, p);
  }
  drawBackdrop(s, p);
  updateThemes();

  // HUD + nav state
  const g = activeGroup(y);
  hud.classList.toggle('show', g.idx >= 0);
  hudLinks.forEach((a, i) => { a.classList.toggle('on', i === g.idx); a.querySelector('.pr').style.width = (i === g.idx ? g.p * 100 : i < g.idx ? 100 : 0) + '%'; });
  navLinks.forEach((a, i) => a.classList.toggle('on', i === g.idx));
  const max = document.documentElement.scrollHeight - innerHeight;
  sbar.style.height = (clamp(y / max) * 100) + '%';
  requestAnimationFrame(frame);
}

const disc = $('#disc');
const DISC_C = ['#2B50E0', '#DCE4FF', '#FF6A3D', '#2B50E0', '#B9C7FF'];
function drawDisc(s, p) {
  let op = 0, sc = 1, col = '#2B50E0', size = isMobile() ? 0.62 : 0.78;
  if (s.type === 'hero') { op = 1 - seg(p, 0.55, 0.85); sc = lerp(0.86, 0.66, p); }
  else if (s.type === 'drive') { op = seg(p, 0.18, 0.4) * (1 - seg(p, 0.76, 0.84)); sc = lerp(0.55, 1.05, easeO(seg(p, 0.15, 0.6))); col = DISC_C[s.drive]; }
  else if (s.type === 'outro') { op = seg(p, 0.35, 0.6); sc = lerp(0.45, 0.72, easeO(seg(p, 0.35, 0.8))); }
  if (op <= 0.001) { disc.style.opacity = 0; return; }
  const c = stage.project({ x: 0, y: 0.1, z: 0.03, clone() { return this; } });
  const d = Math.min(innerHeight, innerWidth * 1.1) * size;
  disc.style.setProperty('--d', d + 'px');
  disc.style.setProperty('--dc', col);
  disc.style.opacity = op;
  disc.style.transform = `translate(${c.x}px,${c.y}px) scale(${sc})`;
}

function activeGroup(y) {
  const vh = innerHeight;
  const drives = scenes.filter(s => s.type === 'drive');
  const outro = scenes.find(s => s.type === 'outro');
  let idx = -1, p = 0;
  drives.forEach((d, i) => {
    const a = d.start - vh * 0.3, b = (drives[i + 1] ? drives[i + 1].start : outro.start) - vh * 0.3;
    if (y >= a && y < b) { idx = i; p = clamp((y - a) / (b - a)); }
  });
  return { idx, p };
}

function drawOverlay(s, p, S) {
  const mob = isMobile();
  let pl = '', cl = '';
  // unbox annotations
  const u = s.type === 'unbox' ? p : -1;
  const a1 = u < 0 ? 0 : seg(u, 0.05, 0.14) * (1 - seg(u, 0.3, 0.4));
  placeCo(coUnbox.cover, stage.nodeWorld('Front_Bay_Door_Base', [-0.06, -0.02, 0.01]), mob ? 0 : a1);
  placeCo(coUnbox.io, stage.nodeWorld('Front_IO_USB_C', [0.03, 0, 0.003]), a1);
  placeCo(coUnbox.size, stage.nodeWorld('Top_Right_Front_Screw', [0.01, 0.002, 0]), mob ? 0 : a1);
  const a2 = u < 0 ? 0 : seg(u, 0.56, 0.66) * (1 - seg(u, 0.9, 0.98));
  coDrives.forEach((c, i) => { placeCo(c, stage.driveAnchor(i, 1), mob ? 0 : a2); c.querySelector('.cb').style.pointerEvents = a2 > 0.5 ? 'auto' : 'none'; c.classList.toggle('hov', hoverDrive === i); });
  if (a2 > 0) {
    const top = stage.driveAnchor(4, -1), bot = stage.driveAnchor(0, -1);
    if (top && bot) {
      const A = stage.project(top), B = stage.project(bot), off = -34;
      pl = `M${A.x + off + 8} ${A.y}H${A.x + off}V${B.y}H${B.x + off + 8}`;
      for (let k = 1; k < 4; k++) { const m = stage.project(stage.driveAnchor(k, -1)); pl += `M${m.x + off} ${m.y}h6`; }
      placeCo(pitchLbl, top.clone().lerp(bot, 0.5).add({ x: -0.03, y: 0, z: 0 }), mob ? 0 : a2);
    }
  } else pitchLbl.style.opacity = 0;
  pitchLine.setAttribute('d', pl); pitchLine.style.opacity = a2;
  // active drive callout during drive scenes
  if (s.type === 'drive') {
    const op = seg(p, 0.5, 0.6) * (1 - seg(p, 0.74, 0.8));
    const i = s.drive;
    if (coActive.dataset.i !== String(i)) { coActive.dataset.i = i; coActive.querySelector('.cb').innerHTML = `<b>DRIVE 0${i + 1} · PULLED</b>${LABELS[i].ch}`; }
    const w = stage.driveAnchor(i, -1);
    const sp = placeCo(coActive, w, mob ? 0 : op);
    if (sp && op > 0) { cl = `M${sp.x} ${sp.y}L${sp.x - 60} ${sp.y + 60}`; }
  } else coActive.style.opacity = 0;
  coLine.setAttribute('d', cl);
}

/* ------------------------------------------------------------------ */
/* pointer: parallax, drag-rotate, drive picking, cursor               */
/* ------------------------------------------------------------------ */
const cursor = $('#cursor'), cRing = $('.c-ring', cursor), cDot = $('.c-dot', cursor), cLb = $('.c-lb', cursor);
const cur = { x: innerWidth / 2, y: innerHeight / 2, rx: innerWidth / 2, ry: innerHeight / 2 };
let cursorMode = '';
function setCursor(mode, label) {
  if (cursorMode === mode + label) return; cursorMode = mode + label;
  cursor.classList.toggle('big', mode === 'big'); cursor.classList.toggle('link', mode === 'link');
  if (label) cLb.textContent = label;
}
gsap.ticker.add(() => {
  cur.rx += (cur.x - cur.rx) * 0.18; cur.ry += (cur.y - cur.ry) * 0.18;
  cDot.style.transform = `translate(${cur.x}px,${cur.y}px)`;
  cRing.style.transform = `translate(${cur.rx}px,${cur.ry}px)`;
  cLb.style.transform = `translate(${cur.rx}px,${cur.ry}px) translate(-50%,-50%)`;
});

function overUI(t) { return t.closest('a,button,.cb,.strip,.tbw,.gwrap,input,#menu,#hud,#hdr,.kol,.chapter,.seg'); }
addEventListener('pointermove', e => {
  pointer.x = e.clientX; pointer.y = e.clientY;
  pointer.nx = e.clientX / innerWidth - 0.5; pointer.ny = e.clientY / innerHeight - 0.5;
  cur.x = e.clientX; cur.y = e.clientY;
  if (pointer.down) {
    const dx = e.clientX - pointer.lastX, dy = e.clientY - pointer.lastY;
    user.yaw += dx * 0.006; user.vy = dx * 0.006; user.pitch = clamp(user.pitch + dy * 0.003, -0.25, 0.4);
    pointer.lastX = e.clientX; pointer.lastY = e.clientY; pointer.moved += Math.abs(dx) + Math.abs(dy);
  }
  const ui = overUI(e.target);
  hoverDrive = -1;
  if (!ui && modelReady) {
    if (S.interactive === 'drives') {
      const h = stage.pick(e.clientX, e.clientY, true);
      if (h && h.drive >= 0) { hoverDrive = h.drive; setCursor('big', `OPEN 0${h.drive + 1}`); return; }
    }
    if (S.drag) { const h = stage.pick(e.clientX, e.clientY, false); if (h) { setCursor('big', pointer.down ? 'ROTATE' : 'DRAG'); return; } }
  }
  const lab = e.target.closest('[data-cursor]');
  if (lab && (lab.matches('.strip') || lab.matches('a.thumb'))) { setCursor('big', lab.dataset.cursor); return; }
  if (e.target.closest('a,button,.cb')) { setCursor('link'); return; }
  setCursor('', '');
}, { passive: true });
addEventListener('pointerdown', e => {
  if (overUI(e.target) || !S.drag || e.button !== 0) return;
  if (!modelReady || !stage.pick(e.clientX, e.clientY, false)) return;
  pointer.down = true; pointer.lastX = e.clientX; pointer.lastY = e.clientY; pointer.moved = 0;
});
addEventListener('pointerup', () => { pointer.down = false; });
addEventListener('click', e => {
  if (overUI(e.target) || hoverDrive < 0) return;
  goTo('#d' + (hoverDrive + 1));
});

/* ------------------------------------------------------------------ */
/* DOM motion                                                          */
/* ------------------------------------------------------------------ */
// rolling letters
$$('[data-roll]').forEach(el => {
  const txt = el.textContent; el.textContent = ''; el.setAttribute('aria-label', txt);
  [...txt].forEach((c, i) => { const s = document.createElement('span'); s.className = 'ch'; s.textContent = c; s.dataset.c = c; s.style.setProperty('--i', i); s.setAttribute('aria-hidden', 'true'); el.appendChild(s); });
});

// nav
$$('[data-go]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); closeMenu(); goTo(a.dataset.go); }));
const menu = $('#menu'), menuBtn = $('#menuBtn');
let menuOpen = false;
function openMenu() {
  if (menuOpen) return; menuOpen = true; menuBtn.setAttribute('aria-expanded', 'true'); lenis?.stop();
  gsap.set(menu, { visibility: 'visible' });
  gsap.to(menu, { clipPath: 'inset(0 0 0% 0)', duration: 0.9, ease: 'expo.inOut' });
  gsap.fromTo('#menu .mrow', { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, stagger: 0.06, duration: 0.9, ease: 'expo.out', delay: 0.35 });
  menuBtn.querySelector('.roll').setAttribute('aria-label', 'CLOSE');
}
function closeMenu() {
  if (!menuOpen) return; menuOpen = false; menuBtn.setAttribute('aria-expanded', 'false'); lenis?.start();
  gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: 0.8, ease: 'expo.inOut', onComplete: () => gsap.set(menu, { visibility: 'hidden' }) });
}
menuBtn.addEventListener('click', () => menuOpen ? closeMenu() : openMenu());
$$('[data-open-menu]').forEach(b => b.addEventListener('click', openMenu));
addEventListener('keydown', e => {
  if (/input|textarea/i.test(e.target.tagName)) return;
  if (e.key === 'm' || e.key === 'M') { e.preventDefault(); menuOpen ? closeMenu() : openMenu(); }
  if (e.key === 'Escape') closeMenu();
  if (/^[1-5]$/.test(e.key)) { closeMenu(); goTo('#d' + e.key); }
});

// magnetic pills
$$('.pill').forEach(b => {
  b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * 0.25, y: (e.clientY - r.top - r.height / 2) * 0.35, duration: 0.5, ease: 'power3.out' }); });
  b.addEventListener('pointerleave', () => gsap.to(b, { x: 0, y: 0, duration: 0.8, ease: 'elastic.out(1,.4)' }));
});

// marquees, speed follows scroll velocity
const mqs = $$('[data-mq]').map(tr => {
  const span = tr.firstElementChild; for (let i = 0; i < 5; i++) tr.appendChild(span.cloneNode(true));
  return { tr, dir: +tr.dataset.mq, x: 0, w: 0 };
});
let lastY = 0, vel = 0;
gsap.ticker.add(() => {
  const y = scrollY(); const v = y - lastY; lastY = y;
  vel += (v - vel) * 0.1;
  mqs.forEach(m => {
    m.w = m.w || m.tr.firstElementChild.offsetWidth;
    const sp = (1.1 + Math.min(Math.abs(vel) * 0.25, 14)) * (vel < -0.3 ? -1 : 1) * m.dir;
    m.x -= sp; if (m.x <= -m.w) m.x += m.w; if (m.x > 0) m.x -= m.w;
    m.tr.style.transform = `translate3d(${m.x}px,0,0)`;
  });
});

function initScrollMotion() {
  // headings: split chars, rise from mask (More / Lusion)
  $$('.sp').forEach(h => {
    const split = new SplitText(h, { type: 'lines,chars', linesClass: 'sl-line', mask: 'lines' });
    gsap.from(split.chars, { yPercent: 115, rotate: 6, duration: 1.1, ease: 'expo.out', stagger: 0.035, scrollTrigger: { trigger: h, start: 'top 88%' } });
  });
  // generic reveals
  ScrollTrigger.batch('.rv', { start: 'top 90%', once: true, onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.07, overwrite: true }) });
  // highlighter
  $$('.mk').forEach(m => ScrollTrigger.create({ trigger: m, start: 'top 80%', once: true, onEnter: () => m.classList.add('on') }));
  // tilted stack cards (More)
  $$('.stack').forEach(st => {
    const cards = $$('.card', st);
    gsap.fromTo(cards, { y: 220, rotate: i => [-9, 6, -5, 8][i % 4], opacity: 0 }, { y: 0, rotate: 0, opacity: 1, duration: 1.4, ease: 'expo.out', stagger: 0.1, scrollTrigger: { trigger: st, start: 'top 85%' } });
    cards.forEach(c => tilt(c, 6));
  });
  // big colour card deck: each card rises over the previous one (More / Lusion)
  const deck = $('#deck');
  if (deck) {
    const cards = $$('.dcard', deck), bars = $$('.deck-prog b', deck);
    gsap.set(cards.slice(1), { yPercent: 110, rotate: 5 });
    const tl = gsap.timeline({ scrollTrigger: { trigger: deck, start: 'top top', end: 'bottom bottom', scrub: 0.6 } });
    tl.fromTo(bars[0], { scaleX: 0 }, { scaleX: 1, duration: 1, ease: 'none' }, 0);
    cards.forEach((c, i) => {
      if (!i) return;
      tl.to(c, { yPercent: 0, rotate: 0, duration: 1, ease: 'power3.out' }, i)
        .to(cards[i - 1], { scale: 0.9, yPercent: -4, filter: 'brightness(.72)', duration: 1, ease: 'power2.out' }, i)
        .fromTo($$('.dc-num, h3, p, .dc-tag', c), { y: 80, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.06, duration: 0.6 }, i + 0.35)
        .fromTo(bars[i], { scaleX: 0 }, { scaleX: 1, duration: 1, ease: 'none' }, i);
    });
    tl.to({}, { duration: 0.4 });
    gsap.from(cards[0], { yPercent: 30, rotate: -4, opacity: 0, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: deck, start: 'top 80%' } });
  }
  // full-screen statements: words light up as you scroll
  $$('[data-stmt]').forEach(st => {
    const t = $('.stmt-t', st);
    const split = new SplitText(t, { type: 'chars', charsClass: 'w' });
    gsap.timeline({ scrollTrigger: { trigger: st, start: 'top 60%', end: 'bottom bottom', scrub: 0.5 } })
      .fromTo(t, { scale: 0.86 }, { scale: 1, duration: 1, ease: 'none' }, 0)
      .to(split.chars, { opacity: 1, stagger: 0.08, duration: 0.3, ease: 'none' }, 0.05)
      .fromTo($$('.stmt-k, .stmt-s', st), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3 }, 0.6);
  });
  // tiers fan-in
  $$('.tiers').forEach(t => gsap.fromTo($$('.tier', t), { rotateX: -55, y: 120, opacity: 0, transformOrigin: '50% 100%' }, { rotateX: 0, y: 0, opacity: 1, duration: 1.3, ease: 'expo.out', stagger: 0.1, scrollTrigger: { trigger: t, start: 'top 85%' } }));
  $$('.tier,.kol').forEach(c => tilt(c, 5));
  // count-up numbers
  $$('[data-count]').forEach(n => {
    const end = +n.dataset.count, obj = { v: 0 };
    ScrollTrigger.create({ trigger: n, start: 'top 92%', once: true, onEnter: () => gsap.to(obj, { v: end, duration: 1.6, ease: 'expo.out', onUpdate: () => { n.textContent = Math.round(obj.v).toLocaleString('en-US'); } }) });
  });
  // image parallax
  $$('[data-par]').forEach(img => gsap.fromTo(img, { yPercent: -7 }, { yPercent: 7, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));
  // horizontal gallery (oryzo)
  $$('.hgal').forEach(g => {
    const track = $('.hgal-track', g), bar = $('.hgal-bar i', g), cards = $$('.aud', g);
    const mm = gsap.matchMedia();
    mm.add('(min-width: 821px)', () => {
      const dist = () => track.scrollWidth - innerWidth;
      gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: g, start: 'top top', end: 'bottom bottom', scrub: 0.6, invalidateOnRefresh: true, onUpdate: self => {
        bar.style.width = self.progress * 100 + '%';
        const cx = innerWidth / 2;
        cards.forEach(c => { const r = c.getBoundingClientRect(); const d = clamp(Math.abs(r.left + r.width / 2 - cx) / innerWidth, 0, 1); c.style.transform = `scale(${1 - d * 0.22}) rotate(${(r.left + r.width / 2 - cx) / innerWidth * 4}deg)`; c.querySelector('img').style.transform = `scale(${1.12 + d * 0.1}) translateX(${(r.left + r.width / 2 - cx) / innerWidth * -30}px)`; });
      } } });
    });
  });
  // price ladder
  const lad = $('#ladder');
  if (lad) {
    const tl = gsap.timeline({ scrollTrigger: { trigger: lad, start: 'top 75%' } });
    tl.from($('.ax', lad), { scaleX: 0, duration: 1.2, ease: 'expo.inOut' })
      .from($$('.tk', lad), { opacity: 0, y: 10, stagger: 0.05, duration: 0.5 }, '-=0.6')
      .from($$('.lad-pt', lad), { scale: 0, opacity: 0, stagger: 0.12, duration: 0.8, ease: 'back.out(2)' }, '-=0.4')
      .from($('.lad-range', lad), { scaleX: 0, duration: 1, ease: 'expo.out' }, '-=0.3')
      .from($('.lad-range .lb', lad), { y: 20, opacity: 0, duration: 0.6 }, '-=0.5');
  }
  // flow + legend reveal handled by .rv; donuts
  $$('.donut-svg').forEach(buildDonut);
  // config mix bars
  const mb = $('#mixbars');
  if (mb) gsap.from($$('.mb-bar i', mb), { scaleX: 0, duration: 1.2, ease: 'expo.out', stagger: 0.1, scrollTrigger: { trigger: mb, start: 'top 80%' } });
  // budget bars
  $$('.bars').forEach(b => ScrollTrigger.create({ trigger: b, start: 'top 85%', once: true, onEnter: () => animBars(b) }));
  // launch window line
  const launch = $('#launch');
  if (launch) {
    const steps = $$('.lstep', launch);
    gsap.to($('.lline', launch), { scaleX: 1, ease: 'none', scrollTrigger: { trigger: launch, start: 'top 75%', end: 'bottom 45%', scrub: true, onUpdate: s => steps.forEach((st, i) => st.classList.toggle('on', s.progress >= i / (steps.length - 1) - 0.02)) } });
    gsap.from(steps, { y: 40, opacity: 0, stagger: 0.08, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: launch, start: 'top 85%' } });
  }
  // gantt bars grow
  const gw = $('.gwrap');
  if (gw) ScrollTrigger.create({ trigger: gw, start: 'top 80%', once: true, onEnter: () => {
    $$('#ganttBody tr', gw).forEach((tr, r) => gsap.from($$('td.g>i', tr), { scaleX: 0, duration: 0.7, ease: 'expo.out', stagger: 0.04, delay: r * 0.025 }));
    gsap.from($$('#ganttBody td.ms', gw), { scale: 0, opacity: 0, duration: 0.6, ease: 'back.out(3)', stagger: 0.08, delay: 0.4 });
  } });
  // week timeline
  const tl2 = $('#tl2');
  if (tl2) {
    gsap.to($('.tlfill', tl2), { scaleY: 1, ease: 'none', scrollTrigger: { trigger: tl2, start: 'top 60%', end: 'bottom 60%', scrub: true } });
    $$('.tl2-wk', tl2).forEach(w => gsap.from($('.card', w), { x: w.classList.contains('l') && !isMobile() ? -80 : 80, opacity: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: w, start: 'top 88%' } }));
    $$('.tl2-ph', tl2).forEach(ph => gsap.from(ph, { scale: 0.6, opacity: 0, duration: 0.8, ease: 'back.out(2)', scrollTrigger: { trigger: ph, start: 'top 88%' } }));
  }
  // rhythm bars
  const rb = $('#rhythmBars');
  if (rb) gsap.from($$('.rb', rb), { scaleY: 0, duration: 0.9, ease: 'expo.out', stagger: 0.012, scrollTrigger: { trigger: rb, start: 'top 80%' } });
  // strike-throughs
  const dont = $('#dont');
  if (dont) gsap.to($$('.strike', dont), { scaleX: 1, duration: 0.9, ease: 'expo.inOut', stagger: 0.18, scrollTrigger: { trigger: dont, start: 'top 70%' } });
  // footer wordmark rise (More)
  const wm = $('.wordmark');
  if (wm) gsap.from($$('span', wm), { yPercent: 105, ease: 'none', stagger: 0.04, scrollTrigger: { trigger: 'footer', start: 'top bottom', end: 'bottom bottom', scrub: 0.5 } });
  // ch-head bignum slide
  $$('.ch-head .bignum').forEach(n => gsap.fromTo(n, { xPercent: 30, opacity: 0 }, { xPercent: 0, opacity: 1, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: n, start: 'top 90%' } }));
  // cards with hover tilt
  $$('.anchor,.win,.spec').forEach(c => tilt(c, 4));

  // scene copy choreography (scrubbed by each pinned scene)
  sceneCopy();
}

function sceneCopy() {
  // hero copy exits
  gsap.timeline({ scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom bottom', scrub: 0.4 } })
    .to('#hero .hero-copy > div:first-child > *', { y: -80, opacity: 0, stagger: 0.04, duration: 0.3, ease: 'power2.in' }, 0.5)
    .to('#hero .hero-side, #hero .draghint', { opacity: 0, duration: 0.2 }, 0.4)
    .to({}, { duration: 0.2 }, 0.8);
  // spin pops
  const sp = $('#spin');
  if (sp) {
    const tl = gsap.timeline({ scrollTrigger: { trigger: sp, start: 'top top', end: 'bottom bottom', scrub: 0.4 } });
    $$('.spin-pop', sp).forEach((el, i) => {
      const from = el.classList.contains('l') ? -120 : 120, a = [0.1, 0.32, 0.54, 0.76][i];
      tl.fromTo(el, { x: from, yPercent: -40, opacity: 0, rotate: from > 0 ? 6 : -6 }, { x: 0, yPercent: -50, opacity: 1, rotate: 0, duration: 0.07, ease: 'power3.out' }, a)
        .fromTo($$('.sp-big, h3, p', el), { y: 40, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.012, duration: 0.05 }, a + 0.03)
        .to(el, { x: from * 0.6, opacity: 0, duration: 0.05, ease: 'power2.in' }, a + 0.17);
    });
    tl.fromTo('.spin-idx', { opacity: 0 }, { opacity: 1, duration: 0.04 }, 0.04).to('.spin-idx', { opacity: 0, duration: 0.04 }, 0.92).to({}, { duration: 0.04 }, 0.96);
  }
  // unbox
  const u = $('#unbox');
  const steps = $$('.u-steps i b', u);
  gsap.timeline({ scrollTrigger: { trigger: u, start: 'top top', end: 'bottom bottom', scrub: 0.4 } })
    .fromTo($$('.u-copy > *', u), { y: 70, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.03, duration: 0.14 }, 0.5)
    .fromTo($('.u-steps', u), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 0.12)
    .fromTo(steps[0], { scaleX: 0 }, { scaleX: 1, duration: 0.34, ease: 'none' }, 0.16)
    .fromTo(steps[1], { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: 'none' }, 0.55)
    .fromTo(steps[2], { scaleX: 0 }, { scaleX: 1, duration: 0.12, ease: 'none' }, 0.86)
    .to($$('.u-copy > *', u), { y: -50, opacity: 0, stagger: 0.02, duration: 0.08 }, 0.88)
    .to($('.u-steps', u), { opacity: 0, duration: 0.05 }, 0.95);
  // drive intros
  $$('.intro').forEach(sec => {
    const copy = $$('.scene-copy > *', sec), lis = $$('.ch-list li', sec), nums = $$('.keynums > div', sec);
    gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: 0.4 } })
      .set(sec.querySelector('.scene-copy'), { opacity: 1 }, 0)
      .fromTo(copy, { y: 80, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.025, duration: 0.12 }, 0.24)
      .fromTo(lis, { x: -40, opacity: 0 }, { x: 0, opacity: 1, stagger: 0.03, duration: 0.1 }, 0.34)
      .fromTo(nums, { y: 40, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.03, duration: 0.1 }, 0.42)
      .fromTo($('.gohint', sec), { opacity: 0 }, { opacity: 1, duration: 0.05 }, 0.6)
      .to([...copy, $('.gohint', sec)], { y: -60, opacity: 0, stagger: 0.015, duration: 0.08 }, 0.74)
      .to({}, { duration: 0.18 }, 0.82);
  });
  // outro
  gsap.timeline({ scrollTrigger: { trigger: '#outro', start: 'top top', end: 'bottom bottom', scrub: 0.4 } })
    .fromTo('#outro .closing', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2 }, 0.5)
    .to('#outro .closing', { y: -40, opacity: 0, duration: 0.1 }, 0.9);
}

function tilt(el, deg) {
  if (matchMedia('(hover: none)').matches || reduced) return;
  el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; gsap.to(el, { rotateY: x * deg, rotateX: -y * deg, transformPerspective: 900, duration: 0.6, ease: 'power3.out' }); });
  el.addEventListener('pointerleave', () => gsap.to(el, { rotateY: 0, rotateX: 0, duration: 1, ease: 'elastic.out(1,.5)' }));
}

function buildDonut(d) {
  const svg = $('svg', d), segs = d.dataset.seg.split(',').map(s => { const [v, c] = s.split(':'); return { v: +v, c }; });
  const R = 80, C = 2 * Math.PI * R; let acc = 0; const els = [];
  segs.forEach(s => {
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', 100); c.setAttribute('cy', 100); c.setAttribute('r', R); c.setAttribute('stroke', s.c);
    const len = C * s.v / 100;
    c.setAttribute('stroke-dasharray', `${Math.max(0, len - 1.5)} ${C}`);
    c.style.strokeDashoffset = -C * acc / 100;
    c.dataset.len = len; c.dataset.off = -C * acc / 100; acc += s.v;
    svg.appendChild(c); els.push(c);
  });
  els.forEach(c => c.setAttribute('stroke-dasharray', `0 ${C}`));
  ScrollTrigger.create({ trigger: d, start: 'top 80%', once: true, onEnter: () => {
    els.forEach((c, i) => { const o = { l: 0 }; gsap.to(o, { l: +c.dataset.len, duration: 1.2, delay: i * 0.12, ease: 'expo.out', onUpdate: () => c.setAttribute('stroke-dasharray', `${Math.max(0, o.l - 1.5)} ${C}`) }); });
    gsap.from($('.dc', d), { scale: 0.6, opacity: 0, duration: 1, ease: 'back.out(2)' });
  } });
}
function animBars(b) { gsap.fromTo($$('.bt i', b), { scaleX: 0 }, { scaleX: 1, duration: 1.3, ease: 'expo.out', stagger: 0.08 }); }

/* ------------------------------------------------------------------ */
/* data widgets (gantt, rhythm, budget toggle, waterfall, strip)       */
/* ------------------------------------------------------------------ */
const GANTT_N = 25;
const span = (a, b, cls) => Object.fromEntries(Array.from({ length: b - a + 1 }, (_, i) => [a + i, cls]));
const gcat = t => ({ cat: t }), grow = (name, cells) => ({ name, cells });
const GANTT_ROWS = [
  gcat('关键节点'), grow('预热正式开始（2026.12.07）', { 4: 'ms' }), grow('众筹正式上线（2027.01.21）', { 10: 'ms' }), grow('60 天档期结束（2027.03.22）', { 19: 'ms' }), grow('90 天档期结束（2027.04.21）', { 23: 'ms' }), grow('发货期启动（2027 年 4 月第 4 周）', { 24: 'ms' }),
  gcat('必备前置 · 品牌方'), grow('产品素材与本地化授权提供', span(0, 1, 'on')), grow('评测样机备货（7 / 10 台）', span(1, 3, 'on')),
  gcat('筹备期 · 4 周'), grow('策略、时间表与卖点对齐', { 0: 'on' }), grow('三款配置 Reward 结构确认', { 1: 'on' }), grow('实机演示与页面主视觉', span(1, 2, 'on')), grow('5 组 1:1 广告素材方向', { 2: 'on' }), grow('预热页与平台预约路径', span(2, 3, 'on')), grow('邮件序列与转化追踪校验', { 3: 'on' }), grow('KOL 名单确认与档期锁定', span(1, 3, 'on')),
  gcat('预热期 · 45 天'), grow('预热广告启动与 CPL 校准', { 4: 'pre' }), grow('素材 A/B 轮换与扩量', span(5, 7, 'pre')), grow('平台预约与 LINE 内容运营', span(4, 9, 'pre')), grow('评测样机寄送至 KOL', span(5, 6, 'pre')), grow('KOL 提纲与预热内容', span(7, 8, 'pre')), grow('PR TIMES 通稿排期', span(7, 8, 'pre')), grow('众筹页面制作与优化', span(4, 8, 'pre')), grow('上线前邮件（一周 / 48h / 24h）', span(9, 10, 'pre')), grow('页面与 Reward 最终确认', { 9: 'pre' }),
  gcat('众筹期 · 60 / 90 天'), grow('KOL 评测解禁与分批释放', Object.assign(span(10, 13, 'camp'), span(14, 15, 'ext'))), grow('上线期广告投放与再营销', Object.assign(span(10, 19, 'camp'), span(20, 23, 'ext'))), grow('项目上线与首 72h 冲刺', { 10: 'camp' }), grow('首日流量与转化分析', { 10: 'camp' }), grow('每周复盘与预算再分配', Object.assign(span(10, 19, 'camp'), span(20, 23, 'ext'))), grow('PR TIMES 通稿与线下展示', Object.assign(span(10, 12, 'camp'), span(20, 21, 'ext'))), grow('早鸟同价加开', Object.assign({ 14: 'camp' }, { 21: 'ext' })), grow('结束前邮件与 LINE 冲刺', Object.assign({ 19: 'camp' }, { 23: 'ext' })), grow('项目结束与 Update 发布', Object.assign({ 19: 'camp' }, { 23: 'ext' })),
  gcat('发货期'), grow('订单整理与地址收集', { 24: 'ship' }), grow('发货通知与生产排期确认', { 24: 'ship' })
];
const GANTT_STATE = { on: '筹备期', pre: '预热期', camp: '60 天主档', ext: '90 天延伸', ship: '发货期' };
function renderGantt() {
  const body = $('#ganttBody'); if (!body) return;
  body.innerHTML = GANTT_ROWS.map(r => {
    if (r.cat) return `<tr class="catrow"><th scope="rowgroup" colspan="${GANTT_N + 1}">${r.cat}</th></tr>`;
    const cells = Array.from({ length: GANTT_N }, (_, i) => { const c = r.cells[i]; return c === 'ms' ? '<td class="g ms"><span class="visually-hidden">关键节点</span>◆</td>' : c ? `<td class="g ${c}"><i></i><span class="visually-hidden">${GANTT_STATE[c]}</span></td>` : '<td class="g"></td>'; }).join('');
    return `<tr><th scope="row" class="tk">${r.name}</th>${cells}</tr>`;
  }).join('');
}
const RHYTHM_MID = Array.from({ length: 54 }, (_, i) => .65 + .25 * (.5 + .5 * Math.sin(i / 3)) + .12 * Math.sin(i / 1.7));
const RHYTHM_MID_SUM = RHYTHM_MID.reduce((a, b) => a + b, 0);
const RHYTHM = [22, 8, 5, ...RHYTHM_MID.map(x => x * 45 / RHYTHM_MID_SUM), 6, 6, 8].map(x => x / 22 * 100);
function renderRhythm() { const el = $('#rhythmBars'); if (el) el.innerHTML = RHYTHM.map(h => `<i class="rb" style="height:${h}%"></i>`).join(''); }

function initBudget() {
  const L = $('#budgetL'), R = $('#budgetR'), btns = $$('#n-budget button');
  btns.forEach(b => b.addEventListener('click', () => {
    const key = b.dataset.bud;
    btns.forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
    const show = key === 'L' ? L : R, hide = key === 'L' ? R : L;
    if (!hide.hidden) gsap.to(hide, { opacity: 0, y: -20, duration: 0.3, onComplete: () => { hide.hidden = true; show.hidden = false; gsap.fromTo(show, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: 'expo.out' }); animBars(show); gsap.from($$('.kpi', show), { y: 30, opacity: 0, stagger: 0.06, duration: 0.7, ease: 'expo.out' }); ScrollTrigger.refresh(); measure(); } });
  }));
}

const WF = {
  L: [3333.33, 303.03, 733.33, 543.67, 500, 1253.30],
  R: [3333.33, 303.03, 733.33, 611.33, 500, 1185.64],
};
function initWaterfall() {
  const chart = $('#wfChart'); if (!chart) return;
  const kinds = ['start', 'minus', 'minus', 'minus', 'minus', 'end'];
  chart.innerHTML = kinds.map(k => `<div class="wf-col ${k}"><div class="wf-bar"></div><div class="wf-val"></div></div>`).join('');
  const cols = $$('.wf-col', chart), max = 3333.33;
  const state = WF.L.map(v => ({ v: 0 }));
  function layout(vals) {
    let run = vals[0];
    cols.forEach((c, i) => {
      let bottom, h;
      if (i === 0) { bottom = 0; h = vals[0]; }
      else if (i === 5) { bottom = 0; h = vals[5]; }
      else { run -= vals[i]; bottom = run; h = vals[i]; }
      const bar = $('.wf-bar', c), val = $('.wf-val', c);
      bar.style.bottom = bottom / max * 100 + '%'; bar.style.height = h / max * 100 + '%';
      val.style.bottom = (bottom + h) / max * 100 + '%';
      val.textContent = (i > 0 && i < 5 ? '− $' : '$') + h.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    });
  }
  function to(key, dur = 1.2) {
    const target = WF[key];
    state.forEach((s, i) => gsap.to(s, { v: target[i], duration: dur, delay: i * 0.12, ease: 'expo.out', onUpdate: () => layout(state.map(x => x.v)) }));
  }
  let cur = 'L';
  layout(state.map(x => x.v));
  ScrollTrigger.create({ trigger: chart, start: 'top 80%', once: true, onEnter: () => to(cur) });
  $$('#wf [data-wf]').forEach(b => b.addEventListener('click', () => {
    cur = b.dataset.wf;
    $$('#wf [data-wf]').forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
    to(cur, 0.9);
  }));
}

function initStrip() {
  const strip = $('#adStrip'); if (!strip) return;
  const track = $('.strip-track', strip), tiles = $$('.adtile', strip);
  let x = 0, tx = 0, dragging = false, sx = 0, startX = 0, v = 0, lastX = 0;
  const bounds = () => { const w = track.scrollWidth, pad = parseFloat(getComputedStyle(track).paddingLeft); return { min: -(w - pad * 2 - tiles[0].offsetWidth), max: 0 }; };
  strip.addEventListener('pointerdown', e => { dragging = true; sx = e.clientX; startX = tx; lastX = e.clientX; strip.setPointerCapture(e.pointerId); });
  strip.addEventListener('pointermove', e => { if (!dragging) return; tx = startX + (e.clientX - sx) * 1.2; v = e.clientX - lastX; lastX = e.clientX; });
  const end = () => { if (!dragging) return; dragging = false; tx += v * 12; snap(); };
  strip.addEventListener('pointerup', end); strip.addEventListener('pointercancel', end);
  function snap() {
    const b = bounds(); tx = clamp(tx, b.min, b.max);
    const step = tiles[0].offsetWidth + 22; tx = Math.round(tx / step) * step; tx = clamp(tx, b.min, b.max);
  }
  // start on the middle tile
  requestAnimationFrame(() => { const step = tiles[0].offsetWidth + 22; tx = x = -step * 2; });
  gsap.ticker.add(() => {
    x += (tx - x) * 0.09;
    track.style.transform = `translate3d(${x}px,0,0)`;
    const cx = innerWidth / 2;
    tiles.forEach(t => { const r = t.getBoundingClientRect(); const d = (r.left + r.width / 2 - cx) / innerWidth; const a = Math.min(1, Math.abs(d) * 2); t.style.transform = `scale(${1.12 - a * 0.28}) rotate(${d * 8}deg)`; t.style.zIndex = Math.round(10 - a * 10); t.style.opacity = 1 - a * 0.35; });
  });
}

/* ------------------------------------------------------------------ */
/* boot                                                                */
/* ------------------------------------------------------------------ */
renderGantt(); renderRhythm(); initBudget(); initWaterfall(); initStrip();

function heroIn() {
  const h1 = $('#hero h1');
  const split = new SplitText(h1, { type: 'lines,chars', linesClass: 'sl-line', mask: 'lines' });
  const tl = gsap.timeline();
  tl.from(split.chars, { yPercent: 120, rotate: 8, duration: 1.4, ease: 'expo.out', stagger: 0.03 })
    .from('.h-in', { y: 40, opacity: 0, duration: 1.2, ease: 'expo.out', stagger: 0.07 }, 0.25)
    .from('#hdr > *', { y: -30, opacity: 0, duration: 1, ease: 'expo.out', stagger: 0.08 }, 0.3)
    .from('.draghint', { opacity: 0, x: 30, duration: 1 }, 0.9);
  // model rises in
  const o = { v: 0 }; introLift = o;
  gsap.to(o, { v: 1, duration: 2.2, ease: 'expo.out' });
}
let introLift = { v: 1 };

// loader
let loaderDone = false;
const minTime = new Promise(r => setTimeout(r, reduced ? 0 : 1400));
(function tickLoader() {
  if (loaderDone) return;
  shownP += (Math.max(loadP, shownP) - shownP) * 0.12 + 0.002;
  shownP = Math.min(shownP, modelReady ? 1 : 0.96);
  loaderNum.textContent = String(Math.floor(shownP * 100)).padStart(3, '0');
  loaderBar.style.width = shownP * 100 + '%';
  requestAnimationFrame(tickLoader);
})();

Promise.all([stage.ready, minTime, document.fonts.ready]).then(() => {
  modelReady = true;
  measure();
  initScrollMotion();
  ScrollTrigger.refresh();
  requestAnimationFrame(frame);
  gsap.to({}, { duration: 0.5, onComplete: finishLoader });
}).catch(err => {
  console.error(err);
  modelReady = false;
  measure(); initScrollMotion(); requestAnimationFrame(frame);
  $('#loader .lt span:last-child').textContent = '3D 模型需通过本地服务或线上地址打开';
  setTimeout(finishLoader, 1200);
});
function finishLoader() {
  loaderDone = true;
  loaderNum.textContent = '100'; loaderBar.style.width = '100%';
  gsap.to('#loader', { clipPath: 'inset(0 0 100% 0)', duration: 1.1, ease: 'expo.inOut', delay: 0.15, onComplete: () => { $('#loader').remove(); } });
  document.documentElement.classList.remove('loading');
  lenis?.start();
  setTimeout(heroIn, 350);
}

// model intro lift: apply as an offset on vertical screen shift
const _apply = stage.apply;
stage.apply = (St, time) => { St.sy -= (1 - introLift.v) * 0.25; St.az -= (1 - introLift.v) * 1.2; _apply(St, time); };

/* ------------------------------------------------------------------ */
/* presenter sync: a separate notes window follows / drives this page   */
/* ------------------------------------------------------------------ */
const pres = 'BroadcastChannel' in window ? new BroadcastChannel('lucy-presenter') : null;
const noteEls = NOTES.map(n => n.sel.startsWith('stmt:') ? $$('[data-stmt]')[+n.sel.slice(5)] : $(n.sel));
let noteIdx = -1, noteHold = 0;
function currentNote() {
  const line = innerHeight * 0.55; let k = 0;
  noteEls.forEach((el, i) => { if (el && el.getBoundingClientRect().top <= line) k = i; });
  return k;
}
function gotoNote(i) {
  const el = noteEls[i]; if (!el) return;
  const sc = scenes.find(x => x.el === el);
  if (sc) {
    const f = { hero: 0, spin: 0.14, unbox: 0.62, drive: 0.64, outro: 0.72 }[sc.type] ?? 0;
    return scrollToY(sc.start + (sc.end - sc.start) * f, document.hidden);
  }
  scrollToY(el.getBoundingClientRect().top + scrollY() - innerHeight * 0.12, document.hidden);
}
if (pres) {
  pres.onmessage = e => {
    const m = e.data || {};
    if (m.type === 'hello') pres.postMessage({ type: 'pos', idx: currentNote() });
    if (m.type === 'goto') { closeMenu(); noteIdx = m.idx; noteHold = Date.now() + 2600; gotoNote(m.idx); }
  };
  setInterval(() => { if (Date.now() > noteHold) noteIdx = currentNote(); pres.postMessage({ type: 'pos', idx: noteIdx }); }, 400);
}
function openPresenter() { window.open('presenter.html', 'lucy-presenter', 'width=980,height=900'); }
addEventListener('keydown', e => { if ((e.key === 'p' || e.key === 'P') && !/input|textarea/i.test(e.target.tagName)) { e.preventDefault(); openPresenter(); } });

window.__app = { stage, get lenis(){return lenis}, get scenes(){return scenes}, goTo, get S(){return S} };
let rT;
addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(() => { stage.resize(); ScrollTrigger.refresh(); measure(); }, 120); });
ScrollTrigger.addEventListener('refresh', measure);
addEventListener('load', () => { ScrollTrigger.refresh(); measure(); });
