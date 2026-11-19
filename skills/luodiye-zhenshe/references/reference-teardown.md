# 参考页动效拆解（还原参考页的强制步骤）

目的：让模型**真的把参考页的动效 100% 还原**，而不是“看个大概就自己发挥”。  
参考页的动效是**下限**；还原完之后，再按 `motion-library.md` 额外加 ≥2 种。

## 步骤 1：录下参考页

用 `ego-browser`（客户规定的浏览器）打开参考页，**固定 1440×900** 视口：

```js
await page.cdp("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
```

1. 先用 `page.evaluate` 读出文档总高度 `H`；
2. 在 `0, H/19, 2H/19 … H` 共 **20 个固定点**各截一张（等 1.2 秒再截，让平滑滚动落稳）；
3. 在**每个“有动效”的场景**内部再取 **5 个进度点**（0 / .25 / .5 / .75 / 1）；
4. 用 `Page.captureScreenshot`（`format: "jpeg", fromSurface: true`）截图；不要用 `page.screenshot()`（sticky + 平滑滚动下可能得到空白帧）。
5. 记录页面用的库与结构：`window.gsap`、`window.ScrollTrigger`、`window.Lenis`、`canvas` 数量、`video` 数量、`position: sticky` 元素、`IntersectionObserver` 使用情况（可在控制台读取）。
6. 对手机宽度 390 重复一遍。

## 步骤 2：动效表（必须交给用户看）

| 场景 | 位置(vh) | 触发 | 变化的属性 | 开始→结束(进度) | 缓动/时长 | 素材 | 对应卖点 | 我如何实现 |
|---|---|---|---|---|---|---|---|---|
| 例：首屏 | 0–300 | 滚动进度 | `clip-path` 内缩、文字颜色 | .36→.8 | easeInOut | 4 段视频 | 产品登场 | 原语 #1 |

要求：
- **一行一个动效**，连很小的（光晕、磁吸、计数弹跳）也要列。
- “我如何实现”必须对应 `motion-library.md` 的原语编号；找不到对应原语就新写一个并补充到库里。
- 表中任何一行没有实现，就不能说“已还原”。

## 步骤 3：逐屏计划表（必须用户确认后才写代码）

| # | 卖点原句 | 标题(≤8 词) | 主视觉（文件 / 生成 / 3D / canvas） | 动效原语 | 外层高度 | 字数 | 手机端简化 |
|---|---|---|---|---|---|---|---|

检查：
- 至少 6–7 屏；包含首屏 / 中段横幅 / 终极 CTA 三个表单屏；
- ≥8 种原语，其中 ≥2 种在参考页里**没有**；
- 相邻两屏原语不同；
- 每个主视觉能证明那一屏的文案（见 `design-system.md` §8）；
- 全页预估字符 ≤5,000。

## 步骤 4：开发

照 `examples/sweetmyo-gen2-v4/` 的结构起步：
```
src/template.js   # buildPartHTML(part, A)：整页 HTML；A(path) 解析素材路径
src/styles.css    # 全部 CSS，根类 .sw-white-root 下
src/element.js    # 自定义元素 + 场景引擎 + 各原语
scripts/process_assets_*.py   # ffmpeg / PIL 素材流水线（裁切、scrub 视频、封面）
scripts/build_wix.py          # 打包成单文件 Wix 自定义元素 + 本地宿主测试页
scripts/serve.mjs             # 支持 Range 请求的本地服务（视频 scrub 必须）
```

## 步骤 5：自检

```bash
node scripts/serve.mjs "$PWD" 8796 &
ego-browser nodejs < <skill>/scripts/qa/page-metrics.mjs   # 必须 GATE: PASS
ego-browser nodejs < <skill>/scripts/qa/scroll-shots.mjs   # 每场景 3 个进度点，桌面+手机
```
`page-metrics` 的 HARD 项（任何一项失败即不可交付）：
- 可见字符 ≤5,000；无文字 <12px；≤12px 文字占比 ≤5%
- 字体 ≤3 种；带边框元素 ≤6；无 backdrop-filter / blur 滤镜；背景色 ≤3
- 视频 ≥5 且 视频+canvas ≥6；高度 ≥2.2vh 的钉住场景 ≥6
- 无破图；桌面/手机均无横向溢出；Wix 表单占位恰好 3 个

然后**逐张打开截图**（桌面 1440 + 手机 390）检查：
1. 产品或数据是否被文字遮挡？
2. 有没有内容挤在一角、其余空着？
3. 转场结束时上一张图有没有残影？
4. 数字是否与官方资料一致？
5. 手机端有没有裁切、重叠、小于 12px？
6. 表单占位与真实表单是否对齐（`dx=dy=dw=0`）？

## 步骤 6：交付

- 总览截图（桌面 + 手机）；
- 非原文文案清单、资料冲突清单（例如 200 次 vs 300+ 次洗涤）；
- **未验证项**（线上 Wix、真实表单提交、真机 Safari/iOS）分开写，诚实汇报；
- 发布 Wix 前必须得到客户明确同意（Wix 发布是整站发布）。
