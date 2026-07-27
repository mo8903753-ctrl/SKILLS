#!/usr/bin/env python3
"""Print a Google Sheet-compatible CSV header for KOL research."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


RESEARCH_HEADERS = [
    "KOL NAME / KOL名称",
    "View Counts / 总观看量",
    "Followers/Subscribers / 粉丝数 / 订阅数",
    "Location / 地区",
    "Example link / 示例链接",
    "Fee / 报价 / 费用",
    "Average Views / 近期平均播放",
    "CPM",
    "video content style / 视频内容风格",
    "Crowdfunding experience / 众筹经验",
    "Client advice （Yes/No/Backup） / 品牌方建议",
    "Client Notes / 品牌方备注",
    "MadSpace Advice / MadSpace建议",
    "MS Notes / MS备注",
    "Madspace Contact PR / MadSpace PR开发人员",
    "Note For PR / PR备注",
    "Contact / 联系方式",
    "Source checked date / 信息核查日期",
]


EXECUTION_HEADERS = RESEARCH_HEADERS + [
    "Shipping Address / 收货地址",
    "Product status (Tracking Number) / 产品状态（物流单号）",
    "Additional Info / 补充信息",
    "Product Received (Y/N) / 是否已收货（是 / 否）",
    "Final review link / 最终评测链接",
    "Payment proof / 付款凭证",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate CSV headers matching the MadSpace YouTube KOL sheet structure."
    )
    parser.add_argument(
        "--mode",
        choices=("research", "execution"),
        default="research",
        help="research omits sensitive fulfillment/payment columns; execution includes them.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional CSV file path. Defaults to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    headers = EXECUTION_HEADERS if args.mode == "execution" else RESEARCH_HEADERS

    if args.output:
        with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
