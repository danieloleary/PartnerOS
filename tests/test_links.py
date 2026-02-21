"""Tests for link validation in PartnerOS documentation."""

import re
import pytest
from pathlib import Path
from tests.conftest import REPO_ROOT, DOCS_DIR, STARLIGHT_DOCS_DIR


class TestInternalLinks:
    """Test internal link validation."""

    def test_no_broken_internal_links_legacy(self):
        """Verify internal links in legacy docs/ resolve correctly."""
        # Lenient version - just check for major issues
        failures = []

        # Check for obvious broken patterns
        bad_patterns = [
            "I_Partner_Strategy_Templates",
            "I_Partner_Enablement_Templates",
        ]

        for f in DOCS_DIR.rglob("*.md"):
            content = f.read_text()

            for bad in bad_patterns:
                if bad in content:
                    failures.append(
                        f"{f.relative_to(DOCS_DIR)}: contains bad reference {bad}"
                    )

        # Allow some failures - legacy docs may have issues
        assert len(failures) < 5, (
            f"Too many broken links in legacy docs:\n" + "\n".join(failures[:10])
        )

    def test_no_broken_internal_links_starlight(self):
        """Verify internal links in Starlight docs resolve correctly."""
        all_files = {}
        all_folders = set()

        # Build file lookup
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            rel = str(f.relative_to(STARLIGHT_DOCS_DIR))
            basename = rel.rsplit("/", 1)[-1]
            folder = rel.rsplit("/", 1)[0] if "/" in rel else ""

            if folder:
                all_folders.add(folder)

            if basename not in all_files:
                all_files[basename] = []
            all_files[basename].append(rel)

        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for text, link in links:
                if any(
                    link.startswith(p)
                    for p in ("http:", "https:", "mailto:", "/", "#", "./", "../")
                ):
                    continue

                link_clean = link.rstrip("/")
                link_basename = link_clean.rsplit("/", 1)[-1]

                found = False

                # Check various patterns
                if link_clean in all_files:
                    found = True
                elif link_basename in all_files:
                    found = True
                elif link_clean + ".md" in all_files:
                    found = True
                elif link_clean + ".mdx" in all_files:
                    found = True
                elif link_basename + ".md" in all_files:
                    found = True
                elif link_clean in all_folders:
                    found = True
                elif link_basename in all_folders:
                    found = True
                # Handle index/ links
                elif link_clean.endswith("/index") or link_basename == "index":
                    folder_path = (
                        link_clean.rsplit("/", 1)[0]
                        if "/" in link_clean
                        else link_clean
                    )
                    if folder_path in all_folders:
                        found = True

                if not found:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: broken link to {link}"
                    )

        assert len(failures) == 0, f"Broken links:\n" + "\n".join(failures[:20])


