#!/usr/bin/env python3
"""
众筹整合营销方案 - 飞书风格 HTML 生成器
MadSpace 内部工具

用法：
  python generate_html.py --json plan_data.json --output output.html
  或在 Claude skill 中作为模块导入使用
"""

import json
import html
import math
import os
import sys
from datetime import datetime

# ============================================================
# 飞书风格 CSS
# ============================================================

FEISHU_CSS = """
:root {
    --primary: #3370FF;
    --primary-light: #E8F0FF;
    --warning: #FF9800;
    --warning-light: #FFF8E1;
    --success: #00B365;
    --success-light: #E6F9F0;
    --danger: #F54A45;
    --danger-light: #FFF0F0;
    --info: #7B61FF;
    --info-light: #F3F0FF;
    --text-primary: #1F2329;
    --text-secondary: #646A73;
    --text-light: #8F959E;
    --border: #DEE0E3;
    --bg-page: #F5F6F7;
    --bg-white: #FFFFFF;
    --bg-hover: #F0F1F2;
    --yellow-header: #FFF8E1;
    --yellow-header-border: #FFE082;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
    color: var(--text-primary);
    background: var(--bg-page);
    line-height: 1.7;
    font-size: 14px;
}

/* 整体布局 */
.layout {
    display: flex;
    min-height: 100vh;
}

/* 左侧目录 */
.sidebar {
    width: 260px;
    background: var(--bg-white);
    border-right: 1px solid var(--border);
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    overflow-y: auto;
    padding: 20px 0;
    z-index: 100;
}

.sidebar-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    padding: 8px 20px 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}

.toc-list {
    list-style: none;
    padding: 0;
}

.toc-item {
    padding: 0;
}

.toc-item a {
    display: block;
    padding: 6px 20px;
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 13px;
    border-left: 3px solid transparent;
    transition: all 0.2s;
}

.toc-item a:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.toc-item a.active {
    color: var(--primary);
    border-left-color: var(--primary);
    background: var(--primary-light);
    font-weight: 500;
}

.toc-item.sub a {
    padding-left: 36px;
    font-size: 12px;
}

/* 主内容区 */
.main {
    margin-left: 260px;
    flex: 1;
    max-width: 900px;
    padding: 40px 48px;
    background: var(--bg-white);
    min-height: 100vh;
}

/* 标题 */
.doc-title {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
    line-height: 1.4;
}

.doc-meta {
    font-size: 13px;
    color: var(--text-light);
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}

.doc-meta span { margin-right: 16px; }

h2 {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 40px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--primary);
    display: flex;
    align-items: center;
    gap: 8px;
}

h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 28px 0 12px;
}

h4 {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 20px 0 8px;
}

p {
    margin: 8px 0;
    line-height: 1.8;
}

/* 表格 - 飞书黄色表头风格 */
.feishu-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 13px;
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
}

.feishu-table thead th {
    background: var(--yellow-header);
    border: 1px solid var(--yellow-header-border);
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
    color: var(--text-primary);
    white-space: nowrap;
}

.feishu-table tbody td {
    border: 1px solid var(--border);
    padding: 9px 12px;
    vertical-align: top;
}

.feishu-table tbody tr:nth-child(even) {
    background: #FAFBFC;
}

.feishu-table tbody tr:hover {
    background: var(--bg-hover);
}

/* 特殊表格 - 蓝色表头 */
.feishu-table.blue thead th {
    background: var(--primary-light);
    border-color: #B3D1FF;
}

/* 特殊表格 - 绿色表头 */
.feishu-table.green thead th {
    background: var(--success-light);
    border-color: #80D9AD;
}

/* 引用色块 */
.callout {
    border-radius: 6px;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 13px;
    line-height: 1.7;
    border-left: 4px solid;
}

.callout-blue {
    background: var(--primary-light);
    border-color: var(--primary);
}

.callout-yellow {
    background: var(--warning-light);
    border-color: var(--warning);
}

.callout-green {
    background: var(--success-light);
    border-color: var(--success);
}

.callout-red {
    background: var(--danger-light);
    border-color: var(--danger);
}

.callout-purple {
    background: var(--info-light);
    border-color: var(--info);
}

.callout-title {
    font-weight: 600;
    margin-bottom: 6px;
}

/* 标签 */
.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    margin: 2px 4px 2px 0;
}

.tag-blue { background: var(--primary-light); color: var(--primary); }
.tag-yellow { background: var(--warning-light); color: #E68900; }
.tag-green { background: var(--success-light); color: var(--success); }
.tag-red { background: var(--danger-light); color: var(--danger); }
.tag-purple { background: var(--info-light); color: var(--info); }

/* 列表 */
ul, ol {
    margin: 8px 0;
    padding-left: 24px;
}

li {
    margin: 4px 0;
    line-height: 1.7;
}

/* KPI 卡片 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.kpi-card {
    background: var(--bg-page);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    border: 1px solid var(--border);
}

.kpi-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--primary);
    margin: 4px 0;
}

.kpi-label {
    font-size: 12px;
    color: var(--text-secondary);
}

/* 分隔线 */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
}

/* 进度条 */
.progress-bar {
    height: 8px;
    background: #E8E8E8;
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0;
}

.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s;
}

/* 时间线 */
.timeline {
    position: relative;
    padding-left: 24px;
    margin: 16px 0;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 8px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--border);
}

.timeline-item {
    position: relative;
    margin-bottom: 20px;
    padding-left: 16px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -20px;
    top: 6px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--primary);
    border: 2px solid var(--bg-white);
}

.timeline-date {
    font-size: 12px;
    color: var(--text-light);
    font-weight: 500;
}

.timeline-content {
    margin-top: 4px;
}

/* 打印样式 */
@media print {
    .sidebar { display: none; }
    .main {
        margin-left: 0;
        padding: 20px;
        max-width: 100%;
    }
    .feishu-table { page-break-inside: avoid; }
    h2 { page-break-after: avoid; }
    .callout { page-break-inside: avoid; }
    body { background: white; }
}

/* 响应式 */
@media (max-width: 768px) {
    .sidebar { display: none; }
    .main {
        margin-left: 0;
        padding: 20px;
    }
}
"""

