# 正面提示词（Positive Prompts）

给其他模型直接粘贴。英文为执行版本，中文为对照。  
搭配 `negative-prompts.md` 一起贴；先贴本文件的「MASTER PROMPT」，再贴反面清单。

---

## MASTER PROMPT (EN) — paste first

```
You are building a crowdfunding pre-launch landing page that must feel like an award-winning product site (Apple product pages, Lando Norris, Lusion). The reference implementation is examples/sweetmyo-gen2-v4/ — read src/template.js, src/element.js and src/styles.css BEFORE designing anything. Match its level of motion, scale and restraint; do not copy its content.

PRINCIPLES
1. One scene = one idea = one full-screen takeover. Each scene is a tall wrapper (240–420vh) with a position:sticky 100svh stage; scroll progress drives the scene.
2. Big type, big imagery, few words. Headline <= 8 words, one paragraph <= 35 words, <= 3 spec numbers. Whole page <= 5,000 visible characters.
3. Zero lines and boxes. Separate with space, scale, colour fields and full-bleed media.
4. Every scene proves its sentence with real media (client footage / official photos / generated or Blender-rendered product art) or a data visualisation driven by a real parameter.
5. Motion is the product demo. Use at least 8 different scroll primitives, at least 6 pinned scenes, never the same primitive in adjacent scenes. Reproduce 100% of the reference page's motion first, then add at least 2 new primitives of your own that serve a selling point.

TYPE
- Pick ONE approved set (default: Inter Tight 600 + Instrument Serif Italic + JetBrains Mono 500).
- Headline: weight 600, letter-spacing -0.04 to -0.05em, line-height 0.9–1.0, size clamp(38px,5.4vw,88px); hero clamp(52px,9.4vw,156px).
- Emphasise 1–3 key words per headline in the serif italic (1.06–1.08em).
- Body 16–17px; lead clamp(17px,1.3vw,20px); number captions 13px sans; footnotes 12px (the floor). Nothing below 12px.
- Giant numbers (clamp(96px,12vw,210px)) for the key claim, with count-up on scroll.

COLOUR
- Extract the palette from the brand's own film/site. Max 3 background colours, switched only at scene boundaries; nav inverts automatically.
- Accent colour on at most 2 elements per viewport; one full accent-coloured scene at most.
- Text = near-black or near-white (60–75% opacity for secondary). No grey text.
- Never recolour the product.

LAYOUT
- Content sits at opposite ends of the screen (title top-left, number/media bottom-right, or left text / right media). Text column <= 560px.
- Every scene has a primary visual >= 40% of the viewport.
- Hero: either (A) full-screen real video whose scroll shrinks into a capsule window inside the headline, or (B) a large still (>=60% viewport) with scroll-linked motion (scale-in, clip-path reveal, layered parallax, part pull-out). Always: headline, one sentence, email form, 3–4 count-up spec numbers.
- Three Wix form slots only: hero, mid-page banner, final CTA. Pill-shaped, 560–620px wide on desktop, full width minus 40px on mobile. Do NOT put the form slot inside a sticky container.

MOTION ENGINE
- Own rect-based progress per scene with per-scene smoothing (k = .14–.18). position:sticky for pinning. Lenis lerp .1 (off inside Wix). GSAP only for small tweens. No ScrollTrigger pin:true.
- Videos: forward only, muted, >= 4.5 s per clip, poster set, paused off-screen via IntersectionObserver. Scrub videos encoded with -g 2.
- Glows are pre-rendered PNGs. No backdrop-filter, no runtime blur.

PROCESS (mandatory, in order)
1. Record the reference page's scroll motion at 20 fixed scroll points and write the MOTION TABLE (scene / trigger / property changed / duration / selling point). Show it to the user.
2. Write the SCENE PLAN (per scene: headline, hero visual, motion primitive, asset file, word count). Get user confirmation.
3. Prepare assets (crop to slot ratio, no watermark, one use per shot).
4. Build.
5. Run scripts/qa/page-metrics.mjs (must print GATE: PASS) and scripts/qa/scroll-shots.mjs; review every screenshot at 1440 and 390 widths; fix and repeat.
6. Deliver: overview screenshot sheet, list of non-verbatim copy, list of unverified items (live Wix, real form submit, real devices).
```

---

## 中文对照

