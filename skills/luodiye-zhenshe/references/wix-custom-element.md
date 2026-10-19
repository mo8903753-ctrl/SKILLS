# 落到 Wix：自定义元素 + 原生表单

给其他 AI 用的完整提示词版本在 `wix-custom-page-prompt.md`，本文是操作细节。案例实现在 `examples/biaxbew-genesis01/wix/`。

## 为什么这样做

客户的硬性要求：页面放在 Wix 上、动效全保留、邮箱用 Wix 原生表单、首屏中段结尾各一个、只输一次、提交后直接弹 Wix 弹窗。以下方案都被否过：

| 方案 | 问题 |
|---|---|
| 嵌入网页（iframe） | 跟随滚动的动效失效；表单没法嵌进去 |
| 页面里自己做输入框，再把邮箱传给 Wix | 客户担心丢数据 |
| 原生表单固定成常驻底栏 | 和范例不一致 |
| 拆成几段嵌入块夹原生表单 | 跟随滚动的动效要降级 |

**最终方案：Wix「自定义元素」。** 代码直接运行在 Wix 页面里（不是 iframe），和页面共用滚动；原生表单和它放在同一区块里叠在上面。前提是站点付费并绑定域名（按 Wix 规则；免费站未实测）。

## 结构

1. 页面打包成一个脚本，注册自定义标签（案例：`<gx-genesis>`），用属性 `part` 区分显示哪一段。
2. 脚本存站点代码文件 `public/custom-elements/<名字>.js`；图片传站点媒体库。没有外部托管。
3. Wix 页面按表单位置切成几个区块（案例 4 段：首屏到工艺 / 中段订阅 / 轴体到场景 / 结尾）。每个区块一个自定义元素；需要表单的区块再放一个原生表单。
4. 页面在邮箱框位置留空的 `.slot`。脚本运行时量出位置，把同区块里的原生表单用 `transform` 挪过去；窗口变化、字体加载后重新对齐。电脑和手机通用。

## 打包（`scripts/wix/build_wix.py`）

做的事：
- 所有 CSS 选择器加统一根类前缀（案例 `.gxg`），`html` / `body` / `:root` 上的规则改挂到根类，`@keyframes` 加前缀。
- 根元素宽度用 `!important` 设成视口宽度并用负左边距铺满（Wix 有条样式会压回 980px）。
- 删掉平滑滚动库、自己的表单逻辑、顶栏逻辑；HTML 切成几段；表单处留 `.slot`。
- GSAP / ScrollTrigger 内联进脚本（`wix/vendor/`），不从 CDN 再加载。
- 图片地址按映射表（本地路径 → Wix 图片地址）替换。
- 同时生成本地模拟 Wix 结构的 `host.html`，先在本地看。

这个脚本和案例页面的 HTML 结构绑定（按注释标记切段、按字符串替换 JS），换项目要相应修改。

## 操作 Wix 编辑器（经典编辑器）

用能执行页面 JavaScript 的浏览器自动化打开已登录的编辑器：

- 入口：`document.getElementById("preview").contentWindow.documentServices`（下称 `ds`）。
- 等改动生效：`await new Promise(r => ds.waitForChangesApplied(r))`；看真实报错：`ds.registerToErrorThrown(e => …)`。
- 写代码文件：`const fs = ds.wixCode.fileSystem; await fs.writeFile(fs.getVirtualDescriptor("public/custom-elements/x.js", false), code); await fs.flush();`
- 加自定义元素：`ds.components.buildDefaultComponentStructure("wixui.CustomElementComponent")`，设 `data.tagName`、`data.url = "public/custom-elements/x.js"`、`data.hostedInCorvid = true`、`data.initialAttributes = JSON.stringify({ part: "a" })`，再 `ds.components.add(区块引用, 结构)`。
- 上传图片：`Authorization` 用 `ds.wixCode.getClientSpec().instance`，POST `https://www.wixapis.com/site-media/v1/files/generate-upload-url`（`mimeType`、`fileName`、`parentFolderId`）拿上传地址，再 PUT 文件，返回 `file.url`。令牌只在内存里用，不写文件不打印。
- 区块背景色、背景图：`ds.components.design.get/update`（首屏占位静帧用 `background.mediaRef`，`fittingType: "fit"`、`alignType: "top"`）。
- 页面设成落地页（去页眉页脚）：`ds.pages.data.update(页面id, { isLandingPage: true, isMobileLandingPage: true })`。
- 手机布局：组件引用 `type: "MOBILE"`；显示被隐藏的组件 `ds.mobile.hiddenComponents.show(组件id, 页面id)`。
- 发布：点编辑器右上角「發佈 / Publish」，等"已发布并上线"提示。有时会先弹"编辑行动版网站"提示，点取消再发布。

## 原生表单

- **用 Wix 表单界面新建**一个专用表单和提交表，再配置"提交后打开弹窗"。不要用接口复制别的页面的表单当正式表单：复制出来仍指向原表单，数据会混在一起、弹的也是原弹窗。
- 可以改外观（深色输入框、圆角、按钮颜色字号）、删掉表单里多余的文字图片只留输入框和按钮。不要改数据设置。
- 不要自己提交测试，需要时问客户，用 example.com 测试邮箱并在交接时说明。

## 必踩的坑

- **编辑器预览里自定义元素是空白的**，只能发布后在线上验证。
- **Wix 发布是整站发布**，其他页面的草稿会一起上线。每次发布前得到客户同意，并确认没有别人在改站。
- Wix 在页面 `load` 之后才请求自定义元素脚本，发布后首次访问还要现打包。首屏一定要有原生背景静帧兜底，脚本到了且产品图加载完再隐藏静帧。改了首屏产品位置，静帧要重新截。
- 判断可见性一律 `IntersectionObserver`。ScrollTrigger 只做跟随滚动的效果，并用 `ResizeObserver` 在尺寸变化时 `refresh`。
- 手机布局里表单必须和自定义元素在位置上重叠，否则 Wix 把表单排到下面留白缝。
- `img { height: auto }` 必须保留。
- 本地网络如果走代理，访问任何 Wix 站点握手都可能很慢，先拿范例页对比，别误判成页面慢。
