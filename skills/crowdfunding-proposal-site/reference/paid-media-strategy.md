# 投广策略模块规格（内容 + 展现形式）

> 当客户重点关注受众结构、获客成本、前测验证或欧美付费投放打法时（尤其是 Kickstarter / Indiegogo 欧美全案），在提案中独立设立「投广策略」章节（带 `data-nav="投广策略"` 直达入口）。
> 本规范包含**五个必选内容板块（Part 1–Part 5）**与**沉浸版前端展现代码**，母版 CSS / GSAP 动效已预置在 `templates/immersive-bay/`。

---

## 一、内容规范（五部分缺一不可）

整体节奏默认对接 **前测 7 天（独立预算 $5,000）→ 预热 30 天（目标 4.40%）→ 上线 45 天（目标 8.72% / 10.76%）**（若用户指定其他周期或预算，按其数值替换并重算各图表加总，确保每一张图表的日耗之和精确等于对应阶段总预算）。

### Part 1 · 每日总预算分配（必须用图表展示）
用**三组可视化柱状图**拆解全周期日耗坡度（禁止只写一段文字或只给总金额）：
1. **7 天前测逐日预算曲线（7 根柱，合计 $5,000）**
   - 节奏：`D1–D2` 冷启动测通 Landing Page 与素材分组（如 `$500/天`）→ `D3–D4` 初步淘汰与提速（`$700/天`）→ `D5–D6` 向低 CPL 组爬坡（`$850/天`）→ `D7` 收口冲刺（`$900/天`），精确加总 `= $5,000`。
2. **30 天预热分周日均预算爬坡（4 根柱，按目标 4.40% 反推）**
   - 例如 `$600K`（`$26,400`）/ `$1M`（`$44,000`）：
     - `W1（7 天）`：`$600 / $1,000` 日均
     - `W2（7 天）`：`$800 / $1,400` 日均
     - `W3（8 天）`：`$1,000 / $1,650` 日均
     - `W4（8 天）`：`$1,075 / $1,750` 日均
   - 校验：`7×W1 + 7×W2 + 8×W3 + 8×W4` 必须精确等于 30 天预热广告总预算。
3. **45 天上线期脉冲与稳态日均预算（3 根宽柱，按目标 8.72% / 10.76% 反推）**
   - 呈现「首 3 天冲榜脉冲 → 中段 38 天稳态扩量 → 收官 4 天冲刺」的 U 型投放曲线；各段天数 × 日均必须精确加总等于上线广告总预算（例如 `$600K`：`3×$2,400 + 38×$960 + 4×$2,160 = $52,320`；`$1M`：`3×$4,800 + 38×$2,000 + 4×$4,300 = $107,600`）。

### Part 2 · Landing Page + 订金 + KS Followers 各自预算分配
必须分阶段对比呈现（用分段比例条 + 右对齐金额明细）：
- **前测阶段（7 天 · $5,000）**：
  - **Landing Page：100%（$5,000）** — 全部流量聚焦 Landing Page 收集邮箱（Lead）与后置问卷（按品牌方关心的产品/价格/功能意向定制问卷题项），不开设订金页与 KS 关注分流，保证前测样本纯净。
- **预热阶段（30 天 · 4.40%）**：
  - **Landing Page（邮箱留资）：20%** — 低成本扩大邮箱池与再营销受众基础。
  - **订金页（$5 / $10 锁客）：40%** — 直锁 `Secret Reward` 高意向付款用户，保障上线首日核销。
  - **KS Followers（Coming Soon 关注）：40%** — 直投 Kickstarter 预热页沉淀 Notify 粉丝，拉高开盘平台自然推荐权重。
  - 校验：`20% + 40% + 40% = 100%`，两档金额分别核算到美元个位。

### Part 3 · 国家与平台策略
- **国家策略（北美为主）**：默认 **北美 80%（美国 70% + 加拿大 10%）**，辅以英国 8%、澳大利亚 6%、德法 6%（英语核心区合计 94%），使用横向占比条 `.mixbars` 呈现。
- **平台策略（Meta 为主）**：预热期与上线期均执行 **Meta 90% / Google 10%**；使用两张并排 SVG 双环图 `.adpies`（`.donut-svg`），图上直接标出百分比，右侧逐档写明两套目标金额及平台分工（Meta 主动种草/锁客/放量，Google 承接品牌词与高意图搜索）。