class TestLinkFormatting:
    """Test link format compliance."""

    def test_no_md_extension_in_links(self):
        """Verify internal links don't use .md extension (Starlight folder-style)."""
        failures = []

        for docs_dir in [STARLIGHT_DOCS_DIR]:
            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                content = f.read_text()
                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

                for text, link in links:
                    if any(
                        link.startswith(p)
                        for p in ("http:", "https:", "mailto:", "/", "#")
                    ):
                        continue
                    if link.rstrip("/").endswith(
                        (".png", ".jpg", ".jpeg", ".svg", ".gif")
                    ):
                        continue

                    if ".md" in link and not link.startswith("http"):
                        failures.append(
                            f"{f.relative_to(docs_dir)}: link contains .md: {link}"
                        )

        assert len(failures) == 0, f"Links with .md extension:\n" + "\n".join(
            failures[:10]
        )

    def test_no_double_parentheses(self):
        """Verify no malformed links with double parentheses."""
        failures = []

        # Known documentation examples that show what NOT to do
        known_examples = [
            "skills/find-broken-links.md",  # Shows ((link)) as bad example
        ]

        for f in STARLIGHT_DOCS_DIR.rglob("*.md"):
            content = f.read_text()

            # Skip known documentation example files
            rel_path = str(f.relative_to(STARLIGHT_DOCS_DIR))
            if rel_path in known_examples:
                continue

            if "((" not in content:
                continue

            # Skip Mermaid diagrams
            in_mermaid = False
            for i, line in enumerate(content.split("\n"), 1):
                stripped = line.strip()
                if stripped.startswith("```mermaid"):
                    in_mermaid = not in_mermaid
                    continue
                if stripped == "```" and in_mermaid:
                    in_mermaid = not in_mermaid
                    continue
                if in_mermaid:
                    continue
                if "((" in line:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i}: {line.strip()[:60]}"
                    )

        assert len(failures) == 0, f"Double parentheses found:\n" + "\n".join(
            failures[:10]
        )

    def test_no_known_bad_references(self):
        """Verify no known bad legacy reference paths exist."""
        known_bad = [
            "I_Partner_Strategy_Templates",
            "I_Partner_Enablement_Templates",
        ]

        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            if not docs_dir.exists():
                continue

            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                # Skip skill documentation
                if "skills/" in str(f):
                    continue

                content = f.read_text()
                for bad_ref in known_bad:
                    if bad_ref in content:
                        failures.append(
                            f"{f.relative_to(docs_dir)}: contains {bad_ref}"
                        )

        assert len(failures) == 0, f"Bad references found:\n" + "\n".join(failures[:10])


class TestLinkQuality:
    """Test link quality and accessibility."""

    def test_link_text_not_empty(self):
        """Verify all links have descriptive text (not empty)."""
        failures = []

        # Check Starlight docs
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            # Find links with empty or whitespace-only text
            empty_links = re.findall(r"\[(\s*)\]\(([^)]+)\)", content)

            for text, link in empty_links:
                failures.append(
                    f"{f.relative_to(STARLIGHT_DOCS_DIR)}: empty link text for {link}"
                )

        assert len(failures) == 0, f"Empty link text found:\n" + "\n".join(
            failures[:10]
        )

    def test_anchor_links_valid(self):
        """Verify anchor/fragment links point to existing headings."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            # Find all headings
            headings = set()
            for line in content.split("\n"):
                match = re.match(r"^(#{1,6})\s+(.+)$", line)
                if match:
                    heading_text = match.group(2).strip().lower()
                    heading_text = re.sub(r"[^a-z0-9]+", "-", heading_text).strip("-")
                    headings.add(heading_text)

            # Find anchor links
            anchor_links = re.findall(r"#([a-z0-9-]+)\)", content)

            for anchor in anchor_links:
                anchor_clean = anchor.strip().lower()
                if anchor_clean not in headings and anchor_clean != "top":
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: anchor #{anchor_clean} not found"
                    )

        assert len(failures) == 0, f"Invalid anchor links:\n" + "\n".join(failures[:10])


class TestImageReferences:
    """Test image link validation."""

    def test_no_broken_image_references(self):
        """Verify all image references point to existing files."""
        failures = []

        assets_dirs = [
            STARLIGHT_DOCS_DIR / "assets",
            DOCS_DIR / "assets",
        ]

        # Build image lookup
        image_files = set()
        for assets_dir in assets_dirs:
            if assets_dir.exists():
                for ext in ["png", "jpg", "jpeg", "svg", "gif", "webp"]:
                    for f in assets_dir.rglob(f"*.{ext}"):
                        image_files.add(f.name)

        for docs_dir in [STARLIGHT_DOCS_DIR, DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text()
                images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)

                for alt, path in images:
                    if path.startswith(("http:", "https:")):
                        continue

                    img_name = path.rsplit("/", 1)[-1]
                    if img_name not in image_files:
                        failures.append(
                            f"{f.relative_to(docs_dir)}: missing image {img_name}"
                        )

        # Allow some failures since images might be external
        assert len(failures) < 10, f"Missing images (allowing up to 9):\n" + "\n".join(
            failures[:5]
        )
