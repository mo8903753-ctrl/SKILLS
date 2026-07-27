# 固定参考图映射

这个文件用于说明所有项目通用参考图的放置和映射方式。机器可读清单在 `references/static-reference-manifest.json`，生成拍摄 brief 时优先读取 `assets/static-references/` 下的图片，并放入 HTML 表格的「参考文件」列。

注意：`产品静态图实拍 + 渲染` 模块的 9 个参考图 slot 默认应由项目专属 AI 生图覆盖；下表对应的通用图只作为 `image_gen` 不可用或用户明确要求不生图时的回退。

## 使用规则

1. 固定参考图必须放在：
   `/Users/madspace20250515/.codex/skills/shooting-brief-master/assets/static-references/`
2. 文件名优先使用下方「建议文件名」，实际执行以 `references/static-reference-manifest.json` 为准。如果文件不存在，对应位置回退为灰色占位框 `[请插入参考图]`。
3. 为保证最终 HTML 可单文件发送，生成 brief 时应将图片转成 base64 data URI 后写入 `<img>`，不要使用外链或本地绝对路径作为最终交付。
4. 每个单元格最多放 2 张固定图；更多参考图只在说明文字中提示“可补充更多同类参考”。
5. 参考图只表达构图/机位/画面要求，不替代具体项目产品图。

## 产品静态图实拍 + 渲染

| slot | 对应章节 | 建议文件名 | 默认图注 |
|---|---|---|---|
| `{{参考图_错误案例}}` | 总体拍摄原则 - 错误案例小提醒 | `static-warning-wrong-example.jpg` | 错误案例：不要使用夸张表情、过近人物特写或抢产品主体的画面 |
| `{{参考图_KV}}` | 一-1 KV 侧面 45° 或正面 | `static-kv-45-front.jpg` | KV 45° 主视觉构图参考 |
| `{{参考图_核心功能}}` | 一-2 核心功能 | `static-core-function-closeup.jpg` | 核心功能工作状态特写参考 |
| `{{参考图_产品特写}}` | 一-3 产品特写 | `static-product-detail.jpg` | 产品正侧面与细节质感参考 |
| `{{参考图_材质细节}}` | 一-4 材质细节 | `static-material-detail.jpg` | 材质、纹理、接口细节参考 |
| `{{参考图_场景应用}}` | 一-5 场景应用 | `static-lifestyle-scene.jpg` | 北美户外/生活方式场景参考 |
| `{{参考图_生活镜头}}` | 一-6 生活镜头 | `static-life-moment.jpg` | 人物自然互动与中长景参考 |
| `{{参考图_产品品质}}` | 一-7 产品品质 | `static-quality-test.jpg` | 品质测试与数据展示参考 |
| `{{参考图_纯色渲染}}` | 一-8 纯色背景渲染图 | `static-render-orthographic.jpg` | 六视图/尺寸/配件展示参考 |
| `{{参考图_核心部件}}` | 一-9 核心部件 | `static-component-closeup.jpg` | 核心部件与模块特写参考 |

## 设计生产运输拍摄

| slot | 对应章节 | 建议文件名 | 默认图注 |
|---|---|---|---|
| `{{参考图_正常运转}}` | 三-1 产品正常运转画面 | `static-factory-operation.jpg` | 产品亮灯/屏幕/运转状态参考 |
| `{{参考图_设计手稿}}` | 三-2 产品设计师手稿 | `static-designer-sketch.jpg` | 手稿/CAD/结构草图参考 |
| `{{参考图_产线辨识}}` | 三-3 产线辨识图 | `static-identifiable-product-line.jpg` | 产线中可辨识产品/半成品参考 |
| `{{参考图_生产过程}}` | 三-4 产品生产过程 | `static-production-line.jpg` | 工人组装与产线远近景参考 |
| `{{参考图_零部件组装}}` | 三-5 零部件组装过程 | `static-assembly-process.jpg` | 核心部件/外壳组装参考 |
| `{{参考图_装货过程}}` | 三-6 装货过程 | `static-packing-loading.jpg` | 装箱、装车、货车码放参考 |
| `{{参考图_打包装车}}` | 三-7 打包 - 装车 | `static-packed-shipment.jpg` | 包装完毕与待发货陈列参考 |
| `{{参考图_全流程视频}}` | 三-8 全流程视频 | `static-production-line.jpg` | 生产到包装全流程视频参考 |

## HTML 片段格式

当图片存在时，将 slot 替换为：

```html
<figure class="ref-card">
  <img class="ref-img" src="data:image/jpeg;base64,..." alt="KV 45° 主视觉构图参考">
  <figcaption>KV 45° 主视觉构图参考</figcaption>
</figure>
```

当图片不存在时，将 slot 替换为：

```html
<div class="img-placeholder">参考图<br>[请插入]</div>
```
