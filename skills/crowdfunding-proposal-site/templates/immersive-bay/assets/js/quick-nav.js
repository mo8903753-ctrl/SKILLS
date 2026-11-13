// Content anchors are the single source for both navigation surfaces.
export function initQuickNav({ goTo, closeMenu }) {
  const header = document.getElementById('hdr');
  const host = document.getElementById('quickNav');
  const topics = document.getElementById('menuTopics');
  const targets = [...document.querySelectorAll('[data-nav][id]')];
  if (!host || !targets.length) return { restore() {} };
  const links = [];
  let active = -1, scheduled = false;
  const nav = document.createElement('nav');
  nav.setAttribute('aria-label', '内容直达');
  nav.className = 'topic-links';
  const step = (label, delta) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label;
    button.addEventListener('click', () => visit(Math.max(0, Math.min(targets.length - 1, active + delta))));
    return button;
  };
  const prev = step('上一项', -1), next = step('下一项', 1);
  host.append(prev, nav, next);
  targets.forEach((target, index) => {
    target.classList.add('topic-anchor');
    const link = document.createElement('a');
    link.href = '#' + target.id; link.textContent = target.dataset.nav;
    link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); visit(index);
    });
    nav.append(link); links.push(link);
    if (topics) {
      const copy = link.cloneNode(true);
      copy.addEventListener('click', event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault(); visit(index);
      });
      topics.append(copy);
    }
  });
  function visit(index, push = true) {
    const target = targets[index];
    if (!target) return;
    closeMenu();
    if (push && location.hash !== '#' + target.id) history.pushState(null, '', '#' + target.id);
    // Meeting navigation skips long 3D transitions and lands on the actual content.
    goTo('#' + target.id, true);
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    update();
  }
  function update() {
    scheduled = false;
    const line = header.getBoundingClientRect().bottom + 32;
    let index = -1;
    targets.forEach((target, i) => { if (target.getBoundingClientRect().top <= line) index = i; });
    if (index !== active) {
      active = index;
      links.forEach((link, i) => {
        link.classList.toggle('on', i === active);
        if (i === active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      const link = links[active];
      if (link) nav.scrollTo({ left: link.offsetLeft - nav.offsetLeft - nav.clientWidth / 2 + link.offsetWidth / 2, behavior: 'auto' });
    }
    prev.disabled = active <= 0;
    next.disabled = active === targets.length - 1;
  }
  function queue() { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }
  const resize = new ResizeObserver(() => {
    document.documentElement.style.setProperty('--header-height', header.offsetHeight + 'px');
    active = -2;
    queue();
  });
  resize.observe(header);
  addEventListener('scroll', queue, { passive: true });
  addEventListener('resize', queue);
  function restore() {
    const index = targets.findIndex(target => '#' + target.id === location.hash);
    if (index >= 0) visit(index, false);
    else if (!location.hash) goTo('#hero', true);
    else if (document.getElementById(location.hash.slice(1))) goTo(location.hash, true);
  }
  addEventListener('hashchange', restore);
  addEventListener('popstate', restore);
  update();
  return { restore };
}
