# 沉浸版（Immersive）· 动效 / 交互 / 色彩体系

> 来源：2026-11 Cephalon Lucy AI Studio 日本方案站（线上 cephalon-japan-proposal.vercel.app）。
> 参考站：lusion.co（加载计数、滚字 hover、光标、3D 跟手）、more-nutrition.webflow.io（大色块切换、彩色卡片堆叠、巨型页脚字标、SplitText）、oryzo.ai（产品自转 + 背景换色弹卡、巨字从产品背后穿过、构造线标注、中心放大横向画廊、丝带）。
> 活代码母版：`templates/immersive-bay/`（可直接 `python3 -m http.server` 打开）。改造步骤见该目录 `TEMPLATE.md`。

## 0. 定位
所有众筹方案网站都用本体系。2026-11 起沉浸版是**唯一形式**（替代原结论版 / 叙事版）；文件夹交付 + GitHub 私有仓库 + Vercel 自动部署。

## 1. 叙事骨架：产品结构 = 方案结构
主角的物理结构决定章节划分（Lucy：5 个硬盘位 = 5 章）。滚动顺序固定：

| 场景 | 高度 | 做什么 |
|---|---|---|
| 加载 | — | 巨号计数 000→100，跟 GLB 真实加载进度；完成后 clip-path 向上收起 |
| hero | 230vh | 主角 3/4 视角 + 可拖拽旋转 + 背后巨字「LUCY AI」横移 + 蓝色圆盘 |
| spin | 440vh | 主角转 360°，背景以主角为圆心四次扩散换色，左右交替弹出 4 张大号参数卡，3D 文字丝带螺旋缠绕并被"拉出" |
| 跑马灯 | — | 黑底倾斜条，速度跟滚动速度、方向跟滚动方向 |
| unbox | 340vh | 拆前盖 → 构造线标注（尺寸/接口/27mm 间距）→ 每个盘位挂可点击章节标签 |
| 每章 intro | 330vh ×N | 上一盘位 sleeve 收回 → 上一块硬盘推回 → 本块拉出（盘面印章节名）→ 盘位前板长出 sleeve 铺满全屏 |
| 章节内容 | 正常流 | 圆角白卡从蓝色 sleeve 上"升起"，内部按主题色块切换 |
| outro | 300vh | sleeve 收回、硬盘归位、前盖装回、丝带再缠一次、结语 |
| 页脚 | — | 整块品牌蓝 + 23.5vw 巨型字标逐字升起 |

**换产品时**：找到产品"可打开/可拉出/可分层"的结构（抽屉、模块、电池仓、镜头组、配件）当章节容器；找不到就用 spin + disc + 色块，不硬造拆解。

## 2. 引擎：滚动位置 → 状态 → 渲染（不要用 GSAP pin 驱动 3D）
- 每个 `[data-scene]` 算 `start/end`（end = top + height − vh），当前场景 = 最后一个 start ≤ scrollY 的场景，`p∈[0,1]`；章节内容区间自动"保持"上一场景 p=1 的状态。
- `sceneState(s,p)` 返回纯状态 `{az,el,dist,sx,sy,ty,tz,cover,drives[],sleeve,sleeveDrive,spin,ribA,ribB,idle,drag,interactive}`，用 `seg(p,a,b)` + `easeIO` 分段。**每个场景的起点状态必须等于上一个场景的终点**，倒着滚自然倒放。
- `stage.apply(S)`：相机按球坐标绕 target；`camera.setViewOffset(W,H,-sx·W,-sy·H,W,H)` 把主角推到屏幕左右（文字让位），比移动模型稳。
- 叠加层：鼠标视差（±0.1 az）、拖拽惯性（只在 hero/unbox 早段）、hover 拉出 0.016m。
- 章节完全盖住视口时 `canvas.style.visibility='hidden'` 且不 render（省 GPU）。
- DOM 文案用 GSAP ScrollTrigger scrub（trigger=场景，start top top，end bottom bottom），时间轴位置直接写 p 值。

## 3. 色彩系统
基底白，但**色块多**——纯白会被嫌单调（2026-11 用户原话"整体颜色一片白，不是很好看"）。