你要做的是一个众筹预热落地页，要达到获奖级产品站的质感（苹果产品页、Lando Norris、Lusion）。**参考实现**在 `examples/sweetmyo-gen2-v4/`，设计前**必须先读**它的 `template.js`、`element.js`、`styles.css`：动效量级、尺度和克制程度向它看齐，但不抄内容。

**原则**
1. 一屏 = 一个想法 = 一次整屏接管。每个场景是 240–420vh 的外层 + `position: sticky` 的 100svh 舞台，由滚动进度驱动。
2. 大字、大画面、少文字：标题 ≤8 词、段落 ≤35 词、规格数字 ≤3 个；全页 ≤5,000 字符。
3. 没有线框；用留白、尺寸、色块、整屏媒体分隔。
4. 每屏用真实素材（客户视频 / 官方图 / 基于产品生成或 Blender 渲染）或由真实参数驱动的数据可视化来证明这一句文案。
5. 动效就是产品演示：≥8 种不同滚动原语、≥6 个钉住场景、相邻不重复；先 100% 还原参考页动效，再额外加 ≥2 种服务卖点的新原语。

**字体**：四套白名单选一套（默认 Inter Tight 600 + Instrument Serif 斜体 + JetBrains Mono 500）。标题字重 600、字距 −0.04~−0.05em、行高 0.9–1.0；每个标题强调 1–3 个关键词用衬线斜体。正文 16–17px，数字说明 13px，脚注 12px（地板）。关键数字用超大号并随滚动计数。

**配色**：从品牌方自己的视频/官网提取；背景最多 3 种，仅在场景边界切换，导航自动反色；点缀色每个画面 ≤2 个元素；文字只用近黑/近白（次要文字 60–75% 透明度），不用灰；不改产品颜色。

**版面**：内容分布在对角两端，文字栏 ≤560px；每屏主视觉 ≥视口 40%；首屏二选一：(A) 全屏真实视频，向下滚动时收缩成标题里的胶囊；(B) 大静图（≥60% 视口）+ 滚动联动（缩放穿入 / clip-path 展开 / 分层视差 / 部件拉出）。首屏必须有：标题、一句话、邮箱表单、3–4 个计数规格数字。三个 Wix 表单位：首屏、中段横幅、终极 CTA；药丸形；**表单占位不得放进 sticky 容器**。

**动效引擎**：自写 rect 进度 + 每场景平滑（k=.14–.18）；`position: sticky` 钉住；Lenis lerp .1（Wix 内关闭）；GSAP 只做小动画；禁用 ScrollTrigger `pin:true`。视频只正放、静音、每段 ≥4.5s、有 poster、离屏暂停；scrub 视频 `-g 2`。光晕用预渲染 PNG。

**流程（强制，按顺序）**
1. 录下参考页 20 个固定滚动点的动效，写成**动效表**（场景 / 触发 / 变化属性 / 时长 / 对应卖点），给用户看。
2. 写**逐屏计划表**（标题 / 主视觉 / 动效原语 / 素材文件 / 字数），**用户确认后**再继续。
3. 处理素材（裁到版位比例、无水印、同镜头只用一次）。
4. 开发。
5. 跑 `page-metrics.mjs`（必须 `GATE: PASS`）和 `scroll-shots.mjs`；桌面 1440 / 手机 390 逐张看截图；修了再跑。
6. 交付：总览截图、非原文文案清单、未验证项清单（线上 Wix、真实表单提交、真机）。

---

## 单屏提示词模板（让模型逐屏写）

```
SCENE <n>: <selling point sentence, verbatim from the brief>
- Tall wrapper <240–420>vh, sticky 100svh stage.
- Primary visual: <asset file / generated / 3D / canvas>, covering >= 40% of the viewport, placed <left|right|full-bleed>.
- Motion primitive: <name from references/motion-library.md>; it must prove the sentence above. Must differ from scenes <n-1> and <n+1>.
- Text: headline "<=8 words>" (emphasise "<1–3 words>" in serif italic), one paragraph <=35 words, <=3 spec numbers with count-up.
- No borders, no labels beyond one optional eyebrow, nothing below 12px.
- Mobile: <how it simplifies>.
```

---

## 动效“拉满”的检查口诀
1. 滚一屏，能不能**不读字就懂**这个卖点？
2. 这一屏的动作，上一屏和下一屏有没有重复？
3. 画面里有没有一个**大到压得住场**的东西（数字 / 视频 / 3D / 波形）？
4. 有没有任何一块内容**挤在角落**？
5. 去掉这块文字，这一屏还成立吗？成立就删。
