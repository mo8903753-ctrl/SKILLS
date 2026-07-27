---
name: crowdfunding-marketing-plan
description: >
  众筹整合营销方案生成器。为 MadSpace 团队生成完整的 Kickstarter/Indiegogo/Makuake/Zeczec 众筹产品整合营销方案。
  当用户提供产品信息（Excel/PDF/PNG/文字描述）并要求生成众筹营销方案、整合营销计划、crowdfunding marketing plan 时触发。
  也适用于：众筹推广方案、众筹投放计划、crowdfunding campaign plan、KS营销方案、IGG营销方案、众筹广告策略。
  也适用于：文案本地化、文案调整、会议文案适配——用户提供已有方案网页/文档，要求把AI翻译腔调成能开会讲的商务中文。
  即使用户只是说"帮我做个方案"或"新项目来了"并附带产品信息，也应当触发此 skill。
---

# 众筹整合营销方案生成器

MadSpace 团队内部工具。根据客户产品信息，生成完整的众筹整合营销方案，输出飞书风格 HTML + 单页 PDF。

## 平台模式选择

先判断平台/市场，再套用规则：

- **美国/海外模式**：Kickstarter、Indiegogo 或用户未指定日本/Makuake时，沿用本 Skill 原有结构、预算公式、Meta:Google=60:40、联盟/Booster/第三方社区模块、英文Slogan风格。
- **日本/Makuake模式**：用户提到 Makuake、日本、日语页面、日本众筹、日本市场时启用。日本模式必须覆盖美国模式中的不适用内容，尤其是 deposit、Kickbooster、联盟、UTM 和英文营销话术。

美国模式不因日本模式新增规则而改变；日本模式只在明确日本/Makuake场景下使用。

## 方案变体 (Plan Variants)

本 Skill 支持三种方案变体。根据用户请求自动选择，无需用户显式指定。

### 首面提案 (First Meeting Proposal) — 10-12页战略论证

当对接陌生品牌方、且对方总负责人（Big Boss）在场的高规格线上会议时，不适合使用完整方案。适用于：首面/第一次线上会/初步方案/日本市场进入提案。

**四步结构：**

1. **一句话身份背书**（1页或附录）— 全球定位 + 目标市场落地能力 + 核心战绩。控制在开场2分钟内。
2. **产品本土化洞察**（全场最吸睛）— 不讲功能，只讲每个功能在目标市场"怎么讲故事"（Concept层）。用户场景解构 + 本土痛点 + 市场结构性差异。
3. **方法论代替案例炫耀** — 不堆案例数量，抽取爆款底层逻辑。对比表："传统做法 vs 我们的操盘逻辑 vs 对客户的价值"。
4. **行动路线图 + 安全边界**（给Boss的定心丸）— 冷启动排期 + 运营红线机制（每日同步、止损阈值、ROAS监控）。

**避坑要点：** 不做功能复述（品牌方比你熟）；不批评客户原有打法（说"针对日本市场建议调整"，不说"你们在美国做错了"）；不放完整29页结构。

**工作流：** 先出完整中文文案给用户过目 → 确认语气和准确性 → 再出HTML。不要在文案确认前跳到HTML阶段。

详细案例见 `references/first-meeting-proposal.md` 和 `references/japan-market-entry-proposal-example.md`。

### Campaign Page Copy & Visual Assets — 英文页面文案 + 配图Prompt

当用户需要撰写众筹页面的**实际英文文案**和**GPT配图Prompt**（而非客户提案），适用此变体。输出为单个 Markdown 文件 `{product_slug}_igg_plan_copy.md`。

**24页结构（页面文案版）：**
- 01 Cover / 02 Executive Summary / 03 Why Now / 04 Core Market Judgment
- 05 Product Positioning / 06 User Personas / 07 Consumer Insights / 08 Competitive Landscape
- 09 Core Messaging / 10 Page Structure / 11 Hero Copy / 12 Problem Copy / 13 Solution Copy
- 14 Comfort Proof / 15-17 Use Cases / 18 App & Data / 19 Trust & Team
- 20 Safety & Boundaries / 21 Perk Strategy / 22 Prelaunch Funnel / 23 Marketing Mix / 24 Timeline & Budget

**语言：** 英文（页面文案）为主，中文仅用于内部注释。

