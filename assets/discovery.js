(() => {
  "use strict";

  const results = document.querySelector("#discovery-results");
  const status = document.querySelector("#discovery-status");
  const shuffle = document.querySelector("#discovery-shuffle");
  const form = document.querySelector("#discovery-search");
  const query = document.querySelector("#discovery-query");
  const modeButtons = [...document.querySelectorAll("[data-discovery-mode]")];
  let catalog = [];
  let activeMode = "popular";
  let lastIDs = new Set();

  function shuffled(items) {
    const copy = [...items];
    for (let index = copy.length - 1; index > 0; index -= 1) {
      const swap = Math.floor(Math.random() * (index + 1));
      [copy[index], copy[swap]] = [copy[swap], copy[index]];
    }
    return copy;
  }

  function matchesQuery(article, rawQuery) {
    const needle = rawQuery.trim().toLocaleLowerCase("ja");
    if (!needle) return true;
    const haystack = [article.id, article.title, article.kind, ...article.tags]
      .join(" ")
      .toLocaleLowerCase("ja");
    return haystack.includes(needle);
  }

  function detail(article) {
    const parts = [article.kind, `${article.characters.toLocaleString("ja-JP")}文字`, `Wiki +${article.score}`];
    if (article.createdAt) {
      parts.push(new Date(article.createdAt * 1000).toLocaleDateString("ja-JP"));
    }
    return parts.join(" · ");
  }

  function articleCard(article) {
    const card = document.createElement("article");
    card.className = "discovery-result";

    const file = document.createElement("p");
    file.className = "discovery-file";
    file.textContent = article.id;

    const title = document.createElement("h3");
    const titleLink = document.createElement("a");
    titleLink.href = article.url;
    titleLink.target = "_blank";
    titleLink.rel = "noopener noreferrer";
    titleLink.textContent = article.title;
    title.append(titleLink);

    const meta = document.createElement("p");
    meta.className = "discovery-meta";
    meta.textContent = detail(article);

    const tags = document.createElement("div");
    tags.className = "discovery-tags";
    for (const tag of article.tags.slice(0, 5)) {
      const chip = document.createElement("span");
      chip.textContent = tag;
      tags.append(chip);
    }

    const actions = document.createElement("div");
    actions.className = "discovery-actions";
    const official = document.createElement("a");
    official.className = "pill";
    official.href = article.url;
    official.target = "_blank";
    official.rel = "noopener noreferrer";
    official.textContent = "公式Wikiで読む";
    const app = document.createElement("a");
    app.className = "pill";
    app.href = article.openUrl;
    app.textContent = "SCP Docsで開く";
    actions.append(official, app);

    card.append(file, title, meta, tags, actions);
    return card;
  }

  function render() {
    const rawQuery = query.value;
    let pool = rawQuery.trim()
      ? catalog.filter(article => matchesQuery(article, rawQuery))
      : catalog.filter(article => article.modes.includes(activeMode));
    const unseen = pool.filter(article => !lastIDs.has(article.id));
    if (unseen.length >= 3) pool = unseen;
    const chosen = shuffled(pool).slice(0, 3);
    lastIDs = new Set(chosen.map(article => article.id));
    results.replaceChildren(...chosen.map(articleCard));

    if (chosen.length === 0) {
      status.textContent = "この候補集では見つかりませんでした。別の言葉か気分を試すか、アプリの全文検索を利用してください。";
      return;
    }
    status.textContent = rawQuery.trim()
      ? `「${rawQuery.trim()}」の候補 ${pool.length}件から表示しています。`
      : `${pool.length}件の候補から3件を選びました。もう一度選ぶと入れ替わります。`;
  }

  function selectMode(button) {
    activeMode = button.dataset.discoveryMode;
    query.value = "";
    lastIDs.clear();
    for (const candidate of modeButtons) {
      candidate.setAttribute("aria-pressed", String(candidate === button));
    }
    render();
  }

  async function start() {
    try {
      const response = await fetch("assets/discovery-ja.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      catalog = Array.isArray(payload.articles) ? payload.articles : [];
      if (catalog.length === 0) throw new Error("empty catalog");
      shuffle.disabled = false;
      query.disabled = false;
      for (const button of modeButtons) button.disabled = false;
      render();
    } catch (_) {
      status.textContent = "候補集を読み込めませんでした。時間をおいて再読み込みしてください。";
    }
  }

  for (const button of modeButtons) {
    button.addEventListener("click", () => selectMode(button));
  }
  shuffle.addEventListener("click", render);
  form.addEventListener("submit", event => {
    event.preventDefault();
    lastIDs.clear();
    for (const button of modeButtons) button.setAttribute("aria-pressed", "false");
    render();
  });

  start();
})();
