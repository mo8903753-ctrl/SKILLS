# 标杆：Sweetmyo Gen2 · v4 "Signal"

用本 skill 的模型，做出的页面要达到这个水准（视觉、动效、克制程度）。**学结构与手法，不抄内容。**

- 线上预览：GitHub 分支 `mo8903753-ctrl/sweetmyo-gen2-landing` → `redesign-v4-opus`（Vercel 预览需登录）
- 本地：先准备素材（见下），`python3 scripts/build_wix.py`，`node scripts/serve.mjs "$PWD" 8796`，打开 `http://127.0.0.1:8796/`
- 截图总览：`benchmark/desktop-1..3.jpg`、`benchmark/mobile-1..2.jpg`（每场景 3 个进度点）
- 通过 `scripts/qa/page-metrics.mjs`：字符 ≈4,450；≤12px 文字 3.1%；带边框元素 0；字体 3 种；背景色 3 种；视频 8、canvas 2；钉住场景 8；表单位 3

## 目录

```
src/template.js        整页 HTML（buildPartHTML(part, A)；part = all | a | b | c | d 对应 Wix 分段）
src/styles.css         全部样式（根类 .sw-white-root；零边框；字阶见 design-system.md）
src/element.js         自定义元素 <sweetmyo-gen2-landing>：场景引擎 + 各原语 + Wix 表单对位
scripts/process_assets_v4.py   ffmpeg / PIL 素材流水线（scrub 视频 -g 2、裁切、封面、光晕 PNG）
scripts/build_wix.py           打包成单文件 Wix 自定义元素 + 本地 980px Wix 宿主测试页
scripts/serve.mjs              支持 Range 的本地服务器（视频 scrub 必须）
vendor/                        gsap / ScrollTrigger / lenis（内联进 Wix 包，不走 CDN）
assets-manifest.txt            页面引用的 23 个素材键（素材本身是客户资产，未放进 skill）
benchmark/                     截图总览
```
素材没有放进来：`v4/*` 由 `process_assets_v4.py` 从官网素材生成；其余沿用上一版导出。没有素材也能 `SW_SKIP_ASSET_CHECK=1 python3 scripts/build_wix.py` 看代码结构。

## 逐屏计划表（本页实际做法）

| # | 场景 id | 卖点原句（官方） | 主视觉 | 动效原语（motion-library #） | 外层高度 | 备注 |
|---|---|---|---|---|---|---|
| 1 | sw-hero | Work Out Smarter. Not Longer. | 全屏真实视频（客户指定 4 个画面） | 全屏→胶囊收缩 #1；光晕跟随鼠标 #25；规格数字计数 #10 | 300vh | 标题在 sticky 层；**表单与副标题在普通流层**，随页面滚走，保证 Wix 表单对齐 |
| 2 | sw-couch | Burn Up to 500 kcal on the Couch. | 沙发实拍视频 | 纸白幕布 #3；逐词点亮 #9；胶囊放大 #1；数字计数 #10 | 420vh | 500 放在左上，让大腿上的中控露出来 |
| 3 | sw-wave | Deep Muscle Activation（2 kHz 正弦） | canvas 实时波形 | 波形混合 #14；文字擦换（clip-path）；Hz 计数 #10 | 360vh | 数据由真实参数驱动，不是装饰 |
| 4 | sw-zones | One 20-Min Session. Every Muscle Fired Up. | 官方荧光身体渲染视频 | 视频 scrub #15；名单荧光下划线逐项点亮 | 380vh | scrub 视频 `-g 2`，需 Range 服务 |
| 5 | sw-motion | It Adapts to How You Move. | 深蹲/跑步/骑行三段实拍 | 手风琴视频 #23；脉冲线变速 | 自然高度 | 每段 ≥4.5s，片尾自动换下一个，点击接管 |
| 6 | sw-mid | Don't Miss Out. Over 50% OFF… | 横向场景大图 | 内缩展开 #2 | 100svh+ | **表单位 2** |
| 7 | sw-scan | Scan Your Body. See Your True Progress. | 官方玻璃卡片扫描视频（荧光整屏） | 扫描线揭示 #4 | 240vh | 整页唯一的荧光整屏 |
| 8 | sw-app | Training, Generated for You. | 4 张官方 App 截图 | 3D 圆弧转盘 #20 | 340vh | 说明文字随转盘切换 |
| 9 | sw-easy + safety | Train longer. Charge less. / Built to Protect You at Every Layer. | 实拍/特写 + 大数字 | 横向长廊 #21；速度跑马灯 #11 | 420vh | 手机端改纵向 |
| 10 | sw-final | Don't Miss the Kickstarter Launch. | 光晕 + 倒计时 | 光晕跟随 #25；字标升起；按钮磁吸 #26 | 自然高度 | **表单位 3**；订金步骤用官方文案 |

共 10 屏；使用了 #1 #2 #3 #4 #9 #10 #11 #14 #15 #20 #21 #23 #25 #26 共 14 种原语。

## 这个标杆吸取过的教训（已写进规则）
1. 首屏最初是“胶囊里藏视频”，客户反馈**看不到产品** → 改成全屏真实视频，滚动再收缩成胶囊。
2. 所有视频都有 Range 服务才能 scrub；`page.screenshot()` 在 sticky + 平滑滚动下会空白，用 `Page.captureScreenshot`。
3. 表单占位**不能放在 sticky 容器里**。
4. 视频的背景色要与页面背景一致（zones 的 mask 渐隐处理）。
5. `<sup>` 默认会缩到 7px → 用 `max(12px, .6em)`。

## 已知的资料冲突（交接时要告诉客户）
- 洗涤次数：官网 300+，品牌方文档 200。
- kcal：官网标题 500 kcal，文档写 up to 500 kcal/hour（页面用标题 + 每小时脚注）。
