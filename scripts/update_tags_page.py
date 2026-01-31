#!/usr/bin/env python3
"""Regenerate docs/tags.md from site/tags.json.

Usage:
  1. Run `mkdocs build` to produce `site/tags.json`.
  2. Run `python3 scripts/update_tags_page.py` to regenerate `docs/tags.md`.

This makes it easy to keep the Tags doc in sync with what the site publishes.
"""
from pathlib import Path
import json

ROOT = Path('.')
SITE = ROOT / 'site'
TAGS_JSON = SITE / 'tags.json'
OUT = ROOT / 'docs' / 'tags.md'

if not TAGS_JSON.exists():
    print("site/tags.json not found. Run `mkdocs build` first.")
    raise SystemExit(2)

data = json.loads(TAGS_JSON.read_text(encoding='utf-8'))

# Count pages per tag
counts = {}
for m in data.get('mappings', []):
    for tag in m.get('tags', []):
        counts[tag] = counts.get(tag, 0) + 1

sorted_tags = sorted(counts.items(), key=lambda t: (-t[1], t[0]))

lines = [
    '---',
    'title: Tags',
    'description: Browse templates and pages by tag',
    '---',
    '',
    '# Tags',
    '',
    'Browse templates by topic and discover resources grouped by tag.',
    '',
    '## Current tag index',
    '',
]

for tag, cnt in sorted_tags:
    lines.append(f'- **{tag}** — {cnt} pages')
    # list pages for this tag (use page titles and relative links)
    for m in data.get('mappings', []):
        if tag in m.get('tags', []):
            item = m.get('item', {})
            url = item.get('url', '').rstrip('/') + '/'  # ensure trailing slash
            title = item.get('title', url)
            # relative link from /tags/ -> ../{url}
            rel = '../' + url
            lines.append(f'  - [{title}]({rel})')

lines += [
    '',
    '---',
    '',
    '## How this page is maintained',
    '',
    'This page is generated from `site/tags.json` via `scripts/update_tags_page.py` after a `mkdocs build`.',
    '',
    '<div style="text-align: right; font-size: 0.9rem; opacity: 0.8; margin-top: 1rem;">Back to <a href="/">Home</a></div>',
]

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {OUT} with {len(sorted_tags)} tags.')