# ============================================================
# 飞书风格 JS（目录高亮 + 平滑滚动）
# ============================================================

FEISHU_JS = """
document.addEventListener('DOMContentLoaded', function() {
    // 平滑滚动
    document.querySelectorAll('.toc-item a').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // 滚动高亮目录
    var headings = document.querySelectorAll('h2[id], h3[id]');
    var tocLinks = document.querySelectorAll('.toc-item a');

    function updateTOC() {
        var scrollPos = window.scrollY + 80;
        var current = '';
        headings.forEach(function(h) {
            if (h.offsetTop <= scrollPos) {
                current = h.getAttribute('id');
            }
        });
        tocLinks.forEach(function(link) {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateTOC);
    updateTOC();
});
"""


# ============================================================
# HTML 组件生成函数
# ============================================================

def esc(text):
    """HTML转义"""
    if text is None:
        return ""
    return html.escape(str(text))


def make_table(headers, rows, style=""):
    """
    生成飞书风格表格
    headers: ["列1", "列2", ...]
    rows: [["值1", "值2", ...], ...]
    style: "" | "blue" | "green"
    """
    cls = f"feishu-table {style}".strip()
    lines = [f'<table class="{cls}">']
    lines.append("<thead><tr>")
    for h in headers:
        lines.append(f"<th>{h}</th>")
    lines.append("</tr></thead>")
    lines.append("<tbody>")
    for row in rows:
        lines.append("<tr>")
        for cell in row:
            lines.append(f"<td>{cell}</td>")
        lines.append("</tr>")
    lines.append("</tbody></table>")
    return "\n".join(lines)


