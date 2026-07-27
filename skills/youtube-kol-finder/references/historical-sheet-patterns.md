# Historical Sheet Patterns

This reference summarizes the user's historical KOL Google Sheets without preserving private contact, shipping, tracking, payment, or address data.

## Observed Pattern

Six historical sheets share a recurring operating structure:

- KOL identity: KOL name, channel URL, example link.
- Scale metrics: total view count, subscribers/followers.
- Geography: location/country.
- Commercial signal: fee, actual fee, quote notes, CPM, average views.
- Fit signal: video content style, brand/client advice, MadSpace advice, client comments, MadSpace notes.
- Outreach ownership: MadSpace contact PR and PR notes.
- Fulfillment tracking: shipping address, tracking number, sample/product status, product received.
- Publishing/payment: final review link and payment proof.

Country concentration in the historical sheets is strongly Western-market oriented, with United States first, then United Kingdom and Canada, followed by Australia, Germany, France, and other Western or English-friendly regions.

## Default Research Schema

Use this structure when the user asks to find or screen new KOLs. It is optimized for research and avoids sensitive execution fields.

| Column | Purpose |
|---|---|
| KOL NAME / KOL名称 | Channel or creator name. |
| View Counts / 总观看量 | Public total channel views when available. |
| Followers/Subscribers / 粉丝数 / 订阅数 | Public subscriber count. |
| Location / 地区 | Creator location or primary market. |
| Example link / 示例链接 | Best relevant channel/video URL. |
| Fee / 报价 / 费用 | Public quote, known quote, estimate, product exchange, or Need verify. |
| Average Views / 近期平均播放 | Recent relevant average or median views; specify basis in notes if needed. |
| CPM | Fee divided by average views times 1000 when fee and views are known. |
| video content style / 视频内容风格 | Main content type and product category fit. |
| Crowdfunding experience / 众筹经验 | Kickstarter/Indiegogo/launch review history or Need verify. |
| Client advice （Yes/No/Backup） / 品牌方建议 | Leave blank unless the client has provided a decision. |
| Client Notes / 品牌方备注 | Client-side feedback only. |
| MadSpace Advice / MadSpace建议 | Yes, Backup, or No based on the rubric. |
| MS Notes / MS备注 | Concise reason, risks, and next action. |
| Madspace Contact PR / MadSpace PR开发人员 | Owner if assigned. |
| Note For PR / PR备注 | Outreach angle, fee question, sample note, or prelaunch timing note. |
| Contact / 联系方式 | Public contact URL/email if available; otherwise Need verify. |
| Source checked date / 信息核查日期 | Date the public data was checked. |

## Execution Schema

Use this only when the user is managing active outreach, sample delivery, publishing, or payment.

Start with all research schema columns, then append:

| Column | Purpose |
|---|---|
| Shipping Address / 收货地址 | Current-project address only, provided by the creator or user. |
| Product status (Tracking Number) / 产品状态（物流单号） | Sample status and tracking number. |
| Additional Info / 补充信息 | Fulfillment or creator constraints. |
| Product Received (Y/N) / 是否已收货（是 / 否） | Sample receipt status. |
| Final review link / 最终评测链接 | Published video or short link. |
| Payment proof / 付款凭证 | Current-project payment proof reference. |

## Formatting Rules

- Preserve bilingual column names when creating a Google Sheet-compatible table.
- Keep `MadSpace Advice` separate from `Client advice`; do not overwrite brand decisions with internal recommendations.
- Put short operational comments in `MS Notes` or `Note For PR`.
- Use `Need verify` instead of guessing missing fee, contact, country, or crowdfunding history.
- Keep rows one KOL/channel per line.
