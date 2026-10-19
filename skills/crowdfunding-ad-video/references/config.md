# project.json

Platform-specific `lang` / `platform` / `offer` blocks: `platforms.md`.
Neutral schema (fill before rendering): `example_project_pongbot.json` (historical filename retained for compatibility; no client configuration bundled). Paths may be absolute, `~`, or relative to project.json.

```jsonc
{
  "out_dir": "out", "cache_dir": "work/pieces", "cards_dir": "work/cards",
  "naming": {"grey": "A_灰调_", "frame": "B_底栏框_", "overlay": "C_新素材_", "overlay_frame": "C_新素材_底栏框_"},
  "grade": "…optional ffmpeg filter for grey style…",
  "lang": "ja",                                   // ja | en | zh-Hant | zh-Hans → font preset (adkit/draw.py LANG_FONTS)
  "fonts":  {"serif": ["/path/font.ttc", 0], …},  // optional per-key override of the preset
  "colors": {"offer": [243,112,33], "cta": [24,70,52], "band": [16,42,84], "band_accent": [255,214,0], …},          // optional
  "brand":    {"title": "次世代AIテニスコーチ", "logo_png": "…alpha logo…", "product_cutout": "…cutout.py output…"},
  "platform": {"name": "Makuake", "logo_png": "…platform_logo.py output…",
               "badge_pre": "まもなく", "badge_post": "にて登場", "band_line1": "まもなく", "band_line2": "にて登場！"},
  "offer": {
    "tag_lines":     ["まもなくMakuakeにて登場！", "事前登録者限定 最大35%OFF", "お得な情報をお届け"],  // grey mid-video tag, 16:9 tag
    "top_tag_lines": ["事前登録者限定", "最大35%OFF", "お得な情報をお届け"],                       // 9:16 upper band
    "ticket": {"head": "事前登録者限定", "pre": "最大", "big": "35%", "post": "OFF", "note": "お得な情報をお届け"},
    "cta": {"pre": "事前登録者限定 最大", "number": "35", "pct": "%", "post": "OFF情報"},
    "cta_sub": "クリックして5秒でカンタン登録完了！", "cta_sub_lines": ["クリックして", "5秒でカンタン登録完了！"]
  },
  "tvc": {
    "source": "…4K TVC…", "fps": 25, "src_size": [3840, 2160],
    "tails": {"logo": [174.3, 177.4], "lineup": [172.6, 177.4]},
    "vframe": [[0.0, 0.62], [2.68, 0.52], [67.88, "fit"], …],      // shot start → crop centre (0–1) or "fit"
    "edits": [{
      "name": "02_VoiceCoach", "styles": ["grey", "frame"],
      "segs": [{"audio": [33.56, 36.2], "video": [[167.48, 168.88], [79.56, 80.8]]},   // product opener under VO
               [36.2, 41.0], [43.92, 56.16], "@logo"],
      "cards": [{"t": [0.2, 7.3], "head": "自主練中も、\nAIコーチはそばにいる。", "sub": "…", "badge": true,
                 "src": "诉求表 No.3"},
                {"t": [7.6, 13.7], "head": "…", "y": 1480},
                {"t": [14.0, 19.5], "head": "…", "offer": true}]
    }]
  },
  "overlay_jobs": [{
    "name": "B_MultiPosition", "source": "…client 16:9 or 9:16 mp4…", "end": 35.0,      // end-card start (s)
    "styles": ["band", "frame"], "end_title_logo": true,
    "h_opts": {"px": 6, "ph": 230, "bar_y": 950, "bar_x": 740, "text_above": true},     // 16:9 label avoidance
    "cards": [{"t": [0.2, 4.6], "head": "…", "sub": "…", "side": "right"}]
  }]
}
```

Notes
- Card times are output-timeline seconds. Card times past `end` are clipped at `end`.
- Override segments: Σ video lengths must equal the audio length after snapping to the fps grid (script exits
  with the mismatch otherwise).
- `vframe` entries are shot starts in source time; pieces are split at these boundaries automatically.
- Copy lines: `\n` = line break. Keep headlines ≤ 15 full-width chars per line at 62 px on 1080 width.
