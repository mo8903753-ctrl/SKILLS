---
name: youtube-kol-finder
description: Find, screen, score, and format YouTube KOL candidates for Western tech crowdfunding campaigns. Use when the user asks to find YouTube influencers/KOLs/creators for Kickstarter, Indiegogo, Makuake, Zeczec, crowdfunding prelaunch, paid reviews, product seeding, Shorts/Reels support, or long-form review outreach, especially for consumer electronics, AI hardware, camera gear, outdoor tech, EDC, 3D printing, smart home, robotics, keyboards, audio, or health tech projects.
---

# YouTube KOL Finder

## Core Workflow

1. Clarify only missing campaign constraints before sourcing:
   - Product category, product price, launch platform, launch timing, target markets, language, campaign stage, target KOL count, budget range, sample availability, and preferred collaboration types.
   - Use the MadSpace defaults below when the user does not specify preferences.

2. Apply MadSpace defaults:
   - Categories: consumer electronics, AI hardware, camera gear, outdoor tech, EDC, 3D printing, smart home, robotics, keyboards/peripherals, audio, health tech, and adjacent tech products.
   - Markets: United States and Canada first; then United Kingdom, Germany, France, Nordics, Australia, and broader Western English-speaking markets.
   - Channel scale: mix of small, mid, and large channels, ranked by cost efficiency rather than follower count alone.
   - Collaboration types: paid review, product seeding review, Shorts/Reels support, long-form deep review, and custom campaign-specific formats.
   - Priority signals: recent average views, comment quality, crowdfunding experience, likely conversion value, affordable quote, audience fit, reachable email/contact, and willingness to coordinate before launch.
   - Exclusions: phone-news-only channels, creators who do not accept crowdfunding, inflated pricing, declining views, suspicious audience quality, Shorts-only channels, overly broad content, and non-English channels unless explicitly requested.

3. Read supporting references as needed:
   - Use `references/historical-sheet-patterns.md` when matching the user's Google Sheet structure or deciding which columns to include.
   - Use `references/scoring-rubric.md` when ranking candidates into Yes/Backup/No.
   - Use `references/research-workflow.md` when sourcing new YouTube channels from web research.

4. Source candidates with current data:
   - Browse/search the web because YouTube channel data, recent views, contact availability, and pricing signals change frequently.
   - Prefer direct YouTube channel/video pages, creator websites/media kits, campaign pages, and credible public references.
   - Do not invent emails, fees, average views, countries, or prior crowdfunding experience. Mark unknown fields as blank or `Need verify`.

5. Qualify each candidate:
   - Reject hard exclusions early.
   - Estimate recent average views from recent relevant long-form videos, not total channel views.
   - Separate Shorts performance from long-form review performance.
   - Check whether comments show real product interest, buying intent, technical questions, or crowdfunding-related discussion.
   - Prefer creators who have reviewed comparable products or have an audience that buys early-adopter hardware.

6. Score and label candidates:
   - Use the scoring rubric to assign `MadSpace Advice` as `Yes`, `Backup`, or `No`.
   - Put the reasoning in `MS Notes`, not in hidden assumptions.
   - Include cost-efficiency reasoning when fee and average views are available.

7. Output in the user's Google Sheet style by default:
   - For discovery/research, use the research schema from `references/historical-sheet-patterns.md`.
   - For active outreach or fulfillment, use the execution schema only when the user asks for shipping, sample status, payment, or final review tracking.
   - If a CSV header template is useful, run `scripts/build_sheet_template.py`.

## Output Rules

- Keep the table sortable and operational, not essay-like.
- Include source URLs for channel pages and example videos.
- Use `Yes`, `Backup`, and `No` consistently for recommendation columns.
- Preserve the user's bilingual column style where practical.
- Do not save or repeat historical private data such as shipping addresses, tracking numbers, payment proof, personal emails, or private notes unless the user explicitly provides them for the current task.
- When evidence is thin, rank conservatively and explain what needs verification.

## Typical User Requests

- "帮我给这个 Kickstarter AI 硬件找 50 个欧美 YouTube KOL。"
- "为这个户外科技产品找美国和加拿大优先的测评频道，按性价比排序。"
- "按照我之前 KOL 表的格式输出一份候选 Google Sheet 字段。"
- "筛掉只做手机新闻、播放下滑、报价太高、不接众筹的频道。"
- "帮我判断这批 YouTube KOL 哪些值得邀约。"
