# 修改记录（历史）

> 当前状态请看 `HANDOFF.md`。本文按时间叠加记录了各轮修改，其中部分做法已被后续版本替换；“迁移前历史交接记录”一节描述的是旧测试站，不是部署目标。

# 当前正式站配置（2026-10-13 迁移后）

后续修改与部署以这一节为准。本文后面的旧测试站说明仅用于历史参考，不能作为部署目标。

- **正式 Wix 编辑器**：https://w95182-website-153.editor.wix.com/html/editor/web/renderer/edit/e93701cd-75dc-4b40-a798-43c6c1b150d8?metaSiteId=c88dbc40-682a-4166-b4d3-12c2a4329ca9
- **目标域名**：https://www.biaxbew.com/ 。域名解析由用户处理，用户明确要求当前先不要管域名，不修改 DNS。
- **已发布的 Wix 临时地址**：https://w95182.wixsite.com/website-153
- **首页**：`tuckg`，仅更换首页内容，保留新站原有购物、结账等其他页面。
- **四个区块**：`comp-mv6d41ai`（a）、`comp-mv6d905m`（c）、`comp-mv6d905q`（b）、`comp-mv6d905s`（d）。
- **原生表单 Widget**：`comp-mv6dgng8`（首屏）、`comp-mv6dl8wh`（中段）、`comp-mv6dl8wm`（结尾）。
- **原生 FormContainer**：`comp-mv6dgny0`、`comp-mv6dl9f9`、`comp-mv6dl9g93`。
- **独立提交表**：`comp-mv6dgny0_Forms/contactForm10`，名称 `Genesis01 Launch Updates`。三个表单共用这张新建表；没有迁入 Brightin Star 的提交记录、表单绑定或弹窗。
- **新建成功弹窗**：`lflu4`，`Genesis01 Launch Survey`；提交后直接弹 Wix 原生问卷邀请弹窗。问卷链接 `https://forms.gle/DjiKNt7eVM2qXjoh7`，主 CTA `Take the survey`（新标签页打开），关闭项 `Maybe later`。图片使用用户上传的桌面键盘实拍，配置与组件 ID 见 `wix/survey-popup.json`。
- **素材映射**：`wix/media-map.production.json`。70 张产品图片已上传新站媒体库，与测试站素材 URL 不复用。
- **正式构建产物**：`wix/dist-production/gx-genesis.js`。`python3 wix/build_wix.py` 默认构建正式版；`wix/deploy.mjs` 默认指向新站。
- **目标清单**：`wix/production-target.json`。
- **迁移前备份**：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/migration-backup/`。
- **已验证**：桌面与手机首屏实际渲染、原生邮箱表单提交、独立成功弹窗。测试使用明确标识的 example.com 邮箱，未向 Brightin Star 表单写入。

## 整页细节调整（2026-10-15，Claude，已构建，待用户确认发布）

- 工艺横向长廊保留（用户要求不要删），只去掉与 CNC 短片重复的 `corner-black`、`edge-silver` 两张，剩 `lightbar`、`macro-aurum`、`side-rgb`。
- CNC 每段刀路揭开结束时，mask 里叠一块渐显的整幅白矩形（`.cnc__done`），避免上一张图的残影留在画面里（用户在 Finish 段看到过铣刀残留）。
- 屏幕同步：起始放大从 2.4/2.9 降到 1.55/1.8，纯屏幕画面从约两屏缩到不到一屏，键盘更早入镜。
- 定位区与 AI 灯效区之间的空白收窄（`.ai.ksp` 顶部留白）。
- 手机端：轴体刻度旁 "actuation" 字样被裁切 → 手机只显示 "1.1 mm"；续航数字旁小字被裁切 → 改小字号并允许换行。
- 打字演示键帽最多 6 个，避免压到右侧键盘图。
- 改前备份：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/backups/claude-v6-polish-20261015-1425/`。

## 工艺与轴体改成滚动短片（2026-10-15，Claude，已发布）

用户反馈：「Machined. Then refined.」和「Feel the difference.」图片单调、靠标签/滑块换图不优雅，要求参考竞品的动态表达。

