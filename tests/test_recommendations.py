import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCALES = [
    "en", "ja", "fr", "ru", "ko", "es", "pl", "cs", "de", "it", "pt-br",
    "th", "vi", "zh-hans", "zh-hant", "tr",
]


class RecommendationListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recommendations = json.loads(
            (ROOT / "assets" / "recommendations-ja.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "assets" / "discovery-ja.json").read_text(encoding="utf-8")
        )
        cls.catalog_by_id = {article["id"]: article for article in catalog["articles"]}
        cls.catalog_ids = set(cls.catalog_by_id)

    def test_has_at_least_twelve_distinct_themes(self):
        themes = self.recommendations["themes"]
        self.assertGreaterEqual(len(themes), 12)
        self.assertEqual(len({theme["id"] for theme in themes}), len(themes))
        self.assertEqual(len({theme["label"] for theme in themes}), len(themes))

    def test_each_theme_has_ten_to_twenty_catalog_articles(self):
        for theme in self.recommendations["themes"]:
            with self.subTest(theme=theme["id"]):
                article_ids = theme["articleIds"]
                self.assertGreaterEqual(len(article_ids), 10)
                self.assertLessEqual(len(article_ids), 20)
                self.assertEqual(len(article_ids), len(set(article_ids)))
                self.assertEqual(
                    [article_id for article_id in article_ids if article_id not in self.catalog_ids],
                    [],
                )
                for article_id in article_ids:
                    article = self.catalog_by_id[article_id]
                    self.assertTrue(article["url"].startswith("https://"))
                    self.assertTrue(article["openUrl"].startswith("open/?"))

    def test_recommendation_sources_are_named_https_links(self):
        references = self.recommendations["references"]
        self.assertGreaterEqual(len(references), 3)
        for reference in references:
            with self.subTest(reference=reference["label"]):
                self.assertTrue(reference["label"].strip())
                self.assertTrue(reference["url"].startswith("https://"))

    def test_lists_have_an_independent_page(self):
        html = (ROOT / "reading-ja.html").read_text(encoding="utf-8")
        self.assertIn('id="reading-theme-list"', html)
        self.assertIn('id="reading-list-panel"', html)
        self.assertIn('id="reading-list-total"', html)
        self.assertIn('src="assets/reading-lists.js"', html)

    def test_search_and_home_only_show_prominent_list_entry(self):
        discover = (ROOT / "discover-ja.html").read_text(encoding="utf-8")
        home = (ROOT / "index-ja.html").read_text(encoding="utf-8")
        self.assertNotIn('id="reading-theme-list"', discover)
        self.assertIn('class="home-route-entry" href="reading-ja.html"', discover)
        self.assertLess(discover.index('href="reading-ja.html"'), discover.index('class="discovery-console search-console"'))
        self.assertIn('class="home-route-entry" href="reading-ja.html"', home)

    def test_detailed_search_and_theme_reading_have_equal_weight(self):
        for filename in ["index-ja.html", "discover-ja.html"]:
            with self.subTest(filename=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                self.assertEqual(html.count('class="home-route-entry"'), 2)
                self.assertIn("条件を指定して詳しく探す", html)
                self.assertIn("テーマで読む", html)

    def test_japanese_generator_preserves_the_home_entry(self):
        source = (ROOT / "scripts" / "generate_pages.py").read_text(encoding="utf-8")
        self.assertIn('class="home-route-entry" href="reading-ja.html"', source)


class LocalizedRecommendationListTests(unittest.TestCase):
    def test_every_locale_has_an_independent_page_and_entry(self):
        for locale in LOCALES:
            suffix = "" if locale == "en" else f"-{locale}"
            reading = ROOT / f"reading{suffix}.html"
            index = ROOT / ("index.html" if locale == "en" else f"index-{locale}.html")
            with self.subTest(locale=locale):
                self.assertTrue(reading.exists())
                reading_html = reading.read_text(encoding="utf-8")
                self.assertIn('id="reading-theme-list"', reading_html)
                self.assertIn(f'data-reading-assets="{locale}"', reading_html)
                self.assertIn(f'href="reading{suffix}.html"', index.read_text(encoding="utf-8"))

    def test_every_non_japanese_locale_has_ten_curated_themes(self):
        signatures = set()
        for locale in [value for value in LOCALES if value != "ja"]:
            with self.subTest(locale=locale):
                payload = json.loads((ROOT / "assets" / f"recommendations-{locale}.json").read_text(encoding="utf-8"))
                themes = payload["themes"]
                article_ids = {article["id"] for article in payload["articles"]}
                self.assertEqual(len(themes), 10)
                self.assertGreaterEqual(len(payload["references"]), 3)
                for theme in themes:
                    self.assertGreaterEqual(len(theme["articleIds"]), 10)
                    self.assertLessEqual(len(theme["articleIds"]), 20)
                    self.assertEqual(len(theme["articleIds"]), len(set(theme["articleIds"])))
                    self.assertTrue(set(theme["articleIds"]).issubset(article_ids))
                    self.assertTrue(theme["label"].strip())
                    self.assertTrue(theme["description"].strip())
                signatures.add(tuple(theme["id"] for theme in themes))
        self.assertGreaterEqual(len(signatures), 10)


if __name__ == "__main__":
    unittest.main()
