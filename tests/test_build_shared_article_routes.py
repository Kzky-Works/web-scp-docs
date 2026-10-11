from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_shared_article_routes as subject


class SharedArticleRouteTests(unittest.TestCase):
    def test_route_id_matches_the_ios_contract(self) -> None:
        self.assertEqual(
            subject.route_id("HTTP://SCP-WIKI.WIKIDOT.COM/scp-173/"),
            "a3ecd8849da128f3d092c004",
        )

    def test_builds_all_supported_language_route_and_rejects_unknown_hosts(self) -> None:
        payload = {
            "entries": [
                {
                    "sourceURL": "https://scp-wiki.wikidot.com/scp-173",
                    "original": {"language": "EN", "url": "https://scp-wiki.wikidot.com/scp-173"},
                    "versions": [
                        {"language": language, "url": url}
                        for language, url in {
                            "EN": "https://scp-wiki.wikidot.com/scp-173",
                            "ES": "https://lafundacionscp.wikidot.com/scp-173",
                            "FR": "https://fondationscp.wikidot.com/scp-173",
                            "JP": "https://scp-jp.wikidot.com/scp-173",
                            "KO": "https://scpko.wikidot.com/scp-173",
                            "PL": "https://scp-pl.wikidot.com/scp-173",
                            "RU": "https://scpfoundation.net/scp-173",
                            "CN": "https://scp-wiki-cn.wikidot.com/scp-173",
                            "TH": "https://scp-th.wikidot.com/scp-173",
                            "DE": "https://scp-wiki-de.wikidot.com/scp-173",
                            "IT": "https://fondazionescp.wikidot.com/scp-173",
                            "PT": "https://scp-pt-br.wikidot.com/scp-173",
                            "VN": "https://scp-vn.wikidot.com/scp-173",
                            "CS": "https://scp-cs.wikidot.com/scp-173",
                            "ZH-TR": "https://scp-zh-tr.wikidot.com/scp-173",
                            "TR": "https://scpvakfi.wikidot.com/scp-173",
                            "ID": "https://scp-id.wikidot.com/scp-173",
                            "EVIL": "https://evil.example/scp-173",
                        }.items()
                    ],
                }
            ]
        }

        routes = subject.build_routes(payload)
        route = routes["a3ecd8849da128f3d092c004"]

        self.assertEqual(list(route["versions"]), list(subject.ALLOWED_LANGUAGES))
        self.assertEqual(route["versions"]["TH"], "http://scp-th.wikidot.com/scp-173")
        self.assertNotIn("EVIL", route["versions"])

    def test_italian_original_and_existing_route_id_are_preserved(self) -> None:
        source = "https://scp-int.wikidot.com/scp-020-it"
        original = "https://fondazionescp.wikidot.com/scp-020-it"
        route = subject.build_routes({"entries": [{"sourceURL": source,
            "original": {"language": "IT", "url": original},
            "versions": [{"language": "EN", "url": source}, {"language": "IT", "url": original}]
        }]})["036e1e5b862dad3c8600d9f4"]
        self.assertEqual(route["original"], {"language": "IT", "url": original})
        self.assertEqual(route["versions"]["IT"], original)

    def test_missing_original_is_not_replaced_and_versions_are_not_invented(self) -> None:
        source = "https://scp-int.wikidot.com/scp-020-it"
        for original in ({}, {"language": "IT", "url": "https://evil.example/scp-020-it"}):
            route = subject.build_routes({"entries": [{"sourceURL": source,
                "original": original, "versions": []}]})[subject.route_id(source)]
            self.assertEqual(route["original"]["url"], "")
            self.assertEqual(route["versions"], {})

    def test_portuguese_alias_and_chinese_identity_are_separate(self) -> None:
        source = "https://scp-wiki.wikidot.com/scp-173"
        route = subject.build_routes({"entries": [{"sourceURL": source,
            "versions": [{"language": "PT/BR", "url": "https://scp-pt-br.wikidot.com/scp-173"},
                         {"language": "ZH-TR", "url": "https://scp-zh-tr.wikidot.com/scp-173"}]
        }]})[subject.route_id(source)]
        self.assertIn("PT", route["versions"])
        self.assertIn("ZH-TR", route["versions"])
        self.assertNotIn("CN", route["versions"])

    def test_writes_hash_prefix_shards(self) -> None:
        routes = {
            "a3ecd8849da128f3d092c004": {
                "sourceURL": "https://scp-wiki.wikidot.com/scp-173",
                "original": {"language": "EN", "url": "https://scp-wiki.wikidot.com/scp-173"},
                "versions": {"EN": "https://scp-wiki.wikidot.com/scp-173"},
            }
        }
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            subject.write_shards(routes, output, "2026-07-20T00:00:00Z")

            shard = json.loads((output / "a3.json").read_text(encoding="utf-8"))
            index = json.loads((output / "index.json").read_text(encoding="utf-8"))

        self.assertIn("a3ecd8849da128f3d092c004", shard["routes"])
        self.assertEqual(index["routeCount"], 1)

    def test_adds_japanese_catalog_articles_as_direct_routes(self) -> None:
        routes: dict[str, dict] = {}
        catalog = {
            "articles": [
                {"id": "scp-178-jp", "url": "https://scp-jp.wikidot.com/scp-178-jp"},
                {"id": "invalid", "url": "https://example.com/not-official"},
            ]
        }

        subject.add_catalog_routes(routes, catalog, "JP")

        identifier = subject.route_id("https://scp-jp.wikidot.com/scp-178-jp")
        self.assertEqual(
            routes[identifier],
            {
                "sourceURL": "https://scp-jp.wikidot.com/scp-178-jp",
                "original": {
                    "language": "JP",
                    "url": "https://scp-jp.wikidot.com/scp-178-jp",
                },
                "versions": {"JP": "https://scp-jp.wikidot.com/scp-178-jp"},
            },
        )
        self.assertEqual(len(routes), 1)


if __name__ == "__main__":
    unittest.main()
