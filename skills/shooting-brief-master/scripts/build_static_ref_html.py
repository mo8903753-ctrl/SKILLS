#!/usr/bin/env python3
"""Build HTML snippets for reusable shooting brief reference images."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
from pathlib import Path


PLACEHOLDER = '<div class="img-placeholder">参考图<br>[请插入]</div>'


def build_img_html(path: Path, caption: str) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        '<figure class="ref-card">'
        f'<img class="ref-img" src="data:{mime};base64,{data}" alt="{caption}">'
        f"<figcaption>{caption}</figcaption>"
        "</figure>"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assets-dir",
        default=Path(__file__).resolve().parents[1] / "assets" / "static-references",
        type=Path,
    )
    parser.add_argument(
        "--manifest",
        default=Path(__file__).resolve().parents[1] / "references" / "static-reference-manifest.json",
        type=Path,
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    snippets = {}
    for item in manifest:
        slot = item["slot"]
        filename = item["filename"]
        caption = item["caption"]
        path = args.assets_dir / filename
        snippets[slot] = build_img_html(path, caption) if path.exists() else PLACEHOLDER

    print(json.dumps(snippets, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
