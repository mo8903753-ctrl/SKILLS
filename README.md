# MadSpace Skills

MadSpace 迈思自研的众筹代运营工作流 Skills（Claude Code / Codex 通用）。

## 安装

```bash
git clone git@github.com:mo8903753-ctrl/SKILLS.git
cp -R SKILLS/skills/* ~/.claude/skills/        # Claude Code
cp -R SKILLS/skills/* ~/.codex/skills/         # Codex
```

## 目录

### 方案与提案

| Skill | 用途 |
|---|---|
| **crowdfunding-proposal-site** | 把众筹提案做成客户可直接看的滚动网站。含**三份活代码母版**：方案图谱（会议导航层）、时间线三件套（甘特表+周级时间线+节奏图）、完整成品 deck。带完整商业分析方法论（定价单位经济、预算公式、KPI 一致性、风险现实主义）。 |
| **crowdfunding-proposal-ppt** | 众筹方案 PPT 版本 |
| **crowdfunding-marketing-plan** | 众筹整合营销方案生成器 |

### 投放与内容

| Skill | 用途 |
|---|---|
| **landingpage** | 众筹预热页中英文文案生成器（从产品 Excel 出） |
| **ad-copywriting** | Meta / Google 海外广告文案（从 KSP 或预热页文案出） |
| **pretest-report-v2** | 预热投广前测报告（从 Meta 后台导出数据出）；`pretest-report` 为初版 |
| **crowdfunding-edm-image** | 图片式众筹 EDM |
| **EDM** | 众筹 EDM 文本生成（模板变量替换，一问一答收集参数） |
| **Update** | 众筹 Update 更新公告生成 |

### 达人与素材

| Skill | 用途 |
|---|---|
| **youtube-kol-finder** | YouTube KOL candidate 检索、筛选、打分、成表 |
| **shooting-brief-master** | 众筹产品拍摄需求文档（户外/消费电子），输出单页 HTML |

### 获客与沟通

| Skill | 用途 |
|---|---|
| **madspace-lead-sourcing** | 获客自动化系统：发现中国硬件品牌方线索、搭建/运行扫描器 |
| **crowdfunding-lead-generation** | KS/IGG 代运营获客：线索筛选、cron 自动扫描 |
| **chinese-business-copy** | 把机翻/英文思维的中文商务文案，改写成能在会议室逐页讲的正式版本 |
| **chinese-client-messaging** | 甲方微信/邮件短消息：排期协商、风险沟通、范围讨论 |

## 开工前必读

- `crowdfunding-proposal-site/reference/PITFALLS.md` — 30 条实战踩坑
- `crowdfunding-proposal-site/reference/content-methodology.md` — 预算 / KPI / 定价 / 风险的硬规则

## 说明

- 本仓库**不含**各 skill 的大体积素材（模板 PDF、归档 zip），只保留 SKILL.md 与 references 等逻辑部分。
- 部分 reference 母版内含真实客户方案数据，**仅限内部使用，请保持仓库 private**。
