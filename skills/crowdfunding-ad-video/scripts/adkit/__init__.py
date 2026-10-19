"""adkit — config-driven crowdfunding ad-video toolkit (cut TVC → 9:16 pieces, overlays, frames, render)."""
import json, os

def load_project(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["_root"] = os.path.dirname(os.path.abspath(path))
    return cfg

def proj_path(cfg, p):
    """Resolve a path from project.json: absolute, ~, or relative to the project file."""
    if not p:
        return p
    p = os.path.expanduser(p)
    return p if os.path.isabs(p) else os.path.join(cfg["_root"], p)
