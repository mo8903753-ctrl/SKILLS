# immersive-bay 模板 · 改造指南

这是 Cephalon Lucy AI Studio 日本方案站的完整源码（2026-11 定稿版），作为沉浸版母版。体系说明见 `../../reference/immersive-system.md`，演讲稿规范见 `../../reference/speech-presenter.md`。

## 本地运行
```bash
cd templates/immersive-bay && python3 -m http.server 8765   # 打开 http://127.0.0.1:8765
```
必须走 http（GLB 是 fetch 加载）；file:// 双击会在加载页提示。

## 文件职责
| 文件 | 改什么 |
|---|---|
| `index.html` | 全部方案内容。场景：`#hero` `#spin` `#unbox` `#d1…#d5` `#outro`；章节：`.chapter#ch1…ch5`；色块：`<div class="band" data-theme="ice|blue|ink">`；全屏主张：`[data-stmt]`；彩色卡片堆叠：`#deck` |
| `assets/css/site.css` | tokens 在顶部 `@property` + `:root` + `.chapter[data-t=…]`；一般不用改 |
| `assets/js/app.js` | `LABELS`（每章 zh/en/章节号，印到盘面）、`V`/`driveView`（相机机位）、`sceneState`（每个场景的分段编排）、`DISC_C`（每章圆盘色）、`SPIN_AT`（spin 换色时点）、`GANTT_ROWS`、`WF`（瀑布图数据，可删）|
| `assets/js/stage.js` | 模型路径、可动节点名（Front_Cover / HDD_0X / HDD_0X_Side_Label…）、`driveEdge`（标注锚点）、丝带文字 `words`、灯光 |
| `assets/js/notes.js` | 演讲稿唯一数据源；改完跑 `python3 tools/notes2md.py . "项目名 · 演讲稿"` 生成 `演讲稿.md` |
| `presenter.html` | 演讲者窗口，通常不用改（标题里的项目名可改） |
| `assets/model/*.glb` | 换成新产品模型 |

## 换一个产品的步骤
1. **找结构**：产品能拆/能拉出/能分层的部件 = 章节容器（抽屉、电池仓、模块、镜头、配件）。数量 = 章数（3–6）。没有就保留 hero + spin + 色块，删掉 unbox/drive 场景。
2. **模型**：GLB 里可动部件各自是独立节点，名字固定；在 stage.js 里替换 `getObjectByName` 的名字和位移方向/距离（Lucy：前盖 z+0.19 再 x+0.42，硬盘 z+0.13）。
3. **机位**：先只开 hero，调 `V.hero0/hero1` 让主角在右侧 60–70% 处；`driveView(i)` 对准每个部件；手机端 `mob()` 统一把主角放上半屏。
4. **内容**：按 SKILL.md 的模块与内容规则写 `index.html`；章节分组写进 `LABELS` 与 `#menu`/`#hud`/`#hdr nav`。正文模块加 `id` 和 `data-nav`；`assets/js/quick-nav.js` 自动生成顶栏细分导航及完整目录，不另维护重复标签表。
5. **色块**：每章至少一个 blue 或 ink band，冰蓝给数据段；整站不要连续两屏都是白。
6. **讲稿**：每屏一条 notes，口吻按 speech-presenter.md。
7. **QA**：见 SKILL.md「沉浸版 QA」。
8. **部署**：独立私有仓库 + Vercel，push 即部署。

## 案例章（CH 10）
`#c10` 是「代理商相关案例」章节：公司数据带 + 最相关案例大卡 + 分组案例墙 `.cs-card` + KOL 截图 + 线下展示 + 平台奖项，并在市场/KOL 章插 `.refcase` 回指。素材优先从 `../../reference/case-library/` 取现成裁图及索引。默认选 6–8 个不同产品（母版演示 8 个），逐例写关联说明，整卡链接到对应平台项目（新标签页）。平台/KOL/线下资源另列，不计入 6–8 个案例；每项来源与日期可追溯。历史金额按公司介绍口径展示，不当实时值；汇率是口径而非现价。UGREEN NASync 日本项目在 GREEN FUNDING。

## 内含的客户数据
`index.html`、`notes.js`、`演讲稿.md`、`assets/img/*` 是 Cephalon 真实方案内容与素材，只作版式与口吻参照；新项目必须全部替换，不得把 Lucy 的数字带进别家方案。

## 细分导航
改版前读 `../../reference/section-navigation.md`；入口由正文 `[data-nav][id]` 自动生成，删除正文后入口同步消失。预算/订单来源/广告素材/案例/平台资源均有单独入口。
