---
name: luodiye-zhenshe
description: 落地页震慑版（luodiye-zhenshe）。MadSpace 的 Kickstarter / 众筹预热落地页（Landing Page）全流程：盘点品牌方素材 → 按卖点参考竞品做动效 → 写成高质感滚动交互网页 → 用 Wix「自定义元素」落到 Wix 并用 Wix 原生表单收邮箱 → 截图自检 → 发布与交接。用户说「做预热页 / landing page / 落地页 / 按范例做一个新项目 / 放到 Wix / 收邮箱」，或提到「落地页震慑版」、给出 w95182.wixsite.com 范例链接、飞书文案表、素材文件夹时使用。也用于已有预热页的后续修改。
---

# 落地页震慑版

Kickstarter / 众筹预热落地页，落到 Wix，用 Wix 原生表单收邮箱。

这个 skill 复刻 MadSpace 做 biaXbew Genesis01 预热页的完整方法，包括负责人（下称"客户"）的审美偏好和历次反馈。目标是同样的输入能做出同样水准、同样做法的页面。

**动手前必须读：**
1. `references/client-taste-and-rules.md`：客户的偏好、禁忌和工作方式。**违反其中任何一条都会被打回。**
2. 当前阶段对应的 reference（见每一步）。
3. 完整案例 `examples/biaxbew-genesis01/`：源码、Wix 打包脚本、交接文档，遇到不确定的做法先看它怎么做的。

---

## 输入（开工前确认齐全）

| 输入 | 说明 |
|---|---|
| 范例页 | 客户以往的 Wix 预热页，决定结构和 CTA。清单见 `references/page-blueprint.md` |
| 文案表 | 通常是飞书表格，英文列是定稿。**正文只能用表里的句子** |
| 素材文件夹 | 品牌方原片，常见几百到上千张、几十 GB。只读 |
| 参考站（可选） | 客户给的风格参考。借思路，不照搬样式 |
| Wix 站点 | 必须是付费套餐 + 已绑定域名（自定义元素的前提）。拿到编辑器链接和目标页面 |
| 表单与弹窗 | 用哪个 Wix 原生表单、提交后弹哪个弹窗（进群、付定金、问卷） |

缺 Wix 站点也可以先做本地页面，最后再落地。

---

## 流程

### 1. 读文案、看范例和参考站
- 文案表用飞书工具读（`lark-cli sheets +csv-get`，或客户提供的导出）。记下每个卖点的标题、正文、数字规格，以及品牌方原始卖点页签里的产品事实。
- 用浏览器打开 2 至 3 个范例页和参考站，截图，记录结构：顶栏 → 首屏（标题 + 副标题 + Kickstarter 字标 + 折扣 + 邮箱框）→ 卖点区块 → 中段订阅条 → 场景轮播 → 结尾订阅 → 版权。
- 详见 `references/page-blueprint.md`。

### 2. 全量盘点素材（不能抽样）
客户要求"完全彻底扫描所有素材"。做法：
1. `scripts/assets/thumbs.py` 给全部原片生成 1200px 缩略图（多进程，千张约 1 分钟）。
2. `scripts/assets/sheets.py` 拼成带文件名的总览图，每张 42 格，**逐张看完**。
3. 记录：每个文件夹拍了什么、哪些是精修、哪些是花絮不能用、产品有几个配色、哪些是同机位连拍、哪些有道具或第三方 IP 风险。
4. 把结论写进项目笔记，之后不再重新盘点。

详见 `references/asset-pipeline.md`。

### 3. 每个卖点：先查竞品怎么表达，再定画面和动效
- 每个卖点都要回答"用户看完这一屏能不能看懂这个卖点"。
- 先搜同类竞品官网（苹果、Razer、Wooting、Keychron、NuPhy 等）这个卖点是怎么用画面和动效讲的，截图存档，再决定本页做法。
- 已被客户认可的做法和被否掉的做法都在 `references/motion-playbook.md`，优先复用认可过的。
- 每张图都要能回答"它在证明哪一句文案"。同一个镜头全页只出现一次。

### 4. 处理素材（不能裸用）
- 裁切到版位比例（不靠 CSS 硬裁）、统一调色、压暗背景、去道具。
- 灯效连拍先对齐再做切换；产品抠图做透视校正；需要"动起来"的产品拆层（例：轴体拆成轴心和外壳）。
- 缺少的画面可以生成，但**不能改变产品本身**（键帽字符、布局、配色、Logo），生成的工艺示意图要在画面上标 "Process visualization"。
- 主展示配色以客户指定的为准（biaXbew 是亮银为主、烟枪灰其次、黑色辅助），同一画面里产品配色必须一致。
- 详见 `references/asset-pipeline.md`。

### 5. 写页面
- 一个静态页：`index.html` + `css/style.css` + `js/main.js` + `assets/`。动效用 GSAP + ScrollTrigger。
- 版式、字体、色彩、动效的规矩见 `references/client-taste-and-rules.md` 和 `references/motion-playbook.md`。
- 结构从 `examples/biaxbew-genesis01/` 起步最快：保留它的骨架（首屏 3D 产品、整屏滚动短片、自动轮播、数字计数），替换内容和素材。

### 6. 本地自检
- 本地起服务，用浏览器自动化在 1440 宽和 390 宽（手机）逐屏截图，看完每一张再交付。
- 检查清单见 `references/qa-and-delivery.md`。

### 7. 落到 Wix
- 原理和全部操作见 `references/wix-custom-element.md`（技术细节）和 `references/wix-custom-page-prompt.md`（给其他 AI 的完整提示词版本）。
- 打包：`scripts/wix/build_wix.py`（案例里的版本，换项目时要改选择器和分段）。
- 部署：`scripts/wix/deploy.mjs`（上传图片 → 写入代码文件 → 发布）。
- **只能在发布后的线上页面验证**，Wix 编辑器的预览里自定义元素是空白的。
- **Wix 发布是整站发布，每次发布前都要得到客户同意。**

### 8. 交付和交接
- 每轮交付：说清改了什么、哪些在线上验证过、哪些没验证（真机、表单提交）。
- 项目结束或换人：写一份只写当前状态的交接文档，模板见 `references/qa-and-delivery.md`，范例见 `examples/biaxbew-genesis01/HANDOFF.md`。

---

## 改稿时的规矩（最常出错的地方）

- 客户说"有些地方不行"→ 只改指出的那几处，先点名你认为有问题的地方再动，不要全局重做。
- 客户说"删掉某部分"→ 先确认是删整块还是只删重复内容（曾经误删整条横向长廊被要求恢复）。
- 客户说"设计大改 / 重构"→ 换整体形态，旧版只当内容库。
- 客户说"素材单调 / 没灵魂 / 切换不优雅"→ 回到第 3 步查竞品动态表达，重做这一屏的画面和动效，不是换几张图。
- 改完要再截图看一遍自己改的地方，有残影、比例错、文字被裁切都要先自己发现。
- 详细的历次反馈见 `references/feedback-log.md`。

## 工具要求
- 浏览器自动化：能打开已登录的 Wix 编辑器并在页面里执行 JavaScript（客户用 Ego Lite 的 `ego-browser`；也可用 Playwright、Claude in Chrome 等）。
- Python 3（Pillow、OpenCV、NumPy；抠图要 rembg）、Node。
- 飞书读表：`lark-cli`（或客户导出的表格文件）。
- 生图（可选）：用于补缺失的工艺示意画面。
