# biaXbew Genesis01 预热页 · 交接文档

更新：2026-10-15。本文只写**当前状态**。各轮修改过程见同目录 `HANDOFF-history.md`。

---

## 亮银主款更新（2026-10-16 最新发布版）

- 用户最终方向：以亮银为主要展示款；用户撤回了所发三款标色图的准确性，不依据该图辨认黑色/烟枪灰。
- 首屏改为 `assets/obj/hero-silver-rgb.webp`（完整键帽），立体侧边/底座 CSS 同步为银色；Wix 原生首屏占位图同步为 `assets/poster-hero-silver.png`。
- 用户确认第二屏是屏幕联动场景：蓝/橙/紫三帧局部修正银色上边框 + 黑色前下壳的不一致。新素材为 `feature/17-sync-silver-{blue,amber,violet}.webp`，保留原构图和灯色；旧素材保留。
- 产品定位第三图使用原有银色雕刻实拍 `pos/genesis.webp`；CNC 末段改为原有银色弧面实拍 `craft/edge-silver.webp`。
- 其他游戏/办公/咖啡馆等场景、灯效时序、表单、问卷与 DNS 未修改。生成素材 4 张，全部通过本轮视觉检查。
- 本轮目录：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-16-silver-primary/`，含源码及远程草稿备份、生成提示词、原图、核验截图。

## 大幅背板与屏幕联动前置（2026-10-15 最新发布版）

- 屏幕联动 `#ambiance` 直接放在 hero/pain 后、positioning 前。蓝色原图加暖橙/紫粉两张生成变体，1.5 秒切换，支持暂停/手动选择；画面保留屏幕和完整键盘。
- 背板改为单块横向大幅展示，桌面宽度为视口 94%，不再堆叠、倾斜压缩和调暗。AURUM/LUMEN/AUREA 标签可切换，有暂停按钮。
- Lighting Studio 全部调整成深色表面/浅色文字。
- 连接区改为 USB-C、2.4 GHz、Bluetooth 三组静态图标，删除该区轮播图和轮播脚本。
- 新精修共 34 张已扫描，采用 139/134/133/154 四张更新底部四个场景。原图未修改，WebP 位于 assets/retouched。
- 新增两张颜色图位于 assets/feature/16-sync-amber.webp 和 16-sync-violet.webp；6 个新素材已上传正式 Wix 媒体库。
- 现有 CNC、轴体和其他交互按本轮开始时的最新源码保留；原生表单/问卷/DNS 未改。
- 归档：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-15-immersive-refinement/`。正式发布已确认，备份/提示词/素材清单/截图均在该目录。

## 1. 项目是什么

biaXbew（飙虬）Genesis01 AI 灯效机械键盘，欧美 Kickstarter 预热落地页。页面唯一目标是收集邮箱。

- 线上地址：<https://www.biaxbew.com/>（Wix 临时地址 <https://w95182.wixsite.com/website-153>）
- 搭建方式：自己写的网页，以 Wix「自定义元素」的方式嵌进 Wix 首页；三处邮箱框是 **Wix 原生表单**。
- 状态：电脑版、手机版都已上线。手机版只用浏览器模拟 iPhone 尺寸检查过，**没在真机上看过**。

---

## 2. 交接包里有什么

| 文件夹 | 内容 |
|---|---|
| `biaxbew-landing/` | 页面源码、处理好的图片、构建和部署脚本。**日常修改只用这个** |
| `material-scripts/` | 当初处理原始照片的 Python 脚本（对齐灯效连拍、抠图、裁切调色）。重做素材时才用 |

**不在包里、需要单独交接的：**

| 内容 | 位置 | 说明 |
|---|---|---|
| 原始素材 1144 张（32 GB） | 外接硬盘 Hyperdisk：`BIAXBEW 键盘/` | 品牌方拍摄原片。只读，不要改 |
| 素材工作目录（1.1 GB） | Hyperdisk：`biaxbew-landing-work/` | 全量缩略图、素材总览图、竞品截图 |
| Codex 各轮记录（411 MB） | `~/Documents/ChatGPT/Biaxbew/` | 每轮修改前的备份、截图、参考、提示词 |

---

## 3. 交接时要办的账号权限

| 事项 | 怎么办 |
|---|---|
| Wix 站点 | 在 Wix 后台「设置 → 角色与权限」邀请同事为协作者。需要能改代码、上传媒体、发布、看表单提交。不要直接给原账号密码 |
| 域名 biaxbew.com | DNS 由原负责人管理。交接时说明在哪个注册商、谁负责续费。**目前不要改 DNS** |
| 飞书文案表 | 「预热页文字结构」：<https://gq8lolan5ig.feishu.cn/sheets/U3cwsKmOlhwJbVtBrdCcZrWonOc>，给查看权限 |
| 问卷 | 成功弹窗里的 Google 表单：<https://forms.gle/DjiKNt7eVM2qXjoh7>，需要看回收数据的话加协作者 |
| 邮箱数据 | Wix 表单提交表 `Genesis01 Launch Updates`。之前测试提交过 example.com 的测试邮箱，交接前确认是否删除 |

---

## 4. 页面结构（从上到下）

所有自动切换的间隔由 `js/main.js` 里的 `AUTOPLAY_MS = 1500` 统一控制。

| 区块 | 标题 | 做了什么 |
|---|---|---|
| 首屏 | An AI Lighting Mechanical Keyboard That Brings Your Ideas to Light. | 3D 键盘跟随鼠标倾斜，滚动时放平并穿入痛点文案，痛点逐词点亮。**原生表单 1** |
| 定位 | Your Light. Your Feel. Your Genesis. | 三联图自动轮换展开 |
| AI 灯效 | Turn Your Ideas into Light. | Lighting Studio 卡片自动逐字输入 9 种灯效描述，旁边的实拍键盘同步切换对应灯光（9 张对齐过的同机位实拍） |
| 屏幕同步 | Bring Your Screen’s Colors to Your Desk. | 从屏幕画面拉远，再推向键盘并压暗周围；后接 "20+" 灯效两排流动图 |
| 机身工艺 | Machined. Then refined. | 整屏滚动短片：铝块 → 光栅走刀揭开铣削 → 螺旋走刀揭开阳极表面 → 弧形走刀揭开黑色弧面。之后是 3 张横向长廊（灯条、底板雕刻、银色端盖）和三款底板 3D 叠层自动轮换 |
| 中段订阅条 | Sign up now and enjoy over 30% OFF | **原生表单 2** |
| 轴体 | Feel the difference. | 整屏滚动短片：真实轴体拆成轴心和外壳两层，滚动按下，刻度尺到 1.1 mm 时触发发光，按到底回弹，最后切到实装微距并计数到 50,000,000。之后是打字演示（访客敲自己的键盘会弹出发光键帽） |
| 三模连接 | Three modes. One keyboard. | USB-C / 2.4 GHz / Bluetooth 三张图自动轮换 |
| 续航 | From Full Immersion to Quiet Focus. | 同机位亮灯/关灯对比，随滚动把灯光"擦掉"，也可拖动；2,000 小时计数 |
| 游戏设置 | Play it your way. | 游戏场景实拍 + Snap Key / MT / MDS / NKRO |
| 场景轮播 | One keyboard, four desks | 4 个场景自动切换 |
| 结尾 | Give Your Next Setup a Light of Its Own. | **原生表单 3**；页脚 |

提交邮箱后弹出 Wix 原生弹窗 `Genesis01 Launch Survey`，引导填问卷（文案见 `wix/survey-popup.json`）。

---

## 5. 工作原理

1. **页面代码**：源码是一个普通静态网页（`index.html`、`css/style.css`、`js/main.js`）。`wix/build_wix.py` 把它打包成一个脚本文件 `gx-genesis.js`，里面注册一个自定义标签 `<gx-genesis>`。
2. **放进 Wix**：
   - 脚本存在 Wix 站点自己的代码文件 `public/custom-elements/gx-genesis.js`。
   - 图片在 Wix 媒体库文件夹 `biaxbew-genesis01`，没有任何外部托管。
3. **分段**：Wix 首页有 4 个区块，每个放一个 `<gx-genesis>`，分别显示页面的 a（首屏到底板）、c（中段订阅条）、b（轴体到场景轮播）、d（结尾和页脚）。
4. **表单对位**：三个 Wix 原生表单叠在 a / c / d 区块上。页面在该放邮箱框的地方留了空位（`.slot`），脚本运行时把 Wix 表单挪到空位上。改版式时只要空位在对的位置，表单会跟过去。
5. **数据**：表单的提交、存储、提交后的弹窗全部是 Wix 自己的，页面代码不经手邮箱。
6. **首屏占位**：首屏区块有一张 Wix 原生背景图（键盘静帧），脚本到之前先显示它，避免黑屏。**改了首屏键盘的位置或大小，这张静帧要重新截取替换**。

---

## 6. 修改和发布

### 需要的环境
- Python 3、Node。
- Ego Lite（命令 `ego-browser`），并登录有该 Wix 站点权限的账号。部署脚本靠它打开 Wix 编辑器写入代码并发布。
- 只有重做素材才需要：Python 的 Pillow、OpenCV、rembg。

### 流程
```bash
cd biaxbew-landing

