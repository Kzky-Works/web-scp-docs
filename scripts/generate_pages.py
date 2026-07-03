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

# Minimal "containment marker" favicon, URL-encoded inline SVG.
FAVICON_SVG = (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='12' fill='%230a0c0e'/%3E"
    "%3Ccircle cx='32' cy='34' r='15' fill='none' stroke='%23e13030' stroke-width='5'/%3E"
    "%3Crect x='28' y='8' width='8' height='12' fill='%23e13030'/%3E"
    "%3Ccircle cx='32' cy='34' r='5' fill='%23e13030'/%3E"
    "%3C/svg%3E"
)


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
    "es": Language(
        code="es",
        suffix="-es",
        label="ES",
        html_lang="es",
        og_locale="es_ES",
        switch_label="Idioma",
        switch_aria="Selector de idioma",
        nav={
            "index": "Inicio",
            "features": "Funciones",
            "privacy": "Privacidad",
            "support": "Soporte",
            "terms": "Términos",
            "rating-safety": "Seguridad",
        },
        footer_back="Volver al inicio",
        footer_contact="Contacto",
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


def screenshot_path(lang_code: str, kind: str) -> str:
    # No Spanish screenshots exist yet; the app UI does not include Spanish,
    # so Spanish pages show the English screens.
    shot_lang = "en" if lang_code == "es" else lang_code
    return f"assets/images/{kind}-{shot_lang}.png"


def screenshot_url(lang_code: str, kind: str) -> str:
    return f"{BASE_URL}/{screenshot_path(lang_code, kind)}"


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
        image_url = screenshot_url(lang_code, "home")
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
  <meta name="theme-color" content="#0a0c0e" />
  <link rel="icon" href="data:image/svg+xml,{FAVICON_SVG}" />
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


INDEX_STRINGS: dict[str, dict[str, object]] = {
    "en": {
        "title": "SCP Docs — Foundation Archive Reader for iPhone",
        "description": "SCP Docs is an unofficial native iOS reader for SCP Wiki archives with branch directories, guided archive browsing, Library organization, saved searches, sharing, and premium reading tools.",
        "lede": "SCP Docs is an <strong>unofficial fan-made iOS reader</strong> for SCP Wiki and branch-site articles. It turns public source pages into a native archive workspace: browse branch directories, search by number or title, save important files, organize them in your Library, and return to the exact reports you were reading.",
        "hero_alt": "English SCP Docs home screen with continue reading, archive routes, and search filters",
        "cta_main": "Get on the App Store",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "Explore the features",
        "cta2_sub": "Field guide",
        "badges": ["Unofficial fan app", "Free + Premium", "Rated 13+", "No account needed"],
        "stats": [
            ("5", "archive branches"),
            ("10+", "directory routes"),
            ("0", "accounts required"),
            ("17+", "built for iOS"),
        ],
        "screens_title": "Screens that match the workflow",
        "screens": [
            ("home", "Home screen with branch selection, continue reading, archive routes, and quick filters", "Home: branch, archive routes, and continue reading"),
            ("catalog", "SCP catalog list with article rows, series filters, and block filters", "Catalog: browse articles before you know the number"),
            ("library", "Library history screen with read status, ratings, bookmarks, quick actions, and sort controls", "Library: history, ratings, bookmarks, and saved state"),
            ("search", "Search screen with number, keyword, tag, site, type, Object Class, and advanced filters", "Search: number, keyword, tag, and advanced filters"),
        ],
        "workspace_title": "Browse the archive, then keep your place",
        "workspace_p1": "The app is organized around Home, Library, Search, and Settings. Home acts as the archive entry point, with continue-reading, quick search presets, random discovery, and directory routes for SCP reports, Tales, Canons, Canon series, Groups of Interest, guides, and related collections.",
        "workspace_p2": "Library turns browsing into a personal shelf. History, read status, ratings, bookmarks, read-later items, scroll position, memos, folders, and resume-reading data stay tied to the articles you open, so your path through the archive remains visible on device.",
        "scope_title": "Five branches, one archive workflow",
        "scope_p": "SCP Docs supports the English main SCP Foundation archive plus the Japanese, French, Russian, and Korean branches. Switching branches changes Home, search, in-app lists, article destinations, and the app UI language. SCP International and translated archive entry points are listed where catalog data is available.",
        "scope_items": [
            ("Archive lists", "Start from branch-aware directories for SCP articles, Tales, Canons, Canon series, GoI, Joke SCPs, SCP-EX, collections, recent articles, and related routes."),
            ("Search", "Jump directly by number or title for free; Premium adds advanced filters across documents, tags, Object Class, memos, reading status, official score, length, and saved searches."),
            ("Library", "Save articles as bookmarks or read-later items, rate them, add memos, group favorites into folders, and resume from stored scroll positions."),
            ("Reader", "Cleaner typography, themes, scroll tools, better dark mode, and more faithful rendering for specially formatted source pages."),
        ],
        "premium_title": "Tools for deeper reading",
        "premium_cols": [
            [
                ("Reading stats", "Reading time, catalog coverage, frequently read Object Classes and tags, rating trends, memo insights, backlog status, and logs by day, month, and year."),
                ("Saved searches", "Save search conditions and receive on-device notifications when new matching catalog entries appear."),
                ("Bookmark folders", "Organize saved articles into folders that can sync through your own iCloud Drive, along with memos and saved searches."),
            ],
            [
                ("Listen and save", "Text-to-speech reads article text aloud, and offline snapshots keep eligible saved articles available without a connection."),
                ("Share as cards", "Turn an article or selected list into a styled share card for X and other social apps, with templates and optional comments."),
                ("Ads and limits", "Premium hides ads, expands save limits, unlocks memo editing, and enables advanced search. A rewarded ad can grant temporary Premium access when available."),
            ],
        ],
        "req_title": "System requirements",
        "req_items": [
            ("OS", "iOS 17 or later."),
            ("Network", "required for catalog refresh, online article viewing, source-site content, ads, purchase checks, and app links."),
            ("Accounts", "no SCP Foundation or Wikidot account is required for reading in the app."),
        ],
        "cta_title": "Open the archive",
        "legal_p": "SCP Docs is an <strong>unofficial fan application</strong>. Source articles, author credits, copyright notices, and licensing terms remain governed by the source sites. SCP-related works are commonly published under Creative Commons BY-SA 3.0, but each source page is authoritative.",
        "store_name": "SCP Docs for iPhone",
        "store_note": "Built for iOS 17 and later. App UI currently supports English, Japanese, French, Russian, and Korean.",
        "store_main": "Get on the App Store",
    },
    "ja": {
        "title": "SCP Docs — Foundation Archive Reader for iPhone",
        "description": "SCP Docs は SCP Wiki と各支部の記事を快適に読むための非公式 iOS リーダーです。支部対応検索、読書状態、共有カード、保存検索、読書統計などに対応します。",
        "lede": "SCP Docs は、SCP Wiki と各支部サイトの記事をより快適に読むための<strong>非公式ファンメイド iOS リーダー</strong>です。公開されている元ページを、書庫の閲覧、支部別検索、保存、読書記録、読みかけ復帰まで扱えるネイティブな読書ワークスペースにまとめます。",
        "hero_alt": "続きから読む、書庫ルート、検索フィルタを表示した日本語UIのSCP Docsホーム画面",
        "cta_main": "App Store で入手",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "機能を見る",
        "cta2_sub": "Field guide",
        "badges": ["非公式ファンアプリ", "無料 + プレミアム", "13+", "アカウント不要"],
        "stats": [
            ("5", "対応支部"),
            ("10+", "書庫ルート"),
            ("0", "必要なアカウント"),
            ("17+", "対応 iOS"),
        ],
        "screens_title": "ワークフローに対応した画面",
        "screens": [
            ("home", "支部選択、続きから読む、書庫ルート、クイックフィルタを表示したホーム画面", "ホーム: 支部、書庫ルート、続きから読む"),
            ("catalog", "シリーズと番号ブロックで記事を探せるSCPカタログ画面", "カタログ: 番号を知らなくても一覧から探す"),
            ("library", "読書状態、評価、ブックマーク、保存状態を表示したライブラリ画面", "ライブラリ: 履歴、評価、ブックマーク、保存状態"),
            ("search", "番号、キーワード、タグ、支部、種別、Object Class、高度な絞り込みを表示した検索画面", "検索: 番号、キーワード、タグ、高度な絞り込み"),
        ],
        "workspace_title": "読む、探す、整理する、戻ってくる",
        "workspace_p1": "アプリはホーム、書庫、検索、設定を中心に構成されています。現在のホームは「続きから読む」、検索プリセット、ランダム発見、Stories / Tales / Canons / Series / GoI / ガイド類などへ進む整理されたディレクトリを備えます。",
        "workspace_p2": "閲覧履歴、読了状態、評価、ブックマーク、後で読む、スクロール位置、メモ、フォルダ、続きから読むデータを記事に結びつけて保存し、読んできた経路を端末内で見失いにくくします。",
        "scope_title": "5支部をひとつの読書フローに",
        "scope_p": "英語本家 SCP Foundation アーカイブと、日本・フランス・ロシア・韓国支部に対応しています。支部を切り替えると、ホーム、検索、アプリ内リスト、記事リンク先、アプリUI言語が切り替わります。カタログデータがある範囲で SCP International や翻訳アーカイブの入口も整理します。",
        "scope_items": [
            ("書庫リスト", "SCP記事、Tales、Canons、Canonシリーズ、GoI、Joke SCP、SCP-EX、コレクション、新着記事、関連ディレクトリ。"),
            ("検索", "番号・タイトル検索は無料。プレミアムでは対象文書、タグ、オブジェクトクラス、メモ、読書状態、公式評価、長さ、保存検索まで組み合わせられます。"),
            ("書庫", "ブックマーク、後で読む、評価、メモ、フォルダ、スクロール位置を記事に結びつけて、あとから戻れる状態にします。"),
            ("リーダー", "文字組み、テーマ、スクロール操作、ダークモード、特殊レイアウト記事の再現性を見直した本文表示。"),
        ],
        "premium_title": "深く読むためのツール",
        "premium_cols": [
            [
                ("読書統計", "読書時間、カタログ読了率、よく読むオブジェクトクラスやタグ、評価傾向、メモ、積読、曜日・月・年ごとの記録を表示します。"),
                ("保存した検索", "検索条件を保存し、新しく一致する記事がカタログに現れたときに端末上の通知で知らせます。"),
                ("ブックマークフォルダ", "保存した記事をフォルダで整理し、メモや保存検索とともに自分の iCloud Drive 経由で同期できます。"),
            ],
            [
                ("聴く、保存する", "読み上げ機能で本文を音声再生し、対象記事のオフライン保存で通信がない場面でも読み返せます。"),
                ("カードで共有", "記事や選んだリストを、X などで共有しやすいカード画像にできます。テンプレートとコメントにも対応します。"),
                ("広告と上限", "プレミアムでは広告非表示、保存上限拡張、メモ編集、高度な検索を利用できます。利用可能な場合はリワード広告で一時的にプレミアムを解放できます。"),
            ],
        ],
        "req_title": "動作環境",
        "req_items": [
            ("OS", "iOS 17以降。"),
            ("通信", "カタログ更新、オンライン記事表示、元サイトコンテンツ、広告、購入確認、外部リンクに必要です。"),
            ("アカウント", "アプリで読むだけなら SCP Foundation や Wikidot のアカウントは不要です。"),
        ],
        "cta_title": "書庫を開く",
        "legal_p": "SCP Docs は<strong>非公式ファンアプリ</strong>です。記事本文、著者表示、著作権表示、ライセンス条件は各提供元サイトが正本です。SCP 関連作品は一般に Creative Commons BY-SA 3.0 のもとで公開されていますが、個別ページの表示が優先されます。",
        "store_name": "SCP Docs for iPhone",
        "store_note": "iOS 17以降に対応。アプリUIは現在、英語・日本語・フランス語・ロシア語・韓国語に対応しています。",
        "store_main": "App Store で見る",
    },
    "fr": {
        "title": "SCP Docs — Archive de la Fondation pour iPhone",
        "description": "SCP Docs est un lecteur iOS non officiel pour les archives SCP Wiki, la recherche par branche, l'état de lecture, les recherches enregistrées, le partage et les outils Premium.",
        "lede": "SCP Docs est un <strong>lecteur iOS non officiel et fan-made</strong> pour les articles du SCP Wiki et de ses branches. Il transforme les pages publiques en espace de lecture natif pour parcourir les archives, chercher par branche, sauvegarder ce qui compte et reprendre vos rapports en cours.",
        "hero_alt": "Écran d'accueil SCP Docs en français avec reprise de lecture, routes d'archive et filtres de recherche",
        "cta_main": "Voir sur l'App Store",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "Découvrir les fonctions",
        "cta2_sub": "Field guide",
        "badges": ["App fan non officielle", "Gratuit + Premium", "13+", "Sans compte"],
        "stats": [
            ("5", "branches d'archives"),
            ("10+", "routes d'archive"),
            ("0", "compte requis"),
            ("17+", "conçu pour iOS"),
        ],
        "screens_title": "Écrans alignés sur le flux",
        "screens": [
            ("home", "Accueil avec sélection de branche, reprise de lecture, routes d'archive et filtres rapides", "Accueil : branche, routes d'archive et reprise"),
            ("catalog", "Liste de catalogue SCP avec séries, blocs et lignes d'articles", "Catalogue : parcourir avant de connaître le numéro"),
            ("library", "Bibliothèque avec historique, état de lecture, notes, favoris et actions rapides", "Bibliothèque : historique, notes, favoris et état sauvegardé"),
            ("search", "Recherche avec numéro, mot-clé, tag, branche, type, classe d'objet et filtres avancés", "Recherche : numéro, mot-clé, tag et filtres avancés"),
        ],
        "workspace_title": "Lire, chercher, organiser, reprendre",
        "workspace_p1": "L'app s'organise autour d'Accueil, Bibliothèque, Recherche et Réglages. L'accueil met en avant la reprise de lecture, les préréglages de recherche, la découverte aléatoire et des itinéraires plus clairs vers Stories, Tales, Canons, Series, GoI, guides et collections associées.",
        "workspace_p2": "Historique, état lu/non lu, notes, favoris, éléments à lire plus tard, position de défilement, mémos, dossiers et reprise de lecture restent liés aux articles ouverts, pour garder votre parcours visible sur l'appareil.",
        "scope_title": "Cinq branches, un même flux de lecture",
        "scope_p": "SCP Docs prend en charge l'archive principale anglaise de la SCP Foundation ainsi que les branches japonaise, française, russe et coréenne. Changer de branche modifie l'accueil, la recherche, les listes intégrées, les destinations d'articles et la langue de l'interface. SCP International et les archives traduites sont listés lorsque les données de catalogue existent.",
        "scope_items": [
            ("Listes d'archives", "SCP, Tales, Canons, séries Canon, GoI, Joke SCP, SCP-EX, collections, articles récents et répertoires associés."),
            ("Recherche", "la recherche par numéro et titre est gratuite. Premium ajoute des filtres par documents, tags, classe d'objet, mémos, état de lecture, score officiel, longueur et recherches enregistrées."),
            ("Bibliothèque", "favoris, à lire plus tard, notes, mémos, dossiers et position de défilement restent liés aux articles pour y revenir plus facilement."),
            ("Lecteur", "typographie plus claire, thèmes, outils de défilement, meilleur mode sombre et rendu plus fidèle des pages à mise en forme spéciale."),
        ],
        "premium_title": "Des outils pour lire plus loin",
        "premium_cols": [
            [
                ("Statistiques de lecture", "Temps de lecture, progression du catalogue, classes d'objet et tags les plus lus, tendances de notes, mémos, pile à lire et journaux par jour, mois et année."),
                ("Recherches enregistrées", "Enregistrez des critères et recevez une notification sur l'appareil quand de nouvelles entrées correspondantes apparaissent."),
                ("Dossiers de favoris", "Organisez les articles sauvegardés dans des dossiers pouvant se synchroniser via votre iCloud Drive, avec mémos et recherches enregistrées."),
            ],
            [
                ("Écouter et sauvegarder", "La synthèse vocale lit les articles à voix haute, et les instantanés hors ligne gardent les articles éligibles accessibles sans connexion."),
                ("Partager en cartes", "Transformez un article ou une liste choisie en carte de partage pour X et d'autres apps sociales, avec modèles et commentaire facultatif."),
                ("Publicités et limites", "Premium masque les publicités, étend les limites de sauvegarde, déverrouille l'édition de mémos et la recherche avancée. Une publicité récompensée peut donner un accès Premium temporaire lorsqu'elle est disponible."),
            ],
        ],
        "req_title": "Configuration requise",
        "req_items": [
            ("OS", "iOS 17 ou version ultérieure."),
            ("Réseau", "requis pour actualiser les catalogues, lire en ligne, charger les sites sources, publicités, vérifications d'achat et liens externes."),
            ("Comptes", "aucun compte SCP Foundation ou Wikidot n'est requis pour lire dans l'app."),
        ],
        "cta_title": "Ouvrir l'archive",
        "legal_p": "SCP Docs est une <strong>application fan non officielle</strong>. Les articles sources, crédits d'auteurs, mentions de copyright et conditions de licence restent régis par les sites sources. Les œuvres SCP sont généralement publiées sous Creative Commons BY-SA 3.0, mais chaque page source fait autorité.",
        "store_name": "SCP Docs pour iPhone",
        "store_note": "Nécessite iOS 17 ou version ultérieure. L'interface de l'app prend actuellement en charge l'anglais, le japonais, le français, le russe et le coréen.",
        "store_main": "Voir sur l'App Store",
    },
    "ru": {
        "title": "SCP Docs — читалка архива Фонда для iPhone",
        "description": "SCP Docs — неофициальная нативная iOS-читалка архивов SCP Wiki: каталоги филиалов, поиск, Библиотека, сохранённые поиски, публикация карточек и Premium-инструменты.",
        "lede": "SCP Docs — <strong>неофициальная фанатская iOS-читалка</strong> статей SCP Wiki и филиалов. Она превращает публичные исходные страницы в нативное рабочее пространство архива: просматривайте каталоги филиалов, ищите по номеру или названию, сохраняйте важные файлы, организуйте их в Библиотеке и возвращайтесь к тем самым отчётам, которые читали.",
        "hero_alt": "Главный экран SCP Docs на русском с продолжением чтения, маршрутами архива и поисковыми фильтрами",
        "cta_main": "Открыть в App Store",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "Смотреть возможности",
        "cta2_sub": "Field guide",
        "badges": ["Неофициальное фан-приложение", "Бесплатно + Premium", "13+", "Без аккаунта"],
        "stats": [
            ("5", "филиалов архива"),
            ("10+", "маршрутов каталога"),
            ("0", "аккаунтов нужно"),
            ("17+", "для iOS"),
        ],
        "screens_title": "Экраны, соответствующие сценарию",
        "screens": [
            ("home", "Главная с выбором филиала, продолжением чтения, маршрутами архива и быстрыми фильтрами", "Главная: филиал, маршруты архива и продолжение чтения"),
            ("catalog", "Каталог SCP со списком статей, сериями и блоками номеров", "Каталог: просматривайте статьи до того, как знаете номер"),
            ("library", "Библиотека с историей, статусом чтения, оценками, закладками и быстрыми действиями", "Библиотека: история, оценки, закладки и сохранённое состояние"),
            ("search", "Поиск по номеру, ключевым словам, тегам, филиалу, типу, классу объекта и расширенным фильтрам", "Поиск: номер, ключевое слово, тег и расширенные фильтры"),
        ],
        "workspace_title": "Читайте, ищите, организуйте, возвращайтесь",
        "workspace_p1": "Приложение построено вокруг Главной, Библиотеки, Поиска и Настроек. Главная служит входом в архив: продолжение чтения, пресеты поиска, случайное открытие и маршруты каталога для отчётов SCP, Tales, Canons, серий Canon, Групп Интереса, руководств и связанных коллекций.",
        "workspace_p2": "Библиотека превращает просмотр в личную полку. История, статус чтения, оценки, закладки, «прочитать позже», позиция прокрутки, заметки, папки и данные продолжения чтения остаются привязанными к открытым статьям, поэтому ваш путь по архиву виден на устройстве.",
        "scope_title": "Пять филиалов — один рабочий процесс",
        "scope_p": "SCP Docs поддерживает основной английский архив SCP Foundation, а также японский, французский, русский и корейский филиалы. Смена филиала меняет Главную, поиск, списки, переходы к статьям и язык интерфейса. SCP International и переведённые архивы перечислены там, где есть данные каталога.",
        "scope_items": [
            ("Списки архива", "Начинайте с каталогов филиала: статьи SCP, Tales, Canons, серии Canon, GoI, Joke SCP, SCP-EX, коллекции, недавние статьи и связанные маршруты."),
            ("Поиск", "Переходите по номеру или названию бесплатно; Premium добавляет фильтры по документам, тегам, классу объекта, заметкам, статусу чтения, официальному рейтингу, длине и сохранённым поискам."),
            ("Библиотека", "Сохраняйте статьи как закладки или «прочитать позже», оценивайте, добавляйте заметки, группируйте избранное в папки и продолжайте с сохранённой позиции прокрутки."),
            ("Ридер", "Более чистая типографика, темы, инструменты прокрутки, улучшенная тёмная тема и более точное отображение специально свёрстанных страниц."),
        ],
        "premium_title": "Инструменты для глубокого чтения",
        "premium_cols": [
            [
                ("Статистика чтения", "Время чтения, покрытие каталога, часто читаемые классы объектов и теги, тренды оценок, заметки, очередь и журналы по дням, месяцам и годам."),
                ("Сохранённые поиски", "Сохраняйте условия поиска и получайте уведомления на устройстве, когда появляются новые совпадающие записи каталога."),
                ("Папки закладок", "Организуйте сохранённые статьи в папки, которые могут синхронизироваться через ваш iCloud Drive вместе с заметками и сохранёнными поисками."),
            ],
            [
                ("Слушать и сохранять", "Синтез речи читает текст статьи вслух, а офлайн-снимки сохраняют подходящие статьи доступными без соединения."),
                ("Карточки для публикации", "Превратите статью или выбранный список в стилизованную карточку для X и других социальных приложений, с шаблонами и необязательным комментарием."),
                ("Реклама и лимиты", "Premium скрывает рекламу, расширяет лимиты сохранения, открывает редактирование заметок и расширенный поиск. Рекламный просмотр может дать временный Premium, когда доступен."),
            ],
        ],
        "req_title": "Требования",
        "req_items": [
            ("OS", "iOS 17 или новее."),
            ("Сеть", "нужна для обновления каталогов, онлайн-чтения, контента исходных сайтов, рекламы, проверок покупок и внешних ссылок."),
            ("Аккаунты", "для чтения в приложении не нужен аккаунт SCP Foundation или Wikidot."),
        ],
        "cta_title": "Открыть архив",
        "legal_p": "SCP Docs — <strong>неофициальное фанатское приложение</strong>. Исходные статьи, сведения об авторах, уведомления об авторских правах и условия лицензий регулируются исходными сайтами. Работы SCP обычно публикуются под Creative Commons BY-SA 3.0, но каждая исходная страница является основным источником.",
        "store_name": "SCP Docs для iPhone",
        "store_note": "Требуется iOS 17 или новее. Интерфейс приложения поддерживает английский, японский, французский, русский и корейский языки.",
        "store_main": "Открыть в App Store",
    },
    "ko": {
        "title": "SCP Docs — iPhone용 재단 아카이브 리더",
        "description": "SCP Docs는 SCP Wiki 아카이브를 위한 비공식 네이티브 iOS 리더입니다. 지부 디렉터리, 아카이브 탐색, 라이브러리 정리, 저장 검색, 공유, 프리미엄 읽기 도구를 제공합니다.",
        "lede": "SCP Docs는 SCP Wiki와 지부 사이트의 글을 위한 <strong>비공식 팬 제작 iOS 리더</strong>입니다. 공개된 원본 페이지를 네이티브 아카이브 작업 공간으로 바꿔 줍니다: 지부 디렉터리 탐색, 번호·제목 검색, 중요한 문서 저장, 라이브러리 정리, 그리고 읽던 보고서로 정확히 복귀할 수 있습니다.",
        "hero_alt": "이어 읽기, 아카이브 경로, 검색 필터가 보이는 한국어 UI의 SCP Docs 홈 화면",
        "cta_main": "App Store에서 받기",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "기능 살펴보기",
        "cta2_sub": "Field guide",
        "badges": ["비공식 팬 앱", "무료 + 프리미엄", "13+", "계정 불필요"],
        "stats": [
            ("5", "지원 지부"),
            ("10+", "아카이브 경로"),
            ("0", "필요한 계정"),
            ("17+", "지원 iOS"),
        ],
        "screens_title": "흐름에 맞춘 화면",
        "screens": [
            ("home", "지부 선택, 이어 읽기, 아카이브 경로, 빠른 필터가 보이는 홈 화면", "홈: 지부, 아카이브 경로, 이어 읽기"),
            ("catalog", "시리즈와 번호 블록으로 글을 찾는 SCP 카탈로그 화면", "카탈로그: 번호를 몰라도 목록에서 탐색"),
            ("library", "읽기 상태, 평점, 북마크, 저장 상태를 보여 주는 라이브러리 화면", "라이브러리: 기록, 평점, 북마크, 저장 상태"),
            ("search", "번호, 키워드, 태그, 지부, 종류, Object Class, 고급 필터가 보이는 검색 화면", "검색: 번호, 키워드, 태그, 고급 필터"),
        ],
        "workspace_title": "읽고, 찾고, 정리하고, 다시 돌아오기",
        "workspace_p1": "앱은 홈, 라이브러리, 검색, 설정을 중심으로 구성됩니다. 홈은 아카이브 진입점 역할을 하며 이어 읽기, 빠른 검색 프리셋, 랜덤 발견, 그리고 SCP 보고서, Tales, Canons, Canon 시리즈, GoI, 가이드, 관련 컬렉션으로 이어지는 디렉터리 경로를 제공합니다.",
        "workspace_p2": "라이브러리는 탐색을 개인 서가로 바꿉니다. 기록, 읽음 상태, 평점, 북마크, 나중에 읽기, 스크롤 위치, 메모, 폴더, 이어 읽기 데이터가 열어 본 글에 연결되어 남아, 아카이브를 지나온 경로가 기기 안에서 보입니다.",
        "scope_title": "5개 지부, 하나의 아카이브 흐름",
        "scope_p": "SCP Docs는 영어 본가 SCP Foundation 아카이브와 일본어, 프랑스어, 러시아어, 한국어 지부를 지원합니다. 지부를 바꾸면 홈, 검색, 앱 내 목록, 글 링크 대상, 앱 UI 언어가 함께 바뀝니다. 카탈로그 데이터가 있는 범위에서 SCP International과 번역 아카이브 진입점도 정리됩니다.",
        "scope_items": [
            ("아카이브 목록", "SCP 글, Tales, Canons, Canon 시리즈, GoI, Joke SCP, SCP-EX, 컬렉션, 최근 글, 관련 경로의 지부별 디렉터리에서 시작합니다."),
            ("검색", "번호·제목 검색은 무료입니다. 프리미엄은 문서, 태그, Object Class, 메모, 읽기 상태, 공식 점수, 길이, 저장 검색까지 고급 필터를 추가합니다."),
            ("라이브러리", "글을 북마크나 나중에 읽기로 저장하고, 평가하고, 메모를 남기고, 즐겨찾기를 폴더로 묶고, 저장된 스크롤 위치에서 이어 읽습니다."),
            ("리더", "더 깔끔한 타이포그래피, 테마, 스크롤 도구, 개선된 다크 모드, 특수 형식 페이지의 더 충실한 렌더링."),
        ],
        "premium_title": "더 깊이 읽기 위한 도구",
        "premium_cols": [
            [
                ("읽기 통계", "읽기 시간, 카탈로그 커버리지, 자주 읽는 Object Class와 태그, 평점 추세, 메모 인사이트, 읽기 대기 상태, 일·월·년 기록을 보여 줍니다."),
                ("저장 검색", "검색 조건을 저장하고 새로 일치하는 카탈로그 항목이 나타나면 기기 알림으로 알려 줍니다."),
                ("북마크 폴더", "저장한 글을 폴더로 정리하고 메모, 저장 검색과 함께 사용자의 iCloud Drive를 통해 동기화할 수 있습니다."),
            ],
            [
                ("듣고 저장하기", "텍스트 음성 변환이 본문을 읽어 주고, 오프라인 스냅샷은 저장 가능한 글을 연결 없이도 볼 수 있게 유지합니다."),
                ("카드로 공유", "글 하나 또는 선택한 목록을 X 등 소셜 앱에 공유하기 좋은 스타일 카드로 만듭니다. 템플릿과 선택 코멘트를 지원합니다."),
                ("광고와 한도", "프리미엄은 광고 숨김, 저장 한도 확장, 메모 편집, 고급 검색을 제공합니다. 제공되는 경우 리워드 광고로 임시 프리미엄을 받을 수 있습니다."),
            ],
        ],
        "req_title": "요구 사항",
        "req_items": [
            ("OS", "iOS 17 이상."),
            ("네트워크", "카탈로그 새로고침, 온라인 글 보기, 원본 사이트 콘텐츠, 광고, 구매 확인, 외부 링크에 필요합니다."),
            ("계정", "앱에서 읽기만 할 경우 SCP Foundation이나 Wikidot 계정은 필요하지 않습니다."),
        ],
        "cta_title": "아카이브 열기",
        "legal_p": "SCP Docs는 <strong>비공식 팬 애플리케이션</strong>입니다. 원본 글, 저자 표시, 저작권 고지, 라이선스 조건은 각 원본 사이트가 기준입니다. SCP 관련 작품은 일반적으로 Creative Commons BY-SA 3.0으로 공개되지만, 개별 원본 페이지가 우선합니다.",
        "store_name": "iPhone용 SCP Docs",
        "store_note": "iOS 17 이상 지원. 앱 UI는 현재 영어, 일본어, 프랑스어, 러시아어, 한국어를 지원합니다.",
        "store_main": "App Store에서 보기",
    },
    "es": {
        "title": "SCP Docs — Lector del Archivo de la Fundación para iPhone",
        "description": "SCP Docs es un lector iOS nativo no oficial para los archivos de SCP Wiki, con directorios por rama, navegación guiada, Biblioteca, búsquedas guardadas, tarjetas para compartir y herramientas Premium.",
        "lede": "SCP Docs es un <strong>lector iOS no oficial hecho por fans</strong> para los artículos de SCP Wiki y sus ramas. Convierte las páginas públicas de origen en un espacio de lectura nativo: recorre los directorios de cada rama, busca por número o título, guarda los expedientes importantes, organízalos en tu Biblioteca y vuelve exactamente a los informes que estabas leyendo.",
        "hero_alt": "Pantalla de inicio de SCP Docs con continuar leyendo, rutas de archivo y filtros de búsqueda",
        "cta_main": "Descargar en el App Store",
        "cta_sub": "iPhone · iOS 17+",
        "cta2_main": "Explorar las funciones",
        "cta2_sub": "Field guide",
        "badges": ["App fan no oficial", "Gratis + Premium", "13+", "Sin cuenta"],
        "stats": [
            ("5", "ramas del archivo"),
            ("10+", "rutas de directorio"),
            ("0", "cuentas necesarias"),
            ("17+", "hecha para iOS"),
        ],
        "screens_title": "Pantallas alineadas con el flujo de lectura",
        "screens": [
            ("home", "Pantalla de inicio con selección de rama, continuar leyendo, rutas de archivo y filtros rápidos", "Inicio: rama, rutas de archivo y continuar leyendo"),
            ("catalog", "Catálogo SCP con filas de artículos, filtros por serie y por bloque", "Catálogo: explora artículos antes de saber el número"),
            ("library", "Biblioteca con historial, estado de lectura, valoraciones, marcadores y acciones rápidas", "Biblioteca: historial, valoraciones, marcadores y estado guardado"),
            ("search", "Búsqueda por número, palabra clave, etiqueta, rama, tipo, Clase de Objeto y filtros avanzados", "Búsqueda: número, palabra clave, etiqueta y filtros avanzados"),
        ],
        "workspace_title": "Explora el archivo y conserva tu lugar",
        "workspace_p1": "La app se organiza en Inicio, Biblioteca, Búsqueda y Ajustes. Inicio funciona como puerta de entrada al archivo: continuar leyendo, preajustes de búsqueda, descubrimiento aleatorio y rutas de directorio hacia informes SCP, Tales, Canons, series Canon, Grupos de Interés, guías y colecciones relacionadas.",
        "workspace_p2": "La Biblioteca convierte la navegación en una estantería personal. Historial, estado de lectura, valoraciones, marcadores, leer más tarde, posición de desplazamiento, notas, carpetas y datos de reanudación quedan ligados a los artículos que abres, de modo que tu recorrido por el archivo sigue visible en el dispositivo.",
        "scope_title": "Cinco ramas, un mismo flujo de archivo",
        "scope_p": "SCP Docs es compatible con el archivo principal en inglés de la SCP Foundation y con las ramas japonesa, francesa, rusa y coreana. Al cambiar de rama cambian el Inicio, la búsqueda, las listas integradas, los destinos de los artículos y el idioma de la interfaz. SCP International y los puntos de entrada de archivos traducidos se listan donde existen datos de catálogo.",
        "scope_items": [
            ("Listas de archivo", "Empieza por los directorios de cada rama: artículos SCP, Tales, Canons, series Canon, GoI, Joke SCP, SCP-EX, colecciones, artículos recientes y rutas relacionadas."),
            ("Búsqueda", "Salta directamente por número o título gratis; Premium añade filtros avanzados por documentos, etiquetas, Clase de Objeto, notas, estado de lectura, puntuación oficial, longitud y búsquedas guardadas."),
            ("Biblioteca", "Guarda artículos como marcadores o para leer más tarde, valóralos, añade notas, agrupa favoritos en carpetas y reanuda desde la posición de desplazamiento guardada."),
            ("Lector", "Tipografía más limpia, temas, herramientas de desplazamiento, mejor modo oscuro y un renderizado más fiel de las páginas con formato especial."),
        ],
        "premium_title": "Herramientas para leer más a fondo",
        "premium_cols": [
            [
                ("Estadísticas de lectura", "Tiempo de lectura, cobertura del catálogo, Clases de Objeto y etiquetas más leídas, tendencias de valoración, notas, pila de pendientes y registros por día, mes y año."),
                ("Búsquedas guardadas", "Guarda condiciones de búsqueda y recibe notificaciones en el dispositivo cuando aparecen nuevas entradas coincidentes en el catálogo."),
                ("Carpetas de marcadores", "Organiza los artículos guardados en carpetas que pueden sincronizarse a través de tu propio iCloud Drive, junto con notas y búsquedas guardadas."),
            ],
            [
                ("Escuchar y guardar", "La lectura en voz alta reproduce el texto del artículo, y las instantáneas sin conexión mantienen disponibles los artículos guardados aptos."),
                ("Compartir como tarjetas", "Convierte un artículo o una lista elegida en una tarjeta con estilo para X y otras apps sociales, con plantillas y comentario opcional."),
                ("Anuncios y límites", "Premium oculta los anuncios, amplía los límites de guardado, desbloquea la edición de notas y activa la búsqueda avanzada. Un anuncio con recompensa puede otorgar acceso Premium temporal cuando esté disponible."),
            ],
        ],
        "req_title": "Requisitos del sistema",
        "req_items": [
            ("OS", "iOS 17 o posterior."),
            ("Red", "necesaria para actualizar catálogos, leer en línea, cargar contenido de los sitios de origen, anuncios, verificaciones de compra y enlaces externos."),
            ("Cuentas", "no se necesita cuenta de SCP Foundation ni de Wikidot para leer en la app."),
        ],
        "cta_title": "Abrir el archivo",
        "legal_p": "SCP Docs es una <strong>aplicación fan no oficial</strong>. Los artículos de origen, los créditos de autor, los avisos de copyright y las condiciones de licencia siguen rigiéndose por los sitios de origen. Las obras SCP suelen publicarse bajo Creative Commons BY-SA 3.0, pero cada página de origen es la referencia autorizada.",
        "store_name": "SCP Docs para iPhone",
        "store_note": "Requiere iOS 17 o posterior. La interfaz de la app está disponible actualmente en inglés, japonés, francés, ruso y coreano.",
        "store_main": "Ver en el App Store",
    },
}


def build_index(lang: str) -> dict[str, str]:
    s = INDEX_STRINGS[lang]
    l = LANGS[lang]
    badges = "\n".join(f"              <li>{b}</li>" for b in s["badges"])
    stats = "\n".join(
        f"""          <div class="hero-stat"><span class="num">{num}</span><span class="lbl">{lbl}</span></div>"""
        for num, lbl in s["stats"]
    )
    screens = "\n".join(
        f"""          <figure class="screen-frame">
            <img src="{screenshot_path(lang, kind)}" alt="{alt}" loading="lazy" />
            <figcaption>{cap}</figcaption>
          </figure>"""
        for kind, alt, cap in s["screens"]
    )
    scope_items = "\n".join(
        f"            <li><strong>{k}</strong> — {v}</li>" for k, v in s["scope_items"]
    )
    premium_cols = "\n".join(
        f"""          <div class="card">
            <dl class="dl-flat">
{chr(10).join(f'              <dt>{dt}</dt>{chr(10)}              <dd>{dd}</dd>' for dt, dd in col)}
            </dl>
          </div>"""
        for col in s["premium_cols"]
    )
    req_items = "\n".join(
        f"            <li><strong>{k}</strong> — {v}</li>" for k, v in s["req_items"]
    )
    pills = "\n".join(
        f'            <a class="pill" href="{page_file(p, lang)}">{l.nav[p]}</a>'
        for p in ["features", "privacy", "support", "terms", "rating-safety"]
    )
    body = f"""
    <main class="main-pad">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-grid">
          <div class="hero-copy">
            <p class="hero-kicker"><span class="blink">▮</span> ITEM #: SCP-DOCS-APP · OBJECT CLASS: <span class="accent">READER</span></p>
            <h2 id="hero-title" class="hero-title">Secure.<br />Contain.<br /><span class="accent">Read.</span></h2>
            <p class="hero-lede">{s['lede']}</p>
            <div class="hero-cta">
              <a class="btn-primary" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">
                <span class="btn-main">{s['cta_main']}</span>
                <span class="btn-sub">{s['cta_sub']}</span>
              </a>
              <a class="btn-ghost" href="{page_file('features', lang)}">
                <span class="btn-main">{s['cta2_main']}</span>
                <span class="btn-sub">{s['cta2_sub']}</span>
              </a>
            </div>
            <ul class="hero-badges">
{badges}
            </ul>
          </div>
          <figure class="hero-shot" aria-label="SCP Docs app preview">
            <img src="{screenshot_path(lang, 'home')}" alt="{s['hero_alt']}" />
          </figure>
        </div>
        <div class="hero-stats">
{stats}
        </div>
      </section>

      <section aria-labelledby="screens-title" style="margin-top:64px;">
        <p class="section-label">Field screens</p>
        <h2 id="screens-title" class="section-title-lg">{s['screens_title']}</h2>
        <div class="feature-shot-grid">
{screens}
        </div>
      </section>

      <section aria-labelledby="workspace-title" style="margin-top:56px;">
        <p class="section-label">Reading workspace</p>
        <h2 id="workspace-title" class="section-title-lg">{s['workspace_title']}</h2>
        <div class="grid-2">
          <div class="card">
            <p style="margin:0;">{s['workspace_p1']}</p>
          </div>
          <div class="card">
            <p style="margin:0;">{s['workspace_p2']}</p>
          </div>
        </div>
      </section>

      <section aria-labelledby="branch-title" style="margin-top:56px;">
        <p class="section-label">Content scope</p>
        <h2 id="branch-title" class="section-title-lg">{s['scope_title']}</h2>
        <div class="card">
          <p style="margin-top:0;">{s['scope_p']}</p>
          <ul class="ft-list">
{scope_items}
          </ul>
        </div>
      </section>

      <section aria-labelledby="premium-title" style="margin-top:56px;">
        <p class="section-label">Premium</p>
        <h2 id="premium-title" class="section-title-lg">{s['premium_title']}</h2>
        <div class="grid-2">
{premium_cols}
        </div>
      </section>

      <section aria-labelledby="req-title" style="margin-top:56px;">
        <p class="section-label">Requirements</p>
        <h2 id="req-title" class="section-title-lg">{s['req_title']}</h2>
        <div class="card-flat">
          <ul class="ft-list">
{req_items}
          </ul>
        </div>
      </section>

      <section aria-labelledby="cta-title" style="margin-top:56px;">
        <p class="section-label">Deployment</p>
        <h2 id="cta-title" class="section-title-lg">{s['cta_title']}</h2>
        <div class="card-invert">
          <p class="lede" style="margin-top:0;">{s['legal_p']}</p>
          <div class="pill-row">
{pills}
          </div>
          <div class="store-cta" aria-label="SCP Docs App Store link">
            <div class="store-cta-copy">
              <span class="store-cta-kicker">Available on the App Store</span>
              <strong>{s['store_name']}</strong>
              <span>{s['store_note']}</span>
            </div>
            <a class="store-cta-link" href="{APP_STORE_URL}" target="_blank"
              rel="noopener noreferrer" aria-label="SCP Docs — App Store">
              <span class="store-cta-link-main">{s['store_main']}</span>
              <span class="store-cta-link-sub">View on Apple</span>
            </a>
          </div>
        </div>
      </section>
    </main>"""
    return {"title": s["title"], "description": s["description"], "body": body}


INDEX: dict[str, dict[str, str]] = {code: build_index(code) for code in LANGS}


FEATURES: dict[str, dict[str, str]] = {}


# Free vs Premium comparison table. Cell values: "yes", "no", or (css_class, text).
FEATURE_CMP: dict[str, dict[str, object]] = {
    "en": {
        "title": "Free vs Premium",
        "col_feature": "Capability",
        "col_free": "Free",
        "col_premium": "Premium",
        "note": "Premium is provided as an auto-renewing subscription through the App Store. When available, a rewarded ad can grant temporary Premium access without a subscription.",
        "rows": [
            ("Number & title search", "yes", "yes"),
            ("Archive directories & catalog browsing", "yes", "yes"),
            ("History, bookmarks, read-later, ratings", "yes", "yes"),
            ("Reader themes, typography & dark mode", "yes", "yes"),
            ("Ads", ("part", "shown"), ("yes", "hidden")),
            ("Save limits", ("part", "standard"), ("yes", "expanded")),
            ("Advanced search filters", "no", "yes"),
            ("Memo editing", "no", "yes"),
            ("Offline snapshots", "no", "yes"),
            ("Reading stats", "no", "yes"),
            ("Text-to-speech", "no", "yes"),
            ("Saved searches & new-match alerts", "no", "yes"),
            ("Bookmark folders & iCloud sync", "no", "yes"),
        ],
    },
    "ja": {
        "title": "無料とプレミアムの違い",
        "col_feature": "機能",
        "col_free": "無料",
        "col_premium": "プレミアム",
        "note": "プレミアムは App Store の自動更新購読として提供されます。利用可能な場合は、リワード広告で購読なしに一時的なプレミアムアクセスを利用できます。",
        "rows": [
            ("番号・タイトル検索", "yes", "yes"),
            ("書庫ディレクトリとカタログ閲覧", "yes", "yes"),
            ("履歴・ブックマーク・後で読む・評価", "yes", "yes"),
            ("リーダーのテーマ・文字組み・ダークモード", "yes", "yes"),
            ("広告", ("part", "表示"), ("yes", "非表示")),
            ("保存上限", ("part", "標準"), ("yes", "拡張")),
            ("高度な検索フィルタ", "no", "yes"),
            ("メモ編集", "no", "yes"),
            ("オフライン保存", "no", "yes"),
            ("読書統計", "no", "yes"),
            ("読み上げ（TTS）", "no", "yes"),
            ("保存検索と新着通知", "no", "yes"),
            ("ブックマークフォルダと iCloud 同期", "no", "yes"),
        ],
    },
    "fr": {
        "title": "Gratuit vs Premium",
        "col_feature": "Fonction",
        "col_free": "Gratuit",
        "col_premium": "Premium",
        "note": "Premium est un abonnement à renouvellement automatique géré via l'App Store. Lorsqu'elle est disponible, une publicité récompensée peut donner un accès Premium temporaire sans abonnement.",
        "rows": [
            ("Recherche par numéro et titre", "yes", "yes"),
            ("Répertoires d'archive et catalogue", "yes", "yes"),
            ("Historique, favoris, à lire plus tard, notes", "yes", "yes"),
            ("Thèmes, typographie et mode sombre", "yes", "yes"),
            ("Publicités", ("part", "affichées"), ("yes", "masquées")),
            ("Limites de sauvegarde", ("part", "standard"), ("yes", "étendues")),
            ("Filtres de recherche avancés", "no", "yes"),
            ("Édition des mémos", "no", "yes"),
            ("Instantanés hors ligne", "no", "yes"),
            ("Statistiques de lecture", "no", "yes"),
            ("Synthèse vocale", "no", "yes"),
            ("Recherches enregistrées et alertes", "no", "yes"),
            ("Dossiers de favoris et synchronisation iCloud", "no", "yes"),
        ],
    },
    "ru": {
        "title": "Бесплатно и Premium",
        "col_feature": "Возможность",
        "col_free": "Бесплатно",
        "col_premium": "Premium",
        "note": "Premium предоставляется как автопродлеваемая подписка через App Store. Когда доступно, рекламный просмотр может дать временный Premium-доступ без подписки.",
        "rows": [
            ("Поиск по номеру и названию", "yes", "yes"),
            ("Каталоги и списки архива", "yes", "yes"),
            ("История, закладки, «прочитать позже», оценки", "yes", "yes"),
            ("Темы, типографика и тёмный режим", "yes", "yes"),
            ("Реклама", ("part", "показывается"), ("yes", "скрыта")),
            ("Лимиты сохранения", ("part", "стандартные"), ("yes", "расширенные")),
            ("Расширенные фильтры поиска", "no", "yes"),
            ("Редактирование заметок", "no", "yes"),
            ("Офлайн-снимки", "no", "yes"),
            ("Статистика чтения", "no", "yes"),
            ("Озвучивание текста", "no", "yes"),
            ("Сохранённые поиски и уведомления", "no", "yes"),
            ("Папки закладок и синхронизация iCloud", "no", "yes"),
        ],
    },
    "ko": {
        "title": "무료와 프리미엄 비교",
        "col_feature": "기능",
        "col_free": "무료",
        "col_premium": "프리미엄",
        "note": "프리미엄은 App Store의 자동 갱신 구독으로 제공됩니다. 제공되는 경우 리워드 광고로 구독 없이 임시 프리미엄을 이용할 수 있습니다.",
        "rows": [
            ("번호·제목 검색", "yes", "yes"),
            ("아카이브 디렉터리와 카탈로그 탐색", "yes", "yes"),
            ("기록·북마크·나중에 읽기·평점", "yes", "yes"),
            ("리더 테마·타이포그래피·다크 모드", "yes", "yes"),
            ("광고", ("part", "표시"), ("yes", "제거")),
            ("저장 한도", ("part", "기본"), ("yes", "확장")),
            ("고급 검색 필터", "no", "yes"),
            ("메모 편집", "no", "yes"),
            ("오프라인 스냅샷", "no", "yes"),
            ("읽기 통계", "no", "yes"),
            ("텍스트 음성 변환", "no", "yes"),
            ("저장 검색과 새 항목 알림", "no", "yes"),
            ("북마크 폴더와 iCloud 동기화", "no", "yes"),
        ],
    },
    "es": {
        "title": "Gratis frente a Premium",
        "col_feature": "Función",
        "col_free": "Gratis",
        "col_premium": "Premium",
        "note": "Premium se ofrece como suscripción con renovación automática a través del App Store. Cuando está disponible, un anuncio con recompensa puede otorgar acceso Premium temporal sin suscripción.",
        "rows": [
            ("Búsqueda por número y título", "yes", "yes"),
            ("Directorios de archivo y catálogo", "yes", "yes"),
            ("Historial, marcadores, leer más tarde, valoraciones", "yes", "yes"),
            ("Temas, tipografía y modo oscuro", "yes", "yes"),
            ("Anuncios", ("part", "se muestran"), ("yes", "eliminados")),
            ("Límites de guardado", ("part", "estándar"), ("yes", "ampliados")),
            ("Filtros de búsqueda avanzados", "no", "yes"),
            ("Edición de notas", "no", "yes"),
            ("Instantáneas sin conexión", "no", "yes"),
            ("Estadísticas de lectura", "no", "yes"),
            ("Lectura en voz alta", "no", "yes"),
            ("Búsquedas guardadas y avisos", "no", "yes"),
            ("Carpetas de marcadores y sincronización iCloud", "no", "yes"),
        ],
    },
}


def cmp_cell(value: object) -> str:
    if value == "yes":
        return '<td><span class="yes">✓</span></td>'
    if value == "no":
        return '<td><span class="no">—</span></td>'
    cls, text = value  # type: ignore[misc]
    return f'<td><span class="{cls}">{text}</span></td>'


def cmp_section(lang: str) -> str:
    cmp = FEATURE_CMP[lang]
    rows = "\n".join(
        f"              <tr><td>{label}</td>{cmp_cell(free)}{cmp_cell(premium)}</tr>"
        for label, free, premium in cmp["rows"]
    )
    return f"""      <section aria-labelledby="cmp-title" style="margin-top:38px;">
        <p class="section-label">Access tiers</p>
        <h2 id="cmp-title" class="section-title-lg">{cmp['title']}</h2>
        <div class="table-scroll">
          <table class="cmp-table">
            <thead>
              <tr><th>{cmp['col_feature']}</th><th>{cmp['col_free']}</th><th>{cmp['col_premium']}</th></tr>
            </thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="ft-muted" style="margin-top:12px;">{cmp['note']}</p>
      </section>"""


def translated_feature(lang: str) -> dict[str, str]:
    bodies = {
        "en": (
            "Features — SCP Docs",
            "A screenshot-led tour of SCP Docs: archive directories, branch-aware Home, refreshed search, Library organization, reader tools, sharing, saved searches, reading stats, and sync.",
            "Find a report, then actually get back to it",
            "SCP Docs brings archive entry points, search, reader controls, and personal reading state into one native iOS app. It is designed for the full archive loop: find the next file, save what matters, organize it in Library, and resume without rebuilding your trail.",
            [
                ("Branches", "English, Japanese, French, Russian, and Korean archives", "Switching branches changes Home, search, lists, article destinations, and app language so each archive has its own reading context."),
                ("Directories", "Cleaner archive routes before you know the number", "Move through SCP reports, Tales, Canons, Canon series, GoI, Joke SCPs, SCP-EX, collections, recent articles, guides, and related lists from organized entry points."),
                ("Search", "Fast free search, deeper Premium filters", "Open by SCP number, search titles, and use shortcuts for tags and Object Classes. Premium adds documents, memos, reading status, official score, length, and saved searches."),
                ("Reader", "A focused article view", "Typography controls, calmer themes, improved dark mode, scroll-to-top, offline snapshots, and closer rendering for specially formatted source pages."),
                ("Library", "A personal shelf for the archive", "History, read status, ratings, bookmarks, read-later, scroll position, memos, folders, and resume-reading data stay organized on your device."),
                ("Share", "Share as cards", "Turn an article or hand-picked list into a styled card for X and other social apps, with templates and optional comments."),
                ("Premium", "Stats, speech, and offline reading", "Reading stats, text-to-speech, memo editing, expanded save limits, ad removal, and offline storage support longer reading sessions."),
                ("Sync", "iCloud-backed personal organization", "When available, reading state, memos, saved searches, and bookmark folders sync through your own iCloud Drive. Saved searches can notify you about new matches on device."),
            ],
            "SCP Docs is not an official SCP Foundation or Wikidot app. Source pages, author credits, and license notices on each source site remain authoritative.",
            "Home (light)",
            "Home (dark)",
        ),
        "ja": (
            "機能紹介 — SCP Docs",
            "SCP Docs のホーム、検索、書庫、リーダー、共有カード、保存検索、読書統計、同期機能をスクリーンショット付きで紹介します。",
            "読みたい報告書を見つけ、あとからきちんと戻る",
            "SCP Docs は、書庫の入口、検索、リーダー操作、個人の読書状態をひとつのネイティブ iOS アプリにまとめます。最近のアップデートで、読むだけでなく、見つける、保存する、聴く、共有する、記録するところまで扱える読書ワークスペースになりました。",
            [
                ("Branches", "英語・日本語・フランス語・ロシア語・韓国語の書庫", "支部を切り替えると、ホーム、検索、一覧、記事リンク先、アプリ言語が切り替わり、それぞれの書庫をその文脈で読めます。"),
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
                ("Branches", "Archives anglaise, japonaise, française, russe et coréenne", "Changer de branche modifie l'accueil, la recherche, les listes, les destinations d'articles et la langue de l'app."),
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
                ("Branches", "Английский, японский, французский, русский и корейский архивы", "Смена филиала меняет Главную, поиск, списки, переходы к статьям и язык приложения."),
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
                ("Branches", "영어, 일본어, 프랑스어, 러시아어, 한국어 아카이브", "지부를 바꾸면 홈, 검색, 목록, 글 링크 대상, 앱 언어가 함께 바뀌어 각 아카이브의 문맥으로 읽을 수 있습니다."),
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
        "es": (
            "Funciones — SCP Docs",
            "Un recorrido con capturas por SCP Docs: directorios de archivo, Inicio por rama, búsqueda renovada, Biblioteca, herramientas de lectura, tarjetas para compartir, búsquedas guardadas, estadísticas y sincronización.",
            "Encuentra un informe y vuelve a él de verdad",
            "SCP Docs reúne las entradas al archivo, la búsqueda, los controles de lectura y el estado personal de lectura en una sola app iOS nativa. Está diseñada para el ciclo completo: encontrar el siguiente expediente, guardar lo que importa, organizarlo en la Biblioteca y reanudar sin reconstruir tu rastro.",
            [
                ("Branches", "Archivos en inglés, japonés, francés, ruso y coreano", "Cambiar de rama modifica el Inicio, la búsqueda, las listas, los destinos de los artículos y el idioma de la app, para leer cada archivo en su propio contexto."),
                ("Directories", "Rutas de archivo más claras antes de saber el número", "Recorre informes SCP, Tales, Canons, series Canon, GoI, Joke SCP, SCP-EX, colecciones, artículos recientes, guías y listas relacionadas desde entradas organizadas."),
                ("Search", "Búsqueda gratuita rápida y filtros Premium más profundos", "Abre por número SCP, busca por título y usa atajos de etiquetas y Clases de Objeto. Premium añade documentos, notas, estado de lectura, puntuación oficial, longitud y búsquedas guardadas."),
                ("Reader", "Una vista de artículo para concentrarse", "Controles tipográficos, temas tranquilos, modo oscuro mejorado, volver arriba, instantáneas sin conexión y un renderizado más fiel de las páginas con formato especial."),
                ("Library", "Una estantería personal para el archivo", "Historial, estado de lectura, valoraciones, marcadores, leer más tarde, posición de desplazamiento, notas, carpetas y datos de reanudación quedan organizados en tu dispositivo."),
                ("Share", "Compartir como tarjetas", "Convierte un artículo o una lista elegida en una tarjeta con estilo para X y otras apps sociales, con plantillas y comentario opcional."),
                ("Premium", "Estadísticas, voz y lectura sin conexión", "Estadísticas de lectura, lectura en voz alta, edición de notas, límites ampliados, sin anuncios y almacenamiento sin conexión para sesiones de lectura largas."),
                ("Sync", "Organización personal respaldada por iCloud", "Cuando está disponible, el estado de lectura, las notas, las búsquedas guardadas y las carpetas de marcadores se sincronizan a través de tu propio iCloud Drive. Las búsquedas guardadas pueden avisarte de nuevas coincidencias en el dispositivo."),
            ],
            "SCP Docs no es una app oficial de la SCP Foundation ni de Wikidot. Las páginas de origen, los créditos de autor y los avisos de licencia de cada sitio de origen son la referencia autorizada.",
            "Inicio (claro)",
            "Inicio (oscuro)",
        ),
    }
    title, description, h2, lede, cards, legal, _light_caption, _dark_caption = bodies[lang]
    feature_copy = {
        "en": {
            "overview_label": "Feature overview",
            "screens_label": "Screenshots",
            "screens_title": "Screens that match the workflow",
            "workflow_label": "Archive & Library workflow",
            "workflow_title": "From archive lists to a personal reading shelf",
            "guide_label": "Practical guide",
            "guide_title": "What to use when",
            "points_label": "What it does",
            "points_title": "Core features",
            "hero_alt": "English SCP Docs home screen showing continue reading, archive routes, and search filters",
            "pills": ["Home", "Archive routes", "Library", "Search", "Stats", "Share cards"],
            "screens": [
                ("home", "Home screen with branch selection, continue reading, archive routes, and quick filters", "Home: branch, archive routes, and continue reading"),
                ("catalog", "SCP catalog list with article rows, series filters, and block filters", "Catalog: browse articles before you know the number"),
                ("library", "Library history screen with read status, ratings, bookmarks, quick actions, and sort controls", "Library: history, ratings, bookmarks, and saved state"),
                ("search", "Search screen with number, keyword, tag, site, type, Object Class, and advanced filters", "Search: number, keyword, tag, and advanced filters"),
            ],
            "workflow_cards": [
                (
                    "Use Home as the archive map",
                    [
                        ("Pick a branch", "Choose English, Japanese, French, Russian, or Korean. Home, search, lists, article links, and the app language follow that branch context."),
                        ("Start from directories", "Browse SCP reports, Tales, Canons, Canon series, GoI, Joke SCPs, SCP-EX, collections, recent articles, guides, and related lists without needing the exact article number first."),
                        ("Jump when you know the target", "Use free number and title search for quick access. Premium advanced search adds tags, Object Class, document text, memos, read status, official score, length, and saved conditions."),
                    ],
                ),
                (
                    "Turn browsing into Library state",
                    [
                        ("Save the article", "Bookmark it, mark it read-later, rate it, or keep a memo so the report is no longer just another page in the archive."),
                        ("Resume from context", "History, continue-reading, read status, ratings, memos, and scroll position help you return to the same file or series after a break."),
                        ("Organize for longer projects", "Premium expands save limits, adds bookmark folders, supports memo editing, can sync Library state through your own iCloud Drive, and can store eligible articles for offline reading."),
                    ],
                ),
            ],
            "guide_items": [
                ("I want to browse without a specific article in mind", "Start on Home, choose the branch, then open Archive routes such as SCP, SCP-INT, Stories, or Others. The catalog screen lets you move by series and block, with article rows showing titles, Object Class, tags, scores, and thumbnail previews where available."),
                ("I know the number, title, tag, or Object Class", "Use Search. Number and title lookup are available for normal use, while Premium advanced filters help narrow by document group, branch, tags, official score, length, Object Class, reading state, and memos."),
                ("I found something I want to keep", "Save it from the reader or Library as a bookmark, read-later item, rating, memo, or folder entry. Those signals make the article visible later from Library instead of relying on memory or browser history."),
                ("I stopped halfway through a series", "Use Continue reading, Library history, stored scroll position, and read status to return to the same report or track what has already been handled."),
            ],
        },
        "ja": {
            "overview_label": "機能概要",
            "screens_label": "スクリーンショット",
            "screens_title": "ワークフローに対応した画面",
            "workflow_label": "書庫とライブラリの流れ",
            "workflow_title": "書庫リストから自分の読書棚へ",
            "guide_label": "使い分けガイド",
            "guide_title": "目的別に使う場所",
            "points_label": "できること",
            "points_title": "主な機能",
            "hero_alt": "続きから読む、書庫ルート、検索フィルタを表示した日本語UIのホーム画面",
            "pills": ["ホーム", "書庫ルート", "ライブラリ", "検索", "統計", "共有カード"],
            "screens": [
                ("home", "支部選択、続きから読む、書庫ルート、クイックフィルタを表示したホーム画面", "ホーム: 支部、書庫ルート、続きから読む"),
                ("catalog", "シリーズと番号ブロックで記事を探せるSCPカタログ画面", "カタログ: 番号を知らなくても一覧から探す"),
                ("library", "読書状態、評価、ブックマーク、保存状態を表示したライブラリ画面", "ライブラリ: 履歴、評価、ブックマーク、保存状態"),
                ("search", "番号、キーワード、タグ、支部、種別、Object Class、高度な絞り込みを表示した検索画面", "検索: 番号、キーワード、タグ、高度な絞り込み"),
            ],
            "workflow_cards": [
                (
                    "ホームを書庫の地図として使う",
                    [
                        ("支部を選ぶ", "英語、日本語、フランス語、ロシア語、韓国語を選択できます。ホーム、検索、一覧、記事リンク、アプリ言語がその支部の文脈に揃います。"),
                        ("ディレクトリから始める", "SCP記事、Tales、Canons、Canonシリーズ、GoI、Joke SCP、SCP-EX、コレクション、新着記事、ガイド類を、番号を知らない状態から探せます。"),
                        ("分かっている時は検索へ", "番号やタイトル検索は無料で使えます。プレミアムの高度な検索ではタグ、Object Class、本文、メモ、読書状態、公式評価、長さ、保存条件まで絞り込めます。"),
                    ],
                ),
                (
                    "閲覧をライブラリ状態に変える",
                    [
                        ("記事を保存する", "ブックマーク、後で読む、評価、メモを使うと、記事がただのページではなく自分の読書棚に残ります。"),
                        ("文脈ごと再開する", "履歴、続きから読む、読了状態、評価、メモ、スクロール位置から、同じ報告書やシリーズに戻れます。"),
                        ("長い読書を整理する", "プレミアムでは保存上限拡張、ブックマークフォルダ、メモ編集、iCloud Drive同期、対象記事のオフライン保存を利用できます。"),
                    ],
                ),
            ],
            "guide_items": [
                ("特定の記事を決めずに探したい", "ホームで支部を選び、SCP、SCP-INT、Stories、Others などの書庫ルートを開きます。カタログ画面ではシリーズや番号ブロックで移動でき、タイトル、Object Class、タグ、スコア、サムネイルを見ながら探せます。"),
                ("番号、タイトル、タグ、Object Class が分かっている", "検索を使います。番号・タイトル検索は通常利用でき、プレミアムの高度な検索では文書種別、支部、タグ、公式評価、長さ、Object Class、読書状態、メモまで絞り込めます。"),
                ("あとで読み返したい記事を見つけた", "リーダーやライブラリからブックマーク、後で読む、評価、メモ、フォルダに保存します。後から記憶やブラウザ履歴に頼らずライブラリで見つけられます。"),
                ("シリーズを途中で止めた", "続きから読む、ライブラリ履歴、保存済みスクロール位置、読了状態を使うと、同じ報告書や進捗に戻れます。"),
            ],
        },
        "fr": {
            "overview_label": "Aperçu",
            "screens_label": "Captures",
            "screens_title": "Écrans alignés sur le flux",
            "workflow_label": "Flux archive et bibliothèque",
            "workflow_title": "Des listes d'archives à votre étagère de lecture",
            "guide_label": "Guide pratique",
            "guide_title": "Quel écran utiliser",
            "points_label": "Ce que fait l'app",
            "points_title": "Fonctions principales",
            "hero_alt": "Écran d'accueil SCP Docs en français avec reprise de lecture, routes d'archive et filtres de recherche",
            "pills": ["Accueil", "Routes d'archive", "Bibliothèque", "Recherche", "Stats", "Cartes"],
            "screens": [
                ("home", "Accueil avec sélection de branche, reprise de lecture, routes d'archive et filtres rapides", "Accueil : branche, routes d'archive et reprise"),
                ("catalog", "Liste de catalogue SCP avec séries, blocs et lignes d'articles", "Catalogue : parcourir avant de connaître le numéro"),
                ("library", "Bibliothèque avec historique, état de lecture, notes, favoris et actions rapides", "Bibliothèque : historique, notes, favoris et état sauvegardé"),
                ("search", "Recherche avec numéro, mot-clé, tag, branche, type, classe d'objet et filtres avancés", "Recherche : numéro, mot-clé, tag et filtres avancés"),
            ],
            "workflow_cards": [
                (
                    "Utiliser l'accueil comme carte d'archive",
                    [
                        ("Choisir une branche", "Sélectionnez l'anglais, le japonais, le français, le russe ou le coréen. L'accueil, la recherche, les listes, les liens d'articles et la langue de l'app suivent ce contexte."),
                        ("Commencer par les répertoires", "Parcourez SCP, Tales, Canons, séries Canon, GoI, Joke SCP, SCP-EX, collections, articles récents et guides sans connaître le numéro exact."),
                        ("Aller vite quand vous savez quoi chercher", "La recherche par numéro et titre est gratuite. La recherche avancée Premium ajoute tags, classe d'objet, texte, mémos, état de lecture, score officiel, longueur et critères enregistrés."),
                    ],
                ),
                (
                    "Transformer la lecture en état de bibliothèque",
                    [
                        ("Sauvegarder l'article", "Ajoutez un favori, marquez à lire plus tard, notez ou gardez un mémo pour que le rapport ne soit plus une simple page dans l'archive."),
                        ("Reprendre avec le contexte", "Historique, reprise de lecture, état lu/non lu, notes, mémos et position de défilement aident à revenir au même fichier ou à la même série."),
                        ("Organiser les longues lectures", "Premium étend les limites, ajoute des dossiers de favoris, l'édition des mémos, la synchronisation iCloud Drive et les instantanés hors ligne éligibles."),
                    ],
                ),
            ],
            "guide_items": [
                ("Je veux explorer sans article précis", "Commencez sur Accueil, choisissez la branche, puis ouvrez des routes comme SCP, SCP-INT, Stories ou Others. Le catalogue permet de naviguer par série et bloc, avec titres, classe d'objet, tags, scores et vignettes si disponibles."),
                ("Je connais le numéro, le titre, le tag ou la classe", "Utilisez Recherche. Numéro et titre sont disponibles normalement ; les filtres Premium affinent par groupe, branche, tags, score officiel, longueur, classe d'objet, état de lecture et mémos."),
                ("J'ai trouvé quelque chose à garder", "Depuis le lecteur ou la Bibliothèque, ajoutez favori, à lire plus tard, note, mémo ou dossier. Ces signaux rendent l'article visible ensuite sans dépendre de la mémoire ou de l'historique du navigateur."),
                ("J'ai interrompu une série", "Utilisez Reprise de lecture, historique de Bibliothèque, position de défilement sauvegardée et état de lecture pour revenir au même rapport ou suivre ce qui est déjà traité."),
            ],
        },
        "ru": {
            "overview_label": "Обзор",
            "screens_label": "Скриншоты",
            "screens_title": "Экраны, соответствующие сценарию",
            "workflow_label": "Архив и библиотека",
            "workflow_title": "От списков архива к личной полке чтения",
            "guide_label": "Практический гид",
            "guide_title": "Что использовать когда",
            "points_label": "Возможности",
            "points_title": "Основные возможности",
            "hero_alt": "Главный экран SCP Docs на русском с продолжением чтения, маршрутами архива и поисковыми фильтрами",
            "pills": ["Главная", "Маршруты архива", "Библиотека", "Поиск", "Статистика", "Карточки"],
            "screens": [
                ("home", "Главная с выбором филиала, продолжением чтения, маршрутами архива и быстрыми фильтрами", "Главная: филиал, маршруты архива и продолжение чтения"),
                ("catalog", "Каталог SCP со списком статей, сериями и блоками номеров", "Каталог: просматривайте статьи до того, как знаете номер"),
                ("library", "Библиотека с историей, статусом чтения, оценками, закладками и быстрыми действиями", "Библиотека: история, оценки, закладки и сохранённое состояние"),
                ("search", "Поиск по номеру, ключевым словам, тегам, филиалу, типу, классу объекта и расширенным фильтрам", "Поиск: номер, ключевое слово, тег и расширенные фильтры"),
            ],
            "workflow_cards": [
                (
                    "Используйте Главную как карту архива",
                    [
                        ("Выберите филиал", "Доступны английский, японский, французский, русский и корейский. Главная, поиск, списки, ссылки на статьи и язык приложения следуют выбранному контексту."),
                        ("Начинайте с каталогов", "Открывайте SCP, Tales, Canons, серии Canon, GoI, Joke SCP, SCP-EX, коллекции, недавние статьи и руководства без точного номера статьи."),
                        ("Переходите к поиску, когда цель известна", "Поиск по номеру и названию доступен бесплатно. Premium добавляет теги, классы объектов, текст, заметки, статус чтения, официальный рейтинг, длину и сохранённые условия."),
                    ],
                ),
                (
                    "Превратите просмотр в состояние Библиотеки",
                    [
                        ("Сохраните статью", "Добавьте закладку, отметьте «прочитать позже», оцените или оставьте заметку, чтобы отчёт не был просто ещё одной страницей архива."),
                        ("Возвращайтесь с контекстом", "История, продолжение чтения, статус, оценки, заметки и позиция прокрутки помогают вернуться к тому же файлу или серии."),
                        ("Организуйте длинное чтение", "Premium расширяет лимиты, добавляет папки закладок, редактирование заметок, синхронизацию через iCloud Drive и офлайн-снимки подходящих статей."),
                    ],
                ),
            ],
            "guide_items": [
                ("Хочу просматривать без конкретной статьи", "Начните с Главной, выберите филиал и откройте маршруты архива, например SCP, SCP-INT, Stories или Others. Каталог позволяет двигаться по сериям и блокам, видя названия, классы объектов, теги, оценки и миниатюры, если они есть."),
                ("Я знаю номер, название, тег или класс объекта", "Используйте Поиск. Номер и название доступны обычно, а Premium-фильтры помогают сузить результат по группе документов, филиалу, тегам, официальной оценке, длине, классу объекта, статусу чтения и заметкам."),
                ("Я нашёл материал, который хочу сохранить", "Сохраните его из ридера или Библиотеки как закладку, «прочитать позже», оценку, заметку или запись в папке. Так статья будет видна позже в Библиотеке без опоры на память или историю браузера."),
                ("Я остановился на середине серии", "Используйте продолжение чтения, историю Библиотеки, сохранённую позицию прокрутки и статус чтения, чтобы вернуться к тому же отчёту или отслеживать прогресс."),
            ],
        },
        "ko": {
            "overview_label": "기능 개요",
            "screens_label": "스크린샷",
            "screens_title": "흐름에 맞춘 화면",
            "workflow_label": "아카이브와 라이브러리 흐름",
            "workflow_title": "아카이브 목록에서 개인 읽기 선반으로",
            "guide_label": "사용 가이드",
            "guide_title": "상황별로 사용할 곳",
            "points_label": "기능",
            "points_title": "주요 기능",
            "hero_alt": "이어 읽기, 아카이브 경로, 검색 필터가 보이는 한국어 UI의 홈 화면",
            "pills": ["홈", "아카이브 경로", "라이브러리", "검색", "통계", "공유 카드"],
            "screens": [
                ("home", "지부 선택, 이어 읽기, 아카이브 경로, 빠른 필터가 보이는 홈 화면", "홈: 지부, 아카이브 경로, 이어 읽기"),
                ("catalog", "시리즈와 번호 블록으로 글을 찾는 SCP 카탈로그 화면", "카탈로그: 번호를 몰라도 목록에서 탐색"),
                ("library", "읽기 상태, 평점, 북마크, 저장 상태를 보여 주는 라이브러리 화면", "라이브러리: 기록, 평점, 북마크, 저장 상태"),
                ("search", "번호, 키워드, 태그, 지부, 종류, Object Class, 고급 필터가 보이는 검색 화면", "검색: 번호, 키워드, 태그, 고급 필터"),
            ],
            "workflow_cards": [
                (
                    "홈을 아카이브 지도로 사용하기",
                    [
                        ("지부 선택", "영어, 일본어, 프랑스어, 러시아어, 한국어를 선택할 수 있습니다. 홈, 검색, 목록, 글 링크, 앱 언어가 선택한 지부의 문맥에 맞춰집니다."),
                        ("디렉터리에서 시작", "SCP 글, Tales, Canons, Canon series, GoI, Joke SCP, SCP-EX, 컬렉션, 최근 글, 가이드류를 정확한 번호를 몰라도 탐색할 수 있습니다."),
                        ("목표를 알 때는 검색", "번호와 제목 검색은 무료로 사용할 수 있습니다. 프리미엄 고급 검색은 태그, Object Class, 본문, 메모, 읽기 상태, 공식 점수, 길이, 저장 조건까지 좁힐 수 있습니다."),
                    ],
                ),
                (
                    "탐색을 라이브러리 상태로 바꾸기",
                    [
                        ("글 저장", "북마크, 나중에 읽기, 평점, 메모를 사용하면 글이 단순한 페이지가 아니라 개인 읽기 선반에 남습니다."),
                        ("문맥과 함께 이어 읽기", "기록, 이어 읽기, 읽음 상태, 평점, 메모, 스크롤 위치로 같은 보고서나 시리즈에 다시 돌아갈 수 있습니다."),
                        ("긴 읽기 정리", "프리미엄에서는 저장 한도 확장, 북마크 폴더, 메모 편집, iCloud Drive 동기화, 대상 글 오프라인 저장을 사용할 수 있습니다."),
                    ],
                ),
            ],
            "guide_items": [
                ("특정 글을 정하지 않고 탐색하고 싶을 때", "홈에서 지부를 선택하고 SCP, SCP-INT, Stories, Others 같은 아카이브 경로를 엽니다. 카탈로그 화면에서는 시리즈와 번호 블록으로 이동하면서 제목, Object Class, 태그, 점수, 썸네일을 보고 찾을 수 있습니다."),
                ("번호, 제목, 태그, Object Class를 알고 있을 때", "검색을 사용합니다. 번호와 제목 검색은 일반적으로 사용할 수 있고, 프리미엄 고급 필터는 문서 종류, 지부, 태그, 공식 점수, 길이, Object Class, 읽기 상태, 메모까지 좁힙니다."),
                ("나중에 다시 읽고 싶은 글을 찾았을 때", "리더나 라이브러리에서 북마크, 나중에 읽기, 평점, 메모, 폴더로 저장합니다. 나중에는 기억이나 브라우저 기록에 의존하지 않고 라이브러리에서 찾을 수 있습니다."),
                ("시리즈를 중간에 멈췄을 때", "이어 읽기, 라이브러리 기록, 저장된 스크롤 위치, 읽음 상태를 사용해 같은 보고서나 진행 상황으로 돌아갈 수 있습니다."),
            ],
        },
        "es": {
            "overview_label": "Resumen de funciones",
            "screens_label": "Capturas",
            "screens_title": "Pantallas alineadas con el flujo de lectura",
            "workflow_label": "Flujo de archivo y Biblioteca",
            "workflow_title": "De las listas del archivo a tu estantería de lectura",
            "guide_label": "Guía práctica",
            "guide_title": "Qué usar en cada momento",
            "points_label": "Qué hace",
            "points_title": "Funciones principales",
            "hero_alt": "Pantalla de inicio de SCP Docs con continuar leyendo, rutas de archivo y filtros de búsqueda",
            "pills": ["Inicio", "Rutas de archivo", "Biblioteca", "Búsqueda", "Estadísticas", "Tarjetas"],
            "screens": [
                ("home", "Pantalla de inicio con selección de rama, continuar leyendo, rutas de archivo y filtros rápidos", "Inicio: rama, rutas de archivo y continuar leyendo"),
                ("catalog", "Catálogo SCP con filas de artículos, filtros por serie y por bloque", "Catálogo: explora artículos antes de saber el número"),
                ("library", "Biblioteca con historial, estado de lectura, valoraciones, marcadores y acciones rápidas", "Biblioteca: historial, valoraciones, marcadores y estado guardado"),
                ("search", "Búsqueda por número, palabra clave, etiqueta, rama, tipo, Clase de Objeto y filtros avanzados", "Búsqueda: número, palabra clave, etiqueta y filtros avanzados"),
            ],
            "workflow_cards": [
                (
                    "Usa el Inicio como mapa del archivo",
                    [
                        ("Elige una rama", "Selecciona inglés, japonés, francés, ruso o coreano. El Inicio, la búsqueda, las listas, los enlaces a artículos y el idioma de la app siguen ese contexto de rama."),
                        ("Empieza por los directorios", "Recorre informes SCP, Tales, Canons, series Canon, GoI, Joke SCP, SCP-EX, colecciones, artículos recientes y guías sin necesitar primero el número exacto."),
                        ("Salta cuando conoces el objetivo", "La búsqueda por número y título es gratuita. La búsqueda avanzada Premium añade etiquetas, Clase de Objeto, texto del documento, notas, estado de lectura, puntuación oficial, longitud y condiciones guardadas."),
                    ],
                ),
                (
                    "Convierte la navegación en estado de Biblioteca",
                    [
                        ("Guarda el artículo", "Márcalo como favorito, ponlo en leer más tarde, valóralo o deja una nota para que el informe deje de ser una página más del archivo."),
                        ("Reanuda con contexto", "El historial, continuar leyendo, el estado de lectura, las valoraciones, las notas y la posición de desplazamiento te ayudan a volver al mismo expediente o serie tras una pausa."),
                        ("Organiza proyectos largos", "Premium amplía los límites de guardado, añade carpetas de marcadores, permite editar notas, puede sincronizar la Biblioteca a través de tu propio iCloud Drive y guardar artículos aptos para leer sin conexión."),
                    ],
                ),
            ],
            "guide_items": [
                ("Quiero explorar sin un artículo concreto en mente", "Empieza en Inicio, elige la rama y abre rutas de archivo como SCP, SCP-INT, Stories u Others. La pantalla de catálogo permite moverse por series y bloques, con filas que muestran títulos, Clase de Objeto, etiquetas, puntuaciones y miniaturas cuando existen."),
                ("Conozco el número, el título, la etiqueta o la Clase de Objeto", "Usa Búsqueda. La búsqueda por número y título está disponible en el uso normal, y los filtros avanzados Premium permiten acotar por grupo de documentos, rama, etiquetas, puntuación oficial, longitud, Clase de Objeto, estado de lectura y notas."),
                ("Encontré algo que quiero conservar", "Guárdalo desde el lector o la Biblioteca como marcador, leer más tarde, valoración, nota o entrada de carpeta. Esas señales hacen visible el artículo más adelante desde la Biblioteca, sin depender de la memoria ni del historial del navegador."),
                ("Dejé una serie a medias", "Usa Continuar leyendo, el historial de la Biblioteca, la posición de desplazamiento guardada y el estado de lectura para volver al mismo informe o repasar lo que ya está atendido."),
            ],
        },
    }
    ui = feature_copy[lang]
    card_html = "\n".join(
        f"""          <div class="feature-card">
            <p class="section-label">{label}</p>
            <h3>{heading}</h3>
            <p>{text}</p>
          </div>"""
        for label, heading, text in cards
    )
    pill_html = "\n".join(f'              <span class="code-chip">{pill}</span>' for pill in ui["pills"])
    screen_html = "\n".join(
        f"""          <figure class="screen-frame">
            <img src="{screenshot_path(lang, kind)}" alt="{alt}" />
            <figcaption>{caption}</figcaption>
          </figure>"""
        for kind, alt, caption in ui["screens"]
    )
    workflow_html = "\n".join(
        f"""          <div class="card">
            <h3>{heading}</h3>
            <dl class="dl-flat">
{chr(10).join(f'              <dt>{term}</dt>{chr(10)}              <dd>{definition}</dd>' for term, definition in items)}
            </dl>
          </div>"""
        for heading, items in ui["workflow_cards"]
    )
    guide_html = "\n".join(
        f"""            <dt>{term}</dt>
            <dd>{definition}</dd>"""
        for term, definition in ui["guide_items"]
    )
    body = f"""
    <main class="main-pad">
      <section aria-labelledby="feature-title">
        <p class="section-label">{ui['overview_label']}</p>
        <h2 id="feature-title" class="section-title-lg">{h2}</h2>
        <div class="feature-hero">
          <div>
            <p class="lede">{lede}</p>
            <div class="pill-row">
{pill_html}
            </div>
          </div>
          <figure class="screen-frame screen-frame-compact">
            <img src="{screenshot_path(lang, 'home')}" alt="{ui['hero_alt']}" />
          </figure>
        </div>
      </section>

      <section aria-labelledby="screens-title" style="margin-top:38px;">
        <p class="section-label">{ui['screens_label']}</p>
        <h2 id="screens-title" class="section-title-lg">{ui['screens_title']}</h2>
        <div class="feature-shot-grid">
{screen_html}
        </div>
      </section>

      <section aria-labelledby="archive-workflow-title" style="margin-top:38px;">
        <p class="section-label">{ui['workflow_label']}</p>
        <h2 id="archive-workflow-title" class="section-title-lg">{ui['workflow_title']}</h2>
        <div class="grid-2">
{workflow_html}
        </div>
      </section>

      <section aria-labelledby="use-cases-title" style="margin-top:38px;">
        <p class="section-label">{ui['guide_label']}</p>
        <h2 id="use-cases-title" class="section-title-lg">{ui['guide_title']}</h2>
        <div class="card">
          <dl class="dl-flat">
{guide_html}
          </dl>
        </div>
      </section>

      <section aria-labelledby="points-title" style="margin-top:38px;">
        <p class="section-label">{ui['points_label']}</p>
        <h2 id="points-title" class="section-title-lg">{ui['points_title']}</h2>
        <div class="feature-grid">
{card_html}
        </div>
      </section>

{cmp_section(lang)}

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


for code in LANGS:
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
        "es": {
            "title": "Política de privacidad — SCP Docs",
            "description": "Política de privacidad de SCP Docs: datos en el dispositivo, sincronización con iCloud Drive, búsquedas guardadas, notificaciones, anuncios, suscripciones y sitios de origen de terceros.",
            "heading": "Política de privacidad",
            "updated": "Última actualización: 24 de junio de 2026",
            "sections": [
                ("1. Introducción", "Esta Política de privacidad describe cómo se trata la información en la aplicación móvil «SCP Docs» (la «App»). Lee esta Política antes de usar la App. Si no estás de acuerdo con ella, no utilices la App."),
                ("2. Operador y contacto", f'Para consultas de privacidad sobre la App:<br /><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
                ("3. Resumen de la información que tratamos", "La App conserva un estado en el dispositivo para que puedas explorar, organizar, reanudar y repasar artículos. También realiza comunicaciones de red cuando es necesario para catálogos, páginas de origen, compras, anuncios y enlaces. No es necesario crear una cuenta para usar la App."),
                ("4. Información almacenada en tu dispositivo", "La App puede almacenar URL o claves normalizadas de artículos, historial de navegación, estado de lectura, valoraciones, favoritos, marcadores, entradas de leer más tarde, carpetas de marcadores, posición de desplazamiento, títulos o miniaturas en caché, notas, condiciones de búsqueda guardadas, estado de coincidencias, registros de sesiones de lectura, datos de estadísticas de lectura, instantáneas HTML sin conexión, estado de suscripción y caducidad del Premium temporal por anuncio con recompensa. Estos datos sirven para el historial, la reanudación, la biblioteca, la búsqueda avanzada, las notas, las búsquedas guardadas, las estadísticas, la lectura sin conexión y el estado Premium."),
                ("5. Sincronización con iCloud Drive", "Si has iniciado sesión en iCloud Drive y la función está disponible, el estado de lectura, las notas, las búsquedas guardadas y las carpetas de marcadores pueden sincronizarse a través de tu propio almacenamiento de iCloud. El operador de la App no gestiona un servidor separado para recopilar estos registros de lectura o notas."),
                ("6. Actividad de red y notificaciones", "La actividad de red se produce cuando la App descarga datos de catálogo, etiquetas y listas, muestra el cuerpo de artículos desde Wikidot u otros sitios externos, comprueba el estado de la suscripción del App Store, abre enlaces externos o carga anuncios de Google AdMob. Las notificaciones de búsquedas guardadas se generan en el dispositivo tras comprobar los datos del catálogo; su entrega depende del permiso de notificaciones de iOS."),
                ("7. Publicidad (Google AdMob)", 'La App utiliza el Google Mobile Ads SDK (AdMob), proporcionado por Google LLC, y puede mostrar anuncios de tipo banner, integrados, nativos, intersticiales, con recompensa y formatos similares. Durante la entrega de anuncios, pueden transmitirse identificadores e información del dispositivo o de impresiones a Google y a socios publicitarios con fines de entrega, medición, prevención del fraude y similares. Consulta la <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Política de privacidad de Google</a> y <a href="https://developers.google.com/admob/ios/privacy/play-data-disclosure" rel="noopener noreferrer">Ads &amp; privacy</a>. Según los ajustes de iOS y tus decisiones, la personalización puede estar limitada.'),
                ("8. Sitios de terceros", "Gran parte del contenido al que accedes a través de la App está alojado en sitios web operados por terceros. Se aplican sus registros, cookies, scripts de análisis, reglas del sitio y políticas de privacidad. No controlamos cómo los sitios de terceros tratan la información."),
                ("9. Divulgación a terceros y requerimientos legales", "Además de las divulgaciones descritas anteriormente, como publicidad, pagos, infraestructura de entrega de contenido y diagnósticos ofrecidos por el sistema operativo o el App Store, podemos divulgar información cuando lo exija la ley o en respuesta a requerimientos legítimos de tribunales o autoridades públicas."),
                ("10. Seguridad", "Nos esforzamos por aplicar salvaguardas razonables a los entornos en los que se desarrolla y distribuye la App. Sin embargo, la seguridad no puede garantizarse de forma absoluta en Internet ni en dispositivos móviles."),
                ("11. Conservación", "Los datos almacenados en el dispositivo o en tu iCloud Drive pueden conservarse hasta que desinstales la App, elimines datos con los controles de la App, elimines los archivos de iCloud relacionados o restablezcas el dispositivo o el sistema, según corresponda."),
                ("12. Menores", "La App está destinada a lectores en general. Si permites que un menor use la App, hazlo con la supervisión parental adecuada."),
                ("13. Cambios en esta Política", "Podemos modificar esta Política para reflejar requisitos legales, cambios en la App o necesidades operativas. Las actualizaciones se publicarán en esta página y, cuando proceda, se mostrarán en la App."),
                ("14. Preguntas", f'Preguntas sobre esta Política: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> o <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.'),
            ],
        },
    }
    return privacy[lang]


for code in ["fr", "ru", "ko", "es"]:
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
        "es": (
            "Términos de uso — SCP Docs",
            "Términos de uso de SCP Docs: estado no oficial, licencias del contenido de origen, suscripciones Premium, desbloqueos con recompensa, servicios de terceros y exenciones de responsabilidad.",
            "Términos de uso",
            "Última actualización: 24 de junio de 2026",
            [
                ("1. Alcance y aceptación", "Estos Términos de uso (los «Términos») rigen tu uso de la aplicación móvil «SCP Docs» (la «App»). Al descargar o usar la App, aceptas quedar vinculado por estos Términos."),
                ("2. Naturaleza del servicio", "La App no es una aplicación oficial proporcionada o respaldada por la SCP Foundation, Wikidot, Inc. ni ningún operador oficial del contenido referenciado. Es software no oficial hecho por fans. Las referencias a nombres o universos de ficción son solo por comodidad y no implican asociación, respaldo ni representación."),
                ("3. Contenido y licencias", 'Gran parte del texto y las imágenes accesibles a través de la App se publica por colaboradores individuales bajo licencias como Creative Commons Attribution-ShareAlike 3.0 Unported (<strong>CC BY-SA 3.0</strong>). El <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">texto completo de la licencia</a> está disponible en Creative Commons. Si reproduces, redistribuyes o modificas artículos u otros materiales, debes cumplir la licencia aplicable y las reglas de cada sitio de origen. La App en sí no es el licenciante del contenido de terceros.'),
                ("4. Funciones de la App y datos personales", "La App ofrece navegación por archivos, búsqueda por rama, estado de lectura, marcadores, leer más tarde, valoraciones, notas, tarjetas para compartir, búsquedas guardadas, estadísticas de lectura, lectura en voz alta, instantáneas sin conexión y herramientas de lectura relacionadas. El tratamiento de datos se describe en la Política de privacidad."),
                ("5. Compras, suscripciones y desbloqueos con recompensa", "Las funciones Premium pueden ofrecerse mediante suscripciones con renovación automática, otras compras dentro de la app o desbloqueos temporales por anuncios con recompensa cuando estén disponibles. Apple Inc. gestiona el procesamiento de compras de suscripciones, la facturación, la cancelación, los reembolsos y asuntos relacionados a través del App Store. Un desbloqueo por anuncio con recompensa, cuando se ofrece, solo otorga acceso temporal y no sustituye a una suscripción. La disponibilidad de funciones y los límites pueden cambiar con las actualizaciones de la App o los requisitos de revisión del App Store."),
                ("6. Servicios de terceros y sitios externos", "La App depende de la infraestructura de pago del App Store, plataformas publicitarias, iCloud Drive cuando está activado y sitios web operados por terceros. Cada servicio se rige por sus propios términos y su política de privacidad. Los sitios de origen siguen siendo la referencia autorizada para el texto de los artículos, la autoría, las licencias, las advertencias y las reglas del sitio."),
                ("7. Usos prohibidos", "Te comprometes a no infringir la ley aplicable ni el orden público, no vulnerar derechos de terceros, no imponer una carga indebida a la App o a la infraestructura relacionada, no intentar redistribuciones o descompilaciones no autorizadas, no eludir los mecanismos de compra o publicidad, ni realizar conductas que el operador determine razonablemente inapropiadas."),
                ("8. Exenciones y limitación de responsabilidad", "La App se proporciona «TAL CUAL». El operador no garantiza que la App satisfaga tus requisitos particulares ni que esté disponible, sea precisa, ininterrumpida o libre de errores. En la máxima medida permitida por la ley aplicable, el operador no será responsable de los daños derivados de la App, salvo en casos de dolo o negligencia grave."),
                ("9. Cambios en los Términos", "El operador puede revisar estos Términos cuando sea necesario. Los Términos revisados entran en vigor cuando se publican en esta página o se muestran a través de la App, según proceda."),
                ("10. Ley aplicable y jurisdicción", "Estos Términos se aplican a la luz de la ley aplicable y de los acuerdos con proveedores de plataforma como Apple. Las disputas se resolverán conforme a la ley aplicable correspondiente. Si es necesario indicar una ley o jurisdicción concreta, esta sección podrá actualizarse o complementarse."),
                ("11. Contacto", f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br /><a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>'),
            ],
        ),
    }
    title, description, heading, updated, sections = data[lang]
    return {"title": title, "description": description, "heading": heading, "updated": updated, "sections": sections}


for code in ["ja", "fr", "ru", "ko", "es"]:
    TERMS_TEXT[code] = make_terms(code)


SUPPORT_TEXT = {
    "en": {
        "title": "Support — SCP Docs",
        "description": "SCP Docs support: contact, requirements, archive and Library workflow, supported branches, Premium features, offline reading, ads, iCloud sync, notifications, and source-site notes.",
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
            ("Which branches and languages are supported?", "The app currently supports the English main archive and the Japanese, French, Russian, and Korean branches. The app UI currently supports English, Japanese, French, Russian, and Korean."),
            ("How should I use the archive and Library?", "Start from Home, choose a branch, then browse directory routes such as SCP reports, Tales, Canons, GoI, Joke SCPs, SCP-EX, collections, recent articles, and guides. Use Search when you know a number, title, tag, or Object Class. When you find something useful, bookmark it, mark it read-later, rate it, add a memo, or place it in a folder so it stays available from Library and continue-reading."),
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
            [("アカウントやログインは必要ですか？", "不要です。SCP Docs は Wikidot アカウントなしで閲覧できるよう設計しています。記事編集やコメント投稿は、各公式サイトの規則に従います。"), ("どの支部と言語に対応していますか？", "アプリは現在、英語本家アーカイブと日本・フランス・ロシア・韓国支部に対応しています。アプリUIは英語・日本語・フランス語・ロシア語・韓国語に対応しています。"), ("一覧やタイトルが古い、取得できない", "カタログデータはオンラインで取得し、端末にキャッシュされます。通信状態を確認し、設定からカタログを更新するか、アプリを再起動してください。元サイトの変更には後続のカタログ更新が必要な場合があります。"), ("無料機能とプレミアム機能は何が違いますか？", "番号・タイトル検索、読書、基本的な書庫機能、履歴、評価、ブックマーク、後で読むは通常利用できます。プレミアムでは広告非表示、高度な検索、メモ編集、保存上限拡張、オフライン保存、読書統計、読み上げ、保存検索通知、iCloud 同期対応のブックマークフォルダが利用できます。"), ("オフラインで読みたい", "オフライン保存はプレミアム機能です。プレミアム有効中は、対象の保存済み記事にローカル HTML スナップショットを保持できます。オフライン時に表示できるのは保存済みコピーのある記事のみで、画像、外部リソース、未保存記事、カタログ更新には通信が必要です。"), ("広告を消したい / バナーが出る", "無料利用中は、バナー、記事内、ネイティブフィード、インタースティシャル、リワード広告等が表示されます。月額プレミアム有効中は広告が非表示になります。未購読の場合でも、利用可能なときはリワード広告で一時的にプレミアムを解放できます。"), ("保存検索と通知はどう動きますか？", "保存検索はプレミアム機能です。アプリはカタログ同期後に端末上で一致を確認し、新しい該当項目がある場合に通知できます。iOS の通知許可が必要で、運営者サーバーから通知を生成する仕組みではありません。"), ("自分のデータはどこへ送られますか？", "閲覧履歴、進捗、評価、ブックマーク、後で読む、メモ、読書時間、フォルダ、保存検索、オフラインスナップショット、リワード期限は基本的に端末内に保存されます。iCloud Drive が利用可能な場合、読書状態、メモ、保存検索、ブックマークフォルダは自分の iCloud 領域を通じて同期されることがあります。詳しくはプライバシーポリシーをご覧ください。")],
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
            [("Faut-il un compte ou une connexion ?", "Non. SCP Docs est conçu pour lire sans compte Wikidot. Modifier des articles ou publier des commentaires suit les règles de chaque site source."), ("Quelles branches et langues sont prises en charge ?", "L'app prend actuellement en charge l'archive principale anglaise ainsi que les branches japonaise, française, russe et coréenne. L'interface de l'app prend en charge l'anglais, le japonais, le français, le russe et le coréen."), ("Les listes ou titres semblent anciens / impossible de récupérer", "Les catalogues sont téléchargés en ligne et mis en cache sur l'appareil. Vérifiez la connexion, actualisez les catalogues dans Réglages ou redémarrez l'app. Certains changements de sites sources nécessitent une mise à jour de catalogue ultérieure."), ("Qu'est-ce qui est gratuit ou Premium ?", "La recherche par numéro/titre, la lecture, les fonctions de bibliothèque de base, l'historique, les notes, favoris et éléments à lire plus tard sont utilisables normalement. Premium ajoute suppression des publicités, recherche avancée, édition des mémos, limites étendues, hors ligne, statistiques, synthèse vocale, alertes de recherches enregistrées et dossiers de favoris synchronisés via iCloud."), ("Je veux lire hors ligne", "La sauvegarde hors ligne est Premium. Pendant que Premium est actif, les articles éligibles sauvegardés peuvent conserver un instantané HTML local. Hors ligne, seuls les articles avec copie sauvegardée s'affichent ; images, ressources externes, articles non sauvegardés et mises à jour de catalogues nécessitent le réseau."), ("Je veux supprimer les publicités / je vois une bannière", "Des publicités apparaissent en usage gratuit : bannières, intégrées, natives, interstitielles, récompensées et formats similaires. Premium mensuel actif les masque. Sans abonnement, une publicité récompensée peut donner un accès Premium temporaire lorsqu'elle est disponible."), ("Comment fonctionnent recherches enregistrées et notifications ?", "Les recherches enregistrées sont Premium. L'app vérifie le catalogue sur l'appareil après synchronisation et peut notifier les nouvelles entrées correspondantes. L'autorisation iOS est requise et les notifications ne viennent pas d'un serveur de l'opérateur."), ("Où mes données sont-elles envoyées ?", "Historique, progression, notes, favoris, à lire plus tard, mémos, temps de lecture, dossiers, recherches enregistrées, instantanés hors ligne et expiration récompensée sont principalement stockés sur votre appareil. Si iCloud Drive est disponible, l'état de lecture, mémos, recherches enregistrées et dossiers peuvent se synchroniser via votre iCloud. Voir la Politique de confidentialité.")],
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
            [("Нужен ли аккаунт или вход?", "Нет. SCP Docs рассчитан на чтение без аккаунта Wikidot. Редактирование статей или комментарии подчиняются правилам исходных сайтов."), ("Какие филиалы и языки поддерживаются?", "Приложение сейчас поддерживает основной английский архив, а также японский, французский, русский и корейский филиалы. Интерфейс приложения поддерживает английский, японский, французский, русский и корейский языки."), ("Списки или названия старые / не загружаются", "Каталоги скачиваются онлайн и кэшируются на устройстве. Проверьте соединение, обновите каталоги в Настройках или перезапустите приложение. Изменения исходных сайтов могут требовать последующего обновления каталога."), ("Что бесплатно, а что Premium?", "Поиск по номеру и названию, чтение, базовая библиотека, история, оценки, закладки и «прочитать позже» доступны в обычном режиме. Premium добавляет скрытие рекламы, расширенный поиск, редактирование заметок, большие лимиты, офлайн, статистику, озвучивание, уведомления сохранённых поисков и папки закладок с iCloud."), ("Хочу читать офлайн", "Офлайн-сохранение — функция Premium. Пока Premium активен, подходящие сохранённые статьи могут хранить локальный HTML-снимок. Без сети отображаются только статьи с сохранёнными копиями; изображения, внешние ресурсы, несохранённые статьи и обновления каталогов требуют сеть."), ("Хочу убрать рекламу / вижу баннер", "В бесплатном режиме могут показываться баннеры, встроенная, нативная, межстраничная, вознаграждаемая и похожая реклама. Активный месячный Premium скрывает рекламу. Без подписки рекламный просмотр может временно открыть Premium, если доступен."), ("Как работают сохранённые поиски и уведомления?", "Сохранённые поиски — Premium. Приложение проверяет каталог на устройстве после синхронизации и может уведомлять о новых совпадениях. Требуется разрешение iOS; уведомления не генерируются сервером оператора."), ("Куда отправляются мои данные?", "История, прогресс, оценки, закладки, «прочитать позже», заметки, время чтения, папки, сохранённые поиски, офлайн-снимки и срок рекламного Premium в основном хранятся на устройстве. Если доступен iCloud Drive, состояние чтения, заметки, сохранённые поиски и папки могут синхронизироваться через ваш iCloud. См. Политику конфиденциальности.")],
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
            [("계정이나 로그인이 필요한가요?", "아니요. SCP Docs는 Wikidot 계정 없이 읽을 수 있도록 설계되었습니다. 글 편집이나 댓글 작성은 각 원본 사이트의 규칙을 따릅니다."), ("어떤 지부와 언어를 지원하나요?", "앱은 현재 영어 본가 아카이브와 일본어, 프랑스어, 러시아어, 한국어 지부를 지원합니다. 앱 UI는 영어, 일본어, 프랑스어, 러시아어, 한국어를 지원합니다."), ("목록이나 제목이 오래되었거나 가져올 수 없어요", "카탈로그 데이터는 온라인에서 다운로드되어 기기에 캐시됩니다. 연결을 확인한 뒤 설정에서 카탈로그를 새로고침하거나 앱을 다시 시작하세요. 원본 사이트 변경에는 이후 카탈로그 업데이트가 필요할 수 있습니다."), ("무료와 프리미엄은 무엇이 다른가요?", "번호·제목 검색, 읽기, 기본 라이브러리, 기록, 평가, 북마크, 나중에 읽기는 일반적으로 사용할 수 있습니다. 프리미엄은 광고 제거, 고급 검색, 메모 편집, 저장 한도 확장, 오프라인 저장, 읽기 통계, 텍스트 음성 변환, 저장 검색 알림, iCloud 동기화 북마크 폴더를 추가합니다."), ("오프라인으로 읽고 싶어요", "오프라인 저장은 프리미엄 기능입니다. 프리미엄이 활성화되어 있는 동안 저장 가능한 글은 로컬 HTML 스냅샷을 유지할 수 있습니다. 오프라인에서는 저장된 사본이 있는 글만 표시되며, 이미지, 외부 리소스, 저장하지 않은 글, 카탈로그 업데이트에는 네트워크가 필요합니다."), ("광고를 없애고 싶어요 / 배너가 보여요", "무료 사용 중에는 배너, 인라인, 네이티브 피드, 전면, 리워드 등 광고가 표시될 수 있습니다. 월간 프리미엄이 활성화되어 있으면 광고가 숨겨집니다. 구독하지 않은 경우 제공되는 리워드 광고로 임시 프리미엄을 받을 수 있습니다."), ("저장 검색과 알림은 어떻게 동작하나요?", "저장 검색은 프리미엄 기능입니다. 앱은 카탈로그 동기화 후 기기에서 일치 항목을 확인하고 새 결과가 있으면 알림을 표시할 수 있습니다. iOS 알림 권한이 필요하며, 운영자 서버가 알림을 생성하는 방식은 아닙니다."), ("내 데이터는 어디로 전송되나요?", "열람 기록, 진행률, 평가, 북마크, 나중에 읽기, 메모, 읽기 시간, 폴더, 저장 검색, 오프라인 스냅샷, 리워드 만료 정보는 주로 기기에 저장됩니다. iCloud Drive를 사용할 수 있으면 읽기 상태, 메모, 저장 검색, 북마크 폴더가 사용자의 iCloud 저장 공간을 통해 동기화될 수 있습니다. 자세한 내용은 개인정보 처리방침을 참조하세요.")],
            "원본 콘텐츠가 기준입니다",
            "권리, 공식 본문, 저자 표시, 경고, 라이선스 고지는 각 원본 사이트가 기준입니다. SCP Docs는 탐색과 개인 읽기 상태를 돕는 리더 계층이며, 원본 사이트 규칙을 대체하지 않습니다.",
        ),
        "es": (
            "Soporte — SCP Docs",
            "Soporte de SCP Docs: contacto, requisitos, ramas compatibles, funciones Premium, lectura sin conexión, anuncios, sincronización con iCloud, notificaciones y sitios de origen.",
            "Soporte",
            "Contacto",
            "Las solicitudes de funciones, los problemas de visualización, los problemas de catálogo y los comentarios se aceptan por correo electrónico cuando es posible. La respuesta puede tardar varios días.",
            "Incluye tu versión de iOS, la versión de la app SCP Docs, la rama seleccionada y la pantalla o acción donde ocurrió el problema.",
            "Requisitos",
            [("Plataforma", "iPhone / iPod touch. El comportamiento en iPad depende del dispositivo y de la compatibilidad del sistema."), ("OS", "Las versiones actuales del App Store están dirigidas a iOS 17 y posteriores."), ("Red", "Necesaria para actualizar listas, leer en línea, cargar contenido de los sitios de origen, compras, anuncios y comprobaciones de búsquedas guardadas. La lectura sin conexión solo funciona con instantáneas guardadas."), ("Sitios de origen", "Los cambios de diseño o el mantenimiento de Wikidot y otros sitios de origen pueden causar problemas de visualización temporales o cargas más lentas.")],
            "Preguntas frecuentes",
            [("¿Necesito una cuenta o iniciar sesión?", "No. SCP Docs está diseñada para leer sin cuenta de Wikidot. Editar artículos o publicar comentarios sigue las reglas de cada sitio oficial de origen."), ("¿Qué ramas e idiomas son compatibles?", "La app admite actualmente el archivo principal en inglés y las ramas japonesa, francesa, rusa y coreana. La interfaz de la app está disponible en inglés, japonés, francés, ruso y coreano."), ("Las listas o los títulos parecen antiguos / no se pueden obtener", "Los datos de catálogo se descargan en línea y se guardan en caché en tu dispositivo. Comprueba la conexión, actualiza los catálogos desde Ajustes o reinicia la app. Algunos cambios de los sitios de origen pueden requerir una actualización de catálogo posterior."), ("¿Qué es gratis y qué es Premium?", "La búsqueda por número y título, la lectura, las funciones básicas de biblioteca, el historial, las valoraciones, los marcadores y leer más tarde están disponibles en el uso normal. Premium añade eliminación de anuncios, búsqueda avanzada, edición de notas, límites de guardado más altos, almacenamiento sin conexión, estadísticas de lectura, lectura en voz alta, avisos de búsquedas guardadas y carpetas de marcadores con sincronización iCloud."), ("Quiero leer sin conexión", "El guardado sin conexión es una función Premium. Mientras Premium está activo, los artículos guardados aptos pueden conservar una instantánea HTML local. Si estás sin conexión, solo pueden mostrarse los artículos con copia guardada; las imágenes, los recursos externos, los artículos no guardados y las actualizaciones de catálogo siguen requiriendo conexión."), ("Quiero quitar los anuncios / veo un banner", "Durante el uso gratuito se muestran anuncios de tipo banner, integrados, nativos, intersticiales, con recompensa y formatos similares. Mientras el Premium mensual está activo, los anuncios se ocultan. Si no estás suscrito, un anuncio con recompensa puede otorgar acceso Premium temporal cuando esté disponible."), ("¿Cómo funcionan las búsquedas guardadas y las notificaciones?", "Las búsquedas guardadas son Premium. La app comprueba los datos de catálogo en el dispositivo tras la sincronización y puede avisarte cuando aparecen nuevas entradas coincidentes. Se requiere el permiso de notificaciones de iOS, y las notificaciones no se generan en un servidor del operador."), ("¿Adónde se envían mis datos?", "El historial de lectura, el progreso, las valoraciones, los marcadores, leer más tarde, las notas, el tiempo de lectura, las carpetas, las búsquedas guardadas, las instantáneas sin conexión y la caducidad del Premium por recompensa se almacenan principalmente en tu dispositivo. Si iCloud Drive está disponible, el estado de lectura, las notas, las búsquedas guardadas y las carpetas de marcadores pueden sincronizarse a través de tu propio almacenamiento de iCloud. Consulta la Política de privacidad para más detalles.")],
            "El contenido de origen es la referencia autorizada",
            "Los derechos, el texto oficial, los créditos de autor, las advertencias y los avisos de licencia se rigen por cada sitio de origen. SCP Docs es una capa de lectura que ayuda con la navegación y el estado personal de lectura; no sustituye las reglas de los sitios de origen.",
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
    support_descriptions = {
        "ja": "SCP Docs のサポート。連絡先、動作環境、書庫とライブラリの使い方、対応支部、プレミアム機能、オフライン読書、広告、iCloud同期、通知、元サイトに関する注意。",
        "fr": "Assistance SCP Docs : contact, configuration, flux archive et bibliothèque, branches prises en charge, Premium, lecture hors ligne, publicités, iCloud, notifications et sites sources.",
        "ru": "Поддержка SCP Docs: контакты, требования, архив и Библиотека, филиалы, Premium, офлайн-чтение, реклама, iCloud, уведомления и исходные сайты.",
        "ko": "SCP Docs 지원: 문의, 요구 사항, 아카이브와 라이브러리 사용법, 지원 지부, 프리미엄 기능, 오프라인 읽기, 광고, iCloud 동기화, 알림, 원본 사이트 안내.",
        "es": "Soporte de SCP Docs: contacto, requisitos, flujo de archivo y Biblioteca, ramas compatibles, funciones Premium, lectura sin conexión, anuncios, sincronización con iCloud, notificaciones y sitios de origen.",
    }
    archive_faq = {
        "ja": ("書庫とライブラリはどう使い分けますか？", "まずホームで支部を選び、SCP記事、Tales、Canons、GoI、Joke SCP、SCP-EX、コレクション、新着記事、ガイドなどの書庫ルートから探します。目的の記事が分かっている場合は検索を使います。見つけた記事はブックマーク、後で読む、評価、メモ、フォルダに保存すると、あとからライブラリや続きから読むで戻れます。"),
        "fr": ("Comment utiliser les archives et la Bibliothèque ?", "Commencez sur Accueil, choisissez une branche, puis parcourez les routes d'archive : SCP, Tales, Canons, GoI, Joke SCP, SCP-EX, collections, articles récents et guides. Si vous savez quoi chercher, utilisez Recherche. Quand un article compte, ajoutez favori, à lire plus tard, note, mémo ou dossier pour le retrouver dans la Bibliothèque et la reprise de lecture."),
        "ru": ("Как использовать архив и Библиотеку?", "Начните с Главной, выберите филиал и просматривайте маршруты архива: SCP, Tales, Canons, GoI, Joke SCP, SCP-EX, коллекции, недавние статьи и руководства. Если цель известна, используйте Поиск. Когда материал важен, сохраните его как закладку, «прочитать позже», оценку, заметку или запись в папке, чтобы вернуться через Библиотеку и продолжение чтения."),
        "ko": ("아카이브와 라이브러리는 어떻게 나눠 쓰나요?", "먼저 홈에서 지부를 선택하고 SCP 글, Tales, Canons, GoI, Joke SCP, SCP-EX, 컬렉션, 최근 글, 가이드 같은 아카이브 경로에서 찾습니다. 찾을 대상이 분명하면 검색을 사용합니다. 중요한 글은 북마크, 나중에 읽기, 평점, 메모, 폴더로 저장하면 나중에 라이브러리와 이어 읽기에서 다시 돌아갈 수 있습니다."),
        "es": ("¿Cómo debo usar el archivo y la Biblioteca?", "Empieza en Inicio, elige una rama y recorre rutas de directorio como informes SCP, Tales, Canons, GoI, Joke SCP, SCP-EX, colecciones, artículos recientes y guías. Usa Búsqueda cuando conozcas un número, título, etiqueta o Clase de Objeto. Cuando encuentres algo útil, márcalo como favorito, ponlo en leer más tarde, valóralo, añade una nota o colócalo en una carpeta para que siga disponible desde la Biblioteca y continuar leyendo."),
    }
    faqs = list(faqs)
    faqs.insert(2, archive_faq[lang])
    return {
        "title": title,
        "description": support_descriptions[lang],
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


for code in ["ja", "fr", "ru", "ko", "es"]:
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
        "es": ("Política de clasificación y seguridad — SCP Docs", "Política de clasificación y seguridad de SCP Docs: idoneidad 13+ del App Store, temas de terror de ficción, orientación para lectores y responsabilidad de los sitios de origen.", "Política de clasificación y seguridad", "Última actualización: 24 de junio de 2026", [("1. Objeto de esta página", "Esta página ofrece información adicional sobre la idoneidad por edad y la seguridad del contenido de la aplicación móvil «SCP Docs» (la «App»). La App se considera apropiada para una clasificación 13+ del App Store."), ("2. Naturaleza de la app", "La App es un cliente no oficial de navegación y lectura para obras creativas públicas de la comunidad en línea conocida como SCP Foundation. No la proporcionan ni la respaldan la SCP Foundation, Wikidot, Inc. ni los operadores oficiales del contenido referenciado."), ("3. Contenido esperado", "Las obras relacionadas con SCP pueden incluir terror en formato de texto, suspenso, entidades anómalas, procedimientos de contención ficticios, prosa de advertencia, temas trágicos, violencia implícita, referencias a sangre, temas perturbadores e imágenes ocasionales proporcionadas por los sitios de origen. La mayor parte del contenido es ficción y no pretende fomentar conductas peligrosas en el mundo real."), ("4. Orientación para lectores", "La App está destinada a lectores de 13 años o más. Los lectores sensibles al terror o a la ficción inquietante, y los menores que usen la App, deben elegir sus lecturas con cuidado. Las etiquetas de los artículos, las advertencias, las reglas de los sitios de origen y la orientación parental pueden ser relevantes."), ("5. Controles y límites de la app", "SCP Docs ofrece ajustes de lectura y herramientas de navegación, pero no reescribe ni clasifica por edad cada artículo de origen. Los padres y tutores pueden usar Tiempo de uso de iOS, las restricciones de edad y los controles de contenido para gestionar el entorno de navegación de un menor."), ("6. Contacto", f'Las preguntas sobre la idoneidad por edad o esta página pueden enviarse a <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> o <a href="{X_URL}" target="_blank" rel="noopener noreferrer">X: @SCPdocs</a>.')]),
    }
    title, description, heading, updated, sections = data[lang]
    return {"title": title, "description": description, "heading": heading, "updated": updated, "sections": sections}


for code in ["ja", "fr", "ru", "ko", "es"]:
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
