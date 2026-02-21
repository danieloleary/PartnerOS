"""Tests for deployed site link correctness."""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = REPO_ROOT / "partneros-docs" / "dist"
DOCS_DIR = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"


class TestDeployedLinks:
    """Verify links work correctly in deployed site."""

    def test_dist_directory_exists(self):
        """Verify dist directory exists (run build first)."""
        assert DIST_DIR.exists(), "Run 'npm run build' first"

    def test_no_absolute_partneros_links_in_source(self):
        """Verify source docs don't use hardcoded /PartnerOS/ links."""
        failures = []

        for f in DOCS_DIR.rglob("*.md"):
            content = f.read_text()
            matches = re.findall(r"\]\(/PartnerOS/[^)]+\)", content)
            if matches:
                rel_path = f.relative_to(DOCS_DIR)
                failures.append(f"{rel_path}: {matches}")

        for f in DOCS_DIR.rglob("*.mdx"):
            content = f.read_text()
            matches = re.findall(r"\]\(/PartnerOS/[^)]+\)", content)
            if matches:
                rel_path = f.relative_to(DOCS_DIR)
                failures.append(f"{rel_path}: {matches}")

        assert len(failures) == 0, (
            f"Found absolute /PartnerOS links in source (use relative links instead):\n"
            + "\n".join(failures)
        )

    def test_relative_links_in_built_site(self):
        """Verify built site uses relative links for navigation."""
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Hero actions should NOT have /PartnerOS/ in the href
        # They should be relative (e.g., /getting-started/quick-start/)
        # Starlight automatically handles the base URL
        assert 'href="/PartnerOS/getting-started/' not in content, (
            "Hero links should NOT have /PartnerOS/ prefix in built HTML"
        )
        assert 'href="/PartnerOS/strategy/' not in content, (
            "Hero links should NOT have /PartnerOS/ prefix in built HTML"
        )

    def test_base_url_config_present(self):
        """Verify astro.config.mjs has correct site and base configuration."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "base:" in content, "Missing base URL config"
        assert "site:" in content, "Missing site URL config"
        assert "/PartnerOS" in content, "base should be set to /PartnerOS"

    def test_build_produces_valid_html(self):
        """Verify build produces valid HTML with correct base."""
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Should have correct base path in assets
        assert "/PartnerOS/_astro/" in content, (
            "Assets should reference /PartnerOS/_astro/"
        )

    def test_assets_use_base_url(self):
        """Verify CSS/JS assets use the base URL."""
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Find asset references
        astro_assets = re.findall(r'href="(/PartnerOS/_astro/[^"]+)"', content)
        assert len(astro_assets) > 0, "Should have Astro assets with base URL"
