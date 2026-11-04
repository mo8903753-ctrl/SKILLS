# 时间线三件套：全案周计划表 / 周级竖向时间线 / 筹款节奏图

> 做时间线章时读本文。**默认三个模块都要有，顺序固定**：
> ① 上线 0–48h 作战窗口（速览）→ ② **全案周计划表（甘特矩阵，主模块）** → ③ 周级竖向时间线 → ④ 筹款节奏柱状图。
> ②是客户最认的形式（"表格形式最好"），源自品牌方/代理侧真实在用的「全案时间表」工作表。
>
> **活代码：`templates/immersive-bay/`（index.html 的 `#launch` / `.gwrap` / `#tl2` / `#rhythmBars`，app.js 的 `GANTT_ROWS` + `renderGantt` + `renderRhythm`）。**

---

## 1. 全案周计划表（甘特矩阵）— 主模块

### 为什么是它
客户方的项目管理语言就是这张表：**任务 × 自然周**。竖向时间线适合讲故事，甘特表适合对齐执行。两者都要，但甘特表放前面。

### 结构硬要求
- **列 = 自然周，不是相对周**。写「7 月第 3 周」不写「W1」。让品牌方能直接对到自己的日历。
- **三层表头**：阶段（筹备/预热/众筹/发货）→ 月份 → 第 N 周。用 `colspan` 合并。
- **首列 = 任务，`position:sticky;left:0`** 固定，横向滚动时不跑。
- **类别分组行**：整行深色 `--metal` 底 + 白字，`colspan` 全宽。
- **必须包含这两类**（最常被漏，也是客户最在意的）：
  - **必备前置 · 品牌方** — 只列素材授权、样机备货两项。⛔实体注册/收款账户/Meta BM 开户/平台协议这类开户注册事项不进方案（2026-07-30 拍板，与认证类内容同禁，见 content-methodology.md §5）。
  - **发货期** — 订单整理与地址收集、发货通知与生产排期。方案不能停在众筹结束。
- **关键节点用 ◆ 菱形**独立成行（预热开始 / 正式上线 / 各档期结束），不要和任务条混在一起。

### 档期变体的表达（重要）
众筹期有 30/45 两种档期时，**不要做两张表**。同一张表里：
- 短档期覆盖的周 = **实心色块**
- 长档期多出来的周 = **斜纹**（`repeating-linear-gradient(45deg, var(--gold) 0 4px, transparent 4px 8px)`）
- 底部图例说明两者

这样客户一眼看出"选 45 天多干哪两周"，比切换视图直观。

### 关键 CSS
```css
.gwrap{overflow-x:auto;border:1px solid var(--card-bd)}      /* 容器滚动，不撑破页面 */
table.gantt{border-collapse:collapse;min-width:1180px;width:100%}
table.gantt th.tk,table.gantt td.tk{position:sticky;left:0;z-index:2;min-width:290px}
table.gantt th.tk{background:var(--card)}                     /* sticky 列必须有不透明底 */
table.gantt td.tk{background:var(--bg)}
table.gantt tr.catrow td{background:var(--metal);color:#fff;position:sticky;left:0}
table.gantt td.g{width:58px;height:36px;padding:0}
/* 用 background-image 画条，不用子元素——空格子天然不占位 */
table.gantt td.g.on  {background-image:linear-gradient(var(--acc),var(--acc));   background-size:calc(100% - 8px) 13px;background-repeat:no-repeat;background-position:center}
table.gantt td.g.ext {background-image:repeating-linear-gradient(45deg,var(--gold) 0 4px,transparent 4px 8px);background-size:calc(100% - 8px) 13px;background-repeat:no-repeat;background-position:center}
@media(max-width:860px){table.gantt th.tk,table.gantt td.tk{min-width:210px;position:static}}
```
> **为什么用 `background-image` 画甘特条**：空格子不需要任何元素，也就不会出现"空 `<div>` 露出容器底色"的问题。

### 生成方式
36 条任务 × 15 列手写会出错。**用 Python 生成 tbody**，行数据写成 `(任务名, {列索引: 类型})`，`span(a,b,cls)` 生成连续区间。

---

## 2. 周级竖向时间线

skill 早就要求"筹备期与预热期各拆 4 周、众筹期拆 N 周、圆形节点必须居中"——**这是周级颗粒度，不是 3 个阶段节点**。只给「筹备期/预热期/众筹期」三段会被打回"不够详细"。

- 中轴线 `.tl2::before{left:50%;transform:translateX(-50%)}`
- 卡片左右交替（`:nth` 或生成时按奇偶给 `.l`/`.r`）
- **节点圆心必须压在轴线上**——用 `grid-template-columns:1fr 70px 1fr`，圆点放中间列 `justify-self:center`。交付前实测圆心与轴线偏移应为 0。
- 阶段标签做成居中色块药丸（`.tl2-ph`），筹备/预热/众筹分别用 accent/teal/gold。
- **每周必须写具体动作**，不是"首周冲刺"这种空话。
- 移动端：轴线移到 `left:8px`，卡片全宽，不再左右交替。

---

## 3. 筹款节奏柱状图

30 根柱模拟 daily funding 曲线。形状按档期给：
- **30 天冲刺**：首日最高 → 快速回落 → 中段平缓 → 末段陡升（U 型更极端）
- **45 天**：首峰略低、中段更长、尾段回升

下方配 3 张说明卡（首周 / 中段节奏 / 最后 72h）。

---

## 4. 档期默认值（已更新）

**默认给 30 天 / 45 天两档，不要再默认 60 天**（实测客户会直接砍掉 60 天版）。

| | 30 天 | 45 天 |
|---|---|---|
| 众筹期周数 | 4 周 | 6 周 |
| 首 72h 目标 | 40% | 35% |
| KOL 释放 | 集中，每周 4–5 条 | 分批，每周 2–3 条 |
| 上线期广告 | 总额不变、日均 +50% | 总额不变、按 45 天摊 |

**KOL 排期必须与名单容量对得上**：达人一人通常一条视频。「每周 N 条 × 持续 M 周」的总数**不得超过 KOL 矩阵里的达人总数**。这是最容易被甲方一眼算穿的自相矛盾。

---

## 5. 与其他模块的口径联动

- **0–48h 作战窗口**里的达标率（如 T+48h 30%）与**周计划表 W1**（首 72h 35–40%）是不同时间点，**递增即不矛盾**；但漏斗卡若写"48h 达标"，配文就不能写"in 72h"。
- 甘特表里「评测样机寄送」必须排在**上线前 3–5 周**（样机寄送 1–2 周 + 视频制作 2–3 周，来自代理侧实操经验）。
- **日本 Makuake 方案：评测样机在上线前 4–6 周寄出**（2026-11 Lucy 拍板），甘特条跨 2 周，周级时间线与讲稿同口径。
- 甘特表的样机数量要与 KOL 矩阵、品牌方配合清单三处一致。