**配图规则：**
- 默认风格：premium consumer product, warm low light, cinematic, editorial
- 禁止：hospitals, doctors, glowing brains, neon, cyborg, sci-fi
- 所有Prompt统一样式关键词，附录集中列出
- Trust & Team 页只用机构Logo + 排版，禁止生成虚假人像

**Prompt模板与禁止词清单**见 `references/gpt2-prompt-templates.md`。

**硬规则：**
- 禁止医疗声称（cure/treat/therapy/medical device → help support/guide/promote）
- Safety & Boundaries 必须独立成页，不能埋在FAQ里
- Perk定价必须数学验证：目标金额 ÷ 目标台数 ≥ 均价，不允许提出无法数学达成的定价表
- 预算只列营销费用，不写净利润

### 完整整合营销方案（默认）

当用户未指定变体时，按下方"工作流程"生成完整的11大模块（美国）或12大模块（日本）方案，输出飞书风格HTML + 单页PDF。这是默认模式。

### 文案本地化适应 (Copy Adaptation)

当用户提供**已有的方案网页/文档**（如部署在 Vercel 的提案页、飞书文档、已有 PDF），要求将文案从"AI 翻译腔"适配为「能直接开会讲给甲方听的商务中文」时，触发此变体。用户典型话术："这个网站文案是 Claude 翻的，不够符合国情，帮我调一版能开会讲的。"

**不生成 HTML。只出纯文案。** 用户拿文案自己去 Claude 或其他工具做页面。

**工作流：**

1. **提取源文本** — 先用 `web_extract`，失败则用 `browser_navigate` + `browser_scroll` 多轮 + `browser_console(document.body.innerText)` 获取全部文本。详见 `references/web-text-extraction.md`。

2. **逐章重写** — 按源结构逐章输出，不改变数据、不改变章节顺序、不改变表格内容。只改写表达方式。

3. **调性标准（与 chinese-client-messaging 共享核心规则，但用于长文档场景）：**
   - **不用"第一/第二"枚举结构** — 改用"判断一、判断二"或自然段落推进
   - **"我们"替代中立汇报语态** — "我们对市场的判断分两半"而非"市场可分为两部分"
   - **减少短促断裂句** — "是空的。已被验证。"改为连贯节奏
   - **专业术语不降级** — "信噪比""品类定义权""U形曲线"照用，但用口语化连接词串联
   - **数据保留不动** — 竞品价格、Lead 模型、KPI 数字原样保留
   - **全简体中文** — 日文零容忍（品牌 Slogan 除外）
   - **读出声检验** — 每段重写后读一遍，像真实策略总监在会议室说话才算过

4. **交付** — 直接输出全部章节的纯文案到对话中，不生成 HTML/PDF。

## 工作流程

### 第一步：收集产品信息（主动反问）

收到产品信息后，先分析已有信息，然后主动向用户反问缺失变量。分2-3轮提问，已有信息不重复问。

**必须收集的核心变量：**

1. **产品名称与品牌**（如 "DESLOC V150 Plus"）
2. **产品品类**（如智能门锁、投影仪、扫地机器人）
3. **众筹目标金额**（如 $500,000）——所有预算按此推算
4. **众筹平台**（Kickstarter / Indiegogo / Makuake / Zeczec）
5. **MSRP建议零售价**（如 $299.99）
6. **众筹定价三档**（Super Early Bird / Early Bird / KS Special）
7. **核心功能与卖点KSP**（至少3-5个）
8. **目标市场/投放地区**（默认美国+加拿大）
9. **预热期天数**（默认30天）和**众筹期天数**（默认45天）

**需进一步确认的变量：**

10. **竞品列表**——问用户是否有指定竞品，如无则联网搜索
11. **目标人群画像**——如未提供则根据品类推断
12. **套餐设计**——问用户是否需要多套餐
13. **Upsell加购包**——问用户产品是否有配件/增值服务
14. **特殊市场教育需求**——是否需要"伪命题破除"内容
15. **AOV目标**——如未提供按早鸟价估算
16. **红人礼盒**——问用户是否需要

**提问策略：** 第一轮问1-8；第二轮问9-13；第三轮问14-16。如用户上传了规格书，先提取再补问。

### 第二步：联网搜索（如需要）

