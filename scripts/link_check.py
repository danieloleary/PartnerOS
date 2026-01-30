"""Simple link checker for locally built MkDocs site.

Checks local relative links and image sources to ensure files exist and anchors are present on target pages.
"""
from bs4 import BeautifulSoup
from pathlib import Path
import sys

SITE_DIR = Path('site')

if not SITE_DIR.exists():
    print("Site directory not found. Run 'mkdocs build' first.")
    sys.exit(2)

errors = []

for html in SITE_DIR.rglob('*.html'):
    soup = BeautifulSoup(html.read_text(encoding='utf-8'), 'html.parser')
    for tag in soup.find_all(['a', 'img']):
        attr = 'href' if tag.name == 'a' else 'src'
        val = tag.get(attr)
        if not val:
            continue
        # Ignore external links
        if val.startswith('http://') or val.startswith('https://') or val.startswith('//'):
            continue
        # Ignore GitHub Pages absolute links (site hosted under /PartnerOS)
        if val.startswith('/PartnerOS'):
            continue
        # Ignore mailto, javascript pseudo-links and anchors-only links
        if val.startswith('mailto:') or val.startswith('javascript:'):
            continue
        if val.startswith('#'):
            # anchor in same page
            anchor = val[1:]
            if anchor and not soup.find(id=anchor) and not soup.find(attrs={'name': anchor}):
                errors.append(f"Missing anchor #{anchor} in {html}")
            continue
        # Handle fragment
        if '#' in val:
            path_str, anchor = val.split('#', 1)
        else:
            path_str, anchor = val, None

        target = (html.parent / path_str).resolve()
        # If path_str ends with '/', map to index.html
        if str(path_str).endswith('/'):
            target = target / 'index.html'
        # If target is a directory, check for index.html
        if target.is_dir():
            if not (target / 'index.html').exists():
                errors.append(f"Missing index.html for directory link {val} in {html}")
            continue
        if not target.exists():
            # Fallback: try resolving relative to site root (some MkDocs links are root-relative or rewritten)
            root_based = (SITE_DIR / Path(val).as_posix().lstrip('/')).resolve()
            # If path ends with '/', point to index.html
            if str(val).endswith('/'):
                if (root_based / 'index.html').exists():
                    continue
            if root_based.exists():
                if anchor:
                    content = root_based.read_text(encoding='utf-8')
                    if f'id="{anchor}"' not in content and f'name="{anchor}"' not in content:
                        errors.append(f"Missing anchor #{anchor} in {root_based} (linked from {html})")
                    continue
                continue

            errors.append(f"Broken link {val} in {html}")
            continue
        if anchor:
            content = target.read_text(encoding='utf-8')
            if f'id="{anchor}"' not in content and f'name="{anchor}"' not in content:
                errors.append(f"Missing anchor #{anchor} in {target} (linked from {html})")

if errors:
    print("Link check found issues:")
    for e in errors:
        print(' -', e)
    sys.exit(1)
else:
    print("No broken local links or missing anchors found.")
    sys.exit(0)
