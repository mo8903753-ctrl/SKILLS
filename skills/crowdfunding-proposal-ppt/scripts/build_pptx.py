#!/usr/bin/env python3
"""Fallback editable PPTX builder for crowdfunding proposal decks.

This script is intentionally conservative. It generates a native editable PPTX
from researched slide data when Canva or a canonical PPT template is not
available. It does not replace template-matching QA.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ANCHORS = [
    (
        500_000,
        {
            "prelaunch_ads": 22_000,
            "campaign_ads": 44_000,
            "kol": 6_000,
            "media_pr": 5_000,
            "community": 10_000,
            "tools": 1_500,
            "giveaway": 1_500,
        },
    ),
    (
        1_000_000,
        {
            "prelaunch_ads": 55_000,
            "campaign_ads": 107_000,
            "kol": 10_000,
            "media_pr": 5_000,
            "community": 22_000,
            "tools": 1_500,
            "giveaway": 1_500,
        },
    ),
    (
        2_000_000,
        {
            "prelaunch_ads": 125_000,
            "campaign_ads": 227_000,
            "kol": 20_000,
            "media_pr": 5_000,
            "community": 50_000,
            "tools": 3_000,
            "giveaway": 8_000,
        },
    ),
]

SOURCE_SPLIT = {
    "Crowdfunding platform": 0.45,
    "Campaign ads": 0.30,
    "Prelaunch email": 0.10,
    "Other": 0.10,
    "Crowdfunding community": 0.03,
    "PR/KOL": 0.02,
}


def money(value: float) -> str:
    return f"${int(round(value)):,}"


def round_budget(value: float, unit: int = 100) -> int:
    return int(round(value / unit) * unit)


def interpolate_budget(goal: float) -> Tuple[Dict[str, int], str]:
    for anchor_goal, anchor_budget in ANCHORS:
        if math.isclose(goal, anchor_goal):
            return dict(anchor_budget), "Exact budget anchor."

    if goal <= ANCHORS[0][0]:
        base_goal, base = ANCHORS[0]
        ratio = goal / base_goal
        note = "Below $500k anchor; scaled from nearest anchor and needs manual review."
        return {k: round_budget(v * ratio) for k, v in base.items()}, note

    if goal >= ANCHORS[-1][0]:
        base_goal, base = ANCHORS[-1]
        ratio = goal / base_goal
        note = "Above $2M anchor; scaled from nearest anchor and needs manual review."
        return {k: round_budget(v * ratio) for k, v in base.items()}, note

    for (low_goal, low), (high_goal, high) in zip(ANCHORS, ANCHORS[1:]):
        if low_goal <= goal <= high_goal:
            t = (goal - low_goal) / (high_goal - low_goal)
            out = {
                k: round_budget(low[k] + (high[k] - low[k]) * t)
                for k in low.keys()
            }
            return out, "Linear interpolation between budget anchors."

    raise ValueError("Unreachable budget interpolation state")


def budget_model(goal: float, aov: float | None = None) -> Dict[str, Any]:
    channels, note = interpolate_budget(goal)
    total = sum(channels.values())
    ad_split = {
        "prelaunch_meta": round_budget(channels["prelaunch_ads"] * 0.60),
        "prelaunch_google": round_budget(channels["prelaunch_ads"] * 0.40),
        "campaign_meta": round_budget(channels["campaign_ads"] * 0.70),
        "campaign_google": round_budget(channels["campaign_ads"] * 0.30),
    }
    source_orders = {
        name: round(goal * share, 2) for name, share in SOURCE_SPLIT.items()
    }
    return {
        "goal": goal,
        "aov": aov,
        "sales_units": round(goal / aov) if aov else None,
        "channels": channels,
        "marketing_total": total,
        "ad_split": ad_split,
        "source_split": SOURCE_SPLIT,
        "source_revenue": source_orders,
        "note": note,
    }


def add_text(slide, text: str, x, y, w, h, size=18, bold=False, color="FFFFFF"):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor.from_string(color)
    return box


def add_title(slide, title: str, subtitle: str = ""):
    add_text(slide, title, Inches(0.55), Inches(0.35), Inches(12.2), Inches(0.55), 27, True)
    if subtitle:
        add_text(slide, subtitle, Inches(0.58), Inches(0.98), Inches(11.5), Inches(0.32), 12, False, "C9CDD3")


def add_footer(slide):
    add_text(slide, "MadSpace | Crowdfunding Proposal", Inches(9.2), Inches(7.1), Inches(3.7), Inches(0.25), 8, False, "AEB4BE")


def set_background(slide, color="161616"):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color)


def add_table(slide, rows: List[List[str]], x, y, w, h, header=True):
    table_shape = slide.shapes.add_table(len(rows), len(rows[0]), x, y, w, h)
    table = table_shape.table
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            cell = table.cell(r, c)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor.from_string("E7F0DF" if r == 0 and header else "FFFFFF")
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10 if r else 11)
                p.font.bold = bool(r == 0 and header)
                p.font.color.rgb = RGBColor.from_string("111111")
    return table_shape


def add_bullets(slide, bullets: Iterable[str], x, y, w, h, size=15):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    for i, item in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor.from_string("FFFFFF")
        p.space_after = Pt(8)
    return box


def add_image_or_placeholder(slide, path: str | None, label: str, x, y, w, h):
    if path and Path(path).exists():
        slide.shapes.add_picture(path, x, y, w, h)
        return
    shape = slide.shapes.add_shape(1, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string("30343A")
    shape.line.color.rgb = RGBColor.from_string("5B6470")
    txt = shape.text_frame
    txt.text = label
    txt.paragraphs[0].font.size = Pt(14)
    txt.paragraphs[0].font.color.rgb = RGBColor.from_string("CDD4DD")
    txt.paragraphs[0].alignment = PP_ALIGN.CENTER


def add_section(prs, title: str):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_text(slide, title, Inches(0.8), Inches(2.7), Inches(11.6), Inches(0.7), 34, True)
    add_footer(slide)


def add_content_slide(prs, title: str, bullets: List[str], subtitle: str = ""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_title(slide, title, subtitle)
    add_bullets(slide, bullets[:7], Inches(0.8), Inches(1.65), Inches(11.6), Inches(4.9))
    add_footer(slide)


def build_deck(data: Dict[str, Any], output: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    project = data.get("project", {})
    goal = float(project.get("funding_goal_usd", 1_000_000))
    budget_goals = project.get("budget_goals") or [goal]
    budget_goals = [float(item) for item in budget_goals]
    aov = project.get("aov")
    aov = float(aov) if aov else None
    budget = budget_model(goal, aov)

    # Cover
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_text(slide, "MadSpace", Inches(10.4), Inches(0.55), Inches(2.3), Inches(0.4), 22, True)
    add_text(slide, project.get("product_name", "Product Name"), Inches(0.7), Inches(2.35), Inches(11.7), Inches(0.85), 36, True)
    add_text(slide, "美国众筹方案", Inches(0.75), Inches(3.25), Inches(5.5), Inches(0.45), 22, True, "F4F4F4")
    goal_label = " / ".join(money(item) for item in budget_goals)
    add_text(slide, f"目标金额：{goal_label}", Inches(0.78), Inches(4.05), Inches(6.2), Inches(0.36), 16, False, "C9CDD3")
    add_footer(slide)

    # Goal
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_title(slide, "众筹项目目标", project.get("platform", "Kickstarter / Indiegogo"))
    rows = [["指标", "目标"]]
    for item_goal in budget_goals:
        item_budget = budget_model(item_goal, aov)
        rows.append([
            f"销售额目标 {money(item_goal)}",
            f"{item_budget['sales_units']:,} 单" if item_budget["sales_units"] else "待 AOV 确认",
        ])
    rows.extend([
        ["众筹开始日期", project.get("launch_date", "TBD")],
        ["众筹结束日期", project.get("end_date", "TBD")],
    ])
    add_table(slide, rows, Inches(1.1), Inches(1.8), Inches(6.1), Inches(3.3))
    add_bullets(slide, data.get("strategy_summary", ["基于产品信息和调研结果生成策略摘要。"])[:4], Inches(7.7), Inches(1.9), Inches(4.7), Inches(3.3), 15)
    add_footer(slide)

    add_section(prs, "美国市场洞察")
    for item in data.get("market_insights", [])[:4]:
        add_content_slide(prs, item.get("title", "市场洞察"), item.get("bullets", []), item.get("subtitle", ""))

    add_section(prs, "受众定位与营销打法")
    for persona in data.get("personas", [])[:5]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, persona.get("name", "用户画像"), persona.get("scenario", ""))
        add_image_or_placeholder(slide, persona.get("image_path"), "Persona image", Inches(0.8), Inches(1.55), Inches(4.4), Inches(4.6))
        add_bullets(slide, [
            f"痛点：{persona.get('pain_point', '')}",
            f"沟通重点：{persona.get('message', '')}",
            f"素材方向：{persona.get('creative_direction', '')}",
        ], Inches(5.55), Inches(1.75), Inches(6.5), Inches(3.8), 15)
        add_footer(slide)

    for concept in data.get("concepts", [])[:3]:
        add_content_slide(prs, concept.get("title", "传播核心概念"), [
            concept.get("english", ""),
            concept.get("chinese", ""),
            concept.get("usage", ""),
        ])

    add_section(prs, "美国众筹策略")
    competitors = data.get("competitors", [])
    if competitors:
        rows = [["项目", "募集金额", "Backers", "品类", "启发"]]
        for comp in competitors[:6]:
            rows.append([
                comp.get("name", ""),
                comp.get("funding", ""),
                comp.get("backers", ""),
                comp.get("category", ""),
                comp.get("insight", ""),
            ])
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, "竞品与市场参考")
        add_table(slide, rows, Inches(0.55), Inches(1.45), Inches(12.2), Inches(4.8))
        add_footer(slide)

    for block in data.get("ad_strategy", [])[:5]:
        add_content_slide(prs, block.get("title", "广告策略"), block.get("bullets", []), block.get("subtitle", ""))

    # Budget slides
    add_section(prs, "预算评估")
    channel_labels = {
        "prelaunch_ads": "预热广告",
        "campaign_ads": "上线广告",
        "kol": "KOL合作",
        "media_pr": "媒体新闻稿",
        "community": "众筹社群营销",
        "tools": "其他营销工具",
        "giveaway": "抽奖奖品",
    }
    for item_goal in budget_goals:
        item_budget = budget_model(item_goal, aov)
        rows = [["费用项目", "预算", "占目标比例"]]
        for key, value in item_budget["channels"].items():
            rows.append([channel_labels[key], money(value), f"{value / item_goal:.2%}"])
        rows.append(["营销费用合计", money(item_budget["marketing_total"]), f"{item_budget['marketing_total'] / item_goal:.2%}"])
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, f"预算评估 - 目标 {money(item_goal)}")
        add_table(slide, rows, Inches(0.75), Inches(1.3), Inches(7.2), Inches(5.45))
        add_bullets(slide, [item_budget["note"], "广告拆分：预热期 Meta 60% / Google 40%；上线期 Meta 70% / Google 30%。"], Inches(8.3), Inches(1.7), Inches(4.4), Inches(3.2), 14)
        add_footer(slide)

        rows = [["阶段", "Meta", "Google", "合计"], [
            "预热期",
            money(item_budget["ad_split"]["prelaunch_meta"]),
            money(item_budget["ad_split"]["prelaunch_google"]),
            money(item_budget["channels"]["prelaunch_ads"]),
        ], [
            "上线/众筹期",
            money(item_budget["ad_split"]["campaign_meta"]),
            money(item_budget["ad_split"]["campaign_google"]),
            money(item_budget["channels"]["campaign_ads"]),
        ]]
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, f"广告预算拆分 - {money(item_goal)}")
        add_table(slide, rows, Inches(1.1), Inches(1.7), Inches(7.0), Inches(2.2))
        add_footer(slide)

        rows = [["订单来源", "金额占比", "预估金额"]]
        for name, share in item_budget["source_split"].items():
            rows.append([name, f"{share:.0%}", money(item_budget["source_revenue"][name])])
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, f"美国各流量订单来源预估 - {money(item_goal)}")
        add_table(slide, rows, Inches(0.9), Inches(1.35), Inches(8.2), Inches(4.7))
        add_footer(slide)

    add_section(prs, "PR / KOL")
    for kol in data.get("kols", [])[:10]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        add_title(slide, kol.get("channel_name", "KOL Channel"), kol.get("tier", ""))
        add_image_or_placeholder(slide, kol.get("screenshot_path"), "YouTube screenshot", Inches(0.75), Inches(1.45), Inches(5.5), Inches(4.2))
        add_bullets(slide, [
            f"订阅量：{kol.get('subscribers', 'TBD')}",
            f"内容方向：{kol.get('content_focus', '')}",
            f"适配理由：{kol.get('fit_reason', '')}",
            f"链接：{kol.get('channel_url', kol.get('video_url', ''))}",
        ], Inches(6.65), Inches(1.55), Inches(5.9), Inches(4.0), 13)
        add_footer(slide)

    add_section(prs, "运营与服务保障")
    fixed_slides = [
        ("汇报机制", ["周例会与详细 to do list", "每日投广数据表", "随时拉通平台对接", "项目结束后完整复盘"]),
        ("项目人员配置", ["PR总监", "广告投放专家", "创意总监", "文案团队", "英语客服"]),
        ("迈思海外众筹成绩", ["单项目最高金额", "累计项目金额", "累计海外用户", "累计众筹项目"]),
    ]
    for title, bullets in fixed_slides:
        add_content_slide(prs, title, bullets)

    add_section(prs, "项目排期表")
    for block in data.get("timeline", [])[:3]:
        add_content_slide(prs, block.get("title", "项目时间表"), block.get("bullets", []), block.get("subtitle", ""))

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_text(slide, "联系我们", Inches(0.8), Inches(1.2), Inches(7.2), Inches(0.7), 34, True)
    add_bullets(slide, [
        "w@mad-space.com",
        "+86 186-0107-7190",
        "www.madspace-global.com/",
        "北京｜深圳｜美国｜台北",
    ], Inches(0.9), Inches(2.3), Inches(7.0), Inches(2.7), 17)
    add_footer(slide)

    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)


def sample_data(goal: float, aov: float | None) -> Dict[str, Any]:
    return {
        "project": {
            "product_name": "Archon Scout Mini 384",
            "platform": "Kickstarter / Indiegogo",
            "funding_goal_usd": goal,
            "aov": aov,
            "launch_date": "2026-08-04",
            "end_date": "2026-09-22",
        },
        "strategy_summary": [
            "轻量化热成像模块具备多场景扩展潜力。",
            "打法以广告测试、KOL验证、社群转化和媒体信任组合推进。",
            "高客单价产品需要真实样机、技术背书和 FAQ 降低决策阻力。",
        ],
        "market_insights": [
            {"title": "品类容量已被验证", "bullets": ["夜视和热成像在海外众筹存在百万级案例。", "用户需求集中在夜间安全、户外观察、车载巡查和内容创作。"]},
            {"title": "差异化来自轻量与多挂载", "bullets": ["避免陷入低价夜视竞争。", "强调轻量、热成像、多挂载和内容分享。"]},
        ],
        "personas": [
            {"name": "硬核户外探索者", "scenario": "夜间徒步 / 露营 / 越野", "pain_point": "夜间看不清，装备重。", "message": "轻量热成像，先发现目标。", "creative_direction": "夜间营地和山地搜索场景。"},
            {"name": "安防与战术爱好者", "scenario": "巡逻 / 安全 / 装备", "pain_point": "传统热像设备贵且形态单一。", "message": "非枪瞄替代品，多用途挂载模块。", "creative_direction": "设备可靠性和安全观察。"},
        ],
        "concepts": [
            {"title": "Conquer the Night", "english": "The ultimate tactical companion for hunting, hiking, and security.", "chinese": "征服黑夜：狩猎、徒步与安防的战术伴侣。", "usage": "主视觉与广告标题。"},
        ],
        "competitors": [
            {"name": "AKASO Sight-300", "funding": "$572,874", "backers": "2,748", "category": "AI 全彩夜视", "insight": "价格低，品牌认知强。"},
            {"name": "Duovox Ultra", "funding": "$1,191,648", "backers": "6,769", "category": "全彩夜视", "insight": "证明品类容量。"},
        ],
        "ad_strategy": [
            {"title": "Meta 六类人群标签", "bullets": ["户外夜间探索", "狩猎/战术", "摄影/创作者", "车载/安防/农牧", "科技早鸟", "再营销/LAL"]},
            {"title": "Google / YouTube 关键词", "bullets": ["High-intent keywords", "Scenario keywords", "Competitor keywords", "In-market placements"]},
        ],
        "kols": [],
        "timeline": [
            {"title": "美国众筹时间表规划", "bullets": ["筹备期：素材、项目数据对接。", "预热期：页面上线和广告测试。", "众筹初期：PR/KOL同步发布。", "众筹后期：倒计时冲刺。"]},
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Project JSON after research")
    parser.add_argument("--output", type=Path, default=Path("crowdfunding-proposal.pptx"))
    parser.add_argument("--goal", type=float, default=1_000_000)
    parser.add_argument("--aov", type=float)
    parser.add_argument("--budget-only", action="store_true")
    parser.add_argument("--sample-archon", action="store_true")
    args = parser.parse_args()

    if args.budget_only:
        print(json.dumps(budget_model(args.goal, args.aov), indent=2, ensure_ascii=False))
        return

    if args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        data = sample_data(args.goal, args.aov)

    build_deck(data, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