使用 WebSearch 搜索：竞品价格/功能/评价、消费者常见疑虑、同品类众筹案例。

### 第三步：生成方案

读取以下参考文件后，生成完整方案。方案结构按以下优先级确定：

1. **用户提供了客户文档/飞书链接/结构大纲** → 以用户提供的结构为展示顺序，将 Skill 的完整内容穿插进去。不要让用户文档结构"打败" Skill 的完备性——是把 Skill 的内容装进用户的框架里。
2. **用户未提供结构** → 按下方默认的 11大模块（美国）或 12大模块（日本）结构生成。

参考文件：
- `references/budget-formula.md` — 预算公式和每日投广推算逻辑
- `references/community-list.md` — 24家第三方社区固定列表（美国/海外模式用，日本模式用社群&站内增长策略替代）
- `references/benchmark-data.md` — 行业Benchmark指标
- `references/plan-template.md` — 完整模板和KOL/Landing Page/风险等框架
- `references/makuake-preheat-leads.md` — 日本Makuake预热期Email收集效率提升策略（从20%到60-80%）

**美国/海外模式 11大模块结构：**

1. **项目顶层策略**：目标KPI、人群画像、USP、市场定位（竞品对比矩阵）、营销费用预估表
2. **产品解读 & 沟通点拆解**：用户洞察（三圈层）、产品定位（Slogan中英文）、卖点Storytelling（3大故事线）、五大核心卖点排序、海外传播话术、渠道沟通点
3. **整合营销策略**：渠道分层表（7渠道）、三阶段打法（冷启动→放量→冲刺）
4. **红人 & 媒体策略**：KOL矩阵（4层级）、平台选择、媒体合作、红人礼盒
5. **广告策略**：平台选择、投放结构、素材策略、每日投广计划表（Meta+Google）、测试人群、Benchmark
6. **联盟 & Booster 策略**：联盟平台、Beta Tester、第三方社区（固定列表）、FB群组
7. **产品组合 & 定价**：套餐设计、阶梯定价、Upsell、礼品规划
8. **落地页结构**：11-Section架构、页面要素
9. **时间节奏 & Timeline**：8阶段时间表
10. **成功保障**：风险识别与应对、加速方案、成功Benchmark
11. **执行清单 & 交付件**：供应商物料、营销方交付成果

### 日本/Makuake模式结构

使用 12 个模块，保持飞书风格 HTML + 单页 PDF：

1. **项目顶层策略**：目标GMV、固定预算、周期、预热/上线拆分、ROI、竞品对比
2. **产品解读 & 沟通点拆解**：产品定位、日语Slogan、用户圈层、卖点优先级、日语叙事主线
3. **内容策略 & 传播体系**：核心叙事框架、内容支柱、渠道内容规划、EDM/LINE培育、日语文案示例
4. **整合营销策略**：Makuake站内、官方推播、Meta/Instagram、Google/PMAX、YouTube/KOL、PR/媒体、X/LINE/社群、线下展示、阶段打法
5. **红人 & 媒体策略**：头部KOL、中腰部KOL、小型KOL/KOC、PR TIMES、媒体测评、体验会；不把机动池作为KOL层级
6. **广告策略**：预算结构、预热广告排期、上线期广告排期（只写MS部分）、首轮测试人群、素材矩阵
7. **日本本地社群 & 站内增长策略**：Makuake站内增长、LINE私域、X/Twitter话题、日本ガジェット社群、测试体验官
8. **产品组合 & 定价**：早割、超早割、Makuake限定价、25% OFF、套餐/AOV策略
9. **落地页结构**：Makuake/预热页11段落架构、FAQ、日语客服/配送/隐私说明
10. **时间节奏 & 时间线**：预热30天、上线54天，或按用户文件给出的周期
11. **成功保障**：风险识别、决策阈值、加速方案
12. **执行清单 & 交付件**：品牌方物料、营销方日报/周报/结案复盘

### 第四步：输出文件

生成飞书风格 HTML 文件（带目录、表格、色块），并转为单页 PDF。两种平台模式都必须同时输出 HTML 和单页 PDF。输出到用户工作目录。

日本/Makuake模式下，每个大章节标题区都要带 MadSpace logo；如用户另给品牌或团队logo，优先使用用户提供的logo。

## 数据计算规则

所有数字通过公式计算，不允许编造：