### Part 4 · 受众策略（至少六层 + 闭环再营销）
采用 **3×2 六层受众卡片网格** + 底部闭环再营销说明，**前两层固定不变，第三至六层严格结合当前产品品类展开**：
- **LAYER 01 · 核心首选（永远第一层）**：**众筹用户 + 科技人群**（Kickstarter / Indiegogo 历史科技硬件支持者、消费电子早鸟极客，承担冷启动像素校准、素材赛马与低 CPL 验证）。
- **LAYER 02 · 智能放量层**：**Advantage+ 自动化扩量**（复用第一层胜出素材与转化像素，由系统宽泛定向自动扩量）。
- **LAYER 03 · 竞品精准替代层**：直接竞品与同类软硬件关注者（结合本案竞品表填写具体品牌/工具人群）。
- **LAYER 04 · 品类核心场景/效率层**：与产品使用场景强相关的生态与工具人群（例如效率办公工具、户外运动装备、家居/创作者生态等）。
- **LAYER 05 · 核心职业/管理决策层**：目标决策与高频使用职业人群（例如企业管理、Founder/CEO/VP、专业顾问、B2B 销售、内容创作者等）。
- **LAYER 06 · 高收入/高客单消费层**：**High-Income** 消费力分层（北美家庭收入 Top 10%–25% 邮编段、商旅与高客单消费群，承接主力档与多件装加购）。
- **闭环再营销池（动态调配）**：Landing Page 访客、50%+ 视频完播、已留邮箱未付订金线索、上线加购未支付人群。

### Part 5 · 投放 Benchmark 与对应的调优 / 止损动作
使用 4 列标准数据表（`核心指标 | 基准达标区间 | 预警 / 止损线 | 对应调优与止损动作`），至少包含以下 8 项核心指标：

| 核心指标 | 默认基准达标区间 | 预警 / 止损线 | 调优与止损动作要点 |
|---|---:|---:|---|
| CPM（千次展示成本） | `$18 – $24` | `> $30` | 排查人群过窄或地域重叠，合并重叠组并切入 Advantage+ 扩池 |
| CPC（单次点击成本） | `$0.90 – $1.30` | `> $1.80` | 替换前 2 秒视觉钩子与标题对比度，从素材矩阵切换高反差风格 |
| CTR（链接点击率） | `2.3% – 2.6%` | `< 1.5%` | 上线满 48h 且消耗超 1.5× 目标 CPL 仍低于 1.5% 直接关停 |
| 落地页 CVR（留资率） | `18% – 20%` | `< 14%` | 检查移动端首屏加载、卖点顺序与表单曝光位置 |
| 单线索 CPL（邮箱成本） | `$4.0 – $5.0` | `> $8.0（48h）` | 连续 48h 高于 `$8.0` 直接关停；稳定 `< $4.0` 胜出组按 20%–30% 梯度加仓 |
| 订金转化成本（CPA） | **`≤ $100`** | **`> $100`** | 超过 `$100` 复核订金页 Secret 价锚与限时权益，关停高成本冷组、优先触达前测已互动邮箱池 |
| 频次 Frequency | `< 2.5` | `> 2.8` | 触及 `2.8` 且 CTR 下滑时轮换新视觉风格与 KOL 切片防疲劳 |
| 上线期广告 ROAS | `2.8x – 3.5x` | `< 2.0x（72h）` | 低于 `2.0x` 收紧宽泛组、暂停低转化素材，预算回流众筹科技层与再营销池 |

*(注：若涉及前测问卷，问卷题数不写死「5 题」，保持「轻量意向问卷」表述，方便按品牌方关注的测试点灵活增减题项；不主动塞入 AB 双文案测试或 1v1 深度访谈，除非客户明确要求。)*

---

## 二、展现形式规范（沉浸版 HTML + CSS + GSAP 动效）

