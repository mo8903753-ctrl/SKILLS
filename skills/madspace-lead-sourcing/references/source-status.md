# MadSpace Lead Scanner — Data Source Status

Last verified: 2026-06-05

## Working Sources

| Source | URL | Method | Output | Notes |
|--------|-----|--------|--------|-------|
| 36氪 RSS | `https://36kr.com/feed` | XML parse | Company, founder, round, amount | Best source for funded hardware companies |
| 爱范儿 RSS | `https://www.ifanr.com/feed` | XML parse | Product launches, tech news | Noisy, needs filtering |
| 少数派 RSS | `https://sspai.com/feed` | XML parse | Hardware reviews | Low signal-to-noise |
| Kicktraq Hotlist | `https://www.kicktraq.com/hotlist/` | HTML scrape | Project name, category, %, goal, time left, KS link | No Cloudflare — gold mine |
| HN Algolia | `https://hn.algolia.com/api/v1/search` | JSON API | KS project discussions | Low signal, reference only |

## Blocked Sources (No Workaround)

| Source | Reason | Impact |
|--------|--------|--------|
| Kickstarter.com | Cloudflare JS challenge | Cannot scrape project pages directly |
| Indiegogo.com | Cloudflare JS challenge | Cannot scrape project pages |
| Google Search | CAPTCHA / JS required | Cannot direct-scrape results |
| DuckDuckGo | anomaly detection / CAPTCHA | Worked briefly, now blocked |
| Bing Search | Timeout / JS required | Cannot scrape |
| 京东众筹 (z.jd.com) | SSL error / redirect | Cannot access |
| 淘宝众筹 (izhongchou) | React SPA, no SSR data | Empty HTML shell |
| 1688 (s.1688.com) | Bot detection | Cannot scrape products |
| IT桔子 (itjuzi.com) | HTTP 412 | Cannot access |
| 猎云网 (lieyunwang.com) | Connection refused | Cannot access |
| 品玩 (pingwest.com) | Not real RSS | Returns HTML, not XML |

## Cron Job Architecture

The only path for Google-level search discovery is through the Hermes agent's `web_search` tool, which uses a different infrastructure. The cron job must be agent-driven:

1. Agent runs `lead_scanner_v2.py` via terminal (for RSS + Kicktraq)
2. Agent uses `web_search` for Chinese hardware brand discovery
3. Agent searches for company websites, founders, LinkedIn/企查查 links
4. Agent generates combined Markdown report

Required toolsets: `web`, `terminal`, `file`, `skills`