### 美国/海外模式总营销预算分配

以众筹目标为基数：
- 预热广告 = 目标 × 4.4%
- 上线广告 = 目标 × 8.72%
- KOL合作 = 目标 × 2.4%
- 媒体新闻稿 = 目标 × 0.4%
- 众筹社群 = 目标 × 1.44%
- 其他工具 = 目标 × 0.3%
- 抽奖奖品 = 目标 × 0.3%
- 合计 ≈ 目标 × 17.96%

**每日投广计划必须满足：**
- Meta : Google = 60 : 40
- 各周之和 = 阶段总预算
- 每日之和 = 所属周预算
- 预热期 Leads = 预算 ÷ CPL（$3-$5）
- 众筹期订单 = UV × 转化率 × AOV

详细公式见 `references/budget-formula.md`。

### 日本/Makuake模式变量与预算规则

日本/Makuake模式必须先判断变量来源，再生成预算表。把变量分成两层：

1. **默认变量**：用户未给预算或比例时，仍使用美国/海外模式的通用预算公式。日本模式不自动把总预算改成30%、$300,000或其他固定数。
2. **客户显式覆盖变量**：用户明确给出预算、比例、周期、广告拆分或客户方要求时，只作为当前项目覆盖项使用，不沉淀为默认公式。

预算优先级：**用户明确给出的预算 > 用户给出的比例 > 用户上传的测算表 > 通用默认公式**。如果用户说"总预算固定"，所有费用项必须在该总额内重排，不得为了表格项、工具费、PR TIMES、线下体验或执行费额外加总。

⚠️ **测算表陷阱**：用户上传的 ROI/投入产出测算表（通常是 Excel）里的数字是最终权威，必须逐单元格提取使用。测算表内的 per-unit 百分比（如 "预热广告 6%"、"众筹投放 9%"）、汇率、一次性费用、佣金比例会与 Skill 默认公式完全不同。不要用 Skill 的 17.96% 默认公式去覆盖测算表数字。提取测算表后，先在对话中确认关键数字再生成方案。

固定预算处理：

- 若客户明确给出"营销费比30%、广告16.2%、KOL 10%、PR 3.8%"等口径，仅作为该项目的客户预算覆盖项
- 若客户明确给出固定总预算，例如 `$300,000`，则广告、KOL、PR、工具、线下等费用必须共同落在该总额内
- PR专项费可包含 PR TIMES、媒体测评、线下体验、EDM/页面/数据看板等执行费用；固定总预算场景下不要把这些费用再额外加到总预算中
- 若平台费和服务商抽成用于ROI测算，写"预估ROI"，不要写成内部敏感口径；交付版不要出现"内部话术""以某抽成为例"等说明

日本/Makuake广告拆分变量：

- 预热期默认30天，上线期默认54天；如用户提供时间表，以用户文件或口头说明为准
- 广告总预算默认按预热40%、上线60%拆分，除非用户明确给出不同拆分
- 预热期广告：Meta/Instagram 70%，Google/PMAX 30%
- 上线后广告预算原则：70%给 Makuake 官方推播，30%由 MS 执行
- MS上线投广内部：Meta/Instagram 70%，Google/PMAX 30%
- 上线期广告排期表只写 **MS执行部分**；Makuake官方推播出现在预算结构和渠道分层表中，不进入MS排期表
- 可备注：上线后可以由 MS 与 Makuake 一同投放
- 首轮测试人群如用户提供截图/表格，直接采用用户给出的 audience/keyword；不要泛化成美国众筹人群

日本/Makuake广告预算表必须至少输出两张：

1. **广告用块表**：列出 Meta/Instagram预热推广、Google/PMAX预热推广、Makuake官方推播、MadSpace上线投广、MS上线Meta/Instagram、MS上线Google/PMAX、广告合计，并写出计算逻辑。
2. **广告策略预算结构表**：按预热30天、上线54天、合计三行展示总广告预算、Makuake官方推播、MS执行Meta、MS执行Google/PMAX和目标。

若用户给出以下覆盖口径，按此模板计算，但不要把金额写成默认值：

