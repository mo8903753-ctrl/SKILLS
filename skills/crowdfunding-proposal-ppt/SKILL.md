---
name: crowdfunding-proposal-ppt
description: >
  众筹方案 PPT 生成器。为 MadSpace 团队根据产品信息、目标金额、预算和市场调研生成完整可编辑的众筹方案 PPTX。
  当用户要求“众筹方案”“美国众筹方案”“Kickstarter众筹方案”“众筹PPT”“客户提案PPT”“把产品做成众筹方案”时触发。
  这是“众筹方案”工具，不是“整合营销方案”工具；不要改用或修改 crowdfunding-marketing-plan。
---

# 众筹方案 PPT 生成器

为 MadSpace 团队生成客户可交付的众筹方案演示稿。核心不是套模板换产品名，而是：

`产品信息拆解 -> 联网调研 -> 策略分析 -> 严格按模板生成可编辑 PPTX`

## 输出标准

- 默认输出 40-55 页完整客户提案。
- 默认语言：中文主体，核心 slogan / 广告语提供英文 + 中文解释。
- 默认市场：美国 Kickstarter / Indiegogo；用户指定日本、台湾或其他市场时再切换。
- Canva 优先；Canva 不可访问或无法导出时，用本 skill 的本地 PPTX 兜底流程。
- 最终文件必须是可编辑 `.pptx`。标题、正文、表格、流程图、预算表、时间轴尽量使用 PPT 原生元素，不能把整页做成截图。

## 工作流

1. **拆产品变量**：读取用户文件、文字、图片或表格，先整理产品名、品牌、品类、平台、市场、目标金额、AOV/价格、销量目标、日期、核心卖点、素材、样机数量。变量规则见 `references/variable-schema.md`。
2. **联网调研**：必须搜索竞品、同品类众筹案例、价格带、用户痛点、美国市场应用场景、广告关键词、YouTube KOL。调研流程见 `references/research-workflow.md`。
3. **分析生成策略**：用调研结果生成市场洞察、用户画像、竞品对标、产品差异化、传播概念、Meta 标签、Google/YouTube 关键词、KOL 分层。
4. **生成视觉素材**：用户画像图片默认用 image generation / image2 按产品场景生成；KOL 必须用真实 YouTube 频道或视频页面截图，不得伪造。
5. **按模板出 PPT**：严格遵守模板固定页、固定图片、图片比例、位置、页边距和表格风格。模板规则见 `references/template-rules.md`，页结构见 `references/deck-structure.md`。
6. **预算计算**：按目标金额计算预算、广告拆分和订单模型。预算规则见 `references/budget-model.md`。
7. **验证交付**：检查 PPT 能打开、文本可选中、表格可编辑、固定页未改动、图片比例未变、变量页无溢出和遮挡。

## Canva 优先规则

- 如果用户提供 Canva 链接，先通过 Canva 工具读取设计内容、页面和可编辑文本。
- 如果 Canva 链接无法被连接器访问，不要卡住；说明原因后使用 PDF/截图/本地 PPTX 模板作为视觉参考。
- 不要在未获用户明确确认前保存对 Canva 原设计的修改。
- Canva 不可用时，使用 `scripts/build_pptx.py` 从整理好的 JSON 生成本地可编辑 PPTX。

## 本地 PPTX 兜底

当没有可访问 Canva 模板或模板 PPTX 时：

1. 先完成调研和变量整理。
2. 按 `references/deck-structure.md` 生成 slide data JSON。
3. 运行：

```bash
python3 scripts/build_pptx.py --input project.json --output output.pptx
```

也可以先验证预算：

```bash
python3 scripts/build_pptx.py --budget-only --goal 1000000 --aov 649
```

兜底脚本只负责生成可编辑 PPTX 骨架和预算页；正式交付仍要按模板检查与人工视觉调整。

## 严禁

- 不得把“众筹方案”任务转到 `crowdfunding-marketing-plan`。
- 不得跳过联网调研直接泛写市场洞察、用户画像、打法或 KOL。
- 不得用虚构 KOL、虚构订阅量或伪造 YouTube 截图。
- 不得改变模板固定页、固定图片、固定图形比例或 MadSpace 公司信息。
- 不得为了塞长文案挤压模板元素；内容过长时压缩文案或拆页。
