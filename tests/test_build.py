"""Tests for build and deployment."""

import subprocess
import pytest
from pathlib import Path
from tests.conftest import REPO_ROOT


class TestStarlightBuild:
    """Test Starlight (Astro) build process."""

    def test_starlight_build_succeeds(self):
        """Verify Starlight build completes without errors."""
        starlight_dir = REPO_ROOT / "partneros-docs"

        if not starlight_dir.exists():
            pytest.skip("partneros-docs not found")

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(starlight_dir),
            capture_output=True,
            text=True,
            timeout=300,
        )

        assert result.returncode == 0, f"Build failed:\n{result.stderr}"

    def test_starlight_dist_exists(self):
        """Verify build output directory exists."""
        dist_dir = REPO_ROOT / "partneros-docs" / "dist"

        if not dist_dir.exists():
            pytest.skip("dist directory not found (run build first)")

        assert dist_dir.exists(), "Starlight dist/ directory should exist"
        assert (dist_dir / "index.html").exists(), "index.html should exist"

    def test_starlight_package_json_valid(self):
        """Verify package.json is valid JSON."""
        import json

        package_path = REPO_ROOT / "partneros-docs" / "package.json"
        assert package_path.exists(), "package.json not found"

        with open(package_path) as f:
            data = json.load(f)

        assert "scripts" in data, "package.json should have scripts"
        assert "build" in data["scripts"], "package.json should have build script"


class TestConfiguration:
    """Test configuration files."""

    def test_astro_config_valid(self):
        """Verify astro.config.mjs is valid."""
        astro_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        assert astro_path.exists(), "astro.config.mjs not found"

        content = astro_path.read_text()

        assert "starlight" in content, "astro.config.mjs should configure starlight"
        assert "base:" in content, "astro.config.mjs should have base URL"

    def test_social_links_valid(self):
        """Verify social links in config are valid URLs."""
        astro_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = astro_path.read_text()

        # Extract URLs from social config
        import re

        urls = re.findall(r'href:\s*["\']([^"\']+)["\']', content)

        for url in urls:
            if url.startswith("http"):
                assert url.startswith("https://"), (
                    f"Social link should use HTTPS: {url}"
                )
