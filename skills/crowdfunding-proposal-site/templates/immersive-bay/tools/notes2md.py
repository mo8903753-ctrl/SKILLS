#!/usr/bin/env python3
"""Regenerate 演讲稿.md from assets/js/notes.js (the single source of truth for speaker notes).
Usage: python3 tools/notes2md.py [project_dir] [title]"""
import json, os, re, sys
root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
title = sys.argv[2] if len(sys.argv) > 2 else '众筹方案 · 演讲稿'
src = open(os.path.join(root, 'assets/js/notes.js'), encoding='utf-8').read()
notes = json.loads(re.search(r'export const NOTES = (\[.*\]);', src, re.S).group(1))
total = sum(n['sec'] for n in notes)
out = [f"# {title}\n\n共 {len(notes)} 段，预计 {total // 60} 分 {total % 60} 秒。每段对应网页上的一屏，提词是这一屏需要带到的数字或关键词。\n"]
cur = None
for i, n in enumerate(notes, 1):
    if n['ch'] != cur:
        cur = n['ch']; out.append(f"\n## {cur}\n")
    out.append(f"### {i:02d} · {n['t']}　约 {n['sec']} 秒\n")
    out.append(n['s'].replace('\n', '\n\n') + "\n")
    if n.get('cues'): out.append("**提词：** " + " · ".join(n['cues']) + "\n")
open(os.path.join(root, '演讲稿.md'), 'w', encoding='utf-8').write('\n'.join(out))
print(f'{len(notes)} notes · {total}s → 演讲稿.md')
