# C2000 Case Study: B2B Enterprise NAS → KS Consumer Crowdfunding

> ⚠️ 本文是历史案例记录：其中的档位命名（SEB/EB/KS Special）早于现行五档阶梯（Secret Reward < Launch Special 主力 < SEB < EB < Late Pledge），且当时方案含认证类表述——现行规则是认证类内容一律不入方案（content-methodology.md §5）。复用时以 SKILL.md 现行默认为准。

## Source Product
中科通量 金刚·C2000 信创智能NAS存储一体机 (SmarCoStor)
- R&D lineage: 中科院计算所 · 睿芯集团
- Target market (domestic): 政府/央企/公检法/教育/医疗 — 信创合规B2B
- Hardware: 12Gb SAS, RAID-TP (3-disk tolerance), RECC ECC, dual system SSD, BMC, Docker+AI
- Original docs: zero consumer pricing, zero KS positioning, pure enterprise spec sheets

## Repositioning Strategy

### What to strip
- "信创国产化" — meaningless and counterproductive on KS
- "中科院血统" as pricing premium — trust proof only, not a selling point
- Domestic government deployment counts as headline claims
- B2B pricing logic (cost-plus, tender-based)

### What to build
- "8-Bay Enterprise NAS Under $999" as the price-memory anchor
- Enterprise Protection / No Cloud Dependency / Built for Heavy Files as the three narrative pillars
- Competitive pricing anchored to UGREEN DXP8800 Plus ($899-$1,049 on KS 2024)
- Diskless base tiers + Add-On menus (not default drive bundles)

### Critical product decision: 10GbE
The original spec: "标配2个1GbE，10/25GbE走扩展槽"
This is the single most important product decision for the campaign. If KS version can't ship with 10GbE, the $899 price anchor collapses → must drop to $749 and accept 30-40% lower fundraising expectations.

### Pricing outcome
- Plan A (10GbE): SEB $899 / EB $999 / KS Special $1,099 · MSRP $1,599
- Plan B (no 10GbE): SEB $749 / EB $849 / KS Special $949 · MSRP $1,299
- Add-Ons: 10GbE upgrade, HDD bundles, extended warranty, data migration

### Budget
- Fundraising goal: $200K or $500K
- Marketing budget: goal × 17.96% (from crowdfunding-marketing-plan formula)
- $200K → $35,920 marketing; $500K → $89,800 marketing

## Section Innovations Tested

1. **Cover with photography background**: Left-to-right dark gradient overlay (rgba(4,6,8,.85)→.55→0), white left-aligned text, right-side product visibility. Final iteration dropped the SVG animation entirely for a single-column left-aligned text layout — proved more legible at 125% zoom. Replaced the original warm-white overlay which made text and image unreadable ("太灰了,导致文字和图片都看不清").

2. **Use-case scene section**: Full-width product desk shot as background. Left-side vertical glass cards (rgba(4,6,8,.82) + blur 18px) with 01/02/03 numbers. Cards must NOT overlap the product body. Each card: one sentence body text max.

3. **"Winning Logics" section**: Three oversized-number columns explaining why the product wins on KS. Inserted after the overview.

4. **"What We Don't Say" section**: Five strategic boundaries on dark bg. Each card compressed to one sentence. Demonstrated professional judgment — the user called this "很出彩，也很专业."

5. **Campaign Success Picture**: Five-column stat strip. Title: "Campaign结束后的品牌资产" (NOT "你得到什么" — user rejected the latter as too blunt/colloquial for a professional consulting deck).

6. **Client Coordination section**: 2×2 grid of functional responsibility areas (产品决策/信任资产/转化资产/交付资产), each with color-coded left border (accent/teal/gold/negative).

7. **Product Teardown Variant B**: 860×520 SVG with dark title bar, device silhouette with drop-shadow, and 2-row×4-column feature grid. Developed because Variant A (callout lines) was too cramped for 8 enterprise features.

