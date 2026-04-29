# web-scp-docs（GitHub Pages / 法務・紹介サイト）

このフォルダはリポジトリ **[Kzky-Works/web-scp-docs](https://github.com/Kzky-Works/web-scp-docs)** の **ローカル clone** です。**原本は常に GitHub の `main`** であり、ここを編集したら **`git push`** して反映します。親リポ（`app-scp-docs`）の `main` とは **別の Git 履歴**です（親側の `.gitignore` でこのパスは無視されます）。

## サイトの役割

| ページ | URL 例（Project Pages） | 用途 |
|--------|-------------------------|------|
| トップ | `https://kzky-works.github.io/web-scp-docs/` | **アプリ紹介**・ディスクレーマー・各ページへの導線。**Marketing URL（任意）** にもそのまま使える |
| プライバシー（日本語） | `.../privacy.html` | **App Store Connect の Privacy Policy URL** 候補 |
| プライバシー（英語） | `.../privacy-en.html` | グローバル向け補助 URL |
| サポート | `.../support.html` | **サポート URL** |
| 利用規約 | `.../terms.html` | 非公式性・CC・免責など |

ルートの **`.nojekyll`** は Jekyll を無効にし、`assets/` をそのまま配信するためです。

## ワークフロー（このフォルダだけで完了）

```bash
# 変更後
git add -A
git status
git commit -m "docs: ..."
git push origin main
```

初回のみ: 親フォルダ `scp_docs/` で `git clone https://github.com/Kzky-Works/web-scp-docs.git web-scp-docs`（既にあれば不要）。

GitHub **Settings → Pages**: **Deploy from a branch** — **`main`** / **`/ (root)`**。

反映まで数十秒〜数分。強制再読込で確認すること。

### 親リポ `app-scp-docs` と二重コミットはしない

- サイトの **`git`** は **`web-scp-docs` のリモートだけ**向ける。
- iOS アプリの URL を変えた場合のみ、親リポで `Constants.swift` とローカライズを更新してコミットする。

## App Store Connect（ASC）チェックリスト

| 項目 | 例 |
|------|-----|
| Privacy Policy URL | `https://kzky-works.github.io/web-scp-docs/privacy.html` または `privacy-en.html` |
| Support URL | `.../support.html` |
| Marketing URL（任意） | トップ |
| アプリのプライバシーに関する質問 | このサイト本文と実装を一致させる |

## アプリとの対応

[`../../ScpDocs/ScpDocs/Sources/Core/Constants.swift`](../../ScpDocs/ScpDocs/Sources/Core/Constants.swift) の `AppLegalURLs`。プライバシー文言は **`HomeViewModel.resolvedPrivacyPolicyWebURL`** で `privacy.html` / `privacy-en.html` に切り替わります。

## 連絡先の変更

`scpdocs_admin@proton.me` を変えるときは、各 HTML のフッターと `support.html` を置換後、`git push`。
