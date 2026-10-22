"""Render README.md through GitHub's Markdown API into .preview.html for a local look.

Needs the gh CLI logged in. Serve the repo root (python -m http.server) and open
/.preview.html; the page follows prefers-color-scheme like github.com does.

    python scripts/preview.py
"""

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

body = json.dumps({"text": (ROOT / "README.md").read_text(encoding="utf-8"), "mode": "markdown"})
html = subprocess.run(
    [shutil.which("gh") or "gh", "api", "markdown", "--input", "-"],
    input=body, capture_output=True, text=True, encoding="utf-8", check=True,
).stdout

page = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>README preview</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css">
<style>
  body {{ margin: 0; background: #ffffff; }}
  @media (prefers-color-scheme: dark) {{ body {{ background: #0d1117; }} }}
  .markdown-body {{ box-sizing: border-box; max-width: 896px; margin: 24px auto; padding: 24px;
    border: 1px solid #d0d7de; border-radius: 6px; }}
  @media (prefers-color-scheme: dark) {{ .markdown-body {{ border-color: #30363d; }} }}
</style></head>
<body><article class="markdown-body">{html}</article></body></html>
"""
(ROOT / ".preview.html").write_text(page, encoding="utf-8")

# Forced-dark copy, so dark mode can be checked whatever the OS theme is
dark = (page.replace("-light.svg", "-dark.svg").replace("theme=light", "theme=dark")
        .replace("@media (prefers-color-scheme: dark)", "@media all")
        .replace("github-markdown.min.css", "github-markdown-dark.min.css"))
(ROOT / ".preview-dark.html").write_text(dark, encoding="utf-8")
print("wrote .preview.html and .preview-dark.html")
