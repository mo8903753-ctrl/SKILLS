---
name: crowdfunding-edm-image
description: Use when creating image-based crowdfunding EDMs for Kickstarter or Indiegogo campaigns, especially when the user provides product renders or real photos and wants fixed email templates converted into pure image EDMs using image generation/image2 plus variable replacement.
---

# Crowdfunding EDM Image

Create pure-image crowdfunding EDMs from fixed lifecycle templates. The user provides product renders, real photos, or campaign assets plus project variables; use those inputs to build the EDM image, place the approved fixed copy into the final image, and return email-safe wrappers.

## Core Rule

The user's EDM template copy is the source of truth. Do not rewrite, summarize, polish, shorten, expand, re-order, or paraphrase it unless the user explicitly asks. Only replace variables such as `{{product_name}}`, `{{brand_name}}`, `{{deposit_amount}}`, `{{deposit_benefit}}`, URLs, prices, dates, and feature values.

The agent's responsibility is visual: layout, hierarchy, spacing, image direction, background/image2 usage, Figma composition, export structure, and email-safe handoff. Copy fidelity is more important than style.

Most important: never alter the product appearance during image2 generation. The provided product render/photo is the source of truth. The generated result must preserve the product's identity, shape, proportions, face, materials, colors, key details, and silhouette. Do not redraw, morph, beautify, re-face, re-shape, recolor, or invent product details.

## Inputs To Collect

Required:

- Product render or real product photo. If missing, ask for it before image2 output unless the user explicitly accepts a placeholder.
- The exact EDM template source for each requested stage, such as Google Sheet row, pasted template text, MailerLite/Klaviyo draft, or existing template file. If the user already referenced a sheet/template, use that source instead of built-in fallback copy.
- `brand_name`
- `product_name`
- `platform`: Kickstarter or Indiegogo
- `campaign_url`

Campaign offer variables when relevant:

- `launch_date`
- `deposit_url`
- `deposit_amount`
- `deposit_benefit`
- `price`
- `msrp`
- `discount`
- `limited_quantity`

Optional:

- `kol_name`, `kol_review_url`
- `press_name`, `press_url`
- `shipping_survey_url`
- brand colors, logo, typography preference
- target language

## Workflow

1. Confirm which stages to produce.
2. Locate the template copy for those stages from the user's source. If the user provided a Google Sheet, row, MailerLite/Klaviyo link, pasted template, or `EDM_Templates.md`, use that as the canonical copy. Read `references/templates.md` only as fallback stage guidance when no external template is supplied.
3. Extract the template fields exactly:
   - Subject
   - Preview text if present
   - Headline if present
   - Body paragraphs
   - CTA text and CTA URL variable
   - Any benefit/offer modules already in the template
4. Replace variables only. Do not change the surrounding wording.
5. If variables are incomplete, ask only for missing values required by the selected template text.
6. Use the user's product render or photo as the visual source of truth.
7. For each selected stage, create an image2 prompt with a product-lock instruction:
   - Use the provided product image as the visual source of truth.
   - Preserve the product exactly in appearance: same face/body/product geometry, same proportions, same materials, same colors, same visible details.
   - Do not create a similar product or upgraded product.
   - Changes are allowed only to background, lighting mood, supporting graphics, layout space, offer badge shapes, and EDM design elements.
   - Do not bake template copy into generated image2 output unless the user explicitly requests all text in the generated image. Prefer Figma/layout text placement for spelling and fidelity control.
8. Generate image2 assets using the available image generation tool only when needed.
9. For visual construction, read `references/edm_design_spec.md` and follow its canvas, module, token, and stage mapping rules.
10. Compose the EDM as a pure image or Figma export:
   - Hero/product visual
   - Exact template headline/body modules with variables replaced
   - Readable black or white content panels for headline/body text
   - Offer block
   - Feature bullets
   - CTA
   - Footer/brand signoff
11. Return:
   - Subject
   - Preview text
   - Final image path or generated image
   - HTML wrapper with a linked image
   - Alt text
   - Plain-text fallback
   - Copy fidelity note: state whether the copy came from the user's template source or fallback templates

## Default Stages

