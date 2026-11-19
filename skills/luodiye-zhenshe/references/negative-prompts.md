# 反面提示词（Negative Prompts）

给其他模型直接粘贴使用。每一条都来自真实交付物里出现过的错误（aroti.ai/deposit-new、:4180 本地版、历次客户打回）。  
英文为执行版本，中文为对照。

---

## 复制用：NEGATIVE PROMPT (EN)

```
HARD PROHIBITIONS — violating any of these means the page is rejected.

TYPOGRAPHY
- Never use fonts outside the approved four sets (Inter Tight / Instrument Sans / Archivo 700 standard width / Manrope + their paired italic serif and mono). No condensed, compressed, narrow, pixel, handwritten, sci-fi/HUD or display fonts (Anton, Bebas Neue, Mona Sans Condensed, Archivo Narrow, etc.).
- Never set letter-spacing tighter than -0.05em. Glyphs must never touch or overlap.
- Never render any text below 12px (including <sup>). No more than 5% of visible characters may be 12px or smaller.
- Never use more than 3 font families.
- Never use monospace for number captions. Monospace is only for ONE small eyebrow label per scene and countdown units.
- Never use uppercase tracking-wide micro labels as a decorative texture.

DENSITY
- Never exceed 5,000 visible characters on the page.
- Never put more than: 1 headline (<=8 words) + 1 paragraph (<=35 words) + 3 spec numbers in one scene.
- Never stack label -> title -> subtitle -> paragraph -> spec row in a single block.
- Never fill a screen with small text. If you need to add a second paragraph, split the scene or delete text. Do not shrink the font.

LINES AND BOXES
- No 1px bordered boxes, corner brackets, dashed frames, HUD overlays, outlined cards, card grids, outlined pill tags.
- No "01 / 02 / 03" decorative numbering (functional pagers like "2 / 4" are fine).
- No tab buttons that swap an image inside a frame ("Blueprint / Frame / Exploded / Detail").
- No divider lines between sections (use space, colour change, scale contrast). Thin rules only inside a spec table or footer.

LAYOUT
- Never cram a block into one corner or a narrow strip while the rest of the screen is empty.
- Never leave a scene without a primary visual covering >=40% of the viewport.
- Never use the same layout or the same motion in two adjacent scenes.
- Never make the hero a static photo with no scroll-linked motion.
- Never put the email form inside a position:sticky container (the Wix form will drift off its slot).

COLOUR
- Never use more than 3 background colours on the page, and never change them mid-section.
- Never use more than 2 accent-coloured elements in one viewport.
- Never use grey body text on dark or tinted backgrounds. Use the near-white / near-black at 60-75% opacity.
- Never recolour the product (no blue / silver / other colourways than the one the client specified).
- No cyberpunk cyan, neon multi-colour, decorative gradients, coloured dot decorations.

MOTION
- No opening loader. No fade-up-on-enter as the main motion. No full-screen noise. No backdrop-filter / glassmorphism. No runtime filter: blur(). No big drop-shadows.
- Never play a video in reverse or ping-pong. Never loop a clip shorter than 4.5 seconds without telling the client.
- Never rely on hover or click to reveal content. Everything auto-plays or follows scroll; a click may only take over for a few seconds.
- Never use ScrollTrigger pin:true (it re-parents DOM and breaks Wix form alignment). Use position:sticky.
- Never ship fewer than 8 distinct scroll motion primitives or fewer than 6 pinned scenes.

ASSETS
- Never reuse the same shot twice on the page.
- Never use hand-drawn diagrams, fake phone/app UI, stock-looking filler, or AI-looking decorative art.
- Never leave watermarks, annotation text, or production notes ("DESIGN PREVIEW", "WIX FORM", placeholder labels) in the page or media.
- Never crop with CSS object-fit as a substitute for cutting the asset to the slot ratio.
- Never cover the product with a headline, a number or a form.

COPY
- Never invent claims, numbers or labels. Every number must match the official brief (500 kcal means 500, not 462).
- Never put academic citations or disclaimers at the same visual level as a selling point.
```

---

## 中文对照（逐条）

