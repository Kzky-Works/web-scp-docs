const concepts = {
  a: {
    title: "SCP Docs — 公開記録閲覧室",
    brand: "PUBLIC ARCHIVE",
    code: "PUBLIC ACCESS / JP",
    classification: "公開閲覧用",
    overline: "財団記録・公開閲覧窓口",
    hero: "公開された異常記録を、<em>読みやすい書庫へ。</em>",
    lede: "SCP、Tales、Canon、GoI。散らばった記録を探し、読み、あとから同じ場所へ戻るための非公式アーカイブリーダー。",
    strip: "このサイトだけでも、次に読む記事が見つかる。",
    discover: "今夜読む記録を、ここで選ぶ。",
    discoverLede: "アプリを持っていなくても使える記事発見ページ。評価、長さ、タグ、読了状態ではなく「どんな読後感がほしいか」から入れます。",
    closing: "公式サイトを置き換えない。<br />そこへ戻る道を、読みやすくする。",
  },
  b: {
    title: "SCP Docs — 異常世界案内所",
    brand: "ANOMALY FIELD GUIDE",
    code: "FIELD GUIDE / ISSUE 017",
    classification: "READ / WANDER / RETURN",
    overline: "普通のSCPファンのための読書案内",
    hero: "面白いSCP、<em>次は何を読む？</em>",
    lede: "有名作の次も、短い一作も、知らない支部の傑作も。異常な世界を歩くための記事ガイドと、読書を続けるためのiOSアプリ。",
    strip: "怖さだけじゃない。物語、世界観、ユーモアまで歩き回る。",
    discover: "気分から選ぶ、異常世界の入口。",
    discoverLede: "ランキングだけに寄らず、怖い、切ない、奇妙、短く読めるなど、読者の気分を入口に次の一作へ案内します。",
    closing: "異常な世界は広い。<br />迷う時間まで、読書に変える。",
  },
  c: {
    title: "SCP Docs — 第17サイト閲覧端末",
    brand: "SITE-17 READING SYSTEM",
    code: "NODE 17 / ARCHIVE ONLINE",
    classification: "SYSTEM NORMAL",
    overline: "財団記録・読書支援システム",
    hero: "17支部の記録へ、<em>最短でアクセス。</em>",
    lede: "索引、検索、読書状態、個人書庫をひとつの操作系へ。SCPの膨大な公開記録を、精密に探して読み進めるネイティブ環境。",
    strip: "検索は全機能無料。個人書庫はプレミアムで拡張。",
    discover: "本日の推奨記録を照合する。",
    discoverLede: "高評価、長さ、文書種別、タグを横断し、今の条件に合う候補を即座に提示します。Webから公式記事へ直接アクセスできます。",
    closing: "公開記録へのアクセスを、<br />速く、正確に、途切れなく。",
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
