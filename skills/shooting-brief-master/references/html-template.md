# HTML 模板骨架

以下是完整的 HTML 文档骨架。生成文档时以此为基础，将变量替换后输出完整文件。

---

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{产品名称}} 拍摄需求文档</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    font-size: 13px;
    color: #1a1a1a;
    background: #fff;
    padding: 40px;
    max-width: 1280px;
    margin: 0 auto;
  }

  /* ── 封面 ── */
  .cover {
    text-align: center;
    padding: 60px 0 40px;
    border-bottom: 3px solid #2d7d46;
    margin-bottom: 40px;
  }
  .cover h1 {
    font-size: 26px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 10px;
  }
  .cover .subtitle {
    font-size: 14px;
    color: #666;
    margin-bottom: 6px;
  }
  .cover .date {
    font-size: 12px;
    color: #999;
  }
  .cover .badge {
    display: inline-block;
    background: #2d7d46;
    color: white;
    font-size: 11px;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 12px;
  }

  /* ── 章节标题 ── */
  .section-header {
    background: #2d7d46;
    color: white;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 16px;
    margin: 36px 0 0 0;
    border-radius: 4px 4px 0 0;
  }
  .section-header.blue { background: #1a5fa8; }
  .section-header.teal { background: #0d7ea0; }

  /* ── 总体原则 ── */
  .principles {
    border: 1px solid #c8e6c9;
    border-top: none;
    padding: 16px 20px;
    background: #f9fffe;
    border-radius: 0 0 4px 4px;
    margin-bottom: 8px;
  }
  .principles ol { padding-left: 20px; }
  .principles li { margin-bottom: 6px; line-height: 1.7; }
  .principles li strong { color: #2d7d46; }
  .principles .warning {
    background: #fff8e1;
    border-left: 3px solid #ffc107;
    padding: 8px 12px;
    margin-top: 12px;
    font-size: 12px;
    color: #7a6000;
  }
  .principles .note {
    font-size: 11px;
    color: #888;
    margin-top: 10px;
    font-style: italic;
  }
  .principles .warning-ref {
    width: 180px;
    margin-top: 10px;
  }

  /* ── 表格 ── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 4px;
    font-size: 12.5px;
  }
  thead tr { background: #e8f5e9; }
  thead th {
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
    color: #1b5e20;
    border: 1px solid #c8e6c9;
    white-space: nowrap;
  }
  .blue-table thead tr { background: #e3f2fd; }
  .blue-table thead th { color: #0d47a1; border-color: #bbdefb; }
  .teal-table thead tr { background: #e0f7fa; }
  .teal-table thead th { color: #006064; border-color: #b2ebf2; }

  tbody tr { border-bottom: 1px solid #e0e0e0; }
  tbody tr:nth-child(even) { background: #fafafa; }
  tbody td {
    padding: 9px 12px;
    vertical-align: top;
    border: 1px solid #e0e0e0;
    line-height: 1.6;
  }
  td .tag {
    display: inline-block;
    background: #e8f5e9;
    color: #2d7d46;
    font-size: 10px;
    padding: 1px 7px;
    border-radius: 10px;
    margin-right: 4px;
    margin-bottom: 2px;
  }
  td ul { padding-left: 16px; margin: 4px 0; }
  td ul li { margin-bottom: 3px; }
  .qty {
    text-align: center;
    font-weight: 600;
    color: #c62828;
    white-space: nowrap;
  }
  .highlight-todo {
    background: #fff9c4;
    color: #5d4037;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 11px;
  }

  /* ── 占位图 ── */
  .img-placeholder {
    width: 100%;
    min-height: 70px;
    background: #f0f0f0;
    border: 2px dashed #ccc;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #aaa;
    font-size: 11px;
    text-align: center;
    padding: 8px;
  }
  .ref-card {
    width: 100%;
    margin: 0 0 6px;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    min-width: 0;
  }
  .ref-card:last-child { margin-bottom: 0; }
  .ref-img {
    display: block;
    width: 100%;
    height: 170px;
    padding: 4px;
    object-fit: contain;
    background: #f7f7f7;
    box-sizing: border-box;
  }
  .warning-ref .ref-img {
    height: 110px;
  }
  .ref-card figcaption {
    padding: 6px 7px;
    color: #666;
    font-size: 10.5px;
    line-height: 1.35;
  }

  /* ── 备注区 ── */
  .remark-box {
    border: 1px solid #ddd;
    border-top: none;
    padding: 12px 16px;
    background: #fafafa;
    border-radius: 0 0 4px 4px;
    font-size: 12px;
    margin-bottom: 4px;
  }
  .remark-box .remark-row {
    display: flex;
    gap: 12px;
    margin-bottom: 6px;
  }
  .remark-box .remark-label {
    font-weight: 600;
    color: #555;
    min-width: 60px;
    white-space: nowrap;
  }

  /* ── 视频脚本块 ── */
  .script-block {
    border: 1px solid #bbdefb;
    border-top: none;
    padding: 16px 20px;
    background: #f8fbff;
    border-radius: 0 0 4px 4px;
    margin-bottom: 4px;
  }
  .script-block h4 {
    color: #1a5fa8;
    font-size: 12px;
    font-weight: 700;
    margin: 12px 0 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .script-block h4:first-child { margin-top: 0; }
  .script-block ul { padding-left: 18px; margin: 0; }
  .script-block li { margin-bottom: 4px; line-height: 1.6; }
  .script-block .req-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
  }
  .script-block .req-item {
    background: #e3f2fd;
    color: #0d47a1;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 12px;
  }

  /* ── 页脚 ── */
  .footer {
    text-align: center;
    margin-top: 60px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
    font-size: 11px;
    color: #aaa;
  }

  /* ── 打印优化 ── */
  @media print {
    body { padding: 20px; font-size: 11px; }
    .section-header { page-break-after: avoid; }
    table { break-inside: auto; page-break-inside: auto; }
    thead { display: table-header-group; }
    tr, .ref-card { break-inside: avoid; page-break-inside: avoid; }
    .cover { page-break-after: always; }
    .ref-img { height: 125px; padding: 3px; object-fit: contain; }
    .warning-ref .ref-img { height: 88px; }
  }
</style>
</head>
<body>

<!-- 封面 -->
<div class="cover">
  <h1>{{产品名称}}</h1>
  <div class="subtitle">众筹产品拍摄需求文档</div>
  <div class="date">{{当前日期}} · MadSpace 众筹代运营</div>
  <div class="badge">SHOOTING BRIEF</div>
</div>

<!-- 总体拍摄原则 -->
<div class="section-header">总体拍摄原则</div>
<div class="principles">
  <ol>
    <li><strong>中长镜头范围</strong>：取景不要太近，以便于设计做图</li>
    <li><strong>构图</strong>：与人的身体（如手臂）相结合，使图片更有趣，显得产品更实用；<span style="color:#c62828">注意不要有多余夸张表情</span></li>
    <li>对产品进行<strong>多角度拍摄</strong>，有必要突出产品的特点</li>
    <li><strong>背景</strong>：杂乱的背景可以采用<strong>虚化处理</strong>；还是尽量采用干净、整洁的背景；也可以选择<strong>纯色的背景</strong>，与产品相近或能与产品进行互补的纯色背景</li>
    <li>可以采用<strong>对角线拍摄</strong>，使产品看起来更加灵活</li>
    <li>也可以选择与产品相关的物体</li>
    <li>拍摄时<strong>加强产品的视觉冲击力</strong>，不要拍得过于板正</li>
    <li><strong>不要竖屏的照片</strong></li>
  </ol>
  <div class="warning">⚠ 所有照片必须全部横屏，竖屏一张都不要。图片长宽比建议：4000 × 3000</div>
  <div class="warning-ref">{{参考图_错误案例}}</div>
  <div class="note">范例仅供参考，如有不完整请贵司自行针对产品的特点来参考</div>
</div>

<!-- 一. 产品静态图实拍+渲染 -->
<div class="section-header" style="margin-top:32px;">一. 产品静态图实拍 + 渲染&emsp;<span style="font-weight:400;font-size:12px;">（风格：高品质、突出产品特点，场景化展示）&emsp;尺寸：1920 × 1080 像素 / 建议 4000 × 3000</span></div>

<table>
  <thead>
    <tr>
      <th style="width:40px;">序号</th>
      <th style="width:130px;">项目描述</th>
      <th>要求</th>
      <th style="width:70px;">数量</th>
      <th style="width:260px;">参考文件</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><strong>KV</strong><br>侧面 45° 或正面</td>
      <td>
        <ul>
          <li>产品 45° 角展示，同时展现 {{KV核心状态描述}}</li>
          <li>背景：{{KV背景描述}}，光线突出产品轮廓（建议从早到傍晚连拍，展示长续航）</li>
          <li>屏幕/显示区域展示实时数据（{{屏幕数据示例}}）</li>
          <li>画面左下角留出空间压字 "{{产品Slogan_EN}}"</li>
          <li>突出产品作为主体的使用场景</li>
        </ul>
      </td>
      <td class="qty">{{KV图数量}}</td>
      <td>{{参考图_KV}}</td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>核心功能</strong><br>（静态图）</td>
      <td>
        大特写下面功能的工作时状态：
        <ul>
          {{核心功能列表_li}}
        </ul>
      </td>
      <td class="qty">{{核心功能数量}}</td>
      <td>{{参考图_核心功能}}</td>
    </tr>
    <tr>
      <td>3</td>
      <td><strong>产品特写</strong><br>（静态图）</td>
      <td>
        <ul>
          <li>展示产品的正面与侧面 45° 三视图</li>
          <li>体现高品质工艺细节</li>
        </ul>
      </td>
      <td class="qty">5</td>
      <td>{{参考图_产品特写}}</td>
    </tr>
    <tr>
      <td>4</td>
      <td><strong>材质细节</strong><br>（静态图）</td>
      <td>
        <ul>
          {{材质细节列表_li}}
        </ul>
      </td>
      <td class="qty">5</td>
      <td>{{参考图_材质细节}}</td>
    </tr>
    <tr>
      <td>5</td>
      <td><strong>场景应用</strong><br>（静态图）</td>
      <td>
        展示不同场景中的使用：
        <ul>
          {{场景应用列表_li}}
        </ul>
      </td>
      <td class="qty">{{场景应用数量}}</td>
      <td>{{参考图_场景应用}}</td>
    </tr>
    <tr>
      <td>6</td>
      <td><strong>生活镜头</strong><br>（静态图）</td>
      <td>
        <ul>
          {{生活镜头列表_li}}
        </ul>
      </td>
      <td class="qty">{{生活镜头数量}}</td>
      <td>{{参考图_生活镜头}}</td>
    </tr>
    <tr>
      <td>7</td>
      <td><strong>产品品质</strong><br>（静态图）</td>
      <td>
        <ul>
          {{品质测试列表_li}}
        </ul>
      </td>
      <td class="qty">3</td>
      <td>{{参考图_产品品质}}</td>
    </tr>
    <tr>
      <td>8</td>
      <td><strong>纯色背景渲染图</strong></td>
      <td>
        <ul>
          <li>六视图（正 / 背 / 左 / 右 / 顶 / 底）</li>
          <li>开合状态对比（关闭 vs 开启）</li>
          <li>尺寸标注图（含具体参数：{{产品规格}}）</li>
          <li>配件全家福（{{配件清单}}）</li>
          <li>多配色展示</li>
        </ul>
      </td>
      <td class="qty">{{渲染图数量}}</td>
      <td>{{参考图_纯色渲染}}</td>
    </tr>
    <tr>
      <td>9</td>
      <td><strong>核心部件</strong></td>
      <td>
        <ul>
          {{核心部件列表_li}}
        </ul>
        <span style="color:#c62828;font-weight:600;">重点强调本产品的多模块精密设计</span>
      </td>
      <td class="qty">{{核心部件数量}}</td>
      <td>{{参考图_核心部件}}</td>
    </tr>
  </tbody>
</table>

<div class="remark-box">
  <div class="remark-row">
    <span class="remark-label">场景主要有</span>
    <span>{{目标场景列表}}</span>
  </div>
  <div class="remark-row">
    <span class="remark-label">模特需求</span>
    <span>{{目标用户}}</span>
  </div>
</div>

<!-- 二. 产品视频拍摄 -->
<div class="section-header blue" style="margin-top:32px;">二. 产品视频拍摄&emsp;<span style="font-weight:400;font-size:12px;">（风格：高品质、突出产品特点，场景化展示）</span></div>

<table class="blue-table">
  <thead>
    <tr>
      <th style="width:40px;">序号</th>
      <th style="width:130px;">项目描述</th>
      <th>要求</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><strong>视频主题</strong></td>
      <td>
        <strong>"{{产品Slogan_CN}}"</strong><br>
        {{产品Slogan_EN}}
      </td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>视频时长</strong></td>
      <td>
        <span class="tag">完整版</span> 主视频：{{视频主版时长}}<br>
        <span class="tag">社媒版</span> 精华剪辑：{{视频社媒时长}}
      </td>
    </tr>
    {{视频场景行_tr}}
  </tbody>
</table>

<div class="section-header blue" style="border-radius:0;">脚本建议</div>
<div class="script-block">
  <h4>🎬 开场</h4>
  <ul>
    <li>{{痛点场景描述}}</li>
  </ul>
  <h4>🌟 产品亮相</h4>
  <ul>
    <li>360° 旋转展示产品外观</li>
    <li>特写控制面板 / 操作区亮起瞬间</li>
    <li>{{产品亮相动作描述}}</li>
  </ul>
  <h4>⚡ 功能演示</h4>
  <ul>
    {{功能演示列表_li}}
  </ul>
  <h4>🌍 多场景应用</h4>
  <ul>
    {{多场景应用列表_li}}
  </ul>
  <h4>🔬 品质展示</h4>
  <ul>
    {{品质展示列表_li}}
  </ul>
  <h4>🏁 收尾</h4>
  <ul>
    <li>同场景用户满意微笑的快速剪辑</li>
    <li>产品 Slogan 定格：<strong>{{产品Slogan_EN}}</strong></li>
  </ul>
</div>

<div class="section-header blue" style="border-radius:0;">拍摄要求</div>
<div class="script-block">
  <div class="req-list">
    <span class="req-item">每个场景包含完整使用流程</span>
    <span class="req-item">捕捉自然光线下的产品质感</span>
    <span class="req-item">确保功能演示清晰直观</span>
    <span class="req-item">所有功能必须真实演示</span>
    <span class="req-item">数据参数显示清晰</span>
    <span class="req-item">场景转换要求自然流畅</span>
    <span class="req-item">模特表情要求真实自然</span>
    <span class="req-item">重点突出产品便携性和核心功能特点</span>
  </div>
</div>

<!-- 三. 设计生产运输拍摄 -->
<div class="section-header teal" style="margin-top:32px;">三. 设计生产运输拍摄&emsp;<span style="font-weight:400;font-size:12px;">（风格：真实清晰展示）&emsp;尺寸：1920 × 1080 像素 / 建议 4000 × 3000</span></div>

<table class="teal-table">
  <thead>
    <tr>
      <th style="width:40px;">序号</th>
      <th style="width:160px;">项目描述</th>
      <th>要求</th>
      <th style="width:70px;">数量</th>
      <th style="width:260px;">参考文件</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><strong>产品正常运转画面</strong><br><span style="color:#666;font-size:11px;">（平台审核用）</span></td>
      <td>要实拍的视频，要看到产品能正常使用（如亮灯、屏幕亮起、运转状态）；时长可以稍长一些</td>
      <td class="qty">{{生产图_运转视频数量}}</td>
      <td>{{参考图_正常运转}}</td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>产品设计师手稿</strong></td>
      <td>如贵司能按平台要求提供符合要求的 CAD 截图亦可。考虑产品 CAD 设计图相对机密，大部分项目提供手稿</td>
      <td class="qty">2</td>
      <td>{{参考图_设计手稿}}</td>
    </tr>
    <tr>
      <td>3</td>
      <td><strong>产线辨识图</strong><br><span style="color:#666;font-size:11px;">（模具/壳料/半成品）</span></td>
      <td>产线上能一眼辨别是本次众筹产品的视频或图片</td>
      <td class="qty">3</td>
      <td>{{参考图_产线辨识}}</td>
    </tr>
    <tr>
      <td>4</td>
      <td><strong>产品生产过程</strong></td>
      <td>
        <ul>
          <li>工人（穿头罩和制服）组装核心零件过程：近景 ×1，远景 ×1</li>
          <li>核心零件在生产线上不同角度：横向远景 ×3</li>
        </ul>
      </td>
      <td class="qty">5</td>
      <td>{{参考图_生产过程}}</td>
    </tr>
    <tr>
      <td>5</td>
      <td><strong>零部件组装过程</strong></td>
      <td>拍摄产品的生产过程（组装核心部件、外壳等）</td>
      <td class="qty">3</td>
      <td>{{参考图_零部件组装}}</td>
    </tr>
    <tr>
      <td>6</td>
      <td><strong>装货过程</strong></td>
      <td>
        <ul>
          <li>拍摄生产装箱完毕，准备搬上货车的过程（<strong>外箱露出 LOGO</strong>）</li>
          <li>装车时 ×3：工人把产品装上货车的过程</li>
          <li>装车完毕 ×3：所有产品在货车里整齐码放</li>
          <li>工人注意戴头罩和制服</li>
        </ul>
      </td>
      <td class="qty">3</td>
      <td>{{参考图_装货过程}}</td>
    </tr>
    <tr>
      <td>7</td>
      <td><strong>打包 - 装车</strong></td>
      <td>让消费者看到产品已经量产并且包装完毕；要看到品牌 LOGO 和产品名；可多角度拍摄；看到一堆已包装的产品整齐排列待发货即可</td>
      <td class="qty">2</td>
      <td>{{参考图_打包装车}}</td>
    </tr>
    <tr>
      <td>8</td>
      <td><strong>全流程视频</strong></td>
      <td>拍摄生产 → 测试 → 包装 → 打包 → 装车的整个流程过程视频</td>
      <td class="qty">2</td>
      <td>{{参考图_全流程视频}}</td>
    </tr>
  </tbody>
</table>

<!-- 页脚 -->
<div class="footer">
  本文档由 MadSpace 众筹代运营团队制作 · {{当前日期}}<br>
  如有疑问请联系对应项目负责人
</div>

</body>
</html>
```

---

## 变量替换说明

### 列表类变量展开规则

`{{核心功能列表_li}}` → 每条功能展开为 `<li>功能描述</li>`

`{{材质细节列表_li}}` → 每个材质/部件细节一条

`{{场景应用列表_li}}` → 每个场景加使用细节描述

`{{视频场景行_tr}}` → 每个拍摄场景展开为一行 `<tr>`:
```html
<tr>
  <td>3</td>
  <td><strong>场景名称</strong></td>
  <td><ul><li>场景描述 1</li><li>场景描述 2</li></ul></td>
</tr>
```

### 待确认变量样式
```html
<span class="highlight-todo">【待确认：字段名】</span>
```

### 固定参考图变量展开规则

`{{参考图_*}}` 变量按 `references/static-reference-map.md` 替换。

图片存在时：
```html
<figure class="ref-card">
  <img class="ref-img" src="data:image/jpeg;base64,..." alt="参考图说明">
  <figcaption>参考图说明</figcaption>
</figure>
```

图片不存在时：
```html
<div class="img-placeholder">参考图<br>[请插入]</div>
```
