# 真实产品视频 → 滚动逐帧擦洗 hero + 电影感字幕场景

做"用真实产品动画当首屏、随滚动播放"时读本文。默认仍是 SKILL.md 的浅色滚动站；本文是可选的**深色首屏底盘**。成品母版见 `viaim-conclusion-scrub.html`。

## 1. 先扒品牌方真实素材（别用程序化 3D 占位）
- **Shopify 店（store.xxx）**：`/products/handle.json` 拿全部产品图；首页 HTML 里 `<video><source src="//store.../cdn/shop/videos/c/vp/HASH/HASH.HD-1080p-*.mp4">` 是真视频（多为达人口播）。透明产品图找 `*-removebg-preview*.png` / `*_white*.png`。
- **营销 SPA（如 viaim.ai）**：首屏产品动画由前端运行时加载，静态扒不到。用 Claude_in_Chrome 打开站点 → `javascript_tool` 跑 `[...document.querySelectorAll('video')].map(v=>v.currentSrc)` 拿 OSS 直链（如 `.../video/xxx.mp4`）→ curl 下载。OSS 目录通常不可列。
- **logo**：先在本机（~/Downloads 等）或品牌站找**真 logo 透明 PNG**；浮右上角 + 淡投影、**无白底胶囊**；除非用户同意，绝不复刻 logo。

## 2. all-intra 重编码 → currentTime 擦洗才原生丝滑（关键）
图片序列帧本质有限帧、快滚会卡。真丝滑用 `<video>` + 随滚动设 `currentTime`，并把视频**每一帧都编成关键帧**（任意 seek 瞬时）：
```
ffmpeg -i in.mp4 -an -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p \
  -g 1 -keyint_min 1 -sc_threshold 0 -crf 24 -preset slow -movflags +faststart hero-scrub.mp4
```
13s / 1280×720 all-intra ≈ 4MB。静态 ffmpeg 与沙箱 SIGTRAP 见记忆 local-video-toolchain（dangerouslyDisableSandbox）。

## 3. 首屏 = 钉屏暗底 + video 擦洗
- `.hero-track{height:260-300vh}` + `.hero-sticky{position:sticky;top:0;height:100vh;background:#07080B}`；`<video id="heroVid" muted playsinline preload="auto" poster=首帧图>` object-fit:cover 铺满。
- 文案（标题/statbar）绝对定位覆盖，左侧深色渐变 veil 保可读；首屏 pose marker `data-theme="dark"`，下一章 `data-theme="light"` 翻回。
- 擦洗 JS 要点：**别只信 loadedmetadata**（preload 常抢先触发），用 `heroVid.readyState>=1 && heroVid.duration>0` 现取时长；`currentTime=p*duration` 用 seeking 守卫（seeked 后若目标已变再 seek）防排队。
- 交付是**文件夹**（index.html + assets/），不是单文件；提醒用户部署 Netlify 拖整个文件夹。

## 4. 电影感全屏字幕场景（可选：一屏大场景 + 字幕随滚动渐显、场景渐隐）
- `.cine-track{height:~320vh}` + sticky 全屏 bg 图 + scrim；多条 `.csub` 绝对居中，按滚动进度 p 分窗口交叉淡入淡出（seg<.5 淡入，否则淡出；最后一条到末段常驻）；`cine-bg` opacity 随 p→1 渐隐到近黑，最后只剩一句主张。
- 移动端降级：track 高度 auto、字幕改静态堆叠。

## 5. 所有滚动动画都要挂 scroll 事件（不能只靠 rAF）
预览器/被切走的标签里 rAF 被节流——擦洗、主题翻转、钉屏、字幕、漂浮主角都要 `addEventListener('scroll',()=>render(true),{passive:true})` 兜底；rAF 负责平滑插值，scroll 保证跟手。见 PITFALLS.md #13。
