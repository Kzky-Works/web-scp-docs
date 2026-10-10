import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_pages
from released_product_copy import COPY


class SearchEntitlementCopyTests(unittest.TestCase):
    def test_every_product_locale_has_released_entitlements(self):
        self.assertEqual(set(COPY), set(generate_pages.LANGS))
        for code, values in COPY.items():
            for kind in ("index", "support"):
                page = ROOT / generate_pages.page_file(kind, code)
                html = page.read_text()
                with self.subTest(locale=code, kind=kind):
                    self.assertIn(values[1].replace("&", "&amp;"), html)
                    self.assertIn(values[2].replace("&", "&amp;"), html)

    def test_japanese_pages_state_the_released_boundary(self):
        for filename in ("index-ja.html", "features-ja.html", "support-ja.html"):
            html = (ROOT / filename).read_text()
            with self.subTest(page=filename):
                self.assertIn("お気に入りは20件、後で読むは100件", html)
                self.assertIn("購読上限はありません", html)
                self.assertIn("10,000", html)
                self.assertIn("メモ検索・自分の記録での絞り込み", html)
                self.assertNotIn("各200件", html)
                self.assertNotIn("検索機能はすべて無料", html)
                self.assertNotIn("NotebookLM", html)
                self.assertNotIn("機械翻訳", html)

    def test_share_content_and_methods_are_named(self):
        html = (ROOT / "features-ja.html").read_text()
        for text in ("6.0.2", "記事URL・タイトル・本文・メモ・ハイライト", "標準の共有", "コピー", "ファイル保存", "登録済みの共有先", "次回も設定を保持"):
            self.assertIn(text, html)

    def test_japanese_discovery_keeps_tag_directory(self):
        html = (ROOT / "discover-ja.html").read_text()
        for text in ('id="tag-filter"', 'id="tag-list"', 'id="tag-show-all"', "タグから探す"):
            self.assertIn(text, html)
