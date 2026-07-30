# Craftwork 动效交互体系(纯 CSS 克制微交互)

> 来源:2026-07-29 实地拆解 craftwork.design(Next.js + Tailwind + Radix UI,**零动效库**——无 GSAP/framer-motion/Lottie/Lenis)。
> 定位:方案站的**站点底盘交互层**。3D/滚动主角引擎照旧(SKILL.md 运动语法),但卡片、弹层、加载、hover、入场这些"站点铬件"全部换用本体系。
> 核心哲学:**动效全部交给 CSS,JS 只负责切状态**(class / data-state / hover)。opacity/transform 走合成线程,几十张大图同屏不掉帧。

## 1. 数值宪法(高级感来自"小和快",不是炫)
- 时长:**150–400ms**。提示层 150ms、hover 200–300ms、弹层 250–300ms、手风琴 400ms。
- 位移:**≤2px**;缩放:**≤1.02**;提亮:**≤20% 白色叠加**。超过这些值就俗。
- 缓动只用两条:
  - 入场/弹层:`cubic-bezier(0.16, 1, 0.3, 1)`(近 ease-out-expo,开头快结尾缓,"跟手")
  - hover/常规:`cubic-bezier(0.4, 0, 0.2, 1)`(标准 material ease)
- 循环动画只给加载态与氛围层(骨架屏 pulse 2s、渐变流光 7s),内容元素不空转。

## 2. 卡片 hover 三件套(核心配方)
```css
/* ① 白色提亮层:伪元素,不加节点 */
.card-hv{position:relative}
.card-hv::after{content:"";opacity:0;pointer-events:none;background:#fff;
  border-radius:inherit;transition:opacity .3s cubic-bezier(.4,0,.2,1);position:absolute;inset:0}
.card-hv:hover::after{opacity:.2}
/* 深色底盘用黑色提亮层 opacity:.12 反相 */

/* ② 浅阴影浮现(craftwork 原值) */
.card-hv{transition:box-shadow .3s ease-in-out}
.card-hv:hover{box-shadow:0 -1px 0 0 #2f2b431a inset, 0 1px 3px 0 #2f2b431a}

/* ③ 个别重点卡微放大(不要全部卡都放) */
.card-hv-scale{transition:transform .2s}
.card-hv-scale:hover{transform:scale(1.02)}
```
图片卡外层用 aspect-ratio 锁比例(或 padding-bottom 技法),hover 时零布局位移。

## 3. data-state 弹层动画(Radix 模式,原生可仿)
JS 只切 `data-state="open|closed"`,CSS 盯属性放动画:
```css
[data-state=open].overlay{animation:overlayShow .25s cubic-bezier(.16,1,.3,1) forwards}
[data-state=open].panel{animation:contentShow .3s cubic-bezier(.16,1,.3,1) forwards}
[data-state=closed].panel{animation:contentHide .2s cubic-bezier(.4,0,1,1) forwards}
@keyframes overlayShow{from{opacity:0}to{opacity:1}}
@keyframes contentShow{from{opacity:0}to{opacity:1}}
@keyframes contentHide{from{opacity:1}to{opacity:0}}
/* 提示/下拉:上移2px+淡入,150ms */
@keyframes slideDownAndFade{from{opacity:0;transform:translateY(-2px)}to{opacity:1;transform:translateY(0)}}
/* 手风琴:把内容高度写进 CSS 变量,纯 CSS 动画高度 */
@keyframes accordionDown{from{height:0}to{height:var(--acc-h)}}
@keyframes accordionUp{from{height:var(--acc-h)}to{height:0}}
```
用途映射:方案图谱全屏层=overlayShow/contentShow;FAQ/风险手风琴=accordionDown(JS 先量 scrollHeight 写入 `--acc-h`);导航/眉题提示=slideDownAndFade。

## 4. 加载与入场
```css
/* 骨架屏:内容未就绪先给灰块 pulse */
.skel{background:var(--card-bd);border-radius:8px;
  animation:pulse 2s cubic-bezier(.4,0,.6,1) infinite}
@keyframes pulse{50%{opacity:.5}}

/* 滚动入场:IntersectionObserver rootMargin 200px 提前触发,加 .in */
.rv{opacity:0;transform:translateY(10px);transition:opacity .5s cubic-bezier(.16,1,.3,1),transform .5s cubic-bezier(.16,1,.3,1)}
.rv.in{opacity:1;transform:none}
/* 同组子元素 transition-delay 依次 +60ms,最多 5 级 */
```

## 5. 点睛件
```css
/* 下划线"画出来":clip-path 从左往右露出(craftwork 原值 1s,方案站建议 .6s) */
.draw{animation:drawLine .6s ease-out forwards}
@keyframes drawLine{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0)}}
/* 用在:章节大标题下的 accent 短线、.mk 荧光标记入场 */

/* 渐变流光(顶部横幅/CTA 底):两道波错相扫过 */
@keyframes waveL{from{transform:translateX(-100%)}to{transform:translateX(100%)}}
/* 首次 3.5s ease-out 400ms 1 both,随后 7s ease-out infinite */
```

## 6. 硬规则
- **禁止 JS 逐帧改样式做 UI 动效**(主角引擎除外)。UI 层 JS 只允许:切 class/data-state、IntersectionObserver 加 `.in`、量高度写 CSS 变量。
- 所有 transition 属性**点名**(`opacity .3s, transform .3s`),不写裸 `all`。
- `prefers-reduced-motion: reduce` 下:入场动画直接终态、循环动画停、主角降级静帧。
- 骨架屏必须和真实内容同尺寸(aspect-ratio 同值),替换时零跳动。
- QA 加两条:① 随机抽 3 张卡 hover 前后 `getBoundingClientRect` 高宽不变(除 scale 卡);② 全文搜 `transition:all` 应为 0 处。
