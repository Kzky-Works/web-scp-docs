#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://kzky-works.github.io/web-scp-docs"
APP_STORE_URL = "https://apps.apple.com/jp/app/scp-docs/id6765882660"
CONTACT_EMAIL = "scpdocs_admin@proton.me"
X_URL = "https://x.com/SCPdocs"


@dataclass(frozen=True)
class Language:
    code: str
    suffix: str
    label: str
    html_lang: str
    og_locale: str
    switch_label: str
    switch_aria: str
    nav: dict[str, str]
    footer_back: str
    footer_contact: str


LANGS: dict[str, Language] = {
    "en": Language(
        code="en",
        suffix="",
        label="EN",
        html_lang="en",
        og_locale="en_US",
        switch_label="Language",
        switch_aria="Language switcher",
        nav={
            "index": "Home",
            "features": "Features",
            "privacy": "Privacy",
            "support": "Support",
            "terms": "Terms",
            "rating-safety": "Safety",
        },
        footer_back="Back to home",
        footer_contact="Contact",
    ),
    "ja": Language(
        code="ja",
        suffix="-ja",
        label="日本語",
        html_lang="ja",
        og_locale="ja_JP",
        switch_label="Language",
        switch_aria="言語切り替え",
        nav={
            "index": "ホーム",
            "features": "機能",
            "privacy": "プライバシー",
            "support": "サポート",
            "terms": "利用規約",
            "rating-safety": "安全方針",
        },
        footer_back="ホームへ戻る",
        footer_contact="連絡先",
    ),
    "fr": Language(
        code="fr",
        suffix="-fr",
        label="FR",
        html_lang="fr",
        og_locale="fr_FR",
        switch_label="Language",
        switch_aria="Sélection de la langue",
        nav={
            "index": "Accueil",
            "features": "Fonctionnalités",
            "privacy": "Confidentialité",
            "support": "Assistance",
            "terms": "Conditions",
            "rating-safety": "Sécurité",
        },
        footer_back="Retour à l'accueil",
        footer_contact="Contact",
    ),
    "ru": Language(
        code="ru",
        suffix="-ru",
        label="RU",
        html_lang="ru",
        og_locale="ru_RU",
        switch_label="Язык",
        switch_aria="Выбор языка",
        nav={
            "index": "Главная",
            "features": "Возможности",
            "privacy": "Конфиденциальность",
            "support": "Поддержка",
            "terms": "Условия",
            "rating-safety": "Безопасность",
        },
        footer_back="Назад на главную",
        footer_contact="Контакт",
    ),
    "ko": Language(
        code="ko",
        suffix="-ko",
        label="한국어",
        html_lang="ko",
        og_locale="ko_KR",
        switch_label="Language",
        switch_aria="언어 선택",
        nav={
            "index": "홈",
            "features": "기능",
            "privacy": "개인정보",
            "support": "지원",
            "terms": "이용약관",
            "rating-safety": "안전",
        },
        footer_back="홈으로 돌아가기",
        footer_contact="문의",
    ),
}


PAGE_ORDER = ["index", "features", "privacy", "support", "terms", "rating-safety"]


def page_file(page: str, lang_code: str) -> str:
    suffix = LANGS[lang_code].suffix
    if page == "index":
        return "index.html" if lang_code == "en" else f"index{suffix}.html"
    return f"{page}{suffix}.html"


def page_url(page: str, lang_code: str) -> str:
    if page == "index" and lang_code == "en":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{page_file(page, lang_code)}"


def linked_versions(page: str, active_lang: str) -> str:
    links = []
    for code, lang in LANGS.items():
        current = ' aria-current="true"' if code == active_lang else ""
        links.append(
            f'<a href="{page_file(page, code)}"{current} lang="{lang.html_lang}">{lang.label}</a>'
        )
    return "\n".join(f"            {link}" for link in links)


def head_alternates(page: str) -> str:
    rows = [
        f'  <link rel="alternate" hreflang="{code}" href="{page_url(page, code)}" />'
        for code in LANGS
    ]
    rows.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url(page, "en")}" />')
    return "\n".join(rows)


def og_locale_alternates(active_lang: str) -> str:
    return "\n".join(
        f'  <meta property="og:locale:alternate" content="{lang.og_locale}" />'
        for code, lang in LANGS.items()
        if code != active_lang
    )


def nav(page: str, active_lang: str) -> str:
    lang = LANGS[active_lang]
    rows = []
    for item in PAGE_ORDER:
        current = ' aria-current="page"' if item == page else ""
        rows.append(f'            <a href="{page_file(item, active_lang)}"{current}>{lang.nav[item]}</a>')
    rows.append(
        '            <a class="nav-store" href="{}" target="_blank"\n'
        '              rel="noopener noreferrer">App Store</a>'.format(APP_STORE_URL)
    )
    return "\n".join(rows)


def header(page: str, active_lang: str, brand_line: str, title: str) -> str:
    lang = LANGS[active_lang]
    return f"""    <header class="terminal-header">
      <div class="terminal-header-inner">
        <div>
          <div class="brand-line">{brand_line}</div>
          <h1 class="brand-title">{title}</h1>
        </div>
        <div class="terminal-header-actions">
          <div class="language-switch" aria-label="{lang.switch_aria}">
            <span class="language-switch-label">{lang.switch_label}</span>
{linked_versions(page, active_lang)}
          </div>
          <nav class="nav" aria-label="Primary navigation">
{nav(page, active_lang)}
          </nav>
        </div>
      </div>
    </header>"""


def footer(active_lang: str, page_title: str) -> str:
    lang = LANGS[active_lang]
    return f"""    <footer class="site-footer">
      <div class="site-footer-inner">
        <div>
          <strong>SCP Docs</strong> — {page_title}
        </div>
        <div>
          {lang.footer_contact}: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br />
          X: <a href="{X_URL}" target="_blank" rel="noopener noreferrer">@SCPdocs</a><br />
          <span class="ft-muted"><a href="{page_file("index", active_lang)}">{lang.footer_back}</a></span>
        </div>
      </div>
    </footer>"""


def layout(
    page: str,
    lang_code: str,
    *,
    title: str,
    description: str,
    brand_line: str,
    h1: str,
    page_title: str,
    body: str,
    og_type: str = "article",
    image: bool = False,
) -> str:
    lang = LANGS[lang_code]
    image_tags = ""
    if image:
        image_url = f"{BASE_URL}/assets/images/home-showcase.png"
        image_tags = f"""
  <meta property="og:image" content="{image_url}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{image_url}" />"""
    else:
        image_tags = '\n  <meta name="twitter:card" content="summary" />'

    html = f"""<!DOCTYPE html>
<html lang="{lang.html_lang}">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="description" content="{escape(description, quote=True)}" />
  <meta name="theme-color" content="#F7F6F0" />
  <title>{escape(title)}</title>
  <link rel="canonical" href="{page_url(page, lang_code)}" />
{head_alternates(page)}
  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="SCP Docs" />
  <meta property="og:locale" content="{lang.og_locale}" />
{og_locale_alternates(lang_code)}
  <meta property="og:title" content="{escape(title, quote=True)}" />
  <meta property="og:description" content="{escape(description, quote=True)}" />
  <meta property="og:url" content="{page_url(page, lang_code)}" />{image_tags}
  <meta name="twitter:title" content="{escape(title, quote=True)}" />
  <meta name="twitter:description" content="{escape(description, quote=True)}" />
  <link rel="stylesheet" href="assets/styles.css" />
</head>

<body>
  <div class="layout-wide">
{header(page, lang_code, brand_line, h1)}

{body}

{footer(lang_code, page_title)}
  </div>
</body>

</html>
"""
    return html


