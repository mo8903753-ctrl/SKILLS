# 迈思案例库 + 平台资源库（来源：MadSpace 公司介绍 2026，82 页）

方案里的「迈思相关案例」章与各章 `.refcase` 回指都从这里取材。**图已裁好**：`cards/<slug>.jpg`（产品卡，约 400×416 白底，和母版 `.cs-card` 同规格），`resources/<name>.jpg`（整页截图，1100 宽，给 KOL / PR / 线下 / 平台章当素材或二次裁切）。用时复制到项目 `assets/img/cases/`。

## 一、挑案例规则（每个方案必跑）
1. **数量**：案例章**6–8 个不同产品案例**（默认 8，用户指定数量优先）（不含公司数据带、KOL、线下、平台奖项）。同一产品跨平台只算 1 个；资料不足时继续核实补齐，不捏造。
2. **相关度排序**（从高到低取，默认取 8 个）：
   ① 同品类（标签完全命中）→ ② 同用户/同场景（如 AI 办公 ↔ AI 录音、宠物 ↔ 家居清洁）→ ③ 同客单区间 / 同产品形态（高客单储能、桌面硬件、穿戴）→ ④ 同目标市场同平台的头部案例（美国方案优先 KS/IGG，日本优先 Makuake，台湾优先 flyingV/嘖嘖）。
3. **一张主案例大卡**（`.cs-hero`）：选相关度最高且金额最大的一个，写清它和本项目共享的是哪一类用户/素材/投放人群。
4. **分组**：按 2–4 组呈现（如「同品类」「同用户」「同市场头部」「高客单」），每组一句为什么相关；不要写成 Lucy 母版的组名。
5. **金额口径**：全部美元。日元 ÷160、新台币 ÷32 折算；原币只进 `.srcline`。同一产品多平台都做过时，主卡写本次目标市场那一笔，其余平台写进卡片说明（如「另在台湾平台约 $318K」）。
6. **回指**：竞品/市场章、KOL 章、预算或线下章各放 1 个 `.refcase`，引用最相关的那个案例或资源。
7. **品类没有 6 个直接命中时**，按第 2 条的邻近标签补齐，并把组名写成「同用户」「同市场」，**不要虚构案例、不要改金额**。
8. Nagualep 为厨余垃圾处理机；日本项目页已定位，其他平台仍按索引状态核对。

### 邻近标签速查（补齐用）
- AI办公 ↔ AI硬件 ↔ 穿戴（AIWATCH）↔ XR眼镜
- AI陪伴 ↔ 机器人 ↔ AI硬件
- 影像 ↔ 创作者 ↔ 创客制造
- 储能 ↔ 户外 ↔（高客单）
- 宠物 ↔ 家居 ↔ 清洁家电
- 健身 ↔ 穿戴（外骨骼）↔ 户外
- 存储计算 ↔ 创作者 ↔ 游戏（Pocket GO）