- 参考：苹果 unibody（一整块铝 → 多道铣削）、Razer BlackWidow（轴体微距 + 分层）、Wooting 80HE（轴体 + 触发深度刻度）。截图在 `/Volumes/hyperdisk/biaxbew-landing-work/v5/refs/`。
- **工艺 `#cnc`**：替换原 `.story--craft`。整屏钉住 430vh，滚动推进四段：铝块（08）→ 光栅走刀揭开铣削（11）→ 螺旋走刀揭开阳极表面（05，扫光）→ 弧形走刀揭开黑色弧面（04）。转场是 SVG mask 里的刀路描边（带模糊软边），刀头有光点，切削时 canvas 飞铝屑；6063 计数；左下四段进度条。铝块/铣削两段标 Process visualization。
- **轴体 `#press`**：替换原 `.story--switch`。整屏钉住 380vh：真实轴体拆成轴心（`assets/v5/switch-stem.webp`）和轴体（`switch-housing.webp`）两层，滚动把轴心按下，右侧刻度尺同步；到 1.1 mm 触发时读数锁定发光、轴体亮起、光环扩散；继续按到底再回弹；最后单颗轴体退场，换成实装微距（12）并滚动计数到 50,000,000。刻度只标 1.1 mm，不标总行程（没有官方数据）。
- 两段都用 `scrubScene()`（ScrollTrigger 取进度 + 自己的插值缓动），不需要点击。旧 `.story` 的 CSS/JS 还在但页面已无 `.story` 元素。
- 新增 2 张图已上传正式媒体库；用户确认后已写入并发布，线上电脑（1440）和手机（390）核验两段都正常运行、无脚本报错。
- 改前备份：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/backups/claude-v5-craft-press-20261015-1242/`。

## 游戏屏幕与材质叙事（2026-10-15 当前发布版）

- 游戏图：`feature/15-gaming-screen.webp`，基于原始 `scene/gaming.webp` 生成，显示玩家、Genesis01 和游戏屏幕。新图已上传正式媒体库。
- Snap Key / MT / MDS / NKRO 增加小型 UI 图标；不改变功能定义，不作为产品图片替代。
- CNC：Machine / Finish / Form 三段摄影叙事。轴体：装机 / 透明轴体近景 / 实际使用三段；1.1 mm 和 50 million 独立于照片。
- 桌面粘性区随滚动切换，支持范围滑块与标签点选；可见时每 1.5 秒自动播放，手动操作暂停自动接管 5 秒，有暂停按钮。减少动态偏好禁用动画及自动播放。
- 原有五张细节轮播、原生表单、问卷和 DNS 不变。
- 已部署读回一致并发布；线上桌面、手机核验完成。浏览器使用 Ego Lite TaskSpace 7。
- 归档与截图：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-15-material-stories/`，见 review.html / QA.md / REFERENCES.md。

## 摄影重构 v2（2026-10-15 历史，部分升级为当前版）

- 用户否定了上一版拼图式示意界面。当前以真实质感的整张摄影为主，已经发布到正式站。
- 使用核验后的最新 taste-skill v2；只重构用户指出的五处，保留既有品牌与其他交互。详见本轮 DESIGN-READ.md / CRITIQUE.md。
- CNC 首图：`feature/11-cnc-hero.webp`，铣刀加工铝材的近景，明确为 Process visualization；不再使用三键盘叠放图。
- 工艺轮播：恢复 `craft/corner-black.webp`、`edge-silver.webp`、`lightbar.webp`、`macro-aurum.webp`、`side-rgb.webp` 五张静态原始产品照片，没有内嵌动画和重复合成卡片。
- 轴体：`feature/12-switch-macro.webp`，已安装轴体微距；1.1 mm / 50 million 独立排版，无行程示意动画。
- 连接：USB-C 延用 `03-wired.webp`；2.4 GHz 用 `13-wireless-desk.webp`；Bluetooth 用原始 `mode/bt.webp`。整张照片，标签与照片同步切换，1.5 秒自动播放，支持暂停/手动临时接管。
- 游戏：`feature/14-gaming-photo.webp`，真实操作构图；删除假按键/REGISTERED UI 和四帧后台序列；保留已有功能名，不编造 MT/MDS 行为。
- 新增四张 WebP 已上传新站媒体库。两个 Bluetooth 生成候选因键帽字符/布局变化淘汰。
- 原生表单、问卷、DNS 和其他 Wix 页面未改；部署前核对远端基线、写入读回一致，发布成功。线上桌面/手机与本地三宽度检查见本轮 STATUS.md。
- 本轮目录：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-15-photo-rebuild-v2/`。

## 缺失卖点画面补齐（2026-10-15 历史，示意方案已被替换）

- 用户要求缺失素材也由我们研究竞品并生成；不再把“没有素材”当作页面表达缺口留给用户。
- 新生成 3 张并全部采用：`08-aluminum-stock.webp`、`09-switch-cutout.webp`、`10-receiver-illustration.webp`。后两张有真实透明通道。
- CNC 增加 Material → Machine → Finish 自动序列；轴体换成透明背景的轴体与键帽组合，独立 1.1 mm 数字，下面加入行程与触发示意；2.4GHz 补充接收器示意；游戏区补充自动多键输入与 REGISTERED 同步反馈。
- 自动阶段统一 1.5 秒；游戏实拍帧也调整为 1.5 秒。示意标注保留，不冒充实际软件或实物录音。声音按钮默认关闭，开启后跟随自动打字播放合成演示音。
- Snap Key / MT / MDS 的具体固件行为尚未有产品说明支持，保留原有功能名称，不复制竞品实现；NKRO 演示对应已有明确产品卖点。
- 参考、提示词、候选、采用图、发布备份及 QA：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-15-remaining-features/`。
- 原生表单、问卷弹窗和 DNS 未修改。新 bundle 已写入读回一致并发布；详见本轮 STATUS.md。