8. **Competitive Position Map**: Replaced the standard radar chart. X-axis = price, Y-axis = data protection capability. C2000 in the high-protection/low-price quadrant. After multiple SVG spacing failures and element overlaps, user replaced it with their own PNG. Lesson: when custom SVGs fail at 125% zoom, accept user-provided images rather than iterating SVG coordinates indefinitely.

9. **Launch Day 0-48h Battle Plan**: 6-column horizontal grid above the vertical timeline covering T-72h through T+48h. T0 cell has accent border, T+48h has teal border. All Reddit/HN/Twitter/X references purged — content limited to KOL reviews, press, email, KS page launch, ads, and data review.

10. **Timeline Phase Merge**: Phases 2 (embargo) and 3 (launch day) were merged into one timeline item since they're only 3 days apart. The merged item reads "评测解禁 → Launch Day" with a condensed description.

11. **Budget Section Cleanup**: The budget-structure explanation box was deleted (user found it redundant after the funnel was added). Budget funnel SVG was later replaced with user-provided PNG when the custom SVG had text overlap issues.

12. **Marketing Channel Pruning**: Reddit, Hacker News, Privacy/Security media, Newsletter sponsorships, and Creator community channels were all deleted in successive passes. Final channel set: YouTube/Tech Review, Third-party crowdfunding communities (24 from skill), Meta+Google ads, PR outreach. ROI-ranking header text ("渠道优先级 · 按ROI从高到低排列") and "最高ROI渠道" label on YouTube were also deleted.

13. **Landing Page Grouping**: 12 individual mini-cards were replaced with 4 grouped stage cards (首屏转化/产品证明/价格转化/信任与风险), each with a distinct border color. User flagged "12个平均排开，重点不突出" — grouping solved this.

14. **Risk Card 3-Line Format**: Paragraph-length risk descriptions were replaced with compact 3-line format (风险：/ 影响：/ 应对：). User flagged "段落太长，读起来费劲" — this format makes risks scannable.

15. **Feasibility Assessment Section**: Inserted between KPI/Risk and "What We Don't Say". Includes main conclusion, 3 why-feasible cards, key prerequisites, and recommended judgment with one-sentence closing. Phrasing: "C2000 具备上 Kickstarter 的可行性" (NOT "…但不适合以信创国产化作为主要卖点" — user deleted the negative framing from the conclusion).

16. **Market Data Bars → Number Cards**: The three-row animated SVG data bars were replaced with 4 large stat cards (12.4% / 18.7% / 78% / $3.5B→$8B) with source attribution per card. Reduces explanation overhead and looks cleaner at 125% zoom.

## User Design Standards (Enforced)

- "图片负责氛围和产品，文字必须有自己的暗色安全区"
- Card density: max 4 card-grid sections per deck; convert excess to strips/tables
- Mode A: All Chinese except product names, slogans, platform names
- Budget: pure marketing spend only, no platform fees, no BOM
- Floating logo: MadSpace agency logo (Mode A), not client product logo
- Cover text: white on dark gradient, left-aligned, 1-2 line tagline max
- 125% zoom: test all SVG elements and image-backed sections at 125% — what looks fine at 100% will overlap at 125%
- When user provides replacement images for broken SVG charts, embed them as base64 rather than continuing to fight with SVG coordinates
- Section titles: professional consulting language, not colloquial direct address ("品牌资产" not "你得到什么")
- Marketing channels: do NOT include Reddit, HN, Privacy/Security media, or independent Newsletter/Creator community channels unless the user explicitly adds them back
- Decision checklist: optional section, omit by default — P0/P1 items are already covered by the 10GbE gate and client coordination section
- Feasibility conclusion: state what IS feasible without the negative framing about what isn't ("C2000 具备上 Kickstarter 的可行性" standalone, without "但不适合以信创国产化作为主要卖点")
