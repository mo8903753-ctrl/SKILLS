# HTML 方案骨架模板

此为 MadSpace 众筹方案的标准 HTML 骨架。可直接复制修改应用到新项目。

## 核心 CSS 变量

```css
:root{
  --charcoal:#2B2D2A; --stone:#5C5C53; --clay:#8B8178; --sand:#C4B5A5;
  --cream:#F5F0E8; --offwhite:#FAF8F5; --warmwhite:#FFFCF7;
  --accent:#C8734A; --accent-deep:#A0522D; --accent-light:#E8A87C;
  --teal:#3D6B66; --teal-light:#5C8D87; --teal-pale:#D0E4E1;
  --negative:#C44D4D; --gold:#B8956A; --bg-dark:#1E1F1C;
}
```

配色方案为 Patagonia 风格：陶土橙 + 深绿 + 暖石灰。可微调 `--accent` 和 `--teal` 适配客户品牌色。

## 封面背景 + 浮动 Logo 模式

```html
<section class="cover" id="cover">
  <div class="cover-bg"></div>
  <div class="cover-overlay"></div>
  <!-- 文字内容 -->
</section>

<!-- 浮动 Logo：base64 内嵌 -->
<div class="floating-logo">
  <img src="data:image/png;base64,..." alt="Logo" style="height:2.2rem;width:auto">
</div>
```

```css
.cover{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-start;padding:5rem 2rem 3rem}
.cover .cover-bg{position:absolute;inset:0;z-index:0;background:url('./cover-bg.png') center/cover no-repeat}
.cover .cover-overlay{position:absolute;inset:0;z-index:1;background:linear-gradient(160deg,rgba(245,240,232,0.35),rgba(250,248,245,0.4))}
.cover>*{position:relative;z-index:2}
.floating-logo{position:fixed;top:0.6rem;right:1rem;z-index:2000;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.2))}
```

## 预算双档切换

用两个独立 `<div class="budget-panel">` + JS `switchBudget()` 真实切换显示/隐藏：

```js
function switchBudget(tier) {
  document.getElementById('btnA').classList.toggle('active', tier==='a');
  document.getElementById('btnB').classList.toggle('active', tier==='b');
  document.getElementById('panelA').classList.toggle('active', tier==='a');
  document.getElementById('panelB').classList.toggle('active', tier==='b');
}
```

## SVG 流程图渐进式动画

```css
.step1{animation:fadeIn 0.6s ease-out 0.2s both}
.step2{animation:fadeIn 0.6s ease-out 0.6s both}
.step3{animation:fadeIn 0.6s ease-out 1.0s both}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
```

## 滚动触发动画

```js
var observer = new IntersectionObserver(function(entries){
  entries.forEach(function(e){ if(e.isIntersecting) e.target.classList.add('visible'); });
}, {threshold:0.1});
document.querySelectorAll('.reveal').forEach(function(el){ observer.observe(el); });
```

```css
.reveal{opacity:0;animation:fadeUp 0.7s ease-out forwards;animation-play-state:paused}
.reveal.visible{animation-play-state:running}
```

## 部署清单

1. 桌面建文件夹，放入 `index.html` + 图片文件
2. 本地测试：`cd 文件夹 && python3 -m http.server 8080`
3. 公网部署：拖文件夹到 https://app.netlify.com/drop
