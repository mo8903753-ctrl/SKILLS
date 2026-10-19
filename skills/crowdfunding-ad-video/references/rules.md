# Client rules

From real feedback on the PONGBOT Makuake job (2026-10). They are platform-independent; the Japanese
examples show the Makuake case — for KS / Indiegogo / zeczec use the equivalents in platforms.md.

## Content
- **Product within the first 3 s** of every video. Open on a product shot even if the VO starts elsewhere
  (audio/video override). Persistent bottom-left product cut-out also counts, but don't rely on it alone.
- **Scenes over internals.** No chip / motor / mechanism CG and no spec lines about them ("不要讲芯片，场景为主").
  Show people using the product on court/at home; keep the VO line only if it still makes sense over scenes.
- Shorts are **20–25 s** (client spec); a client-finished edit keeps its own length — say so, don't trim it.
- Cut only at sentence ends; re-transcribe outputs to prove no clipped words.

## Copy
- **Every overlay line must trace to the campaign's own material** (copy sheet / ad-angle sheet / landing page).
  Never copy wording from a reference ad the user shares — references are for layout only
  (e.g. Halliday's 「Makuakeで日本初上陸」「30%OFF以上でGET」 were NOT allowed).
- Use **stage-correct wording**. Pre-launch (预热) = register / notify / coming soon — e.g. Makuake
  「まもなくMakuakeにて登場」「事前登録者限定」「最大35%OFF」「お得な情報をお届け」, KS "Launching soon on Kickstarter",
  "Get notified at launch". Never promise an available purchase ("購入", "Buy", "Back now") before launch. Interpret the full sentence: GET notified / 情報をGET means information and is not automatically a purchase promise; confirmed project copy takes precedence.
- Use the market's discount notation: %OFF (JP / EN), 折 in Taiwan (35% off = 6.5折).
- Numbers: quote only what the sheets state. A bare 「6億円を突破」 reads like sales — prefer context
  (「海外クラファンで6億円突破」) or a footnote 「※2026年Kickstarter支援総額」.
- Product name: if footage shows a different variant than the campaign SKU (Aura vs Aura S), use the brand +
  category (「次世代AIテニスコーチ」) instead of the model name and flag it.
- TVC-only claims (features not in the JP copy sheet) need brand sign-off — prefer sheet claims.

## Offer & layout
- **Never show the same discount twice in one frame.** When the end CTA bar shows 35%OFF, swap the top-band
  offer for the product title (+ brand logo unless the footage already shows it).
- **9:16 blurred bands must not be empty**: upper band = badge + offer for the whole video; lower band = copy +
  product cut-out.
- **Official platform logo only** (`assets/platform_logos/` or `scripts/platform_logo.py`). Dark logos (Makuake,
  zeczec) go on a white pill on dark bands.
- Bottom band text = **2 lines**: line1 / 「[logo] line2」 (「まもなく」/「[Makuake] にて登場！」,
  "Coming soon on" / "[KICKSTARTER]") — never a third line (违和感).
- Ticket = 3 lines: header / big discount / note (「事前登録者限定」/「最大35%OFF」/「お得な情報をお届け」).
- 16:9 burned-in labels (client's English drill names etc.) must stay visible: move product/CTA bar around them
  (`h_opts.px/ph/bar_x/bar_y/text_above`), right-align copy when the product sits left.
- Match the reference element's typography, not just its wording/position: weight, italic, size ratio
  (e.g. the ticket numeral is heavy italic and fills the body — a regular-weight number "isn't the same").
- **First frame = thumbnail.** Everything that should be on screen from the start (frame, product cut-out,
  top offer) must be fully visible at t=0 — no fade-in on t=0 overlays (render.py handles it; QA checks it).
- Grey-grade style uses thin Mincho headlines; add a soft dark wash on bright shots instead of making text bold.
- Feedback about one element → change that element only; name the files affected.

## Delivery
- One folder of finals + UTF-8 zip + README listing every overlay line and its source.
- Keep scripts and project.json after delivery; only caches may be deleted. Trash on this Mac is unreadable from
  the shell; restore with `osascript -e 'tell application "Finder" to move (item "<name>" of trash) to (POSIX file "<dir>" as alias)'`.