| 变量 | 计算逻辑 |
|---|---|
| 广告总预算 | 用户给定或公式计算 |
| 预热广告 | 广告总预算 × 40% |
| 上线广告 | 广告总预算 × 60% |
| 预热 Meta/Instagram | 预热广告 × 70% |
| 预热 Google/PMAX | 预热广告 × 30% |
| 上线 Makuake官方推播 | 上线广告 × 70% |
| 上线 MadSpace投广 | 上线广告 × 30% |
| MS上线 Meta/Instagram | MS上线投广 × 70% |
| MS上线 Google/PMAX | MS上线投广 × 30% |

日本/Makuake内容节奏变量：

EDM / LINE 培育序列默认按以下顺序输出；不要改成高频预热邮件：

| 顺序 | 节点 | 主题逻辑 |
|---|---|---|
| 1 | T-30 | 初回案内 / 早割通知说明 |
| 2 | T-1 | 上线前提醒 |
| 3 | D-0 | Makuake上线 |
| 4 | D1-D7 | 首周战报 + FAQ |
| 5 | D-8 | 功能教育：翻译和会议 |
| 6 | D-15 | 产品信任：佩戴/续航/隐私 |
| 7 | D-22 | 场景证据：KOL/媒体反馈 |
| 8 | 最后7天 | 最后机会 |

EDM / LINE 频率口径：

- 预热1封
- 上线当周2-3封
- 众筹期每周1-2封
- 倒数周3封

日本/Makuake社媒平台命名与分工：

- 日本市场里 `Facebook` 不写成 `Facebook 社群`；表头、平台分工、矩阵列名统一写 `Facebook`
- Facebook任务不要写 `VIP社群搭建` 或 `晒单扩散`，可写 `Meta广告流量承接、用户互动、意见收集、信任培养`
- `Makuake官方社群（官方LINE，X等）` 如需出现，应单独成行，责任方写 `Makuake`
- Makuake官方社群核心任务写：`日本平台高转化率用户私域传播，促进转化率，由MadSpace与平台协商沟通`

日本/Makuake阶段打法：

表标题建议写"阶段打法"，不要写"三阶段打法"后放6行。默认输出以下6段：

| 阶段 | 时间 | 目标 | 关键动作 |
|---|---|---|---|
| 预热冷启动 | T-30 至 T-23 | 验证素材和人群，建立日语信任 | 页面追踪、Meta/Google小预算测试、KOL样机寄送、PR素材包准备 |
| 逐步放量 | T-22 至 T-10 | 扩大有效素材和高意向人群，累积email/LINE/收藏 | 高胜率素材放量、KOL预告、PR预发确认、LINE/X社群持续更新 |
| 目标差额冲刺 | T-10 至 T-1 | 补齐预热目标差额，制造首日势能 | 倒计时内容、早割权益教育、再营销加码、上线前最终提醒 |
| 上线爆发 | D0-D7 | 首周完成30%-40%目标 | 全量EDM、KOL评测同步、Makuake官方推播、PR TIMES首发、Meta/Google再营销 |
| 中期优化 | D8-D40 | 稳定订单和降低CPA | 素材轮换、KOL二波、媒体专访、线下展示内容回收 |
| 尾期冲刺 | D41-D54 | 倒计时紧迫感和尾款冲刺 | 最后机会邮件、限量早鸟提醒、再营销加码、表现好KOL/媒体复投 |

平台名输出统一写 `PR TIMES`。如果用户输入 `PRTIMES`，交付版也统一改成 `PR TIMES`。

日本/Makuake KOL策略变量：

- KOL层级只保留：头部KOL / 中腰部KOL / 小型KOL/KOC
- 不把"机动池"写成KOL层级；弹性预算只放在"预算调度原则"说明里
- KOL发布后转化无明显增加时，不写"停止固定费复投，转向样机置换/分佣/KOC"
- 对应动作写：邀请KOL开放广告主权限，以KOL的主页名义投放

日本/Makuake成功保障与加速方案措辞：

- `限量赠品` 改为 `抽奖活动`
- `尾期转化提升` 改为 `保持每日增长`
- `提高套餐选择率` 改为 `提高购买意愿`

日本/Makuake营销方交付件：

- 预热前默认交付件：整合营销方案、KOL名单、PR名单、追踪表
- 不默认写"素材脚本"；如用户明确要求脚本，再单独加入

日本/Makuake禁用与替换：

