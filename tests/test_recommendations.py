import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RecommendationListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recommendations = json.loads(
            (ROOT / "assets" / "recommendations-ja.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "assets" / "discovery-ja.json").read_text(encoding="utf-8")
        )
        cls.catalog_ids = {article["id"] for article in catalog["articles"]}

    def test_has_ten_distinct_themes(self):
        themes = self.recommendations["themes"]
        self.assertEqual(len(themes), 10)
        self.assertEqual(len({theme["id"] for theme in themes}), 10)
        self.assertEqual(len({theme["label"] for theme in themes}), 10)

    def test_each_theme_has_ten_to_thirty_catalog_articles(self):
        for theme in self.recommendations["themes"]:
            with self.subTest(theme=theme["id"]):
                article_ids = theme["articleIds"]
                self.assertGreaterEqual(len(article_ids), 10)
                self.assertLessEqual(len(article_ids), 30)
                self.assertEqual(len(article_ids), len(set(article_ids)))
                self.assertEqual(
                    [article_id for article_id in article_ids if article_id not in self.catalog_ids],
                    [],
                )

    def test_recommendation_sources_are_named_https_links(self):
        references = self.recommendations["references"]
        self.assertGreaterEqual(len(references), 3)
        for reference in references:
            with self.subTest(reference=reference["label"]):
                self.assertTrue(reference["label"].strip())
                self.assertTrue(reference["url"].startswith("https://"))

    def test_lists_are_before_the_search_console(self):
        html = (ROOT / "discover-ja.html").read_text(encoding="utf-8")
        self.assertLess(html.index('class="reading-lists"'), html.index('class="discovery-console search-console"'))
        self.assertIn('id="reading-theme-list"', html)
        self.assertIn('id="reading-list-panel"', html)


if __name__ == "__main__":
    unittest.main()
