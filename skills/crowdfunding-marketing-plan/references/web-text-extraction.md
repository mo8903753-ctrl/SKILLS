# 网页全量文本提取技术

当需要提取网页全部文本内容用于文案适配/改写时，按以下优先级尝试：

## 优先级

### 1. `web_extract`（首选，但 JS 渲染页面经常失败）

```python
from hermes_tools import web_extract
result = web_extract(urls=["https://..."], char_limit=100000)
```

**限制：** 对 JS 重度渲染的网站（Vercel/Next.js/React SPA）经常返回空内容。

### 2. `browser_snapshot` full=true（可用但会被截断）

`browser_snapshot(full=true)` 在长页面（13+ 章节的提案页）会被截断在约 700 行处，且重复调用不会推进。

### 3. `browser_console` + `document.body.innerText`（最终兜底，可靠）

```javascript
// 在 browser_console 中执行：
document.body.innerText
```

**一次调用获取全部可见文本**，不受 snapshot 截断限制。格式为纯文本（保留换行），不含 HTML 标签但保留页面文本结构。

**使用前提：** 需先 `browser_navigate(url)`，然后滚动几次确保懒加载内容渲染完毕，再执行 `browser_console`。

### 完整工作流

```
browser_navigate(url) → browser_scroll(down) × 4–5 次 → browser_console(document.body.innerText)
```

文本会以纯文本格式返回，用 `\t` 分隔表格列、`\n` 分隔行。可直接作为文案重写的源材料。