- 日本市场没有 deposit：禁止出现 `deposit`、`$1 deposit`、`$1 reservation`、`订金/定金` 等表达
- `leads` 统一改为 `email`；需要私域时写 `email + LINE`
- 涉及订金权益时，改为 `25% OFF`、上线24小时限定优惠券、早割、超早割、Makuake收藏、上线通知；不合适的订金段落直接删除
- Makuake众筹禁用 `UTM` 字样；需要数据追踪时写"追踪规则""数据回收""广告后台参数""渠道标记"
- Makuake没有 Kickbooster/Booster/联盟模块：删除或替换为"日本本地社群 & 站内增长策略"
- 不写英语众筹社区备份池，不写 Kickstarter/Indiegogo 社区作为主策略
- 不假设页面已完成、已有支持者或已有deposit；除非用户明确说已经上线/已有数据
- 如果原始页面或参考资料里出现 `$1 deposit`、Kickstarter early bird、UTM、Kickbooster 等词，必须在交付版中改写为Makuake适配表达或删除

日本/Makuake语言风格（重要：国内客户优先 —— 默认全中文！）：

- **默认全中文**：除非客户明确要求日文交付，否则方案正文、策略分析、表格表头、执行清单、风险描述等全部使用中文。这是默认规则，不要主动生成日文内容。
- **日语零容忍**：只有品牌核心Slogan（如"ひとつのベルト。無限の可能性。"）、产品名称（如"フルセット"）、套餐名这类不可替换的品牌标识才可保留日语。其他一切——包括策略描述、数据解读、渠道说明、KOL描述、时间线标注——全部用中文。
- 自查问题：删掉这段日语后，品牌方还能理解策略吗？能理解就必须用中文写。
- 保留必要平台/指标术语：Meta、Google、PMAX、YouTube、KOL、KOC、PR、EDM、LINE、ROAS、CPA、CPL、AOV、GMV
- 避免英文营销框架词，改用中文对应词
- Slogan：日语口号 + 中文解读
- 包装/套餐命名可用日语

**交付前语言自查清单：**
- [ ] 全文日语占比 < 3%（极端情况：只能有Slogan和产品名）
- [ ] 所有表格表头为中文
- [ ] 所有策略描述和分析为中文
- [ ] 如客户是国内品牌方 → 全中文（只有Slogan/产品名为日语）
- [ ] 如客户明确说"出日语版" → 才可增加日文内容

日本/Makuake竞品变量：

- 用户给出Makuake竞品链接时，必须加入竞品对比矩阵
- 若竞品是新上线项目，需要联网核查最新页面数据，不要凭旧记忆写金额、支持者数或排名
- 竞品用于提炼定位、页面结构、价格带、素材方向和广告关键词；除非有真实数据，不写"已验证转化结论"

日本/Makuake交付前检查：

- 全文不得残留 `deposit`、`$1` 订金、`leads`、`UTM`、Kickbooster、Booster、联盟、英语众筹社区备份池
- **语言自查**：全文日语占比应 < 3%，仅品牌Slogan和产品名可保留。面向国内客户默认全中文交付。
- 广告预算表内各行加总必须等于广告总预算；固定总预算场景下所有费用加总必须等于客户指定总额
- 上线期广告排期只展示MS部分，Makuake官方推播只在预算结构和渠道分层中展示
- HTML和PDF都要输出，PDF为单页样式；日本/Makuake模式大章节带MadSpace logo

## 语言风格

**默认规则：面向国内品牌方客户时，全部使用中文。不要主动生成日文内容。**

这是用户明确且反复强调的规则。只有品牌核心Slogan、产品名称、套餐名这类不可替换的品牌标识才可保留日文。策略描述、数据解读、渠道说明、KOL描述、时间线标注、执行清单——全部用中文。

- 美国/海外模式：中英混合（中文为主，专业术语保留英文）。Slogan英文为主附中文解读。
- 日本/Makuake模式：**中文交付**。专业平台和指标术语保留原样（Meta、Google、PMAX、YouTube、KOL、KOC、PR、EDM、LINE、ROAS、CPA、CPL、AOV、GMV），品牌Slogan和产品名保留日文（如"ひとつのベルト。無限の可能性。"、"フルセット"）。其余全部中文。
- 用户如明确说"出日语版"或"这是给日本客户看的"，才增加日文内容。

## 自包含 HTML 交付物规范

