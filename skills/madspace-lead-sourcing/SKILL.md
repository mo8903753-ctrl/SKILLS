---
name: madspace-lead-sourcing
description: >
  MadSpace 获客自动化系统。为中国硬件品牌出海众筹代运营机构发现潜在客户线索。
  触发条件：用户说"找客户"、"获客"、"线索"、"lead sourcing"、询问如何找到中国硬件品牌方、
  需要搭建/调整/运行获客扫描器、或讨论 client acquisition workflow。
  也适用于：众筹代运营获客、硬件品牌出海BD、KS/IGG 客户开发。
version: 1.0.0
---

# MadSpace 获客系统

为 MadSpace（中国硬件品牌出海众筹代运营）提供自动化 + 人工双轨获客工作流。

## 核心约束

**能自动化的：**
- 36氪 RSS → 融资硬件公司（含创始人、轮次、金额）
- 爱范儿 RSS → 硬件新品发布
- 少数派 RSS → 硬件产品评测
- Kicktraq 热榜 → KS 活跃项目监控 + 中国团队信号检测
- 对融资公司自动搜索官网/企查查/领英链接

**被反爬墙挡住的（只能用户手动）：**
- 京东众筹 / 淘宝众筹 → 品牌方已被众筹教育，是最佳线索源
- 1688 → 工厂转品牌信号
- 即刻 / 小红书 / 抖音 → 独立开发者/硬件创业
- KS/IGG Discover 页面 → Cloudflare 保护，只能人眼浏览
- Google/Bing/DuckDuckGo 直接抓取 → 全部有验证码

**关键认知：发现「还没上 KS」的中国硬件品牌，最有效的三个渠道（京东众筹、1688、即刻小红书）全部反爬。自动化只能覆盖科技媒体公开报道和 KS 竞品监控。**

## 获客管道

### 自动化管道（cron job 每周一跑）

1. **36氪融资硬件公司**（最高优先级）→ 刚拿钱 + 可能出海 + 还没上 KS
2. **爱范儿/少数派新品** → 硬件品牌媒体曝光
3. **Kicktraq 热榜** → KS 在线项目监控（参考信号，介入空间有限）

### 手动管道（用户每周必做）

- 京东众筹：扫「已结束」→ 筛 3C/智能硬件/户外 → 找国内众筹跑过的品牌
- 1688：搜原创硬件款 → 找工厂做品牌信号（有logo/品牌故事/专利）
- 即刻/小红书：搜「硬件出海」「独立开发者」→ 私信触达
- KS Discover：Coming Soon + Prelaunch → 预上线项目 = 最佳介入点

### KS 裸奔项目触达方法论（用户提供）

**认中国团队信号：** 地址露深圳/广东/杭州、HK$或¥目标、中式英文文案、3C/户外/EDC品类、评论区有中文

**判「差=好切入」：** 进度条卡住、没 Projects We Love、页面糙（无视频、渲染图粗）、头48h乏力、评论有抱怨

**找人路径：** 项目页→官网/社媒→领英找创始人；FAQ/Risks→公司名→企查查反查；产品名丢小红书/微博/抖音搜

**触达话术核心：** 不是「要不要合作」，是「我看了你XX项目，有具体问题（预热名单小/落地页差/ROI低），我们帮同品类YY做到Z万」→ 给价值、给对标、给证据

## 线索筛选打分卡

| 维度 | 权重 | 评分标准 |
|---|---|---|
| 品类匹配度 | 25 | KS上有$500K+案例(25) / 有案例但量级小(15) / 品类冷门(5) |
| 产品差异化 | 20 | 明确技术/设计护城河(20) / 有差异不明显(12) / 同质化(5) |
| 团队背景 | 15 | 连续创业者/大厂/出海经验(15) / 做过硬件(10) / 首次创业(5) |
| KS适配度 | 15 | 有视觉冲击力(15) / 偏功能可拍(10) / 吃体验不好展示(5) |
| 资金实力 | 15 | 已融资/自有工厂(15) / 有团队办公室(10) / 个人创业(5) |
| 决策链 | 10 | 直接和创始人聊(10) / 需过合伙人(6) / 大公司审批(2) |

- 80-100分：创始人亲自跟进，一周内建联
- 60-79分：BD先触达，2周内初筛
- 40-59分：培育池，每月资讯触达
- <40分：放弃

## 线索扫描器

### 脚本位置

- `~/Desktop/lead_scanner_v2.py` — V2多源发现脚本（36氪+爱范儿+少数派+Kicktraq）
- `~/Desktop/lead_scanner.py` — V1脚本（Kicktraq为主）

### Cron Job

Job ID: `74e30e6f9e5a`，每周一 9:00 CST 自动运行。Agent 驱动模式：
1. 运行 `lead_scanner_v2.py` 采集 RSS + Kicktraq 数据
2. 使用 web_search 补充搜索中国硬件出海品牌
3. 对融资公司搜索官网/创始人/企查查/领英链接
4. 生成结构化报告到 `~/Desktop/本周线索_YYYY-MM-DD.md`

需要 web + terminal + file + skills 工具集。

### 报告结构

1. 💰 融资中的硬件公司（最高优先级）— 公司名/轮次/金额/创始人/官网/触达建议
2. 🆕 新品 & 品牌信号 — 来自爱范儿/少数派/搜索
3. 📊 KS 活跃项目（参考）— 来自 Kicktraq，含中国信号标记
4. ⚡ 本周行动建议 — 触达清单 + 手动渠道 checklist
5. ⏰ 上周未处理线索提醒

## 获客全流程 SOP

详见 `references/acquisition-sop.md` — 完整 SOP 文档（线索来源→筛选→触达→转化→签约）。

## 技术要点

### 数据源实测状态

详见 `references/source-status.md` — 所有数据源的当前可用状态和阻断原因。

### Kicktraq 解析

Kicktraq 无 Cloudflare 保护，HTML 结构稳定。项目数据从 hotlist 页提取：
- 正则：`<div class="listentry parent"` 分割项目块
- 标题+slug：`<a href="/projects/([^"]+)"[^>]*title="([^"]*)"`
- 品类：`<div class="listentry cat">(.*?)</div>`
- 进度+目标：`<span class="listentry per\w+">(\d+%)</span>\s*of\s*([^<]+)`
- 剩余时间：`<div class="listentry timeleft">(.*?)</div>`

### 中国团队信号检测

三级检测：
1. 货币信号：goal 含 `HK$` 或 `¥`
2. 地理位置：HTML 含 `shenzhen|guangzhou|hangzhou|shanghai|beijing|dongguan`
3. 品牌名：aeke/glinet/hholove/kungfu/seagull/logcase/innogeex 等已知中国品牌

### macOS SSL 证书

macOS Python 需要 certifi 处理 SSL 证书链问题：
```python
import certifi, ssl
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
```

## 用户偏好（获客相关）

- 用户是 MadSpace 创始人，有小团队
- 获客是核心痛点，需要持续自动化
- 偏好直接执行而非给步骤文档
- 对"只能给列表不能扒公司信息"不满意——要自动提取公司名/创始人/官网
- 认为 KS 在线项目介入空间有限（全流程服务，需要在品牌上 KS 之前介入）
- 主动+被动获客都要，多多益善
- 触达话术核心：给价值+给对标+给证据，不是推销