INDEX: dict[str, dict[str, str]] = {
    "en": {
        "title": "SCP Docs — Foundation Archive",
        "description": "SCP Docs is an unofficial native iOS reader for SCP Wiki archives, branch-aware search, reading state, saved searches, sharing, and premium reading tools.",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="hero-title">
        <p class="section-label">Overview</p>
        <h2 id="hero-title" class="section-title-lg">Secure · Contain · Read</h2>
        <div class="card-invert">
          <p class="lede">
            SCP Docs is an <strong>unofficial fan-made iOS reader</strong> for SCP Wiki and branch-site articles. It turns public source pages into a native reading workspace for browsing archives, searching by branch, saving what matters, and returning to the reports you were reading.
          </p>
          <div class="pill-row">
            <span class="code-chip">Native iOS reader</span>
            <span class="code-chip">Four branch archives</span>
            <span class="code-chip">Reading state</span>
            <span class="code-chip">Premium workspace tools</span>
          </div>
          <div class="store-cta" aria-label="SCP Docs App Store link">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>SCP Docs for iPhone</strong>
              <span>Built for iOS 17 and later. App UI currently supports English, Japanese, French, and Russian.</span>
            </div>
            <a class="store-cta-link" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer" aria-label="Open SCP Docs on the App Store">
              <span class="store-cta-link-main">Get on the App Store</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
        <figure class="hero-media" aria-label="SCP Docs app preview">
          <img src="assets/images/home-showcase.png"
            alt="Preview of the SCP Docs home screen in light and dark appearances" />
        </figure>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:38px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">Browse, search, organize, and resume</h2>
        <div class="grid-2">
          <div class="card">
            <p>
              The app is organized around Home, Library, Search, and Settings. Home now focuses on continue-reading, quick search presets, random discovery, and cleaner directory routes for Stories, Tales, Canons, Series, Groups of Interest, guides, and related collections.
            </p>
          </div>
          <div class="card">
            <p>
              Reading history, read status, ratings, bookmarks, read-later items, scroll position, memos, folders, and resume-reading data stay tied to the articles you open, so your route through the archive remains visible on device.
            </p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:38px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">Four branches, one archive workflow</h2>
        <div class="card">
          <p>
            SCP Docs supports the English main SCP Foundation archive plus the Japanese, French, and Russian branches. Switching branches changes Home, search, in-app lists, article destinations, and the app UI language. SCP International and translated archive entry points are listed where catalog data is available.
          </p>
          <ul class="ft-list">
            <li><strong>Archive lists</strong> — SCP articles, Tales, Canons, Canon series, GoI, Joke SCPs, SCP-EX, collections, recent articles, and related directories.</li>
            <li><strong>Search</strong> — number and title search is free; Premium adds advanced filters across documents, tags, Object Class, memos, reading status, official score, length, and saved searches.</li>
            <li><strong>Reader</strong> — cleaner typography, themes, scroll tools, better dark mode, and more faithful rendering for specially formatted source pages.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:38px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">Tools for deeper reading</h2>
        <div class="grid-2">
          <div class="card">
            <dl class="dl-flat">
              <dt>Reading stats</dt>
              <dd>Reading time, catalog coverage, frequently read Object Classes and tags, rating trends, memo insights, backlog status, and logs by day, month, and year.</dd>
              <dt>Saved searches</dt>
              <dd>Save search conditions and receive on-device notifications when new matching catalog entries appear.</dd>
              <dt>Bookmark folders</dt>
              <dd>Organize saved articles into folders that can sync through your own iCloud Drive, along with memos and saved searches.</dd>
            </dl>
          </div>
          <div class="card">
            <dl class="dl-flat">
              <dt>Listen and save</dt>
              <dd>Text-to-speech reads article text aloud, and offline snapshots keep eligible saved articles available without a connection.</dd>
              <dt>Share as cards</dt>
              <dd>Turn an article or selected list into a styled share card for X and other social apps, with templates and optional comments.</dd>
              <dt>Ads and limits</dt>
              <dd>Premium hides ads, expands save limits, unlocks memo editing, and enables advanced search. A rewarded ad can grant temporary Premium access when available.</dd>
            </dl>
          </div>
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:38px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">System requirements</h2>
        <div class="card-flat">
          <ul class="ft-list">
            <li><strong>OS</strong> — iOS 17 or later.</li>
            <li><strong>Network</strong> — required for catalog refresh, online article viewing, source-site content, ads, purchase checks, and app links.</li>
            <li><strong>Accounts</strong> — no SCP Foundation or Wikidot account is required for reading in the app.</li>
          </ul>
        </div>
      </section>

      <section style="margin-top:40px;">
        <p class="section-label">Legal</p>
        <div class="card">
          <p>
            SCP Docs is an <strong>unofficial fan application</strong>. Source articles, author credits, copyright notices, and licensing terms remain governed by the source sites. SCP-related works are commonly published under Creative Commons BY-SA 3.0, but each source page is authoritative.
          </p>
          <div class="pill-row">
            <a class="pill" href="features.html">Features</a>
            <a class="pill" href="privacy.html">Privacy</a>
            <a class="pill" href="support.html">Support</a>
            <a class="pill" href="terms.html">Terms</a>
            <a class="pill" href="rating-safety.html">Rating &amp; Safety</a>
          </div>
        </div>
      </section>
    </main>""",
    },
    "ja": {
        "title": "SCP Docs — Foundation Archive",
        "description": "SCP Docs は SCP Wiki と各支部の記事を快適に読むための非公式 iOS リーダーです。支部対応検索、読書状態、共有カード、保存検索、読書統計などに対応します。",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="hero-title">
        <p class="section-label">Overview</p>
        <h2 id="hero-title" class="section-title-lg">Secure · Contain · Read</h2>
        <div class="card-invert">
          <p class="lede">
            SCP Docs は、SCP Wiki と各支部サイトの記事をより快適に読むための<strong>非公式ファンメイド iOS リーダー</strong>です。公開されている元ページを、書庫の閲覧、支部別検索、保存、読書記録、読みかけ復帰まで扱えるネイティブな読書ワークスペースにまとめます。
          </p>
          <div class="pill-row">
            <span class="code-chip">ネイティブ iOS リーダー</span>
            <span class="code-chip">4支部対応</span>
            <span class="code-chip">読書状態</span>
            <span class="code-chip">プレミアム読書ツール</span>
          </div>
          <div class="store-cta" aria-label="SCP Docs App Store link">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>SCP Docs for iPhone</strong>
              <span>iOS 17以降に対応。アプリUIは現在、英語・日本語・フランス語・ロシア語に対応しています。</span>
            </div>
            <a class="store-cta-link" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer" aria-label="App Store で SCP Docs を開く">
              <span class="store-cta-link-main">App Store で見る</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
        <figure class="hero-media" aria-label="SCP Docs app preview">
          <img src="assets/images/home-showcase.png"
            alt="SCP Docs のホーム画面プレビュー。ライト表示とダーク表示。" />
        </figure>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:38px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">読む、探す、整理する、戻ってくる</h2>
        <div class="grid-2">
          <div class="card">
            <p>
              アプリはホーム、書庫、検索、設定を中心に構成されています。現在のホームは「続きから読む」、検索プリセット、ランダム発見、Stories / Tales / Canons / Series / GoI / ガイド類などへ進む整理されたディレクトリを備えます。
            </p>
          </div>
          <div class="card">
            <p>
              閲覧履歴、読了状態、評価、ブックマーク、後で読む、スクロール位置、メモ、フォルダ、続きから読むデータを記事に結びつけて保存し、読んできた経路を端末内で見失いにくくします。
            </p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:38px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">4支部をひとつの読書フローに</h2>
        <div class="card">
          <p>
            英語本家 SCP Foundation アーカイブと、日本・フランス・ロシア支部に対応しています。支部を切り替えると、ホーム、検索、アプリ内リスト、記事リンク先、アプリUI言語が切り替わります。カタログデータがある範囲で SCP International や翻訳アーカイブの入口も整理します。
          </p>
          <ul class="ft-list">
            <li><strong>書庫リスト</strong> — SCP記事、Tales、Canons、Canonシリーズ、GoI、Joke SCP、SCP-EX、コレクション、新着記事、関連ディレクトリ。</li>
            <li><strong>検索</strong> — 番号・タイトル検索は無料。プレミアムでは対象文書、タグ、オブジェクトクラス、メモ、読書状態、公式評価、長さ、保存検索まで組み合わせられます。</li>
            <li><strong>リーダー</strong> — 文字組み、テーマ、スクロール操作、ダークモード、特殊レイアウト記事の再現性を見直した本文表示。</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:38px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">深く読むためのツール</h2>
        <div class="grid-2">
          <div class="card">
            <dl class="dl-flat">
              <dt>読書統計</dt>
              <dd>読書時間、カタログ読了率、よく読むオブジェクトクラスやタグ、評価傾向、メモ、積読、曜日・月・年ごとの記録を表示します。</dd>
              <dt>保存した検索</dt>
              <dd>検索条件を保存し、新しく一致する記事がカタログに現れたときに端末上の通知で知らせます。</dd>
              <dt>ブックマークフォルダ</dt>
              <dd>保存した記事をフォルダで整理し、メモや保存検索とともに自分の iCloud Drive 経由で同期できます。</dd>
            </dl>
          </div>
          <div class="card">
            <dl class="dl-flat">
              <dt>聴く、保存する</dt>
              <dd>読み上げ機能で本文を音声再生し、対象記事のオフライン保存で通信がない場面でも読み返せます。</dd>
              <dt>カードで共有</dt>
              <dd>記事や選んだリストを、X などで共有しやすいカード画像にできます。テンプレートとコメントにも対応します。</dd>
              <dt>広告と上限</dt>
              <dd>プレミアムでは広告非表示、保存上限拡張、メモ編集、高度な検索を利用できます。利用可能な場合はリワード広告で一時的にプレミアムを解放できます。</dd>
            </dl>
          </div>
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:38px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">動作環境</h2>
        <div class="card-flat">
          <ul class="ft-list">
            <li><strong>OS</strong> — iOS 17以降。</li>
            <li><strong>通信</strong> — カタログ更新、オンライン記事表示、元サイトコンテンツ、広告、購入確認、外部リンクに必要です。</li>
            <li><strong>アカウント</strong> — アプリで読むだけなら SCP Foundation や Wikidot のアカウントは不要です。</li>
          </ul>
        </div>
      </section>

      <section style="margin-top:40px;">
        <p class="section-label">Legal</p>
        <div class="card">
          <p>
            SCP Docs は<strong>非公式ファンアプリ</strong>です。記事本文、著者表示、著作権表示、ライセンス条件は各提供元サイトが正本です。SCP 関連作品は一般に Creative Commons BY-SA 3.0 のもとで公開されていますが、個別ページの表示が優先されます。
          </p>
          <div class="pill-row">
            <a class="pill" href="features-ja.html">機能</a>
            <a class="pill" href="privacy-ja.html">プライバシー</a>
            <a class="pill" href="support-ja.html">サポート</a>
            <a class="pill" href="terms-ja.html">利用規約</a>
            <a class="pill" href="rating-safety-ja.html">安全方針</a>
          </div>
        </div>
      </section>
    </main>""",
    },
    "fr": {
        "title": "SCP Docs — Archive de la Fondation",
        "description": "SCP Docs est un lecteur iOS non officiel pour les archives SCP Wiki, la recherche par branche, l'état de lecture, les recherches enregistrées, le partage et les outils Premium.",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="hero-title">
        <p class="section-label">Overview</p>
        <h2 id="hero-title" class="section-title-lg">Secure · Contain · Read</h2>
        <div class="card-invert">
          <p class="lede">
            SCP Docs est un <strong>lecteur iOS non officiel et fan-made</strong> pour les articles du SCP Wiki et de ses branches. Il transforme les pages publiques en espace de lecture natif pour parcourir les archives, chercher par branche, sauvegarder ce qui compte et reprendre vos rapports en cours.
          </p>
          <div class="pill-row">
            <span class="code-chip">Lecteur iOS natif</span>
            <span class="code-chip">Quatre branches</span>
            <span class="code-chip">État de lecture</span>
            <span class="code-chip">Outils Premium</span>
          </div>
          <div class="store-cta" aria-label="Lien App Store de SCP Docs">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>SCP Docs pour iPhone</strong>
              <span>Nécessite iOS 17 ou version ultérieure. L'interface de l'app prend actuellement en charge l'anglais, le japonais, le français et le russe.</span>
            </div>
            <a class="store-cta-link" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer" aria-label="Ouvrir SCP Docs sur l'App Store">
              <span class="store-cta-link-main">Voir sur l'App Store</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
        <figure class="hero-media" aria-label="Aperçu de l'app SCP Docs">
          <img src="assets/images/home-showcase.png"
            alt="Aperçu de l'écran d'accueil SCP Docs en modes clair et sombre" />
        </figure>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:38px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">Lire, chercher, organiser, reprendre</h2>
        <div class="grid-2">
          <div class="card">
            <p>
              L'app s'organise autour d'Accueil, Bibliothèque, Recherche et Réglages. L'accueil met en avant la reprise de lecture, les préréglages de recherche, la découverte aléatoire et des itinéraires plus clairs vers Stories, Tales, Canons, Series, GoI, guides et collections associées.
            </p>
          </div>
          <div class="card">
            <p>
              Historique, état lu/non lu, notes, favoris, éléments à lire plus tard, position de défilement, mémos, dossiers et reprise de lecture restent liés aux articles ouverts, pour garder votre parcours visible sur l'appareil.
            </p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:38px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">Quatre branches, un même flux de lecture</h2>
        <div class="card">
          <p>
            SCP Docs prend en charge l'archive principale anglaise de la SCP Foundation ainsi que les branches japonaise, française et russe. Changer de branche modifie l'accueil, la recherche, les listes intégrées, les destinations d'articles et la langue de l'interface. SCP International et les archives traduites sont listés lorsque les données de catalogue existent.
          </p>
          <ul class="ft-list">
            <li><strong>Listes d'archives</strong> — SCP, Tales, Canons, séries Canon, GoI, Joke SCP, SCP-EX, collections, articles récents et répertoires associés.</li>
            <li><strong>Recherche</strong> — la recherche par numéro et titre est gratuite. Premium ajoute des filtres par documents, tags, classe d'objet, mémos, état de lecture, score officiel, longueur et recherches enregistrées.</li>
            <li><strong>Lecteur</strong> — typographie plus claire, thèmes, outils de défilement, meilleur mode sombre et rendu plus fidèle des pages à mise en forme spéciale.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:38px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">Des outils pour lire plus loin</h2>
        <div class="grid-2">
          <div class="card">
            <dl class="dl-flat">
              <dt>Statistiques de lecture</dt>
              <dd>Temps de lecture, progression du catalogue, classes d'objet et tags les plus lus, tendances de notes, mémos, pile à lire et journaux par jour, mois et année.</dd>
              <dt>Recherches enregistrées</dt>
              <dd>Enregistrez des critères et recevez une notification sur l'appareil quand de nouvelles entrées correspondantes apparaissent.</dd>
              <dt>Dossiers de favoris</dt>
              <dd>Organisez les articles sauvegardés dans des dossiers pouvant se synchroniser via votre iCloud Drive, avec mémos et recherches enregistrées.</dd>
            </dl>
          </div>
          <div class="card">
            <dl class="dl-flat">
              <dt>Écouter et sauvegarder</dt>
              <dd>La synthèse vocale lit les articles à voix haute, et les instantanés hors ligne gardent les articles éligibles accessibles sans connexion.</dd>
              <dt>Partager en cartes</dt>
              <dd>Transformez un article ou une liste choisie en carte de partage pour X et d'autres apps sociales, avec modèles et commentaire facultatif.</dd>
              <dt>Publicités et limites</dt>
              <dd>Premium masque les publicités, étend les limites de sauvegarde, déverrouille l'édition de mémos et la recherche avancée. Une publicité récompensée peut donner un accès Premium temporaire lorsqu'elle est disponible.</dd>
            </dl>
          </div>
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:38px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">Configuration requise</h2>
        <div class="card-flat">
          <ul class="ft-list">
            <li><strong>OS</strong> — iOS 17 ou version ultérieure.</li>
            <li><strong>Réseau</strong> — requis pour actualiser les catalogues, lire en ligne, charger les sites sources, les publicités, les vérifications d'achat et les liens externes.</li>
            <li><strong>Comptes</strong> — aucun compte SCP Foundation ou Wikidot n'est requis pour lire dans l'app.</li>
          </ul>
        </div>
      </section>

      <section style="margin-top:40px;">
        <p class="section-label">Legal</p>
        <div class="card">
          <p>
            SCP Docs est une <strong>application fan non officielle</strong>. Les articles, crédits d'auteurs, avis de droit d'auteur et licences restent régis par les sites sources. Les œuvres SCP sont généralement publiées sous Creative Commons BY-SA 3.0, mais chaque page source fait autorité.
          </p>
          <div class="pill-row">
            <a class="pill" href="features-fr.html">Fonctionnalités</a>
            <a class="pill" href="privacy-fr.html">Confidentialité</a>
            <a class="pill" href="support-fr.html">Assistance</a>
            <a class="pill" href="terms-fr.html">Conditions</a>
            <a class="pill" href="rating-safety-fr.html">Sécurité</a>
          </div>
        </div>
      </section>
    </main>""",
    },
    "ru": {
        "title": "SCP Docs — Архив Фонда",
        "description": "SCP Docs — неофициальный iOS-ридер для архивов SCP Wiki, поиска по филиалам, состояния чтения, сохранённых поисков, карточек для публикации и Premium-инструментов.",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="hero-title">
        <p class="section-label">Overview</p>
        <h2 id="hero-title" class="section-title-lg">Secure · Contain · Read</h2>
        <div class="card-invert">
          <p class="lede">
            SCP Docs — <strong>неофициальный фанатский iOS-ридер</strong> для статей SCP Wiki и сайтов филиалов. Он превращает публичные исходные страницы в нативное пространство для чтения: архивы, поиск по филиалам, сохранение важных материалов и возвращение к начатым отчётам.
          </p>
          <div class="pill-row">
            <span class="code-chip">Нативный iOS-ридер</span>
            <span class="code-chip">Четыре филиала</span>
            <span class="code-chip">Состояние чтения</span>
            <span class="code-chip">Premium-инструменты</span>
          </div>
          <div class="store-cta" aria-label="Ссылка SCP Docs в App Store">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>SCP Docs для iPhone</strong>
              <span>Требуется iOS 17 или новее. Интерфейс приложения сейчас поддерживает английский, японский, французский и русский языки.</span>
            </div>
            <a class="store-cta-link" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer" aria-label="Открыть SCP Docs в App Store">
              <span class="store-cta-link-main">Открыть App Store</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
        <figure class="hero-media" aria-label="Превью приложения SCP Docs">
          <img src="assets/images/home-showcase.png"
            alt="Превью главного экрана SCP Docs в светлой и тёмной теме" />
        </figure>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:38px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">Читайте, ищите, упорядочивайте и возвращайтесь</h2>
        <div class="grid-2">
          <div class="card">
            <p>
              Приложение построено вокруг Главной, Библиотеки, Поиска и Настроек. Главная теперь выделяет продолжение чтения, готовые поисковые наборы, случайное открытие и более понятные переходы к Stories, Tales, Canons, Series, GoI, руководствам и связанным коллекциям.
            </p>
          </div>
          <div class="card">
            <p>
              История, статус прочтения, оценки, закладки, список «прочитать позже», позиция прокрутки, заметки, папки и данные продолжения чтения привязаны к открытым статьям, чтобы ваш путь по архиву оставался видимым на устройстве.
            </p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:38px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">Четыре филиала в одном рабочем процессе</h2>
        <div class="card">
          <p>
            SCP Docs поддерживает основной английский архив SCP Foundation, а также японский, французский и русский филиалы. При смене филиала меняются Главная, поиск, списки в приложении, ссылки на статьи и язык интерфейса. SCP International и переводные архивы перечисляются там, где доступны каталожные данные.
          </p>
          <ul class="ft-list">
            <li><strong>Списки архивов</strong> — SCP, Tales, Canons, серии Canon, GoI, Joke SCP, SCP-EX, коллекции, недавние статьи и связанные каталоги.</li>
            <li><strong>Поиск</strong> — поиск по номеру и названию бесплатен. Premium добавляет фильтры по документам, тегам, классу объекта, заметкам, статусу чтения, официальной оценке, длине и сохранённым поискам.</li>
            <li><strong>Ридер</strong> — более аккуратная типографика, темы, инструменты прокрутки, улучшенная тёмная тема и более точное отображение страниц со специальной вёрсткой.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:38px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">Инструменты для глубокого чтения</h2>
        <div class="grid-2">
          <div class="card">
            <dl class="dl-flat">
              <dt>Статистика чтения</dt>
              <dd>Время чтения, охват каталога, часто читаемые классы объектов и теги, динамика оценок, заметки, список к прочтению и журналы по дням, месяцам и годам.</dd>
              <dt>Сохранённые поиски</dt>
              <dd>Сохраняйте условия поиска и получайте уведомления на устройстве, когда появляются новые подходящие записи каталога.</dd>
              <dt>Папки закладок</dt>
              <dd>Раскладывайте сохранённые статьи по папкам, которые могут синхронизироваться через ваш iCloud Drive вместе с заметками и сохранёнными поисками.</dd>
            </dl>
          </div>
          <div class="card">
            <dl class="dl-flat">
              <dt>Слушать и сохранять</dt>
              <dd>Синтез речи читает текст статей вслух, а офлайн-снимки оставляют подходящие сохранённые статьи доступными без сети.</dd>
              <dt>Делиться карточками</dt>
              <dd>Превратите статью или выбранный список в карточку для X и других социальных приложений, с шаблонами и необязательным комментарием.</dd>
              <dt>Реклама и лимиты</dt>
              <dd>Premium скрывает рекламу, расширяет лимиты сохранения, открывает редактирование заметок и расширенный поиск. Рекламный просмотр может временно открыть Premium, если предложение доступно.</dd>
            </dl>
          </div>
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:38px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">Системные требования</h2>
        <div class="card-flat">
          <ul class="ft-list">
            <li><strong>OS</strong> — iOS 17 или новее.</li>
            <li><strong>Сеть</strong> — нужна для обновления каталогов, онлайн-чтения, загрузки исходных сайтов, рекламы, проверки покупок и внешних ссылок.</li>
            <li><strong>Аккаунты</strong> — для чтения в приложении не нужен аккаунт SCP Foundation или Wikidot.</li>
          </ul>
        </div>
      </section>

      <section style="margin-top:40px;">
        <p class="section-label">Legal</p>
        <div class="card">
          <p>
            SCP Docs — <strong>неофициальное фанатское приложение</strong>. Статьи, сведения об авторах, уведомления об авторских правах и лицензии регулируются исходными сайтами. Материалы SCP обычно публикуются по Creative Commons BY-SA 3.0, но приоритет имеет каждая исходная страница.
          </p>
          <div class="pill-row">
            <a class="pill" href="features-ru.html">Возможности</a>
            <a class="pill" href="privacy-ru.html">Конфиденциальность</a>
            <a class="pill" href="support-ru.html">Поддержка</a>
            <a class="pill" href="terms-ru.html">Условия</a>
            <a class="pill" href="rating-safety-ru.html">Безопасность</a>
          </div>
        </div>
      </section>
    </main>""",
    },
    "ko": {
        "title": "SCP Docs — Foundation Archive",
        "description": "SCP Docs는 SCP Wiki 아카이브를 위한 비공식 iOS 리더입니다. 지부별 검색, 읽기 상태, 저장 검색, 공유 카드, 프리미엄 읽기 도구를 제공합니다.",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="hero-title">
        <p class="section-label">Overview</p>
        <h2 id="hero-title" class="section-title-lg">Secure · Contain · Read</h2>
        <div class="card-invert">
          <p class="lede">
            SCP Docs는 SCP Wiki와 각 지부 사이트의 글을 더 편하게 읽기 위한 <strong>비공식 팬 제작 iOS 리더</strong>입니다. 공개된 원문 페이지를 네이티브 읽기 공간으로 정리하여 아카이브 탐색, 지부별 검색, 저장, 읽기 기록, 이어 읽기를 한곳에서 다룰 수 있게 합니다.
          </p>
          <div class="pill-row">
            <span class="code-chip">네이티브 iOS 리더</span>
            <span class="code-chip">4개 지부 아카이브</span>
            <span class="code-chip">읽기 상태</span>
            <span class="code-chip">프리미엄 읽기 도구</span>
          </div>
          <div class="store-cta" aria-label="SCP Docs App Store link">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>iPhone용 SCP Docs</strong>
              <span>iOS 17 이상이 필요합니다. 현재 앱 UI는 영어, 일본어, 프랑스어, 러시아어를 지원합니다.</span>
            </div>
            <a class="store-cta-link" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer" aria-label="App Store에서 SCP Docs 열기">
              <span class="store-cta-link-main">App Store에서 보기</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
        <figure class="hero-media" aria-label="SCP Docs app preview">
          <img src="assets/images/home-showcase.png"
            alt="라이트 모드와 다크 모드로 표시된 SCP Docs 홈 화면 미리보기" />
        </figure>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:38px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">읽고, 찾고, 정리하고, 다시 돌아오기</h2>
        <div class="grid-2">
          <div class="card">
            <p>
              앱은 Home, Library, Search, Settings를 중심으로 구성됩니다. 최신 홈 화면은 이어 읽기, 빠른 검색 프리셋, 랜덤 발견, Stories, Tales, Canons, Series, GoI, 가이드와 관련 컬렉션으로 이동하는 정리된 디렉터리를 제공합니다.
            </p>
          </div>
          <div class="card">
            <p>
              열람 기록, 읽음 상태, 평가, 북마크, 나중에 읽기, 스크롤 위치, 메모, 폴더, 이어 읽기 데이터가 각 글에 연결되어 기기 안에서 읽어 온 경로를 다시 찾기 쉽습니다.
            </p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:38px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">4개 지부를 하나의 읽기 흐름으로</h2>
        <div class="card">
          <p>
            SCP Docs는 영어 본가 SCP Foundation 아카이브와 일본어, 프랑스어, 러시아어 지부를 지원합니다. 지부를 바꾸면 홈, 검색, 앱 내 목록, 글 링크 대상, 앱 UI 언어가 함께 바뀝니다. 카탈로그 데이터가 있는 경우 SCP International과 번역 아카이브의 진입점도 정리해 보여 줍니다.
          </p>
          <ul class="ft-list">
            <li><strong>아카이브 목록</strong> — SCP 글, Tales, Canons, Canon series, GoI, Joke SCP, SCP-EX, 컬렉션, 최근 글, 관련 디렉터리.</li>
            <li><strong>검색</strong> — 번호와 제목 검색은 무료입니다. 프리미엄에서는 문서 범위, 태그, Object Class, 메모, 읽기 상태, 공식 점수, 길이, 저장 검색까지 조합할 수 있습니다.</li>
            <li><strong>리더</strong> — 더 차분한 타이포그래피, 테마, 스크롤 도구, 개선된 다크 모드, 특수 레이아웃 글을 더 원문에 가깝게 보여 주는 표시 방식.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:38px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">더 깊게 읽기 위한 도구</h2>
        <div class="grid-2">
          <div class="card">
            <dl class="dl-flat">
              <dt>읽기 통계</dt>
              <dd>읽기 시간, 카탈로그 진행률, 자주 읽는 Object Class와 태그, 평가 추세, 메모, 나중에 읽을 글, 요일·월·연도별 기록을 확인합니다.</dd>
              <dt>저장 검색</dt>
              <dd>검색 조건을 저장하고, 새로 일치하는 항목이 카탈로그에 나타나면 기기 알림으로 받을 수 있습니다.</dd>
              <dt>북마크 폴더</dt>
              <dd>저장한 글을 폴더로 정리하고, 메모와 저장 검색과 함께 사용자의 iCloud Drive를 통해 동기화할 수 있습니다.</dd>
            </dl>
          </div>
          <div class="card">
            <dl class="dl-flat">
              <dt>듣기와 저장</dt>
              <dd>텍스트 음성 변환으로 글을 들을 수 있고, 오프라인 스냅샷으로 저장 가능한 글을 연결 없이 다시 열 수 있습니다.</dd>
              <dt>카드로 공유</dt>
              <dd>글 하나 또는 직접 고른 목록을 X 등 소셜 앱에 공유하기 쉬운 카드 이미지로 만들 수 있습니다. 템플릿과 선택 코멘트를 지원합니다.</dd>
              <dt>광고와 제한</dt>
              <dd>프리미엄은 광고를 숨기고, 저장 한도를 늘리며, 메모 편집과 고급 검색을 엽니다. 제공되는 경우 리워드 광고로 임시 프리미엄을 사용할 수 있습니다.</dd>
            </dl>
          </div>
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:38px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">시스템 요구 사항</h2>
        <div class="card-flat">
          <ul class="ft-list">
            <li><strong>OS</strong> — iOS 17 이상.</li>
            <li><strong>네트워크</strong> — 카탈로그 새로고침, 온라인 글 보기, 원본 사이트 콘텐츠, 광고, 구매 확인, 외부 링크에 필요합니다.</li>
            <li><strong>계정</strong> — 앱에서 읽기만 할 때는 SCP Foundation 또는 Wikidot 계정이 필요하지 않습니다.</li>
          </ul>
        </div>
      </section>

      <section style="margin-top:40px;">
        <p class="section-label">Legal</p>
        <div class="card">
          <p>
            SCP Docs는 <strong>비공식 팬 애플리케이션</strong>입니다. 원문 글, 저자 표시, 저작권 고지, 라이선스 조건은 각 원본 사이트가 기준입니다. SCP 관련 작품은 일반적으로 Creative Commons BY-SA 3.0으로 공개되지만, 개별 원문 페이지의 표시가 우선합니다.
          </p>
          <div class="pill-row">
            <a class="pill" href="features-ko.html">기능</a>
            <a class="pill" href="privacy-ko.html">개인정보</a>
            <a class="pill" href="support-ko.html">지원</a>
            <a class="pill" href="terms-ko.html">이용약관</a>
            <a class="pill" href="rating-safety-ko.html">안전</a>
          </div>
        </div>
      </section>
    </main>""",
    },
}


FEATURES: dict[str, dict[str, str]] = {
    "en": {
        "title": "Features — SCP Docs",
        "description": "A screenshot-led tour of SCP Docs: branch-aware Home, refreshed search, Library, reader tools, sharing, saved searches, reading stats, and sync.",
        "body": r"""
    <main class="main-pad">
      <section aria-labelledby="feature-title">
        <p class="section-label">Feature Overview</p>
        <h2 id="feature-title" class="section-title-lg">Find a report, then actually get back to it</h2>
        <div class="feature-hero">
          <div>
            <p class="lede">
              SCP Docs brings archive entry points, search, reader controls, and personal reading state into one native iOS app. Recent releases expanded it from a reader into a fuller workspace for discovering, saving, listening, sharing, and tracking what you read.
            </p>
            <div class="pill-row">
              <span class="code-chip">Home</span>
              <span class="code-chip">Library</span>
              <span class="code-chip">Search</span>
              <span class="code-chip">Stats</span>
              <span class="code-chip">Share cards</span>
            </div>
          </div>
          <figure class="screen-frame screen-frame-compact">
            <img src="assets/images/home-showcase.png"
              alt="SCP Docs home screen shown in light and dark appearances" />
          </figure>
        </div>
      </section>

      <section aria-labelledby="screens-title" style="margin-top:38px;">
        <p class="section-label">Screenshots</p>
        <h2 id="screens-title" class="section-title-lg">The interface at a glance</h2>
        <div class="feature-shot-grid">
          <figure class="screen-frame">
            <img src="assets/images/home-light.png" alt="SCP Docs home screen in light mode" />
            <figcaption>Home in light mode</figcaption>
          </figure>
          <figure class="screen-frame">
            <img src="assets/images/home-dark.png" alt="SCP Docs home screen in dark mode" />
            <figcaption>Home in dark mode</figcaption>
          </figure>
        </div>
      </section>

      <section aria-labelledby="points-title" style="margin-top:38px;">
        <p class="section-label">What it does</p>
        <h2 id="points-title" class="section-title-lg">Core features</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <p class="section-label">Branches</p>
            <h3>English, Japanese, French, and Russian archives</h3>
            <p>Switching branches changes Home, search, lists, article destinations, and app language so each archive feels like its own reading context.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Directories</p>
            <h3>Cleaner archive routes</h3>
            <p>Browse SCP reports, Tales, Canons, Canon series, GoI, Joke SCPs, SCP-EX, collections, recent articles, guides, and related lists.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Search</p>
            <h3>Fast free search, deeper Premium filters</h3>
            <p>Open by SCP number, search titles, and use shortcuts for tags and Object Classes. Premium adds documents, memos, reading status, official score, length, and saved searches.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Reader</p>
            <h3>A focused article view</h3>
            <p>Typography controls, calmer themes, improved dark mode, scroll-to-top, offline snapshots, and closer rendering for specially formatted source pages.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Library</p>
            <h3>A place to return</h3>
            <p>History, read status, ratings, bookmarks, read-later, scroll position, memos, and resume-reading data stay organized on your device.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Share</p>
            <h3>Share as cards</h3>
            <p>Turn an article or hand-picked list into a styled card for X and other social apps, with templates and optional comments.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Premium</p>
            <h3>Stats, speech, and offline reading</h3>
            <p>Reading stats, text-to-speech, memo editing, expanded save limits, ad removal, and offline storage support longer reading sessions.</p>
          </div>
          <div class="feature-card">
            <p class="section-label">Sync</p>
            <h3>iCloud-backed personal organization</h3>
            <p>When available, reading state, memos, saved searches, and bookmark folders sync through your own iCloud Drive. Saved searches can notify you about new matches on device.</p>
          </div>
        </div>
      </section>

      <section style="margin-top:40px;">
        <div class="card-flat">
          <p style="margin-top:0;">
            SCP Docs is not an official SCP Foundation or Wikidot app. Source pages, author credits, and license notices on each source site remain authoritative.
          </p>
          <div class="pill-row">
            <a class="pill" href="https://apps.apple.com/jp/app/scp-docs/id6765882660" target="_blank"
              rel="noopener noreferrer">App Store</a>
            <a class="pill" href="support.html">Support</a>
            <a class="pill" href="privacy.html">Privacy</a>
          </div>
        </div>
      </section>
    </main>""",
    },
}


def translated_feature(lang: str) -> dict[str, str]:
    bodies = {
        "ja": (
            "機能紹介 — SCP Docs",
            "SCP Docs のホーム、検索、書庫、リーダー、共有カード、保存検索、読書統計、同期機能をスクリーンショット付きで紹介します。",
            "読みたい報告書を見つけ、あとからきちんと戻る",
            "SCP Docs は、書庫の入口、検索、リーダー操作、個人の読書状態をひとつのネイティブ iOS アプリにまとめます。最近のアップデートで、読むだけでなく、見つける、保存する、聴く、共有する、記録するところまで扱える読書ワークスペースになりました。",
            [
                ("Branches", "英語・日本語・フランス語・ロシア語の書庫", "支部を切り替えると、ホーム、検索、一覧、記事リンク先、アプリ言語が切り替わり、それぞれの書庫をその文脈で読めます。"),
                ("Directories", "整理された書庫ルート", "SCP記事、Tales、Canons、Canonシリーズ、GoI、Joke SCP、SCP-EX、コレクション、新着記事、ガイド類へ移動できます。"),
                ("Search", "無料の高速検索とプレミアム絞り込み", "SCP番号で即オープンし、タイトル、タグ、オブジェクトクラスで検索できます。プレミアムでは対象文書、メモ、読書状態、公式評価、長さ、保存検索まで扱えます。"),
                ("Reader", "集中できる記事ビュー", "文字設定、落ち着いたテーマ、改善したダークモード、トップへ戻る操作、オフライン保存、特殊レイアウト記事の再現性を備えます。"),
                ("Library", "戻ってくるための場所", "閲覧履歴、読了状態、評価、ブックマーク、後で読む、スクロール位置、メモ、続きから読むデータを端末内で整理します。"),
                ("Share", "カードで共有", "記事や選んだリストを、X などで共有しやすいカード画像にできます。テンプレートとコメントにも対応します。"),
                ("Premium", "統計、読み上げ、オフライン", "読書統計、読み上げ、メモ編集、保存上限拡張、広告非表示、オフライン保存が長い読書を支えます。"),
                ("Sync", "iCloudで個人の整理を同期", "利用可能な場合、読書状態、メモ、保存検索、ブックマークフォルダを自分の iCloud Drive 経由で同期できます。保存検索は新着一致を端末上で通知できます。"),
            ],
            "SCP Docs は SCP Foundation や Wikidot の公式アプリではありません。元ページ、著者表示、ライセンス表記は各提供元サイトが正本です。",
            "ホーム（ライト）",
            "ホーム（ダーク）",
        ),
        "fr": (
            "Fonctionnalités — SCP Docs",
            "Visite de SCP Docs avec captures : Accueil par branche, recherche améliorée, Bibliothèque, lecteur, cartes de partage, recherches enregistrées, statistiques et synchronisation.",
            "Trouver un rapport, puis y revenir vraiment",
            "SCP Docs réunit les entrées d'archives, la recherche, les contrôles de lecture et l'état personnel de lecture dans une app iOS native. Les dernières versions en font un espace plus complet pour découvrir, sauvegarder, écouter, partager et suivre vos lectures.",
            [
                ("Branches", "Archives anglaise, japonaise, française et russe", "Changer de branche modifie l'accueil, la recherche, les listes, les destinations d'articles et la langue de l'app."),
                ("Directories", "Itinéraires d'archives plus clairs", "Parcourez SCP, Tales, Canons, séries Canon, GoI, Joke SCP, SCP-EX, collections, articles récents, guides et listes associées."),
                ("Search", "Recherche gratuite rapide, filtres Premium", "Ouvrez par numéro SCP, cherchez les titres et utilisez les raccourcis tags/classes d'objet. Premium ajoute documents, mémos, état de lecture, score officiel, longueur et recherches enregistrées."),
                ("Reader", "Une vue article concentrée", "Contrôles typographiques, thèmes plus calmes, mode sombre amélioré, retour en haut, instantanés hors ligne et rendu plus fidèle des pages spéciales."),
                ("Library", "Un endroit où revenir", "Historique, état de lecture, notes, favoris, à lire plus tard, position de défilement, mémos et reprise restent organisés sur votre appareil."),
                ("Share", "Partage sous forme de cartes", "Transformez un article ou une liste choisie en carte stylisée pour X et d'autres apps sociales, avec modèles et commentaire facultatif."),
                ("Premium", "Statistiques, lecture audio et hors ligne", "Statistiques de lecture, synthèse vocale, édition des mémos, limites étendues, suppression des publicités et stockage hors ligne."),
                ("Sync", "Organisation personnelle via iCloud", "Lorsque disponible, état de lecture, mémos, recherches enregistrées et dossiers de favoris se synchronisent via votre iCloud Drive. Les recherches enregistrées peuvent notifier les nouveaux résultats sur l'appareil."),
            ],
            "SCP Docs n'est pas une app officielle de la SCP Foundation ou de Wikidot. Les pages sources, crédits d'auteurs et licences des sites sources font autorité.",
            "Accueil en mode clair",
            "Accueil en mode sombre",
        ),
        "ru": (
            "Возможности — SCP Docs",
            "Обзор SCP Docs со скриншотами: Главная по филиалам, обновлённый поиск, Библиотека, ридер, карточки для публикации, сохранённые поиски, статистика и синхронизация.",
            "Находите отчёт и действительно возвращайтесь к нему",
            "SCP Docs объединяет входы в архивы, поиск, инструменты чтения и личное состояние чтения в одном нативном iOS-приложении. Последние версии превратили его в пространство для поиска, сохранения, прослушивания, публикации и отслеживания прочитанного.",
            [
                ("Branches", "Английский, японский, французский и русский архивы", "Смена филиала меняет Главную, поиск, списки, переходы к статьям и язык приложения."),
                ("Directories", "Более понятные маршруты по архиву", "Просматривайте SCP, Tales, Canons, серии Canon, GoI, Joke SCP, SCP-EX, коллекции, недавние статьи, руководства и связанные списки."),
                ("Search", "Быстрый бесплатный поиск и Premium-фильтры", "Открывайте по номеру SCP, ищите по названиям, тегам и классам объектов. Premium добавляет документы, заметки, статус чтения, официальный рейтинг, длину и сохранённые поиски."),
                ("Reader", "Сосредоточенный вид статьи", "Настройки типографики, спокойные темы, улучшенная тёмная тема, возврат наверх, офлайн-снимки и более точное отображение специальных страниц."),
                ("Library", "Место, куда можно вернуться", "История, статус чтения, оценки, закладки, «прочитать позже», позиция прокрутки, заметки и продолжение чтения остаются организованными на устройстве."),
                ("Share", "Поделиться карточками", "Превратите статью или выбранный список в карточку для X и других социальных приложений, с шаблонами и необязательным комментарием."),
                ("Premium", "Статистика, озвучивание и офлайн", "Статистика чтения, синтез речи, редактирование заметок, расширенные лимиты, скрытие рекламы и офлайн-хранение."),
                ("Sync", "Личная организация через iCloud", "Когда доступно, состояние чтения, заметки, сохранённые поиски и папки закладок синхронизируются через ваш iCloud Drive. Сохранённые поиски могут уведомлять о новых совпадениях на устройстве."),
            ],
            "SCP Docs не является официальным приложением SCP Foundation или Wikidot. Исходные страницы, сведения об авторах и лицензии на исходных сайтах остаются основным источником.",
            "Главная в светлой теме",
            "Главная в тёмной теме",
        ),
        "ko": (
            "기능 — SCP Docs",
            "SCP Docs의 지부별 홈, 새 검색, 라이브러리, 리더 도구, 공유 카드, 저장 검색, 읽기 통계, 동기화 기능을 스크린샷과 함께 소개합니다.",
            "보고서를 찾고, 나중에 제대로 돌아오기",
            "SCP Docs는 아카이브 진입점, 검색, 리더 조작, 개인 읽기 상태를 하나의 네이티브 iOS 앱에 모읍니다. 최근 버전에서는 읽기뿐 아니라 발견, 저장, 듣기, 공유, 기록까지 다루는 작업 공간으로 확장되었습니다.",
            [
                ("Branches", "영어, 일본어, 프랑스어, 러시아어 아카이브", "지부를 바꾸면 홈, 검색, 목록, 글 링크 대상, 앱 언어가 함께 바뀌어 각 아카이브의 문맥으로 읽을 수 있습니다."),
                ("Directories", "더 정리된 아카이브 경로", "SCP 글, Tales, Canons, Canon series, GoI, Joke SCP, SCP-EX, 컬렉션, 최근 글, 가이드와 관련 목록을 탐색합니다."),
                ("Search", "빠른 무료 검색과 프리미엄 필터", "SCP 번호로 바로 열고, 제목, 태그, Object Class로 찾을 수 있습니다. 프리미엄은 문서, 메모, 읽기 상태, 공식 점수, 길이, 저장 검색을 추가합니다."),
                ("Reader", "집중할 수 있는 글 보기", "타이포그래피 설정, 차분한 테마, 개선된 다크 모드, 맨 위로 이동, 오프라인 스냅샷, 특수 형식 페이지의 더 충실한 표시를 제공합니다."),
                ("Library", "다시 돌아오기 위한 장소", "기록, 읽음 상태, 평가, 북마크, 나중에 읽기, 스크롤 위치, 메모, 이어 읽기 데이터가 기기 안에서 정리됩니다."),
                ("Share", "카드로 공유", "글 하나 또는 직접 고른 목록을 X 등 소셜 앱에 공유하기 쉬운 카드로 만들 수 있습니다. 템플릿과 선택 코멘트를 지원합니다."),
                ("Premium", "통계, 음성 읽기, 오프라인", "읽기 통계, 텍스트 음성 변환, 메모 편집, 저장 한도 확장, 광고 제거, 오프라인 저장을 제공합니다."),
                ("Sync", "iCloud 기반 개인 정리", "사용 가능한 경우 읽기 상태, 메모, 저장 검색, 북마크 폴더가 사용자의 iCloud Drive를 통해 동기화됩니다. 저장 검색은 새 일치 항목을 기기 알림으로 알려 줄 수 있습니다."),
            ],
            "SCP Docs는 SCP Foundation 또는 Wikidot의 공식 앱이 아닙니다. 원본 페이지, 저자 표시, 라이선스 고지는 각 원본 사이트가 기준입니다.",
            "라이트 모드 홈",
            "다크 모드 홈",
        ),
    }
    title, description, h2, lede, cards, legal, light_caption, dark_caption = bodies[lang]
    card_html = "\n".join(
        f"""          <div class="feature-card">
            <p class="section-label">{label}</p>
            <h3>{heading}</h3>
            <p>{text}</p>
          </div>"""
        for label, heading, text in cards
    )
    body = f"""
    <main class="main-pad">
      <section aria-labelledby="feature-title">
        <p class="section-label">Feature Overview</p>
        <h2 id="feature-title" class="section-title-lg">{h2}</h2>
        <div class="feature-hero">
          <div>
            <p class="lede">{lede}</p>
            <div class="pill-row">
              <span class="code-chip">Home</span>
              <span class="code-chip">Library</span>
              <span class="code-chip">Search</span>
              <span class="code-chip">Stats</span>
              <span class="code-chip">Share cards</span>
            </div>
          </div>
          <figure class="screen-frame screen-frame-compact">
            <img src="assets/images/home-showcase.png"
              alt="SCP Docs home screen shown in light and dark appearances" />
          </figure>
        </div>
      </section>

      <section aria-labelledby="screens-title" style="margin-top:38px;">
        <p class="section-label">Screenshots</p>
        <h2 id="screens-title" class="section-title-lg">{'画面の雰囲気' if lang == 'ja' else "L'interface en un coup d'oeil" if lang == 'fr' else 'Интерфейс одним взглядом' if lang == 'ru' else '화면 한눈에 보기'}</h2>
        <div class="feature-shot-grid">
          <figure class="screen-frame">
            <img src="assets/images/home-light.png" alt="{light_caption}" />
            <figcaption>{light_caption}</figcaption>
          </figure>
          <figure class="screen-frame">
            <img src="assets/images/home-dark.png" alt="{dark_caption}" />
            <figcaption>{dark_caption}</figcaption>
          </figure>
        </div>
      </section>

      <section aria-labelledby="points-title" style="margin-top:38px;">
        <p class="section-label">What it does</p>
        <h2 id="points-title" class="section-title-lg">{'主な機能' if lang == 'ja' else 'Fonctions principales' if lang == 'fr' else 'Основные возможности' if lang == 'ru' else '주요 기능'}</h2>
        <div class="feature-grid">
{card_html}
        </div>
      </section>

      <section style="margin-top:40px;">
        <div class="card-flat">
          <p style="margin-top:0;">{legal}</p>
          <div class="pill-row">
            <a class="pill" href="{APP_STORE_URL}" target="_blank"
              rel="noopener noreferrer">App Store</a>
            <a class="pill" href="{page_file('support', lang)}">{LANGS[lang].nav['support']}</a>
            <a class="pill" href="{page_file('privacy', lang)}">{LANGS[lang].nav['privacy']}</a>
          </div>
        </div>
      </section>
    </main>"""
    return {"title": title, "description": description, "body": body}


for code in ["ja", "fr", "ru", "ko"]:
    FEATURES[code] = translated_feature(code)


PRIVACY_TEXT = {
    "en": {
        "title": "Privacy Policy — SCP Docs",
        "description": "SCP Docs Privacy Policy covering on-device data, iCloud Drive sync, saved searches, notifications, ads, subscriptions, and third-party source sites.",
        "heading": "Privacy Policy",
        "updated": "Last updated: June 24, 2026",
        "sections": [
            ("1. Introduction", "This Privacy Policy describes how information is handled in the mobile application “SCP Docs” (the “App”). Please read this Policy before using the App. If you do not agree with it, please do not use the App."),
            ("2. Operator and contact", f'For privacy-related inquiries about the App, contact:<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ("3. Overview of information we handle", "The App retains on-device state so you can browse, organize, resume, and review articles. It also performs network communications where needed for catalogs, source pages, purchases, ads, and app links. You are not required to create an account to use the App."),
            ("4. Information stored on your device", "The App may store article URLs or normalized keys, browsing history, read status, ratings, favorites, bookmarks, read-later entries, bookmark folders, scroll progress, cached titles or thumbnails, memos, saved search conditions, saved-search match state, reading-session records, reading-stat inputs, offline article HTML snapshots, subscription state, and rewarded-ad premium expiry. This data supports history, resume reading, library views, advanced search, memos, saved searches, reading stats, offline reading, and Premium status."),
            ("5. iCloud Drive sync", "If you are signed in to iCloud Drive and the feature is available, reading state, memos, saved searches, and bookmark folders may sync through your own iCloud storage. The App operator does not operate a separate server to collect these reading records or memos."),
            ("6. Network activity and notifications", "Network activity occurs when the App downloads catalog, tag, and list data, displays article bodies from Wikidot or other external sites, checks App Store subscription status, opens external links, or loads Google AdMob ads. Saved-search notifications are generated on device after catalog data is checked; notification delivery depends on iOS notification permission."),
            ("7. Advertising (Google AdMob)", 'The App uses the Google Mobile Ads SDK (AdMob), provided by Google LLC, and may display banner, inline, native, interstitial, rewarded, and similar ads. In the course of delivering ads, identifiers and device or impression information may be transmitted to Google and advertising partners for delivery, measurement, fraud prevention, and related purposes. See <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Google’s Privacy Policy</a> and <a href="https://developers.google.com/admob/ios/privacy/play-data-disclosure" rel="noopener noreferrer">Ads &amp; privacy</a>. Depending on iOS settings and your choices, personalization may be limited.'),
            ("8. Third-party sites", "Much of what you access through the App is hosted on websites operated by third parties. Their logging, cookies, analytics scripts, site rules, and privacy policies apply. We do not control how third-party sites handle information."),
            ("9. Disclosure to third parties and legal requests", "In addition to disclosures described above, such as advertising, payments, content delivery infrastructure, and diagnostics offered by OS or App Store mechanisms, we may disclose information where required by law or in response to lawful requests by courts or public authorities."),
            ("10. Security", "We endeavor to implement reasonable safeguards for the environments in which the App is built and distributed. However, security cannot be guaranteed absolutely on the Internet or mobile devices."),
            ("11. Retention", "Data stored on device or in your iCloud Drive may persist until you uninstall the App, delete data using in-app controls, remove related iCloud files, or reset the device or OS, as applicable."),
            ("12. Children", "The App is intended for general readers. If you allow a minor to use the App, please do so with appropriate parental supervision."),
            ("13. Changes to this Policy", "We may change this Policy to reflect legal requirements, App changes, or business needs. Updates will be posted on this page and, where appropriate, surfaced in the App."),
            ("14. Questions", f'Questions about this Policy: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> or <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
        ],
    },
    "ja": {
        "title": "プライバシーポリシー — SCP Docs",
        "description": "SCP Docs のプライバシーポリシー。端末内データ、iCloud Drive 同期、保存検索、通知、広告、購読、外部サイトについて説明します。",
        "heading": "プライバシーポリシー",
        "updated": "最終更新日: 2026年6月24日",
        "sections": [
            ("1. はじめに", "本プライバシーポリシーは、モバイルアプリ「SCP Docs」（以下「本アプリ」）における情報の取扱いを説明するものです。本アプリを利用する前に本ポリシーをご確認ください。同意できない場合は、本アプリを利用しないでください。"),
            ("2. 運営者と連絡先", f'本アプリのプライバシーに関するお問い合わせは、<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a> までご連絡ください。'),
            ("3. 取り扱う情報の概要", "本アプリは、記事を閲覧、整理、再開、振り返るために端末内の状態を保持します。また、カタログ、元サイトのページ、購入、広告、外部リンクに必要な範囲で通信を行います。利用にあたりアカウント作成は不要です。"),
            ("4. 端末に保存される情報", "本アプリは、記事URLまたは正規化キー、閲覧履歴、読了状態、評価、ブックマーク、お気に入り、後で読む、ブックマークフォルダ、スクロール位置、キャッシュされたタイトルやサムネイル、メモ、保存検索条件、保存検索の一致状態、読書セッション記録、読書統計の入力データ、オフライン保存HTML、購読状態、リワード広告による一時プレミアム期限などを保存することがあります。これらは履歴、続きから読む、書庫、高度な検索、メモ、保存検索、読書統計、オフライン読書、プレミアム状態のために利用されます。"),
            ("5. iCloud Drive 同期", "iCloud Drive にサインインしており機能が利用可能な場合、読書状態、メモ、保存検索、ブックマークフォルダは利用者自身の iCloud 領域を通じて同期されることがあります。アプリ運営者が、読書記録やメモを収集する専用サーバーを運用する設計ではありません。"),
            ("6. 通信と通知", "通信は、カタログ、タグ、一覧データの取得、Wikidot など外部サイトの記事本文表示、App Store 購読状態の確認、外部リンクの表示、Google AdMob 広告の読み込み時に発生します。保存検索の通知は、カタログデータ確認後に端末上で生成されます。通知の表示には iOS の通知許可が必要です。"),
            ("7. 広告（Google AdMob）", '本アプリは Google LLC が提供する Google Mobile Ads SDK（AdMob）を使用し、バナー、記事内、ネイティブ、インタースティシャル、リワード広告等を表示することがあります。広告配信の過程で、広告識別子、端末・表示環境に関する情報等が Google および広告パートナーに送信され、広告配信、測定、不正対策等に利用されることがあります。詳細は <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Google のプライバシーポリシー</a> および <a href="https://developers.google.com/admob/ios/privacy/play-data-disclosure?hl=ja" rel="noopener noreferrer">広告におけるデータ取扱いの説明</a> を参照してください。iOS 設定や利用者の選択により、パーソナライズが制限されることがあります。'),
            ("8. 第三者サイト", "本アプリを通じてアクセスする多くのコンテンツは第三者が運営するウェブサイト上にあります。ログ、Cookie、解析スクリプト、サイト規則、プライバシーポリシーは各運営者のものが適用されます。本アプリ運営者は、第三者サイトでの情報取扱いを管理しません。"),
            ("9. 第三者提供と法令上の開示", "上記の広告、決済、コンテンツ配信基盤、OS や App Store が提供する診断等に加え、法令に基づく請求または裁判所・行政機関等の適法な要請に応じて情報を開示する場合があります。"),
            ("10. セキュリティ", "本アプリの開発・配布環境について合理的な保護措置を講じるよう努めます。ただし、インターネットやモバイル端末上の安全性を完全に保証するものではありません。"),
            ("11. 保存期間", "端末または利用者の iCloud Drive に保存されたデータは、アプリの削除、アプリ内操作による削除、関連する iCloud ファイルの削除、端末や OS のリセット等が行われるまで残る場合があります。"),
            ("12. 未成年者", "本アプリは一般読者向けです。未成年者に利用させる場合は、保護者の適切な監督のもとで利用してください。"),
            ("13. 本ポリシーの変更", "法令、アプリの変更、事業上の必要に応じて本ポリシーを変更することがあります。変更後の内容は本ページに掲載し、必要に応じてアプリ内でも案内します。"),
            ("14. お問い合わせ", f'本ポリシーに関するご質問は <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> または <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a> までご連絡ください。'),
        ],
    },
}


def translated_legal(kind: str, lang: str) -> dict[str, str]:
    if kind == "privacy" and lang in PRIVACY_TEXT:
        return PRIVACY_TEXT[lang]
    privacy = {
        "fr": {
            "title": "Politique de confidentialité — SCP Docs",
            "description": "Politique de confidentialité de SCP Docs : données sur l'appareil, synchronisation iCloud Drive, recherches enregistrées, notifications, publicités, abonnements et sites sources.",
            "heading": "Politique de confidentialité",
            "updated": "Dernière mise à jour : 24 juin 2026",
            "sections": [
                ("1. Introduction", "Cette politique explique comment les informations sont traitées dans l'application mobile « SCP Docs » (l'« App »). Veuillez la lire avant d'utiliser l'App. Si vous n'êtes pas d'accord, n'utilisez pas l'App."),
                ("2. Opérateur et contact", f'Pour toute question relative à la confidentialité :<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
                ("3. Vue d'ensemble", "L'App conserve un état sur l'appareil pour parcourir, organiser, reprendre et revoir les articles. Elle communique aussi avec le réseau lorsque c'est nécessaire pour les catalogues, pages sources, achats, publicités et liens. Aucun compte n'est requis."),
                ("4. Informations stockées sur votre appareil", "L'App peut stocker des URL ou clés normalisées d'articles, historique, état de lecture, notes, favoris, éléments à lire plus tard, dossiers de favoris, position de défilement, titres ou vignettes en cache, mémos, critères de recherche enregistrée, état des résultats, sessions de lecture, données de statistiques, HTML hors ligne, état d'abonnement et expiration Premium liée à une publicité récompensée. Ces données servent à l'historique, la reprise, la bibliothèque, la recherche avancée, les mémos, les recherches enregistrées, les statistiques, la lecture hors ligne et l'état Premium."),
                ("5. Synchronisation iCloud Drive", "Si vous êtes connecté à iCloud Drive et que la fonction est disponible, l'état de lecture, les mémos, recherches enregistrées et dossiers de favoris peuvent se synchroniser via votre propre stockage iCloud. L'opérateur de l'App n'exploite pas de serveur séparé pour collecter ces données de lecture ou mémos."),
                ("6. Réseau et notifications", "Des communications ont lieu lorsque l'App télécharge les catalogues, tags et listes, affiche des articles depuis Wikidot ou d'autres sites, vérifie l'abonnement App Store, ouvre des liens externes ou charge les publicités Google AdMob. Les notifications de recherches enregistrées sont générées sur l'appareil après vérification du catalogue et dépendent de l'autorisation iOS."),
                ("7. Publicité (Google AdMob)", "L'App utilise Google Mobile Ads SDK (AdMob), fourni par Google LLC, et peut afficher bannières, publicités intégrées, natives, interstitielles, récompensées et formats similaires. Des identifiants et informations d'appareil ou d'impression peuvent être transmis à Google et ses partenaires pour diffusion, mesure et prévention de la fraude. Voir la <a href=\"https://policies.google.com/privacy\" rel=\"noopener noreferrer\">Politique de confidentialité de Google</a> et <a href=\"https://developers.google.com/admob/ios/privacy/play-data-disclosure\" rel=\"noopener noreferrer\">Ads &amp; privacy</a>. La personnalisation peut être limitée selon les réglages iOS et vos choix."),
                ("8. Sites tiers", "Une grande partie du contenu consulté via l'App est hébergée par des sites tiers. Leurs journaux, cookies, scripts d'analyse, règles et politiques de confidentialité s'appliquent. Nous ne contrôlons pas leur traitement des informations."),
                ("9. Divulgation et demandes légales", "Outre les divulgations décrites ci-dessus, publicités, paiements, infrastructure de diffusion et diagnostics OS ou App Store, nous pouvons divulguer des informations lorsque la loi l'exige ou en réponse à une demande légale d'une autorité compétente."),
                ("10. Sécurité", "Nous nous efforçons d'appliquer des mesures raisonnables aux environnements de développement et distribution de l'App. La sécurité ne peut toutefois pas être garantie absolument sur Internet ou sur appareil mobile."),
                ("11. Conservation", "Les données stockées sur appareil ou dans votre iCloud Drive peuvent rester jusqu'à désinstallation, suppression via l'App, suppression des fichiers iCloud liés, ou réinitialisation de l'appareil ou du système."),
                ("12. Mineurs", "L'App est destinée au grand public. Si vous autorisez un mineur à l'utiliser, faites-le avec une supervision parentale appropriée."),
                ("13. Modifications", "Cette politique peut changer pour refléter la loi, les changements de l'App ou des besoins opérationnels. Les mises à jour seront publiées sur cette page et, si nécessaire, signalées dans l'App."),
                ("14. Questions", f'Questions : <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> ou <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
            ],
        },
        "ru": {
            "title": "Политика конфиденциальности — SCP Docs",
            "description": "Политика конфиденциальности SCP Docs: данные на устройстве, синхронизация iCloud Drive, сохранённые поиски, уведомления, реклама, подписки и сторонние сайты.",
            "heading": "Политика конфиденциальности",
            "updated": "Последнее обновление: 24 июня 2026 г.",
            "sections": [
                ("1. Введение", "Эта политика описывает, как обрабатывается информация в мобильном приложении «SCP Docs» («Приложение»). Ознакомьтесь с ней перед использованием. Если вы не согласны, не используйте Приложение."),
                ("2. Оператор и контакт", f'По вопросам конфиденциальности:<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
                ("3. Обзор", "Приложение хранит состояние на устройстве, чтобы вы могли просматривать, упорядочивать, продолжать и анализировать статьи. Оно также использует сеть для каталогов, исходных страниц, покупок, рекламы и ссылок. Создание аккаунта не требуется."),
                ("4. Информация на устройстве", "Приложение может хранить URL или нормализованные ключи статей, историю, статус чтения, оценки, избранное, список «прочитать позже», папки закладок, позицию прокрутки, кэшированные названия или миниатюры, заметки, условия сохранённых поисков, состояние совпадений, записи сессий чтения, данные статистики, офлайн-HTML, состояние подписки и срок временного Premium после рекламы. Эти данные нужны для истории, продолжения чтения, библиотеки, расширенного поиска, заметок, сохранённых поисков, статистики, офлайн-чтения и Premium."),
                ("5. Синхронизация iCloud Drive", "Если вы вошли в iCloud Drive и функция доступна, состояние чтения, заметки, сохранённые поиски и папки закладок могут синхронизироваться через ваше собственное хранилище iCloud. Оператор Приложения не использует отдельный сервер для сбора этих записей или заметок."),
                ("6. Сеть и уведомления", "Сеть используется для загрузки каталогов, тегов и списков, отображения статей с Wikidot или других сайтов, проверки подписки App Store, открытия внешних ссылок и загрузки рекламы Google AdMob. Уведомления сохранённых поисков создаются на устройстве после проверки каталога и зависят от разрешения iOS."),
                ("7. Реклама (Google AdMob)", 'Приложение использует Google Mobile Ads SDK (AdMob), предоставляемый Google LLC, и может показывать баннеры, встроенную, нативную, межстраничную, вознаграждаемую рекламу и подобные форматы. Идентификаторы и сведения об устройстве или показах могут передаваться Google и рекламным партнёрам для показа, измерения и предотвращения мошенничества. См. <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Политику конфиденциальности Google</a> и <a href="https://developers.google.com/admob/ios/privacy/play-data-disclosure" rel="noopener noreferrer">Ads &amp; privacy</a>. Персонализация может быть ограничена настройками iOS и вашим выбором.'),
                ("8. Сторонние сайты", "Многие материалы открываются с сайтов третьих лиц. Их журналы, cookies, аналитика, правила и политики конфиденциальности применяются независимо. Мы не контролируем их обработку данных."),
                ("9. Раскрытие и законные запросы", "Помимо описанных выше случаев, реклама, платежи, инфраструктура доставки и механизмы диагностики ОС или App Store, мы можем раскрывать информацию, если это требуется законом или законным запросом суда или государственного органа."),
                ("10. Безопасность", "Мы стараемся применять разумные меры защиты к средам разработки и распространения Приложения. Однако абсолютная безопасность в Интернете и на мобильных устройствах невозможна."),
                ("11. Хранение", "Данные на устройстве или в вашем iCloud Drive могут сохраняться до удаления Приложения, удаления через настройки Приложения, удаления связанных файлов iCloud или сброса устройства или ОС."),
                ("12. Дети", "Приложение предназначено для широкой аудитории. Если несовершеннолетний использует его, обеспечьте надлежащий родительский контроль."),
                ("13. Изменения", "Мы можем изменять эту политику из-за требований закона, изменений Приложения или операционных нужд. Обновления публикуются на этой странице и, при необходимости, отображаются в Приложении."),
                ("14. Вопросы", f'Вопросы: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> или <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
            ],
        },
        "ko": {
            "title": "개인정보 처리방침 — SCP Docs",
            "description": "SCP Docs 개인정보 처리방침: 기기 내 데이터, iCloud Drive 동기화, 저장 검색, 알림, 광고, 구독, 제3자 원본 사이트에 대한 설명.",
            "heading": "개인정보 처리방침",
            "updated": "최종 업데이트: 2026년 6월 24일",
            "sections": [
                ("1. 소개", "이 개인정보 처리방침은 모바일 애플리케이션 “SCP Docs”(이하 “앱”)에서 정보가 어떻게 처리되는지 설명합니다. 앱을 사용하기 전에 이 방침을 읽어 주세요. 동의하지 않는 경우 앱을 사용하지 마세요."),
                ("2. 운영자 및 연락처", f'앱의 개인정보 관련 문의:<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
                ("3. 처리하는 정보의 개요", "앱은 글을 탐색, 정리, 이어 읽기, 되돌아보기 위해 기기 내 상태를 저장합니다. 또한 카탈로그, 원본 페이지, 구매, 광고, 외부 링크에 필요한 경우 네트워크 통신을 수행합니다. 앱 사용에 계정 생성은 필요하지 않습니다."),
                ("4. 기기에 저장되는 정보", "앱은 글 URL 또는 정규화된 키, 열람 기록, 읽음 상태, 평가, 즐겨찾기, 북마크, 나중에 읽기, 북마크 폴더, 스크롤 위치, 캐시된 제목 또는 썸네일, 메모, 저장 검색 조건, 저장 검색 일치 상태, 읽기 세션 기록, 읽기 통계 입력 데이터, 오프라인 글 HTML, 구독 상태, 리워드 광고 임시 프리미엄 만료 정보를 저장할 수 있습니다. 이 데이터는 기록, 이어 읽기, 라이브러리, 고급 검색, 메모, 저장 검색, 읽기 통계, 오프라인 읽기, 프리미엄 상태에 사용됩니다."),
                ("5. iCloud Drive 동기화", "iCloud Drive에 로그인되어 있고 기능을 사용할 수 있는 경우 읽기 상태, 메모, 저장 검색, 북마크 폴더가 사용자의 iCloud 저장 공간을 통해 동기화될 수 있습니다. 앱 운영자는 이러한 읽기 기록이나 메모를 수집하기 위한 별도 서버를 운영하지 않습니다."),
                ("6. 네트워크 활동 및 알림", "앱은 카탈로그, 태그, 목록 데이터를 다운로드할 때, Wikidot 등 외부 사이트의 글 본문을 표시할 때, App Store 구독 상태를 확인할 때, 외부 링크를 열 때, Google AdMob 광고를 로드할 때 네트워크를 사용합니다. 저장 검색 알림은 카탈로그 확인 후 기기에서 생성되며, iOS 알림 권한에 따라 표시됩니다."),
                ("7. 광고(Google AdMob)", '앱은 Google LLC가 제공하는 Google Mobile Ads SDK(AdMob)를 사용하며 배너, 인라인, 네이티브, 전면, 리워드 및 유사한 광고 형식을 표시할 수 있습니다. 광고 제공 과정에서 식별자와 기기 또는 노출 관련 정보가 Google 및 광고 파트너에게 전송되어 광고 제공, 측정, 부정행위 방지 등에 사용될 수 있습니다. 자세한 내용은 <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Google 개인정보처리방침</a> 및 <a href="https://developers.google.com/admob/ios/privacy/play-data-disclosure" rel="noopener noreferrer">Ads &amp; privacy</a>를 참조하세요. iOS 설정과 사용자의 선택에 따라 개인화가 제한될 수 있습니다.'),
                ("8. 제3자 사이트", "앱을 통해 접근하는 많은 콘텐츠는 제3자가 운영하는 웹사이트에 호스팅됩니다. 해당 사이트의 로그, 쿠키, 분석 스크립트, 사이트 규칙, 개인정보 처리방침이 적용됩니다. 우리는 제3자 사이트의 정보 처리를 통제하지 않습니다."),
                ("9. 제3자 제공 및 법적 요청", "위에서 설명한 광고, 결제, 콘텐츠 제공 인프라, OS 또는 App Store 진단 메커니즘 외에도, 법률상 요구되거나 법원 또는 공공기관의 적법한 요청이 있는 경우 정보를 공개할 수 있습니다."),
                ("10. 보안", "앱이 개발 및 배포되는 환경에 합리적인 보호 조치를 적용하기 위해 노력합니다. 다만 인터넷 또는 모바일 기기에서의 보안을 절대적으로 보장할 수는 없습니다."),
                ("11. 보관", "기기 또는 사용자의 iCloud Drive에 저장된 데이터는 앱 삭제, 앱 내 삭제 기능 사용, 관련 iCloud 파일 삭제, 기기 또는 OS 재설정 전까지 남아 있을 수 있습니다."),
                ("12. 아동", "앱은 일반 독자를 대상으로 합니다. 미성년자가 앱을 사용하는 경우 보호자의 적절한 감독하에 사용하도록 해 주세요."),
                ("13. 방침 변경", "법적 요구, 앱 변경, 운영상 필요에 따라 이 방침을 변경할 수 있습니다. 변경 사항은 이 페이지에 게시되며 필요한 경우 앱 내에서도 안내됩니다."),
                ("14. 문의", f'이 방침에 관한 문의: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> 또는 <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
            ],
        },
    }
    return privacy[lang]


for code in ["fr", "ru", "ko"]:
    PRIVACY_TEXT[code] = translated_legal("privacy", code)


TERMS_TEXT = {
    "en": {
        "title": "Terms of Use — SCP Docs",
        "description": "SCP Docs Terms of Use covering unofficial status, source content licensing, Premium subscriptions, rewarded unlocks, third-party services, and disclaimers.",
        "heading": "Terms of Use",
        "updated": "Last updated: June 24, 2026",
        "sections": [
            ("1. Scope and acceptance", "These Terms of Use (the “Terms”) govern your use of the mobile application “SCP Docs” (the “App”). By downloading or using the App, you agree to be bound by these Terms."),
            ("2. Nature of the service", "The App is not an official application provided or endorsed by the SCP Foundation, Wikidot, Inc., or any official operator of referenced content. It is unofficial, fan-made software. References to names or fictional universes are for convenience only and do not imply partnership, endorsement, or agency."),
            ("3. Content and licensing", 'Much of the text and imagery accessible through the App is published by individual contributors under licenses such as Creative Commons Attribution-ShareAlike 3.0 Unported (<strong>CC BY-SA 3.0</strong>). The full <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">license text</a> is available from Creative Commons. If you reproduce, redistribute, or modify articles or other materials, you must comply with the applicable license and each source site\'s rules. The App itself is not the licensor of third-party content.'),
            ("4. App features and personal data", "The App provides archive browsing, branch-aware search, reading state, bookmarks, read-later, ratings, memos, share cards, saved searches, reading stats, text-to-speech, offline snapshots, and related reader tools. Data handling is described in the Privacy Policy."),
            ("5. Purchases, subscriptions, and rewarded unlocks", "Premium features may be provided through auto-renewing subscriptions, other in-app purchases, or temporary rewarded-ad unlocks where available. Apple Inc. handles subscription purchase processing, billing, cancellation, refunds, and related matters through the App Store. A rewarded ad unlock, when offered, grants only temporary access and does not replace a subscription. Feature availability and limits may change with App updates or App Store review requirements."),
            ("6. Third-party services and external sites", "The App relies on App Store payment infrastructure, advertising platforms, iCloud Drive where enabled, and websites operated by third parties. Each such service is governed by its own terms and privacy policy. Source sites remain authoritative for article text, authorship, licenses, warnings, and site rules."),
            ("7. Prohibited uses", "You agree not to violate applicable law or public policy, infringe third-party rights, place an undue load on the App or related infrastructure, attempt unauthorized redistribution or decompilation, bypass purchase or advertising mechanisms, or engage in conduct the operator reasonably determines inappropriate."),
            ("8. Disclaimers and limitation of liability", "The App is provided “AS IS.” The operator makes no warranty that the App will meet your particular requirements or be available, accurate, uninterrupted, or error-free. To the maximum extent permitted by applicable law, the operator shall not be liable for damages arising from the App, except in cases of willful misconduct or gross negligence."),
            ("9. Changes to the Terms", "The operator may revise these Terms as needed. Revised Terms take effect when posted on this page or surfaced through the App, where appropriate."),
            ("10. Governing law and venue", "These Terms apply in light of applicable law and agreements with platform providers such as Apple. Disputes shall be resolved under the relevant governing law. If a specific governing law or venue must be stated, this section may be updated or supplemented."),
            ("11. Contact", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
        ],
    },
}


def make_terms(lang: str) -> dict[str, str]:
    if lang == "en":
        return TERMS_TEXT["en"]
    data = {
        "ja": (
            "利用規約 — SCP Docs",
            "SCP Docs の利用規約。非公式性、元コンテンツのライセンス、プレミアム購読、リワード解放、第三者サービス、免責事項を説明します。",
            "利用規約",
            "最終更新日: 2026年6月24日",
            [
                ("1. 適用範囲と同意", "本利用規約（以下「本規約」）は、モバイルアプリ「SCP Docs」（以下「本アプリ」）の利用に適用されます。本アプリをダウンロードまたは利用することで、本規約に同意したものとみなされます。"),
                ("2. サービスの性質", "本アプリは、SCP Foundation、Wikidot, Inc.、または参照されるコンテンツの公式運営者が提供・承認する公式アプリではありません。非公式のファンメイドソフトウェアです。名称や架空世界への言及は便宜上のものであり、提携、承認、代理関係を意味しません。"),
                ("3. コンテンツとライセンス", '本アプリを通じてアクセスできる多くのテキストや画像は、Creative Commons Attribution-ShareAlike 3.0 Unported（<strong>CC BY-SA 3.0</strong>）等のライセンスの下で各投稿者により公開されています。<a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">ライセンス全文</a>は Creative Commons にて確認できます。記事や素材を転載、再配布、改変する場合は、該当ライセンスと各提供元サイトの規則に従う必要があります。本アプリ自体は第三者コンテンツの許諾主体ではありません。'),
                ("4. アプリ機能と個人データ", "本アプリは、書庫閲覧、支部対応検索、読書状態、ブックマーク、後で読む、評価、メモ、共有カード、保存検索、読書統計、読み上げ、オフライン保存などの読書ツールを提供します。データの取扱いはプライバシーポリシーに記載します。"),
                ("5. 購入、購読、リワード解放", "プレミアム機能は、自動更新購読、その他のアプリ内購入、または利用可能な場合のリワード広告による一時解放として提供されることがあります。購読の購入処理、請求、キャンセル、返金等は Apple Inc. が App Store を通じて取り扱います。リワード広告による解放は一時的なアクセスであり、購読の代替ではありません。機能の内容や上限は、アプリ更新や App Store 審査要件により変更される場合があります。"),
                ("6. 第三者サービスと外部サイト", "本アプリは App Store の決済基盤、広告プラットフォーム、有効な場合の iCloud Drive、第三者が運営するウェブサイトに依存します。各サービスにはそれぞれの利用規約とプライバシーポリシーが適用されます。記事本文、著者、ライセンス、警告、サイト規則については提供元サイトが正本です。"),
                ("7. 禁止事項", "利用者は、法令または公序良俗に反する行為、第三者の権利侵害、本アプリまたは関連インフラへの過度な負荷、無断再配布や逆コンパイル、購入・広告機構の回避、その他運営者が合理的に不適切と判断する行為を行ってはなりません。"),
                ("8. 免責と責任制限", "本アプリは現状有姿で提供されます。運営者は、本アプリが利用者の特定の要求を満たすこと、利用可能であること、正確であること、中断やエラーがないことを保証しません。適用法で認められる最大限の範囲で、運営者は本アプリに起因する損害について責任を負いません。ただし、運営者の故意または重過失による場合を除きます。"),
                ("9. 規約の変更", "運営者は必要に応じて本規約を改定できます。改定後の規約は、本ページに掲載された時点、または必要に応じてアプリ内で案内された時点で効力を生じます。"),
                ("10. 準拠法と管轄", "本規約は、適用法および Apple 等のプラットフォーム提供者との契約を踏まえて適用されます。紛争は関連する準拠法に従って解決されます。特定の準拠法または管轄を明示する必要がある場合、本節を更新または補足することがあります。"),
                ("11. 連絡先", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ],
        ),
        "fr": (
            "Conditions d'utilisation — SCP Docs",
            "Conditions d'utilisation de SCP Docs : statut non officiel, licences des contenus sources, abonnements Premium, déverrouillages récompensés, services tiers et exclusions.",
            "Conditions d'utilisation",
            "Dernière mise à jour : 24 juin 2026",
            [
                ("1. Portée et acceptation", "Ces Conditions régissent votre utilisation de l'application mobile « SCP Docs » (l'« App »). En téléchargeant ou utilisant l'App, vous acceptez ces Conditions."),
                ("2. Nature du service", "L'App n'est pas une application officielle fournie ou approuvée par la SCP Foundation, Wikidot, Inc. ou un opérateur officiel des contenus référencés. Il s'agit d'un logiciel fan non officiel. Les noms et univers fictifs sont cités par commodité et n'impliquent aucun partenariat, soutien ou mandat."),
                ("3. Contenu et licences", "Une grande partie des textes et images accessibles via l'App est publiée par des contributeurs sous des licences comme Creative Commons Attribution-ShareAlike 3.0 Unported (<strong>CC BY-SA 3.0</strong>). Le <a href=\"https://creativecommons.org/licenses/by-sa/3.0/\" rel=\"noopener noreferrer\">texte complet de la licence</a> est disponible chez Creative Commons. Toute reproduction, redistribution ou modification doit respecter la licence applicable et les règles du site source. L'App elle-même n'est pas le concédant des contenus tiers."),
                ("4. Fonctions de l'App et données personnelles", "L'App propose navigation d'archives, recherche par branche, état de lecture, favoris, à lire plus tard, notes, mémos, cartes de partage, recherches enregistrées, statistiques, synthèse vocale, instantanés hors ligne et outils associés. Le traitement des données est décrit dans la Politique de confidentialité."),
                ("5. Achats, abonnements et déverrouillages récompensés", "Les fonctions Premium peuvent être fournies par abonnement renouvelable, autre achat intégré ou déverrouillage temporaire via publicité récompensée lorsque disponible. Apple Inc. traite les achats, facturation, annulations, remboursements et sujets liés via l'App Store. Un déverrouillage récompensé donne seulement un accès temporaire et ne remplace pas un abonnement. Les fonctions et limites peuvent changer avec les mises à jour ou exigences de revue App Store."),
                ("6. Services tiers et sites externes", "L'App dépend de l'infrastructure de paiement App Store, de plateformes publicitaires, d'iCloud Drive lorsque activé et de sites web tiers. Chaque service est régi par ses propres conditions et politiques. Les sites sources font autorité pour texte, auteurs, licences, avertissements et règles."),
                ("7. Usages interdits", "Vous acceptez de ne pas violer la loi ou l'ordre public, porter atteinte aux droits de tiers, surcharger l'App ou l'infrastructure, redistribuer ou décompiler sans autorisation, contourner les achats ou publicités, ou adopter une conduite jugée raisonnablement inappropriée par l'opérateur."),
                ("8. Exclusions et responsabilité", "L'App est fournie « en l'état ». L'opérateur ne garantit pas qu'elle répondra à vos besoins, sera disponible, exacte, ininterrompue ou sans erreur. Dans la mesure permise par la loi, l'opérateur n'est pas responsable des dommages liés à l'App, sauf faute intentionnelle ou négligence grave."),
                ("9. Modifications", "L'opérateur peut réviser ces Conditions si nécessaire. Les Conditions révisées prennent effet lorsqu'elles sont publiées sur cette page ou signalées dans l'App lorsque approprié."),
                ("10. Loi applicable et juridiction", "Ces Conditions s'appliquent selon la loi applicable et les accords avec les plateformes comme Apple. Les litiges seront résolus selon la loi pertinente. Cette section peut être mise à jour si une loi ou juridiction précise doit être indiquée."),
                ("11. Contact", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ],
        ),
        "ru": (
            "Условия использования — SCP Docs",
            "Условия использования SCP Docs: неофициальный статус, лицензии исходного контента, Premium-подписки, временные рекламные разблокировки, сторонние сервисы и отказ от гарантий.",
            "Условия использования",
            "Последнее обновление: 24 июня 2026 г.",
            [
                ("1. Область и согласие", "Эти Условия регулируют использование мобильного приложения «SCP Docs» («Приложение»). Скачивая или используя Приложение, вы соглашаетесь соблюдать эти Условия."),
                ("2. Характер сервиса", "Приложение не является официальным приложением SCP Foundation, Wikidot, Inc. или официальных операторов упомянутого контента. Это неофициальное фанатское ПО. Упоминание названий и вымышленных миров сделано для удобства и не означает партнёрства, одобрения или представительства."),
                ("3. Контент и лицензии", 'Многие тексты и изображения, доступные через Приложение, опубликованы авторами по лицензиям вроде Creative Commons Attribution-ShareAlike 3.0 Unported (<strong>CC BY-SA 3.0</strong>). Полный <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">текст лицензии</a> доступен у Creative Commons. При воспроизведении, распространении или изменении материалов необходимо соблюдать применимую лицензию и правила исходного сайта. Само Приложение не является лицензиаром стороннего контента.'),
                ("4. Функции и персональные данные", "Приложение предоставляет просмотр архивов, поиск по филиалам, состояние чтения, закладки, «прочитать позже», оценки, заметки, карточки для публикации, сохранённые поиски, статистику чтения, синтез речи, офлайн-снимки и связанные инструменты. Обработка данных описана в Политике конфиденциальности."),
                ("5. Покупки, подписки и рекламные разблокировки", "Premium-функции могут предоставляться через автопродлеваемые подписки, другие встроенные покупки или временные разблокировки за рекламный просмотр, если они доступны. Apple Inc. обрабатывает покупки, оплату, отмену, возвраты и связанные вопросы через App Store. Рекламная разблокировка даёт только временный доступ и не заменяет подписку. Доступность функций и лимиты могут меняться с обновлениями или требованиями проверки App Store."),
                ("6. Сторонние сервисы и сайты", "Приложение зависит от платёжной инфраструктуры App Store, рекламных платформ, iCloud Drive при включении и сайтов третьих лиц. Каждый сервис регулируется своими условиями и политиками. Исходные сайты остаются основным источником для текста статей, авторства, лицензий, предупреждений и правил."),
                ("7. Запрещённое использование", "Вы соглашаетесь не нарушать закон или общественный порядок, не нарушать права третьих лиц, не создавать чрезмерную нагрузку, не распространять и не декомпилировать без разрешения, не обходить покупки или рекламу и не совершать действия, которые оператор обоснованно считает неприемлемыми."),
                ("8. Отказ от гарантий и ответственность", "Приложение предоставляется «как есть». Оператор не гарантирует, что оно удовлетворит ваши требования, будет доступным, точным, непрерывным или безошибочным. В максимальной степени, допустимой законом, оператор не отвечает за ущерб, связанный с Приложением, кроме случаев умысла или грубой неосторожности."),
                ("9. Изменения", "Оператор может изменять эти Условия при необходимости. Обновлённые Условия вступают в силу после публикации на этой странице или уведомления в Приложении, где это уместно."),
                ("10. Применимое право и подсудность", "Эти Условия применяются с учётом применимого права и соглашений с платформами, такими как Apple. Споры решаются по соответствующему праву. Раздел может быть обновлён, если нужно указать конкретное право или место рассмотрения."),
                ("11. Контакт", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ],
        ),
        "ko": (
            "이용약관 — SCP Docs",
            "SCP Docs 이용약관: 비공식 상태, 원본 콘텐츠 라이선스, 프리미엄 구독, 리워드 임시 해제, 제3자 서비스, 면책 사항.",
            "이용약관",
            "최종 업데이트: 2026년 6월 24일",
            [
                ("1. 적용 범위 및 동의", "본 이용약관(이하 “약관”)은 모바일 애플리케이션 “SCP Docs”(이하 “앱”)의 사용에 적용됩니다. 앱을 다운로드하거나 사용하는 경우 본 약관에 동의한 것으로 간주됩니다."),
                ("2. 서비스의 성격", "앱은 SCP Foundation, Wikidot, Inc. 또는 참조되는 콘텐츠의 공식 운영자가 제공하거나 승인한 공식 앱이 아닙니다. 비공식 팬 제작 소프트웨어입니다. 명칭과 가상 세계에 대한 언급은 편의를 위한 것이며 제휴, 승인, 대리 관계를 의미하지 않습니다."),
                ("3. 콘텐츠와 라이선스", '앱을 통해 접근할 수 있는 많은 텍스트와 이미지는 각 기여자가 Creative Commons Attribution-ShareAlike 3.0 Unported(<strong>CC BY-SA 3.0</strong>) 등의 라이선스로 공개한 것입니다. 전체 <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">라이선스 문서</a>는 Creative Commons에서 확인할 수 있습니다. 글이나 자료를 복제, 재배포, 수정하는 경우 적용 라이선스와 각 원본 사이트의 규칙을 따라야 합니다. 앱 자체는 제3자 콘텐츠의 라이선스 제공자가 아닙니다.'),
                ("4. 앱 기능과 개인 데이터", "앱은 아카이브 탐색, 지부별 검색, 읽기 상태, 북마크, 나중에 읽기, 평가, 메모, 공유 카드, 저장 검색, 읽기 통계, 텍스트 음성 변환, 오프라인 스냅샷 및 관련 리더 도구를 제공합니다. 데이터 처리는 개인정보 처리방침에 설명되어 있습니다."),
                ("5. 구매, 구독, 리워드 해제", "프리미엄 기능은 자동 갱신 구독, 기타 앱 내 구매 또는 제공되는 경우 리워드 광고를 통한 임시 해제로 제공될 수 있습니다. Apple Inc.는 App Store를 통해 구독 구매 처리, 청구, 취소, 환불 및 관련 사항을 처리합니다. 리워드 광고 해제는 일시적 접근이며 구독을 대체하지 않습니다. 기능 제공 여부와 한도는 앱 업데이트 또는 App Store 심사 요구에 따라 변경될 수 있습니다."),
                ("6. 제3자 서비스 및 외부 사이트", "앱은 App Store 결제 인프라, 광고 플랫폼, 활성화된 경우 iCloud Drive, 제3자가 운영하는 웹사이트에 의존합니다. 각 서비스에는 자체 약관과 개인정보 처리방침이 적용됩니다. 글 본문, 저자, 라이선스, 경고, 사이트 규칙은 원본 사이트가 기준입니다."),
                ("7. 금지 행위", "사용자는 적용 법률 또는 공공질서를 위반하거나, 제3자의 권리를 침해하거나, 앱 또는 관련 인프라에 과도한 부하를 주거나, 무단 재배포 또는 디컴파일을 시도하거나, 구매 또는 광고 메커니즘을 우회하거나, 운영자가 합리적으로 부적절하다고 판단하는 행위를 해서는 안 됩니다."),
                ("8. 면책 및 책임 제한", "앱은 “있는 그대로” 제공됩니다. 운영자는 앱이 사용자의 특정 요구를 충족하거나, 사용 가능하거나, 정확하거나, 중단 없이 제공되거나, 오류가 없음을 보증하지 않습니다. 적용 법률이 허용하는 최대 범위에서 운영자는 앱으로 인해 발생한 손해에 대해 책임지지 않습니다. 다만 운영자의 고의 또는 중대한 과실이 있는 경우는 제외됩니다."),
                ("9. 약관 변경", "운영자는 필요에 따라 본 약관을 개정할 수 있습니다. 개정 약관은 이 페이지에 게시되거나 필요한 경우 앱 내에 표시된 때 효력이 발생합니다."),
                ("10. 준거법 및 관할", "본 약관은 적용 법률 및 Apple 등 플랫폼 제공자와의 계약을 고려하여 적용됩니다. 분쟁은 관련 준거법에 따라 해결됩니다. 특정 준거법 또는 관할을 명시해야 하는 경우 이 조항을 업데이트하거나 보완할 수 있습니다."),
                ("11. 연락처", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ],
        ),
    }
    title, description, heading, updated, sections = data[lang]
    return {"title": title, "description": description, "heading": heading, "updated": updated, "sections": sections}


for code in ["ja", "fr", "ru", "ko"]:
    TERMS_TEXT[code] = make_terms(code)


SUPPORT_TEXT = {
    "en": {
        "title": "Support — SCP Docs",
        "description": "SCP Docs support: contact, requirements, supported branches, Premium features, offline reading, ads, iCloud sync, notifications, and source-site notes.",
        "heading": "Support",
        "contact_title": "Contact",
        "contact_copy": "Feature requests, display issues, catalog problems, and feedback are accepted by email when possible. Replies may take several days.",
        "include": "Please include your iOS version, SCP Docs app version, selected branch, and the screen or action where the issue occurred.",
        "requirements": "Requirements",
        "requirements_items": [
            ("Platform", "iPhone / iPod touch. iPad behavior depends on device and OS support."),
            ("OS", "Current App Store builds target iOS 17 and later."),
            ("Network", "Required for list refreshes, online article viewing, source-site content, purchases, ads, and saved-search checks. Offline reading only works for saved snapshots."),
            ("Source sites", "Wikidot and other source-site layout changes or maintenance may cause temporary display issues or slower loading."),
        ],
        "faq_title": "Frequently asked questions",
        "faqs": [
            ("Do I need an account or login?", "No. SCP Docs is designed for browsing without a Wikidot account. Editing articles or posting comments follows each official source site's rules."),
            ("Which branches and languages are supported?", "The app currently supports the English main archive and the Japanese, French, and Russian branches. The app UI currently supports English, Japanese, French, and Russian. This website also provides Korean support pages for reference."),
            ("Lists or titles look old / cannot be fetched", "Catalog data is downloaded online and cached on your device. Check your connection, then refresh catalogs from Settings or restart the app. Some source-site changes can require a later catalog update."),
            ("What is free, and what is Premium?", "Number and title search, reading, basic library features, history, ratings, bookmarks, and read-later are available for normal use. Premium adds ad removal, advanced search, memo editing, higher save limits, offline storage, reading stats, text-to-speech, saved-search alerts, and bookmark folders with iCloud sync."),
            ("I want to read offline", "Offline saving is a Premium feature. While Premium is active, eligible saved articles can keep a local HTML snapshot. If you are offline, only articles with saved copies can be displayed; images, external resources, unsaved articles, and catalog updates still require a network connection."),
            ("I want to remove ads / I see a banner", "Ads are shown during free use, including banner, inline, native feed, interstitial, rewarded, and similar formats. While monthly Premium is active, ads are hidden. If you are not subscribed, a rewarded ad may grant temporary Premium access when available."),
            ("How do saved searches and notifications work?", "Saved searches are Premium. The app checks catalog data on device after sync and can notify you when new matching entries appear. iOS notification permission is required, and notifications are not generated by an operator-run server."),
            ("Where is my data sent?", "Reading history, progress, ratings, bookmarks, read-later, memos, reading time, folders, saved searches, offline snapshots, and rewarded-ad expiry are primarily stored on your device. If iCloud Drive is available, reading state, memos, saved searches, and bookmark folders may sync through your own iCloud storage. See the Privacy Policy for details."),
        ],
        "reference_title": "Source content remains authoritative",
        "reference_copy": "Rights, official text, author credits, warnings, and license notices are governed by each source site. SCP Docs is a reader layer that helps with navigation and personal reading state; it does not replace source-site rules.",
    },
}


def make_support(lang: str) -> dict[str, object]:
    if lang == "en":
        return SUPPORT_TEXT["en"]
    data = {
        "ja": (
            "サポート — SCP Docs",
            "SCP Docs のサポート。連絡先、動作環境、対応支部、プレミアム機能、オフライン読書、広告、iCloud同期、通知、元サイトに関する注意。",
            "サポート",
            "連絡先",
            "機能要望、表示の問題、カタログの問題、フィードバックは、可能な範囲でメールにて受け付けています。返信には数日かかる場合があります。",
            "iOS バージョン、SCP Docs のアプリバージョン、選択中の支部、問題が発生した画面や操作を記載してください。",
            "動作環境",
            [("プラットフォーム", "iPhone / iPod touch。iPad での挙動は端末と OS の対応状況に依存します。"), ("OS", "現在の App Store 版は iOS 17 以降を対象としています。"), ("通信", "一覧更新、オンライン記事表示、元サイトコンテンツ、購入、広告、保存検索チェックに必要です。オフライン読書は保存済みスナップショットがある記事のみ利用できます。"), ("元サイト", "Wikidot など提供元サイトのレイアウト変更やメンテナンスにより、一時的に表示問題や読み込み遅延が起きる場合があります。")],
            "よくある質問",
            [("アカウントやログインは必要ですか？", "不要です。SCP Docs は Wikidot アカウントなしで閲覧できるよう設計しています。記事編集やコメント投稿は、各公式サイトの規則に従います。"), ("どの支部と言語に対応していますか？", "アプリは現在、英語本家、日本、フランス、ロシア支部に対応しています。アプリUIは英語・日本語・フランス語・ロシア語に対応しています。このサイトでは参考用に韓国語ページも提供しています。"), ("一覧やタイトルが古い、取得できない", "カタログデータはオンラインで取得し、端末にキャッシュされます。通信状態を確認し、設定からカタログを更新するか、アプリを再起動してください。元サイトの変更には後続のカタログ更新が必要な場合があります。"), ("無料機能とプレミアム機能は何が違いますか？", "番号・タイトル検索、読書、基本的な書庫機能、履歴、評価、ブックマーク、後で読むは通常利用できます。プレミアムでは広告非表示、高度な検索、メモ編集、保存上限拡張、オフライン保存、読書統計、読み上げ、保存検索通知、iCloud 同期対応のブックマークフォルダが利用できます。"), ("オフラインで読みたい", "オフライン保存はプレミアム機能です。プレミアム有効中は、対象の保存済み記事にローカル HTML スナップショットを保持できます。オフライン時に表示できるのは保存済みコピーのある記事のみで、画像、外部リソース、未保存記事、カタログ更新には通信が必要です。"), ("広告を消したい / バナーが出る", "無料利用中は、バナー、記事内、ネイティブフィード、インタースティシャル、リワード広告等が表示されます。月額プレミアム有効中は広告が非表示になります。未購読の場合でも、利用可能なときはリワード広告で一時的にプレミアムを解放できます。"), ("保存検索と通知はどう動きますか？", "保存検索はプレミアム機能です。アプリはカタログ同期後に端末上で一致を確認し、新しい該当項目がある場合に通知できます。iOS の通知許可が必要で、運営者サーバーから通知を生成する仕組みではありません。"), ("自分のデータはどこへ送られますか？", "閲覧履歴、進捗、評価、ブックマーク、後で読む、メモ、読書時間、フォルダ、保存検索、オフラインスナップショット、リワード期限は基本的に端末内に保存されます。iCloud Drive が利用可能な場合、読書状態、メモ、保存検索、ブックマークフォルダは自分の iCloud 領域を通じて同期されることがあります。詳しくはプライバシーポリシーをご覧ください。")],
            "元コンテンツが正本です",
            "権利、公式本文、著者表示、警告、ライセンス表記は各提供元サイトが正本です。SCP Docs はナビゲーションと個人の読書状態を補助するリーダー層であり、元サイトの規則を置き換えるものではありません。",
        ),
        "fr": (
            "Assistance — SCP Docs",
            "Assistance SCP Docs : contact, configuration, branches prises en charge, Premium, lecture hors ligne, publicités, iCloud, notifications et sites sources.",
            "Assistance",
            "Contact",
            "Les demandes de fonctionnalités, problèmes d'affichage, soucis de catalogue et retours sont acceptés par e-mail lorsque possible. Une réponse peut prendre plusieurs jours.",
            "Indiquez votre version iOS, la version de SCP Docs, la branche sélectionnée et l'écran ou l'action concernée.",
            "Configuration requise",
            [("Plateforme", "iPhone / iPod touch. Le comportement sur iPad dépend de l'appareil et de l'OS."), ("OS", "Les versions App Store actuelles ciblent iOS 17 et ultérieur."), ("Réseau", "Requis pour actualiser les listes, lire en ligne, charger les sites sources, achats, publicités et vérifications de recherches enregistrées. Le hors ligne fonctionne uniquement avec les instantanés sauvegardés."), ("Sites sources", "Les changements de mise en page ou maintenances de Wikidot et autres sites peuvent provoquer des problèmes temporaires ou des chargements plus lents.")],
            "Questions fréquentes",
            [("Faut-il un compte ou une connexion ?", "Non. SCP Docs est conçu pour lire sans compte Wikidot. Modifier des articles ou publier des commentaires suit les règles de chaque site source."), ("Quelles branches et langues sont prises en charge ?", "L'app prend actuellement en charge l'archive principale anglaise et les branches japonaise, française et russe. L'interface de l'app prend en charge l'anglais, le japonais, le français et le russe. Ce site fournit aussi des pages coréennes de référence."), ("Les listes ou titres semblent anciens / impossible de récupérer", "Les catalogues sont téléchargés en ligne et mis en cache sur l'appareil. Vérifiez la connexion, actualisez les catalogues dans Réglages ou redémarrez l'app. Certains changements de sites sources nécessitent une mise à jour de catalogue ultérieure."), ("Qu'est-ce qui est gratuit ou Premium ?", "La recherche par numéro/titre, la lecture, les fonctions de bibliothèque de base, l'historique, les notes, favoris et éléments à lire plus tard sont utilisables normalement. Premium ajoute suppression des publicités, recherche avancée, édition des mémos, limites étendues, hors ligne, statistiques, synthèse vocale, alertes de recherches enregistrées et dossiers de favoris synchronisés via iCloud."), ("Je veux lire hors ligne", "La sauvegarde hors ligne est Premium. Pendant que Premium est actif, les articles éligibles sauvegardés peuvent conserver un instantané HTML local. Hors ligne, seuls les articles avec copie sauvegardée s'affichent ; images, ressources externes, articles non sauvegardés et mises à jour de catalogues nécessitent le réseau."), ("Je veux supprimer les publicités / je vois une bannière", "Des publicités apparaissent en usage gratuit : bannières, intégrées, natives, interstitielles, récompensées et formats similaires. Premium mensuel actif les masque. Sans abonnement, une publicité récompensée peut donner un accès Premium temporaire lorsqu'elle est disponible."), ("Comment fonctionnent recherches enregistrées et notifications ?", "Les recherches enregistrées sont Premium. L'app vérifie le catalogue sur l'appareil après synchronisation et peut notifier les nouvelles entrées correspondantes. L'autorisation iOS est requise et les notifications ne viennent pas d'un serveur de l'opérateur."), ("Où mes données sont-elles envoyées ?", "Historique, progression, notes, favoris, à lire plus tard, mémos, temps de lecture, dossiers, recherches enregistrées, instantanés hors ligne et expiration récompensée sont principalement stockés sur votre appareil. Si iCloud Drive est disponible, l'état de lecture, mémos, recherches enregistrées et dossiers peuvent se synchroniser via votre iCloud. Voir la Politique de confidentialité.")],
            "Le contenu source fait autorité",
            "Droits, texte officiel, crédits, avertissements et licences sont régis par chaque site source. SCP Docs est une couche de lecture pour la navigation et l'état personnel, sans remplacer les règles des sites sources.",
        ),
        "ru": (
            "Поддержка — SCP Docs",
            "Поддержка SCP Docs: контакты, требования, филиалы, Premium, офлайн-чтение, реклама, iCloud, уведомления и исходные сайты.",
            "Поддержка",
            "Контакт",
            "Запросы функций, проблемы отображения, каталога и отзывы по возможности принимаются по e-mail. Ответ может занять несколько дней.",
            "Укажите версию iOS, версию SCP Docs, выбранный филиал и экран или действие, где возникла проблема.",
            "Требования",
            [("Платформа", "iPhone / iPod touch. Поведение на iPad зависит от устройства и ОС."), ("OS", "Текущие сборки App Store рассчитаны на iOS 17 и новее."), ("Сеть", "Нужна для обновления списков, онлайн-чтения, исходных сайтов, покупок, рекламы и проверок сохранённых поисков. Офлайн работает только для сохранённых снимков."), ("Исходные сайты", "Изменения верстки или обслуживание Wikidot и других сайтов могут временно вызывать проблемы отображения или медленную загрузку.")],
            "Частые вопросы",
            [("Нужен ли аккаунт или вход?", "Нет. SCP Docs рассчитан на чтение без аккаунта Wikidot. Редактирование статей или комментарии подчиняются правилам исходных сайтов."), ("Какие филиалы и языки поддерживаются?", "Приложение сейчас поддерживает основной английский архив, японский, французский и русский филиалы. Интерфейс приложения поддерживает английский, японский, французский и русский. На этом сайте также есть корейские справочные страницы."), ("Списки или названия старые / не загружаются", "Каталоги скачиваются онлайн и кэшируются на устройстве. Проверьте соединение, обновите каталоги в Настройках или перезапустите приложение. Изменения исходных сайтов могут требовать последующего обновления каталога."), ("Что бесплатно, а что Premium?", "Поиск по номеру и названию, чтение, базовая библиотека, история, оценки, закладки и «прочитать позже» доступны в обычном режиме. Premium добавляет скрытие рекламы, расширенный поиск, редактирование заметок, большие лимиты, офлайн, статистику, озвучивание, уведомления сохранённых поисков и папки закладок с iCloud."), ("Хочу читать офлайн", "Офлайн-сохранение — функция Premium. Пока Premium активен, подходящие сохранённые статьи могут хранить локальный HTML-снимок. Без сети отображаются только статьи с сохранёнными копиями; изображения, внешние ресурсы, несохранённые статьи и обновления каталогов требуют сеть."), ("Хочу убрать рекламу / вижу баннер", "В бесплатном режиме могут показываться баннеры, встроенная, нативная, межстраничная, вознаграждаемая и похожая реклама. Активный месячный Premium скрывает рекламу. Без подписки рекламный просмотр может временно открыть Premium, если доступен."), ("Как работают сохранённые поиски и уведомления?", "Сохранённые поиски — Premium. Приложение проверяет каталог на устройстве после синхронизации и может уведомлять о новых совпадениях. Требуется разрешение iOS; уведомления не генерируются сервером оператора."), ("Куда отправляются мои данные?", "История, прогресс, оценки, закладки, «прочитать позже», заметки, время чтения, папки, сохранённые поиски, офлайн-снимки и срок рекламного Premium в основном хранятся на устройстве. Если доступен iCloud Drive, состояние чтения, заметки, сохранённые поиски и папки могут синхронизироваться через ваш iCloud. См. Политику конфиденциальности.")],
            "Исходный контент остаётся основным источником",
            "Права, официальный текст, авторство, предупреждения и лицензии регулируются каждым исходным сайтом. SCP Docs помогает с навигацией и личным состоянием чтения, но не заменяет правила исходных сайтов.",
        ),
        "ko": (
            "지원 — SCP Docs",
            "SCP Docs 지원: 문의, 요구 사항, 지원 지부, 프리미엄 기능, 오프라인 읽기, 광고, iCloud 동기화, 알림, 원본 사이트 안내.",
            "지원",
            "문의",
            "기능 요청, 표시 문제, 카탈로그 문제, 피드백은 가능한 경우 이메일로 받습니다. 답변까지 며칠이 걸릴 수 있습니다.",
            "iOS 버전, SCP Docs 앱 버전, 선택한 지부, 문제가 발생한 화면 또는 동작을 함께 적어 주세요.",
            "요구 사항",
            [("플랫폼", "iPhone / iPod touch. iPad 동작은 기기와 OS 지원 상태에 따라 달라집니다."), ("OS", "현재 App Store 빌드는 iOS 17 이상을 대상으로 합니다."), ("네트워크", "목록 새로고침, 온라인 글 보기, 원본 사이트 콘텐츠, 구매, 광고, 저장 검색 확인에 필요합니다. 오프라인 읽기는 저장된 스냅샷이 있는 글에만 적용됩니다."), ("원본 사이트", "Wikidot 등 원본 사이트의 레이아웃 변경이나 점검으로 일시적인 표시 문제 또는 느린 로딩이 발생할 수 있습니다.")],
            "자주 묻는 질문",
            [("계정이나 로그인이 필요한가요?", "아니요. SCP Docs는 Wikidot 계정 없이 읽을 수 있도록 설계되었습니다. 글 편집이나 댓글 작성은 각 원본 사이트의 규칙을 따릅니다."), ("어떤 지부와 언어를 지원하나요?", "앱은 현재 영어 본가 아카이브와 일본어, 프랑스어, 러시아어 지부를 지원합니다. 앱 UI는 영어, 일본어, 프랑스어, 러시아어를 지원합니다. 이 웹사이트는 참고용 한국어 페이지도 제공합니다."), ("목록이나 제목이 오래되었거나 가져올 수 없어요", "카탈로그 데이터는 온라인에서 다운로드되어 기기에 캐시됩니다. 연결을 확인한 뒤 설정에서 카탈로그를 새로고침하거나 앱을 다시 시작하세요. 원본 사이트 변경에는 이후 카탈로그 업데이트가 필요할 수 있습니다."), ("무료와 프리미엄은 무엇이 다른가요?", "번호·제목 검색, 읽기, 기본 라이브러리, 기록, 평가, 북마크, 나중에 읽기는 일반적으로 사용할 수 있습니다. 프리미엄은 광고 제거, 고급 검색, 메모 편집, 저장 한도 확장, 오프라인 저장, 읽기 통계, 텍스트 음성 변환, 저장 검색 알림, iCloud 동기화 북마크 폴더를 추가합니다."), ("오프라인으로 읽고 싶어요", "오프라인 저장은 프리미엄 기능입니다. 프리미엄이 활성화되어 있는 동안 저장 가능한 글은 로컬 HTML 스냅샷을 유지할 수 있습니다. 오프라인에서는 저장된 사본이 있는 글만 표시되며, 이미지, 외부 리소스, 저장하지 않은 글, 카탈로그 업데이트에는 네트워크가 필요합니다."), ("광고를 없애고 싶어요 / 배너가 보여요", "무료 사용 중에는 배너, 인라인, 네이티브 피드, 전면, 리워드 등 광고가 표시될 수 있습니다. 월간 프리미엄이 활성화되어 있으면 광고가 숨겨집니다. 구독하지 않은 경우 제공되는 리워드 광고로 임시 프리미엄을 받을 수 있습니다."), ("저장 검색과 알림은 어떻게 동작하나요?", "저장 검색은 프리미엄 기능입니다. 앱은 카탈로그 동기화 후 기기에서 일치 항목을 확인하고 새 결과가 있으면 알림을 표시할 수 있습니다. iOS 알림 권한이 필요하며, 운영자 서버가 알림을 생성하는 방식은 아닙니다."), ("내 데이터는 어디로 전송되나요?", "열람 기록, 진행률, 평가, 북마크, 나중에 읽기, 메모, 읽기 시간, 폴더, 저장 검색, 오프라인 스냅샷, 리워드 만료 정보는 주로 기기에 저장됩니다. iCloud Drive를 사용할 수 있으면 읽기 상태, 메모, 저장 검색, 북마크 폴더가 사용자의 iCloud 저장 공간을 통해 동기화될 수 있습니다. 자세한 내용은 개인정보 처리방침을 참조하세요.")],
            "원본 콘텐츠가 기준입니다",
            "권리, 공식 본문, 저자 표시, 경고, 라이선스 고지는 각 원본 사이트가 기준입니다. SCP Docs는 탐색과 개인 읽기 상태를 돕는 리더 계층이며, 원본 사이트 규칙을 대체하지 않습니다.",
        ),
    }
    (
        title,
        description,
        heading,
        contact_title,
        contact_copy,
        include,
        requirements,
        requirements_items,
        faq_title,
        faqs,
        reference_title,
        reference_copy,
    ) = data[lang]
    return {
        "title": title,
        "description": description,
        "heading": heading,
        "contact_title": contact_title,
        "contact_copy": contact_copy,
        "include": include,
        "requirements": requirements,
        "requirements_items": requirements_items,
        "faq_title": faq_title,
        "faqs": faqs,
        "reference_title": reference_title,
        "reference_copy": reference_copy,
    }


for code in ["ja", "fr", "ru", "ko"]:
    SUPPORT_TEXT[code] = make_support(code)


SAFETY_TEXT = {
    "en": {
        "title": "Rating & Safety Policy — SCP Docs",
        "description": "SCP Docs Rating & Safety Policy explaining App Store 13+ suitability, fictional horror themes, reader guidance, and source-site responsibility.",
        "heading": "Rating & Safety Policy",
        "updated": "Last updated: June 24, 2026",
        "sections": [
            ("1. Purpose of this page", "This page provides additional information about age suitability and content safety for the mobile application “SCP Docs” (the “App”). The App is treated as appropriate for an App Store 13+ rating."),
            ("2. Nature of the app", "The App is an unofficial browsing and reading client for public creative works from the online community commonly known as the SCP Foundation. It is not provided or endorsed by the SCP Foundation, Wikidot, Inc., or official operators of referenced content."),
            ("3. Expected content", "SCP-related works may include text-based horror, suspense, anomalous entities, fictional containment procedures, warning-style prose, tragic themes, implied violence, blood references, disturbing topics, and occasional images provided by source sites. Most content is fiction and is not intended to encourage real-world dangerous behavior."),
            ("4. Reader guidance", "The App is intended for readers aged 13 and older. Readers who are sensitive to horror or unsettling fiction, and minors using the App, should choose what they read with care. Article tags, warnings, source-site rules, and parental guidance may be relevant."),
            ("5. App controls and limits", "SCP Docs provides reader settings and navigation tools, but it does not rewrite or age-rate each source article. Parents and guardians may use iOS Screen Time, age restrictions, and content controls to manage a child's browsing environment."),
            ("6. Contact", f'Questions about age suitability or this page can be sent to <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> or <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
        ],
    },
}


def make_safety(lang: str) -> dict[str, object]:
    if lang == "en":
        return SAFETY_TEXT["en"]
    data = {
        "ja": ("Rating & Safety Policy — SCP Docs", "SCP Docs の Rating & Safety Policy。App Store 13+ 相当、フィクションとしてのホラー表現、読者向け注意、元サイト責任を説明します。", "Rating & Safety Policy", "最終更新日: 2026年6月24日", [("1. このページの目的", "このページは、モバイルアプリ「SCP Docs」（以下「本アプリ」）の年齢適合性とコンテンツ安全性について補足するものです。本アプリは App Store 13+ 相当として扱われます。"), ("2. アプリの性質", "本アプリは、SCP Foundation として知られるオンライン創作コミュニティの公開作品を閲覧・読書するための非公式クライアントです。SCP Foundation、Wikidot, Inc.、または参照コンテンツの公式運営者が提供・承認するものではありません。"), ("3. 想定されるコンテンツ", "SCP 関連作品には、テキスト中心のホラー、サスペンス、異常存在、架空の収容手順、警告風の文章、悲劇的テーマ、暗示的暴力、血液への言及、不穏な題材、元サイト由来の画像が含まれる場合があります。多くはフィクションであり、現実の危険行為を促すものではありません。"), ("4. 読者への案内", "本アプリは 13 歳以上の読者を想定しています。ホラーや不穏なフィクションに敏感な方、未成年者が利用する場合は、読む記事を慎重に選んでください。記事タグ、警告、元サイトの規則、保護者の助言が参考になります。"), ("5. アプリ側の制御と限界", "SCP Docs はリーダー設定やナビゲーションを提供しますが、各元記事を改変したり個別に年齢評価したりするものではありません。保護者は iOS のスクリーンタイム、年齢制限、コンテンツ制限を利用して閲覧環境を管理できます。"), ("6. 連絡先", f'年齢適合性や本ページに関する質問は <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> または <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a> までご連絡ください。')]),
        "fr": ("Politique de classification et de sécurité — SCP Docs", "Politique de classification et de sécurité de SCP Docs : App Store 13+, thèmes d'horreur fictionnels, conseils aux lecteurs et responsabilité des sites sources.", "Politique de classification et de sécurité", "Dernière mise à jour : 24 juin 2026", [("1. Objet de cette page", "Cette page fournit des informations supplémentaires sur l'âge conseillé et la sécurité des contenus de l'application mobile « SCP Docs » (l'« App »). L'App est traitée comme appropriée pour une classification App Store 13+."), ("2. Nature de l'App", "L'App est un client non officiel de navigation et lecture pour des œuvres créatives publiques de la communauté en ligne connue comme SCP Foundation. Elle n'est pas fournie ni approuvée par la SCP Foundation, Wikidot, Inc. ou les opérateurs officiels des contenus référencés."), ("3. Contenu attendu", "Les œuvres SCP peuvent inclure horreur textuelle, suspense, entités anormales, procédures de confinement fictionnelles, prose d'avertissement, thèmes tragiques, violence implicite, références au sang, sujets dérangeants et parfois images des sites sources. La plupart du contenu est fictionnel et ne vise pas à encourager des comportements dangereux réels."), ("4. Conseils aux lecteurs", "L'App s'adresse aux lecteurs de 13 ans et plus. Les personnes sensibles à l'horreur ou à la fiction troublante, ainsi que les mineurs, doivent choisir leurs lectures avec prudence. Tags, avertissements, règles des sites sources et supervision parentale peuvent être pertinents."), ("5. Contrôles et limites", "SCP Docs fournit des réglages de lecture et des outils de navigation, mais ne réécrit pas et ne classe pas par âge chaque article source. Parents et responsables peuvent utiliser Temps d'écran iOS, restrictions d'âge et contrôles de contenu."), ("6. Contact", f"Questions sur l'âge conseillé ou cette page : <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a> ou <a href=\"{X_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">X: @SCPdocs</a>.")]),
        "ru": ("Политика рейтинга и безопасности — SCP Docs", "Политика рейтинга и безопасности SCP Docs: App Store 13+, вымышленные хоррор-темы, рекомендации читателям и ответственность исходных сайтов.", "Политика рейтинга и безопасности", "Последнее обновление: 24 июня 2026 г.", [("1. Назначение страницы", "Эта страница содержит дополнительную информацию о возрастной пригодности и безопасности контента мобильного приложения «SCP Docs» («Приложение»). Приложение рассматривается как подходящее для рейтинга App Store 13+."), ("2. Характер приложения", "Приложение является неофициальным клиентом для просмотра и чтения публичных творческих работ онлайн-сообщества, известного как SCP Foundation. Оно не предоставлено и не одобрено SCP Foundation, Wikidot, Inc. или официальными операторами упомянутого контента."), ("3. Ожидаемый контент", "Материалы SCP могут включать текстовый хоррор, саспенс, аномальные сущности, вымышленные процедуры содержания, предупреждающий стиль, трагические темы, подразумеваемое насилие, упоминания крови, тревожные темы и иногда изображения с исходных сайтов. Большинство материалов является вымыслом и не предназначено для поощрения опасного поведения в реальности."), ("4. Рекомендации читателям", "Приложение предназначено для читателей 13 лет и старше. Читателям, чувствительным к хоррору или тревожной художественной прозе, а также несовершеннолетним, следует внимательно выбирать материалы. Теги, предупреждения, правила исходных сайтов и родительский контроль могут быть важны."), ("5. Контроли и ограничения", "SCP Docs предоставляет настройки чтения и навигацию, но не переписывает и не присваивает возрастной рейтинг каждой исходной статье. Родители и опекуны могут использовать Экранное время iOS, возрастные ограничения и контент-фильтры."), ("6. Контакт", f'Вопросы о возрастной пригодности или этой странице: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> или <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.')]),
        "ko": ("등급 및 안전 정책 — SCP Docs", "SCP Docs 등급 및 안전 정책: App Store 13+ 적합성, 픽션 호러 주제, 독자 안내, 원본 사이트 책임에 대한 설명.", "등급 및 안전 정책", "최종 업데이트: 2026년 6월 24일", [("1. 이 페이지의 목적", "이 페이지는 모바일 애플리케이션 “SCP Docs”(이하 “앱”)의 연령 적합성과 콘텐츠 안전성에 대한 추가 정보를 제공합니다. 앱은 App Store 13+ 등급에 적합한 것으로 취급됩니다."), ("2. 앱의 성격", "앱은 SCP Foundation으로 알려진 온라인 창작 커뮤니티의 공개 작품을 탐색하고 읽기 위한 비공식 클라이언트입니다. SCP Foundation, Wikidot, Inc. 또는 참조 콘텐츠의 공식 운영자가 제공하거나 승인한 것이 아닙니다."), ("3. 예상되는 콘텐츠", "SCP 관련 작품에는 텍스트 기반 호러, 서스펜스, 변칙 존재, 가상의 격리 절차, 경고문 형식, 비극적 주제, 암시적 폭력, 피에 대한 언급, 불편할 수 있는 소재, 원본 사이트의 이미지가 포함될 수 있습니다. 대부분은 픽션이며 현실의 위험한 행동을 장려하려는 것이 아닙니다."), ("4. 독자 안내", "앱은 13세 이상 독자를 대상으로 합니다. 호러나 불안한 픽션에 민감한 독자와 미성년자는 읽을 글을 신중히 선택해야 합니다. 글 태그, 경고, 원본 사이트 규칙, 보호자 지도가 도움이 될 수 있습니다."), ("5. 앱의 제어와 한계", "SCP Docs는 리더 설정과 탐색 도구를 제공하지만 각 원본 글을 다시 쓰거나 개별적으로 연령 등급을 매기지는 않습니다. 보호자는 iOS 스크린 타임, 연령 제한, 콘텐츠 제어를 사용해 자녀의 탐색 환경을 관리할 수 있습니다."), ("6. 문의", f'연령 적합성 또는 이 페이지에 관한 문의는 <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> 또는 <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>로 보내 주세요.')]),
    }
    title, description, heading, updated, sections = data[lang]
    return {"title": title, "description": description, "heading": heading, "updated": updated, "sections": sections}


for code in ["ja", "fr", "ru", "ko"]:
    SAFETY_TEXT[code] = make_safety(code)


def prose_page(data: dict[str, object], page: str, lang: str) -> str:
    lang_links = " · ".join(
        f'<a href="{page_file(page, code)}" hreflang="{code}">{LANGS[code].label}</a>'
        for code in LANGS
        if code != lang
    )
    sections = "\n".join(
        f"""      <section>
        <h2>{title}</h2>
        <p>{text}</p>
      </section>"""
        for title, text in data["sections"]
    )
    return f"""
    <article class="prose layout" style="padding-top:8px;">
      <p class="ft-muted" style="margin-top:0;">{lang_links} · {data["updated"]}</p>
{sections}
    </article>"""


def support_body(data: dict[str, object], lang: str) -> str:
    req_items = "\n".join(
        f'            <li><strong>{k}</strong>: {v}</li>' for k, v in data["requirements_items"]
    )
    faq_items = "\n".join(
        f"""            <dt>{q}</dt>
            <dd>{a}</dd>"""
        for q, a in data["faqs"]
    )
    return f"""
    <main class="main-pad layout" style="padding-top:12px;">
      <section aria-labelledby="contact-title">
        <p class="section-label">Contact</p>
        <h2 id="contact-title" class="section-title-lg">{data["contact_title"]}</h2>
        <div class="card-invert">
          <p class="lede" style="margin-top:0;">{data["contact_copy"]}</p>
          <p style="margin-bottom:0;">
            <strong>E-mail:</strong> <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br />
            <strong>X:</strong> <a href="{X_URL}" target="_blank" rel="noopener noreferrer">@SCPdocs</a>
          </p>
        </div>
        <p class="ft-muted">{data["include"]}</p>
      </section>

      <section aria-labelledby="env-title" style="margin-top:36px;">
        <p class="section-label">Environment</p>
        <h2 id="env-title" class="section-title-lg">{data["requirements"]}</h2>
        <div class="card">
          <ul class="ft-list">
{req_items}
          </ul>
        </div>
      </section>

      <section aria-labelledby="faq-title" style="margin-top:36px;">
        <p class="section-label">FAQ</p>
        <h2 id="faq-title" class="section-title-lg">{data["faq_title"]}</h2>
        <div class="card">
          <dl class="dl-flat">
{faq_items}
          </dl>
        </div>
      </section>

      <section aria-labelledby="official-title" style="margin-top:36px;">
        <p class="section-label">Reference</p>
        <h2 id="official-title" class="section-title-lg">{data["reference_title"]}</h2>
        <div class="card">
          <p>{data["reference_copy"]}</p>
          <p class="ft-muted" style="margin-bottom:0;">
            <a href="{page_file('terms', lang)}">{LANGS[lang].nav['terms']}</a> ·
            <a href="{page_file('rating-safety', lang)}">{LANGS[lang].nav['rating-safety']}</a> ·
            <a href="{page_file('privacy', lang)}">{LANGS[lang].nav['privacy']}</a>
          </p>
        </div>
      </section>
    </main>"""


def write_pages() -> None:
    for lang in LANGS:
        index = INDEX[lang]
        (ROOT / page_file("index", lang)).write_text(
            layout(
                "index",
                lang,
                title=index["title"],
                description=index["description"],
                brand_line="File: SCP-DOCS-APP / Level 2 clearance",
                h1="SCP Docs",
                page_title=LANGS[lang].nav["index"],
                body=index["body"],
                og_type="website",
                image=True,
            ),
            encoding="utf-8",
        )

        features = FEATURES[lang]
        (ROOT / page_file("features", lang)).write_text(
            layout(
                "features",
                lang,
                title=features["title"],
                description=features["description"],
                brand_line="Field Guide / Feature Brief",
                h1="SCP Docs",
                page_title=LANGS[lang].nav["features"],
                body=features["body"],
                image=True,
            ),
            encoding="utf-8",
        )

        privacy = PRIVACY_TEXT[lang]
        (ROOT / page_file("privacy", lang)).write_text(
            layout(
                "privacy",
                lang,
                title=privacy["title"],
                description=privacy["description"],
                brand_line="Legal / Privacy",
                h1=privacy["heading"],
                page_title=LANGS[lang].nav["privacy"],
                body=prose_page(privacy, "privacy", lang),
            ),
            encoding="utf-8",
        )

        support = SUPPORT_TEXT[lang]
        (ROOT / page_file("support", lang)).write_text(
            layout(
                "support",
                lang,
                title=support["title"],
                description=support["description"],
                brand_line="Help / Channel",
                h1=support["heading"],
                page_title=LANGS[lang].nav["support"],
                body=support_body(support, lang),
            ),
            encoding="utf-8",
        )

        terms = TERMS_TEXT[lang]
        (ROOT / page_file("terms", lang)).write_text(
            layout(
                "terms",
                lang,
                title=terms["title"],
                description=terms["description"],
                brand_line="Legal / Terms",
                h1=terms["heading"],
                page_title=LANGS[lang].nav["terms"],
                body=prose_page(terms, "terms", lang),
            ),
            encoding="utf-8",
        )

        safety = SAFETY_TEXT[lang]
        (ROOT / page_file("rating-safety", lang)).write_text(
            layout(
                "rating-safety",
                lang,
                title=safety["title"],
                description=safety["description"],
                brand_line="Legal / Rating & Safety",
                h1=safety["heading"],
                page_title=LANGS[lang].nav["rating-safety"],
                body=prose_page(safety, "rating-safety", lang),
            ),
            encoding="utf-8",
        )

    for name, target, title in [
        ("privacy-en.html", "privacy.html", "Redirecting to Privacy Policy - SCP Docs"),
        ("terms-en.html", "terms.html", "Redirecting to Terms of Use - SCP Docs"),
    ]:
        (ROOT / name).write_text(
            dedent(
                f"""\
                <!DOCTYPE html>
                <html lang="en">

                <head>
                  <meta charset="utf-8" />
                  <meta name="viewport" content="width=device-width, initial-scale=1" />
                  <meta http-equiv="refresh" content="0; url={target}" />
                  <link rel="canonical" href="{BASE_URL}/{target}" />
                  <title>{title}</title>
                  <script>
                    window.location.replace("{target}");
                  </script>
                </head>

                <body>
                  <p>Redirecting to <a href="{target}">{target}</a>.</p>
                </body>

                </html>
                """
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    write_pages()
