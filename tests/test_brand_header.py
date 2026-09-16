import hashlib
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCALIZED_INDEX_PAGES = [
    "index.html", "index-ja.html", "index-fr.html", "index-ru.html", "index-ko.html",
    "index-es.html", "index-pl.html", "index-cs.html", "index-de.html", "index-it.html",
    "index-pt-br.html", "index-th.html", "index-vi.html", "index-zh-hans.html",
    "index-zh-hant.html", "index-tr.html",
]


class BrandHeaderTests(unittest.TestCase):
    def test_every_language_uses_the_logo_lockup(self):
        for page in LOCALIZED_INDEX_PAGES:
            with self.subTest(page=page):
                html = (ROOT / page).read_text(encoding="utf-8")
                self.assertIn('class="site-brand"', html)
                self.assertIn('src="assets/images/app-icon-6.0.0.png"', html)
                self.assertIn('<strong>SCP</strong><span>docs</span>', html)
                self.assertIn('READER / CATALOG', html)

    def test_web_icon_matches_the_current_app_icon_canon(self):
        data = (ROOT / "assets" / "images" / "app-icon-6.0.0.png").read_bytes()
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "d9ba231ac5b74c6cc22538c2f8135e1618fb0aae89c0a58e14d18d8419dafb92",
        )
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1024, 1024))

    def test_generator_preserves_the_global_logo_and_icon(self):
        source = (ROOT / "scripts" / "generate_pages.py").read_text(encoding="utf-8")
        self.assertIn('class="site-brand" href="{home}"', source)
        self.assertIn('favicon = "assets/images/app-icon-6.0.0.png"', source)


if __name__ == "__main__":
    unittest.main()
