---
name: proposal-site-bd
description: BD 提案/投标全案——在 crowdfunding-proposal-site 底盘上加「完整公司介绍章 + 投标应答层 + 逐页讲稿」。当用户说"提案 / 做个提案 / 给XX出提案 / 投标文件 / 参加XX招标 / 带公司介绍的方案"时使用；纯策略方案（不带公司资质章、非投标）仍走 crowdfunding-proposal-site。
---

# proposal-site-bd · BD 提案与投标全案

## 定位

对品牌方的正式提案与投标 = **公司是谁（信任）+ 方案怎么做（能力）+ 报价（商务）**。
本 skill 管公司章、投标变体、讲稿；**页面形式与方案方法论一律沿用 `crowdfunding-proposal-site`**（母版 CSS 整段复制、模块清单、预算/定价/KPI 方法论、QA 清单），不在本 skill 重复。

## 触发判断

- 有招标文件/评分表 → 投标模式：读 `reference/bid-response.md`，章节顺序严格对表招标清单。
- 无招标、但要带公司介绍的提案 → 提案模式：按下方默认大纲(公司介绍固定两章,置于方案之后)。
- 用户只要方案不要公司章 → 转 `crowdfunding-proposal-site`。

## 默认大纲（提案模式 · 用户拍板顺序，统一照此写和改）

1. **封面** — 产品名 + 数据条(目标/预算/客单价/支持者) + 官方实拍
2. **核心判断**(重点) — 品类判断 + 胜出逻辑 + 可行性结论,提案的灵魂
3. 市场与受众 — 四类人群 + 大盘数据
4. **竞品与定价**(重点) — 竞品表(价格回源核实) + 三锚点 + 五档 Reward 阶梯 + 档位模型
5. **投放与渠道**(重点) — 两阶段配比 + 受众池规模 + 来源结构饼图 + 素材方向
6. 预热与订金 — Leads 漏斗测算
7. KOL 与媒体 — 矩阵 + 已核实预选卡
8. **时间线**(重点) — 0-48h 作战图 + 全案甘特表(客户最认的形式)
9. **公司介绍 · 两章**(方案之后、收尾之前) — 章一:简介/数字条/平台资质/授权与奖项/团队配置/服务承诺;章二:**案例证明(重点)**——协作者挂牌截图+纪录大图+案例一览+案例墙。现成实例:`reference/company-example.html`
10. 收尾页

页面叙事与视觉、单位经济、风险章、报价等模块**不在默认序列**,按项目需要增补;投标模式的顺序另按 bid-response.md 严格对表招标清单。

## 工作流

1. **读料**：`reference/company-profile.md`（公司数据唯一口径）→ 项目资料 → （投标）招标文件拆读，清单抄成 checklist。
2. **装底盘**：调 `crowdfunding-proposal-site`，按其工作流做方案章；公司章直接用 `reference/company-sections.html` 母版改参（资产用本 skill `assets/`，%%ASSET:名%% 占位）。
3. **数字口径**：company-profile.md 第 0 节的规则是硬约束（300+ 总口径 vs 61 入册清单分场景；底数+以上；美国项目数据条放美国纪录）。
4. **构建与 QA**：沿用 proposal-site 第 7-9 步（含 chinese-business-copy 润色）；投标模式加 bid-response.md 第 3 节红线扫描。
5. **交付**：网站（Vercel 干净目录单文件直发）＋按需讲稿（`reference/speech-guide.md`，七条口径规则必须过）＋盖章件清单提醒。
6. 数字有更新（案例数、纪录、团队）→ 回填 company-profile.md，本 skill 即全局生效。

## reference

- `company-profile.md` — 完整公司介绍数据册（定位/核心数字/平台资质/奖项/团队/深度案例/责任边界/案例索引）
- `madspace-cases.md` — 61 项入册案例明细 + 职责/产出清单（飞书 20260616 版全文）
- `company-sections.html` — 公司介绍 4 章 HTML 母版（简介资质/团队/案例证明/服务承诺，proposal-site 类名体系）
- `bid-response.md` — 投标变体方法论（结构对表/应答浓度/数字红线/交付物族/工程定式）
- `speech-guide.md` + `speech-sample.txt` — 逐页讲稿七条口径规则 + 用户改定样本
- `assets/` — 公司资产库（案例截图/授权证明/奖项/案例墙/logo），全部真图可核验
