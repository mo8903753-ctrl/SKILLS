// Delivery gate for luodiye-zhenshe pages.  Run with:
//   ego-browser nodejs < page-metrics.mjs        (edit URL below or pass via sed)
// Prints JSON + PASS/FAIL per rule. A page that FAILs any HARD rule must not be delivered.
const URL = "http://127.0.0.1:8796/index.html";
const entry = (await listTaskSpaces()).find((s) => s.name === "page-metrics");
const task = entry ? await taskSpace(entry.id) : await taskSpace("page-metrics");
const page = (await task.pages())[0] ?? (await task.adopt((await task.tabs())[0].page));
const out = {};
for (const [tag, w, h] of [["desktop", 1440, 900], ["mobile", 390, 844]]) {
  await page.goto(URL + "?m=" + Date.now(), { timeout: 45000 });
  await page.cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 500 });
  await page.waitForTimeout(3500);
  out[tag] = await page.evaluate(() => {
    const fams = new Map(), sizes = new Map();
    let chars = 0, lt12 = 0, le12 = 0, mono13 = 0;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const n = walker.currentNode, t = n.textContent.trim();
      if (!t) continue;
      const el = n.parentElement;
      if (!el || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(el.tagName)) continue;
      const s = getComputedStyle(el);
      if (s.display === "none" || s.visibility === "hidden" || parseFloat(s.opacity) === 0) continue;
      const f = s.fontFamily.split(",")[0].replace(/["']/g, "").trim();
      fams.set(f, (fams.get(f) || 0) + t.length);
      const px = Math.round(parseFloat(s.fontSize));
      sizes.set(px, (sizes.get(px) || 0) + t.length);
      chars += t.length;
      if (px < 12) lt12 += t.length;
      if (px <= 12) le12 += t.length;
    }
    let borders = 0, shadows = 0, backdrop = 0, blur = 0;
    document.querySelectorAll("body *").forEach((el) => {
      const s = getComputedStyle(el);
      if (s.display === "none") return;
      if (el.closest("form, .wix-form-placeholder, .pv-form-wrap")) return;
      if (["Top", "Right", "Bottom", "Left"].some((k) => parseFloat(s["border" + k + "Width"]) > 0 && s["border" + k + "Style"] !== "none")) borders++;
      if (s.backdropFilter && s.backdropFilter !== "none") backdrop++;
      if (s.filter && s.filter.includes("blur")) blur++;
    });
    const raw = [];
    document.querySelectorAll("section, header, footer, main > div").forEach((el) => {
      const c = getComputedStyle(el).backgroundColor.match(/[\d.]+/g);
      if (!c || (c.length > 3 && parseFloat(c[3]) < 0.5)) return;
      raw.push(c.slice(0, 3).map(Number));
    });
    const bgs = []; // cluster near-identical colours (max channel delta < 14)
    raw.forEach((c) => { if (!bgs.some((b) => Math.max(...b.map((v, i) => Math.abs(v - c[i]))) < 14)) bgs.push(c); });
    const root = document.querySelector("sweetmyo-gen2-landing, [class*='-root']") || document.body;
    return {
      viewport: [innerWidth, innerHeight],
      pageHeightVh: +(document.documentElement.scrollHeight / innerHeight).toFixed(1),
      chars, fonts: [...fams].sort((a, b) => b[1] - a[1]).slice(0, 6),
      textSizes: [...sizes].sort((a, b) => a[0] - b[0]).map((x) => x.join(":")),
      charsBelow12: lt12, shareAtOrBelow12Pct: +(100 * le12 / Math.max(1, chars)).toFixed(1),
      borderedElements: borders, backdropFilterElements: backdrop, blurFilterElements: blur,
      bgColorCount: bgs.length, bgColors: bgs.map((c) => "rgb(" + c.join(",") + ")"),
      videos: document.querySelectorAll("video").length, canvases: document.querySelectorAll("canvas").length,
      images: document.querySelectorAll("img").length,
      brokenImages: [...document.images].filter((i) => i.complete && !i.naturalWidth).length,
      stickyScenes: [...document.querySelectorAll("section")].filter((s) => s.offsetHeight >= innerHeight * 2.2).length,
      horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1,
      wixSlots: document.querySelectorAll(".wix-form-placeholder").length,
    };
  });
}
const d = out.desktop, m = out.mobile;
const checks = [
  ["HARD  visible chars <= 5000", d.chars <= 5000],
  ["HARD  no text below 12px", d.charsBelow12 === 0 && m.charsBelow12 === 0],
  ["HARD  text <=12px share <= 5%", d.shareAtOrBelow12Pct <= 5],
  ["HARD  font families <= 3", d.fonts.length <= 3],
  ["HARD  bordered elements <= 6 (spec table / footer only)", d.borderedElements <= 6],
  ["HARD  zero backdrop-filter / blur filters", d.backdropFilterElements === 0 && d.blurFilterElements === 0],
  ["HARD  background colours <= 3", d.bgColorCount <= 3],
  ["HARD  videos >= 5 and canvases+videos >= 6", d.videos >= 5 && d.videos + d.canvases >= 6],
  ["HARD  pinned/tall scenes (>=2.2 vh) >= 6", d.stickyScenes >= 6],
  ["HARD  no broken images", d.brokenImages === 0 && m.brokenImages === 0],
  ["HARD  no horizontal overflow (desktop & mobile)", !d.horizontalOverflow && !m.horizontalOverflow],
  ["HARD  exactly 3 Wix form slots", d.wixSlots === 3],
];
console.log(JSON.stringify(out, null, 1));
for (const [name, ok] of checks) console.log((ok ? "PASS " : "FAIL ") + name);
console.log(checks.every((c) => c[1]) ? "GATE: PASS" : "GATE: FAIL");
