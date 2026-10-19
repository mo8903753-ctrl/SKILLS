# 生成来源与入库门槛

## 状态顺序
`reference_read → generation_ready → generated → visually_passed → figma_imported → verified`
没有生图能力停在 `BLOCKED_IMAGEGEN`；Figma 可用不能越过 generated。先前已经生成、证据可追溯的合格位图可以直接进入后续阶段，无需为通过检查重新付费生成。

每张清单填 `production_method: image_generation` 与 `generation` 对象。`tool` 是真实工具名；`record_path` 是项目内保存的工具调用证据 JSON；`prompt_path` 是完整最终生成/编辑提示词；`input_assets` 是实际输入图的项目相对路径；`output_sha256` 等于最终成品 SHA256；`complete_ad: true` 只在工具直接输出完整广告时填写。工具若没有调用 ID 留空，不编造。证据 JSON 从实际调用及响应保存工具名、真实输出路径/标识、时间（可得时）、输入、提示词、成品哈希；移除凭据。修订链保留父版本及各次真实调用。

入库前：`python3 scripts/check_delivery.py PROJECT_ROOT MANIFEST --require-generation`。交付时加 `--require-figma --zip OUTPUT.zip`。参数缺失的旧版常规校验不能视为新版生产门槛通过。脚本只查记录存在、字段和哈希一致，不认证真实调用、不自动判断图是否完整；人工/AI 视觉核对和实际工具记录不可省略。

## 具体正反例
- 对：读取固定库 Frame → 将参考图、原产品、原 Logo 和精确日文送入图片工具 → 得到完整广告 → 看图修正 → 单一完整位图导入 Figma。
- 错：Figma 新建广告 Frame → 贴产品 → 新建标题文字 → 画折扣徽章和 CTA → 导出 PNG。即使效果好也不符合该技能。
- 错：生图只做背景，Figma 再完成广告；用 SVG 包装夹带新标题或按钮；把截图当生图结果。
- 对：广告位图外的分类标题和编号；不进入广告导出边界，不改动位图自身内容。

## 行为回归场景（需要实际执行，不能只读后宣称通过）
1. 生图工具缺失但 Figma 可写：应返回 BLOCKED_IMAGEGEN，零次成品写入。
2. 工具只返回无字底图而任务要含字：不能通过 QA，不允许 Figma 补字。
3. 日文错字或 Logo 漂移：调用图片编辑，不能在 Figma 盖字/贴 Logo。
4. 8 张中 1 张未生成：该批不能先写 7 张后在 Figma 制作第8张；先修复或明确剩余缺口。
5. 完整位图已生成并通过 QA：允许单一图片导入、外部分类与等比排列。
6. 只说“按固定库的版式来”：仍调用生图，不走设计插件重建路线。
