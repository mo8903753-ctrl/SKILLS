---
name: crowdfunding-lead-generation
description: Automated and manual client acquisition for KS/IGG crowdfunding agencies — finding Chinese hardware brands, lead qualification, and automated scanning via cron jobs.
version: 1.0.0
author: MadSpace
platforms: [macos]
metadata:
  hermes:
    tags: [crowdfunding, kickstarter, lead-generation, client-acquisition, automation]
---

# Crowdfunding Lead Generation

Use this skill when the user (a KS/IGG crowdfunding agency operator) asks about finding Chinese hardware brand clients, setting up lead scanning automation, or improving their client acquisition workflow.

## Core principle

The user runs MadSpace, a crowdfunding agency helping Chinese hardware brands launch on KS/IGG. Client acquisition is the core business problem. The approach is hybrid: automated data collection (cron jobs) + manual human judgment (KS page review, contact finding, outreach).

## Workflow preference

**Plan first, then build.** When the user asks for a system/workflow, write a concise plan document confirming the architecture and data sources BEFORE writing code or setting up cron jobs. The user will approve the plan, then you build. Do not jump straight to implementation.

**Direct execution, minimal explanation.** The user wants working artifacts, not step-by-step instructions. Build it, test it, show the result.

## Automated scanning (cron job)

### Data sources (tested, working)

| Source | Method | What it yields |
|---|---|---|
| Kicktraq hotlist | Scrape `/hotlist/` page, filter by tech categories | KS project name, slug, category, funding %, goal, time left |
| 36kr RSS | Parse `https://36kr.com/feed`, filter by funding+hardware keywords | Funding news, company names, founders |
| HN Algolia API | Search `kickstarter` + `Show HN`, last 30 days | KS project links, discussion signals |

### Sources that DO NOT work (don't try again)

- **KS/IGG direct scraping** — Cloudflare protected. Cannot bypass.
- **Indiegogo Explore** — Cloudflare protected.
- **Reddit API** — Returns empty responses from this environment.
- **IT Juzi (IT桔子)** — Returns HTTP 412.

### Script location

The lead scanner script lives at `~/Desktop/lead_scanner.py`. It:
1. Scrapes Kicktraq hotlist, filters for tech categories (Gadgets, Hardware, Wearables, DIY Electronics, 3D Printing, Camera Equipment, Sound, Product Design)
2. Parses 36kr RSS, two-tier filtering: title must contain funding keyword, combined text must contain hardware keyword
3. Searches HN Algolia for KS project discussions
4. Outputs a structured markdown report to `~/Desktop/本周线索_YYYY-MM-DD.md`
5. Tracks pending leads in `~/.madspace_leads_history.json` for next-week reminders

### China signal detection (heuristic)

The script flags potential Chinese teams by:
- Asian currency in goal amount (HK$, ¥)
- Chinese city names in page HTML (Shenzhen, Guangzhou, Hangzhou, Shanghai, Beijing, Dongguan)
- Known Chinese brand names in project title/slug

These are HEURISTICS only. The user must manually verify by visiting the KS page.

### Cron job setup

Use `cronjob action='create'` with:
- Schedule: `0 9 * * 1` (Monday 9:00 AM)
- Prompt instructs the agent to run `python3 ~/Desktop/lead_scanner.py` and summarize results
- Name format: `madspace-lead-scanner`

### SSL handling on macOS

Python's `urllib` may fail with SSL certificate errors. Use `certifi`:
```python
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
# Pass context=ssl_context to urlopen()
```

## Manual scouting (the user's methodology)

The user has a detailed three-channel manual scouting process. See [`references/manual-scouting-methods.md`](references/manual-scouting-methods.md) for the full methodology with exact steps per channel, outreach angles, and weekly rhythm.

Summary:
- **Channel 1: KS/IGG "naked" Chinese projects** (highest ROI) — Browse KS Discover by category/Newest, Coming Soon/Prelaunch pages, Kicktraq daily curves. Identify Chinese teams by location/Chinglish copy/category/comments. Judge "bad = good opportunity" by stuck progress, no Projects We Love, poor page quality, weak first 48h.
- **Channel 2: Recently funded hardware companies** — IT Juzi filter by smart hardware/consumer electronics/IoT, 36kr funding news. Angel to Series A, has physical product.
- **Channel 3: 1688/Xiaohongshu/Douyin emerging brands** — Original designs, factory-to-brand signals. Lowest temperature, long nurture cycle.

## Report format

The weekly report has four sections:
1. KS/IGG project signals (Kicktraq) — table with project, category, progress, goal, time left, China signals, checkbox
2. Funding/brand signals (36kr) — article list with round, amount, snippet
3. HN discussions (reference) — low-signal, supplemental
4. Last week's unprocessed leads — reminder table

## Pitfalls

- **Don't try to scrape KS/IGG directly.** Cloudflare blocks it. Kicktraq is the workaround.
- **36kr RSS filtering must be two-tier.** Single-tier "any keyword match" produces too much noise (天猫618, 腾讯AI articles pass through).
- **China signal detection is heuristic, not authoritative.** The user must verify manually. Don't claim a project is Chinese based solely on automated signals.
- **Don't auto-contact leads.** The user decides who to reach out to. Automation stops at report generation.
- **The cron job runs in a fresh session.** The script must be self-contained with no dependencies on conversation context.