def make_callout(content, style="blue", title=""):
    """
    生成色块引用
    style: "blue" | "yellow" | "green" | "red" | "purple"
    """
    parts = [f'<div class="callout callout-{style}">']
    if title:
        parts.append(f'<div class="callout-title">{title}</div>')
    parts.append(f'<div>{content}</div>')
    parts.append('</div>')
    return "\n".join(parts)


def make_kpi_cards(kpis):
    """
    生成 KPI 卡片网格
    kpis: [{"label": "标签", "value": "值"}, ...]
    """
    cards = ['<div class="kpi-grid">']
    for kpi in kpis:
        cards.append(f"""
        <div class="kpi-card">
            <div class="kpi-label">{kpi['label']}</div>
            <div class="kpi-value">{kpi['value']}</div>
        </div>""")
    cards.append('</div>')
    return "\n".join(cards)


def make_tag(text, style="blue"):
    """生成标签"""
    return f'<span class="tag tag-{style}">{esc(text)}</span>'


def make_section(id_str, emoji, title, content):
    """生成一个模块章节"""
    return f"""
<h2 id="{id_str}">{emoji} {esc(title)}</h2>
{content}
"""


def make_subsection(id_str, title, content):
    """生成子章节"""
    return f"""
<h3 id="{id_str}">{esc(title)}</h3>
{content}
"""


# ============================================================
# 预算计算引擎
# ============================================================

def calculate_budget(goal):
    """根据众筹目标金额计算完整预算分配"""
    budget = {}

    # 总预算分配
    budget['preheat_ads'] = round(goal * 0.044, 2)
    budget['launch_ads'] = round(goal * 0.0872, 2)
    budget['kol'] = round(goal * 0.024, 2)
    budget['media_pr'] = round(goal * 0.004, 2)
    budget['community'] = round(goal * 0.0144, 2)
    budget['tools'] = round(goal * 0.003, 2)
    budget['giveaway'] = round(goal * 0.003, 2)
    budget['total'] = round(goal * 0.1796, 2)

    # 平台分配
    budget['preheat_meta'] = round(budget['preheat_ads'] * 0.6, 2)
    budget['preheat_google'] = round(budget['preheat_ads'] * 0.4, 2)
    budget['launch_meta'] = round(budget['launch_ads'] * 0.6, 2)
    budget['launch_google'] = round(budget['launch_ads'] * 0.4, 2)

    # 预热期周分配 - Meta
    preheat_meta_ratios = [0.1856, 0.2652, 0.2917, 0.2045, 0.0530]
    preheat_meta_days = [7, 7, 7, 7, 2]
    budget['preheat_meta_weeks'] = []
    for i, (ratio, days) in enumerate(zip(preheat_meta_ratios, preheat_meta_days)):
        week_budget = round(budget['preheat_meta'] * ratio, 2)
        daily = round(week_budget / days, 2)
        budget['preheat_meta_weeks'].append({
            'week': f'W{i+1}',
            'days': days,
            'ratio': f'{ratio*100:.2f}%',
            'total': week_budget,
            'daily': daily,
            'leads_min': round(daily / 5, 1),
            'leads_max': round(daily / 3.33, 1),
            'clicks': round(daily / 0.5, 0),
        })

    # 预热期周分配 - Google
    preheat_google_ratios = [0.1591, 0.2784, 0.2784, 0.2386, 0.0455]
    preheat_google_days = [7, 7, 7, 7, 2]
    budget['preheat_google_weeks'] = []
    for i, (ratio, days) in enumerate(zip(preheat_google_ratios, preheat_google_days)):
        week_budget = round(budget['preheat_google'] * ratio, 2)
        daily = round(week_budget / days, 2)
        budget['preheat_google_weeks'].append({
            'week': f'W{i+1}',
            'days': days,
            'ratio': f'{ratio*100:.2f}%',
            'total': week_budget,
            'daily': daily,
            'leads_min': round(daily / 5, 1),
            'leads_max': round(daily / 3.33, 1),
            'clicks': round(daily / 0.5, 0),
        })

    # 众筹期周分配 - Meta
    launch_meta_ratios = [0.2154, 0.1481, 0.1404, 0.1212, 0.1212, 0.1615, 0.0923]
    launch_meta_days = [7, 7, 7, 7, 7, 7, 3]
    budget['launch_meta_weeks'] = []
    for i, (ratio, days) in enumerate(zip(launch_meta_ratios, launch_meta_days)):
        week_budget = round(budget['launch_meta'] * ratio, 2)
        daily = round(week_budget / days, 2)
        budget['launch_meta_weeks'].append({
            'week': f'W{i+1}',
            'days': days,
            'ratio': f'{ratio*100:.2f}%',
            'total': week_budget,
            'daily': daily,
            'uv': round(daily / 1.14, 0),
            'order_amount': round(daily * 2.5, 2),
        })

    # 众筹期周分配 - Google
    launch_google_ratios = [0.1790, 0.1591, 0.1506, 0.1392, 0.1392, 0.1563, 0.0767]
    launch_google_days = [7, 7, 7, 7, 7, 7, 3]
    budget['launch_google_weeks'] = []
    for i, (ratio, days) in enumerate(zip(launch_google_ratios, launch_google_days)):
        week_budget = round(budget['launch_google'] * ratio, 2)
        daily = round(week_budget / days, 2)
        budget['launch_google_weeks'].append({
            'week': f'W{i+1}',
            'days': days,
            'ratio': f'{ratio*100:.2f}%',
            'total': week_budget,
            'daily': daily,
            'uv': round(daily / 1.14, 0),
            'order_amount': round(daily * 2.5, 2),
        })

    # 预估汇总
    budget['est_leads'] = round(budget['preheat_ads'] / 4, 0)  # CPL中值$4
    budget['est_sales'] = round(budget['launch_ads'] * 2.5, 2)  # ROI 2.5

    return budget


