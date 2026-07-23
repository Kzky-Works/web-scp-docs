# web-scp-docs（GitHub Pages / 法務・紹介サイト）

このフォルダはリポジトリ **[Kzky-Works/web-scp-docs](https://github.com/Kzky-Works/web-scp-docs)** の **ローカル clone** です。**原本は常に GitHub の `main`** であり、ここを編集したら **`git push`** して反映します。親リポ（`app-scp-docs`）の `main` とは **別の Git 履歴**です（親側の `.gitignore` でこのパスは無視されます）。

## サイトの役割

| ページ | URL 例（Project Pages） | 用途 |
|--------|-------------------------|------|
| トップ（英語・既定） | `https://kzky-works.github.io/web-scp-docs/` | **アプリ紹介**・ディスクレーマー・各ページへの導線。**Marketing URL（任意）** にもそのまま使える |
| トップ（日本語） | `.../index-ja.html` | 日本語版トップ |
| トップ（フランス語） | `.../index-fr.html` | フランス語版トップ |
| トップ（ロシア語） | `.../index-ru.html` | ロシア語版トップ |
| トップ（韓国語） | `.../index-ko.html` | 韓国語版トップ |
| トップ（スペイン語） | `.../index-es.html` | スペイン語版トップ |
| トップ（ポーランド語） | `.../index-pl.html` | ポーランド語版トップ |
| 機能紹介（英語・既定） | `.../features.html` | スクリーンショット付きの簡単な機能紹介 |
| 機能紹介（日本語） | `.../features-ja.html` | 日本語版機能紹介 |
| 機能紹介（フランス語） | `.../features-fr.html` | フランス語版機能紹介 |
| 機能紹介（ロシア語） | `.../features-ru.html` | ロシア語版機能紹介 |
| 機能紹介（韓国語） | `.../features-ko.html` | 韓国語版機能紹介 |
| 機能紹介（スペイン語） | `.../features-es.html` | スペイン語版機能紹介 |
| 機能紹介（ポーランド語） | `.../features-pl.html` | ポーランド語版機能紹介 |
| App Store | `https://apps.apple.com/jp/app/scp-docs/id6765882660` | 公開中の iOS アプリページ |
| プライバシー（英語・既定） | `.../privacy.html` | **App Store Connect の Privacy Policy URL** 候補 |
| プライバシー（日本語） | `.../privacy-ja.html` | 日本語版プライバシーポリシー |
| プライバシー（フランス語） | `.../privacy-fr.html` | フランス語版プライバシーポリシー |
| プライバシー（ロシア語） | `.../privacy-ru.html` | ロシア語版プライバシーポリシー |
| プライバシー（韓国語） | `.../privacy-ko.html` | 韓国語版プライバシーポリシー |
| プライバシー（スペイン語） | `.../privacy-es.html` | スペイン語版プライバシーポリシー |
| プライバシー（ポーランド語） | `.../privacy-pl.html` | ポーランド語版プライバシーポリシー |
| サポート（英語・既定） | `.../support.html` | **サポート URL** |
| サポート（日本語） | `.../support-ja.html` | 日本語版サポート |
| サポート（フランス語） | `.../support-fr.html` | フランス語版サポート |
| サポート（ロシア語） | `.../support-ru.html` | ロシア語版サポート |
| サポート（韓国語） | `.../support-ko.html` | 韓国語版サポート |
| サポート（スペイン語） | `.../support-es.html` | スペイン語版サポート |
| サポート（ポーランド語） | `.../support-pl.html` | ポーランド語版サポート |
| 利用規約（英語・既定） | `.../terms.html` | 非公式性・CC・免責など |
| 利用規約（日本語） | `.../terms-ja.html` | 日本語版利用規約 |
| 利用規約（フランス語） | `.../terms-fr.html` | フランス語版利用規約 |
| 利用規約（ロシア語） | `.../terms-ru.html` | ロシア語版利用規約 |
| 利用規約（韓国語） | `.../terms-ko.html` | 韓国語版利用規約 |
| 利用規約（スペイン語） | `.../terms-es.html` | スペイン語版利用規約 |
| 利用規約（ポーランド語） | `.../terms-pl.html` | ポーランド語版利用規約 |
| Rating & Safety Policy（英語・既定） | `.../rating-safety.html` | **ASC の年齢適合性URL（任意）** 候補 |
| Rating & Safety Policy（日本語） | `.../rating-safety-ja.html` | 日本語版安全方針 |
| Rating & Safety Policy（フランス語） | `.../rating-safety-fr.html` | フランス語版安全方針 |
| Rating & Safety Policy（ロシア語） | `.../rating-safety-ru.html` | ロシア語版安全方針 |
| Rating & Safety Policy（韓国語） | `.../rating-safety-ko.html` | 韓国語版安全方針 |
| Rating & Safety Policy（スペイン語） | `.../rating-safety-es.html` | スペイン語版安全方針 |
| Rating & Safety Policy（ポーランド語） | `.../rating-safety-pl.html` | ポーランド語版安全方針 |

ルートの **`.nojekyll`** は Jekyll を無効にし、`assets/` をそのまま配信するためです。

## 言語構成

- サイトの既定言語は英語。ルートの `index.html` と主要ナビは英語ページへ向ける。
- 英語・既定ページは拡張子前の言語サフィックスなし、日本語版は `*-ja.html` に統一する。
- フランス語版は `*-fr.html` に統一する。
- ロシア語版は `*-ru.html` に統一する。
- 韓国語版は `*-ko.html` に統一する。
- スペイン語版は `*-es.html` に統一する。
- ポーランド語版は `*-pl.html` に統一する。
- サイト用のスペイン語・ポーランド語スクリーンショットは未収録のため、両言語ページでは英語版 `*-en.png` を流用する。
- 旧英語 URL の `privacy-en.html` / `terms-en.html` は外部リンク保護用のリダイレクトとしてだけ残す。
- すべての公開ページの共通ヘッダーに `.language-switch` を置き、英語・日本語・フランス語・ロシア語・韓国語・スペイン語・ポーランド語を切り替えられるようにする。

## ページ生成

主要 HTML は `scripts/generate_pages.py` で生成する。全言語の `hreflang`、Open Graph locale、右上の言語切替、本文の機能説明を同時に更新するため、本文や言語行列を変えるときはスクリプトを更新してから再生成する。

```bash
python3 scripts/generate_pages.py
```

## 記事共有リンク

X などには `https://scpdocs.link/open/?id=...&source=...` を 1 本だけ載せる。`open/` は端末言語または前回選択した言語に対応する公式支部記事へ振り分ける。iOS ではユーザーが押す `scpdocs://` リンク、公式 Wiki、App Storeの3導線を同じ画面に表示する。自動アプリ起動や自動App Store転送は行わない。

- `.well-known/apple-app-site-association`: `com.kzkyworks.scpdocs` の `/open/*` を関連付ける。
- `launch/`: 既存URL保護用の静的ページ。自動遷移はせず、アプリ、App Store、記事選択画面への明示リンクだけを表示する。
- `scripts/build_shared_article_routes.py`: 公開済み `manifest_daily_scp_translations.json` を 2 桁 hash prefix の小さな `routes/*.json` に分割する。
- `.github/workflows/deploy-pages.yml`: push と毎日 05:17 JST に route shard を再生成し、GitHub Pages へ無料配信する。
- Repository variable `SCPDOCS_CUSTOM_DOMAIN=scpdocs.link` を設定すると、deploy artifact に `CNAME` を追加する。

## ワークフロー（このフォルダだけで完了）

```bash
# 変更後
python3 scripts/generate_pages.py
git add -A
git status
git commit -m "docs: ..."
git push origin main
```

初回のみ: wrapper `SCP-docs/` 直下で `git clone https://github.com/Kzky-Works/web-scp-docs.git web-scp-docs`（既にあれば不要）。

GitHub **Settings → Pages → Build and deployment → Source**: **GitHub Actions**。独自ドメイン導入時は、先にPagesのCustom domainへ追加してからDNSを設定し、リポジトリ変数 `SCPDOCS_CUSTOM_DOMAIN` も同じ値にする。

反映まで数十秒〜数分。強制再読込で確認すること。

### 親リポ `app-scp-docs` と二重コミットはしない

- サイトの **`git`** は **`web-scp-docs` のリモートだけ**向ける。
- iOS アプリの URL を変えた場合のみ、親リポで `Constants.swift` とローカライズを更新してコミットする。

## App Store Connect（ASC）チェックリスト

| 項目 | 例 |
|------|-----|
| Privacy Policy URL | `https://kzky-works.github.io/web-scp-docs/privacy.html` |
| Support URL | `.../support.html` |
| Marketing URL（任意） | トップ |
| App Store URL | `https://apps.apple.com/jp/app/scp-docs/id6765882660` |
| 年齢適合性URL（任意） | `.../rating-safety.html` |
| アプリのプライバシーに関する質問 | このサイト本文と実装を一致させる |

## アプリとの対応

[`../../ScpDocs/ScpDocs/Sources/Core/Constants.swift`](../../ScpDocs/ScpDocs/Sources/Core/Constants.swift) の `AppLegalURLs`。アプリ側も、英語・既定は `privacy.html` / `terms.html`、日本語は `privacy-ja.html` / `terms-ja.html` に合わせる。

## 連絡先の変更

`scpdocs_admin@proton.me` または `@SCPdocs` を変えるときは、各 HTML のフッターと `support.html` を置換後、`git push`。
