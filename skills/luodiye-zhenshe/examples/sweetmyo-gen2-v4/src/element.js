import { buildPartHTML } from './template.js';

/**
 * <sweetmyo-gen2-landing> — v4 "Signal" redesign.
 * Own scroll engine (rect-based progress + per-scene smoothing) driving sticky scenes,
 * so nothing is re-parented and the Wix native forms stay locked to their slots.
 * Lenis smooth scroll off-Wix. GSAP only for small tweens (counter pop).
 */
var LAUNCH_AT = '2026-12-08T09:00:00-05:00';
var MIN_CLIP_SECONDS = 4.5;

function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
function lerp(a, b, t) { return a + (b - a) * t; }
function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
function easeInOut(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
function smooth(t) { return t * t * (3 - 2 * t); }

export class SweetmyoLanding extends HTMLElement {
  constructor() {
    super();
    this._mounted = false;
    this._cleanups = [];
    this._observers = [];
    this._timers = [];
    this._intervals = [];
    this._scenes = [];
    this._drawers = [];
    this._raf = 0;
    this._lenis = null;
    this._lenisTicker = null;
    this._mouse = { x: -1, y: -1, nx: .5, ny: .5 };
    this._lastScrollY = 0;
    this._velocity = 0;
    this._reduced = false;
  }

  connectedCallback() {
    if (this._mounted) return;
    this._mounted = true;
    var A = window.__SW_ASSET_FN || function (p) { return 'assets/' + p; };
    var part = this.getAttribute('part') || 'all';
    this.classList.add('sw-white-root', 'sw-js');
    this.setAttribute('data-part', part);
    this.innerHTML = buildPartHTML(part, A);
    this._reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

    this._injectStylesOnce();
    this._setupBreakoutAndFormSync();
    this._setupSmoothScroll();
    this._setupPointer();
    this._setupVideosAndCounters();
    this._setupNav();
    this._sceneHero();
    this._sceneCouch();
    this._sceneWave();
    this._sceneZones();
    this._sceneMotion();
    this._sceneMid();
    this._sceneScan();
    this._sceneApp();
    this._sceneEasy();
    this._sceneMarquee();
    this._sceneFinal();
    this._setupCountdown();
    this._startLoop();

    var self = this;
    [60, 300, 900, 2000, 4000].forEach(function (ms) {
      self._timers.push(setTimeout(function () { if (self._mounted) self.syncWixForms(); }, ms));
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { if (self._mounted) self.syncWixForms(); });
    }
  }

  disconnectedCallback() {
    this._mounted = false;
    cancelAnimationFrame(this._raf);
    this._cleanups.forEach(function (fn) { try { fn(); } catch (_) {} });
    this._observers.forEach(function (o) { try { o.disconnect(); } catch (_) {} });
    this._timers.forEach(clearTimeout);
    this._intervals.forEach(clearInterval);
    this._cleanups = []; this._observers = []; this._timers = []; this._intervals = [];
    this._scenes = []; this._drawers = [];
    if (this._lenisTicker && window.gsap) { try { window.gsap.ticker.remove(this._lenisTicker); } catch (_) {} }
    if (this._lenis) { try { this._lenis.destroy(); } catch (_) {} if (window.__swLenis === this._lenis) window.__swLenis = null; }
    this._lenis = null; this._lenisTicker = null;
  }

  /* ───────────────────────── infrastructure ───────────────────────── */

  _on(target, type, fn, opts) {
    target.addEventListener(type, fn, opts || { passive: true });
    this._cleanups.push(function () { target.removeEventListener(type, fn, opts || { passive: true }); });
  }

  _injectStylesOnce() {
    if (!document.getElementById('sw-gen2-fonts')) {
      var pre = document.createElement('link');
      pre.rel = 'preconnect'; pre.href = 'https://fonts.gstatic.com'; pre.crossOrigin = 'anonymous';
      document.head.appendChild(pre);
      var link = document.createElement('link');
      link.id = 'sw-gen2-fonts';
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap';
      document.head.appendChild(link);
    }
    var existing = document.getElementById('sw-gen2-styles');
    if (existing) {
      if (window.__SW_CSS_TEXT && existing.textContent !== window.__SW_CSS_TEXT) existing.textContent = window.__SW_CSS_TEXT;
      return;
    }
    if (!window.__SW_CSS_TEXT) return;
    var s = document.createElement('style');
    s.id = 'sw-gen2-styles';
    s.textContent = window.__SW_CSS_TEXT;
    document.head.appendChild(s);
  }

  _setupBreakoutAndFormSync() {
    var self = this;
    var update = function () {
      if (!self._mounted) return;
      var vw = document.documentElement.clientWidth || window.innerWidth;
      self.style.setProperty('--sw-vw', vw + 'px');
      self.style.setProperty('--sw-breakout-left', '0px');
      var r = self.getBoundingClientRect();
      self.style.setProperty('--sw-breakout-left', (-r.left) + 'px');
      self._vh = window.innerHeight;
      self.syncWixForms();
    };
    update();
    this._on(window, 'resize', update);
    if (typeof ResizeObserver !== 'undefined') {
      var t = 0;
      var ro = new ResizeObserver(function () {
        clearTimeout(t);
        t = setTimeout(update, 80);
      });
      ro.observe(this);
      this._observers.push(ro);
    }
  }

  /** Moves each external Wix native form onto its placeholder (no data handling of our own). */
  syncWixForms() {
    if (!this._mounted) return;
    var slots = Array.prototype.slice.call(this.querySelectorAll('.wix-form-placeholder'));
    if (!slots.length) return;
    var all = Array.prototype.filter.call(document.querySelectorAll('form'), function (f) { return !f.closest('.sw-white-root'); });
    if (!all.length) return;
    var host = this;
    var pairs = [];
    slots.forEach(function (slot, localIdx) {
      var gi = parseInt(slot.getAttribute('data-wix-slot'), 10);
      if (isNaN(gi)) gi = localIdx;
      var sec = host.closest('section');
      var secForms = sec ? Array.prototype.filter.call(sec.querySelectorAll('form'), function (f) { return !f.closest('.sw-white-root'); }) : [];
      var form = secForms.length === 1 ? secForms[0] : (secForms[localIdx] || all[gi]);
      if (!form) return;
      var branch = host;
      while (branch.parentElement && !branch.parentElement.contains(form)) branch = branch.parentElement;
      var grid = branch.parentElement || document.body;
      var mv = form;
      while (mv.parentElement && mv.parentElement !== grid) mv = mv.parentElement;
      mv.style.transition = 'none';
      mv.style.transform = 'translate3d(0px, 0px, 0px)';
      mv.style.width = ''; mv.style.maxWidth = '';
      mv.style.zIndex = '35';
      mv.style.pointerEvents = 'auto';
      var sr = slot.getBoundingClientRect();
      if (sr.width > 160) { mv.style.width = Math.round(sr.width) + 'px'; mv.style.maxWidth = Math.round(sr.width) + 'px'; }
      var fr = mv.getBoundingClientRect();
      if (fr.height > 44) slot.style.minHeight = Math.ceil(fr.height) + 'px';
      pairs.push({ slot: slot, mv: mv, gi: gi });
    });
    pairs.forEach(function (it) {
      var s = it.slot.getBoundingClientRect();
      var f = it.mv.getBoundingClientRect();
      var dx = Number((s.left - f.left).toFixed(2));
      var dy = Number((s.top - f.top).toFixed(2));
      it.mv.style.transform = 'translate3d(' + dx + 'px, ' + dy + 'px, 0px)';
      it.slot.setAttribute('data-synced', 'true');
      host._magnetic(it.mv);
    });
  }

  _magnetic(mv) {
    var btn = mv.querySelector('button, [type="submit"], [role="button"]');
    if (!btn || btn.dataset.swMagnetic) return;
    btn.dataset.swMagnetic = '1';
    btn.style.transition = 'transform 260ms cubic-bezier(.22,1,.36,1)';
    var move = function (e) {
      var r = btn.getBoundingClientRect();
      var x = clamp((e.clientX - (r.left + r.width / 2)) * .22, -9, 9);
      var y = clamp((e.clientY - (r.top + r.height / 2)) * .28, -6, 6);
      btn.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
    };
    var leave = function () { btn.style.transform = 'translate3d(0,0,0)'; };
    this._on(btn, 'mousemove', move);
    this._on(btn, 'mouseleave', leave);
  }

  _setupSmoothScroll() {
    var isWix = Boolean(window.wixBiSession || document.getElementById('SITE_CONTAINER'));
    if (isWix || this._reduced || !window.Lenis || this.hasAttribute('data-no-lenis') || window.__swLenis) return;
    try {
      var lenis = new window.Lenis({ lerp: .1, smoothWheel: true });
      this._lenis = lenis;
      window.__swLenis = lenis;
      if (window.gsap) {
        var tick = function (t) { lenis.raf(t * 1000); };
        window.gsap.ticker.add(tick);
        window.gsap.ticker.lagSmoothing(0);
        this._lenisTicker = tick;
      } else {
        var self = this;
        var loop = function (t) { if (!self._mounted) return; lenis.raf(t); requestAnimationFrame(loop); };
        requestAnimationFrame(loop);
      }
      this._on(this, 'click', function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (!a) return;
        var el = document.getElementById(a.getAttribute('href').slice(1));
        if (el) { e.preventDefault(); lenis.scrollTo(el, { duration: 1.6 }); }
      }, { passive: false });
    } catch (_) {}
  }

  _setupPointer() {
    var m = this._mouse;
    this._on(window, 'pointermove', function (e) {
      m.x = e.clientX; m.y = e.clientY;
      m.nx = e.clientX / window.innerWidth; m.ny = e.clientY / window.innerHeight;
    });
  }

  /** scene: { el, sticky:bool, update(p), cur, alwaysSmooth } */
  _addScene(el, update, opts) {
    if (!el) return;
    opts = opts || {};
    this._scenes.push({ el: el, update: update, sticky: opts.sticky !== false, cur: -1, k: opts.k || .14 });
  }

  _startLoop() {
    var self = this;
    var last = performance.now();
    var frame = function (now) {
      if (!self._mounted) return;
      var dt = Math.min(64, now - last) / 1000; last = now;
      var vh = window.innerHeight;
      var sy = window.scrollY || window.pageYOffset || 0;
      self._velocity = lerp(self._velocity, (sy - self._lastScrollY) / Math.max(dt, .001), .12);
      self._lastScrollY = sy;
      for (var i = 0; i < self._scenes.length; i++) {
        var sc = self._scenes[i];
        var r = sc.el.getBoundingClientRect();
        if (r.bottom < -vh * .5 || r.top > vh * 1.5) {
          if (sc.cur !== -1 && sc.cur > 0 && sc.cur < 1) { /* settle to edge */ sc.cur = r.top > 0 ? 0 : 1; sc.update(sc.cur, r, vh); }
          continue;
        }
        var target = sc.sticky
          ? clamp(-r.top / Math.max(1, r.height - vh), 0, 1)
          : clamp((vh - r.top) / vh, 0, 1.6);
        if (sc.cur === -1 || self._reduced) sc.cur = target;
        else sc.cur += (target - sc.cur) * sc.k;
        if (Math.abs(target - sc.cur) < .0004) sc.cur = target;
        sc.update(sc.cur, r, vh);
      }
      for (var j = 0; j < self._drawers.length; j++) self._drawers[j](now / 1000, dt);
      self._raf = requestAnimationFrame(frame);
    };
    this._raf = requestAnimationFrame(frame);
  }

  _visibleFlag(el, margin) {
    var flag = { on: false };
    if (!el || !('IntersectionObserver' in window)) { flag.on = true; return flag; }
    var io = new IntersectionObserver(function (es) { flag.on = es[0].isIntersecting; }, { rootMargin: margin || '0px' });
    io.observe(el);
    this._observers.push(io);
    return flag;
  }

  _setupVideosAndCounters() {
    var self = this;
    if (!('IntersectionObserver' in window)) return;
    var vids = Array.prototype.slice.call(this.querySelectorAll('video.sw-auto-vid, video.sw-cap-vid'));
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) { v.muted = true; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else { try { v.pause(); } catch (_) {} }
      });
    }, { threshold: .02 });
    vids.forEach(function (v) { vio.observe(v); });
    this._observers.push(vio);

    var counters = Array.prototype.slice.call(this.querySelectorAll('[data-count]'));
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) self._count(e.target); });
    }, { threshold: .4 });
    counters.forEach(function (c) { cio.observe(c); });
    this._observers.push(cio);
  }

  _count(el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    var host = el.closest('b') || el;
    if (this._reduced || !window.gsap) { el.textContent = String(target); return; }
    var gsap = window.gsap, o = { v: 0 };
    gsap.killTweensOf(o);
    gsap.to(o, {
      v: target, duration: target > 50 ? 1.1 : .8, ease: 'power3.out',
      onUpdate: function () { el.textContent = String(Math.round(o.v)); },
      onComplete: function () {
        el.textContent = String(target);
        gsap.fromTo(host, { scale: 1 }, { scale: 1.08, duration: .14, yoyo: true, repeat: 1, ease: 'power2.out', transformOrigin: '0% 80%' });
      }
    });
  }

  /* ───────────────────────── nav ───────────────────────── */

  _setupNav() {
    var nav = this.querySelector('[data-nav]');
    if (!nav) return;
    var bar = nav.querySelector('[data-nav-bar]');
    var themed = Array.prototype.slice.call(this.querySelectorAll('[data-theme]'));
    var self = this;
    var lastTheme = '';
    this._drawers.push(function () {
      var root = self.getBoundingClientRect();
      var vh = window.innerHeight;
      var prog = clamp(-root.top / Math.max(1, root.height - vh), 0, 1);
      if (bar) bar.style.transform = 'scaleX(' + prog.toFixed(4) + ')';
      nav.classList.toggle('is-solid', root.top < -80);
      var theme = 'light';
      for (var i = themed.length - 1; i >= 0; i--) {
        var r = themed[i].getBoundingClientRect();
        if (r.top <= 34 && r.bottom > 34) { theme = themed[i].getAttribute('data-theme'); break; }
      }
      if (theme !== lastTheme) {
        lastTheme = theme;
        nav.classList.toggle('is-dark', theme === 'dark');
        nav.classList.toggle('is-volt', theme === 'volt');
      }
    });
  }

  /* ───────────────────────── scenes ───────────────────────── */

  _sceneHero() {
    var sec = this.querySelector('#sw-hero');
    if (!sec) return;
    var sticky = sec.querySelector('.sw-hero-sticky');
    var cap = sec.querySelector('[data-capsule]');
    var scrim = sec.querySelector('[data-hero-scrim]');
    var slot = sec.querySelector('[data-cap-slot]');
    var echo = sec.querySelector('[data-hero-echo]');
    var glow = sec.querySelector('.sw-hero-glow');
    var m = this._mouse;
    var g = { x: window.innerWidth * .62, y: window.innerHeight * .55 };
    var full = 1;
    /* Full-screen real video first (product visible), then it shrinks into the capsule inside the headline. */
    this._addScene(sec, function (p) {
      var st = sticky.getBoundingClientRect();
      var s = slot.getBoundingClientRect();
      var f = 1 - easeInOut(seg(p, .36, .8));
      full = f;
      var top = lerp(s.top - st.top, 0, f);
      var left = lerp(s.left - st.left, 0, f);
      var right = lerp(st.right - s.right, 0, f);
      var bottom = lerp(st.bottom - s.bottom, 0, f);
      var rad = lerp(s.height / 2, 0, Math.pow(f, .7));
      cap.style.clipPath = 'inset(' + top.toFixed(1) + 'px ' + right.toFixed(1) + 'px ' + Math.max(0, bottom).toFixed(1) + 'px ' + left.toFixed(1) + 'px round ' + rad.toFixed(1) + 'px)';
      scrim.style.opacity = f.toFixed(3);
      echo.style.opacity = seg(p, .66, .86).toFixed(3);
    }, { k: .18 });
    this._drawers.push(function () {
      if (!glow) return;
      var tx = m.x < 0 ? window.innerWidth * .62 : m.x;
      var ty = m.y < 0 ? window.innerHeight * .55 : m.y;
      g.x += (tx - g.x) * .06; g.y += (ty - g.y) * .06;
      glow.style.transform = 'translate3d(' + g.x.toFixed(1) + 'px,' + g.y.toFixed(1) + 'px,0) translate(-50%,-50%)';
      glow.style.opacity = (.55 * (1 - full)).toFixed(3);
    });
  }

  _sceneCouch() {
    var sec = this.querySelector('#sw-couch');
    if (!sec) return;
    var q = sec.querySelector('.sw-q');
    var ws = Array.prototype.slice.call(sec.querySelectorAll('.sw-w'));
    var media = sec.querySelector('[data-couch-media]');
    var vid = media.querySelector('video');
    var shade = sec.querySelector('.sw-couch-shade');
    var burn = sec.querySelector('[data-burn]');
    var num = sec.querySelector('[data-burn-count]');
    var numHost = sec.querySelector('.sw-burn-num');
    var popped = false, playing = false, lastLit = -1;
    vid.classList.remove('sw-auto-vid');
    this._addScene(sec, function (p, r, vh) {
      var lit = Math.round(seg(p, .02, .36) * ws.length);
      if (lit !== lastLit) {
        lastLit = lit;
        for (var i = 0; i < ws.length; i++) ws[i].classList.toggle('is-lit', i < lit);
      }
      var W = r.width, H = vh;
      var small = W < 760;
      var cw = W * (small ? .72 : .34), ch = small ? cw * .5 : W * .14;
      var a = easeOut(seg(p, .38, .47));
      var b = easeInOut(seg(p, .47, .63));
      var w = lerp(cw * a, W, b), h = lerp(ch * a, H, b);
      var ix = (W - w) / 2, iy = (H - h) / 2;
      var rad = lerp(ch * a / 2, 0, b);
      media.style.clipPath = 'inset(' + iy.toFixed(1) + 'px ' + ix.toFixed(1) + 'px ' + iy.toFixed(1) + 'px ' + ix.toFixed(1) + 'px round ' + rad.toFixed(1) + 'px)';
      var qOut = seg(p, .46, .58);
      q.style.opacity = (1 - qOut).toFixed(3);
      q.style.transform = 'scale(' + (1 - .08 * qOut).toFixed(4) + ')';
      shade.style.opacity = seg(p, .6, .7).toFixed(3);
      var bo = seg(p, .64, .72);
      burn.style.opacity = bo.toFixed(3);
      var c = seg(p, .64, .86);
      num.textContent = String(Math.round(500 * easeOut(c)));
      if (c >= 1 && !popped && window.gsap) {
        popped = true;
        window.gsap.fromTo(numHost, { scale: 1 }, { scale: 1.05, duration: .16, yoyo: true, repeat: 1, ease: 'power2.out', transformOrigin: '0% 100%' });
      }
      if (c < .9) popped = false;
      var shouldPlay = a > 0 && r.bottom > 0 && r.top < vh;
      if (shouldPlay && !playing) { playing = true; vid.muted = true; var pr = vid.play(); if (pr && pr.catch) pr.catch(function () {}); }
      else if (!shouldPlay && playing) { playing = false; try { vid.pause(); } catch (_) {} }
    });
  }

  _sceneWave() {
    var sec = this.querySelector('#sw-wave');
    if (!sec) return;
    var cv = sec.querySelector('[data-wave-canvas]');
    var ctx = cv.getContext('2d');
    var stA = sec.querySelector('[data-wave-a]');
    var stB = sec.querySelector('[data-wave-b]');
    var hzEl = sec.querySelector('[data-hz]');
    var vis = this._visibleFlag(sec, '100px');
    var m = this._mouse;
    var state = { m: 0, lastHz: '' };
    var seed = [];
    for (var i = 0; i < 64; i++) seed.push(Math.random());

    this._addScene(sec, function (p) {
      state.m = smooth(seg(p, .3, .64));
      var wa = easeInOut(seg(p, .34, .45)), wb = easeInOut(seg(p, .47, .6));
      stA.style.clipPath = 'inset(0 0 0 ' + (wa * 100).toFixed(2) + '%)';
      stB.style.clipPath = 'inset(0 ' + ((1 - wb) * 100).toFixed(2) + '% 0 0)';
      var hz = Math.round(20 * Math.pow(100, state.m));
      if (hz > 1990) hz = 2000;
      var txt = hz.toLocaleString('en-US');
      if (txt !== state.lastHz) { state.lastHz = txt; hzEl.textContent = txt; }
    });

    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var size = function () {
      cv.width = Math.round(cv.clientWidth * dpr);
      cv.height = Math.round(cv.clientHeight * dpr);
    };
    size();
    this._on(window, 'resize', size);

    this._drawers.push(function (t) {
      if (!vis.on) return;
      if (cv.width !== Math.round(cv.clientWidth * dpr)) size();
      var W = cv.width, H = cv.height, mm = state.m;
      ctx.clearRect(0, 0, W, H);
      var y0 = H * .6, A = H * .13;
      var rect = cv.getBoundingClientRect();
      var mx = (m.x - rect.left) * dpr, my = (m.y - rect.top) * dpr;
      var hover = m.x >= 0 && my > 0 && my < H;
      var period = W / 6.5;
      var lambda = W / 30;
      var step = Math.max(1, Math.round(1.5 * dpr));

      function sample(x, phase) {
        var u = ((x + t * 40 * dpr) % period + period) % period / period;
        var k = Math.floor((x + t * 40 * dpr) / period);
        var j = seed[((k % 64) + 64) % 64];
        var spike = 0;
        if (u < .035) spike = -1 - j * .35;
        else if (u < .07) spike = .75 + j * .2;
        spike += (seed[Math.floor(x / 9) % 64] - .5) * .05;
        var env = .3 + .7 * smooth(clamp(x / (W * .38), 0, 1));
        var sine = Math.sin((x / lambda) * Math.PI * 2 - t * 5 + phase) * env;
        var y = (1 - mm) * spike + mm * sine;
        var amp = A;
        if (hover) amp *= 1 + .45 * Math.exp(-Math.pow((x - mx) / (90 * dpr), 2));
        return y0 + y * amp;
      }

      function path(phase, offY) {
        ctx.beginPath();
        for (var x = 0; x <= W; x += step) {
          var y = sample(x, phase) + offY;
          if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
      }

      var r = Math.round(lerp(236, 203, mm)), g = Math.round(lerp(234, 242, mm)), b = Math.round(lerp(228, 58, mm));
      ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      /* echoes */
      ctx.strokeStyle = 'rgba(' + r + ',' + g + ',' + b + ',' + (.1 + .06 * mm).toFixed(3) + ')';
      ctx.lineWidth = 1 * dpr;
      path(.9, -A * .5 * mm); ctx.stroke();
      path(-.9, A * .5 * mm); ctx.stroke();
      /* glow passes (pre-composed strokes, no blur filter) */
      if (mm > .02) {
        ctx.strokeStyle = 'rgba(203,242,58,' + (.07 * mm).toFixed(3) + ')';
        ctx.lineWidth = 14 * dpr; path(0, 0); ctx.stroke();
        ctx.strokeStyle = 'rgba(203,242,58,' + (.16 * mm).toFixed(3) + ')';
        ctx.lineWidth = 5 * dpr; path(0, 0); ctx.stroke();
      }
      ctx.strokeStyle = 'rgb(' + r + ',' + g + ',' + b + ')';
      ctx.lineWidth = lerp(1.4, 2, mm) * dpr;
      path(0, 0); ctx.stroke();
    });
  }

  _sceneZones() {
    var sec = this.querySelector('#sw-zones');
    if (!sec) return;
    var vid = sec.querySelector('[data-zones-vid]');
    var items = Array.prototype.slice.call(sec.querySelectorAll('[data-zone-step]'));
    var TIMES = [0.34, 0.92, 1.22, 1.6];
    var END = 0.02;
    var st = { target: 0, cur: 0, step: -2, ready: false };
    var markReady = function () { st.ready = true; };
    vid.addEventListener('loadeddata', markReady, { once: true });
    try { vid.load(); } catch (_) {}
    this._addScene(sec, function (p) {
      var s = (p - .08) / .2;
      var step = p < .08 ? -1 : (s >= 4 ? 4 : Math.floor(s));
      st.target = step < 0 ? 0 : (step >= 4 ? END : TIMES[step]);
      if (step !== st.step) {
        st.step = step;
        items.forEach(function (li) {
          var k = parseInt(li.getAttribute('data-zone-step'), 10);
          li.classList.toggle('is-on', k === step || step === 4);
          li.classList.toggle('is-done', step !== 4 && k < step);
        });
      }
    });
    var vis = this._visibleFlag(sec, '200px');
    this._drawers.push(function () {
      if (!vis.on || !st.ready || vid.seeking) return;
      st.cur += (st.target - st.cur) * .12;
      if (Math.abs(vid.currentTime - st.cur) > .025) {
        try { vid.currentTime = st.cur; } catch (_) {}
      }
    });
  }

  _sceneMotion() {
    var wrap = this.querySelector('[data-accs]');
    if (!wrap) return;
    var self = this;
    var accs = Array.prototype.slice.call(wrap.querySelectorAll('[data-acc]'));
    var label = this.querySelector('[data-pulse-label]');
    var names = ['Squat', 'Run', 'Ride'];
    var st = { i: 0, played: 0, hz: parseFloat(accs[0].getAttribute('data-hz')), hzTarget: parseFloat(accs[0].getAttribute('data-hz')), lastT: 0 };
    var vis = this._visibleFlag(wrap, '0px');

    var activate = function (i) {
      st.i = i; st.played = 0; st.lastT = 0;
      st.hzTarget = parseFloat(accs[i].getAttribute('data-hz')) || 1;
      accs.forEach(function (a, k) {
        a.classList.toggle('is-on', k === i);
        var v = a.querySelector('video');
        if (k === i) { v.currentTime = 0; v.muted = true; if (vis.on) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } }
        else { try { v.pause(); } catch (_) {} }
      });
      if (label) label.textContent = 'Pulse synced · ' + names[i];
    };

    accs.forEach(function (a, i) {
      var v = a.querySelector('video');
      self._on(v, 'ended', function () {
        if (st.i !== i) return;
        if (st.played < MIN_CLIP_SECONDS) { v.currentTime = 0; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
        else activate((i + 1) % accs.length);
      });
      self._on(v, 'timeupdate', function () {
        if (st.i !== i) return;
        var t = v.currentTime;
        if (t >= st.lastT) st.played += t - st.lastT;
        st.lastT = t;
        var bar = a.querySelector('.sw-acc-time i');
        if (bar && v.duration) bar.style.transform = 'scaleX(' + clamp(t / v.duration, 0, 1).toFixed(3) + ')';
      });
      self._on(a, 'click', function () { if (st.i !== i) activate(i); });
    });

    var wasOn = false;
    this._drawers.push(function () {
      if (vis.on !== wasOn) {
        wasOn = vis.on;
        var v = accs[st.i].querySelector('video');
        if (vis.on) { v.muted = true; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
        else { try { v.pause(); } catch (_) {} }
      }
    });

    /* pulse line that follows the current movement cadence */
    var cv = this.querySelector('[data-pulse]');
    if (!cv) return;
    var ctx = cv.getContext('2d');
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var phase = 0;
    this._drawers.push(function (t, dt) {
      if (!vis.on) return;
      if (cv.width !== Math.round(cv.clientWidth * dpr)) { cv.width = Math.round(cv.clientWidth * dpr); cv.height = Math.round(cv.clientHeight * dpr); }
      var W = cv.width, H = cv.height;
      st.hz += (st.hzTarget - st.hz) * .05;
      phase += dt * st.hz * Math.PI * 2;
      ctx.clearRect(0, 0, W, H);
      ctx.beginPath();
      var cycles = 9 * st.hz;
      for (var x = 0; x <= W; x += 2) {
        var u = x / W;
        var burst = Math.pow(Math.max(0, Math.sin(u * cycles * Math.PI - phase)), 6);
        var y = H / 2 - Math.sin(u * cycles * 6 * Math.PI - phase * 3) * burst * H * .38;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = '#CBF23A';
      ctx.lineWidth = 1.6 * dpr;
      ctx.stroke();
    });
  }

  _sceneMid() {
    var sec = this.querySelector('#sw-mid');
    if (!sec) return;
    var media = sec.querySelector('[data-mid-media]');
    var img = media.querySelector('img');
    this._addScene(sec, function (p) {
      if (window.innerWidth <= 760) return;
      var o = easeOut(seg(p, 0, .95));
      media.style.clipPath = 'inset(' + lerp(6, 0, o).toFixed(2) + '% ' + lerp(4, 0, o).toFixed(2) + '% ' + lerp(6, 0, o).toFixed(2) + '% ' + lerp(4, 0, o).toFixed(2) + '% round ' + lerp(48, 0, o).toFixed(1) + 'px)';
      img.style.transform = 'scale(' + lerp(1.1, 1, seg(p, 0, 1.6)).toFixed(4) + ')';
    }, { sticky: false });
  }

  _sceneScan() {
    var sec = this.querySelector('#sw-scan');
    if (!sec) return;
    var line = sec.querySelector('[data-scan-line]');
    var copy = sec.querySelector('[data-scan-copy]');
    var sticky = sec.querySelector('.sw-sticky');
    this._addScene(sec, function (p, r, vh) {
      var y = lerp(-0.02, 1.02, seg(p, .04, .72)) * vh;
      line.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)';
      line.style.opacity = (p > .74 ? 0 : 1);
      var cr = copy.getBoundingClientRect(), sr = sticky.getBoundingClientRect();
      var reveal = y - (cr.top - sr.top);
      var cut = clamp(cr.height - reveal, 0, cr.height);
      copy.style.clipPath = 'inset(0 0 ' + cut.toFixed(1) + 'px 0)';
    });
  }

  _sceneApp() {
    var sec = this.querySelector('#sw-app');
    if (!sec) return;
    var ring = sec.querySelector('[data-ring-el]');
    var cards = Array.prototype.slice.call(sec.querySelectorAll('[data-ring]'));
    var caps = Array.prototype.slice.call(sec.querySelectorAll('[data-ring-cap]'));
    var STEP = 32;
    var lastIdx = -1;
    var m = this._mouse;
    this._addScene(sec, function (p) {
      var w = ring.offsetWidth;
      var R = w * 2.4;
      var pp = smooth(seg(p, .06, .9));
      var rot = -pp * STEP * (cards.length - 1);
      var tilt = (m.ny - .5) * -6;
      ring.style.transform = 'translateZ(' + (-R).toFixed(0) + 'px) rotateX(' + tilt.toFixed(2) + 'deg) rotateY(' + rot.toFixed(2) + 'deg)';
      cards.forEach(function (c, i) {
        var ang = i * STEP;
        var rel = (ang + rot) * Math.PI / 180;
        var face = Math.cos(rel);
        c.style.transform = 'rotateY(' + ang + 'deg) translateZ(' + R.toFixed(0) + 'px)';
        c.style.opacity = (.18 + .82 * clamp((face - .82) / .18, 0, 1)).toFixed(3);
        c.style.zIndex = String(Math.round(face * 100));
      });
      var idx = Math.round(pp * (cards.length - 1));
      if (idx !== lastIdx) {
        lastIdx = idx;
        caps.forEach(function (c, i) { c.classList.toggle('is-on', i === idx); });
      }
    });
  }

  _sceneEasy() {
    var sec = this.querySelector('#sw-easy');
    if (!sec) return;
    var track = sec.querySelector('[data-easy-track]');
    var idxEl = sec.querySelector('[data-easy-idx]');
    var n = track.children.length;
    var last = '';
    this._addScene(sec, function (p) {
      if (window.innerWidth <= 760) return;
      var pp = smooth(seg(p, .04, .94));
      var dist = Math.max(0, track.scrollWidth - window.innerWidth);
      track.style.transform = 'translate3d(' + (-pp * dist).toFixed(1) + 'px,0,0)';
      var i = String(Math.min(n, Math.round(pp * (n - 1)) + 1));
      if (i !== last) { last = i; idxEl.textContent = '0' + i; }
    });
  }

  _sceneMarquee() {
    var mq = this.querySelector('[data-marquee] .sw-marquee-in');
    if (!mq) return;
    var self = this;
    var vis = this._visibleFlag(mq, '100px');
    var x = 0;
    this._drawers.push(function (t, dt) {
      if (!vis.on || self._reduced) return;
      var half = mq.scrollWidth / 2;
      var speed = 60 + Math.min(900, Math.abs(self._velocity)) * .5;
      x -= speed * dt * (self._velocity < -40 ? -1 : 1);
      if (x <= -half) x += half;
      if (x > 0) x -= half;
      mq.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
    });
  }

  _sceneFinal() {
    var sec = this.querySelector('#sw-final');
    if (!sec) return;
    var glow = sec.querySelector('[data-final-glow]');
    var mark = sec.querySelector('[data-final-mark] img');
    var m = this._mouse;
    var vis = this._visibleFlag(sec, '0px');
    var g = { x: 0, y: 0 };
    this._drawers.push(function () {
      if (!vis.on) return;
      var r = sec.getBoundingClientRect();
      var tx = m.x < 0 ? 0 : (m.x - r.left - r.width / 2) * .25;
      var ty = m.y < 0 ? 0 : (m.y - r.top - r.height * .34) * .15;
      g.x += (tx - g.x) * .05; g.y += (ty - g.y) * .05;
      glow.style.transform = 'translate(-50%,-50%) translate3d(' + g.x.toFixed(1) + 'px,' + g.y.toFixed(1) + 'px,0)';
      var vh = window.innerHeight;
      var k = clamp((vh - r.bottom + vh * .9) / (vh * .9), 0, 1);
      if (mark) mark.style.transform = 'translate3d(0,' + lerp(34, 0, easeOut(k)).toFixed(2) + '%,0)';
    });
  }

  _setupCountdown() {
    var els = { d: this.querySelector('[data-cd="d"]'), h: this.querySelector('[data-cd="h"]'), m: this.querySelector('[data-cd="m"]'), s: this.querySelector('[data-cd="s"]') };
    if (!els.d) return;
    var target = new Date(LAUNCH_AT).getTime();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var tick = function () {
      var diff = Math.max(0, target - Date.now());
      els.d.textContent = pad(Math.floor(diff / 864e5));
      els.h.textContent = pad(Math.floor(diff % 864e5 / 36e5));
      els.m.textContent = pad(Math.floor(diff % 36e5 / 6e4));
      els.s.textContent = pad(Math.floor(diff % 6e4 / 1e3));
    };
    tick();
    this._intervals.push(setInterval(tick, 1000));
  }
}

export function registerSweetmyoElement() {
  if (!customElements.get('sweetmyo-gen2-landing')) customElements.define('sweetmyo-gen2-landing', SweetmyoLanding);
}
