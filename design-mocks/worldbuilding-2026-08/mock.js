const concepts = {
  a: {
    title: "SCP Docs — SCP記事アーカイブ",
    brand: "SCP ARTICLE ARCHIVE",
    code: "SCP ARTICLES / JP",
    classification: "SCP記事リーダー",
    overline: "SCP記事を探す・読む",
    hero: "SCP記事を、<em>探しやすく、読みやすく。</em>",
    lede: "SCP、Tales、Canon、GoIを、各支部の一覧や検索から探せます。読んだ記事は、履歴やブックマークからあとで開けます。",
    strip: "このサイトだけでも、次に読む記事を探せます。",
    discover: "次に読む記事を選ぶ。",
    discoverLede: "アプリを持っていなくても使える記事検索。評価、長さ、タグのほか、「短く読める」「ホラー」「メタ」などから候補を探せます。",
    closing: "公式記事へのリンクと作者・ライセンスを保ったまま、<br />スマートフォンで読みやすくします。",
  },
  b: {
    title: "SCP Docs — SCP読書案内",
    brand: "SCP READING GUIDE",
    code: "SCP READING GUIDE / 017",
    classification: "READ / SEARCH / SAVE",
    overline: "SCP記事を探している人へ",
    hero: "面白いSCP、<em>次は何を読む？</em>",
    lede: "有名作の次も、短い一作も、知らない支部の記事も。読みたいタイプからSCP記事を探し、アプリで続けて読めます。",
    strip: "SCP、Tales、Canon、GoIから、次に読む記事を探せます。",
    discover: "読みたいタイプから、記事を選ぶ。",
    discoverLede: "高評価順だけでなく、ホラー、短編、しんみり、メタなど、読みたいタイプから候補を探します。",
    closing: "次に読む記事が、<br />すぐ見つかる。",
  },
  c: {
    title: "SCP Docs — 第17サイト閲覧端末",
    brand: "SCP DOCS / SEARCH SYSTEM",
    code: "17 BRANCHES / SEARCH READY",
    classification: "SEARCH AVAILABLE",
    overline: "17支部の記事検索",
    hero: "17支部の記事を、<em>ひとつの検索から。</em>",
    lede: "SCP、Tales、Canon、GoIを、番号、タイトル、タグ、Object Classなどから検索。読書状態とブックマークも同じアプリで管理できます。",
    strip: "検索機能はすべて無料。フォルダやハイライトはプレミアム。",
    discover: "条件に合う記事を探す。",
    discoverLede: "評価、長さ、文書種別、タグを組み合わせ、読みたい条件に合う記事を探せます。Webから公式記事を直接開けます。",
    closing: "記事を探す、読む、<br />あとからもう一度開く。",
  },
};

const requested = new URLSearchParams(location.search).get("concept");
const concept = concepts[requested] ? requested : "a";
const copy = concepts[concept];
document.body.dataset.concept = concept;
document.title = copy.title;

const setText = (selector, value, html = false) => {
  const node = document.querySelector(selector);
  if (!node) return;
  if (html) node.innerHTML = value;
  else node.textContent = value;
};

setText("[data-brand-sub]", copy.brand);
setText("[data-case-code]", copy.code);
setText("[data-classification]", copy.classification);
setText("[data-hero-overline]", copy.overline);
setText("[data-hero-title]", copy.hero, true);
setText("[data-hero-lede]", copy.lede);
setText("[data-strip-lead]", copy.strip);
setText("[data-discover-title]", copy.discover);
setText("[data-discover-lede]", copy.discoverLede);
setText("[data-closing-title]", copy.closing, true);