Use these stages unless the user selects a smaller set:

- Deposit Invitation
- Kickstarter Follow + Deposit
- 2 Days Countdown
- 24 Hours Countdown
- Launch Day
- Deposit Backer Version
- KOL Review
- Media Report
- Last 48 Hours
- Last 24 Hours
- Shipping Address Survey

## Image2 Prompt Pattern

Use this structure and adapt per stage. This prompt is for image2 generation with the product appearance locked:

```text
Use the provided product image as the strict visual source of truth. Create a premium crowdfunding EDM visual for {{product_name}}, a {{product_category}} product.

Stage: {{stage_name}}.
Purpose: {{stage_goal}}.

Critical product lock: preserve the product's exact appearance from the reference image. Do not change the product's face, body, silhouette, proportions, materials, colors, accessories, surface details, or perceived identity. Do not generate a similar replacement product. You may improve only the EDM presentation around it: background, lighting mood, depth, negative space, supporting graphic shapes, and campaign layout. Leave clear space for text overlay. Do not include fake logos, watermarks, UI screenshots, distorted hands, or invented product parts.
```

## Output Format

For each EDM:

```md
## {{stage_name}}

Subject:
{{subject}}

Preview Text:
{{preview_text}}

Image2 Prompt:
{{image_prompt}}

Final EDM Image:
{{image_path_or_inline_image}}

CTA:
{{cta_text}} -> {{cta_url}}

Alt Text:
{{alt_text}}

Plain Text Fallback:
{{plain_text}}

HTML Wrapper:
{{html_wrapper}}
```

## Quality Bar

- Copy fidelity: layout must adapt to the exact template copy, not the other way around. If copy is long, split it visually by its existing paragraph/module boundaries. Do not rewrite it to make the layout easier.
- Use Really Good Emails / Kickstarter-style email composition as the taste reference: editorial hierarchy, restrained modules, generous spacing, clear reading path, and campaign-native urgency.
- Avoid layouts that look like a web app, dashboard, or HTML component stack. In particular, avoid generic rounded CTA pills, repeated card grids, oversized web buttons, and UI-looking icon tiles unless the source image already contains them.
- Choose colors from the provided product image or brand image. If a coordinated palette is not obvious, default to a white body area with black text and one restrained accent from the source image.
- CTA must match the chosen email style. If the user asks for a button, make it read as a real clickable email button: centered, clearly bounded, proportional, with enough padding and contrast. Do not make it look like a full-width banner unless the user asks for a banner.
- If an EDM needs two CTAs, prefer exporting two vertically continuous images instead of forcing everything into one overloaded long image. Image 1 should carry hero/offer/primary CTA; Image 2 should continue the same visual system with body copy, benefits, secondary CTA, and footer. Make the bottom of Image 1 and top of Image 2 share the same background, margins, and rhythm so they stack seamlessly in MailerLite/Klaviyo.
- Mobile-first email image: keep important text in a central safe area.
- Keep copy blocks readable. If the supplied template is dense, use multiple panels, columns, pull quotes, section breaks, or separate stacked frames to make it readable without changing text.
- Center key visual modules precisely. If benefit cards are used, center the group and center each card's internal typography unless the composition is intentionally editorial-left.
- Put important text on solid or near-solid black/white panels when the background is complex. Do not place paragraph copy directly over a busy product scene.
- Recommended layout: product hero on top, then a black/white editorial body block, then a concise offer/action band, then a quiet footer.
- Avoid tiny body copy in the image; if the copy is long, split it into 2-3 short modules.
- Keep the product inspectable and pixel-faithful to the provided asset. Do not obscure it with oversized badges.
- Product preservation beats visual polish. If a prettier result would change product appearance, reject it.
- If image2 changes the product appearance, treat the result as failed and regenerate with a stricter product-lock prompt.
- Always produce plain-text fallback because image-only emails can be blocked by email clients.
- If product facts are missing, leave a clear placeholder instead of inventing claims.

## Helper Script

Use `scripts/render_edm_brief.py` when the user provides structured JSON variables and wants the template output quickly. The script supports external template overrides through a top-level `templates` object in the JSON. Built-in templates are fallback only. It does not generate images.