## 按卖点制作素材并发布（2026-10-14 历史）

- 用户允许自行判断风格并全面推进。本轮生成 11 张，采用 7 张；4 张桌面/创作场景因键帽、字标或结构漂移退回，保留原实拍。
- `assets/feature/01-cnc.webp` 到 `07-focused-work.webp` 已上传正式 Wix 媒体库，并在正式首页使用。素材网页版合计约 0.8 MB。
- 三联定位区：机械轴体配实际轴体与键帽，金属工艺配黑色弧面，修复原来的图文错配。
- 工艺横向段落：黑色曲面、银色 6063、CNC 工艺示意＋成品、黑银阳极表面、整机比例。CNC 明示 Process illustration；无真实工厂拍摄声明。桌面随滚动横移，手机自动每 1.5 秒切换，触摸后短暂停留。
- 轴体：`sw__composition` 使用 02-switch，左侧独立 1.1 mm 留白、右侧轴体＋键帽、下方真实装机细节。覆盖旧版单颗透明轴体的排版；旧素材保留未删除。数字无大面积遮挡产品。
- 连接：`mode__frame` 替代原 3 张背景照片结构；有线为实际接口插接示意，2.4 GHz / Bluetooth 为原实物透明图＋连接关系示意。只有 wired 和 2.4 GHz 标 1000 Hz。
- 屏幕同步：06-screen-sync 清理道具，屏幕和键盘同蓝色；桌面末段缩放 1.65，减少产品压到文案。保留原滚动镜头关系。
- 办公场景用 07-focused-work；其余三个场景、真实 AI 灯效帧、底板刻纹、续航亮灭对比保留。
- 完整参考、提示词、候选和退回原因：`/Users/madspace20250515/Documents/ChatGPT/Biaxbew/visual-upgrade/2026-10-14-feature-calibration/`。`STATUS.md` 和 `QA-RESULTS.md` 为当前结论；旧校准文档仅记录当时状态。
- 发布前远端 bundle 与备份相等，写入后逐字读回一致，Wix 显示已发布并上线；正式地址已验证新结构和新素材。
- 本轮没有重测表单提交，只确认三个原生表单仍在；表单绑定、问卷弹窗、优惠和 DNS 未修改。
- 本轮当时的证据边界：无真实 CNC 过程、接收器特写、软件录屏或轴体录音。2026-10-15 已补充明确标注的生成画面与前端演示，详见上方最新段落。

## AI 灯效自动演示（2026-10-13 最新）

- 用户要求不再需要打字：灯效区已改成 Lighting Studio 浅色柔和卡片，没有输入框、发送按钮或聊天气泡。
- `#ai-typed` 自动逐字显示 “I want / Forest Rain.” 等 9 种灯效示例，随后实拍切换到对应色，结果卡片反馈，再自动进入下一项。
- 使用滚动/尺寸/可见性事件加每秒位置校验进入可见区域即播放（绕过 Wix 上观察器未触发的问题）；灯效帧提前加载。离屏停止打字计时器，再次进入继续。减少动态效果偏好下直接显示首项并应用灯效，不进行循环打字。
- 参考 Typeless 官网的柔和卡片与大字输入展示；这仍然是实拍联动的前端自动演示。

## 工艺与轴体层级展示（2026-10-13）