def format_usd(amount):
    """格式化美元金额"""
    if amount >= 1000:
        return f"${amount:,.0f}"
    return f"${amount:,.2f}"


# ============================================================
# 每日投广计划表生成
# ============================================================

def generate_daily_plan_table(weeks_data, period="preheat"):
    """生成每日投广计划表格"""
    headers_preheat = ["周", "天数", "占比", "周预算", "日预算", "日Leads(Min)", "日Leads(Max)", "日Clicks"]
    headers_launch = ["周", "天数", "占比", "周预算", "日预算", "日UV", "日订单金额"]

    if period == "preheat":
        rows = []
        total_budget = 0
        for w in weeks_data:
            total_budget += w['total']
            rows.append([
                f"<strong>{w['week']}</strong>",
                str(w['days']),
                w['ratio'],
                format_usd(w['total']),
                format_usd(w['daily']),
                str(w['leads_min']),
                str(w['leads_max']),
                str(int(w['clicks'])),
            ])
        rows.append([
            "<strong>Total</strong>", "30", "100%",
            f"<strong>{format_usd(total_budget)}</strong>",
            "—", "—", "—", "—"
        ])
        return make_table(headers_preheat, rows)
    else:
        rows = []
        total_budget = 0
        total_order = 0
        for w in weeks_data:
            total_budget += w['total']
            total_order += w['order_amount'] * w['days']
            rows.append([
                f"<strong>{w['week']}</strong>",
                str(w['days']),
                w['ratio'],
                format_usd(w['total']),
                format_usd(w['daily']),
                str(int(w['uv'])),
                format_usd(w['order_amount']),
            ])
        rows.append([
            "<strong>Total</strong>", "45", "100%",
            f"<strong>{format_usd(total_budget)}</strong>",
            "—", "—",
            f"<strong>{format_usd(total_order)}</strong>"
        ])
        return make_table(headers_launch, rows)


# ============================================================
# 完整 HTML 文档组装
# ============================================================

