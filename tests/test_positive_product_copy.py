import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PositiveProductCopyTests(unittest.TestCase):
    def test_product_pages_use_affirmative_app_descriptions(self):
        pages = [
            *ROOT.glob("index*.html"),
            *ROOT.glob("features*.html"),
            *ROOT.glob("terms*.html"),
            *ROOT.glob("rating-safety*.html"),
            ROOT / "discover-ja.html",
        ]
        self.assertEqual(len(list(ROOT.glob("index*.html"))), 17)
        self.assertEqual(len(pages), 40)

        banned = (
            "unofficial", "not an official", "not provided or endorsed", "not affiliated",
            "非公式", "公式アプリではありません", "提供・承認するものではありません",
            "non officiel", "n'est pas une application officielle",
            "неофициаль", "не является официальным", "не предоставлено и не одобрено",
            "비공식", "공식 앱이 아닙니다", "no oficial", "no es una app oficial",
            "nieoficjal", "nie jest oficjalną", "neoficiální", "inoffiziell",
            "non ufficial", "não oficial", "ไม่เป็นทางการ", "không chính thức",
            "非官方", "resmi olmayan", "tidak resmi",
        )
        for page in pages:
            text = page.read_text(encoding="utf-8").casefold()
            with self.subTest(page=page.name):
                self.assertFalse([term for term in banned if term.casefold() in text])

    def test_generators_and_shared_stamp_do_not_restore_removed_copy(self):
        paths = [
            ROOT / "scripts" / "generate_pages.py",
            ROOT / "scripts" / "added_locale_copy.py",
            ROOT / "assets" / "styles.css",
        ]
        banned = ("unofficial", "fan-made", "非公式", "非官方", "inoffiziell", "não oficial")
        for path in paths:
            text = path.read_text(encoding="utf-8").casefold()
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse([term for term in banned if term.casefold() in text])

    def test_product_pages_keep_source_and_license_guidance(self):
        pages = [ROOT / "index.html", ROOT / "index-ja.html", ROOT / "terms.html", ROOT / "terms-ja.html"]
        expected = {
            "index.html": ("source page", "licens"),
            "index-ja.html": ("提供元サイト", "ライセンス"),
            "terms.html": ("source", "license"),
            "terms-ja.html": ("参照先", "ライセンス"),
        }
        for page in pages:
            text = page.read_text(encoding="utf-8").casefold()
            with self.subTest(page=page.name):
                for marker in expected[page.name]:
                    self.assertIn(marker.casefold(), text)


if __name__ == "__main__":
    unittest.main()
