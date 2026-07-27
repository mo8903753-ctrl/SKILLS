# 可选主题 · Patagonia 暖土色静态 deck（来自原 plan-html）

> 这是合并前 `crowdfunding-plan-html` 的设计系统与实现模板，作为本 skill 的**可选主题**保留。
> **默认仍是硅谷浅色滚动网站**（见 SKILL.md）。当用户要暖色/商业稳重/Patagonia 风，或要"自包含静态 SVG-deck（无 3D 滚动、零依赖、内联 SVG+CSS 动画+base64）"时，切到本主题。
> 本主题的产出是**单文件 HTML，零外部依赖**：CSS、SVG 插画、JS 动画、base64 图片全部内联。

---

## 1. 色板（warm earth）

```css
--charcoal:#2B2D2A;   /* 正文、暗区 */   --stone:#5C5C53;    /* 次要文字 */
--clay:#8B8178;       /* 弱文字 */        --sand:#C4B5A5;     /* 边框、弱元素 */
--cream:#F5F0E8;      /* 交替区底 */      --offwhite:#FAF8F5; /* 交替区底 */
--warmwhite:#FFFCF7;  /* 默认底 */        --accent:#C8734A;   /* 主 accent 暖铜 */
--accent-deep:#A0522D;--accent-light:#E8A87C;
--teal:#3D6B66;       --teal-light:#5C8D87;
--bg-dark:#1E1F1C;    /* 暗区 */          --negative:#C44D4D; /* 风险/警告 */
--gold:#B8956A;       --success:#3D6B66;  /* 决策树 YES 分支 */
```

## 2. 字体与排版

```css
font-family:'Segoe UI',system-ui,-apple-system,sans-serif;        /* 英文 */
/* 中文追加：'PingFang SC','Microsoft YaHei'，line-height:1.85（CJK 更高） */
h1:clamp(2rem,4.5vw,3.8rem)  h2:clamp(1.5rem,3vw,2.4rem)  h3:clamp(1.1rem,1.8vw,1.4rem)
body:16px / line-height:1.7
```

## 3. 章节结构

```html
<section id="unique-id">
  <div class="section-num">NN</div>
  <h2>Section Title</h2>
  <div class="section-divider"></div>
  <!-- content -->
</section>
```
变体：默认白底 `--warmwhite`；`.section-alt` cream 底 + 装饰圆 `::before`；`.section-dark` 暗底 + 点阵纹理 `::before`。

## 4. 标准 14 章结构

| # | Mode B（消费向英文） | Mode A（中文代理） |
|---|---|---|
|01|Cover hero + 产品 SVG + slogan|品牌名+产品名+"海外众筹出海方案"+代理名+版本|
|02|Executive Summary 大数字行+论点|项目概览（为何众筹/核心判断/数字行）|
|03|Market Opportunity 卡格+数据条|市场机会分析|
|04|Product Deep Dive 双栏+特性卡+流程图|目标市场与受众（优先级排序+4 画像卡）|
|05|Competitive 雷达/二轴+对比表+定位|竞争优势拆解（雷达+对比表+逐竞品卡）|
|06|Target Audience 4 画像卡|定价策略分析（逻辑段+价格卡+**单位经济表**）|
|07|Core Messaging（暗区）slogan+3 支柱|核心叙事框架|
|08|Perk Strategy（featured 徽章）+单位经济|回报档位设计（全档表+策略卡）|
|09|Marketing Mix 渠道卡+三阶段|营销渠道组合（横向交替条带）|
|10|Landing Page 12 编号迷你卡|着陆页结构|
|11|Budget 双档切换|营销预算方案（双档+选档卡+费效）|
|12|Timeline 6 阶段竖向|执行时间线|
|13|KPI & Risk 卡+进度条+6 风险|KPI 与风险矩阵|
|14|Asset Checklist 品牌 vs 代理|所需物料清单|

> 内容（Mode A/B 框架、定价/预算/KPI/风险方法论）见 `content-methodology.md`。本文件只管**暖土色实现**。

## 5. SVG 图表目录（内联、零依赖）

全部内联 SVG。**通用坑：viewBox 一定要比最低元素 y 多留 20-40px，否则底部文字被裁**；`style="overflow:visible"` 防扩散环被裁。