def generate_full_html(plan_data):
    """
    根据方案数据生成完整飞书风格HTML

    plan_data 结构（由 Claude skill 生成后传入）:
    {
        "title": "方案标题",
        "product_name": "产品名",
        "brand": "品牌名",
        "platform": "Kickstarter",
        "goal": 500000,
        "date": "2026-04-02",
        "modules": [
            {
                "id": "mod1",
                "emoji": "🎯",
                "title": "模块标题",
                "content_html": "<p>模块内容HTML...</p>"
            },
            ...
        ]
    }
    """

    title = plan_data.get("title", "众筹整合营销方案")
    product = plan_data.get("product_name", "")
    brand = plan_data.get("brand", "")
    platform = plan_data.get("platform", "Kickstarter")
    goal = plan_data.get("goal", 0)
    date = plan_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    modules = plan_data.get("modules", [])

    # 生成目录
    toc_items = []
    for mod in modules:
        toc_items.append(
            f'<li class="toc-item"><a href="#{mod["id"]}">{mod.get("emoji", "")} {mod["title"]}</a></li>'
        )
        # 子章节
        for sub in mod.get("subs", []):
            toc_items.append(
                f'<li class="toc-item sub"><a href="#{sub["id"]}">{sub["title"]}</a></li>'
            )

    toc_html = "\n".join(toc_items)

    # 生成模块内容
    content_parts = []
    for mod in modules:
        content_parts.append(
            make_section(mod["id"], mod.get("emoji", ""), mod["title"], mod.get("content_html", ""))
        )

    content_html = "\n<hr class='divider'>\n".join(content_parts)

    # 组装完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>
{FEISHU_CSS}
</style>
</head>
<body>

<div class="layout">
    <!-- 左侧目录 -->
    <nav class="sidebar">
        <div class="sidebar-title">📋 目录导航</div>
        <ul class="toc-list">
            {toc_html}
        </ul>
    </nav>

    <!-- 主内容 -->
    <main class="main">
        <h1 class="doc-title">{esc(title)}</h1>
        <div class="doc-meta">
            <span>📦 产品：{esc(product)}</span>
            <span>🏢 品牌：{esc(brand)}</span>
            <span>🚀 平台：{esc(platform)}</span>
            <span>🎯 目标：{format_usd(goal) if goal else 'TBD'}</span>
            <span>📅 日期：{esc(date)}</span>
        </div>

        {content_html}

        <hr class="divider">
        <p style="text-align:center; color:var(--text-light); font-size:12px; margin-top:40px;">
            Generated by MadSpace Marketing Plan Generator | {esc(date)}
        </p>
    </main>
</div>

