> **历史示例（legacy）**：这个案例保留的价值是 **Wix 打包/部署脚本** 与 **CNC 刀路揭开、慢动作按压** 等针对键盘的滚动短片技法。它的**视觉风格（深色舞台、噪点、标签式切换等）不再作为模板**——新项目的视觉与动效一律以 `references/design-system.md`、`references/motion-library.md` 和 `examples/sweetmyo-gen2-v4/` 为准。

# 案例：biaXbew Genesis01 预热页

线上：https://www.biaxbew.com/

这里是完整源码和 Wix 打包部署脚本，用来参考做法。**图片素材没有放进来**（约 14 MB，属于客户项目），所以本地打开会缺图；看代码结构、动效实现和 Wix 打包方式即可。

- `index.html` / `css/style.css` / `js/main.js`：页面源码。按 `#cnc`、`#press`、`scrubScene`、`watch(`、`[data-count]`、`.kb` 等名字搜对应做法。
- `wix/build_wix.py`：打包成 Wix 自定义元素脚本。
- `wix/deploy.mjs`：上传图片、写入 Wix、发布（指向的是 biaXbew 的站点，**新项目必须改掉编辑器地址后再用**）。
- `wix/media-map.production.json`、`production-target.json`、`survey-popup.json`：biaXbew 站点的图片映射、组件标识、弹窗配置。
- `HANDOFF.md`：当前状态的交接文档（其中引用的本机路径是原作者电脑上的，忽略即可）。
- `HANDOFF-history.md`：各轮修改记录。
