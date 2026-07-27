#!/usr/bin/env python3
"""Generate a pretest report HTML/PDF from Meta breakdown exports.

This implementation supports partial datasets and still renders a complete
report skeleton, including:
- benchmark comparison
- gender / placement breakdown analysis
- insight summary
- follow-up budget estimation
- email collection estimation
- fixed strategy, KOL, community, risk, and closing sections
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from openpyxl import load_workbook


ALIASES = {
    "gender": ["性别", "Gender"],
    "placement": ["平台", "Placement", "Publisher platform", "Platform position", "版位"],
    "spend": ["已花费金额 (USD)", "Amount spent (USD)", "Amount spent", "花费"],
    "leads": ["潜在客户人数", "Leads", "潜在客户", "Results", "成效"],
    "cpl": ["单次成效费用", "Cost per result", "CPL"],
    "impressions": ["展示次数", "Impressions"],
    "clicks": ["链接点击量", "Link clicks", "点击量"],
    "ctr": ["链接点击率", "Link CTR", "CTR"],
    "reach": ["覆盖人数", "Reach"],
    "frequency": ["频次", "Frequency"],
    "cpm": ["千次展示费用", "CPM"],
    "cpc": ["单次链接点击费用", "Cost per link click", "CPC"],
    "report_start": ["报告开始日期", "Report start"],
    "report_end": ["报告结束日期", "Report end"],
}

BENCHMARKS = {
    "CPM": {"low": 18.0, "high": 20.0, "prefer_low": True},
    "CTR": {"low": 2.0, "high": 3.0, "prefer_low": False},
    "CPC": {"low": 0.8, "high": 1.0, "prefer_low": True},
    "CPL": {"low": 3.0, "high": 5.0, "prefer_low": True},
    "CVR": {"low": 15.0, "high": 20.0, "prefer_low": False},
}

LABEL_MAP = {
    "male": "男性",
    "female": "女性",
    "unknown": "未知",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "messenger": "Messenger",
    "threads": "Threads",
}

SECTION_TITLES = {
    "gender": "性别表现分析",
    "placement": "版位表现分析",
}

GLOSSARY = [
    ("CTR", "点击率（点击次数 / 展示次数）"),
    ("CPC", "点击成本（花费 / 点击次数）"),
    ("CPM", "千次展示费用（花费 / 展示次数 x 1000）"),
    ("CVR", "成果转化率（成果 / 点击次数）"),
    ("CPL", "Lead 收集成本（花费 / Lead 数）"),
]

FOLLOW_UP_STRATEGIES = [
    "鉴于目前的广告数据，我们认为广告所带来的转化效果在行业普遍指标内，MadSpace 在后续推广计划内将会致力于降低 CPL，争取以同样预算收集到更多销售线索。",
    "预热邮箱的收集与广告数据对于上线后的投广、页面安排、KOL 合作会起到一定的帮助，有助于我们更准确地锚定受众群体。",
    "众筹上线后广告安排 $50,000 美金，理想 ROAS 在 2.5~3 之间，若早期间发现 ROAS 长期低于此标准，可立即将预算灵活调整到众筹社区。（连续 5 天无转化即可视为低于标准）",
    "项目订单转化主要通过以下六个渠道：预热用户和 Facebook 群组转化、KOL 流量引导、众筹平台站内资源、上线后广告投放、众筹社区以及其他流量。",
    "同时充分利用 6 个订单渠道的资源来源，在项目上线前三天尽可能推动较高的金额，以吸引后续更多自然流量。同时，上线后的第三方会员社区预计有 10 多个，建议把 MadSpace 推荐的社区都做起来，效果好的（ROI 大于 2 可以考虑二推三推）。",
]

TRAFFIC_SOURCES = [
    ("众筹平台流量转化", 50, "#10B981", "众筹平台对热度越高的项目会给予越多的流量支援，并且是免费流量。充分的预热与资源的花费都是为了换来众筹平台更多的流量比重，同时这也是项目订单的最大来源。一般范围为 30~60%。"),
    ("众筹期投广转化", 30, "#3B82F6", "众筹期广告投放可为项目带来持续不断的热度与销量，是促成项目达成目标金额的有力手段，并且通过广告可以更精准了解对产品感兴趣的用户画像，对品牌的拓展帮助极大。"),
    ("其他转化", 10, "#6B7280", "其他诸如品牌老用户、kickbooster、社媒流量、自然流量等转化渠道，这些流量会随项目金额上升而等比扩大。"),
    ("预热邮箱转化", 4, "#F59E0B", "通过预热期邮箱收集，在上线首周通过 EDM 进行第一波订单转化，迅速提升项目在平台的排名，进而引来更多平台资源与流量。此外，预热邮箱还可以作为上线后广告的类似受众名单进行用户画像的更精准定位。"),
    ("PR / KOL 转化", 3, "#EF4444", "PR 与 KOL 的露出大多数情况不是以转化为首要目标，而是使消费者增加对产品的信任度以及了解产品使用的第一手心得，从而增加下单欲望。"),
    ("众筹社区转化", 3, "#8B5CF6", "众筹社区为欧美众筹中常用到的营销手法，各大众筹社群都有大量的众筹相关用户，通过对用户的 EDM 推送引导兴趣用户下单，参考 ROI 为 2~5。"),
]

ALLOCATION_ITEMS = [
    ("预热广告（预热 30 天）", 0.2558, "预热广告目的：收集预热邮箱。预热投广收集邮箱是上线流量保障的重要来源，也会驱动站内活动。结合付定金确定折扣等活动，可在上线前 48 小时获取大量早鸟订单。"),
    ("上线广告（上线 45-60 天）", 0.5814, "上线广告目的：在上线期，通过广告投放，直接引流到众筹页面形成购买转化。"),
    ("KOL 合作", 0.0581, "将尽可能通过样机置换的方式获取测评资源。如有合作费用，会和项目方沟通确认是否合作。通常每个众筹项目大概会有 6-8 个评测露出。"),
    ("众筹社群营销", 0.0930, "这是一个社群的官网，他们有自己的订阅用户。社群会定期给订阅用户发送 newsletter，通知用户一些新品讯息，达成销售转化。"),
    ("其他营销工具", 0.0058, "EDM 工具、landing page 建站工具、perk 设置工具等零散费用，一般几十到一百美金不等。"),
    ("抽奖奖品", 0.0058, "众筹预热期及上线期间的抽奖奖品将根据项目实际情况进行灵活调整。具体费用将通过沟通协商确定。"),
]

ROI_CHANNELS = [
    ("预热邮箱", 0.91, "#3B82F6"),
    ("众筹期投广", 3.00, "#3B82F6"),
    ("PR / KOL", 4.00, "#3B82F6"),
    ("众筹社区", 3.75, "#3B82F6"),
]

COMMUNITY_ROWS = [
    ("Backermany", "$499 - 项目在 newsletter 的普通位置", "$599 - 项目在 newsletter 的 top spot", "$899 - Dedicated newsletter"),
    ("Backerspaces", "$399 - 普通位置", "$499 - top spot", "$799 - Dedicated newsletter"),
    ("PledgeBox 替补", "IGG 项目专属: $799+25% / $799+20%", "KS 项目专属: $999+25%/20% / $899+25%/20% / $799+25%/20%", "—"),
    ("Backerviews", "$349 - Shared Newsletter (2nd or 3rd slot)", "$499 - Shared Newsletter (top 1st slot)", "$799 - Dedicated newsletter"),
    ("reBacker", "$349+20% 佣金 - top spot", "$499+20% 佣金 - Dedicated newsletter", "—"),
    ("Kickstartech", "$399 - 和其他项目共享一个 newsletter（2 次）", "$549 - 和其他项目共享一个 newsletter(1 次) + 专属 newsletter（1 次）", "$899 - 共享 + top spot + 专属 newsletter"),
    ("Backer Crew", "$399 - 项目在 newsletter 的普通位置", "$399+成交金额 10% 佣金 - 项目在 newsletter 的 top spot", "$999 - Dedicated newsletter"),
    ("Backer Now", "$379+成交金额 20% 佣金 - 专属 newsletter，触达受众 55K", "$879+成交金额 10% 佣金 - 专属 newsletter，触达受众 175K", "—"),
    ("iGadget", "$249 - 项目在 newsletter 的普通位置", "$399 - 项目在 newsletter 的 top spot", "$599 - Dedicated newsletter"),
    ("Backer Land", "$249 - 项目在 newsletter 的普通位置", "$349 - 项目在 newsletter 的 top spot", "—"),
]

KOL_STEPS = [
    "预热第一周至第四周：建立候选名单给品牌方审核，确认合作的 KOL 尽快进行付费并寄送样机。",
    "预热第三周至第四周：沟通大致脚本内容并开始拍摄。",
    "众筹上线：持续安排 KOL 内容发布，多的话每周安排 3-5 位。",
    "挑选流量表现较好的视频植入众筹详情页，或者用来剪辑广告素材。",
    "安排 Kickbooster 让 KOL 与产品销量绑定，增加积极性。",
]

RISK_ITEMS = [
    ("预热 / 众筹期间的投放数据与预期有所差距", "此情况可能与产品吸引力、产品价格、素材品质、市场情况、竞品情况、受众疲劳等多项因素有关。MadSpace 团队将尽最大努力优化整体预热数据。若改善范围有限，建议将预算降低或保留至其他投流渠道，以达成在此风险情况下最佳收益。"),
    ("预热 Leads 的转化率没有达到理想情况", "此情况与产品本身吸引力、价格诱惑力、评测视频推力等因素有关。虽然 MadSpace 团队预测的数据在 1%-3% 之间，但少数情况会低于此数值。若发生此风险，可以多加 EDM 推广力度，或承诺给与预热用户额外赠品来促进转化。"),
    ("KOL 视频播放量 / 转化量不尽理想", "KOL 的价值不仅在直接转化，还在于建立消费者信任感并展示产品实际使用心得。MadSpace 团队会将部分 KOL 视频素材用于二次剪辑投广，达成资源最大化利用。"),
    ("众筹社区转化率未达理想", "部分众筹社区拥有 ROI 不足 1 时的退差价机制，并且 MadSpace 团队有历史经验效果较佳的推荐社区。建议先按预算测试推荐社区，若 ROI 表现较好再做二推、三推。"),
    ("众筹平台带来的流量未达预期", "根据以往项目经验，自带流量越多，平台流量扶持通常越大。但由于平台受众数量与市场情况变化，有可能出现实际平台流量不佳的风险。MadSpace 将积极与平台协商资源，也建议品牌方加大整体投流预算，将项目排名推至更前。"),
]

CLOSING_TEXT = "感谢您对 MadSpace 团队的支持与指教，本次前测能一定量体现出产品在后续众筹的情况，故此安排以上后续方案。若有任何问题欢迎随时联系我们。若是对方案内容、众筹目标、预算规划等范畴有任何修改建议，也请随时提出。"


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


@dataclass
class ReportInputs:
    product_name: Optional[str]
    date_range: Optional[str]
    crowdfunding_goal: Optional[float]
    average_price: Optional[float]
    output_dir: Path
    meta_summary: Optional[Path]
    meta_daily: Optional[Path]
    meta_demographics: Optional[Path]
    meta_placement: Optional[Path]
    meta_creatives: Optional[Path]
    questionnaire_json: Optional[Path]
    notes_json: Optional[Path]


@dataclass
class BreakdownRow:
    label: str
    raw_label: str
    spend: float
    leads: float
    reach: float
    frequency: float
    impressions: float
    clicks: float
    ctr: float
    cpc: float
    cpm: float
    cpl: float
    cvr: float


@dataclass
class BreakdownSection:
    kind: str
    title: str
    dimension_label: str
    source_path: Path
    start_date: Optional[str]
    end_date: Optional[str]
    rows: list[BreakdownRow]

    @property
    def totals(self) -> BreakdownRow:
        spend = sum(row.spend for row in self.rows)
        leads = sum(row.leads for row in self.rows)
        reach = sum(row.reach for row in self.rows)
        impressions = sum(row.impressions for row in self.rows)
        clicks = sum(row.clicks for row in self.rows)
        frequency = safe_div(impressions, reach) if reach else 0.0
        ctr = safe_div(clicks * 100.0, impressions)
        cpc = safe_div(spend, clicks)
        cpm = safe_div(spend * 1000.0, impressions)
        cpl = safe_div(spend, leads)
        cvr = safe_div(leads * 100.0, clicks)
        return BreakdownRow("合计", "total", spend, leads, reach, frequency, impressions, clicks, ctr, cpc, cpm, cpl, cvr)


@dataclass
class EstimateContext:
    has_inputs: bool
    crowdfunding_goal: Optional[float]
    average_price: Optional[float]
    marketing_total: Optional[float]
    total_orders: Optional[float]
    first_three_day_orders: Optional[float]
    email_orders: Optional[float]
    required_emails: Optional[float]
    warmup_spend: Optional[float]
    warmup_share: Optional[float]
    current_cpl: Optional[float]
    message: Optional[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate crowdfunding pretest report.")
    parser.add_argument("--product-name")
    parser.add_argument("--date-range")
    parser.add_argument("--crowdfunding-goal", type=float)
    parser.add_argument("--average-price", type=float)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--meta-summary")
    parser.add_argument("--meta-daily")
    parser.add_argument("--meta-demographics")
    parser.add_argument("--meta-placement")
    parser.add_argument("--meta-creatives")
    parser.add_argument("--questionnaire-json")
    parser.add_argument("--notes-json")
    return parser.parse_args()


def build_inputs(args: argparse.Namespace) -> ReportInputs:
    return ReportInputs(
        product_name=(args.product_name or "").strip() or None,
        date_range=(args.date_range or "").strip() or None,
        crowdfunding_goal=args.crowdfunding_goal,
        average_price=args.average_price,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        meta_summary=resolve_optional_path(args.meta_summary),
        meta_daily=resolve_optional_path(args.meta_daily),
        meta_demographics=resolve_optional_path(args.meta_demographics),
        meta_placement=resolve_optional_path(args.meta_placement),
        meta_creatives=resolve_optional_path(args.meta_creatives),
        questionnaire_json=resolve_optional_path(args.questionnaire_json),
        notes_json=resolve_optional_path(args.notes_json),
    )


def resolve_optional_path(raw: Optional[str]) -> Optional[Path]:
    return Path(raw).expanduser().resolve() if raw else None


def ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)


def sanitize_filename(name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name.strip())
    return safe or "pretest_report"


def read_sheet_rows(path: Path) -> tuple[list[str], list[dict[str, object]]]:
    wb = load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    headers = [normalize_header(value) for value in rows[0]]
    records = []
    for values in rows[1:]:
        record = {headers[idx]: values[idx] for idx in range(min(len(headers), len(values))) if headers[idx]}
        if any(value not in (None, "") for value in record.values()):
            records.append(record)
    return headers, records


def normalize_header(value: object) -> str:
    return str(value).strip() if value is not None else ""


def find_column(headers: Iterable[str], aliases: list[str]) -> Optional[str]:
    for alias in aliases:
        for header in headers:
            if header == alias or header.lower() == alias.lower():
                return header
    return None


def normalize_number(value: object) -> float:
    if value in (None, "", "-"):
        return 0.0
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return 0.0
        return float(value)
    text = str(value).strip().replace(",", "").replace("%", "")
    if not text or text == "-":
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def normalize_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未知"
    return LABEL_MAP.get(text.lower(), text)


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def load_breakdown(path: Optional[Path], kind: str) -> Optional[BreakdownSection]:
    if not path or not path.exists():
        return None

    headers, records = read_sheet_rows(path)
    if not records:
        return None

    dimension_column = find_column(headers, ALIASES[kind])
    if not dimension_column:
        return None

    spend_column = find_column(headers, ALIASES["spend"])
    leads_column = find_column(headers, ALIASES["leads"])
    reach_column = find_column(headers, ALIASES["reach"])
    frequency_column = find_column(headers, ALIASES["frequency"])
    impressions_column = find_column(headers, ALIASES["impressions"])
    clicks_column = find_column(headers, ALIASES["clicks"])
    ctr_column = find_column(headers, ALIASES["ctr"])
    cpc_column = find_column(headers, ALIASES["cpc"])
    cpm_column = find_column(headers, ALIASES["cpm"])
    cpl_column = find_column(headers, ALIASES["cpl"])
    start_column = find_column(headers, ALIASES["report_start"])
    end_column = find_column(headers, ALIASES["report_end"])

    rows: list[BreakdownRow] = []
    starts: list[str] = []
    ends: list[str] = []

    for record in records:
        raw_label = str(record.get(dimension_column, "") or "").strip()
        if not raw_label:
            continue

        spend = normalize_number(record.get(spend_column)) if spend_column else 0.0
        leads = normalize_number(record.get(leads_column)) if leads_column else 0.0
        reach = normalize_number(record.get(reach_column)) if reach_column else 0.0
        frequency = normalize_number(record.get(frequency_column)) if frequency_column else 0.0
        impressions = normalize_number(record.get(impressions_column)) if impressions_column else 0.0
        clicks = normalize_number(record.get(clicks_column)) if clicks_column else 0.0
        ctr = normalize_number(record.get(ctr_column)) if ctr_column else 0.0
        cpc = normalize_number(record.get(cpc_column)) if cpc_column else 0.0
        cpm = normalize_number(record.get(cpm_column)) if cpm_column else 0.0
        cpl = normalize_number(record.get(cpl_column)) if cpl_column else 0.0

        if not ctr and impressions > 0 and clicks > 0:
            ctr = safe_div(clicks * 100.0, impressions)
        if not cpc and clicks > 0:
            cpc = safe_div(spend, clicks)
        if not cpm and impressions > 0:
            cpm = safe_div(spend * 1000.0, impressions)
        if not cpl and leads > 0:
            cpl = safe_div(spend, leads)
        if not frequency and reach > 0:
            frequency = safe_div(impressions, reach)

        rows.append(
            BreakdownRow(
                label=normalize_label(raw_label),
                raw_label=raw_label,
                spend=spend,
                leads=leads,
                reach=reach,
                frequency=frequency,
                impressions=impressions,
                clicks=clicks,
                ctr=ctr,
                cpc=cpc,
                cpm=cpm,
                cpl=cpl,
                cvr=safe_div(leads * 100.0, clicks),
            )
        )

        if start_column and record.get(start_column):
            starts.append(str(record[start_column]))
        if end_column and record.get(end_column):
            ends.append(str(record[end_column]))

    rows.sort(key=lambda item: item.spend, reverse=True)
    return BreakdownSection(kind, SECTION_TITLES[kind], dimension_column, path, min(starts) if starts else None, max(ends) if ends else None, rows)


def resolve_product_name(inputs: ReportInputs) -> str:
    return inputs.product_name or "Meta 广告前测项目"


def resolve_date_range(inputs: ReportInputs, sections: list[BreakdownSection]) -> str:
    if inputs.date_range:
        return inputs.date_range
    starts = [section.start_date for section in sections if section.start_date]
    ends = [section.end_date for section in sections if section.end_date]
    return f"{min(starts)} - {max(ends)}" if starts and ends else "未提供"


def pick_overall_section(sections: list[Optional[BreakdownSection]]) -> Optional[BreakdownSection]:
    for section in sections:
        if section and section.rows:
            return section
    return None


def benchmark_status(metric: str, value: float) -> str:
    config = BENCHMARKS[metric]
    if value == 0:
        return "neutral"
    if config["prefer_low"]:
        if value < config["low"]:
            return "good"
        if value > config["high"]:
            return "bad"
        return "okay"
    if value > config["high"]:
        return "good"
    if value < config["low"]:
        return "bad"
    return "okay"


def status_text(status: str) -> str:
    return {"good": "优于 Benchmark", "okay": "处于 Benchmark 区间", "bad": "低于 Benchmark 预期", "neutral": "样本不足"}[status]


def format_currency(value: Optional[float], digits: int = 2) -> str:
    return "待补充" if value is None else f"${value:,.{digits}f}"


def format_number(value: Optional[float], digits: int = 0) -> str:
    return "待补充" if value is None else f"{value:,.{digits}f}"


def format_pct(value: Optional[float], digits: int = 2) -> str:
    return "待补充" if value is None else f"{value:.{digits}f}%"


def share_text(part: float, total: float) -> str:
    return format_pct(safe_div(part * 100.0, total))


def render_metric_cards(overall: BreakdownRow) -> str:
    cards = [
        ("总花费", format_currency(overall.spend)),
        ("总 Leads", format_number(overall.leads, 0)),
        ("整体 CPL", format_currency(overall.cpl)),
        ("整体 CTR", format_pct(overall.ctr)),
        ("整体 CPC", format_currency(overall.cpc)),
        ("整体 CVR", format_pct(overall.cvr)),
    ]
    return "".join(f'<div class="card metric-card"><strong>{label}</strong><span>{value}</span></div>' for label, value in cards)


def render_benchmark_rows(overall: BreakdownRow) -> str:
    rows = []
    for metric, value in [("CPM", overall.cpm), ("CTR", overall.ctr), ("CPC", overall.cpc), ("CPL", overall.cpl), ("CVR", overall.cvr)]:
        status = benchmark_status(metric, value)
        bounds = BENCHMARKS[metric]
        low = format_currency(bounds["low"]) if metric in ("CPM", "CPC", "CPL") else format_pct(bounds["low"])
        high = format_currency(bounds["high"]) if metric in ("CPM", "CPC", "CPL") else format_pct(bounds["high"])
        current = format_currency(value) if metric in ("CPM", "CPC", "CPL") else format_pct(value)
        rows.append(f"<tr><td>{metric}</td><td>{low} - {high}</td><td class=\"{status}\">{current}</td><td>{status_text(status)}</td></tr>")
    return "".join(rows)


def render_breakdown_table(section: BreakdownSection) -> str:
    total = section.totals
    rows = []
    for row in section.rows:
        rows.append(
            "<tr>"
            f"<td>{html.escape(row.label)}</td>"
            f"<td>{format_currency(row.spend)}</td>"
            f"<td>{share_text(row.spend, total.spend)}</td>"
            f"<td>{format_number(row.leads, 0)}</td>"
            f"<td>{share_text(row.leads, total.leads)}</td>"
            f"<td>{format_currency(row.cpl)}</td>"
            f"<td>{format_pct(row.ctr)}</td>"
            f"<td>{format_currency(row.cpc)}</td>"
            f"<td>{format_pct(row.cvr)}</td>"
            "</tr>"
        )
    return "".join(rows)


def build_insights(overall: Optional[BreakdownSection], gender: Optional[BreakdownSection], placement: Optional[BreakdownSection]) -> list[str]:
    insights: list[str] = []
    if overall:
        total = overall.totals
        insights.append(
            f"整体投放共消耗 {format_currency(total.spend)}，累计收集 {format_number(total.leads, 0)} 个 Leads，CPL 为 {format_currency(total.cpl)}。CTR {format_pct(total.ctr)} 落在预热 Benchmark 区间内，但 CPM {format_currency(total.cpm)} 和 CPC {format_currency(total.cpc)} 偏高，说明当前拿量成本仍有优化空间。"
        )
        insights.append(
            f"CVR 为 {format_pct(total.cvr)}，高于 15%-20% 的行业参考带，说明点击后的承接质量不差，后续优化重点应优先放在降低前端流量成本，而不是大改转化链路。"
        )
    if gender and gender.rows:
        total = gender.totals
        primary = max(gender.rows, key=lambda row: row.leads if row.leads else row.spend)
        insights.append(
            f"性别分布高度集中在 {primary.label}，该人群贡献 {share_text(primary.spend, total.spend)} 的花费和 {share_text(primary.leads, total.leads)} 的 Leads。当前算法已明显向高转化性别倾斜，后续若继续放量，可先以该人群为主，再视需求补充次级人群测试。"
        )
    if placement and placement.rows:
        total = placement.totals
        primary = max(placement.rows, key=lambda row: row.spend)
        efficient = min([row for row in placement.rows if row.leads > 0], key=lambda row: row.cpl, default=None)
        insights.append(
            f"主力版位为 {primary.label}，承担 {share_text(primary.spend, total.spend)} 的花费并带来 {share_text(primary.leads, total.leads)} 的 Leads，当前仍应作为主要承接版位。"
        )
        if efficient and efficient.label != primary.label:
            insights.append(
                f"{efficient.label} 的 CPL 最优，为 {format_currency(efficient.cpl)}，但当前预算占比不高。该版位适合以小预算持续验证，确认样本稳定后再逐步扩量。"
            )
        instagram = next((row for row in placement.rows if row.raw_label.lower() == "instagram"), None)
        facebook = next((row for row in placement.rows if row.raw_label.lower() == "facebook"), None)
        if instagram and facebook:
            insights.append(
                f"Instagram 的 CTR 为 {format_pct(instagram.ctr)}，高于 Facebook 的 {format_pct(facebook.ctr)}，但 Instagram 的 CPL 为 {format_currency(instagram.cpl)}，高于 Facebook 的 {format_currency(facebook.cpl)}。说明 Instagram 更适合点击测试，Facebook 仍是当前更稳的线索获取主阵地。"
            )
    return insights


def render_insights(insights: list[str]) -> str:
    return "".join(f"<li>{html.escape(text)}</li>" for text in insights)


def render_missing_sections(inputs: ReportInputs, sections: list[BreakdownSection]) -> str:
    available = {section.kind for section in sections}
    missing = []
    if not inputs.meta_daily:
        missing.append("每日趋势拆解：未提供按日期日报表")
    if not inputs.meta_summary:
        missing.append("广告汇总与兴趣成效：未提供汇总表")
    if not inputs.meta_creatives:
        missing.append("素材成效分析：未提供素材级数据")
    if "gender" not in available:
        missing.append("性别分析：未提供性别 breakdown")
    if "placement" not in available:
        missing.append("版位分析：未提供 placement breakdown")
    if not inputs.questionnaire_json:
        missing.append("问卷分析：未提供结构化问卷结果")
    if inputs.crowdfunding_goal is None or inputs.average_price is None:
        missing.append("测算实值：未提供众筹目标金额和平均单价，测算板块已展示公式框架但无法输出最终金额")
    return "".join(f"<li>{html.escape(item)}</li>" for item in missing) or "<li>无</li>"


def render_data_sources(inputs: ReportInputs) -> str:
    rows = [
        ("广告汇总表", stringify_path(inputs.meta_summary)),
        ("日报表", stringify_path(inputs.meta_daily)),
        ("人口统计 breakdown", stringify_path(inputs.meta_demographics)),
        ("版位 breakdown", stringify_path(inputs.meta_placement)),
        ("素材级数据表", stringify_path(inputs.meta_creatives)),
        ("问卷结构化 JSON", stringify_path(inputs.questionnaire_json)),
    ]
    return "".join(f"<tr><td>{html.escape(label)}</td><td>{html.escape(path)}</td></tr>" for label, path in rows)


def stringify_path(path: Optional[Path]) -> str:
    return str(path) if path else "未提供"


def load_notes_html(path: Optional[Path]) -> str:
    if not path or not path.exists():
        return "<p>未提供额外备注。</p>"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"<p>备注文件读取失败：{html.escape(str(exc))}</p>"
    if isinstance(data, list):
        return "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in data) + "</ul>"
    if isinstance(data, dict):
        return "<ul>" + "".join(f"<li><strong>{html.escape(str(k))}</strong>: {html.escape(str(v))}</li>" for k, v in data.items()) + "</ul>"
    return f"<p>{html.escape(str(data))}</p>"


def chart_payload(section: BreakdownSection) -> dict[str, object]:
    total = section.totals
    return {
        "labels": [row.label for row in section.rows],
        "spend": [round(row.spend, 2) for row in section.rows],
        "leads": [round(row.leads, 2) for row in section.rows],
        "cpl": [round(row.cpl, 2) for row in section.rows],
        "spend_share": [round(safe_div(row.spend * 100.0, total.spend), 2) for row in section.rows],
        "lead_share": [round(safe_div(row.leads * 100.0, total.leads), 2) for row in section.rows],
    }


def benchmark_chart_payload(overall: Optional[BreakdownRow]) -> dict[str, object]:
    if not overall:
        return {"labels": [], "benchmarkMid": [], "actual": []}
    labels = ["CPM", "CTR", "CPC", "CPL", "CVR"]
    actual = [overall.cpm, overall.ctr, overall.cpc, overall.cpl, overall.cvr]
    benchmark_mid = [(BENCHMARKS[label]["low"] + BENCHMARKS[label]["high"]) / 2 for label in labels]
    return {"labels": labels, "benchmarkMid": benchmark_mid, "actual": [round(value, 2) for value in actual]}


def allocation_chart_payload(ctx: EstimateContext) -> dict[str, object]:
    labels = [item[0] for item in ALLOCATION_ITEMS]
    if ctx.has_inputs and ctx.marketing_total is not None:
        values = [round(ctx.marketing_total * item[1], 2) for item in ALLOCATION_ITEMS]
    else:
        values = [round(86000.0 * item[1], 2) for item in ALLOCATION_ITEMS]
    colors = ["#20487b", "#1b7f83", "#8b5cf6", "#f59e0b", "#ef4444", "#64748b"]
    return {"labels": labels, "values": values, "colors": colors}


def email_chart_payload(ctx: EstimateContext) -> dict[str, object]:
    if not ctx.has_inputs:
        return {
            "labels": ["总订单数", "前三天订单", "邮箱订单", "所需邮箱数"],
            "values": [1355, 271, 54, 2710],
            "hasInputs": False,
        }
    return {
        "labels": ["总订单数", "前三天订单", "邮箱订单", "所需邮箱数"],
        "values": [
            round(ctx.total_orders or 0, 0),
            round(ctx.first_three_day_orders or 0, 0),
            round(ctx.email_orders or 0, 0),
            round(ctx.required_emails or 0, 0),
        ],
        "hasInputs": True,
    }


def estimate_context(inputs: ReportInputs, overall: Optional[BreakdownSection]) -> EstimateContext:
    if inputs.crowdfunding_goal is None or inputs.average_price is None:
        return EstimateContext(
            has_inputs=False,
            crowdfunding_goal=inputs.crowdfunding_goal,
            average_price=inputs.average_price,
            marketing_total=None,
            total_orders=None,
            first_three_day_orders=None,
            email_orders=None,
            required_emails=None,
            warmup_spend=None,
            warmup_share=None,
            current_cpl=overall.totals.cpl if overall else None,
            message="需补充众筹目标金额和产品平均单价后，才能输出测算实值。",
        )

    goal = inputs.crowdfunding_goal
    price = inputs.average_price
    cpl = overall.totals.cpl if overall else None
    total_orders = safe_div(goal, price)
    first_three_day_orders = total_orders * 0.20
    email_orders = first_three_day_orders * 0.20
    required_emails = email_orders / 0.02
    warmup_spend = required_emails * cpl if cpl is not None else None
    warmup_share = safe_div(warmup_spend * 100.0, goal) if warmup_spend is not None else None

    return EstimateContext(
        has_inputs=True,
        crowdfunding_goal=goal,
        average_price=price,
        marketing_total=goal * 0.172,
        total_orders=total_orders,
        first_three_day_orders=first_three_day_orders,
        email_orders=email_orders,
        required_emails=required_emails,
        warmup_spend=warmup_spend,
        warmup_share=warmup_share,
        current_cpl=cpl,
        message=None,
    )


def render_glossary() -> str:
    return "".join(f"<tr><td>{term}</td><td>{html.escape(desc)}</td></tr>" for term, desc in GLOSSARY)


def render_section(section: BreakdownSection) -> str:
    total = section.totals
    payload = chart_payload(section)
    return f"""
    <section class="section">
      <div class="section-header">
        <div>
          <h2>{section.title}</h2>
          <p>共统计 {len(section.rows)} 个 {section.dimension_label} 维度，总花费 {format_currency(total.spend)}，总 Leads {format_number(total.leads, 0)}，整体 CPL {format_currency(total.cpl)}。</p>
        </div>
        <div class="chip">来源：{html.escape(section.source_path.name)}</div>
      </div>
      <div class="chart-grid">
        <div class="chart-card">
          <h3>花费与 Leads 分布</h3>
          <canvas id="{section.kind}-performance-chart"></canvas>
        </div>
        <div class="chart-card">
          <h3>CPL 对比</h3>
          <canvas id="{section.kind}-cpl-chart"></canvas>
        </div>
        <div class="chart-card">
          <h3>花费 / Leads 占比结构</h3>
          <canvas id="{section.kind}-share-chart"></canvas>
        </div>
      </div>
      <table>
        <thead>
          <tr><th>{section.dimension_label}</th><th>花费</th><th>花费占比</th><th>Leads</th><th>Lead 占比</th><th>CPL</th><th>CTR</th><th>CPC</th><th>CVR</th></tr>
        </thead>
        <tbody>{render_breakdown_table(section)}</tbody>
      </table>
      <script type="application/json" id="{section.kind}-data">{html.escape(json.dumps(payload, ensure_ascii=False))}</script>
    </section>
    """


def render_strategy_list(items: list[str]) -> str:
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def render_traffic_source_cards() -> str:
    cards = []
    for name, _, color, desc in TRAFFIC_SOURCES:
        cards.append(f'<div class="source-card"><strong style="color:{color}">{html.escape(name)}</strong><p>{html.escape(desc)}</p></div>')
    return "".join(cards)


def render_allocation_rows(ctx: EstimateContext) -> str:
    if not ctx.has_inputs or ctx.marketing_total is None or ctx.crowdfunding_goal is None:
        return (
            "<tr><td>众筹目标</td><td>待补充</td><td>待补充</td><td>—</td><td>需补充众筹目标金额后自动测算</td></tr>"
            "<tr><td>营销费用合计</td><td>待补充</td><td>待补充</td><td>17.20%</td><td>按众筹目标 * 17.2% 计算</td></tr>"
        )

    rows = [
        f"<tr><td>众筹目标</td><td>{format_currency(ctx.crowdfunding_goal)}</td><td>/</td><td>—</td><td>—</td></tr>"
    ]
    for label, ratio, desc in ALLOCATION_ITEMS:
        spend = ctx.marketing_total * ratio
        goal_share = safe_div(spend * 100.0, ctx.crowdfunding_goal)
        rows.append(
            f"<tr><td>{html.escape(label)}</td><td>—</td><td>{format_currency(spend)}</td><td>{format_pct(goal_share)}</td><td>{html.escape(desc)}</td></tr>"
        )
    rows.append(
        f"<tr><td><strong>营销费用合计</strong></td><td>—</td><td><strong>{format_currency(ctx.marketing_total)}</strong></td><td><strong>17.20%</strong></td><td>行业内营销费用主要包含投广、PR 两部分。</td></tr>"
    )
    return "".join(rows)


def roi_chart_payload(ctx: EstimateContext) -> dict[str, object]:
    if ctx.has_inputs and ctx.marketing_total is not None:
        budget_map = {
            "预热邮箱": ctx.marketing_total * 0.2558,
            "众筹期投广": ctx.marketing_total * 0.5814,
            "PR / KOL": ctx.marketing_total * 0.0581,
            "众筹社区": ctx.marketing_total * 0.0930,
        }
    else:
        budget_map = {
            "预热邮箱": 22000.0,
            "众筹期投广": 50000.0,
            "PR / KOL": 5000.0,
            "众筹社区": 8000.0,
        }
    labels, budgets, conversions, tags = [], [], [], []
    for label, ratio, _ in ROI_CHANNELS:
        budget = budget_map[label]
        labels.append(label)
        budgets.append(round(budget, 2))
        conversions.append(round(budget * ratio, 2))
        tags.append(f"{'ROAS' if label == '众筹期投广' else 'ROI'} {ratio:.2f}")
    return {"labels": labels, "budgets": budgets, "conversions": conversions, "tags": tags}


def render_email_estimate(ctx: EstimateContext) -> str:
    if not ctx.has_inputs:
        return (
            '<div class="warning-card">'
            f"<p>{html.escape(ctx.message or '缺少测算参数')}</p>"
            "<ul>"
            "<li>总订单数 = 众筹目标 ÷ 平均单价</li>"
            "<li>前三天订单 = 总订单数 × 20%</li>"
            "<li>前三天来自预热邮箱的订单 = 前三天订单 × 20%</li>"
            "<li>需要收集的邮箱数 = 前三天来自邮箱的订单 ÷ 2%</li>"
            "<li>预热花费 = 所需邮箱数 × 当前 CPL</li>"
            "</ul></div>"
        )

    return (
        "<table><thead><tr><th>测算项</th><th>结果</th><th>说明</th></tr></thead><tbody>"
        f"<tr><td>总订单数</td><td>{format_number(ctx.total_orders, 0)}</td><td>众筹目标 ÷ 平均单价</td></tr>"
        f"<tr><td>前三天订单</td><td>{format_number(ctx.first_three_day_orders, 0)}</td><td>总订单数 × 20%</td></tr>"
        f"<tr><td>前三天来自预热邮箱的订单</td><td>{format_number(ctx.email_orders, 0)}</td><td>前三天订单 × 20%</td></tr>"
        f"<tr><td>所需预热邮箱数</td><td>{format_number(ctx.required_emails, 0)}</td><td>邮箱订单 ÷ 2%</td></tr>"
        f"<tr><td>当前 CPL</td><td>{format_currency(ctx.current_cpl)}</td><td>来自当前前测数据</td></tr>"
        f"<tr><td>预热花费</td><td>{format_currency(ctx.warmup_spend)}</td><td>所需邮箱数 × 当前 CPL</td></tr>"
        f"<tr><td>预热花费占众筹目标比例</td><td>{format_pct(ctx.warmup_share)}</td><td>预热花费 ÷ 众筹目标</td></tr>"
        "</tbody></table>"
    )


def render_community_rows() -> str:
    return "".join(
        f"<tr><td>{html.escape(name)}</td><td>{html.escape(plan1)}</td><td>{html.escape(plan2)}</td><td>{html.escape(note)}</td></tr>"
        for name, plan1, plan2, note in COMMUNITY_ROWS
    )


def render_risk_items() -> str:
    blocks = []
    for idx, (title, desc) in enumerate(RISK_ITEMS, 1):
        blocks.append(f"<div class=\"risk-card\"><h3>{idx}. {html.escape(title)}</h3><p>{html.escape(desc)}</p></div>")
    return "".join(blocks)


def render_html(inputs: ReportInputs, sections: list[BreakdownSection]) -> str:
    product_name = resolve_product_name(inputs)
    date_range = resolve_date_range(inputs, sections)
    overall_section = pick_overall_section(sections)
    notes_html = load_notes_html(inputs.notes_json)
    missing_html = render_missing_sections(inputs, sections)
    sources_html = render_data_sources(inputs)
    goal_text = format_currency(inputs.crowdfunding_goal)
    price_text = format_currency(inputs.average_price)
    section_html = "".join(render_section(section) for section in sections)
    estimate = estimate_context(inputs, overall_section)

    if overall_section:
        overall = overall_section.totals
        overall_cards = render_metric_cards(overall)
        benchmark_rows = render_benchmark_rows(overall)
        insights_html = render_insights(
            build_insights(
                overall_section,
                next((section for section in sections if section.kind == "gender"), None),
                next((section for section in sections if section.kind == "placement"), None),
            )
        )
    else:
        overall_cards = '<div class="card">未读取到可分析的数据。</div>'
        benchmark_rows = "<tr><td colspan='4'>未读取到可分析的数据。</td></tr>"
        insights_html = "<li>当前没有足够数据生成洞察。</li>"

    traffic_payload = {
        "labels": [item[0] for item in TRAFFIC_SOURCES],
        "values": [item[1] for item in TRAFFIC_SOURCES],
        "colors": [item[2] for item in TRAFFIC_SOURCES],
    }
    roi_payload = roi_chart_payload(estimate)
    benchmark_payload = benchmark_chart_payload(overall if overall_section else None)
    allocation_payload = allocation_chart_payload(estimate)
    email_payload = email_chart_payload(estimate)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(product_name)} 预热投广前测报告</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #eef3f8;
      --ink: #1f2937;
      --muted: #5b6472;
      --panel: #ffffff;
      --line: #d8e1ec;
      --navy: #20487b;
      --teal: #1b7f83;
      --sand: #fff7ed;
      --gold: #f59e0b;
      --good: #15803d;
      --okay: #2563eb;
      --bad: #dc2626;
      --dark: #1a1a2e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at top right, rgba(32,72,123,0.08), transparent 24%), linear-gradient(180deg, #f6f9fc 0%, #eef3f8 100%);
    }}
    .page {{
      width: min(1120px, calc(100vw - 32px));
      margin: 24px auto 40px;
      background: rgba(255,255,255,0.95);
      border: 1px solid rgba(216,225,236,0.9);
      border-radius: 28px;
      padding: 36px;
      box-shadow: 0 18px 60px rgba(31, 41, 55, 0.08);
    }}
    .hero {{
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 20px;
      margin-bottom: 28px;
    }}
    .hero-main {{
      padding: 28px;
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(32,72,123,0.98), rgba(27,127,131,0.92));
      color: #fff;
    }}
    .hero-main h1 {{ margin: 0 0 10px; font-size: 32px; line-height: 1.2; }}
    .hero-main p {{ margin: 0; color: rgba(255,255,255,0.84); line-height: 1.7; }}
    .hero-side {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}
    .card, .chart-card, .source-card, .risk-card, .warning-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .metric-card {{
      background: linear-gradient(180deg, #ffffff 0%, #f6fbff 100%);
      min-height: 110px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .metric-card strong {{ color: var(--muted); font-size: 14px; }}
    .metric-card span {{ font-size: 28px; font-weight: 700; color: var(--navy); }}
    .section {{ margin-top: 28px; }}
    .section h2 {{ margin: 0 0 12px; color: var(--navy); }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }}
    .section-header p, .source-card p, .risk-card p, .warning-card p, .section p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
    }}
    .chip {{
      white-space: nowrap;
      border-radius: 999px;
      padding: 8px 12px;
      background: #eff6ff;
      color: var(--navy);
      border: 1px solid #dbeafe;
      font-size: 13px;
    }}
    .chart-grid, .two-col, .benchmark-wrap, .estimate-wrap {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 16px;
    }}
    .triple-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 16px;
    }}
    .chart-card {{
      min-height: 320px;
      background: linear-gradient(180deg, #fdfefe 0%, #f7fbff 100%);
    }}
    .dark-card {{
      background: var(--dark);
      color: #fff;
      border-radius: 22px;
      padding: 20px;
    }}
    .dark-card h3 {{ margin: 0 0 12px; }}
    .dark-card p {{ color: rgba(255,255,255,0.8); }}
    .source-grid, .risk-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      background: #fff;
      overflow: hidden;
      border-radius: 18px;
    }}
    th, td {{
      padding: 12px 14px;
      border-bottom: 1px solid #e5edf5;
      text-align: left;
      font-size: 14px;
      vertical-align: top;
    }}
    th {{
      background: #f5f9fd;
      color: var(--navy);
      font-weight: 700;
    }}
    tr:last-child td {{ border-bottom: none; }}
    .insight-box, .missing {{
      background: linear-gradient(180deg, #fffdf8 0%, #fff8ed 100%);
      border: 1px solid #f4d8ac;
      border-radius: 20px;
      padding: 20px;
    }}
    .insight-box ul, .missing ul, .strategy-list, .warning-card ul {{
      margin: 0;
      padding-left: 20px;
      line-height: 1.8;
    }}
    .good {{ color: var(--good); font-weight: 700; }}
    .okay {{ color: var(--okay); font-weight: 700; }}
    .bad {{ color: var(--bad); font-weight: 700; }}
    .neutral {{ color: var(--muted); font-weight: 700; }}
    .warning-card {{ background: var(--sand); border-color: #f4d8ac; }}
    .closing {{
      background: linear-gradient(135deg, #eff6ff, #f8fafc);
      border: 1px solid #dbeafe;
      border-radius: 20px;
      padding: 20px;
      line-height: 1.8;
      color: var(--muted);
    }}
    @media (max-width: 920px) {{
      .page {{ padding: 20px; }}
      .hero, .metric-grid, .chart-grid, .two-col, .benchmark-wrap, .estimate-wrap, .source-grid, .risk-grid, .triple-grid {{ grid-template-columns: 1fr; }}
      .hero-side {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 560px) {{
      .hero-side {{ grid-template-columns: 1fr; }}
      .metric-grid {{ grid-template-columns: 1fr 1fr; }}
      .metric-card span {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-main">
        <h1>{html.escape(product_name)} 预热投广前测报告</h1>
        <p>本版报告已接入基础测算、后续推进方案与风险评估结构。当前你给到的数据主要覆盖性别和版位两个维度，因此分析部分聚焦受众与流量承接判断，未提供的原始数据会在报告内明确标注。</p>
      </div>
      <div class="hero-side">
        <div class="card"><strong>前测日期</strong><br>{html.escape(date_range)}</div>
        <div class="card"><strong>众筹目标金额</strong><br>{goal_text}</div>
        <div class="card"><strong>产品平均单价</strong><br>{price_text}</div>
        <div class="card"><strong>当前状态</strong><br>已生成含测算框架的前测报告</div>
      </div>
    </section>

    <section class="section">
      <h2>一、核心数据概览</h2>
      <div class="metric-grid">{overall_cards}</div>
      <div class="two-col">
        <div class="card">
          <h3>关键数据 VS Benchmark</h3>
          <table>
            <thead><tr><th>指标</th><th>Benchmark</th><th>当前数据</th><th>判断</th></tr></thead>
            <tbody>{benchmark_rows}</tbody>
          </table>
        </div>
        <div class="card">
          <h3>名词解释</h3>
          <table>
            <thead><tr><th>名词</th><th>解释</th></tr></thead>
            <tbody>{render_glossary()}</tbody>
          </table>
        </div>
      </div>
      <div class="chart-grid">
        <div class="chart-card">
          <h3>Benchmark 对比图</h3>
          <canvas id="benchmark-chart"></canvas>
        </div>
        <div class="chart-card">
          <h3>当前指标表现图</h3>
          <canvas id="metric-mix-chart"></canvas>
        </div>
      </div>
    </section>

    {section_html}

    <section class="section">
      <h2>四、前测期投广洞察</h2>
      <div class="insight-box">
        <ul>{insights_html}</ul>
      </div>
    </section>

    <section class="section">
      <h2>五、后续继续推进众筹方案</h2>
      <p>当前板块按 skill 固定模板生成。若已提供众筹目标金额与客单价，则测算部分会使用实算值；若未提供，则先展示公式框架与预算结构。</p>

      <div class="card">
        <h3>后续策略</h3>
        <ul class="strategy-list">{render_strategy_list(FOLLOW_UP_STRATEGIES)}</ul>
      </div>

      <div class="estimate-wrap">
        <div class="dark-card">
          <h3>KS 各流量订单来源预估</h3>
          <div class="chart-card" style="background:transparent;border:none;padding:0;min-height:300px">
            <canvas id="traffic-source-chart"></canvas>
          </div>
        </div>
        <div>
          <h3>各来源说明</h3>
          <div class="source-grid">{render_traffic_source_cards()}</div>
        </div>
      </div>

      <div class="section">
        <h3>各付费渠道后续花费预估</h3>
        <div class="chart-card" style="margin-top:12px">
          <h3>预算分配图</h3>
          <canvas id="allocation-chart"></canvas>
        </div>
        <table>
          <thead><tr><th>项目</th><th>众筹目标</th><th>费用 $(美金)</th><th>占比</th><th>说明</th></tr></thead>
          <tbody>{render_allocation_rows(estimate)}</tbody>
        </table>
      </div>

      <div class="estimate-wrap">
        <div class="dark-card">
          <h3>各付费转化渠道投产比预估</h3>
          <div class="chart-card" style="background:transparent;border:none;padding:0;min-height:320px">
            <canvas id="roi-chart"></canvas>
          </div>
        </div>
        <div>
          <h3>预热邮箱数量计算</h3>
          <div class="chart-card" style="margin-top:12px;margin-bottom:12px">
            <h3>邮箱测算图</h3>
            <canvas id="email-chart"></canvas>
          </div>
          {render_email_estimate(estimate)}
        </div>
      </div>

      <div class="two-col">
        <div class="card">
          <h3>KOL 合作策划</h3>
          <p>当前先按通用科技 / 消费电子类项目逻辑展示。若你后续补充产品品类，我可以把垂直方向文案改成更贴近产品的版本。</p>
          <ol class="strategy-list">{''.join(f'<li>{html.escape(step)}</li>' for step in KOL_STEPS)}</ol>
        </div>
        <div class="card">
          <h3>众筹社区策划</h3>
          <table>
            <thead><tr><th>众筹社群</th><th>套餐 1</th><th>套餐 2</th><th>备注</th></tr></thead>
            <tbody>{render_community_rows()}</tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>六、风险评估</h2>
      <div class="risk-grid">{render_risk_items()}</div>
    </section>

    <section class="section">
      <h2>七、数据缺失说明</h2>
      <div class="missing"><ul>{missing_html}</ul></div>
    </section>

    <section class="section">
      <h2>八、输入文件记录</h2>
      <table>
        <thead><tr><th>输入项</th><th>路径</th></tr></thead>
        <tbody>{sources_html}</tbody>
      </table>
    </section>

    <section class="section">
      <h2>九、备注</h2>
      <div class="card">{notes_html}</div>
    </section>

    <section class="section">
      <h2>十、结尾</h2>
      <div class="closing">{html.escape(CLOSING_TEXT)}</div>
    </section>
  </div>

  <script type="application/json" id="traffic-source-data">{html.escape(json.dumps(traffic_payload, ensure_ascii=False))}</script>
  <script type="application/json" id="roi-data">{html.escape(json.dumps(roi_payload, ensure_ascii=False))}</script>
  <script type="application/json" id="benchmark-data">{html.escape(json.dumps(benchmark_payload, ensure_ascii=False))}</script>
  <script type="application/json" id="allocation-data">{html.escape(json.dumps(allocation_payload, ensure_ascii=False))}</script>
  <script type="application/json" id="email-data">{html.escape(json.dumps(email_payload, ensure_ascii=False))}</script>
  <script>
    function buildBreakdownCharts(prefix) {{
      const raw = document.getElementById(`${{prefix}}-data`);
      if (!raw) return;
      const data = JSON.parse(raw.textContent);
      const palette = ["#20487b", "#1b7f83", "#8b5cf6", "#f59e0b", "#ef4444", "#64748b"];

      new Chart(document.getElementById(`${{prefix}}-performance-chart`), {{
        type: 'bar',
        data: {{
          labels: data.labels,
          datasets: [
            {{ label: '花费 (USD)', data: data.spend, backgroundColor: palette[0], borderRadius: 8, yAxisID: 'y' }},
            {{ label: 'Leads', data: data.leads, type: 'line', borderColor: palette[1], backgroundColor: palette[1], tension: 0.25, yAxisID: 'y1' }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }},
          scales: {{
            y: {{ beginAtZero: true, title: {{ display: true, text: '花费 (USD)' }} }},
            y1: {{ beginAtZero: true, position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Leads' }} }}
          }}
        }}
      }});

      new Chart(document.getElementById(`${{prefix}}-cpl-chart`), {{
        type: 'bar',
        data: {{
          labels: data.labels,
          datasets: [{{ label: 'CPL (USD)', data: data.cpl, backgroundColor: palette.slice(1, 1 + data.labels.length), borderRadius: 8 }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'USD' }} }} }}
        }}
      }});

      new Chart(document.getElementById(`${{prefix}}-share-chart`), {{
        type: 'doughnut',
        data: {{
          labels: data.labels,
          datasets: [
            {{ label: '花费占比', data: data.spend_share, backgroundColor: palette.slice(0, data.labels.length), borderWidth: 0 }},
            {{ label: 'Lead 占比', data: data.lead_share, backgroundColor: palette.slice(0, data.labels.length).map(c => c + 'AA'), borderWidth: 0 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }}
        }}
      }});
    }}

    function buildBenchmarkCharts() {{
      const raw = document.getElementById('benchmark-data');
      const data = JSON.parse(raw.textContent);
      if (!data.labels.length) return;

      new Chart(document.getElementById('benchmark-chart'), {{
        type: 'radar',
        data: {{
          labels: data.labels,
          datasets: [
            {{
              label: 'Benchmark 中位值',
              data: data.benchmarkMid,
              borderColor: '#94a3b8',
              backgroundColor: 'rgba(148,163,184,0.18)',
              pointBackgroundColor: '#94a3b8'
            }},
            {{
              label: '当前数据',
              data: data.actual,
              borderColor: '#20487b',
              backgroundColor: 'rgba(32,72,123,0.18)',
              pointBackgroundColor: '#20487b'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }}
        }}
      }});

      new Chart(document.getElementById('metric-mix-chart'), {{
        type: 'bar',
        data: {{
          labels: data.labels,
          datasets: [
            {{ label: 'Benchmark 中位值', data: data.benchmarkMid, backgroundColor: '#cbd5e1', borderRadius: 8 }},
            {{ label: '当前数据', data: data.actual, backgroundColor: '#1b7f83', borderRadius: 8 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }},
          scales: {{ y: {{ beginAtZero: true }} }}
        }}
      }});
    }}

    function buildTrafficSourceChart() {{
      const raw = document.getElementById('traffic-source-data');
      const data = JSON.parse(raw.textContent);
      new Chart(document.getElementById('traffic-source-chart'), {{
        type: 'pie',
        data: {{
          labels: data.labels,
          datasets: [{{ data: data.values, backgroundColor: data.colors, borderColor: '#1a1a2e', borderWidth: 2 }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#ffffff' }} }}
          }}
        }}
      }});
    }}

    function buildRoiChart() {{
      const raw = document.getElementById('roi-data');
      const data = JSON.parse(raw.textContent);
      new Chart(document.getElementById('roi-chart'), {{
        type: 'bar',
        data: {{
          labels: data.labels,
          datasets: [
            {{ label: '花费预算', data: data.budgets, backgroundColor: '#3B82F6', borderRadius: 8 }},
            {{ label: '转化金额', data: data.conversions, backgroundColor: '#F59E0B', borderRadius: 8 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#ffffff' }} }},
            tooltip: {{
              callbacks: {{
                afterBody: function(items) {{
                  const index = items[0].dataIndex;
                  return data.tags[index];
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#ffffff' }}, grid: {{ color: 'rgba(255,255,255,0.08)' }} }},
            y: {{ ticks: {{ color: '#ffffff' }}, grid: {{ color: 'rgba(255,255,255,0.08)' }} }}
          }}
        }}
      }});
    }}

    function buildAllocationChart() {{
      const raw = document.getElementById('allocation-data');
      const data = JSON.parse(raw.textContent);
      new Chart(document.getElementById('allocation-chart'), {{
        type: 'doughnut',
        data: {{
          labels: data.labels,
          datasets: [{{ data: data.values, backgroundColor: data.colors, borderWidth: 0 }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }}
        }}
      }});
    }}

    function buildEmailChart() {{
      const raw = document.getElementById('email-data');
      const data = JSON.parse(raw.textContent);
      new Chart(document.getElementById('email-chart'), {{
        type: 'line',
        data: {{
          labels: data.labels,
          datasets: [{{
            label: data.hasInputs ? '测算结果' : '示意结构',
            data: data.values,
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245,158,11,0.18)',
            tension: 0.25,
            fill: true,
            pointBackgroundColor: '#f59e0b'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom' }} }},
          scales: {{ y: {{ beginAtZero: true }} }}
        }}
      }});
    }}

    buildBreakdownCharts('gender');
    buildBreakdownCharts('placement');
    buildBenchmarkCharts();
    buildTrafficSourceChart();
    buildRoiChart();
    buildAllocationChart();
    buildEmailChart();
  </script>
</body>
</html>
"""