当生成 HTML 方案作为最终交付物时，必须遵守以下规则：

### 图片处理：优先 Base64 内嵌

**绝对不要用 `file://` 绝对路径引用本地图片。** `file://` 路径仅在当前机器可用，部署到 Netlify/GitHub Pages 或分享给他人后全部断裂。部分浏览器（Safari）对 `file://` 有安全限制，本地都无法加载。

处理顺序：
1. **Logo/品牌图片**：读取为 base64 data URI 直接嵌入 `<img src="data:image/png;base64,...">`
2. **背景图**：如果图片 < 5MB，同样转为 base64 嵌入 CSS `background: url('data:...')`。如果太大，复制到 HTML 同目录用相对路径 `./cover-bg.png`
3. **SVG 图标/插图**：全部内联 `<svg>` 标签，不引用外部文件

### 封面背景 + 文字叠加模式

```css
.cover-bg{position:absolute;inset:0;z-index:0;background:url('./cover-bg.png') center/cover no-repeat}
.cover-overlay{position:absolute;inset:0;z-index:1;background:linear-gradient(160deg,rgba(245,240,232,0.35),rgba(250,248,245,0.4))}
.cover>*{position:relative;z-index:2}
```

遮罩透明度控制在 **0.3–0.4** 之间，不要让背景图过浅看不清。不要用 0.7–0.8 的遮罩。

### 浮动 Logo

Logo 固定在右上角，使用 `position:fixed; top:0.6rem; right:1rem; z-index:2000`。用内嵌 SVG 或 base64 `<img>`，不要引用外部文件。

### 部署

1. 在桌面建干净文件夹（如 `xijian-plan`），包含 `index.html` + 必要的图片文件
2. 拖到 https://app.netlify.com/drop 即得公网 URL
3. 本地测试用 `python3 -m http.server 8080`，共用 WiFi 的人可直接访问

## 预算表交付规范

面向品牌方客户时，预算表**只展示营销费用明细**（预热广告、上线广告、KOL、PR、社群、工具、奖品），不展示平台费用（KS 8% 抽成）、服务商首期/尾期服务费、总费用预估行。这些是内部运营数据，不是客户需要看到的内容。

## KPI 基准值

以下为行业标准 KPI 基准，生成方案时使用：
- 预热 CPL（邮箱成本）：$3–5
- **邮箱 → 上线转化率：1–3%**（注意：不是 8–12%，众筹行业邮箱转化率远低于电商）
- 上线期 CPA：$25–35
- **上线期 ROAS：2.5–3.5×**
- KS 页面自然转化率：1.5–2%

## SVG 常见陷阱

### viewBox 裁切

当 SVG 包含底部弧形返回路径和说明文字时，viewBox 高度必须留足余量。若内容最底部元素 y 坐标为 170，viewBox 高度至少设为 185，否则会被裁切。

### 对比表左列样式

功能对比表的左列标签（特征名称）应使用深色背景 + 白色文字（`fill="var(--charcoal)"` 底 + `fill="#FFFFFF"` 字），而非灰字浅底。这样和表头形成统一深色列，可读性显著提升。

### 渐进式动画

步骤流程图使用 CSS `@keyframes fadeIn` + 递增 `animation-delay`（每步间隔 0.4s）实现从左到右的渐进揭示效果，比一次性全部出现更有演示感。

## 竞品数据采集 (Competitor Data Extraction)

### Kickstarter 页面抓取（Wayback Machine 方案）

Kickstarter 页面被 Cloudflare 保护，大部分编程式访问会被拦截。当已知 KS 页面 URL 时，使用 Wayback Machine 获取快照：

```
https://web.archive.org/web/2025/<ks-url>
```

返回完整 HTML 快照。从 meta 标签（og:title, og:description, name="description"）和 JSON-LD 块提取产品信息。页面主体内容通过 React/JS 动态加载，静态 HTML 中不会出现——meta 标签通常是最好的可用数据源。

### KS 搜索陷阱：产品名冲突

部分产品名与 K-pop 团体（如 "Loona" = LOONA/本月少女）、名人或常见词典词重名。搜索时：
- 始终在搜索词中包含公司名：`"ProductName" "CompanyName"`
- 包含平台上下文：`Kickstarter`、`Makuake`、`Indiegogo`
- 避免使用通用搜索引擎进行名称发现；改用直接的 KS URL + Wayback Machine
- K-pop 名称冲突尤其常见——Bing/DuckDuckGo 会在产品结果之前返回粉丝站和简介

