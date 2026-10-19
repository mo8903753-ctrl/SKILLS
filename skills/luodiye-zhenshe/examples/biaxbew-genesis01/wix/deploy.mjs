// Deploy the Wix build of the Genesis01 landing page to the production biaXbew home page.
// Run:  python3 wix/build_wix.py && ego-browser nodejs < wix/deploy.mjs
// Needs: Ego Lite signed in to the Wix account. Opens the editor, uploads any new images to the site's
// media library, writes the bundle into the site's code files, and clicks Publish (publishes the WHOLE site).
const fs = await import("node:fs/promises"); const path = await import("node:path");
const ROOT = process.env.GX_ROOT || process.cwd();          // run from the biaxbew-landing folder
const MAPF = ROOT + "/wix/media-map.production.json";
const EDITOR = "https://w95182-website-153.editor.wix.com/html/editor/web/renderer/edit/e93701cd-75dc-4b40-a798-43c6c1b150d8?metaSiteId=c88dbc40-682a-4166-b4d3-12c2a4329ca9";
const PUBLISH = process.env.NO_PUBLISH ? false : true;

const task = await taskSpace("biaxbew production deploy");
const page = task.page("p1");
try { await page.goto(EDITOR); } catch (e) {}
await page.waitForFunction(() => { const f = document.getElementById("preview"); return !!(f && f.contentWindow && f.contentWindow.documentServices); }, undefined, { timeout: 90000 });
await page.waitForTimeout(6000);

// 1) images that are not in the media map yet (delete a key from the map to force a re-upload)
const inst = await page.evaluate(() => document.getElementById("preview").contentWindow.documentServices.wixCode.getClientSpec().instance);
const H = { "Content-Type": "application/json", "Authorization": inst };
const map = JSON.parse(await fs.readFile(MAPF, "utf8"));
async function walk(d) { let out = []; for (const e of await fs.readdir(d, { withFileTypes: true })) { if (e.name.startsWith(".")) continue; const p = path.join(d, e.name); if (e.isDirectory()) out = out.concat(await walk(p)); else out.push(p); } return out; }
let uploaded = 0;
for (const f of (await walk(ROOT + "/assets")).filter((f) => /\.(webp|png|jpg)$/.test(f))) {
  const rel = path.relative(ROOT + "/assets", f); if (map[rel]) continue;
  const mime = f.endsWith(".png") ? "image/png" : f.endsWith(".jpg") ? "image/jpeg" : "image/webp";
  const name = "gx-" + rel.replace(/[\/@]/g, "-").replace(/\.(\w+)$/, "-" + Date.now().toString(36) + ".$1");
  const g = await fetch("https://www.wixapis.com/site-media/v1/files/generate-upload-url", { method: "POST", headers: H, body: JSON.stringify({ mimeType: mime, fileName: name, parentFolderId: map.__folder }) });
  const { uploadUrl } = await g.json();
  const u = await fetch(uploadUrl + "?filename=" + encodeURIComponent(name), { method: "PUT", headers: { "Content-Type": mime }, body: await fs.readFile(f) });
  const j = await u.json(); if (!(j.file && j.file.url)) throw new Error("upload failed: " + rel);
  map[rel] = j.file.url; uploaded++;
}
await fs.writeFile(MAPF, JSON.stringify(map, null, 1));
console.log("images uploaded:", uploaded, uploaded ? "→ re-run build_wix.py so the bundle picks up the new URLs, then deploy again" : "");
if (uploaded) { await task.finish({ keep: [] }); process.exit(0); }

// 2) bundle → site code file
const code = await fs.readFile(ROOT + "/wix/dist-production/gx-genesis.js", "utf8");
await page.evaluate(async (code) => { const ds = document.getElementById("preview").contentWindow.documentServices; const f = ds.wixCode.fileSystem; await f.writeFile(f.getVirtualDescriptor("public/custom-elements/gx-genesis.js", false), code); await f.flush(); }, code);
console.log("bundle written:", Math.round(code.length / 1024), "KB");

// 3) publish (whole site)
if (PUBLISH) {
  await page.waitForTimeout(3500);
  try { await page.click('text="取消"'); } catch (e) {}          // a "edit mobile site" dialog sometimes covers the button
  await page.click('text="發佈"');
  await page.waitForTimeout(15000);
  console.log(/已發佈並上線/.test(await page.snapshot()) ? "published" : "PUBLISH NOT CONFIRMED — check the editor");
  try { await page.click('text="已完成"'); } catch (e) {}
}
await task.finish({ keep: [] });
