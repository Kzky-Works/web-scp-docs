from __future__ import annotations

import base64
import hashlib
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_discovery_catalog as subject


class DiscoveryCatalogTests(unittest.TestCase):
    def test_mode_assignment_uses_real_reading_dimensions(self) -> None:
        modes = subject._modes(
            "Tale",
            score=150,
            characters=2_500,
            created_at=1_700_000_000,
            tags={"ホラー", "異次元"},
        )

        self.assertEqual(
            modes,
            ["popular", "short", "eerie", "strange", "world", "recent"],
        )

    def test_open_link_binds_the_route_id_to_the_official_url(self) -> None:
        url = "https://scp-jp.wikidot.com/scp-173"
        open_url = subject._route_url(url)
        query = parse_qs(urlparse(open_url).query)

        self.assertEqual(query["id"][0], hashlib.sha256(url.encode()).hexdigest()[:24])
        encoded = query["source"][0]
        decoded = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode()
        self.assertEqual(decoded, url)


if __name__ == "__main__":
    unittest.main()