## 链接与来源
- `catalog.json` 保留 65 条平台记录、图片、原币金额、PDF 页码、标签、项目 URL 与链接核验状态；数字来源是用户提供的 2026 公司介绍，不代表实时项目页金额。
- `select_cases.py` 按标签与市场给候选，每个产品只出现一次。返回的 `needs_link_verification` 表示该条尚不能直接放客户页，应以官方项目/品牌发布补齐项目链接或换选。
- `search_match` 表示官方项目搜索结果或品牌公告已定位；`page_match` 表示 ego-browser 实际打开并核对标题；二者均不表示金额、平台合作身份和最新纪录已逐条复核。引用时保留字段级来源。
- 对外卡片用 `<a class="cs-card cs-link" href="真实项目URL" target="_blank" rel="noopener noreferrer">` 包住图片与正文；有嵌套交互时将唯一项目链接铺满整卡。不可用搜索链接、平台首页、空链接或猜测路径替代。
- 资料库保留未定位链接的记录作为研究线索；进入具体方案前必须完成该项目链接核对。独立站业绩需链接实际项目销售页并标注独立站，不能包装成众筹。
- **UGREEN NASync 平台修正**：日本项目为 GREEN FUNDING，不是 Makuake。[项目页](https://greenfunding.jp/focal/projects/8650)。PDF 金额 ¥1,022,589,620 保留为资料快照，不混写其他更新日期的总额。
- 徽章、第一名、历史纪录及 KOL 订阅/播放量都是历史资料；客户版无日期与口径时使用中性描述，不能写成当前排名。合作平台资源写历史合作/可协调申请，不承诺获得推荐位。

## 二、案例总表（65 条，同产品不同平台分行）
| 图 `cards/` | 品牌 · 产品 | 品类 | 标签 | 平台 | 金额(USD) | 原币 | 徽章/背书 |
|---|---|---|---|---|---|---|---|
| `rokid-glasses.jpg` | Rokid · Rokid Glasses | AI/AR 智能眼镜 | XR眼镜,AI硬件,穿戴 | Kickstarter | $3,633,205 | — |  |
| `allpowers-monster-x.jpg` | ALLPOWERS · Monster X | 大容量户外电源 | 储能,户外 | Indiegogo | $2,051,250 | — |  |
| `walkingpad-r1-pro.jpg` | WalkingPad · R1 Pro | 折叠跑步机 | 健身,家居 | Indiegogo | $1,522,699 | — | Forbes/Digital Trends/Gear Patrol 报道 |
| `dnsys-x1.jpg` | dnsys · X1 | 髋部助力外骨骼 | 健身,户外,穿戴 | Kickstarter | $1,188,887 | — |  |
| `rokid-ar-lite.jpg` | Rokid · AR lite | AR 空间计算眼镜 | XR眼镜,穿戴 | Kickstarter | $1,158,200 | — |  |
| `irmo-m1.jpg` | IRMO · M1 Exoskeleton | 髋部外骨骼 | 健身,户外,穿戴 | Kickstarter | $1,112,581 | — |  |
| `feiyu-pocket3.jpg` | FeiyuTech · Pocket 3 | 分体式口袋云台相机 | 影像,创作者 | Kickstarter | $1,090,214 | — |  |
| `leoch-powerstation.jpg` | LEOCH · Leoch | 户外储能电源 | 储能,户外 | Indiegogo | $1,059,294 | — |  |
| `mokacam-moka4k.jpg` | Mokacam · Moka 4K | 4K 运动相机 | 影像 | Indiegogo | $1,053,550 | — |  |
| `inmo-go3.jpg` | INMO · GO3 | AI 智能眼镜 | XR眼镜,AI硬件,穿戴 | Kickstarter | $1,035,332 | — |  |
| `hengbot-sirius.jpg` | HENGBOT · Sirius | 桌面机器狗 | 机器人,AI陪伴 | Kickstarter | $880,612 | — |  |
| `hyperdisk.jpg` | HYPER DISK · Hyperdisk | 便携高速固态存储 | 存储计算,创作者 | Kickstarter | $782,343 | — |  |
| `3dmakerpro-whale.jpg` | 3DMakerpro · Whale | 3D 扫描仪 | 创客制造,创作者 | Shopify 独立站 | $752,034 | — |  |
| `yashica-fx-d.jpg` | YASHICA · FX-D | 复古数码相机 | 影像 | Kickstarter | $745,175 | — |  |
| `petkit-purobot-ultra.jpg` | PETKIT · PUROBOT ULTRA | 智能猫砂盆 | 宠物,家居 | Indiegogo | $618,706 | — |  |
| `hoorii-clawstage.jpg` | HooRii · ClawStage | AI 桌面全息陪伴 | AI陪伴,AI硬件 | Kickstarter | $608,372 | — |  |
| `allpowers-monster-pro.jpg` | ALLPOWERS · Monster Pro | 户外电源 | 储能,户外 | Indiegogo | $578,882 | — |  |
| `nagualep.jpg` | NAGUALEP · Nagualep | 厨余垃圾处理机 | 家居 | Indiegogo | $493,601 | — | Indiegogo 年度最佳文案奖 2021 |
| `mokacam-alpha4k.jpg` | Mokacam · Alpha 4K | 运动相机 | 影像 | Indiegogo | $468,638 | — |  |
| `feiyu-scorp-mini.jpg` | FeiyuTech · Scorp mini | 相机稳定器 | 影像,创作者 | Kickstarter | $460,318 | — |  |
| `ortur-h20.jpg` | ORTUR · H20 | 桌面激光雕刻机 | 创客制造,创作者 | Kickstarter | $441,605 | — |  |
| `inkjoy-frame.jpg` | InkJoy · InkJoy Frame | 彩色电子墨水画框 | 家居,AI硬件 | Kickstarter | $413,574 | — |  |
| `tecno-pocket-go.jpg` | TECNO · Pocket GO | AR 眼镜 + 掌机 PC | XR眼镜,存储计算,游戏 | Kickstarter | $400,288 | — | ETA PRIME / ShortCircuit 评测；IFA 2024 Best of |
| `litheli-w1-pro.jpg` | Litheli · W1 PRO | 电动露营推车 | 户外 | Indiegogo | $373,109 | — | Indiegogo 年度最佳文案奖 2023 |
| `smartmi-p1.jpg` | smartmi · P1 | 空气净化器 | 家居 | Indiegogo | $354,084 | — |  |
| `ugreen-nasync.jpg` | UGREEN · NASync | 多盘位私有云 NAS | 存储计算,AI硬件 | GREEN FUNDING | $6.39M | ¥1,022,589,620 | 日本 Funded 历史纪录；韩国 Wadiz 科技类第 1（₩2,386,783,550） |
| `allpowers-monster-x.jpg` | ALLPOWERS · Monster X | 大容量户外电源 | 储能,户外 | Makuake | $2.33M | ¥373,325,800 | 日本 Funded 历史纪录 |
| `code27.jpg` | CODE27 · CODE27 | AI 桌面全息陪伴 | AI陪伴,AI硬件 | Makuake | $1.35M | ¥215,524,600 |  |
| `hoverair-x1-smart.jpg` | HOVERAir · X1 SMART | AI 跟拍飞行相机 | 影像,AI硬件,创作者 | Makuake | $1.33M | ¥212,410,602 | Makuake 相机类历史销售额第 1；Makuake Of The Year 2024 |
| `tcl-note-a1.jpg` | TCL · Note A1 | AI 电子纸笔记本 | AI办公,AI硬件 | Makuake | $1.18M | ¥188,052,430 |  |
| `neabot-nomo-q11.jpg` | neabot · NoMo Q11 | 扫地机器人 | 清洁家电,家居 | Makuake | $1.15M | ¥183,885,780 |  |
| `iflytek-aiwatch.jpg` | iFLYTEK · AIWATCH | AI 智能手表 | 穿戴,AI硬件,AI办公 | Makuake | $1.07M | ¥170,927,660 | Makuake 智能穿戴历史销售额第 1 |
| `halliday-ai-glass.jpg` | Halliday · AI Glass | AI 智能眼镜 | XR眼镜,AI硬件,穿戴 | Makuake | $1.01M | ¥161,308,420 | Makuake 智能眼镜历史销售额第 1 |
| `iflytek-ainote-air2.jpg` | iFLYTEK · AINOTE Air2 | AI 办公电子纸 | AI办公,AI硬件 | Makuake | $810K | ¥129,557,650 |  |
| `hidock-p1.jpg` | HiDock · P1 | AI 录音与会议纪要 | AI办公,AI硬件 | Makuake | $758K | ¥121,346,380 |  |
| `makera-carvera-air.jpg` | MAKERA · Carvera Air | 桌面 CNC | 创客制造,创作者 | Makuake | $582K | ¥93,085,800 |  |
| `feiyu-pocket2s.jpg` | FeiyuTech · Pocket 2S | 口袋云台相机 | 影像,创作者 | Makuake | $518K | ¥82,892,723 |  |
| `looi.jpg` | LOOI Robot · LOOI | AI 桌面机器人 | 机器人,AI陪伴,AI硬件 | Makuake | $495K | ¥79,177,200 | Makuake 机器人类历史销售额第 1 |
| `ropet-lopeto.jpg` | ropet · lopeto | AI 情感陪伴机器人 | 机器人,AI陪伴 | Makuake | $475K | ¥76,075,420 |  |
| `creality-crscan-lizard.jpg` | CREALITY · CR-Scan Lizard | 3D 扫描仪 | 创客制造,创作者 | Makuake | $454K | ¥72,578,940 |  |
| `mirror-fit.jpg` | MIRROR FIT · MIRROR FIT | 智能健身镜 | 健身,家居 | Makuake | $419K | ¥67,016,215 |  |
| `loona.jpg` | KEYi Tech · Loona | AI 宠物机器人 | 机器人,AI陪伴 | Makuake | $353K | ¥56,466,983 |  |
| `goovis-g3-max.jpg` | GOOVIS · G3 MAX | 头戴影院 | XR眼镜,影音 | Makuake | $351K | ¥56,089,000 |  |
| `litheli-frozenpack.jpg` | Litheli · FrozenPack | 电池供电车载冰箱 | 户外,储能 | Makuake | $335K | ¥53,567,480 |  |
| `litheli-frozenpack-wild.jpg` | Litheli · FrozenPack Wild | 背负式电动冰箱 | 户外,储能 | Makuake | $285K | ¥45,622,040 |  |
| `dreame-x30-ultra.jpg` | Dreame · X30 ULTRA | 扫地机器人 | 清洁家电,家居 | Makuake | $268K | ¥42,902,408 |  |
| `udcap-vr-glove.jpg` | UDCAP · VR Glove | VR 动捕手套 | XR眼镜,游戏 | Makuake | $261K | ¥41,798,251 |  |
| `3dmakerpro-whale.jpg` | 3DMakerpro · Whale | 3D 扫描仪 | 创客制造,创作者 | Makuake | $259K | ¥41,510,240 |  |
| `nagualep.jpg` | NAGUALEP · Nagualep | 厨余垃圾处理机 | 家居 | Makuake | $259K | ¥41,463,330 |  |
| `segway-cube1000.jpg` | Segway-Ninebot · Cube 1000 | 户外储能 | 储能,户外 | Makuake | $255K | ¥40,771,920 | 东京线下媒体实机体验会 |
| `ecovacs-deebot-x1.jpg` | ECOVACS · DEEBOT X1 | 扫地机器人 | 清洁家电,家居 | flyingV | $3.53M | NT$112,885,672 | 2022 台湾募资金额第 1 |
| `ecovacs-deebot-t8.jpg` | ECOVACS · DEEBOT T8 | 扫地机器人 | 清洁家电,家居 | flyingV | $1.66M | NT$53,120,464 | 2020 台湾募资金额第 1 |
| `hoverair-x1-smart.jpg` | HOVERAir · X1 SMART | AI 跟拍飞行相机 | 影像,AI硬件,创作者 | flyingV | $1.05M | NT$33,536,825 |  |
| `petsnowy-snow-plus.jpg` | PetSnowy · SNOW+ | 智能猫砂盆 | 宠物,家居 | flyingV | $986K | NT$31,557,152 | 台湾宠物类募资金额第 1 |
| `mokacam-alpha3.jpg` | Mokacam · Alpha3 | 运动相机 | 影像 | 嘖嘖 | $777K | NT$24,870,280 |  |
| `furbulous-box.jpg` | FURBULOUS · Furbulous BOX | 智能猫砂盆 | 宠物,家居 | flyingV | $628K | NT$20,103,845 |  |
| `neabot-nomo-q11.jpg` | neabot · NoMo Q11 | 扫地机器人 | 清洁家电,家居 | flyingV | $411K | NT$13,161,170 |  |
| `feiyu-pocket3.jpg` | FeiyuTech · Pocket 3 | 分体式口袋云台相机 | 影像,创作者 | flyingV | $328K | NT$10,500,351 |  |
| `makera-carvera-air.jpg` | MAKERA · Carvera Air | 桌面 CNC | 创客制造,创作者 | 嘖嘖 | $318K | NT$10,174,040 |  |
| `iflytek-ainote-air2.jpg` | iFLYTEK · AINOTE Air 2 | AI 办公电子纸 | AI办公,AI硬件 | flyingV | $254K | NT$8,140,628 |  |
| `lava-genie.jpg` | LAVA MUSIC · GENIE | 智能吉他 | 乐器,创作者 | flyingV | $249K | NT$7,983,471 |  |
| `lalahome-realscooper.jpg` | LALAHOME · RealScooper | 智能猫砂盆 | 宠物,家居 | 嘖嘖 | $223K | NT$7,145,044 |  |
| `ecovacs-n8.jpg` | ECOVACS · ECOVACS N8 | 扫地机器人 | 清洁家电,家居 | flyingV | $165K | NT$5,293,366 |  |
| `creality-crscan-lizard.jpg` | CREALITY · CR-Scan Lizard | 3D 扫描仪 | 创客制造,创作者 | flyingV | $148K | NT$4,725,000 |  |
| `lava-me4.jpg` | LAVA MUSIC · LAVA ME 4 | 智能吉他 | 乐器,创作者 | flyingV | $130K | NT$4,156,663 |  |

> 折算口径：JPY ÷160、TWD ÷32 是这份历史资料的固定展示口径，并非实时汇率；新方案如需现价，先核实汇率，均为约数；对外写「约 $X」，原币进 `.srcline`：「来源：迈思创新公司介绍 2026」。

## 三、公司数据带（按需求选用；不强制新增公司背景章节）
300+ 累计众筹项目 · $100M+ 累计项目金额 · 150,000+ 累积海外用户 · $7,020,387 单项目最高金额。2015 年起运营 Kickstarter / Indiegogo，首个项目即破 $1M。合作品牌：TCL、FeiyuTech、ECOVACS、Formovie、GOOVIS、Midea、Segway-Ninebot、GoPro、NARWAL、CREALITY、ORTUR、Loona、PetSnowy、3DMakerpro、RayNeo、Tineco、Dreame、JMGO、Rokid、PETKIT（`resources/brand-wall.jpg`）。

## 四、平台资源（「平台资源」模块必放，按目标市场取）
**公司介绍记载的平台身份（使用前核实有效性）**（`resources/platform-partners.jpg`）
- Kickstarter **Expert Partner**；Indiegogo / Kickstarter / Makuake / 嘖嘖 / flyingV / Wadiz **官方推荐服务商**
- Makuake：**首家获得 Makuake Partner 赏的众筹 Agency**；Makuake Of The Year 2023 / 2024；2022、2024、2025、2026 年创始人在 Makuake 年度活动分享；2023 参加 Makuake 展会（`platform-makuake-*.jpg`）
- Indiegogo：年度最佳文案奖（Nagualep 2021、Litheli W1 PRO 2023）（`platform-igg-award.jpg`）
- Kickstarter：2023 与 Kickstarter 同行参访飞宇科技（`platform-kickstarter-visit.jpg`）
- flyingV：2023 到访台湾总部交流（`platform-flyingv-visit.jpg`）
- 官方资源协调：上线期争取平台首页/编辑推荐/EDM 位、Makuake 线下专区（Yodobashi、Nojima、茑屋家电）

**团队与据点**：北京运营总部 · 深圳商务与供应链 · 洛杉矶媒体与 PR 中心 · 台北分公司 · 日本分公司。欧美团队 15 人（6 位外籍）+ 美国本土 PR 团队（20 年以上 PR 经验）；日本团队 16 人（8 位日籍）；台湾 7 位本地同事。

**PR 媒体露出**（`pr-*.jpg`）：Forbes、Digital Trends、Gear Patrol、Gadgetify、TrendHunter、Android Central、urbantecno、CNET、Fox Business、Android Headlines（IFA 2024 Best of）、Tech Advisor、Techpression。纽约 Pepcom 媒体活动（CNN、Fox News、Digital Trends 到场）。

**KOL 实绩（1,500+ 位合作经验）**——格式：频道 · 订阅 · 合作视频播放
- 欧美头部：ETA PRIME 1.25M · 426K（2024/11，17K 赞）；ShortCircuit 2.42M + Linus Tech Tips 16.3M · 350 万+ 播放；Self Sufficient Me 2.41M · 835K（26K 赞）；Arthur R 221K · 195K
- 欧美腰部：KhanFlicks 1.02M · Max Tech 1.22M · Darbin Orvar 357K · HOBOTECH 218K · HansTechTalk 258K · ben's gadget reviews 258K · Aaron X Loud and Wireless 128K · Wex Photo Video 118K · Sami Luo Tech 106K · Stephen J Reid 100K（190K 播放）· HolzHeini 31K · One Man and His Whippet 41.2K
- 日本：Kaede and Ahtan 3.75M · 瀬戸弘司 1.67M · 桜雲AUN 1.33M · マメ 406K · taroshin 270K（200K 播放）· Mikasu-Channel 225K · サトシの趣味部屋 208K
- 台湾：奇軒Tricking 15.6M（台湾 YT 排行 No.1）· 魚乾 1.3M · the劉沛 1.22M · 頭城小夫妻 94.1K · 懷爸瘋科技 67K
- 名人：Arabian Prince（N.W.A. 创始成员）、NFL 球员 Jaeden Graham / Evan Engram、《黑豹》演员 Carrie Bernans（`celebrity.jpg`）

**线下展示与体验会**（`offline-*.jpg`）
- 美国：纽约 Pepcom 媒体活动；Rokid 纽约时代广场试戴；宠物美容仪纽约体验会；CES 期间 Influencer 活动
- 日本：东京新宿伊势丹展示；飞宇涩谷大屏广告；创想三维 3D 扫描仪体验会；Segway 储能东京媒体实机体验会；Litheli 登上日本综艺；Nojima 横滨/涩谷、茑屋家电、Yodobashi 店内展示
- 台湾：科沃斯 T8 体验会；Segway 滑板车试骑；HoverAir 体验会；PetSnowy 宠物展 + 综艺

**运营能力素材**：本地化广告素材（`ad-creative-*.jpg`）、高转化落地页（`landing-page-1.jpg`）、SNS 私域（`sns.jpg`）、EDM（`edm.jpg`）、每日投放数据表与周报复盘。

**客户证言**（`testimonials.jpg`，可选放 1–2 条）：峰米科技 CEO 赖永赛；智米科技 周余；飞宇科技 Jane Zhan；PinturaLife Jing Ling；福蕾科技 沈周奕（台湾平台 15 天 NT$1,000 万）；糯雪科技 PetSnowy Vincent Tsang。

## 五、按市场的平台资源模块怎么放
- **美国方案**：KS Expert Partner + IGG 官方服务商与文案奖 → 美国 PR 媒体墙 → 欧美 KOL 头部 3 张卡 + 腰部名单 → Pepcom / 时代广场 / CES 线下
- **日本方案**：Makuake Partner 赏 + Of The Year → 日本 KOL 名单 → Yodobashi / Nojima / 茑屋 / 伊势丹 / 媒体体验会 → 日本团队 16 人
- **台湾方案**：flyingV / 嘖嘖 官方服务商 + 台湾募资第 1 纪录 → 台湾 KOL → 台湾体验会 / 综艺 → 台湾 7 人团队
- 资源截图里有别家客户的产品图，只作「迈思做过」的佐证，不要和本项目产品混排成同一视觉。

> PDF 更新后：把新 PDF 放进来，用本目录的 `crop.py`（卡片坐标 x=[80,342,604,865,1127]，y=206–438，页面 1440×810）重裁，并改这份表。
