# Platform presets

Pick the platform + stage, then fill project.json `lang`, `platform`, `offer`. The wording below is a
**starting point only** — the final lines must match the client's own pre-launch page / campaign page / copy
sheet (rules.md). Logos: copies in `assets/platform_logos/` (verified 2026-10-19); refresh with
`scripts/platform_logo.py` if a site redesigns.

Stage changes the verbs: pre-launch = register / notify / "coming soon" (never "buy"/"get"/"back now");
live = back / pledge / "live now"; post (Indiegogo InDemand, KS late pledge) = "order now / still available".

## Makuake (Japan) — `lang: "ja"`
- Logo: `assets/platform_logos/makuake.png` (colour icon + **black** wordmark → white pill on dark bands).
  `platform_logo.py --page https://www.makuake.com/ --symbol makuakelogo_pc --out makuake.png`
- Pre-launch: badge 「まもなく」+logo+「にて登場」; band 「まもなく」/「[logo] にて登場！」;
  offer 「事前登録者限定」「最大35%OFF」「お得な情報をお届け」; CTA sub 「クリックして5秒でカンタン登録完了！」(if the LP says so).
- Live: 「Makuakeにて好評実施中」/「応援購入受付中」, 「早割 最大35%OFF」, CTA 「今すぐ応援購入」.
- Discount notation: %OFF. Typical tiers: 超早割 / 早割 / Makuake割.

```json
"lang": "ja",
"platform": {"name": "Makuake", "logo_png": "<skill>/assets/platform_logos/makuake.png",
             "badge_pre": "まもなく", "badge_post": "にて登場", "band_line1": "まもなく", "band_line2": "にて登場！"}
```

## Kickstarter — `lang: "en"`
- Logo: `assets/platform_logos/kickstarter.png` (KS green wordmark; fine on light and dark, white pill optional).
  `platform_logo.py --page https://www.kickstarter.com/ --selector 'svg.valign-middle' --out kickstarter.png`
- Pre-launch: badge "Launching soon on"+logo; band "Coming soon on" / "[logo]" (band_line2 may be ""),
  offer "Early Bird" / "Up to 35% OFF" / "Get notified at launch"; CTA bar pre "EARLY BIRD UP TO", number "35",
  pct "%", post "OFF"; CTA sub "Sign up now — save your Early Bird spot".
- Live: badge "Live now on"+logo; offer "Super Early Bird" / "Up to 35% OFF MSRP"; CTA "Back it now".
- Discount notation: "% OFF (MSRP)" or "$X off"; KS bans "pre-order/shop" language on the page — keep ads consistent.

```json
"lang": "en",
"platform": {"name": "Kickstarter", "logo_png": "<skill>/assets/platform_logos/kickstarter.png",
             "badge_pre": "Launching soon on", "badge_post": "", "band_line1": "Coming soon on", "band_line2": ""}
```

## Indiegogo — `lang: "en"`
- Logo: `assets/platform_logos/indiegogo.png` (magenta wordmark).
  `platform_logo.py --page https://www.indiegogo.com/ --selector 'img.gfu-header-logo__full' --out indiegogo.png`
- Pre-launch: "Coming soon to"+logo; offer "Super Early Bird" / "Up to 35% OFF" / "Reserve your perk".
- Live: "Live now on"+logo, "Claim your perk"; InDemand: "Now on Indiegogo InDemand" / "Order now".
- Rewards are called **perks** on Indiegogo (not "rewards"/"tiers").

## 嘖嘖 zeczec (Taiwan) — `lang: "zh-Hant"`
- Logo: `assets/platform_logos/zeczec.png` (dark grey icon + 嘖嘖 → white pill on dark bands).
  `platform_logo.py --page https://www.zeczec.com/ --selector 'svg.logo' --parent 2 --out zeczec.png`
- Pre-launch: badge 「即將登上」+logo; band 「即將登上」/「[logo] 嘖嘖集資」 or 「搶先登記」;
  offer 「預先登記限定」「早鳥最低65折」「優惠資訊搶先通知」.
- Live: 「嘖嘖集資熱烈進行中」, 「早鳥限定 65折起」, CTA 「立即支持」.
- **Discount notation in Taiwan is 折**: 35% OFF = 「65折」 (and 「最低65折」 = up to 35% off). Don't print
  "35%OFF" for a TW audience unless the client's own page does. Use Traditional characters throughout.

```json
"lang": "zh-Hant",
"platform": {"name": "嘖嘖", "logo_png": "<skill>/assets/platform_logos/zeczec.png",
             "badge_pre": "即將登上", "badge_post": "", "band_line1": "即將登上", "band_line2": "群眾集資"},
"offer": {"cta": {"pre": "早鳥限定 最低", "number": "65", "pct": "", "post": "折"}, ...}
```

## Notes for any platform
- Ticket fields (`offer.ticket`): head / pre / big / post / note — e.g. EN: "EARLY BIRD" / "UP TO" / "35%" / "OFF" /
  "Get notified at launch"; TW: 「預先登記限定」/「最低」/「65」/「折」/「優惠資訊搶先通知」.
- Long English lines are wider than Japanese: keep tag lines ≤ ~26 chars at size 38, headlines ≤ ~22 chars per line.
- If the logo is a pure wordmark (KS, Indiegogo) the badge reads "Launching soon on [KICKSTARTER]"; leave
  `badge_post` empty rather than inventing words.