- 2026-10-14：工艺区开头已按用户要求改为无背景放大铺展。`assets/craft/ensemble-cutout.png` 为透明 RGBA 三机组合，内置 image_gen 以 `9-22静物产品/09-220626.jpg` 提取，提示词保存在 `assets/craft/ensemble-cutout.prompt.md`。旧 ensemble.webp 保留但不再用于该屏。
- 桌面三机画面向右铺展，滚动从 .9 放大至 1.07 并轻微展开角度，左文案保持可读；overview 使用 overflow:clip 限制出屏画面避免横向滚动。手机改为文案下方整组展示，.96 到 1 的轻微放大。
- 旧版轴体区（已由上方 2026-10-14 素材升级替换）`.sw__depth` 使用透明 RGBA 图 `assets/sw/ice-snow-cutout.png`（内置 image_gen；提示词见同目录 .prompt.md）。轴体与数字 1.1 共用中轴，mm 独立放右侧；补充轻微环形投影和下方 `assets/sw/macro.webp` 实装近照，避免孤立展示。数字保留计数，产品轻微滚动位移。没有爆炸结构，未套用 45gf。
- 次级规格保留 50M keystrokes / Linear travel；原生表单、问卷弹窗及 AI 对话区未调整。
- 新素材已上传正式站媒体库并加入正式映射。构建命令保持不变。

## 自动播放间隔（2026-10-14）

- `js/main.js` 中 `AUTOPLAY_MS = 1500` 统一控制卖点自动切换、底板、连接模式、场景轮播、AI 灯效完成后的停留及页面辉光轮换。
- 打字字符速度、画面过渡、滚动动画与用户临时接管后的恢复延迟保持各自原值。

## 后续修改与部署

```bash
cd ~/claudcode\ d/biaxbew-landing
python3 wix/build_wix.py
# 写入正式站草稿：
NO_PUBLISH=1 ego-browser nodejs < wix/deploy.mjs
# 在用户要求发布时：
ego-browser nodejs < wix/deploy.mjs
```

- 唯一源码仍为 `index.html`、`css/style.css`、`js/main.js`；保持当前首屏与打字演示已确认的紧凑版式。
- Wix 仍是整站发布。只操作正式站首页和本次新建成功弹窗；不要修改其他页面。
- **Brightin Star 内容不要迁移**；旧 `/test` 留作历史测试，不是未来默认部署目标。
- 文案事实源仍为原飞书英文定稿；不要自行改正文。

---

# 以下为迁移前历史交接记录

# biaXbew Genesis01 预热页 — 交接文档

写给接手修改的人（Codex）。先读完「改页面的流程」和「不能踩的坑」再动手。

## 1. 这是什么

biaXbew Genesis01（AI 灯效机械键盘）的欧美 Kickstarter 预热落地页。目前部署在一个 Wix 站点的测试页上：

- 线上地址：<https://www.brightinstarlens.com/test>
- 这个站点是 **Brightin Star（另一个品牌）的正式站**，只是借它的 `test` 页做测试。**除 test 页外，站内任何页面都不要动。**
- 状态：电脑版和手机版都已上线到 test 页；表单是临时的（见第 6 节）。

## 2. 文件在哪

| 位置 | 内容 |
|---|---|
| `~/claudcode d/biaxbew-landing/` | 页面源码（本文件所在目录） |
| `index.html` / `css/style.css` / `js/main.js` | **唯一的源码**，独立可运行的静态页 |
| `assets/` | 处理后的图片（webp/png/jpg），约 9MB |
| `wix/build_wix.py` | 把源码打包成 Wix 自定义元素脚本 |
| `wix/dist/gx-genesis.js` | 打包产物，上传到 Wix 的就是它（不要手改） |
| `wix/dist/host.html` | 本地模拟 Wix 页面结构的测试页 |
| `wix/deploy.mjs` | 上传图片 + 写入 Wix + 发布 |
| `wix/vendor/` | GSAP 3.12.5 和 ScrollTrigger，打包时内联进脚本 |
| `/Volumes/hyperdisk/BIAXBEW 键盘/` | 原始素材 1144 张（32G），只读，不要改 |
| `/Volumes/hyperdisk/biaxbew-landing-work/` | 工作目录：`scripts/`（图片处理脚本）、`thumbs/`（全量缩略图）、`sheets/`（素材总览图）、`wix_media_map.json`（本地图片 → Wix 媒体库地址的映射） |

文案事实源是飞书表 `https://gq8lolan5ig.feishu.cn/sheets/U3cwsKmOlhwJbVtBrdCcZrWonOc` 的 Sheet1 C 列（英文定稿）。**正文文案不要自己改写**；配图说明、小标签是我补的，可以调整。