| Token | 值 | 用途 |
|---|---|---|
| page 白 | #FFFFFF | 默认底 |
| ice 冰蓝 | #E6EBFF（卡片 #DCE4FF） | 配置对比、预算、受众层级等"数据冷静"段 |
| blue 品牌蓝 | #2B50E0 | 锚点、页面叙事、上线作战、品牌资产、sleeve、页脚 |
| ink 墨 | #0E1117（强调 #8EA4FF） | 受众画廊、档位、广告素材、全屏主张 2 |
| orange 信号橙 | #FF6A3D | 只给卡片堆叠第 4 张、spin 第 3 色、第 3 章圆盘；全站点缀，不铺底 |
| peri 浅紫蓝 | #B9C7FF | spin 第 4 色、第 5 章圆盘 |
| 巨字底色 | #E3E9FD | hero/unbox/章节号巨字，压在 canvas 后 |

- **整屏换色**：章节内用 `<div class="band" data-theme="ice|blue|ink">` 标区域；每帧找视口中线落在哪个 band，把 `data-t` 设到 `.chapter` 上。颜色变量全部 `@property` 注册为 `<color>`，`.chapter` 上 `transition: --page .9s, --ink .9s …`，于是背景、文字、卡片、线条一起平滑变色。
- 组件背景一律用 `var(--card)`（不是 `var(--bg)`），蓝/墨主题里 card 为 rgba 白 8% / 4.5%；凡"蓝底白字"的徽标用 `var(--on-acc)`，否则在蓝主题里白底白字。
- 顶栏/HUD 跟随：每帧 `elementsFromPoint(中线, 40px)` 看顶栏下面是蓝/墨/页脚/蓝卡，是就给 `html[data-hdr=dark]` 切白字。
- 主角背后的**彩色圆盘** `.disc`：直径 ≈ 0.78×min(vh, 1.1vw)，圆心 = 主角投影点，每章换色，scale 随 p 0.55→1.05。

## 4. 签名动效清单（每个都有活代码）
| 动效 | 参考 | 代码位置（templates/immersive-bay） |
|---|---|---|
| 加载计数 000→100% | Lusion | index.html `#loader` + app.js `tickLoader/finishLoader` |
| 滚字 hover（字母上翻） | Lusion | `[data-roll]` → `.roll .ch:after{content:attr(data-c)}` |
| 自定义光标：点+环，模型上变 92px 蓝圆显示 DRAG / OPEN 03 / PLAY | Lusion | `#cursor` + `setCursor` |
| 磁吸按钮 | Lusion | `.pill` pointermove |
| 巨字从产品背后穿过 | Oryzo | `#backdrop .bd`（z0，canvas z1） |
| 构造线标注 + 可点击盘位标签 | Oryzo | `drawOverlay` + `mkCo` |
| 产品自转 + 圆形扩散换色 + 弹卡 + 度数计数 | Oryzo | `#spin` + `drawSpinBg`（clip-path circle 以主角投影为圆心）+ `.spin-pop` |
| 3D 文字丝带（真实前后遮挡、被拉出、字在流动） | Oryzo/Lusion | stage.js `RIB_N` 段：螺旋曲线 → 竖向带状网格 → CanvasTexture 重复；`setDrawRange` 控制拉出；**u 取负号**否则正面字镜像 |
| 盘位 sleeve 转场（从硬盘前板长到全屏） | 自研 | `drawSleeve`：驱动 rect = 前板 8 角投影包围盒 → lerp 到视口 |
| 圆角章节"幕布"从蓝色里升起 | More | `.chapter{border-radius:44px;box-shadow:0 -30px 80px -40px …}` |
| 大号彩色卡片堆叠切换 | More | `#deck`：440vh，下一张 yPercent 110→0 + rotate 5→0，上一张 scale .9 + brightness .72，底部进度条 |
| 全屏主张逐字点亮 | Lusion/Apple | `[data-stmt]`：SplitText chars，opacity .14→1 scrub，整体 scale .86→1 |
| 标题字符从遮罩升起 | More | `.sp` SplitText `mask:'lines'`，yPercent 115 + rotate 6 |
| 荧光笔划过 | 自有 | `.mk` background-size 0→100%（进入视口加 `.on`） |
| 倾斜卡片飞入 + 3D 倾斜 hover | More | `.stack` / `tilt()` |
| Max 卡流光描边 | Oryzo "Powered by AI" | `.spec.max:before` conic-gradient + `@property --ang` |
| 横向画廊：中心放大、两侧倾斜 | Oryzo | `.hgal` sticky + track x scrub + 按到中心距离 scale/rotate |
| 可拖拽素材条：中心放大、吸附 | Oryzo | `#adStrip` / `initStrip` |
| 跑马灯随滚速变速变向 | More/Lusion | `[data-mq]` |
| 价格带坐标轴（竞品点 + 我方区间条） | 自研 | `#ladder` |
| 配置比例对比条（KS 实际 vs 本次规划） | 自研 | `#mixbars` |
| SVG 环形图描画 | — | `buildDonut`（`data-seg="45:#2B50E0,…"`） |
| 甘特条逐行长出 / 时间线中轴随滚动填充 / 节奏柱升起 / 删除线划过 | — | `initScrollMotion` |
| 巨型页脚字标逐字升起 | More | `.wordmark span` scrub |
| 盘位 HUD（左下迷你盘位，当前章抽出 + 进度） | 自研 | `#hud` |
| 全屏菜单（clip-path 下拉 + 大号章节行） | Lusion | `#menu`，键盘 M / 1–5 |

