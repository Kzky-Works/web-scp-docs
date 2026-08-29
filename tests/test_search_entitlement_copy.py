import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_pages  # noqa: E402


class SearchEntitlementCopyTests(unittest.TestCase):
    def test_support_copy_uses_free_search_entitlement_in_every_locale(self) -> None:
        self.assertEqual(
            set(generate_pages.SEARCH_SUPPORT_COPY),
            set(generate_pages.LANGS),
        )
        for code, (premium_answer, saved_search_answer) in generate_pages.SEARCH_SUPPORT_COPY.items():
            with self.subTest(locale=code):
                self.assertEqual(
                    generate_pages.SUPPORT_TEXT[code]["faqs"][4][1],
                    premium_answer,
                )
                self.assertEqual(
                    generate_pages.SUPPORT_TEXT[code]["faqs"][7][1],
                    saved_search_answer,
                )

    def test_full_locale_comparison_marks_search_free(self) -> None:
        for code, comparison in generate_pages.FEATURE_CMP.items():
            with self.subTest(locale=code):
                self.assertEqual(comparison["rows"][0][1:], ("yes", "yes"))
                self.assertEqual(comparison["rows"][6][1:], ("yes", "yes"))

    def test_japanese_pages_state_the_current_boundary(self) -> None:
        index_html = (ROOT / "index-ja.html").read_text(encoding="utf-8")
        features_html = (ROOT / "features-ja.html").read_text(encoding="utf-8")
        support_html = (ROOT / "support-ja.html").read_text(encoding="utf-8")

        self.assertIn("検索機能はすべて無料です", index_html)
        self.assertIn("すべて無料の高機能検索", features_html)
        self.assertIn("保存検索と新着通知は無料です", support_html)
        self.assertNotIn("保存検索はプレミアム機能です", support_html)


if __name__ == "__main__":
    unittest.main()