### 1. 视觉结构与排版节奏
- 每个 Part 使用统一标题头 `.pm-hd`（左侧蓝底圆角编号胶囊 `.pm-tag` `PART 01`–`PART 05` + 衬线大标题 `<h3>` + 右侧一行结论副标 `.pm-sub`，底部分割线）。
- **Part 1**：`.daily-charts`（桌面 2 列 + 底部 1 张跨全宽 `.dchart-wide`），每根柱子顶部用等宽字体 `.val` 直接标出精确美元数，重点冲刺日/周用信号橙 `.dbar.hi`，稳态中段用深墨 `.dbar.alt`，其余用品牌蓝渐变 `.dbar`。
- **Part 2**：`.alloc-split` 左右两张对比卡（左：7 天前测 100% LP；右：30 天预热 20% / 40% / 40%），每张卡顶部一条 `40px` 高的三色分段比例条 `.alloc-bar`（蓝 `.s-lp` / 墨 `.s-dep` / 橙 `.s-ks`），下方 `.alloc-list` 左侧竖排「加粗名称 + 灰色说明」，右侧等宽数字金额对齐不换行。
- **Part 3**：复用母版 `.mixbars` 横向国家条 + `.adpies` 并排双 `.donut-svg` 环形图。
- **Part 4**：`.aud-tiers` 固定 `repeat(3, minmax(0, 1fr))` 组成工整的 **3×2 六卡矩阵**（LAYER 01 与 LAYER 02 使用 `.primary` 蓝框与实心蓝徽章突出优先级），移动端自动降为单列。
- **Part 5**：复用母版 `.tbw > table.dt`，CPL 行用 `.main` 蓝左标高亮，ROAS 行用 `.total` 淡蓝底加粗收口。

### 2. HTML 结构骨架（可直接复用）
```html
<div class="wrap" id="c07" data-nav="投广策略">
  <div class="ch-head">
    <div><div class="eyebrow"><b>PART 04</b>07 / Paid Media Strategy</div><h2 class="chname sp">投广策略</h2></div>
    <div class="bignum" aria-hidden="true">07</div>
  </div>
  <p class="lede rv">整体投放按 <span class="mk">7 天前测（$5,000）→ 30 天预热（4.40%）→ 45 天上线（8.72% / 10.76%）</span> 推进，分五个执行维度落地。</p>

  <!-- PART 01: 每日总预算分配 -->
  <div class="pm-part">
    <div class="pm-hd"><span class="pm-tag">PART 01</span><h3>每日总预算分配</h3><span class="pm-sub">冷启动测通 → 胜出放量 → 节点脉冲</span></div>
    <div class="daily-charts">
      <div class="dchart rv">
        <div class="dchart-top"><h4>7 天前测 · 每日预算曲线</h4><span class="dtot">合计 $5,000 · 100% 投 Landing Page</span></div>
        <div class="dchart-bars c7">
          <div class="dbar"><div class="fill" style="height:56%"><span class="val">$500</span></div></div>
          <!-- D2..D7 -->
        </div>
        <div class="dchart-xl c7"><span>D1</span><span>D2</span><span>D3</span><span>D4</span><span>D5</span><span>D6</span><span>D7</span></div>
      </div>
      <div class="dchart rv">
        <div class="dchart-top"><h4>30 天预热 · 分周日均预算爬坡</h4><span class="dtot">$26,400 / $44,000</span></div>
        <div class="dchart-bars c4"><!-- W1..W4 --></div>
        <div class="dchart-xl c4"><span>W1（7天）</span><span>W2（7天）</span><span>W3（8天）</span><span>W4（8天）</span></div>
      </div>
      <div class="dchart dchart-wide rv">
        <div class="dchart-top"><h4>45 天上线期 · 脉冲与稳态日均预算</h4><span class="dtot">$52,320 / $107,600</span></div>
        <div class="dchart-bars c3"><!-- D1-3 / D4-41 / D42-45 --></div>
        <div class="dchart-xl c3"><span>首 3 天冲榜</span><span>中段 38 天稳态</span><span>收官 4 天冲刺</span></div>
      </div>
    </div>
  </div>

  <!-- PART 02: Landing Page + 订金 + KS Followers -->
  <div class="pm-part">
    <div class="pm-hd"><span class="pm-tag">PART 02</span><h3>Landing Page + 订金 + KS Followers 预算分配</h3><span class="pm-sub">前测 100% LP · 预热 20% / 40% / 40%</span></div>
    <div class="alloc-split">
      <div class="alloc-card rv">
        <h4>7 天前测阶段 <span>预算 $5,000</span></h4>
        <div class="alloc-bar"><i class="s-lp" style="width:100%">Landing Page 100% · $5,000</i></div>
        <ul class="alloc-list">
          <li><div><b>Landing Page（邮箱 + 问卷）</b><span>全额聚焦收集邮箱与品牌方意向问卷</span></div><b>100% · $5,000</b></li>
          <li><div><b>订金页（$5 / $10）</b><span>前测暂不开设</span></div><b>0% · $0</b></li>
          <li><div><b>KS Followers（Coming Soon）</b><span>前测不分散流量</span></div><b>0% · $0</b></li>
        </ul>
      </div>
      <div class="alloc-card rv">
        <h4>30 天预热阶段 <span>$26,400 / $44,000</span></h4>
        <div class="alloc-bar"><i class="s-lp" style="width:20%">LP 20%</i><i class="s-dep" style="width:40%">订金 40%</i><i class="s-ks" style="width:40%">KS Followers 40%</i></div>
        <ul class="alloc-list">
          <li><div><b>Landing Page 邮箱留资 · 20%</b><span>扩大邮箱基数与再营销池</span></div><b>$5,280 / $8,800</b></li>
          <li><div><b>$5 / $10 订金页锁客 · 40%</b><span>直锁 Secret 资格保障首日核销</span></div><b>$10,560 / $17,600</b></li>
          <li><div><b>KS Followers 站内关注 · 40%</b><span>拉高开盘站内推荐权重</span></div><b>$10,560 / $17,600</b></li>
        </ul>
      </div>
    </div>
  </div>

  <!-- PART 03: 国家与平台策略（.mixbars + .adpies）-->
  <!-- PART 04: 受众策略（.aud-tiers 6 张 .aud-tier 卡）-->
  <!-- PART 05: 投放 Benchmark 与调优 / 止损动作（.tbw > table.dt）-->
</div>
```

