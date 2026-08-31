import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AnalyticsIntegrationTests(unittest.TestCase):
    def test_main_generated_pages_load_privacy_first_analytics(self) -> None:
        pages = sorted(ROOT.glob("index*.html"))
        pages += sorted(ROOT.glob("reading*.html"))
        pages += sorted(ROOT.glob("privacy*.html"))
        pages += sorted(ROOT.glob("support*.html"))
        pages += sorted(ROOT.glob("features*.html"))
        pages += [ROOT / "discover-ja.html"]

        redirects = {"privacy-en.html"}
        checked = 0
        for page in pages:
            if page.name in redirects:
                continue
            self.assertIn(
                '<script src="assets/analytics.js?v=20260831-1" defer></script>',
                page.read_text(encoding="utf-8"),
                page.name,
            )
            checked += 1
        self.assertGreaterEqual(checked, 60)

    def test_every_localized_privacy_page_discloses_google_analytics(self) -> None:
        pages = [page for page in sorted(ROOT.glob("privacy*.html")) if page.name != "privacy-en.html"]
        self.assertEqual(len(pages), 17)
        for page in pages:
            self.assertIn("Google Analytics", page.read_text(encoding="utf-8"), page.name)


if __name__ == "__main__":
    unittest.main()