## 3. 改页面的流程

```bash
cd ~/claudcode\ d/biaxbew-landing

# 1. 改源码：index.html / css/style.css / js/main.js

# 2. 本地看独立版
python3 -m http.server 8787 --bind 127.0.0.1
#    http://127.0.0.1:8787/index.html

# 3. 打包 Wix 版，并在本地模拟页里看
python3 wix/build_wix.py
#    http://127.0.0.1:8787/wix/dist/host.html

# 4. 部署到 Wix test 页（会发布整站，见第 5 节）
ego-browser nodejs < wix/deploy.mjs
```

说明：

- `deploy.mjs` 如果发现有新图片，会先上传并退出，提示你重新 `build_wix.py` 再部署一次（因为打包时要用到新图片的 Wix 地址）。
- 换了某张已有图片的内容：先从 `wix_media_map.json` 里删掉对应的 key，再部署，才会重新上传。
- 只想写入不发布：`NO_PUBLISH=1 ego-browser nodejs < wix/deploy.mjs`。
- 需要 Ego Lite 已登录 Wix 账号。浏览器操作按用户规定一律用 `ego-browser`。

**验证只能看发布后的线上页面。** Wix 编辑器的「预览」里自定义元素被关在隔离框里，是空白的，不能用来验证。

## 4. 页面是怎么搭在 Wix 上的

用的是 Wix 的「自定义元素」，代码直接运行在 Wix 页面里（不是 iframe），所以滚动动效能跟着 Wix 页面走。

- test 页有 4 个区块，每个放一个 `<gx-genesis>`，用属性 `part` 区分：`a`（首屏到底板）、`c`（中段订阅条）、`b`（冰雪轴到场景轮播）、`d`（结尾和页脚）。
- 脚本存在站点代码文件 `public/custom-elements/gx-genesis.js`，图片在站点媒体库文件夹 `biaxbew-genesis01`。没有任何外部托管。
- `build_wix.py` 做的事：给所有 CSS 加 `.gxg` 前缀、去掉独立版的丝滑滚动和自制表单、把 HTML 切成四段、表单的位置留一个空的 `.slot`。
- **三处邮箱表单是 Wix 原生表单**，叠在 a / c / d 三个区块上。脚本里的 `layout()` 在运行时把每个表单移到对应的 `.slot` 上，所以改版式时只要保证 `.slot` 在该在的位置，表单会自己跟过去。
- 首屏区块有一张 Wix 原生背景图（键盘静帧），脚本加载前先显示它，避免黑屏；脚本和键盘图就绪后自动隐藏。改了首屏键盘的位置或大小后，这张静帧需要重新截取并替换，否则切换时会跳。

Wix 侧的标识（改编辑器结构时用）：

- 编辑器：`https://w95182-website-125.editor.wix.com/html/editor/web/renderer/edit/f46dda4a-978a-482d-a20b-37bb50665701?metaSiteId=1f7c15fe-7ecc-4842-bab6-a546e500f8c0`
- test 页 id：`dghhm`
- 四个区块：`comp-mv65ar0r`（a）、`comp-mv65txup`（c）、`comp-mv65txwi`（b）、`comp-mv65txye`（d）
- 三个表单：`comp-mv65ujn3`（首屏）、`comp-mv65vfuy`（中段）、`comp-mv65vhfh`（结尾）
- 编辑器内部接口入口：`document.getElementById("preview").contentWindow.documentServices`

## 5. 不能踩的坑

**发布相关**
- Wix 的发布是**整站发布**，会把 Brightin Star 其他页面的草稿改动一起推上线。用户已同意为测试 test 页而发布，但每次发布前应确认没有别人正在改这个站。
- 不要提交表单做测试（见第 6 节）。

**Wix 环境**
- Wix 有一条样式会把自定义元素的宽度压回 980px，所以根元素的 `width` 必须带 `!important`（已处理，别删）。
- 自动播放、数字动画的触发一律用 `IntersectionObserver`（源码里的 `watch` / `zone` / `onSeen`）。**不要用 ScrollTrigger 的 `onToggle` 判断"是否在屏幕里"**：Wix 页面里它算出的位置会过期，表现就是"不自动切换"。ScrollTrigger 只用于跟随滚动的那几个效果。
- 手机版是 Wix 里一套独立的布局（宽 320）。**手机布局中表单的位置必须和自定义元素重叠**，否则 Wix 会把表单排到下方并留出一条缝。
- Wix 要等自己的页面加载完才会请求我们的脚本，发布后的第一次访问更慢。这是平台行为。