def export_pdf(html_path: Path, pdf_path: Path) -> Optional[str]:
    if module_available("playwright"):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.pdf(path=str(pdf_path), format="A4", print_background=True, margin={"top": "12mm", "right": "10mm", "bottom": "12mm", "left": "10mm"})
            browser.close()
        return "playwright"
    if module_available("weasyprint"):
        from weasyprint import HTML

        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return "weasyprint"
    if module_available("pdfkit") and shutil.which("wkhtmltopdf"):
        import pdfkit

        pdfkit.from_file(str(html_path), str(pdf_path))
        return "pdfkit+wkhtmltopdf"
    return None


def main() -> int:
    args = parse_args()
    inputs = build_inputs(args)
    ensure_output_dir(inputs.output_dir)

    sections = [section for section in [load_breakdown(inputs.meta_demographics, "gender"), load_breakdown(inputs.meta_placement, "placement")] if section]
    product_name = resolve_product_name(inputs)
    base = sanitize_filename(product_name)
    html_path = inputs.output_dir / f"{base}_pretest_report.html"
    pdf_path = inputs.output_dir / f"{base}_pretest_report.pdf"

    html_path.write_text(render_html(inputs, sections), encoding="utf-8")
    pdf_backend = export_pdf(html_path, pdf_path)

    print(f"HTML: {html_path}")
    if pdf_backend:
        print(f"PDF backend available: {pdf_backend}")
        print(f"PDF target path: {pdf_path}")
        print("Note: PDF rendered successfully.")
    else:
        print("PDF backend available: none")
        print("Note: HTML created successfully. Install playwright, weasyprint, or pdfkit+wkhtmltopdf for PDF export.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
