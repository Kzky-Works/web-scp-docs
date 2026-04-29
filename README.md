# web-scp-docs（GitHub Pages / 法務・紹介サイト）

このディレクトリは **公開ウェブサイト** の元データ置き場です。**原本としての正** は GitHub **`Kzky-Works/web-scp-docs`（あるいは `kzky-works/web-scp-docs` の実体リポジトリ）の `main`** にマージ済みであることとします。このリポから未 push のみの変更がある場合、その内容はドラフト状態です。

## サイトの役割

| ページ | URL 例（Project Pages） | 用途 |
|--------|-------------------------|------|
| トップ | `https://kzky-works.github.io/web-scp-docs/` | **アプリ紹介**（本文の中心）・ディスクレーマー・各ページへの導線。**Marketing URL（任意）** にもそのまま使える |
| プライバシー（日本語） | `.../privacy.html` | **App Store Connect の Privacy Policy URL** 候補（日本ユーザー向け） |
| プライバシー（英語） | `.../privacy-en.html` | グローバル向けレビュワー／英語 UI のユーザー。**ASC の Privacy に日本語のみ貼ってもよい**。英語版は補助 |
| サポート | `.../support.html` | **サポート URL**（問い合わせメール・FAQ） |
| 利用規約 | `.../terms.html` | 非公式ファンソフトウェアとしての説明・免責 |

ルートには **`.nojekyll`**（空ファイル）を置いてあります。Jekyll によるビルドを無効にし、`assets/` をそのまま配信させます。

## デプロイ手順（scp_docs → GitHub）

1. このリポ（`scp_docs`）で `contrib/web-scp-docs` を編集し、コミットする。
2. 公開用の **`web-scp-docs` リポジトリ**を clone した作業ディレクトリで、**ルートに上書きコピー**する（下記 `rsync` 例）。
3. `web-scp-docs` 側で `git add` → `commit` → `origin main` へ **`git push`**。
4. GitHub **Settings → Pages**: **Deploy from a branch** — **`main`** の **`/ (root)`**（初回のみ設定）。

反映まで数十秒〜数分。**Actions** タブに Pages のデプロイが出る環境では、完了ログを確認。

### rsync の例（macOS / Linux）

`WEBSCP_DOCS` を `web-scp-docs` リポジトリの clone 先に置き換える:

```bash
CONTRIB="/Volumes/SSD_External/AppDev/Projects/SCP-docs/scp_docs/contrib/web-scp-docs"
WEBSCP_DOCS="$HOME/Developer/web-scp-docs"   # 例

rsync -av --delete \
  "$CONTRIB/" \
  "$WEBSCP_DOCS/"

cd "$WEBSCP_DOCS" || exit
git add -A
git status
git commit -m "Sync site from scp_docs contrib/web-scp-docs"
git push origin main
```

`--delete` は publish 先にしかないファイルを消すため、**意図した静的ファイルだけ**が残るようにする。初回 clone に余計なファイルがある場合は手で整理してから。

### プライベートリポジトリで Pages を使う場合

Organization のプランや設定によっては **Public リポジトリ + Pages** が簡単なことが多い。Public のままなら、上記 URL はそのまま利用可能。

## App Store Connect（ASC）で使うチェックリスト

審査・ストア掲載でよく求められる対応。

| 項目 | 例（このサイト） | メモ |
|------|------------------|------|
| **Privacy Policy URL** | `https://kzky-works.github.io/web-scp-docs/privacy.html` または `.../privacy-en.html` | **HTTPS**・審査時に開けること。本文はアプリの実データ取扱と一致させる |
| **Support URL** | `https://kzky-works.github.io/web-scp-docs/support.html` | 問い合わせ先が記載されていること |
| **Marketing URL（任意）** | `https://kzky-works.github.io/web-scp-docs/` | 未設定でも可。アプリ紹介を載せるならトップ |
| **アプリのプライバシーに関する質問** | App Store Connect のフォーム | **サイトの記載と矛盾しない**こと（AdMob・課金・端末内データ等） |

App 内の設定画面は [`AppLegalURLs`](../../ScpDocs/ScpDocs/Sources/Core/Constants.swift) と **プライバシーは UI 言語に応じて** `privacy.html` / `privacy-en.html` を切替（`HomeViewModel.resolvedPrivacyPolicyWebURL`）。

## アプリとの対応

iOS アプリは `AppLegalURLs`（`website`・`privacyPolicy`・`privacyPolicyEnglish`・`support`・`termsOfUse`）および設定のリンク文言（`LocalizationKey.settingsWebsiteLink` 等）で上記と揃える。ウェブでパスを変えたら **Swift の enum と同じリリースで更新**する。

## 連絡先の変更

メール `scpdocs_admin@proton.me` を差し替えるときは、`privacy.html` / `privacy-en.html` / `support.html` / `terms.html` / `index.html` のフッター・問い合わせ節を一括置換し、`web-scp-docs` にデプロイし直す。
