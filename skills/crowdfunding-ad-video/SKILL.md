---
name: crowdfunding-ad-video
description: Turn a product TVC or client-finished videos into crowdfunding ad creatives for Kickstarter, Indiegogo, Makuake or 嘖嘖 zeczec (pre-launch / live / post) — watch + transcribe the source, cut a long version and 20–25 s selling-point shorts, per-shot 9:16 reframing, copy overlays in Japanese / English / Traditional or Simplified Chinese traced to the campaign's own copy sheets, official platform logo badge, discount tag / coupon ticket / CTA bar, two layout styles (grey-grade serif cards; KS-"Live Now" bottom-band frame), QA and UTF-8 zip delivery. Use when the user says 剪投放素材/广告素材/竖版/压字/折扣框/预热信息/KS/IGG/Makuake/嘖嘖 投放视频, sends a TVC or 成片 to "加压字和折扣", or shares a reference ad layout to copy.
---

# Crowdfunding ad video

## 飞轮视频分支
由 `ad-flywheel-impact` 统一调度；发现获授权的可剪辑源视频时必须执行本分支，不能只抽帧做图。图片完整生图规则只约束静态广告，视频允许本技能的 FFmpeg/Pillow 字幕和叠层渲染；禁止用 Figma 制作视频。当前任务只更新技能时，不渲染客户视频。

先读 `references/integration.md`，确认真实工具、字体、素材和语音处理能力。

Config-driven: every project gets one `project.json`; scripts in `scripts/` do the cutting and drawing.
Use `references/example_project_pongbot.json` only as a neutral schema example; replace ALL source paths, scene times, edits, copy, claims and offer values with verified current-project values, then select
the `lang` / `platform` / `offer` blocks with the preset for the target platform in `references/platforms.md`.

Read before writing any copy or layout: `references/rules.md` (client rules from real feedback).
Schema: `references/config.md`. Layout geometry + which style: `references/layouts.md`.
Platform logos (verified, transparent PNG): `assets/platform_logos/{kickstarter,indiegogo,makuake,zeczec}.png`.

Work dir per project: `<project-workspace>/video/` (project.json, work/, out/). **Never delete the
scripts/work dir when the user says "删掉没用的"** — delete caches only (`work/pieces`, `work/cards`, qa images).

## Workflow

1. **Identify platform + stage + market.** Kickstarter / Indiegogo → `lang: "en"`; Makuake → `"ja"`;
   zeczec → `"zh-Hant"` (discounts in 折). Platform language is a default only; the user’s target market/language takes precedence. Stage = pre-launch (register / notify), live (back / pledge),
   post (InDemand / late pledge). Ask only if the sources don't say.
2. **Inventory + watch everything.** `python3 scripts/inspect_source.py SRC work/inspect_<n>` → Read every
   `sheet_*.jpg` (1 fps) and `words.txt`. No speech model? `bash scripts/get_whisper_model.sh`.
   Note structure (hook / reveal / claims / scenes / brand close / logo frame), VO lines with timestamps, which
   shots are product, which are CG internals (avoid), burned-in text. Music-only client edits → overlay-only path.
3. **Gather campaign facts.** Copy sheet / ad-angle sheet (Feishu → `lark-cli sheets +workbook-export
   --spreadsheet-token … --output-path x.xlsx`, then openpyxl), the pre-launch or campaign page (ego-browser per
   the user's global rule). Extract product name as the market uses it, exact offer wording + notation, CTA,
   quotable numbers. Every overlay line must come from these — add `"src"` per card, list sources in the README.
4. **Plan the cut** (TVC only). Long ≈ 60–95 s + shorts of **20–25 s**, one selling point / ad angle each. Product
   on screen in the first 3 s (`{"audio","video"}` override under the original VO); cut at sentence ends and shot
   boundaries; replace off-brief footage with scene shots under the same audio. Fill `tvc.vframe` from
   `shots_*.jpg` (crop centre 0–1, or `"fit"` for split screens / diagrams / UI / group shots). End on `"@logo"`.
5. **Assets.** Platform logo from `assets/platform_logos/` (or refresh: `scripts/platform_logo.py`, selectors in its
   docstring). Product cut-out from a white-background 3/4 (≈45°) render: `scripts/cutout.py RENDER.png out.png`.
   Brand logo PNG with alpha from the brand site.
6. **Mock, then render.** `python3 scripts/render.py project.json stills` → composite one card per layout on a real
   frame, Read it, fix. Then
   - TVC: `python3 scripts/render.py project.json tvc [--style grey|frame] [EDIT...]`
   - client videos: `python3 scripts/render.py project.json overlay [--style band|frame] [JOB...]`
7. **QA.** `python3 scripts/qa.py out --open3s qa_open.jpg --sheet qa_all.jpg [--transcribe ~/.cache/adkit/fw-base]`:
   product in first 3 s; frame/product/offer fully visible on the very first frame (thumbnail); copy readable on bright shots; nothing covers faces / product / burned-in labels; no
   discount twice in one frame; no empty 9:16 band; no clipped words; durations; audio present.
8. **Deliver.** `python3 scripts/pack_zip.py out <PackageName>` (UTF-8 names). Provide clickable final file links; reveal in the file manager only if available. README with every
   overlay line + source. Re-run QA after every revision.

## Revisions

Edit project.json → re-render only the affected names (pieces are cached: a 9:16 TVC short ≈ 40 s; 1440p client
videos 3–5 min each, run in background). Feedback about one element → change only that element and name the
files it touches. Same offer wording must be consistent across every style/file in the delivery.
When the user says "只调 skill / 先不用改视频", change the skill only — never overwrite delivered files; if a render
is already running, stop it and repair any half-written output (check every file opens).