**字体**
- 只允许四套白名单字体；禁止压缩/窄体/像素体/手写体/HUD 字体。
- 字距不得小于 −0.05em，字母不能粘连或重叠。
- 任何文字不得小于 12px（含上标）；≤12px 文字占比 ≤5%。
- 全页字体 ≤3 种。
- 等宽字只用于**每场景 1 条眉标**与倒计时单位，**不用于数字说明**。
- 不把“全大写加宽字距小标签”当作装饰质感。

**文字密度**
- 全页可见字符 ≤5,000。
- 每场景 ≤1 标题(≤8 词)+≤1 段(≤35 词)+≤3 个规格数字。
- 不在一个区块里堆「标签→标题→副标→段落→规格行」。
- 想加第二段就拆场景或删字，**不要缩字号**。

**线框**
- 禁止 1px 边框盒、角括号、虚线框、HUD 叠层、描边卡片、卡片阵列、描边标签。
- 禁止 01/02/03 装饰编号（“2 / 4”这样的功能性页码可以）。
- 禁止「点 tab 换图」。
- 禁止区块之间画分隔线；仅规格表与页脚可用细线。

**版面**
- 禁止把一个区块塞进一个角落/窄条而其余屏幕空着。
- 每屏必须有 ≥视口 40% 的主视觉。
- 相邻两屏不得同布局、同动效。
- 首屏不得是毫无滚动联动的静态图。
- **不要把邮箱表单放进 sticky 容器**（会和占位错位）。

**配色**
- 全页最多 3 种背景色，章节内部不换色。
- 一个画面里点缀色元素 ≤2。
- 深色/有色背景上不用灰字，用近白/近黑的 60–75% 透明度。
- 产品颜色以客户指定为准，禁止蓝/银等变体。
- 禁止赛博青、多色霓虹、装饰渐变、彩色圆点。

**动效**
- 禁止开场加载、以淡入上浮为主的入场、全屏噪点、毛玻璃、运行时模糊、大投影。
- 禁止倒放/往返播放视频；每段循环 ≥4.5 秒。
- 禁止必须点击/悬停才出现内容；点击只可临时接管。
- 禁止 ScrollTrigger `pin:true`，用 `position: sticky`。
- 少于 8 种滚动原语或少于 6 个钉住场景视为不合格。

**素材**
- 同一镜头全页只用一次。
- 禁止手绘示意图、仿 UI、AI 味装饰图、库存图凑数。
- 禁止残留水印、标注、制作说明文字。
- 禁止用 CSS 硬裁代替按版位比例预裁素材。
- 禁止让标题/数字/表单遮挡产品。

**文案**
- 禁止自造卖点、数字、标签；数字必须与官方一致。
- 学术引用/免责不得与卖点同级排版。

---

## 真实案例（为什么要写这些）

### 案例 1：aroti.ai/deposit-new（“HUD 说明书”）
- 123 个带边框元素：到处是 1px 框、角括号、标签小方块。
- 8,270 个可见字符，21.7% 在 ≤12px（10px、11px 等宽大写标签）。
- 0 个视频、0 个 canvas，51 张静图靠 `Blueprint / Frame / Exploded / Detail` 小按钮切换。
- 文字挤在左侧窄栏，右侧一个小框，大面积空黑。
- → 触发规则：线框、小字、字数、tab 切图、版面集中、素材。

### 案例 2：:4180 本地版（“有动效但糊/乱”）
- 超粗压缩体 + 极负字距，`DON'T MISS THE`、页脚 `SWEETMYO` 字母互相粘连。
- 深橄榄 / 米白 / 荧光 / 黑 / 灰整页跳色约 8 次。
- 能量灯被做成**蓝色**（品牌是荧光绿）；中控特写裁切过大；App 卡片文字与图片重叠。
- 数字写成 “462 KCAL”（官方 500）；页面残留 “DESIGN PREVIEW · WIX FORM”。
- 3 段横向长廊连续出现，节奏单一。
- → 触发规则：字体/字距、配色、产品色、数字一致、制作说明文字、相邻动效重复。

### 案例 3：客户历次打回（见 `feedback-log.md`）
- 白底圆角卡片阵列、手绘示意图、仿手机界面、淡入上浮、开场加载、标签+滑块切图、全屏噪点/毛玻璃、把配角（屏幕）当主角、转场残影。
