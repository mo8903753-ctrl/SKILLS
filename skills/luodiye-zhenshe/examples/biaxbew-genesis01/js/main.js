/* biaXbew Genesis01 — interactions
   GSAP + ScrollTrigger + Lenis. Every lighting change on this page swaps between real photographs. */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const mq = (q) => window.matchMedia(q).matches;
  const REDUCE = mq('(prefers-reduced-motion: reduce)');
  const DESK = mq('(min-width: 901px)');
  const FINE = mq('(hover: hover) and (pointer: fine)');
  const AUTOPLAY_MS = 1500;
  const root = document.documentElement;
  const clamp = gsap.utils.clamp;

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'power3.out' });

  /* ───────── smooth scroll ───────── */
  let lenis = null;
  if (!REDUCE && window.Lenis) {
    lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  $$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
    const t = $(a.getAttribute('href'));
    if (!t) return;
    e.preventDefault();
    const focus = () => { const i = $('input[type=email]', t); if (i) i.focus({ preventScroll: true }); };
    if (lenis) lenis.scrollTo(t, { offset: -innerHeight * 0.3, duration: 1.4, onComplete: focus });
    else { t.scrollIntoView({ block: 'center' }); focus(); }
  }));

  /* ───────── the page glow follows the keyboard's light ───────── */
  const GLOW = {
    blue: [47, 107, 255], violet: [162, 91, 255], white: [223, 230, 255], wave: [60, 230, 140], red: [255, 59, 59],
    amber: [255, 194, 59], green: [55, 255, 107], cyan: [47, 230, 255], prism: [255, 80, 190], gold: [201, 164, 92], off: [34, 34, 40],
  };
  const glowV = { r: 47, g: 107, b: 255 };
  let glowAt = 0, glowRoots = null;
  function paintGlow(force) {
    const now = performance.now();
    if (force !== true && now - glowAt < 90) return;
    glowAt = now;
    glowRoots = glowRoots || ($$('.gxg').length ? $$('.gxg') : [root]);
    const r = Math.round(glowV.r), g = Math.round(glowV.g), b = Math.round(glowV.b);
    glowRoots.forEach((el) => { el.style.setProperty('--gr', r); el.style.setProperty('--gg', g); el.style.setProperty('--gb', b); });
  }
  function setGlow(c, d = 0.9) {
    const [r, g, b] = Array.isArray(c) ? c : GLOW[c];
    gsap.to(glowV, { r, g, b, duration: d, ease: 'power2.out', overwrite: true, onUpdate: paintGlow, onComplete: () => paintGlow(true) });
  }
  const CYCLE = ['blue', 'violet', 'prism', 'amber', 'green', 'cyan'];
  let cycleOn = true, cycleI = 0;
  setInterval(() => { if (cycleOn && !document.hidden) setGlow(CYCLE[++cycleI % CYCLE.length], 2.2); }, AUTOPLAY_MS);
  const el$ = (t) => (typeof t === 'string' ? $(t) : t);
  // fires when the element crosses the middle of the screen
  const zone = (trigger, enter) => new IntersectionObserver(([e]) => { if (e.isIntersecting) enter(); }, { rootMargin: '-48% 0px -48% 0px' }).observe(el$(trigger));
  // reports whether a good part of the element is on screen
  const watch = (trigger, fn, th = 0.3) => new IntersectionObserver(([e]) => fn(e.isIntersecting), { threshold: th }).observe(el$(trigger));
  const onSeen = (trigger, fn, once) => { const io = new IntersectionObserver(([e]) => { if (!e.isIntersecting) return; fn(); if (once) io.disconnect(); }, { rootMargin: '0px 0px -8% 0px' }); io.observe(el$(trigger)); };

  /* ───────── text splitting ───────── */
  function splitWords(el) {
    const wrap = (node) => {
      if (node.nodeType === 3) {
        const f = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach((t) => {
          if (!t) return;
          if (/^\s+$/.test(t)) { f.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.className = 'w';
          const i = document.createElement('i'); i.textContent = t; w.appendChild(i); f.appendChild(w);
        });
        node.replaceWith(f);
      } else if (node.nodeType === 1) [...node.childNodes].forEach(wrap);
    };
    [...el.childNodes].forEach(wrap);
    return $$('.w > i', el);
  }
  $$('[data-split]').forEach((el) => {
    const words = splitWords(el);
    if (REDUCE) return;
    if (el.closest('.hero')) return;            // the first screen is readable the moment it paints
    gsap.set(words, { yPercent: 115 });
    onSeen(el, () => gsap.to(words, { yPercent: 0, duration: 1.1, ease: 'expo.out', stagger: 0.045 }), true);
  });
  $$('[data-words]').forEach((el) => {
    el.innerHTML = el.textContent.trim().split(/\s+/).map((w) => `<span class="pw">${w}</span>`).join(' ');
  });

  /* ───────── cursor + magnetic ───────── */
  if (FINE && !REDUCE) {
    const cur = $('.cursor'), ring = $('.cursor b');
    const x = gsap.quickTo(cur, 'x', { duration: 0.18, ease: 'power3' }), y = gsap.quickTo(cur, 'y', { duration: 0.18, ease: 'power3' });
    addEventListener('mousemove', (e) => { x(e.clientX); y(e.clientY); cur.style.opacity = 1; }, { passive: true });
    document.addEventListener('mouseleave', () => { cur.style.opacity = 0; });
    const LAB = [['.dim', 'DRAG'], ['.scenes__rail', 'DRAG'], ['.type', 'TYPE']];
    document.addEventListener('mouseover', (e) => {
      const t = e.target;
      const lab = LAB.find(([s]) => t.closest(s));
      const hot = t.closest('a,button,input,[role=tab],.pos__p,.pos__title span,.game__tok li');
      cur.classList.toggle('is-lab', !!lab && !hot);
      cur.classList.toggle('is-hot', !!hot);
      ring.textContent = lab && !hot ? lab[1] : '';
    });
    $$('[data-magnetic]').forEach((b) => {
      b.addEventListener('mousemove', (e) => {
        const r = b.getBoundingClientRect();
        gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * 0.28, y: (e.clientY - r.top - r.height / 2) * 0.4, duration: 0.4 });
      });
      b.addEventListener('mouseleave', () => gsap.to(b, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1,.45)' }));
    });
  }

  /* ───────── nav ───────── */
  const nav = $('.nav');
  ScrollTrigger.create({
    start: 0, end: 'max',
    onUpdate: (s) => {
      nav.classList.toggle('is-solid', s.scroll() > 40);
      nav.classList.toggle('is-hide', s.direction === 1 && s.scroll() > innerHeight * 0.8);
    },
  });

  /* ───────── forms (front-end only: connect to the mailing list before launch) ───────── */
  $$('.form').forEach((f) => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const i = $('input', f), m = $('.form__msg', f);
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(i.value.trim());
    f.classList.toggle('is-ok', ok); f.classList.toggle('is-err', !ok);
    m.textContent = ok ? 'You’re on the list — watch your inbox for launch day.' : 'Please enter a valid email address.';
    if (ok) { i.value = ''; i.blur(); setGlow([5, 206, 120], 0.5); }
  }));

  /* ───────── numbers roll up each time they enter view, then land with a bounce ───────── */
  $$('[data-count]').forEach((el) => {
    const to = parseFloat(el.dataset.count), dec = +el.dataset.dec || 0, sep = !!el.dataset.sep;
    const fmt = (v) => (sep ? Math.round(v).toLocaleString('en-US') : v.toFixed(dec));
    el.textContent = fmt(to);
    if (REDUCE) return;
    const o = { v: 0 }, pop = el.closest('.fx__num') || el;   // gradient text must bounce as one piece
    const play = () => {
      gsap.killTweensOf(o); o.v = 0;
      gsap.to(o, {
        v: to, duration: 1.5, ease: 'power3.out', onUpdate: () => { el.textContent = fmt(o.v); },
        onComplete: () => { el.textContent = fmt(to); gsap.fromTo(pop, { scale: 1.22, y: -4 }, { scale: 1, y: 0, duration: 0.55, ease: 'back.out(3.2)' }); },
      });
    };
    onSeen(el, play);
  });

  /* ───────── image reveals + inner parallax ───────── */
  if (!REDUCE) {
    $$('.sw__fig, .game__fig').forEach((f) => {
      gsap.fromTo(f, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 1.3, ease: 'expo.out', scrollTrigger: { trigger: f, start: 'top 88%', once: true } });
    });
    $$('[data-par]').forEach((f) => {
      const p = parseFloat(f.dataset.par), img = $('img', f);
      gsap.fromTo(img, { yPercent: p > 0 ? -13.5 : 0 }, { yPercent: p > 0 ? 0 : -13.5, ease: 'none', scrollTrigger: { trigger: f, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  }

  /* ═════════ HERO ═════════ */
  (() => {
    const kb = $('.kb'), kb3d = $('.kb3d'), body = $('.kb__body'), stage = $('.hero__stage');
    for (let i = 1; i <= 6; i++) {
      const l = document.createElement('div'); l.className = 'kb__layer';
      l.style.transform = `translateZ(${-i * 6}px)`;
      body.after(l);
    }
    body.style.transform = 'translateZ(-38px)';
    const pose = () => (DESK
      ? { x: innerWidth * (innerWidth < 1800 ? 0.22 : 0.16), y: innerHeight * 0.055, rotateX: 48, rotateZ: -24, scale: 1.06 }
      : { x: innerWidth * 0.1, y: -innerHeight * 0.25, rotateX: 58, rotateZ: -27, scale: 1.5 });
    kb.classList.add('is-js');
    gsap.set(kb, { xPercent: -50, yPercent: -50, ...pose() });

    const words = $$('.pain__text .pw');
    let tilt = 1;
    if (REDUCE) { gsap.set('.pain', { autoAlpha: 0 }); return; }

    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: '.hero', start: 'top top', end: 'bottom bottom', scrub: 0.7, invalidateOnRefresh: true,
        onUpdate: (s) => {
          tilt = 1 - clamp(0, 1, s.progress / 0.3);
          const p = clamp(0, 1, (s.progress - 0.5) / 0.38), n = Math.round(p * words.length);
          words.forEach((w, i) => w.classList.toggle('is-on', i < n));
        },
      },
    });
    tl.fromTo(kb, pose, { x: 0, y: () => (DESK ? 0 : -innerHeight * 0.04), rotateX: 0, rotateZ: 0, scale: () => (DESK ? 0.86 : 0.96), duration: 0.36, ease: 'power2.inOut', immediateRender: false }, 0)
      .to('.hero__copy', { autoAlpha: 0, y: -50, duration: 0.14 }, 0.02)
      .to('.hero__hint', { autoAlpha: 0, duration: 0.06 }, 0)
      .to('.kb__glow', { opacity: 0.45, duration: 0.3 }, 0.05)
      .to(kb, { scale: () => (DESK ? 2.5 : 3.4), y: () => innerHeight * 0.1, duration: 0.5, ease: 'power2.in' }, 0.36)
      .to(stage, { opacity: 0.16, duration: 0.28 }, 0.4)
      .to('.pain', { autoAlpha: 1, duration: 0.08 }, 0.44)
      .to({}, { duration: 0.14 }, 0.86);

    // cursor tilt + sheen
    if (FINE) {
      const rx = gsap.quickTo(kb3d, 'rotateX', { duration: 0.9 }), ry = gsap.quickTo(kb3d, 'rotateY', { duration: 0.9 });
      const sheen = $('.kb__sheen');
      $('.hero').addEventListener('mousemove', (e) => {
        const nx = e.clientX / innerWidth - 0.5, ny = e.clientY / innerHeight - 0.5;
        rx(-ny * 9 * tilt); ry(nx * 12 * tilt);
        sheen.style.setProperty('--sx', `${100 - (nx + 0.5) * 100}%`);
        sheen.style.opacity = 0.9 * tilt;
      }, { passive: true });
    }
    zone('.hero', () => { cycleOn = true; });

    // intro
    const intro = () => {
      gsap.from(kb3d, { z: -160, rotateY: 8, duration: 1.4, ease: 'expo.out' });
      gsap.from('.nav', { yPercent: -120, duration: 1, delay: 0.5, ease: 'expo.out', clearProps: 'transform' });
    };
    intro();
  })();

  /* ═════════ POSITIONING ═════════ */
  (() => {
    const ps = $$('.pos__p'), ts = $$('.pos__title span');
    let auto = null, active = false, idle = null, k = 0;
    const set = (i) => { k = i; ps.forEach((p) => p.classList.toggle('is-on', +p.dataset.k === i)); ts.forEach((t) => t.classList.toggle('is-on', +t.dataset.k === i)); };
    set(0);
    const run = () => { clearInterval(auto); if (active) auto = setInterval(() => set((k + 1) % 3), AUTOPLAY_MS); };
    const pick = (i) => { clearInterval(auto); clearTimeout(idle); set(i); idle = setTimeout(run, 3500); };
    [...ps, ...ts].forEach((el) => {
      el.addEventListener('mouseenter', () => pick(+el.dataset.k));
      el.addEventListener('click', () => pick(+el.dataset.k));
    });
    watch('.pos__panels', (v) => { active = v; run(); });
    zone('.pos', () => { cycleOn = false; setGlow('cyan'); });
    if (!REDUCE) gsap.from(ps, { clipPath: 'inset(100% 0 0 0)', duration: 1.3, ease: 'expo.out', stagger: 0.1, scrollTrigger: { trigger: '.pos__panels', start: 'top 82%', once: true } });
  })();

  /* ═════════ 01 AI LIGHTING ═════════ */
  (() => {
    const stage = $('.ai__stage'), stack = $('#stack'), steps = $$('.ai__steps li'), dots = $$('.ai__palette i');
    const NAMES = ['blue', 'violet', 'white', 'wave', 'red', 'amber', 'green', 'cyan', 'prism'];
    const suf = DESK ? '' : '@m';
    const imgs = {};
    NAMES.forEach((n, i) => {
      const im = new Image(); im.alt = `Genesis01 with ${n} lighting`;  im.decoding = 'async';
      im.src = `assets/seq/a-${n}${suf}.webp`; if (i === 0) im.className = 'is-on';
      stack.appendChild(im); imgs[n] = im;
    });


    let cur = 'blue', busy = false, active = false, timer = null, typing = null, generation = 0;
    const step = (i) => steps.forEach((s, j) => s.classList.toggle('is-on', j === i));
    function go(name, done = () => {}) {
      dots.forEach(c => c.classList.toggle('is-on', c.dataset.f === name));
      if (busy) return;
      if (name === cur) { step(2); done(); return; }
      busy = true; step(1);
      const a = imgs[cur], b = imgs[name];
      if (b.dataset.src) { b.src = b.dataset.src; delete b.dataset.src; }
      const run = () => {
        setGlow(name, 1);
        if (REDUCE) { a.classList.remove('is-on'); b.classList.add('is-on'); cur = name; busy = false; step(2); done(); return; }
        b.classList.add('is-in'); stage.classList.add('is-gen');
        gsap.fromTo(stage, { '--p': 0 }, {
          '--p': 122, duration: 1.15, ease: 'power2.inOut',
          onComplete: () => {
            a.classList.remove('is-on'); b.classList.remove('is-in'); b.classList.add('is-on'); stage.classList.remove('is-gen');
            cur = name; busy = false; step(2); done();
          },
        });
      };
      if (b.complete && b.naturalWidth) run(); else { b.onload = run; b.onerror = () => { busy = false; status.textContent = 'Loading the next lighting preview…'; schedule(1200); }; }
    }
    const typed = $('#ai-typed'), mood = $('#ai-mood'), status = $('#ai-status'), studio = $('.ai__studio');
    const demos = [['green','Forest Rain'],['violet','Neon Dusk'],['wave','Aurora Wave'],['red','Lava Flow'],['cyan','Arctic Drift'],['amber','Golden Hour'],['prism','Arcade Prism'],['white','Moonlit Focus'],['blue','Deep-sea Pulse']];
    let index = 0;
    const schedule = ms => { clearTimeout(timer); if (active && !REDUCE) timer = setTimeout(play, ms); };
    function play() {
      if (!active) return;
      if (busy) { schedule(300); return; }
      clearInterval(typing); const token = ++generation;
      const [name,label] = demos[index++ % demos.length], sentence = `I want\n${label}.`;
      typed.textContent = ''; mood.textContent = label; status.textContent = 'An idea becomes a lighting mood.';
      studio.classList.add('is-typing'); step(0); let count = 0;
      const complete = () => {
        clearInterval(typing); studio.classList.remove('is-typing');
        if (token !== generation || !active) return;
        timer = setTimeout(() => {
          if (!active || token !== generation) return;
          status.textContent = 'Creating your lighting…';
          go(name, () => { status.textContent = `${label} is ready.`; stage.dataset.mood = name; schedule(AUTOPLAY_MS); });
        }, REDUCE ? 0 : 380);
      };
      if (REDUCE) { typed.textContent = sentence; complete(); }
      else typing = setInterval(() => { typed.textContent = sentence.slice(0, ++count); if (count >= sentence.length) complete(); }, 58);
    }
    const visibility = () => {
      const r = stage.getBoundingClientRect();
      const v = !document.hidden && r.bottom > innerHeight * .15 && r.top < innerHeight * .85;
      if (v === active) return;
      active = v; clearTimeout(timer);
      if (v) { cycleOn = false; setGlow(cur); if (!busy) play(); }
      else { clearInterval(typing); generation++; studio.classList.remove('is-typing'); }
    };
    let visibilityFrame = null;
    const checkVisibility = () => { if (visibilityFrame) return; visibilityFrame = requestAnimationFrame(() => { visibilityFrame = null; visibility(); }); };
    addEventListener('scroll', checkVisibility, {passive:true});
    addEventListener('resize', checkVisibility);
    document.addEventListener('visibilitychange', checkVisibility);
    visibility(); setInterval(visibility, 1000);
  })();

  /* ═════════ 02 AMBIANCE ═════════ */
  (() => {
    const frames = $$('.amb__scene'), tabs = $$('.amb__tabs button'), pause = $('.amb__pause');
    let current = 0, visible = false, paused = false, timer = null, held = 0;
    const colors = ['blue','amber','violet'];
    const select = (index) => {
      current = index;
      frames.forEach((f,i)=>{f.classList.toggle('is-on',i===index);f.setAttribute('aria-hidden',i!==index);});
      tabs.forEach((t,i)=>{t.classList.toggle('is-on',i===index);t.setAttribute('aria-selected',i===index);});
      if(visible){cycleOn=false;setGlow(colors[index]);}
    };
    const play = () => {clearInterval(timer);if(visible&&!paused&&!REDUCE)timer=setInterval(()=>{if(!document.hidden&&performance.now()>held)select((current+1)%3);},AUTOPLAY_MS);};
    tabs.forEach((t,i)=>{t.addEventListener('click',()=>{held=performance.now()+5000;select(i);});t.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const n=(current+(e.key==='ArrowRight'?1:2))%3;tabs[n].focus();tabs[n].click();});});
    pause.addEventListener('click',()=>{paused=!paused;pause.textContent=paused?'Play':'Pause';pause.setAttribute('aria-pressed',paused);play();});
    watch('.amb__stage',v=>{visible=v;play();},.25);select(0);

    // "20+" light tiles — two endless rows, speed leans on scroll velocity
    const rows = $$('.fx__row').map((row) => {
      row.append(...[...row.children].map((n) => n.cloneNode(true)));
      return { row, dir: +row.dataset.dir, x: 0 };
    });
    let live = false, vel = 0;
    new IntersectionObserver(([e]) => { live = e.isIntersecting; }, { rootMargin: '200px' }).observe($('.fx__rows'));
    if (lenis) lenis.on('scroll', (e) => { vel = e.velocity; });
    if (!REDUCE) gsap.ticker.add((t, dt) => {
      if (!live) return;
      rows.forEach((r) => {
        const half = r.row.scrollWidth / 2;
        r.x += r.dir * (0.045 * dt + vel * 0.55);
        if (r.x <= -half) r.x += half; if (r.x > 0) r.x -= half;
        r.row.style.transform = `translate3d(${r.x}px,0,0)`;
      });
      vel *= 0.92;
    });
    zone('.fx', () => { cycleOn = true; });
  })();

  /* ═════════ 03 CRAFT ═════════ */
  (() => {
    const pin = $('.craft__pin'), track = $('.craft__track');
    if (pin && track && DESK && !REDUCE) {
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      const size = () => { pin.style.height = `${dist() + innerHeight}px`; };
      size(); ScrollTrigger.addEventListener('refreshInit', size);
      const st = { trigger: pin, start: 'top top', end: 'bottom bottom', scrub: 0.6, invalidateOnRefresh: true };
      gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: st });
      gsap.to('.craft__bar i', { scaleX: 1, ease: 'none', scrollTrigger: st });
      $$('.craft__main').forEach((im) => gsap.fromTo(im, { scale: 1.18 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: pin, start: 'top top', end: 'bottom bottom', scrub: 0.6 } }));
    }
    if (pin && !DESK && !REDUCE) {
      const rail = $('.craft__sticky'), frames = $$('.craft__f');
      let timer = null, active = false, held = 0;
      rail.addEventListener('pointerdown', () => { held = performance.now() + 5000; });
      watch(rail, (v) => {
        active = v; clearInterval(timer);
        if (active) timer = setInterval(() => {
          if (document.hidden || performance.now() < held) return;
          const current = frames.reduce((best, f, i) => Math.abs(f.offsetLeft - rail.scrollLeft - 20) < Math.abs(frames[best].offsetLeft - rail.scrollLeft - 20) ? i : best, 0);
          rail.scrollTo({left:frames[(current + 1) % frames.length].offsetLeft - frames[0].offsetLeft,behavior:'smooth'});
        }, AUTOPLAY_MS);
      });
    }
    zone('.craft', () => { cycleOn = false; setGlow('gold'); });

    // A single large engraving at a time keeps every etched line readable.
    const plates = $$('.plate'), tabs = $$('.plates__tabs button'), stage = $('.plates__stage'), pause = $('.plates__pause');
    let on = 0, auto = null, active = false, paused = false, held = 0;
    const pick = i => {
      on=i;
      plates.forEach((p,n)=>{p.classList.toggle('is-on',n===i);p.setAttribute('aria-hidden',n!==i);});
      tabs.forEach((t,n)=>{t.classList.toggle('is-on',n===i);t.setAttribute('aria-selected',n===i);});
      if(!REDUCE)gsap.fromTo(plates[i],{y:22,scale:.97},{y:0,scale:1,duration:.7,ease:'power2.out',overwrite:true});
    };
    const run=()=>{clearInterval(auto);if(active&&!paused&&!REDUCE)auto=setInterval(()=>{if(!document.hidden&&performance.now()>held)pick((on+1)%3)},AUTOPLAY_MS);};
    tabs.forEach((t,i)=>{t.addEventListener('click',()=>{held=performance.now()+5000;pick(i);});t.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const n=(on+(e.key==='ArrowRight'?1:2))%3;tabs[n].focus();tabs[n].click();});});
    pause.addEventListener('click',()=>{paused=!paused;pause.textContent=paused?'Play':'Pause';pause.setAttribute('aria-pressed',paused);run();});
    watch(stage,v=>{active=v;run();});pick(0);

  })();

  zone('.strip', () => { cycleOn = true; });

  /* Material stories: scroll-linked photographic chapters, with optional drag control. */
  $$('.story').forEach((story) => {
    const frames = $$('.story__frame', story), details = $$('.story__detail', story), tabs = $$('.story__tabs button', story);
    const range = $('input[type=range]', story), pause = $('.story__pause', story), caption = $('.story__caption', story), bar = $('.story__progress i', story);
    const captions = story.dataset.story === 'craft' ? ['CNC machining · Process visualization', 'The finished Genesis01 silver enclosure.', 'The finished Genesis01 black enclosure.'] : ['Ice Snow, installed in Genesis01.', 'Actual switch close-up · external construction.', 'Made for everyday typing and gaming.'];
    let active = false, paused = false, timer = null, held = 0, on = -1, progress = 0, lastScroll = scrollY, scrollHeld = 0;
    function show(value, animate = true) {
      progress = clamp(0, 1, value); const next = Math.min(2, Math.floor(progress * 3));
      range.value = Math.round(progress * 100); bar.style.transform = `scaleX(${progress})`;
      if (next !== on) {
        on = next; story.dataset.chapter = String(on);
        frames.forEach((f, i) => {f.classList.toggle('is-on', i === on);f.setAttribute('aria-hidden', i !== on);});
        details.forEach((d, i) => {d.classList.toggle('is-on', i === on);d.setAttribute('aria-hidden', i !== on);});
        tabs.forEach((t, i) => {t.classList.toggle('is-on', i === on);t.setAttribute('aria-selected', i === on);});
        caption.textContent = captions[on];
        if (animate && !REDUCE) {
          gsap.fromTo(frames[on], {clipPath:'inset(0 0 0 18%)'}, {clipPath:'inset(0)',duration:.55,ease:'power2.out',overwrite:true});
          gsap.fromTo($('.story__cutout', frames[on]) || $('img', frames[on]), {scale:1.12,y:16}, {scale:1,y:0,duration:1.25,ease:'power2.out',overwrite:true});
          gsap.fromTo(details[on], {opacity:.35,y:12}, {opacity:1,y:0,duration:.45,overwrite:true});
        }
      }
    }
    show(0,false);
    const stop = () => {clearInterval(timer); timer = null;};
    const run = () => {stop();if(active && !paused && !REDUCE)timer = setInterval(()=>{if(document.hidden || performance.now()<held || performance.now()<scrollHeld)return;show(((on+1)%3)/3+.08);},AUTOPLAY_MS);};
    const choose = (value) => {held = performance.now()+5000;show(value);};
    range.addEventListener('input',()=>choose(Number(range.value)/100));
    tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>choose(i/3+.08));tab.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const n=(on+(e.key==='ArrowRight'?1:2))%3;tabs[n].focus();tabs[n].click();});});
    pause.addEventListener('click',()=>{paused=!paused;pause.setAttribute('aria-pressed',paused);pause.textContent=paused?'Play':'Pause';run();});
    watch($('.story__sticky',story),v=>{active=v;run();},.3);
    if(DESK && !REDUCE) {
      ScrollTrigger.create({trigger:story,start:'top 8%',end:'bottom 90%',invalidateOnRefresh:true,onUpdate:self=>{
        if(Math.abs(scrollY-lastScroll)<2)return;lastScroll=scrollY;scrollHeld=performance.now()+600;
        if(performance.now()<held)return;
        show(self.progress); // scrolling reveals the material and the finished product in order
      }});
    }
  });

  /* ═════════ v5 helpers: a scroll-scrubbed scene with its own easing, so wheel jumps still glide ═════════ */
  const scrubScene = (el, draw) => {
    let target = 0, cur = 0, live = false, last = -1;
    const st = ScrollTrigger.create({ trigger: el, start: 'top top', end: 'bottom bottom', invalidateOnRefresh: true, onUpdate: (s) => { target = s.progress; } });
    new IntersectionObserver(([e]) => { live = e.isIntersecting; if (live) target = st.progress; }, { rootMargin: '200px 0px' }).observe(el);
    gsap.ticker.add(() => {
      if (!live) return;
      cur += (target - cur) * 0.16;
      if (Math.abs(target - cur) < 0.0004) cur = target;
      if (Math.abs(cur - last) < 0.00005) return;
      draw(cur, cur - last); last = cur;
    });
    return st;
  };
  const seg = (p, a, b) => clamp(0, 1, (p - a) / (b - a));

  /* ═════════ v5 CRAFT — one block of aluminium, cut, finished and shaped (toolpath reveals) ═════════ */
  (() => {
    const cnc = $('#cnc'); if (!cnc) return;
    const W = 1536, H = 1024;
    const done = $$('.cnc__done', cnc), paths = $$('.cnc__tp', cnc), tool = $('.cnc__tool', cnc), sheen = $('.cnc__sheen', cnc), imgs = $$('.cnc__layer image', cnc);
    const steps = $$('.cnc__steps li', cnc), rail = $$('.cnc__rail span', cnc), fill = $('.cnc__fill', cnc), cap = $('.cnc__cap', cnc), num = $('.cnc__num', cnc);
    const canvas = $('.cnc__chips', cnc), pin = $('.cnc__pin', cnc), cx = canvas.getContext('2d');
    // toolpaths in image space: raster passes, a pocketing spiral, then sweeping arcs that follow the curve
    let d1 = '', n = 8, h = H / n; for (let i = 0; i < n; i++) { const y = h / 2 + i * h; d1 += (i ? ` V ${y}` : `M -90 ${y}`) + (i % 2 ? ' H -90' : ` H ${W + 90}`); }
    let d2 = '', x0 = -60, y0 = -60, x1 = W + 60, y1 = H + 60, s = 135; d2 = `M ${x0} ${y0}`;
    while (x1 - x0 > s && y1 - y0 > s) { d2 += ` H ${x1} V ${y1} H ${x0} V ${y0 + s}`; x0 += s; y0 += s; x1 -= s; y1 -= s; d2 += ` H ${x0}`; }
    d2 += ` H ${W / 2 + 200}`;
    let d3 = '', r = 70, dir = 0, R = Math.hypot(W, H) + 120; d3 = `M ${r} ${H}`;
    while (r < R) { const r2 = r + 135; if (dir === 0) d3 += ` A ${r} ${r} 0 0 0 0 ${H - r} L 0 ${H - r2}`; else d3 += ` A ${r} ${r} 0 0 1 ${r} ${H} L ${r2} ${H}`; r = r2; dir ^= 1; }
    [d1, d2, d3].forEach((d, i) => paths[i].setAttribute('d', d));
    const L = paths.map((pa) => pa.getTotalLength());
    paths.forEach((pa, i) => { pa.style.strokeDasharray = `${L[i]} ${L[i]}`; pa.style.strokeDashoffset = L[i]; });
    const SEG = [[0.1, 0.34], [0.42, 0.64], [0.72, 0.93]];

    // metal chips, thrown from the cutter while it moves
    const chips = []; let dpr = 1, toolXY = null, cw = 0, ch = 0;
    const size = () => { dpr = Math.min(2, devicePixelRatio || 1); cw = pin.clientWidth; ch = pin.clientHeight; canvas.width = cw * dpr; canvas.height = ch * dpr; };
    size(); addEventListener('resize', size);
    const toScreen = (x, y) => { const k = Math.max(cw / W, ch / H); return [(x - W / 2) * k + cw / 2, (y - H / 2) * k + ch / 2]; };
    const spawn = (x, y, speed) => {
      const m = Math.min(6, 1 + Math.floor(speed * 900));
      for (let i = 0; i < m; i++) chips.push({ x, y, vx: (Math.random() - 0.35) * 9, vy: -Math.random() * 8 - 2, a: Math.random() * 6.28, va: (Math.random() - 0.5) * 0.6, len: 4 + Math.random() * 9, life: 1 });
      if (chips.length > 260) chips.splice(0, chips.length - 260);
    };
    let ticking = false;
    const tick = () => {
      cx.setTransform(dpr, 0, 0, dpr, 0, 0); cx.clearRect(0, 0, cw, ch);
      for (let i = chips.length - 1; i >= 0; i--) {
        const c = chips[i]; c.vy += 0.42; c.vx *= 0.985; c.x += c.vx; c.y += c.vy; c.a += c.va; c.life -= 0.022;
        if (c.life <= 0 || c.y > ch + 20) { chips.splice(i, 1); continue; }
        const dx = Math.cos(c.a) * c.len, dy = Math.sin(c.a) * c.len * 0.5;
        const g = cx.createLinearGradient(c.x - dx, c.y - dy, c.x + dx, c.y + dy);
        g.addColorStop(0, `rgba(160,170,185,${0.2 * c.life})`); g.addColorStop(0.5, `rgba(255,255,255,${0.95 * c.life})`); g.addColorStop(1, `rgba(150,160,175,${0.2 * c.life})`);
        cx.strokeStyle = g; cx.lineWidth = 1.6; cx.beginPath(); cx.moveTo(c.x - dx, c.y - dy); cx.quadraticCurveTo(c.x + dy, c.y - dx * 0.4, c.x + dx, c.y + dy); cx.stroke();
      }
      if (!chips.length) { gsap.ticker.remove(tick); ticking = false; }
    };

    let idx = -1, counted = false;
    const setStep = (i) => {
      if (i === idx) return; idx = i;
      steps.forEach((li, k) => li.classList.toggle('is-on', k === i));
      rail.forEach((sp, k) => sp.classList.toggle('is-on', k <= i));
      cap.style.opacity = i <= 1 ? 1 : 0;
      if (i === 0 && !counted && !REDUCE) { counted = true; const o = { v: 0 }; gsap.to(o, { v: 6063, duration: 1.4, ease: 'power3.out', onUpdate: () => { num.textContent = Math.round(o.v); }, onComplete: () => { counted = false; } }); }
    };
    const draw = (p, dp) => {
      let cutting = -1;
      paths.forEach((pa, i) => {
        const t = seg(p, SEG[i][0], SEG[i][1]);
        pa.style.strokeDashoffset = L[i] * (1 - t);
        done[i].setAttribute('opacity', seg(p, SEG[i][1] - 0.06, SEG[i][1] + 0.01).toFixed(3));
        const sc = 1.07 - 0.07 * seg(p, SEG[i][0], SEG[i][1] + 0.12);
        imgs[i + 1].setAttribute('transform', `translate(${W / 2} ${H / 2}) scale(${sc}) translate(${-W / 2} ${-H / 2})`);
        if (t > 0 && t < 1) cutting = i;
      });
      imgs[0].setAttribute('transform', `translate(${W / 2} ${H / 2}) scale(${1.08 - 0.08 * seg(p, 0, 0.3)}) translate(${-W / 2} ${-H / 2})`);
      if (cutting >= 0) {
        const t = seg(p, SEG[cutting][0], SEG[cutting][1]), pt = paths[cutting].getPointAtLength(L[cutting] * t);
        tool.setAttribute('cx', pt.x); tool.setAttribute('cy', pt.y); tool.style.opacity = 1;
        if (!REDUCE && Math.abs(dp) > 0.0002 && pt.x > 0 && pt.x < W && pt.y > 0 && pt.y < H) {
          const [sx, sy] = toScreen(pt.x, pt.y); spawn(sx, sy, Math.abs(dp));
          if (!ticking) { ticking = true; gsap.ticker.add(tick); }
        }
      } else tool.style.opacity = 0;
      sheen.setAttribute('x', -700 + 2600 * seg(p, 0.6, 0.86));
      fill.style.transform = `scaleX(${p})`;
      setStep(p < 0.24 ? 0 : p < 0.54 ? 1 : p < 0.82 ? 2 : 3);
    };
    if (REDUCE) { draw(1, 0); return; }
    draw(0, 0);
    scrubScene(cnc, draw);
    zone(cnc, () => { cycleOn = false; setGlow('white'); });
  })();

  /* ═════════ v5 SWITCH — one keystroke, slowed down ═════════ */
  (() => {
    const pr = $('#press'); if (!pr) return;
    const sw = $('.press__sw', pr), stem = $('.press__stem', pr), bloom = $('.press__bloom', pr), halo = $('.press__halo', pr), rings = $$('.press__rings i', pr);
    const gauge = $('.press__gauge', pr), marker = $('.press__marker', pr), act = $('.press__act', pr), stage = $('.press__stage', pr);
    const read = $('.press__read', pr), mm = $('.press__mm', pr), steps = $$('.press__steps li', pr), odo = $('.press__odo', pr);
    const field = $('.press__field', pr), fimg = $('.press__field img', pr);
    const PX_MM = 58 / 940, BOTTOM = 2.2, SCALE_MM = 2.4;     // stem travel measured on the photo: ~58 px per mm on a 940 px wide switch
    const place = () => { act.style.top = `${(1.1 / SCALE_MM) * gauge.clientHeight}px`; };
    place(); addEventListener('resize', place);
    const ring = () => { if (REDUCE) return; rings.forEach((r, i) => gsap.fromTo(r, { scale: 0.5, opacity: 0.9 }, { scale: 2.6 + i * 0.6, opacity: 0, duration: 0.9 + i * 0.15, delay: i * 0.08, ease: 'power2.out', overwrite: true })); };
    let idx = -1, locked = false, bottomed = false;
    const setStep = (i) => { if (i === idx) return; idx = i; steps.forEach((li, k) => li.classList.toggle('is-on', k === i)); };
    const draw = (p) => {
      // travel: press to 1.1 mm (actuates), on to the bottom, then a crisp return
      let travel;
      if (p < 0.08) travel = 0;
      else if (p < 0.4) travel = 1.1 * seg(p, 0.08, 0.4);
      else if (p < 0.55) travel = 1.1 + (BOTTOM - 1.1) * seg(p, 0.4, 0.55);
      else if (p < 0.64) { const t = seg(p, 0.55, 0.64); travel = BOTTOM * (1 - gsap.parseEase('back.out(2.2)')(t)); }
      else travel = 0;
      travel = Math.max(0, travel);
      stem.style.transform = `translate3d(0, ${travel * PX_MM * sw.clientWidth}px, 0)`;
      marker.style.transform = `translateY(${(travel / SCALE_MM) * gauge.clientHeight}px)`;
      const actuated = p >= 0.4 && p < 0.7;
      if (actuated && !locked) { locked = true; read.classList.add('is-locked'); act.classList.add('is-on'); ring(); if (!REDUCE) gsap.fromTo(read, { scale: 1.12 }, { scale: 1, duration: 0.55, ease: 'back.out(3)', transformOrigin: '0% 80%' }); }
      if (!actuated && locked) { locked = false; read.classList.remove('is-locked'); act.classList.remove('is-on'); }
      const atBottom = p >= 0.55 && p < 0.64;
      if (atBottom && !bottomed) { bottomed = true; ring(); }
      if (p < 0.5) bottomed = false;
      mm.textContent = (locked ? 1.1 : Math.min(1.1, travel)).toFixed(1);
      bloom.style.opacity = locked ? 1 : (travel / 1.1) * 0.25;
      bloom.style.transform = `scale(${0.7 + (locked ? 0.35 : travel * 0.2)})`;
      halo.style.opacity = locked ? 1 : (travel / 1.1) * 0.3; halo.style.transform = `scale(${locked ? 1 : 0.85 + travel * 0.1})`;
      // the single switch steps back into a whole board of them
      const z = seg(p, 0.68, 0.84);
      stage.style.opacity = 1 - seg(p, 0.68, 0.78); stage.style.transform = `translate(-50%, -50%) scale(${1 - 0.35 * z})`;
      if (!DESK) stage.style.top = '34%';
      field.style.opacity = z; fimg.style.transform = `scale(${1.2 - 0.2 * seg(p, 0.68, 1)})`;
      read.style.opacity = 1 - seg(p, 0.64, 0.69);
      odo.textContent = Math.round(50000000 * gsap.parseEase('power2.out')(seg(p, 0.72, 0.95))).toLocaleString('en-US');
      setStep(p < 0.4 ? 0 : p < 0.7 ? 1 : 2);
    };
    if (REDUCE) { draw(0.45); return; }
    draw(0);
    scrubScene(pr, draw);
    zone(pr, () => { cycleOn = false; setGlow('cyan'); });
  })();

  /* ═════════ 04 SWITCH — the page answers your own keyboard ═════════ */
  (() => {
    const box = $('#type'), keys = $('#keys'), kc = $('#kcount'), kl = $('#kleft'), hint = $('.type__hint'), snd = $('#snd'), obj = $('.type__obj img');
    const PAL = [[255, 75, 75], [255, 194, 59], [55, 255, 107], [47, 230, 255], [47, 107, 255], [162, 91, 255], [255, 80, 190]];
    let live = false, n = 0, pi = 0, typed = false, sound = false, ctx = null, demo = null, idle = null, wi = 0;
    const WORDS = ['GENESIS', 'BIAXBEW', 'ICE SNOW', 'LINEAR', '1.1 MM'];
    const runDemo = () => {
      clearInterval(demo);
      if (!live || typed || REDUCE) return;
      let word = WORDS[wi++ % WORDS.length], i = 0, rest = 0;
      demo = setInterval(() => {
        if (typed || !live) { clearInterval(demo); return; }
        if (i < word.length) { const ch = word[i++]; if (ch === ' ') add('SPACE', true, true); else add(ch, false, true); return; }
        if (++rest > 6) { word = WORDS[wi++ % WORDS.length]; i = 0; rest = 0; keys.innerHTML = ''; }
      }, 230);
    };
    new IntersectionObserver(([e]) => { live = e.isIntersecting; runDemo(); }, { threshold: 0.3 }).observe(box);
    const userTyped = () => {
      if (!typed) { typed = true; clearInterval(demo); keys.innerHTML = ''; hint.textContent = 'Keep typing'; }
      clearTimeout(idle); idle = setTimeout(() => { typed = false; keys.innerHTML = ''; hint.textContent = FINE ? 'Type on your own keyboard' : 'Tap anywhere here'; runDemo(); }, 6000);
    };
    if (!FINE) hint.textContent = 'Tap anywhere here';

    function click() {
      if (!sound) return;
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state === 'suspended') ctx.resume();
        const t = ctx.currentTime, len = Math.floor(ctx.sampleRate * 0.03);
        const buf = ctx.createBuffer(1, len, ctx.sampleRate), d = buf.getChannelData(0);
        for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 3);
        const src = ctx.createBufferSource(); src.buffer = buf;
        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 3400 + Math.random() * 900; bp.Q.value = 1.1;
        const g1 = ctx.createGain(); g1.gain.value = 0.5;
        src.connect(bp).connect(g1).connect(ctx.destination); src.start(t);
        const osc = ctx.createOscillator(), g2 = ctx.createGain();
        osc.type = 'triangle'; osc.frequency.setValueAtTime(260 + Math.random() * 40, t); osc.frequency.exponentialRampToValueAtTime(110, t + 0.05);
        g2.gain.setValueAtTime(0.22, t); g2.gain.exponentialRampToValueAtTime(0.0001, t + 0.07);
        osc.connect(g2).connect(ctx.destination); osc.start(t); osc.stop(t + 0.08);
      } catch (_) { /* audio unavailable */ }
    }
    function add(label, wide, silent) {
      const c = PAL[pi++ % PAL.length];
      const k = document.createElement('span'); k.className = 'key' + (wide ? ' is-wide' : ''); k.textContent = label;
      k.style.setProperty('--kc', c.join(' '));
      keys.appendChild(k);
      while (keys.children.length > (DESK ? 6 : 5)) keys.firstChild.remove();
      if (!REDUCE) {
        gsap.fromTo(k, { y: -30, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2.4)' });
        gsap.fromTo(obj, { y: 7 }, { y: 0, duration: 0.5, ease: 'elastic.out(1,.4)', overwrite: true });
      }
      setGlow(c, 0.25);
      if (silent) { click(); return; }
      n++; kc.textContent = n.toLocaleString('en-US'); kl.textContent = (5e7 - n).toLocaleString('en-US');
      click();
    }
    const WIDE = { ' ': 'SPACE', Enter: 'ENTER', Backspace: 'BKSP', Tab: 'TAB', Shift: 'SHIFT', Escape: 'ESC', CapsLock: 'CAPS', Control: 'CTRL', Alt: 'ALT', ArrowUp: '↑', ArrowDown: '↓', ArrowLeft: '←', ArrowRight: '→' };
    addEventListener('keydown', (e) => {
      if (!live || e.repeat || e.metaKey || e.ctrlKey) return;
      if (e.target.closest && e.target.closest('input,textarea,[role=slider]')) return;
      let lab = e.key.length === 1 && e.key !== ' ' ? e.key.toUpperCase() : WIDE[e.key];
      if (!lab) return;
      if (e.key === ' ') e.preventDefault();
      userTyped();
      add(lab, lab.length > 1 && !/^[↑↓←→]$/.test(lab));
    });
    box.addEventListener('pointerdown', (e) => {
      if (FINE || e.target.closest('button')) return;
      userTyped();
      add('BIAXBEW'[n % 7]);
    });
    snd.addEventListener('click', () => { sound = !sound; snd.setAttribute('aria-pressed', sound); snd.textContent = sound ? 'Mute demo sound' : 'Play demo sound'; if (sound) click(); });
    if (!REDUCE) gsap.fromTo(obj, { rotateZ: 18, rotateX: 38 }, { rotateZ: 8, rotateX: 24, ease: 'none', scrollTrigger: { trigger: box, start: 'top bottom', end: 'bottom top', scrub: 0.8 } });
    zone('.sw', () => { cycleOn = false; setGlow('white'); });
  })();

  /* 05 Connection modes are deliberately static icons. */

  /* ═════════ 06 BATTERY — drag the light away ═════════ */
  (() => {
    const dim = $('#dim'), h = $('.dim__handle'), read = $('.dim__n'), hrs = $('#hrs');
    const o = { x: 94 };
    let active = false;
    const apply = () => {
      dim.style.setProperty('--x', `${o.x}%`);
      const off = 1 - (o.x - 4) / 92;                    // share of the frame in lights-off mode
      read.style.opacity = clamp(0.25, 1, off * 1.7);
      h.setAttribute('aria-valuenow', Math.round(off * 100));
    };
    apply();
    const move = (cx) => { const r = dim.getBoundingClientRect(); o.x = clamp(4, 96, ((cx - r.left) / r.width) * 100); apply(); };
    let drag = false, held = 0;
    dim.addEventListener('pointerdown', (e) => { drag = true; held = Infinity; dim.setPointerCapture(e.pointerId); gsap.killTweensOf(o); move(e.clientX); });
    dim.addEventListener('pointermove', (e) => { if (drag) move(e.clientX); });
    ['pointerup', 'pointercancel'].forEach((ev) => dim.addEventListener(ev, () => { drag = false; }));
    h.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); o.x = clamp(4, 96, o.x + (e.key === 'ArrowLeft' ? -4 : 4)); apply(); } });
    const v = { n: 0 };
    const count = () => { gsap.killTweensOf(v); v.n = 0; gsap.to(v, { n: 2000, duration: REDUCE ? 0 : 1.8, ease: 'power3.out', onUpdate: () => { hrs.textContent = Math.round(v.n).toLocaleString('en-US'); }, onComplete: () => { if (!REDUCE) gsap.fromTo(hrs, { scale: 1.12 }, { scale: 1, duration: 0.5, ease: 'back.out(3)' }); } }); };
    hrs.style.display = 'inline-block';
    onSeen(read, count);
    if (REDUCE) { o.x = 40; apply(); }
    else ScrollTrigger.create({
      trigger: dim, start: 'top 72%', end: 'bottom 42%', scrub: 0.5,
      onUpdate: (s) => { if (drag || performance.now() < held) return; o.x = 94 - s.progress * 86; apply(); },
    });
    watch(dim, (v) => { active = v; if (v) { cycleOn = false; setGlow('white'); } else held = 0; }, 0.2);
  })();

  zone('.game', () => { cycleOn = false; setGlow('red'); });

  /* ═════════ SCENES ═════════ */
  (() => {
    const rail = $('#rail'), sc = $$('.scene'), idx = $('.scenes__idx span');
    let on = -1, active = false;
    const mark = (i) => {
      if (i === on) return; on = i;
      sc.forEach((s, j) => s.classList.toggle('is-on', j === i));
      idx.textContent = `0${i + 1}`;
      if (active) setGlow(sc[i].dataset.glow.split(' ').map(Number));
    };
    const nearest = () => { const c = rail.scrollLeft + rail.clientWidth * 0.4; let b = 0, bd = 1e9; sc.forEach((s, i) => { const d = Math.abs(s.offsetLeft + s.offsetWidth / 2 - c); if (d < bd) { bd = d; b = i; } }); return b; };
    let forced = -1, forcedT = null;
    rail.addEventListener('scroll', () => mark(forced >= 0 ? forced : nearest()), { passive: true });
    mark(0);
    const to = (i) => { i = clamp(0, sc.length - 1, i); forced = i; clearTimeout(forcedT); forcedT = setTimeout(() => { forced = -1; }, 1100); mark(i); rail.scrollTo({ left: sc[i].offsetLeft - parseFloat(getComputedStyle(rail).paddingLeft), behavior: REDUCE ? 'auto' : 'smooth' }); };
    $$('.scenes__btn').forEach((b) => b.addEventListener('click', () => to(on + +b.dataset.d)));
    rail.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') to(on + 1); if (e.key === 'ArrowLeft') to(on - 1); });
    // mouse drag
    let down = false, sx = 0, sl = 0, moved = 0;
    rail.addEventListener('pointerdown', (e) => { forced = -1; if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = rail.scrollLeft; moved = 0; });
    addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - sx; moved = Math.abs(dx); if (moved > 4) rail.classList.add('is-drag'); rail.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; if (moved > 4) { const n = nearest(); rail.classList.remove('is-drag'); to(n); } });
    let auto = null, ai = 0;
    const run = () => { clearInterval(auto); if (active && !REDUCE) auto = setInterval(() => { if (down) return; ai = (Math.max(on, 0) + 1) % sc.length; to(ai); }, AUTOPLAY_MS); };
    $$('.scenes__btn').forEach((b) => b.addEventListener('click', run));
    watch(rail, (v) => { active = v; if (active) { cycleOn = false; setGlow(sc[Math.max(on, 0)].dataset.glow.split(' ').map(Number)); } run(); });
  })();

  /* ═════════ END ═════════ */
  zone('.end', () => { cycleOn = true; });
  if (!REDUCE) gsap.fromTo('.end__bg img', { scale: 1.25, yPercent: -8 }, { scale: 1, yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.end', start: 'top bottom', end: 'bottom bottom', scrub: 0.6 } });

  let rT = null; const refresh = () => { clearTimeout(rT); rT = setTimeout(() => ScrollTrigger.refresh(), 250); };
  addEventListener('load', refresh);
  if (window.ResizeObserver) { const ro = new ResizeObserver(refresh); ($$('.gxg').length ? $$('.gxg') : [document.body]).forEach((n) => ro.observe(n)); }
  [600, 2000, 5000].forEach((t) => setTimeout(refresh, t));
  if (document.fonts) document.fonts.ready.then(() => ScrollTrigger.refresh());
})();