## 客户文件处理 (Client File Handling)

### 读取 .docx 和 .xlsx

客户常以 .docx 和 .xlsx 格式发送产品简介和预算表格。使用 `execute_code` + `subprocess.run()` 读取：

```python
import subprocess
# For docx:
result = subprocess.run(["python3", "-c",
    f"import docx; doc=docx.Document('{path}'); [print(p.text) for p in doc.paragraphs]"
], capture_output=True, text=True, timeout=15)
# For xlsx:
result = subprocess.run(["python3", "-c",
    f"import openpyxl; wb=openpyxl.load_workbook('{path}'); ..."
], capture_output=True, text=True, timeout=15)
```

macOS 上，客户文件常落在微信沙箱中（`~/Library/Containers/com.tencent.xinWeChat/...`）。不在 Downloads 中时，使用 `mdfind -name '关键词'` 定位。

## 输出格式

### ⚠️ 文件操作陷阱

**绝对不要用 `sed` 做中文/日文批量替换。** `sed` 的字符处理会破坏 UTF-8 编码的 CJK 文本，导致中文句子被截断、乱码或部分删除。这个问题在实际项目中发生过——一次 `sed` 命令破坏了整份 HTML 文档，导致不得不从零重写。

需要批量替换文本时，必须用 Python 脚本，使用精确字符串匹配（`str.replace()`），每次替换后验证剩余日文字符数量。

### HTML 飞书版（默认首次生成）

当用户明确要求"商业版"或"给客户看的"时，飞书文档风格不够——需要升级为以下标准：

- **浅色背景**：白色 + 暖白交替，不使用深色背景（国内客户习惯浅色文档）
- **设计语言**：参考 Notion（暖白底色、细边框、Inter字体）+ Apple（毛玻璃导航、紧凑标题、负letter-spacing）
- **必须有动效**：滚动渐入（Intersection Observer）、卡片hover上浮、KPI数字计数器、浮动装饰元素
- **必须有SVG图表**：竞品定位象限图、预算瀑布图、Email漏斗对比图、渠道整合流程图 —— 不要只放表格
- **必须有SVG图标**：每个KPI卡片配独立语义色图标（蓝/金/青/玫瑰）
- **内容完整性**：覆盖skill全部12个模块，不得为了美观删减内容
- **导航**：固定毛玻璃顶栏 + 锚点滚动高亮
- **排版**：clamp()响应式标题、双列卡片网格、交错暖白分区
- **语言**：参考上方语言风格规则。日本模式：主体中文，仅品牌口号/产品名/套餐名保留日文
- 输出到桌面 `~/Desktop/`

首次生成方案时输出飞书风格 HTML（左侧目录、黄色表头表格、浅色引用框、emoji 图标）并转为 PDF。

### 商业版（用户要求时）

当用户说"商业版本""客户提案""要好看"或对设计有明显要求时，升级为 premium HTML：

- **加载设计 Skill**：先加载 `claude-design` + `popular-web-designs`（Notion + Apple 模板）获取设计指导
- **浅色背景**：`#ffffff` + `#f7f6f4` 暖白交替（不要深色，除非用户明确要求）
- **完整内容**：包含 Skill 全部 12 个模块，不允许缩略。即使用户提供的框架只有 6 个章节，也要把所有内容穿插进去
- **SVG 图表**：至少 3 组——竞品定位象限图、Email 漏斗对比图、预算瀑布图
- **动效**：Intersection Observer 滚动渐入 + 卡片 hover 上浮 + 玻璃导航 + hero 浮动光球
- **SVG 图标**：KPI 卡片用语义色图标（蓝/金/青/红），不用 emoji
- **数字计数器**：KPI 数值从 0 滚动动画
- **排版**：Inter 字体、负 letter-spacing 标题、卡式布局

详细设计系统见 `references/html-design-standards.md`。

### PDF

两种版本都要输出 PDF。textutil 转换会丢失 CSS——优先用浏览器打印（`browser_navigate` + `window.print()`）或 weasyprint。如果环境不支持，交付 HTML 并提示用户手动打印。
