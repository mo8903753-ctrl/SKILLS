// Scene-by-scene screenshots at 3 scroll-progress points per scene (0.15 / 0.5 / 0.9).
//   ego-browser nodejs < scroll-shots.mjs     (edit URL / OUT / VIEWPORTS below)
// Uses CDP Page.captureScreenshot (page.screenshot() can return blank frames with sticky scenes + Lenis).
const URL = "http://127.0.0.1:8796/index.html";
const OUT = "/tmp/luodiye-shots";
const VIEWPORTS = [["d", 1440, 900], ["m", 390, 844]];
const fs = await import("node:fs/promises");
await fs.mkdir(OUT, { recursive: true });
const entry = (await listTaskSpaces()).find((s) => s.name === "scroll-shots");
const task = entry ? await taskSpace(entry.id) : await taskSpace("scroll-shots");
const page = (await task.pages())[0] ?? (await task.adopt((await task.tabs())[0].page));
for (const [tag, w, h] of VIEWPORTS) {
  await page.goto(URL + "?s=" + Date.now(), { timeout: 45000 });
  await page.cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 500 });
  await page.waitForTimeout(3500);
  const plan = await page.evaluate(() => {
    const vh = innerHeight, out = [];
    document.querySelectorAll("section[id]").forEach((s, i) => {
      const top = s.getBoundingClientRect().top + scrollY, span = Math.max(0, s.offsetHeight - vh);
      (span < vh * 0.4 ? [0] : [0.15, 0.5, 0.9]).forEach((k) => out.push([`${String(i).padStart(2, "0")}-${s.id}-${k}`, Math.round(top + k * span)]));
    });
    out.push(["end", document.documentElement.scrollHeight - vh]);
    return out;
  });
  let n = 0;
  for (const [name, y] of plan) {
    await page.evaluate((y) => { if (window.__swLenis) window.__swLenis.scrollTo(y, { immediate: true, force: true }); window.scrollTo(0, y); }, y);
    await page.waitForTimeout(1400);
    const cap = await page.cdp("Page.captureScreenshot", { format: "jpeg", quality: 72, fromSurface: true });
    await fs.writeFile(`${OUT}/${tag}-${String(n++).padStart(2, "0")}-${name}.jpg`, Buffer.from(cap.data, "base64"));
  }
  console.log(tag, "shots:", n, "overflow:", await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]));
}