- **漏斗图**：polygon 递减宽度，4 层带标签。
- **雷达/蜘蛛图**：3 层同心五边形网格 + 各竞品数据多边形 + 顶点文字；可加 `radialGradient` 雷达扫描脉冲（两个错相半周期的扩张环）。
- **二轴竞品定位图**（B2B→消费产品比雷达更易读）：X=价格、Y=数据保护能力，竞品为带标签圆点，产品高亮在"高保护/价值价"象限，虚线四象限分隔。viewBox `0 0 360 350`，`overflow:visible`。**用二轴定位图时，删掉并排的特性对比表 SVG，竞品章改单列（`max-width:30rem;margin:0 auto`）**——对比表与下方定价锚点表重复，且 125% 易重叠。
- **特性对比表 SVG**：暗底表头白字，左列暗底块白标签，右列 accent/teal/clay 表 ✓/✗。底部注释行需 `viewBox 0 0 340 320`。
- **进度条（KPI）**：cream 背景条 + accent/teal 填充条（宽度按百分比）。
- **决策树（二叉）**：中心问题节点 + YES（左，success 绿）/ NO（右，negative 红）两分支方案卡。`viewBox 0 0 680 180`。
- **产品拆解图**：变体 A 引线标注（4-6 特性，紧凑）；变体 B 设备图 + 下方 2×4 特性网格卡（6-8 特性，datasheet 感，`viewBox 0 0 860 520`）。
- **预算漏斗（4 段收窄）**：宽度 640→520→400→300，箭头 marker 连接，左右虚线边界成漏斗形，末段 accent 底高亮结果。放在预算分析 box 之上。`viewBox 0 0 720 260`。
- **市场数据条 `<animate>`**：宽度 0→target，按 0.3s 错峰；数值标签在条结束 +0.3s 淡入。多行标签 viewBox 留到 y≈170。
- **流程图**：5 圆 + 箭头 + 虚线回环，`.step1/.step2` 错峰 fadeIn。

## 6. CSS 动画

```css
.reveal{opacity:0;animation:fadeUp .7s ease-out forwards;animation-play-state:paused}
.reveal.visible{animation-play-state:running}           /* IntersectionObserver 加 .visible */
.float{animation:float 5s ease-in-out infinite}          /* translateY ±6px */
.spin-slow{animation:spinSlow 22s linear infinite}        /* 装饰轨道 */
.pulse{animation:pulse 2s ease-in-out infinite}           /* 传感器/指示点 */
```

## 7. 卡片 & 组件

```css
.card{...}  .card.accent-left{border-left-color:var(--accent)}  /* 顶部风险边：border-top:3px solid var(--negative) */
.perk-card.featured::after{content:"★ MOST POPULAR"}
/* Mode A 专用 */
.analysis-box{background:#fff;border:1px solid var(--sand);border-radius:10px;padding:1.4rem}  /* h4 用 accent */
.price-card{border:2px solid var(--sand);border-radius:14px;text-align:center}  /* tier-name accent / tier-price 2.4rem / tier-msrp 删除线 */
.data-table thead th{background:var(--charcoal);color:#fff}  .data-table tbody tr:nth-child(even){background:var(--cream)}
.data-table .total-row td{font-weight:700;border-top:2px solid var(--accent);background:var(--cream)}
```

**视觉多样性（破卡片单调）**：`card-grid` 最多 4 章用；超出转成——横向 profile 条带（受众/特性/团队，icon 左+文右+border-bottom，不同色调 icon 底）、交替渠道条带（zebra cream 偶行，`margin:0 -1rem` 出血）、统一 stat 条（KPI，一个分栏容器代替 4 卡）。14 章分布建议：卡 3-4 章、表 3-4 章、条带 2-3 章、纯 SVG 1-2 章、时间线 1、暗区 1-2、清单 1。

## 8. 预算双档切换

切换的是**两个目标档**（默认：一般市场 $500K/$1M，美国市场 $600K/$1M），各自营销预算 = 目标 × **费率**（≤$600K 用 17.96%，$1M 用 20%；拆分见 `content-methodology.md` §1）。`.budget-panel` 用 `display` 切换，**不要藏在注释里**。按钮标两个数：`目标 $200K · 营销预算 $35,920`。每行带"公式"列 + "说明"列（Meta/Google 60:40、CPL $3-5、ROAS 2.5x）。Mode A 代理提案默认档 = **$500K/$1M**（Panel A=$500K 默认激活），不要用 $200K/$500K 作默认。

## 9. 封面图层 & 背景图（base64，关键易错点）

带背景图的 section 必须 `max-width:none;padding:0` 覆盖全局 `section{max-width:56rem}`，三层：背景层(z0) + 遮罩层(z1) + 内容层(z2)。

**左暗安全区 + 右产品展示（背景图封面必须）**：左→右暗渐变，文字全白左对齐放左侧暗区，SVG/产品放右侧亮区。
```css
/* 封面遮罩 */ background:linear-gradient(90deg, rgba(8,10,12,.78) 0%, rgba(8,10,12,.45) 42%, rgba(8,10,12,0) 72%)
```
- 文字全白：h1 `#F0F2F3`、副标题 `rgba(255,255,255,.72)`、元信息 `rgba(255,255,255,.45)`；accent 只点关键词。
- 短标语 1-2 行；元信息并入 CTA 行，不要漂浮在视觉中心。
- **禁居中文字**（像 PPT 封面）；**禁 0.5+ 均匀遮罩 / 暖白遮罩**——用户明确反馈"太灰了,文字和图片都看不清"。