## 5. 排版
- 中文大标题：Noto Serif SC 900，章节名 clamp(48px,7vw,124px)，letter-spacing −.045em。
- 拉丁巨字/数字：**Archivo 可变字宽**（`wdth 62..125`，用 font-stretch 66–80%，800 字重）——巨字、档位折扣、KPI、页脚字标都用它。
- 眉题/数据：IBM Plex Mono 12–13px，letter-spacing .14–.2em。正文 Noto Sans SC 16px，lede 20–25px。
- 章节头：左侧眉题（蓝色 DRIVE 徽标 + 编号 / 英文名）+ 衬线大标题，右侧描边巨号 `.bignum`。
- 子标题 `h3.sub-t[data-n="04.B"]`：编号作 `:before` 显示在同一行左侧。

## 6. 3D 主角规范
- 模型：GLB，**节点命名即接口**（Front_Cover、HDD_01…05、HDD_0X_Front_Plate、HDD_0X_Side_Label、Front_Status_LED）。换产品先确认可动部件是独立节点。**部件排列方向决定机位与标注**：Lucy v2 模型（2026-11-04）五块硬盘竖立、沿 X 横向并排（真实 Jonsbo N2 结构），所以每章相机 `tx` 跟随该盘 x 位置、标签印在硬盘左侧面（相机在左前方，拉出后正对镜头）、unbox 标签在盘位上方扇形展开 + 引线、尺寸线横在下方、HUD 是五个竖条。部件若上下叠放，则改为 `ty` 跟随、标签印顶面、标注沿左侧竖排。
- 白底打光：RoomEnvironment(0.03) + ACES 曝光 1.3 + 冷白主光(投影) + 蓝色轮廓光 + ShadowMaterial 地面(0.13) + 地面蓝色辐射光晕贴图。黑色机身在白底上要靠 rim 和 env 撑出边缘。
- 盘面标签：在 Side_Label 包围盒外 0.35mm 加平面（`rotation.y=-π/2` 朝 −X），CanvasTexture 写「DRIVE 0X / 中文章节名 / 英文 / 章节号」，**等字体加载完再画**。
- 可交互：raycast 只在 `interactive==='drives'` 时测硬盘；拖拽只在 `drag===true` 的场景。

## 7. 演示配套
沉浸版默认附带演讲稿 + 演讲者窗口（按 P），规范见 `reference/speech-presenter.md`。

## 8. 交付
文件夹 → `git init`（**不要推进外层别的项目仓库**）→ `gh repo create <name> --private --source=. --push` → `vercel deploy --prod --yes` 首发（会自动关联仓库）→ 之后 push main 即自动部署，部署后 curl 核验线上内容。`.vercelignore` 排除 `演讲稿.md`。

## 内容直达导航补充（2026-11）
会议跳读采用双层固定 headbar：章节入口与细分内容入口并存。预算、订单来源、广告素材、案例与平台资源分别定位到正文，不经部件转场；手机保留横滑细分按钮和完整目录。正文 `[data-nav][id]` 为唯一配置源，实现见 `section-navigation.md` 及母版 `assets/js/quick-nav.js`。
