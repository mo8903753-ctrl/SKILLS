# B2B/Enterprise Product → Consumer Crowdfunding Repositioning

Pattern used when the client's product was built for enterprise/government/industrial buyers
and needs to be reframed for a Western Kickstarter/IGG audience.

## Core Principle

Don't translate the B2B narrative. Rebuild it from the user's pain point outward.
The enterprise origin story is a CREDIBILITY SIGNAL, not the headline.

## Step-by-step

### 1. Strip unsellable angles
- Remove: national-security narratives, government mandates, compliance-only features, domestic-policy drivers (e.g. 信创, 等保, 79号文)
- Keep: hardware specs, reliability data, deployment track record as trust signals

### 2. Find the consumer pain point
Map each enterprise feature to a consumer anxiety:
- RAID-TP (3-drive tolerance) → "your 4K project footage can't be re-shot"
- Audit logging → "zero telemetry, zero cloud account required"
- SAS backplane → "no silent data corruption eating your photo library"
- Docker + AI GPU → "run local LLMs, your data never leaves your network"

### 3. Build the new narrative arc
- **Headline**: Enterprise feature → consumer benefit. "12Gb SAS" becomes "data center DNA on your desk"
- **Enemy**: Not competitors — the STATUS QUO. Cloud subscriptions, data loss anxiety, Big Tech surveillance
- **Hero**: The product as liberation from the enemy

### 4. Price derivation (when no consumer pricing exists)

**Competitive anchoring is mandatory.** Find the nearest KS-validated competitor in the same product category and price band — that's your price ceiling, not your floor. The user's psychology on KS is comparison, not isolation.

**Steps:**
1. Identify the #1 KS competitor in the same category (e.g., UGREEN NASync DXP8800 Plus for 8-bay NAS at $899-$1,049)
2. Build a competitive pricing anchor table with: product name, positioning, key specs, KS price range, current retail price
3. Set your Launch Special（主力档，销量 ≥60%）at or near the competitor's early-bird anchor — don't try to price higher on "enterprise features" narrative
4. Differentiate on VALUE at the same price, not on price premium

**Two-scenario pricing**: When a key spec is uncertain (e.g., 10GbE — standard or optional?), present both scenarios:
- **Plan A** (spec included): Price at competitor anchor, compete on enterprise features at same price
- **Plan B** (spec gapped): Drop price by $100-150 to compensate the visible spec gap in comparison tables

**MSRP anchor**: Set post-KS retail at roughly 1.6-1.8x the Launch Special price. This creates the "discount depth" perception that drives KS conversion.

**Diskless-first + Add-Ons (NOT default bundles)**: Diskless base tiers drive volume by keeping the entry price low. Hard drives, networking upgrades, extended warranty, and migration services are separate Add-Ons the user selects at checkout. This follows the UGREEN/ZimaCube proven pattern: ~65% of units sold are Diskless, Add-Ons capture the remaining revenue. Do NOT make bundles the default or the "featured" tier — it raises the psychological entry price and shrinks the funnel.

**Pitfall**: Do NOT use domestic-market prestige (信创, 国家级实验室, 中科院血统, government deployment count) to justify a higher KS price. These credibility signals are valuable as trust elements in the narrative, but they do not translate to willingness-to-pay on Kickstarter. KS users compare price-to-specs, not price-to-pedigree.

### 5. Competitive positioning reframe
- Don't compare on enterprise specs directly — consumer buyers don't know what SAS is
- Compare on OUTCOMES: "Triple-drive failure without data loss" vs "RAID-6 is the best Synology offers"
- Use feature comparison tables with ✓/✗, radar charts with relatable dimensions
- Position enterprise competitors (Dell, HPE) as "you'd pay $7,000+ for this, minimum"

### 6. Audience selection
Enterprise buyers become these Kickstarter personas:
- IT/ops → "Developers & Homelabbers"
- Compliance officers → "Privacy Advocates"  
- Department heads → "Small Studios & Agencies"
- End users → "Content Creators"

## When NOT to reposition
- If the product genuinely has no consumer use case (e.g., regulatory-only compliance hardware)
- If the price floor can't drop below $2,000 (crowdfunding psychology breaks above ~$1,500 avg pledge)
- If the brand has zero Western-facing assets (no English docs, no international warranty path)

## Concrete example: C2000 NAS (this session)

> 下例档位命名（SEB/EB/KS Special）是该案例的历史结构；现行阶梯 = Secret Reward < Launch Special（主力 ≥60%）< SEB < EB < Late Pledge，见 SKILL.md「价格与行动」。复用时套现行命名，价位逻辑不变。
- Original: 信创智能NAS存储一体机 for Chinese government/SOE/education/healthcare
- Reframed: "Enterprise Storage. Your Desk." — data-center hardware in desktop form for creators
- Stripped: 信创 certification, domestic CPU narrative, 79号文 compliance timeline
- Kept: SAS, RAID-TP, RECC ECC, dual system SSD, Docker+AI, one-click setup, WORM, audit logging, PC backup, AD permissions
- Added: privacy angle, cloud fatigue narrative, creator use cases
- Pricing (Plan A, 10GbE standard): $899 SEB / $999 EB / $1,099 KS Special, MSRP anchor $1,599
- Pricing (Plan B, 1GbE only): $749 SEB / $849 EB / $949 KS Special, MSRP anchor $1,299
- Competitive anchors: UGREEN DXP8800 Plus ($899-$1,049 KS), Synology DS1823xs+ (~$1,799 retail), TerraMaster F8 SSD Plus ($719-$799), ZimaCube Pro ($1,099)
- Tiers: 3 Diskless base tiers + Rackmount EB + Add-On menu (HDD bundles, 10GbE/25GbE upgrade, extended warranty, data migration)
- Key learning: Do not price above UGREEN's $999 anchor. Differentiate on enterprise features at the same price, not on pedigree premium.
