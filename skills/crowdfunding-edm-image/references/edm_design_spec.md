# EDM Design Spec

Use with the Crowdfunding EDM image workflow. Copy still comes from `EDM_Templates.md`; this spec controls visual design and construction only.

## Hard Rules

- Copy must be 100% sourced from `EDM_Templates.md` or the user-provided template source. Replace variables only.
- Do not add, delete, rewrite, polish, reorder, or add emoji to template copy.
- CTA uses platform or brand color. Default Kickstarter green is `#05CE78`; this workflow explicitly allows green.
- Other decorative elements should avoid cyan-green, neon color, and unrelated palettes.

## Visual Baseline

- Light premium email design.
- Warm white or pure white body.
- Large whitespace.
- Single-column `600px` canvas.
- Product-led opening.
- Large bold headline with one eyebrow.
- One high-contrast pill CTA.
- Dark footer.

Taste anchors:

- Elgato: light brand tint panel.
- Bose: white body plus strikethrough MSRP pricing.
- DJI: left copy and right product/spec points.
- GoPro: check list and eyebrow.
- Hawthorne: centered product.
- Designmodo: large number/stat impact.

## Canvas

- Width: `600px`.
- Export: `@2x`, actual image width `1200px`.
- Horizontal padding: `32px`.
- Module vertical spacing: `48px`.
- Spacing scale: `8 / 16 / 24 / 32 / 48`.

## Color Tokens

- `paper`: `#FFFFFF`
- `paper-warm`: `#F6F4F1`
- `tint`: brand at 8%
- `ink`: `#141414`
- `body`: `#3A3A3D`
- `muted`: `#8C8C92`
- `brand`: default Kickstarter green `#05CE78`
- `cta-bg`: brand
- `cta-text`: `#FFFFFF`
- `rule`: `#E7E3DC`
- `footer-bg`: `#141414`

If brand color is too light for white CTA text, either use `ink` text or darken brand one step.

Keep each EDM to no more than two neutral colors plus one brand color.

## Type

Use web-safe stack for real email text: `Helvetica Neue, Arial, sans-serif`.

- eyebrow: `12px`, caps, letter spacing `1.5`, muted or brand.
- H1: `32-40px`, bold, letter spacing `-0.5`, line-height `1.1`.
- H2: `22px`, semibold.
- body: `16px`, line-height `1.6`, body color.
- stat: `44-56px`, bold.
- price: `36px` bold + MSRP `15px` strikethrough muted.
- CTA: `15px`, bold, caps optional.
- footer: `12px`, muted.

## Module Library

- M0 Header: adaptive logo header. Dark logo uses white header; light logo uses black bar.
- M1 Hero: image2 plus text. Light brand tint panel with product, eyebrow, H1, pill CTA; or centered product. Image has no text; title stays as editable text.
- M2 Title + Opening: eyebrow, H1, opening sentence.
- M3 Stat strip: big stat numbers for discount, limited quantity, raised amount, specs.
- M4 Quote block: top and bottom hairlines, MSRP strikethrough, launch price, discount, limited chip.
- M5 CTA: single pill button in brand color.
- M6 Feature row: icons plus checklist or dot list.
- M7 Detail section: left text/right product image, spec points.
- M8 Product display: white or tint flat-lay/clean product.
- M9 Countdown: light background and large text such as `2 DAYS`, `24 HOURS`, `LAST 48 HRS`.
- M10 KOL/Media: thumbnail/badge and one quote line.
- M11 Milestone: large number, such as `Hit $X in Y hrs`.
- M12 Steps: `New to [Platform]? 1 / 2 / 3`.
- M13 Footer: dark background, logo/social circles/address/unsubscribe.

## image2 Rules

Generate images at `@2x`. Images must have no text, no logo, and no watermark.

- hero: `1200x1500` or `1200x800`.
- product: `1200x1200`.
- scene: `1200x800`.
- icon: `240x240`.

Prompt skeleton:

```text
[product, locked exact design] + [scene/context] + [composition] +
[soft studio lighting / clean light background] + [style: premium product photography] +
[palette: light, brand accent] + [NO text, NO logo, NO watermark] + [aspect ratio]
```

Product lock:

```text
match the exact product design, do not invent or alter any details
```

## Figma Rules

- One email equals one `600px` frame.
- Vertical auto-layout; each module is one auto-layout band.
- If the user-provided first-screen/hero image is already a complete designed EDM hero, use it full-bleed as the first module. Do not put it inside a tint panel, do not add another frame around it, and do not duplicate headline, benefits, or other text already present in that image.
- M0-M13 should become reusable components when possible.
- Text binds to variables and Codex replaces template variables only.
- Colors use Figma variables; skin changes by editing `brand`.
- Image fills use names such as `img/hero`, `img/product`, `icon/feat1`.
- Hero title is an independent text layer over/near image, not baked into the image.
- Export each band as `@2x PNG` named `[stage]_[NN]_[module].png`.

## Stage Mapping

Invite Deposit:

```text
M0 · M1 · M2 · M4 · M6 · M5 · M13
```

## Execution

1. User provides stage and product variables.
2. Read `EDM_Templates.md` and replace variables only.
3. Read this design spec and choose mapped modules.
4. Generate image2 assets for image slots only.
5. Build the Figma frame with components/modules.
6. Export module bands at `@2x`.