### 3. 核心 CSS 与 GSAP 动效（已同步至 `templates/immersive-bay/`）
- CSS 样式位于 `templates/immersive-bay/assets/css/site.css` 末尾（`.pm-part`、`.daily-charts`、`.dchart-bars`、`.alloc-split`、`.alloc-bar`、`.aud-tiers`），保证全站最小字号 `>= 14px`、平板/手机自动单列、零横向溢出。
- GSAP ScrollTrigger 入场动效位于 `templates/immersive-bay/assets/js/app.js` 的 `initScrollMotion()`：
  ```js
  $$('.dchart-bars').forEach(ch => gsap.from($$('.fill', ch), { scaleY: 0, duration: 0.9, ease: 'expo.out', stagger: 0.06, scrollTrigger: { trigger: ch, start: 'top 84%', once: true } }));
  $$('.alloc-bar').forEach(ab => gsap.from($$('i', ab), { scaleX: 0, transformOrigin: 'left', duration: 0.9, ease: 'expo.out', stagger: 0.08, scrollTrigger: { trigger: ab, start: 'top 85%', once: true } }));
  ```

### 4. QA 核对项
- [ ] Part 1 三张柱状图每一组日耗之和与对应阶段总预算（前测 / 预热 / 上线）精确相等，且实测柱体 `.fill` 高度不为 0。
- [ ] Part 2 前测 `100% LP`，预热严格 `20% LP + 40% 订金 + 40% KS Followers` 且加总等于 30 天预热广告额。
- [ ] Part 3 国家以北美为主（80%）、平台以 Meta 为主（Meta 90% / Google 10%），双环图显示明确比例。
- [ ] Part 4 至少 6 层受众卡片，Layer 1 为「众筹用户 + 科技」，Layer 2 为「Advantage+」，Layer 3–6 紧扣本案产品品类（竞品/效率/管理/High-Income 等）。
- [ ] Part 5 基准表含订金 CPA（默认 `≤ $100`）、CPL、CTR、CVR、CPM、CPC、频次与 ROAS 八项及具体止损动作。
