from __future__ import annotations

import base64
import hashlib
import json
import sys
import tempfile
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

    def test_object_class_uses_known_tag(self) -> None:
        self.assertEqual(subject._object_class({"jp", "keter", "建造物"}), "keter")
        self.assertIsNone(subject._object_class({"jp", "建造物"}))

    def test_catalog_keeps_searchable_articles_without_discovery_modes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            branch_dir = Path(directory)
            for filename in subject.MANIFESTS:
                entries = []
                metadata = {}
                if filename == "manifest_scp-jp.json":
                    entries = [
                        {"i": "scp-999-jp", "t": "検索できる記事", "u": "https://scp-jp.wikidot.com/scp-999-jp"},
                    ]
                    metadata = {
                        "scp-999-jp": {"os": 0, "cc": 120, "g": ["safe", "jp"]},
                    }
                (branch_dir / filename).write_text(
                    json.dumps({"generatedAt": "2026-08-30T00:00:00Z", "entries": entries, "metadata": metadata}),
                    encoding="utf-8",
                )

            catalog = subject.build_catalog(branch_dir)

        self.assertEqual(catalog["schemaVersion"], 2)
        self.assertEqual(catalog["articleCount"], 1)
        self.assertEqual(catalog["articles"][0]["id"], "scp-999-jp")
        self.assertEqual(catalog["articles"][0]["modes"], [])
        self.assertEqual(catalog["articles"][0]["objectClass"], "safe")


if __name__ == "__main__":
    unittest.main()
