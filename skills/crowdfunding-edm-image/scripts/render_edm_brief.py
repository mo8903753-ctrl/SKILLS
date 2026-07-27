#!/usr/bin/env python3
"""Render fixed crowdfunding EDM image briefs from JSON variables.

Built-in templates are fallback only. A JSON file may provide exact template
copy through top-level `templates`, keyed by stage key, and those fields are
used verbatim with variable replacement.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEMPLATES = {
    "deposit": {
        "stage": "Deposit Invitation",
        "goal": "get pre-launch users to place a refundable deposit",
        "subject": "Deposit x Saving Event is Here - Grab {{product_name}} Best Offer",
        "preview": "Place {{deposit_amount}} deposit and secure {{deposit_benefit}} before the official launch.",
        "headline": "Deposit x Saving Event is Here",
        "cta": "Place {{deposit_amount}} Refundable Deposit",
        "url": "{{deposit_url}}",
        "body": "Dear {{audience_name}}, thanks for signing up for the {{product_name}} campaign! The team is excited to announce a limited-time VIP deposit offer for {{product_name}}. For a short period, you can secure your spot before the official launch with a {{deposit_amount}} refundable deposit and unlock {{deposit_benefit}}. {{product_positioning}} See you at the official launch!",
    },
    "follow": {
        "stage": "Kickstarter Follow + Deposit",
        "goal": "drive pre-launch follows and optional deposit conversion",
        "subject": "Pre-Launch Event is Here - Follow {{product_name}} on {{platform}}",
        "preview": "Follow the pre-launch page and place {{deposit_amount}} deposit to lock the best campaign offer.",
        "headline": "Follow {{product_name}} on {{platform}}",
        "cta": "Follow on {{platform}}",
        "url": "{{campaign_url}}",
        "body": "Be among the first to experience {{product_positioning}} Follow our page and secure your early supporter benefit.",
    },
    "two-days": {
        "stage": "2 Days Countdown",
        "goal": "remind users before launch",
        "subject": "Live in 2 Days - Grab {{product_name}} Campaign Best Offer",
        "preview": "{{product_name}} launches in 2 days on {{platform}}. Mark your calendar and secure the best offer.",
        "headline": "Live in 2 Days",
        "cta": "Mark Your Calendar",
        "url": "{{campaign_url}}",
        "body": "{{product_name}} launches on {{platform}} on {{launch_date}}. The best early bird offer will be limited.",
    },
    "one-day": {
        "stage": "24 Hours Countdown",
        "goal": "final pre-launch reminder",
        "subject": "24 Hours Countdown - Grab Best Deal Now",
        "preview": "Only 24 hours until {{product_name}} launches on {{platform}}.",
        "headline": "24 Hours Countdown",
        "cta": "Get Ready Now",
        "url": "{{campaign_url}}",
        "body": "{{product_name}} goes live tomorrow. If you plan to back, it is worth being early because the launch offer moves fast.",
    },
    "launch": {
        "stage": "Launch Day",
        "goal": "convert users once campaign is live",
        "subject": "Just Launched - Grab Your {{product_name}} Now",
        "preview": "{{product_name}} is live now on {{platform}} with {{discount}} launch pricing.",
        "headline": "Just Launched",
        "cta": "Grab Launch Day Offer",
        "url": "{{campaign_url}}",
        "body": "{{product_name}} is now live. Get it at {{price}}, {{discount}}, MSRP {{msrp}}. {{limited_quantity}}.",
    },
    "deposit-backer": {
        "stage": "Deposit Backer Version",
        "goal": "convert deposit users and remind them to claim exclusive benefits",
        "subject": "Your VIP Offer is Live - Claim {{deposit_benefit}}",
        "preview": "Your deposit benefit is ready. Back {{product_name}} now and claim your VIP saving.",
        "headline": "Your VIP Offer is Live",
        "cta": "Claim VIP Offer",
        "url": "{{campaign_url}}",
        "body": "Thank you for placing your {{deposit_amount}} deposit. Your exclusive benefit, {{deposit_benefit}}, is ready to claim.",
    },
    "kol": {
        "stage": "KOL Review",
        "goal": "use creator review as social proof",
        "subject": "Latest Review - See Why Creators Love {{product_name}}",
        "preview": "A new hands-on review shows what {{product_name}} can do in real life.",
        "headline": "Latest Review",
        "cta": "Watch the Review",
        "url": "{{kol_review_url}}",
        "body": "We are excited to share a new creator review of {{product_name}}. See the real experience before choosing your reward.",
    },
    "press": {
        "stage": "Media Report",
        "goal": "use press coverage as credibility",
        "subject": "{{product_name}} Featured by {{press_name}}",
        "preview": "See why {{product_name}} is getting attention from the press.",
        "headline": "Featured by {{press_name}}",
        "cta": "Read the Story",
        "url": "{{press_url}}",
        "body": "{{product_name}} is gaining attention for its design, features, and campaign value. Discover why people are talking about it.",
    },
    "last-48": {
        "stage": "Last 48 Hours",
        "goal": "final conversion push",
        "subject": "Last 48 Hours - Grab Your {{product_name}} Now",
        "preview": "The campaign ends in 48 hours. Get {{product_name}} at {{price}} before it closes.",
        "headline": "Last 48 Hours",
        "cta": "Back Before It Ends",
        "url": "{{campaign_url}}",
        "body": "The {{product_name}} campaign is ending soon. This is your chance to get it at {{price}}, {{discount}}.",
    },
    "last-24": {
        "stage": "Last 24 Hours",
        "goal": "last call before campaign closes",
        "subject": "Last 24 Hours - Final Chance to Get {{product_name}}",
        "preview": "The final 24 hours are here. Back {{product_name}} before the campaign closes.",
        "headline": "Last 24 Hours",
        "cta": "Back Now",
        "url": "{{campaign_url}}",
        "body": "This is the final chance to back {{product_name}} at the campaign offer. Do not miss {{price}}, {{discount}} before it ends.",
    },
    "survey": {
        "stage": "Shipping Address Survey",
        "goal": "collect fulfillment details",
        "subject": "Action Needed - Confirm Your Shipping Details",
        "preview": "Please provide your shipping details so we can process your {{product_name}} reward.",
        "headline": "Confirm Your Shipping Details",
        "cta": "Confirm Shipping Details",
        "url": "{{shipping_survey_url}}",
        "body": "Thank you for supporting {{product_name}}. Please complete your shipping details so we can process your reward smoothly.",
    },
}


def fill(text: str, values: dict[str, object]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, f"{{{{{key}}}}}")
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return str(value)

    return re.sub(r"\{\{([a-zA-Z0-9_]+)\}\}", repl, text)


def image_prompt(template: dict[str, str], values: dict[str, object]) -> str:
    product = values.get("product_name", "{{product_name}}")
    category = values.get("product_category", values.get("category", "crowdfunding"))
    return (
        f"Use the provided product image as the strict visual source of truth. Create a premium "
        f"crowdfunding EDM visual for {product}, a {category} product.\n\n"
        f"Stage: {template['stage']}.\n"
        f"Purpose: {template['goal']}.\n\n"
        "Critical product lock: preserve the product's exact appearance from the reference image. "
        "Do not change the product's face, body, silhouette, proportions, materials, colors, "
        "accessories, surface details, or perceived identity. Do not generate a similar replacement "
        "product. You may improve only the EDM presentation around it: background, lighting mood, "
        "depth, negative space, supporting graphic shapes, and campaign layout. Leave clear space for "
        "text overlay. Do not include fake logos, watermarks, UI screenshots, distorted hands, or "
        "invented product parts."
    )


def render_stage(key: str, values: dict[str, object]) -> str:
    external_templates = values.get("templates", {})
    external = {}
    if isinstance(external_templates, dict):
        candidate = external_templates.get(key, {})
        if isinstance(candidate, dict):
            external = candidate
    template = {**TEMPLATES[key], **external}
    subject = fill(template["subject"], values)
    preview = fill(template["preview"], values)
    body = fill(template["body"], values)
    cta = fill(template["cta"], values)
    url = fill(template["url"], values)
    alt = f"{fill(template['headline'], values)} for {values.get('product_name', '{{product_name}}')}. {body} CTA: {cta}."
    plain = "\n".join(
        [
            subject,
            "",
            body,
            "",
            f"{cta}: {url}",
            "",
            f"{values.get('brand_name', '{{brand_name}}')} Team",
        ]
    )
    html = (
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0">\n'
        '  <tr><td align="center">\n'
        f'    <a href="{url}" target="_blank"><img src="UPLOAD_IMAGE_URL_HERE" width="640" '
        f'alt="{alt}" style="display:block;width:100%;max-width:640px;height:auto;border:0;" /></a>\n'
        "  </td></tr>\n"
        "</table>"
    )
    return f"""## {template['stage']}

Subject:
{subject}

Preview Text:
{preview}

Image2 Prompt:
{image_prompt(template, values)}

CTA:
{cta} -> {url}

Alt Text:
{alt}

Plain Text Fallback:
{plain}

HTML Wrapper:
{html}

Copy Fidelity:
{"External user template override used. Copy was variable-replaced only." if external else "Fallback built-in template used because no external template override was provided."}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Path to a JSON file containing project variables.")
    parser.add_argument(
        "--stages",
        default="deposit,follow,two-days,one-day,launch,deposit-backer,kol,press,last-48,last-24,survey",
        help="Comma-separated stage keys.",
    )
    args = parser.parse_args()
    values = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    selected = [stage.strip() for stage in args.stages.split(",") if stage.strip()]
    missing = [stage for stage in selected if stage not in TEMPLATES]
    if missing:
        raise SystemExit(f"Unknown stages: {', '.join(missing)}")
    print("\n\n".join(render_stage(stage, values) for stage in selected))


if __name__ == "__main__":
    main()