<script>
{FEISHU_JS}
</script>
</body>
</html>"""

    return full_html


# ============================================================
# 辅助函数：供 Claude skill 直接调用
# ============================================================

def build_budget_summary_html(goal):
    """生成预算总览模块的 HTML"""
    b = calculate_budget(goal)

    # KPI 卡片
    kpis = make_kpi_cards([
        {"label": "众筹目标", "value": format_usd(goal)},
        {"label": "营销总预算", "value": format_usd(b['total'])},
        {"label": "预估Leads", "value": f"{int(b['est_leads'])}"},
        {"label": "预估广告销售额", "value": format_usd(b['est_sales'])},
    ])

    # 预算分配表
    budget_table = make_table(
        ["费用项目", "占比", "金额"],
        [
            ["预热广告（30天）", "4.40%", format_usd(b['preheat_ads'])],
            ["上线广告（45天）", "8.72%", format_usd(b['launch_ads'])],
            ["KOL 合作", "2.40%", format_usd(b['kol'])],
            ["媒体新闻稿", "0.40%", format_usd(b['media_pr'])],
            ["众筹社群营销", "1.44%", format_usd(b['community'])],
            ["其他营销工具", "0.30%", format_usd(b['tools'])],
            ["抽奖奖品", "0.30%", format_usd(b['giveaway'])],
            [f"<strong>合计</strong>", "<strong>17.96%</strong>", f"<strong>{format_usd(b['total'])}</strong>"],
        ]
    )

    # 平台分配
    platform_table = make_table(
        ["平台", "预热期预算", "众筹期预算", "合计"],
        [
            ["Meta（FB/IG）60%",
             format_usd(b['preheat_meta']),
             format_usd(b['launch_meta']),
             format_usd(b['preheat_meta'] + b['launch_meta'])],
            ["Google/YouTube 40%",
             format_usd(b['preheat_google']),
             format_usd(b['launch_google']),
             format_usd(b['preheat_google'] + b['launch_google'])],
            ["<strong>合计</strong>",
             f"<strong>{format_usd(b['preheat_ads'])}</strong>",
             f"<strong>{format_usd(b['launch_ads'])}</strong>",
             f"<strong>{format_usd(b['preheat_ads'] + b['launch_ads'])}</strong>"],
        ],
        style="blue"
    )

    return f"""
{kpis}
<h3>营销费用预估表</h3>
{budget_table}
<h3>广告平台预算分配</h3>
{platform_table}
"""


def build_daily_ad_plan_html(goal):
    """生成完整的每日投广计划HTML"""
    b = calculate_budget(goal)

    html_parts = []

    # 预热期
    html_parts.append("<h3>📊 预热期每日投广计划</h3>")
    html_parts.append(make_callout(
        f"预热期广告总预算：{format_usd(b['preheat_ads'])} | Meta: {format_usd(b['preheat_meta'])} | Google: {format_usd(b['preheat_google'])} | 周期：30天",
        style="blue", title="💰 预热期预算概览"
    ))

    html_parts.append("<h4>Meta 预热期每日计划</h4>")
    html_parts.append(generate_daily_plan_table(b['preheat_meta_weeks'], "preheat"))

    html_parts.append("<h4>Google 预热期每日计划</h4>")
    html_parts.append(generate_daily_plan_table(b['preheat_google_weeks'], "preheat"))

    # 众筹期
    html_parts.append("<h3>📊 众筹期每日投广计划</h3>")
    html_parts.append(make_callout(
        f"众筹期广告总预算：{format_usd(b['launch_ads'])} | Meta: {format_usd(b['launch_meta'])} | Google: {format_usd(b['launch_google'])} | 周期：45天 | 目标ROAS: 2.5",
        style="yellow", title="💰 众筹期预算概览"
    ))

    html_parts.append("<h4>Meta 众筹期每日计划</h4>")
    html_parts.append(generate_daily_plan_table(b['launch_meta_weeks'], "launch"))

    html_parts.append("<h4>Google 众筹期每日计划</h4>")
    html_parts.append(generate_daily_plan_table(b['launch_google_weeks'], "launch"))

    # Benchmark
    html_parts.append("<h3>📈 行业 Benchmark 指标</h3>")
    html_parts.append(make_table(
        ["阶段", "CTR", "CPC", "CPM", "CVR", "其他"],
        [
            ["预热期", "2%-3%", "$0.8-$1", "$18-$20", "15%-20%（→留邮箱）", "CPL: $3-$5"],
            ["众筹期", "0.5%-2%", "$1-$1.5", "$10-$25", "0.5%-1%（→下单）", "ROAS: 1.5-3.5"],
        ],
        style="green"
    ))

    return "\n".join(html_parts)


# ============================================================
# CLI 入口
# ============================================================

def main():
    """命令行入口：python generate_html.py --json data.json --output plan.html"""
    import argparse

    parser = argparse.ArgumentParser(description="众筹营销方案飞书风格HTML生成器")
    parser.add_argument("--json", required=True, help="方案数据JSON文件路径")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")

    args = parser.parse_args()

    with open(args.json, 'r', encoding='utf-8') as f:
        plan_data = json.load(f)

    html_content = generate_full_html(plan_data)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML 文件已生成: {args.output}")
    print(f"   文件大小: {os.path.getsize(args.output) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
