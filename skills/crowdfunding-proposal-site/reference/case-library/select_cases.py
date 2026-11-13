#!/usr/bin/env python3
"""Rank PDF-backed product cases; unresolved links remain explicit research tasks."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--tags', required=True, help='Comma-separated catalog tags')
p.add_argument('--market', choices=['US', 'JP', 'TW'], required=True)
p.add_argument('--limit', type=int, choices=range(6, 9), default=8)
a = p.parse_args()
data = json.loads(Path(__file__).with_name('catalog.json').read_text())
tags = {x.strip() for x in a.tags.replace('，', ',').split(',') if x.strip()}
adjacent = [set(x.split(',')) for x in ['AI办公,AI硬件,穿戴,XR眼镜', 'AI陪伴,机器人,AI硬件', '影像,创作者,创客制造', '储能,户外', '宠物,家居,清洁家电', '健身,穿戴,户外', '存储计算,创作者,游戏']]
near = set().union(*(group for group in adjacent if group & tags)) - tags
ranked = []
for case in data['cases']:
    direct = tags & set(case['tags'])
    related = near & set(case['tags'])
    score = (100 + len(direct) * 10 if direct else 30 + len(related) if related else 0)
    score += 15 if case['market'] == a.market else 0
    ranked.append((score, case, direct, related))
ranked.sort(key=lambda row: -row[0])
selected, products = [], set()
for score, case, direct, related in ranked:
    if case['product'] in products:
        continue
    products.add(case['product'])
    selected.append({**case, 'match': 'direct' if direct else 'adjacent' if related else 'market_fallback', 'matched_tags': sorted(direct or related), 'needs_link_verification': case['link_status'] not in ('search_match', 'page_match'), 'relation_note_required': True})
    if len(selected) == a.limit:
        break
print(json.dumps({'selected': selected, 'review': 'Check relevance and source dates; verify unresolved URLs before publishing. Historical PDF amounts are not live totals.'}, ensure_ascii=False, indent=2))