**use-case 实景区**：卡放左侧暗区，**绝不压产品主体**。玻璃卡 `rgba(12,14,16,.72)` + `blur(14px)`，最多 3 卡竖排，每卡 1 句（≤2 行），用大数字 01/02/03（accent/teal/gold）不用 SVG icon。

**125% 缩放兼容（用户在 125% 测）——最低值**：
- 封面暗渐变左缘 `rgba(4,6,8,.85)`（不是 .78）；use-case 左缘 `rgba(2,4,6,.82)`（不是 .72）。
- 图上玻璃卡 `rgba(4,6,8,.82)` + `blur(18px)`；卡内正文 `rgba(255,255,255,.82)`（不是 .65）。
- SVG 圆点/标签间距 ≥20px。拿不准就砍掉封面 SVG，用单列左对齐白字暗渐变封面（永远可读）。

**视频封面**：Pattern A（无遮罩，标题在视频上方独立暖白区，`video{width:100%;height:auto;display:block}`，**禁 object-fit:cover** 会裁切）/ Pattern B（暗渐变遮罩 + 白字）。视频需 `autoplay muted loop playsinline` 四属性，文件拷到部署目录。

## 10. 浮动 Logo（Mode A）

代理提案右上角必须是 **MadSpace 代理 logo（真 PNG base64）**，不是产品 SVG 或文字块。优先 Strategy A：logo 作为 `<nav>` 最后一个 flex 子元素（无 z-index 冲突）。Strategy B 固定定位时，nav links 要 compact（font .7rem/gap .35rem/nowrap）+ logo `right:.8rem` 防重叠。Mode B 用产品/品牌 logo。

## 11. 部署 & 自检

部署：同目录放 `index.html` + `cover-bg.png`（+ 视频）；logo 转 base64；本地 `python3 -m http.server 8080`；Netlify Drop 改名 index.html。
交付前 checklist：14 章齐全编号（滚动站可压缩为 8-13 章）；预算按目标档取费率（≤$600K 用 17.96%，$1M 用 20%，非乱数）；KPI 与定价档自洽；封面左暗渐变+白字左对齐单列；预算切换两张完整表；浮 logo 全程可见；SVG 无 viewBox 裁切；125% 无重叠；图上玻璃卡 ≥0.80 不透明；KS 页禁 cure/treat/medical；spec-gap 决策闸在定价前；backer 信任风险标 medium；量化声明有来源小字。

---

## 12. 实现坑（与设计无关，两套主题通用）

### GSAP
- **`gsap.from()` 残留 transform → 卡片重叠**（125% 尤甚）：改 `fromTo({y:36,opacity:0},{y:0,opacity:1,clearProps:"transform"})`。
- **count-up 混合格式数字**（`$500K`、`~$460K`、`1,400+`）：`gsap.from({textContent:0})` 会丢前后缀。改计数对象 + 手动 prefix/num/suffix 解析；range（含 `–`）跳过。
- **删除封面元素后残留选择器**：清掉指向已删元素的 GSAP 块（`.orb-accent`、`.cover-eyebrow`），否则 console 警告。

### SVG
- **viewBox 太紧裁切**：最低元素 y 之上留 20-40px；雷达图例移到 `viewBox 0 20 340 330`；特性对比表底注 `0 0 340 320`。
- **>100% 缩放文字重叠**：行间 y 拉开 ≥18-20px，密集区字号 8-10px，用更大 viewBox（400×380 代替 340×340）。

### 编辑安全
- **禁短数字串全局替换**：`$220` 会污染 `$220–240`→`$150–170–240`。old_string 带足上下文，替换后再搜确认无级联。
- **execute_code 里禁用 hermes `read_file()` 改 HTML**：它带行号前缀（`187|content`），写回会把行号嵌进文件。用 Python 原生 `open().read()/write()`；必须用 read_file 时先 `re.sub(r'^\s*\d+\|','',html,flags=re.M)` 去前缀。

### 反模式（DO NOT）
- 禁外部字体 CDN / 外链图片 / `file://` 绝对路径（破坏离线与部署）。
- 禁把硬盘 bundle 设为默认/featured 档（Diskless + Add-On 才对）。
- 禁用国内背书（信创/国家级/中科院/政府部署数）作定价溢价。
- 禁预算写成大额平摊（"$200K total marketing"）——目标≠营销预算。
- 禁 KPI 不从定价档推导（$200K÷$999≠1,500 backers）。
- 禁把 backer 信任标低风险（中国品牌+数据存储=中风险起）。
- 禁渠道含 Reddit/HN/Twitter-X/隐私安全媒体（已删）。
- 成功页标题禁"你得到什么"，用"Campaign结束后的品牌资产"。
- 玻璃卡禁压产品主体；use-case 卡禁 SVG icon（用数字）；封面禁居中文字/过浅均匀遮罩。
- claim 软化：禁"首款"、禁"竞品需 18-24 月追平"、未确认认证降级（详见 `content-methodology.md` §10）。
