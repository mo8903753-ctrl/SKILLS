# CP Series Feasibility Study — Worked Example (2026-06)

## Product Context
CP Series: male intimate wellness device with AI companion ecosystem
- Hardware: dual-motor + air-cushion grip, LED display, self-cleaning dock
- Software: Spine 2D character companion, voice cloning, AI image/video generation, real-time Vision AI sync
- Target: $500K internal goal on Kickstarter, $149.99 entry price

## Structure (11 sections, feasibility study variant)

01. Cover — video background (title above, `width:100%;height:auto` no crop)
02. 核心判断 — 3-card thesis: market validated, tiered pricing, upgrade entry
03. 市场验证 — Segai SyncOne $460K/1,400+ backers case study + 4 key signals
04. 用户洞察 — 3 resistance types (won't buy / regret / recommend) → CP solutions
05. 竞品分析 — Segai deep dive + 4-competitor matrix table
06. 差异化定位 — one-sentence position + 6 messaging claims + core diff vs table stakes
07. 定价与档位策略 — 4 AOV scenarios + 5-tier perk table (dark section)
08. 营销渠道 — 4 priority strips (YouTube → Meta+Google → 3rd-party communities → PR)
09. 执行路线 — 6-phase timeline (T-8 weeks pre-launch through post-launch ops)
10. 预算方案 — $500K × 17.96% = $89,800 single-goal budget table + explanation
11. KPI与风险 — 4 KPI stat-strip + 4 risk cards (3-line format)

## Key Design Decisions

### Video Cover
- Title block on warm-white bg ABOVE video, not overlaid
- `<video autoplay muted loop playsinline style="width:100%;height:auto;display:block">`
- No gradient overlay — user explicitly rejected overlays; `text-shadow` is preferred for any overlay text
- `max-width:none;padding:0` on cover section to override global `section` CSS

### Sensitive Product Category Handling
- NO product imagery on cover or anywhere in deck
- Community research framed generically: "海外主流用户社群调研"
- Individual subreddit/forum names omitted from client-facing text
- Channel naming: "海外垂直社群与论坛" as generic label

### Pivot: AOV套餐 → 规模优先 → 阶梯定价
The pricing strategy underwent three iterations in this session:
1. Initial: AOV bundle-centric model (套餐拉升客单)
2. Revision: Scale-first model (规模优先, $149.99 main tier, bundles auxiliary)
3. Final: Tiered pricing (阶梯定价, entry price drives volume, bundles drive AOV — both ends needed)

Each pivot required changing: subtitle, card 2, section 06 title, all 4 stat cards, perk table, strategy note, KPI AOV, KPI backers, and footnote — across ~14 locations. The frequent repivots demonstrate why global string replacements are dangerous and section-scoped replacements are essential.

### Channel Pruning
User successively deleted from channel section:
- "渠道优先级 · 按 ROI 从高到低排列" label
- "+ Discord 社群预热"
- "+ 定向行业媒体 outreach"  
- Entire "05 海外垂直社群与论坛" strip
- Meta/Google ratio changed from 60:40 to 70:30 throughout（该项目当时口径；2026-07 起现行默认 = 两阶段均 90:10，见 SKILL.md）

### Budget Simplification
Deleted from budget section:
- "以下预算仅包含纯营销费用..." disclaimer paragraph
- "营销预算 = 众筹目标 × 17.96% · 行业标准公式" label
- "17.96% 是行业标准众筹营销费比" in explanation
- "KS 平台自身贡献约 15-25% 自然流量" in explanation
- "垂直论坛" from community budget row

### Competitive Claims Softening
- "Segai没有AI伴侣生态" → "Segai已提出开放平台/虚拟亲密生态愿景；CP应强调已可演示的..."
- "免脚本AI同步" moved from core differentiator to category standard
- "No scripts needed" description changed from "直击funscript模式用户最大痛点" → "降低普通用户使用门槛"

### Logo Handling
- MadSpace logo integrated into nav bar as last flex child (Strategy A), not separate floating element
- Left-side "MadSpace" text brand removed — logo image only on right
- Old cover SVG/illustration replaced with user-provided product KV image, then replaced again with video
