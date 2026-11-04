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
| **crowdfunding-proposal-site** | 把众筹提案做成客户可直接看的**沉浸式 3D 滚动网站**（唯一形式，已替代原结论版 / 叙事版；3D 产品结构=章节、整屏色块切换、彩色卡片堆叠、产品自转换色 + 3D 丝带、盘位 sleeve 转场；`templates/immersive-bay/` 为可运行母版）。含**演讲稿 + 演讲者窗口**（共享屏幕对方看不到讲稿）、方案图谱、时间线三件套，以及完整商业分析方法论（定价单位经济、预算公式、KPI 一致性、日本 Makuake 多配置定价）。 |
| **crowdfunding-proposal-ppt** | 众筹方案 PPT 版本 |
| **crowdfunding-marketing-plan** | 众筹整合营销方案生成器 |

### 投放与内容

| Skill | 用途 |
|---|---|
| **ad-flywheel-impact** | 投放飞轮·震慑版（2.3-repo）：调用生图工具生成完整广告；固定 Figma 范例参考、产品与 Logo 核对、逐图质检和生成来源校验。Figma 只收纳成品，不能替代生图。 |
| **landingpage** | 众筹预热页中英文文案生成器（从产品 Excel 出） |
| **luodiye-zhenshe** | 落地页震慑版：Kickstarter / 众筹预热落地页全流程（全量盘点素材 → 按卖点查竞品动效 → GSAP 滚动交互页 → Wix 自定义元素 + 原生表单收邮箱 → 截图自检 → 发布交接），含完整案例源码。 |
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

### 投放飞轮·震慑版

调用：`执行投放飞轮·震慑版`。安装或更新后重载技能，确认加载 `2.3-repo`。实际生图/编辑工具及 ego lite、Figma 权限由本机提供；缺少生图工具时明确阻塞，不改用 Figma 拼广告。仓库只含规则、脚本与脱敏案例，不含客户原始素材或第三方技能。


## 投广素材飞轮 3.0：图片＋视频

调用“执行投放飞轮·震慑版”。获授权素材有源视频/TVC/客户成片时，同时执行 `crowdfunding-ad-video` 制作投广 MP4；图片仍必须生图工具输出完整成图。视频按原片剪辑/压字，不能只抽帧做图冒充视频；Figma仅参考与整理。更新后重载两个技能，检查ffmpeg、Python库、字体与语音模型。用户明确只做图片/只修技能或视频仅为参考时不自动剪辑。

| Skill | 用途 |
|---|---|
| `ad-flywheel-impact` | 图片与视频的统一调度、共用事实及独立验收。 |
| `crowdfunding-ad-video` | 原片审片/转写、TVC长短剪辑、逐镜竖版构图、来源可追溯压字、真实MP4与音画QA。 |