**样式**
- 渐变色文字（"20+"）的子元素不能单独加位移或缩放，否则文字会消失；动画要加在渐变的那一层上。
- 全局要保留 `img { height: auto }`，否则带宽高属性的图片会被压扁。

**素材**
- 灯效连拍是手持拍的，必须先对齐才能做无跳动切换，对齐脚本在 `biaxbew-landing-work/scripts/`（`lib.py`、`a_seq.py`、`d_misc.py`、`b_rect.py`、`c_assets.py`）。
- 原片里反复出现一块绿色 "RELAXED" 灯牌，是道具，裁图时尽量避开。

## 6. 还没解决的事

1. **表单是临时的。** 现在三处表单是从 Brightin Star 首页表单复制来的，仍然指向首页那一个表单：提交会进同一张提交记录，提交后弹出的也是首页的「歐美燈箱」。正式用之前必须换成 biaXbew 自己的表单和弹窗，需要用户确认怎么建。**在此之前不要提交表单**，否则会往 Brightin Star 的真实数据里写入测试邮箱。
2. **表单提交和弹窗从未测试过。**
3. **最终落在哪个站没定。** 如果搬到 biaXbew 自己的 Wix 站，那个站也必须是付费套餐并绑定域名（自定义元素的前提）。搬的时候需要：新站建四个区块和自定义元素、重新上传图片（生成新的映射）、新建表单。
4. **手机版没在真机上看过**，只用模拟的 iPhone 尺寸检查过。屏幕同步那一段手机版最后一次调亮也没有再截图确认。
5. **手机版的工艺长廊**是左右滑动的一排图，不滑只能看到第一张，和"不需要用户操作"的要求不完全一致。
6. **首屏静帧**和真实键盘的位置大小略有差别，切换瞬间有轻微跳动；宽屏上表单在脚本加载后会动一下。
7. **卡顿**：已去掉最耗性能的效果，但没有可靠的帧率数据，是否够流畅以用户实际感受为准。

## 7. 用户已经明确的要求

这些是多轮反馈里定下来的，后续修改不要违反：

- 结构和 CTA 按范例页：首屏、中段、结尾各一个邮箱框，文案是 "Launching Soon on Kickstarter / Sign up now and enjoy over 30% OFF"，Kickstarter 用官方标志图。
- 邮箱收集必须是 **Wix 原生表单**，输入框直接在页面上、只输一次、提交后直接弹 Wix 弹窗。不接受常驻底栏，不接受自己写代码存邮箱。
- **页面上不能有"必须点击才出现"的内容。** 所有切换都要自动播放或跟随滚动；用户操作只是临时接管。
- 轮播切换间隔要短（约 2.5 到 3 秒），不要"鼠标悬停就暂停"。
- 页面上的数字和规格要有动效（滚动计数加落地弹跳）。
- 不要开场加载动画。
- 不要给画面加说明性标签（比如 "Screen" / "Desk"）。
- 每个卖点画面的落点必须是键盘本身，屏幕、桌面这些只做过场。
- 交互时页面辉光不要乱变色。
- 同一组图片的尺寸比例要一致。
- 设计上不要"AI 味"：不用白底圆角卡片阵列、通用线性图标、手绘的假界面；素材不要裸用，要裁切调色。
- 用户说"有些地方不行"时，只改指出的那几处，不要全局重做。

## 8. 页面区块一览（从上到下）

| 区块 | 做了什么 |
|---|---|
| 首屏 | 3D 键盘跟随鼠标倾斜；滚动时放平并穿入痛点文案，痛点逐词点亮 |
| 定位 | 三联图自动轮换展开 |
| 01 AI 灯效 | 9 张对齐过的实拍，自动切换，也可输入或点词条 |
| 02 屏幕同步 | 从屏幕拉远，再推向键盘并压暗周围；后接 "20+" 双排流动图 |
| 03 机身工艺 | 横向滚动长廊（5 张同比例）；三块雕刻底板 3D 叠层自动轮换 |
| 中段订阅条 | Wix 原生表单 |
| 04 冰雪轴 | 自动打字演示，访客敲键盘可接管，带合成按键声 |
| 05 三模连接 | 三张图自动轮换 |
| 06 长续航 | 随滚动把灯光"擦掉"的对比图，可拖动；2,000 小时计数 |
| 07 游戏设置 | 4 帧实拍循环播放按键灯光扩散 |
| 场景轮播 | 4 个场景自动切换 |
| 结尾 | Wix 原生表单 |
