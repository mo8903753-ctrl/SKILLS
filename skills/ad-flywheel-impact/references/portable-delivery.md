# Figma、清单、ZIP与恢复的可移植做法
先读 figma-library.md。所有路径相对项目目录，不携带原作者 /Users 路径、临时截图路径或固定节点。

## 推荐目录
project/brief.json；sources/；research/；prompts/；output/；delivery/images/<category>/；delivery/manifest.json；history/；checkpoint.md。
主清单按 templates/creative-manifest.json。资源路径相对项目，实际像素尺寸与展示尺寸分开，hash对应最终文件。

## Figma UI已验证方法（工具存在时）
1. 读取页面和真实图层。先用小样验证PNG或SVG包装导入；每板最多6张、3列，按比例展示；外部编号不放进广告像素。SVG可用 `<image>` 引用base64 PNG，不能拿SVG重画广告内容。
2. ego文件选择：先waitForFileChooser，再按宿主Figma图像导入快捷键或点击入口，setFiles绝对路径。等待出现“全部导入”并确认实际节点；不要把上传回执当完成。
3. 多文件可能叠在同一坐标。Figma当前UI可用 Alt+L 收起全部图层、选具体顶层画框、设置X/Y。按现场DOM和截图定位，不照抄固定selector或节点。
4. 设置每个坐标后等输入值和选择状态稳定再操作下一项；本案例过快连续fill导致写到旧状态。读回并截图确认无重叠。Shift+1总览、Shift+2选中放大仅在现场确认为对应快捷键时用。
5. 读取每个板中的实际图片名称/节点，和清单对账。外部文字、容器、参考图和历史修订不算成品图片。
6. 用户修订：先确认原板/节点未被人工改动。替换对应图片；若只能整体重导入原由本任务创建的板，可保留相同分组与位置，并记录新节点。不要删除别人的人工设计。新节点改变后更新下载清单与链接。

## 完成交付
逐图原尺寸检查+整批联系表+Figma总览/代表大图/横图/NT检查。成图加载清晰再验收。记录母版/变体/修订和文本模式数量；一个概念多背景不重复说成多个母版。
用 `scripts/check_delivery.py PROJECT_ROOT manifest.json --zip OUTPUT.zip` 校验已列出的文件/哈希并打包；脚本不会证明视觉质量或Figma存在。Figma必须另外实际验证。最终答复简洁提供数量、Figma、ZIP、尚存缺口。

## 中断恢复
checkpoint.md 记录：当前用户约束、完成编号/版本、原素材与prompt相对路径、已验收/待修图、Figma页面与节点、工具仍运行的任务、下一步。恢复先查文件和实时平台，再从缺口续作。不得重跑整批冒充新增，不要把已经删除的旧节点当新图位置。