# 1. 改源码：index.html / css/style.css / js/main.js

# 2. 本地预览独立版
python3 -m http.server 8787 --bind 127.0.0.1
#    浏览器打开 http://127.0.0.1:8787/index.html

# 3. 打包 Wix 版
python3 wix/build_wix.py
#    产物：wix/dist-production/gx-genesis.js
#    本地模拟 Wix 页面：http://127.0.0.1:8787/wix/dist-production/host.html

# 4. 只写入 Wix 草稿，不发布
NO_PUBLISH=1 ego-browser nodejs < wix/deploy.mjs

# 5. 写入并发布（整站发布，见第 8 节）
ego-browser nodejs < wix/deploy.mjs
```

- 部署命令要在 `biaxbew-landing` 文件夹里运行。
- 新加了图片：第一次运行 `deploy.mjs` 会先上传到 Wix 媒体库并退出，提示重新打包。重新运行 `build_wix.py` 后再部署一次。
- 换掉某张已有图片的内容：先在 `wix/media-map.production.json` 里删掉那张图对应的条目，再部署，才会重新上传。
- **只能在发布后的线上页面验证效果。** Wix 编辑器的「预览」里自定义元素被关在隔离框里，是空白的。
- `deploy.mjs` 去掉了写死的本机路径之后，还没有完整跑过一次部署，第一次用时留意输出。

---

## 7. Wix 里的标识

| 项目 | 值 |
|---|---|
| 编辑器 | https://w95182-website-153.editor.wix.com/html/editor/web/renderer/edit/e93701cd-75dc-4b40-a798-43c6c1b150d8?metaSiteId=c88dbc40-682a-4166-b4d3-12c2a4329ca9 |
| 首页 id | `tuckg` |
| 四个区块（a / c / b / d） | `comp-mv6d41ai` / `comp-mv6d905m` / `comp-mv6d905q` / `comp-mv6d905s` |
| 三个表单（首屏 / 中段 / 结尾） | `comp-mv6dgng8` / `comp-mv6dl8wh` / `comp-mv6dl8wm` |
| 提交数据表 | `comp-mv6dgny0_Forms/contactForm10`（Genesis01 Launch Updates） |
| 成功弹窗 | `lflu4`（Genesis01 Launch Survey） |
| 编辑器内部接口入口 | 编辑器页面里 `document.getElementById("preview").contentWindow.documentServices` |

同样的信息也在 `wix/production-target.json`。

---

## 8. 必须遵守的规则

### 客户（项目负责人）明确要求过的
- **结构和 CTA**：
  - 首屏、中段、结尾各一个邮箱框。
  - 文案 "Launching Soon on Kickstarter / Sign up now and enjoy over 30% OFF"。
  - Kickstarter 用官方绿色字标图。
- **邮箱收集**：
  - 必须是 Wix 原生表单，输入框直接在页面上，只输一次，提交后直接弹 Wix 弹窗。
  - 不接受常驻底栏，不接受自己写代码存邮箱。
- **不要有"必须点击才出现"的内容**：
  - 所有切换要自动播放或跟随滚动，用户操作只是临时接管。
  - 轮播间隔要短，不要"鼠标悬停就暂停"。
- **动效**：
  - 数字和规格要有动效（滚动计数 + 落地弹跳）。
  - 不要开场加载动画。
  - 交互时页面辉光不要乱变色。
- **画面**：
  - 每个卖点画面的落点必须是键盘本身，屏幕、桌面只做过场。
  - 不要给画面加说明性标签（如 "Screen" / "Desk"）。
  - 同一组图片尺寸比例要一致；同一个镜头不要在页面里重复出现。
  - 素材不要裸用，要裁切调色。
  - 卖点表达参考竞品的动态做法（苹果、Razer、Wooting 等），用动效讲清卖点，不要"标签 + 滑块换图"。
- **设计**：不要"AI 味"，不用白底圆角卡片阵列、通用线性图标、手绘假界面。
- **反馈怎么改**：说"有些地方不行"时只改指出的那几处，不要全局重做；说删某部分时，先确认是删整块还是只删重复内容。
- **发布**：每次发布前都要得到负责人同意。

### 文案
- 正文以飞书表 C 列英文定稿为准，不要自己改写。
- 以下标题和补充句**不是飞书原句**（之前改的或补的），需要时请品牌方确认：
  - 标题：Machined. Then refined.、Feel the difference.、Three modes. One keyboard.、Play it your way.
  - 工艺短片：Genesis01 begins as a solid block of aerospace-grade 6063 aluminum. / Rounded front and back contours, set in golden-ratio proportions.
  - 底板：AURUM / LUMEN / AUREA 三款的名称和副标，是从实物雕刻上读出来的。

### 技术上的坑
- **Wix 发布是整站发布**，会把站内其他页面未发布的草稿一起推上线。
- Wix 有一条样式会把自定义元素宽度压回 980px，根元素宽度必须带 `!important`（已处理，别删）。
- **判断"元素在不在屏幕里"一律用 `IntersectionObserver`**（源码里的 `watch` / `zone` / `onSeen`）。不要用 ScrollTrigger 的 `onToggle`，在 Wix 里它算出的位置会过期，表现为"不自动切换"。ScrollTrigger 只用于跟随滚动的效果。
- Wix 手机版是独立的 320 宽布局。手机布局里表单的位置必须和自定义元素重叠，否则 Wix 会把表单排到下方留出白缝。
- 渐变色文字（"20+"）的子元素不能单独加位移缩放，否则文字消失。
- 全局要保留 `img { height: auto }`，否则图片会被压扁。
- 灯效连拍是手持拍的，必须先对齐才能做无跳动切换（`material-scripts/align.py`、`lib.py`）。
- 原片里反复出现一块绿色 "RELAXED" 道具灯牌，裁图时尽量避开。

---

## 9. 未完成和待确认

1. 手机版没有在真机上看过。
2. 场景轮播 Desk Styling 的画面里 RELAXED 灯牌很显眼，要去掉需要修图。
3. 第 8 节列出的非飞书原句文案，需要时请品牌方确认。
4. 表单提交表里的 example.com 测试数据是否删除。
5. 项目没有用 Git，建议放进私有仓库后再继续修改。

---

## 10. 文件夹说明

```
biaxbew-landing/
├── index.html / css/style.css / js/main.js   唯一的源码
├── assets/            处理后的图片（webp/png/jpg）
│   ├── seq/           AI 灯效 9 张对齐实拍
│   ├── v5/            轴体拆层（轴心、外壳）
│   ├── feature/       各卖点主图（部分为生成的工艺示意图）
│   └── …
├── wix/
│   ├── build_wix.py              打包脚本
│   ├── deploy.mjs                上传图片 + 写入 Wix + 发布
│   ├── media-map.production.json 本地图片 → Wix 图片地址
│   ├── production-target.json    Wix 组件标识
│   ├── survey-popup.json         成功弹窗配置
│   ├── vendor/                   GSAP 动效库（打包时内联）
│   └── dist-production/          打包产物（自动生成，不要手改）
├── HANDOFF.md            本文
└── HANDOFF-history.md    各轮修改记录
```

## 2026-10-16 — Feishu approved English copy, revision 134
- Source: https://gq8lolan5ig.feishu.cn/sheets/U3cwsKmOlhwJbVtBrdCcZrWonOc?sheet=a3c4a7 ; English column C, rows 4–40.
- Replaced English marketing headings/body with approved copy. Retained current section order, images, autoplay timing, native forms and interactions.
- User explicitly requested no new selling-point blocks: 75% layout paragraph appended to positioning; modified tray, PC plate, acoustic foam and IXPE descriptions integrated into switch section without separate headings/cards.
- CNC copy includes gem-cut side lighting, UV-printed artwork and WorkBuddy AI. Removed obsolete engraved/engraving descriptions from visible copy and alt labels.
- Functional controls and survey popup copy are not supplied by this sheet and remain unchanged.
- Backup/source/audit/screenshots: `/Users/madspace20250515/Documents/ChatGPT/Biaxbew/copy-update/2026-10-16/`.
- Built via `python3 wix/build_wix.py`; syntax checked. Remote file baseline compared before write; exact read-back verified; Wix publish success dialog confirmed.
