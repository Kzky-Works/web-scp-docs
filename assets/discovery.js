const SCPDocsSearch = (() => {
  "use strict";

  const PAGE_SIZE = 24;

  function normalize(value) {
    return String(value || "")
      .normalize("NFKC")
      .toLocaleLowerCase("ja")
      .replace(/[‐‑–—−]/g, "-")
      .replace(/\s+/g, " ")
      .trim();
  }

  function searchableText(article) {
    return normalize([
      article.id,
      article.title,
      article.kind,
      article.objectClass,
      ...(article.tags || []),
    ].join(" "));
  }

  function parseState(params) {
    const positiveInteger = value => {
      const parsed = Number.parseInt(value, 10);
      return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
    };
    return {
      query: String(params.get("q") || ""),
      kind: String(params.get("kind") || ""),
      objectClass: String(params.get("class") || ""),
      length: String(params.get("length") || ""),
      minimumScore: Number.parseInt(params.get("score") || "", 10) || 0,
      sort: String(params.get("sort") || "relevance"),
      mode: String(params.get("mode") || ""),
      page: positiveInteger(params.get("page")),
    };
  }

  function stateParameters(state) {
    const params = new URLSearchParams();
    if (state.query.trim()) params.set("q", state.query.trim());
    if (state.kind) params.set("kind", state.kind);
    if (state.objectClass) params.set("class", state.objectClass);
    if (state.length) params.set("length", state.length);
    if (state.minimumScore) params.set("score", String(state.minimumScore));
    if (state.sort !== "relevance") params.set("sort", state.sort);
    if (state.mode) params.set("mode", state.mode);
    if (state.page > 1) params.set("page", String(state.page));
    return params;
  }

  function matchesLength(article, length) {
    const characters = Number(article.characters || 0);
    if (!length) return true;
    if (length === "short") return characters > 0 && characters < 5_000;
    if (length === "medium") return characters >= 5_000 && characters < 15_000;
    if (length === "long") return characters >= 15_000;
    return true;
  }

  function articleAppURL(article, baseURL) {
    const route = new URL(article.openUrl, baseURL);
    return `scpdocs://open?${route.searchParams.toString()}`;
  }

  function openArticleInApp(article, pageLocation) {
    pageLocation.href = articleAppURL(article, pageLocation.href);
  }

  function relevance(article, needle) {
    if (!needle) return Number(article.score || 0);
    const id = normalize(article.id);
    const title = normalize(article.title);
    const tags = (article.tags || []).map(normalize);
    let score = 0;
    if (id === needle) score += 2_000;
    else if (id.startsWith(needle)) score += 900;
    else if (id.includes(needle)) score += 500;
    if (title === needle) score += 1_600;
    else if (title.startsWith(needle)) score += 750;
    else if (title.includes(needle)) score += 450;
    if (tags.includes(needle)) score += 350;
    score += Math.min(Number(article.score || 0), 500) / 10;
    return score;
  }

  function filterArticles(articles, state) {
    const needle = normalize(state.query);
    const tokens = needle.split(" ").filter(Boolean);
    const filtered = articles.filter(article => {
      const haystack = article.searchableText || searchableText(article);
      if (tokens.some(token => !haystack.includes(token))) return false;
      if (state.kind && article.kind !== state.kind) return false;
      if (state.objectClass && article.objectClass !== state.objectClass) return false;
      if (!matchesLength(article, state.length)) return false;
      if (state.minimumScore && Number(article.score || 0) < state.minimumScore) return false;
      if (state.mode && !(article.modes || []).includes(state.mode)) return false;
      return true;
    });

    const compareID = (left, right) => String(left.id).localeCompare(String(right.id), "ja", { numeric: true });
    filtered.sort((left, right) => {
      if (state.sort === "score") return Number(right.score || 0) - Number(left.score || 0) || compareID(left, right);
      if (state.sort === "shortest") return Number(left.characters || 0) - Number(right.characters || 0) || compareID(left, right);
      if (state.sort === "longest") return Number(right.characters || 0) - Number(left.characters || 0) || compareID(left, right);
      if (state.sort === "newest") return Number(right.createdAt || 0) - Number(left.createdAt || 0) || compareID(left, right);
      return relevance(right, needle) - relevance(left, needle) || compareID(left, right);
    });
    return filtered;
  }

  return {
    PAGE_SIZE,
    articleAppURL,
    filterArticles,
    normalize,
    openArticleInApp,
    parseState,
    searchableText,
    stateParameters,
  };
})();

if (typeof document !== "undefined") {
  (() => {
    "use strict";

    const form = document.querySelector("#catalog-search");
    if (!form) return;

    const query = document.querySelector("#catalog-query");
    const kind = document.querySelector("#filter-kind");
    const objectClass = document.querySelector("#filter-object-class");
    const length = document.querySelector("#filter-length");
    const minimumScore = document.querySelector("#filter-score");
    const sort = document.querySelector("#filter-sort");
    const reset = document.querySelector("#search-reset");
    const status = document.querySelector("#search-status");
    const results = document.querySelector("#search-results");
    const pagination = document.querySelector("#search-pagination");
    const presetButtons = [...document.querySelectorAll("[data-search-preset]")];
    let catalog = [];
    let state = SCPDocsSearch.parseState(new URLSearchParams(window.location.search));

    function isAppleMobile() {
      return /iPad|iPhone|iPod/.test(navigator.userAgent)
        || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    }

    function appURL(article) {
      return SCPDocsSearch.articleAppURL(article, window.location.href);
    }

    function openInstalledApp(event, article) {
      if (!isAppleMobile()) return;
      event.preventDefault();
      SCPDocsSearch.openArticleInApp(article, window.location);
    }

    function formatScore(value) {
      const score = Number(value || 0);
      return `Wiki ${score > 0 ? "+" : ""}${score}`;
    }

    function detail(article) {
      const parts = [article.kind];
      if (article.objectClass) parts.push(article.objectClass);
      if (article.characters) parts.push(`${Number(article.characters).toLocaleString("ja-JP")}文字`);
      parts.push(formatScore(article.score));
      return parts.join(" · ");
    }

    function applyTag(tag) {
      state.query = tag;
      state.mode = "";
      state.page = 1;
      query.value = tag;
      render(true);
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function articleCard(article) {
      const card = document.createElement("article");
      card.className = "search-result-card";

      const heading = document.createElement("div");
      heading.className = "search-result-heading";
      const file = document.createElement("p");
      file.className = "discovery-file";
      file.textContent = article.id;
      const meta = document.createElement("p");
      meta.className = "discovery-meta";
      meta.textContent = detail(article);
      heading.append(file, meta);

      const title = document.createElement("h3");
      const titleLink = document.createElement("a");
      titleLink.href = isAppleMobile() ? appURL(article) : article.url;
      if (!isAppleMobile()) {
        titleLink.target = "_blank";
        titleLink.rel = "noopener noreferrer";
      }
      titleLink.textContent = article.title;
      titleLink.addEventListener("click", event => openInstalledApp(event, article));
      title.append(titleLink);

      const tags = document.createElement("div");
      tags.className = "discovery-tags";
      for (const tag of (article.tags || []).slice(0, 6)) {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.textContent = tag;
        chip.addEventListener("click", () => applyTag(tag));
        tags.append(chip);
      }

      const actions = document.createElement("div");
      actions.className = "discovery-actions";
      if (isAppleMobile()) {
        const app = document.createElement("a");
        app.className = "pill pill-primary";
        app.href = appURL(article);
        app.textContent = "SCP Docsで開く";
        app.addEventListener("click", event => openInstalledApp(event, article));
        actions.append(app);
      }
      const official = document.createElement("a");
      official.className = "pill";
      official.href = article.url;
      official.target = "_blank";
      official.rel = "noopener noreferrer";
      official.textContent = "公式Wikiで読む ↗";
      actions.append(official);

      card.append(heading, title, tags, actions);
      return card;
    }

    function pageButton(label, page, disabled = false, current = false) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.disabled = disabled;
      if (current) button.setAttribute("aria-current", "page");
      button.addEventListener("click", () => {
        state.page = page;
        render(true);
        status.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      return button;
    }

    function renderPagination(totalPages) {
      if (totalPages <= 1) {
        pagination.replaceChildren();
        return;
      }
      const items = [pageButton("前へ", Math.max(1, state.page - 1), state.page === 1)];
      const start = Math.max(1, Math.min(state.page - 2, totalPages - 4));
      const end = Math.min(totalPages, start + 4);
      for (let page = start; page <= end; page += 1) {
        items.push(pageButton(String(page), page, false, page === state.page));
      }
      items.push(pageButton("次へ", Math.min(totalPages, state.page + 1), state.page === totalPages));
      pagination.replaceChildren(...items);
    }

    function syncControls() {
      query.value = state.query;
      kind.value = state.kind;
      objectClass.value = state.objectClass;
      length.value = state.length;
      minimumScore.value = String(state.minimumScore || "");
      sort.value = state.sort;
      for (const button of presetButtons) {
        button.setAttribute("aria-pressed", String(button.dataset.searchPreset === state.mode));
      }
    }

    function updateURL(push) {
      const params = SCPDocsSearch.stateParameters(state);
      const target = `${window.location.pathname}${params.size ? `?${params}` : ""}`;
      window.history[push ? "pushState" : "replaceState"]({}, "", target);
    }

    function render(push = false) {
      syncControls();
      const matched = SCPDocsSearch.filterArticles(catalog, state);
      const totalPages = Math.max(1, Math.ceil(matched.length / SCPDocsSearch.PAGE_SIZE));
      state.page = Math.min(state.page, totalPages);
      const start = (state.page - 1) * SCPDocsSearch.PAGE_SIZE;
      const visible = matched.slice(start, start + SCPDocsSearch.PAGE_SIZE);
      results.replaceChildren(...visible.map(articleCard));
      renderPagination(totalPages);
      updateURL(push);

      if (matched.length === 0) {
        status.textContent = "条件に合う記事が見つかりませんでした。検索語や条件を減らしてみてください。";
        return;
      }
      const first = start + 1;
      const last = start + visible.length;
      status.textContent = `${matched.length.toLocaleString("ja-JP")}件中 ${first.toLocaleString("ja-JP")}〜${last.toLocaleString("ja-JP")}件を表示`;
    }

    function readControls() {
      state = {
        query: query.value,
        kind: kind.value,
        objectClass: objectClass.value,
        length: length.value,
        minimumScore: Number.parseInt(minimumScore.value || "0", 10) || 0,
        sort: sort.value,
        mode: state.mode,
        page: 1,
      };
    }

    async function start() {
      try {
        const response = await fetch("assets/discovery-ja.json", { cache: "no-cache" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const payload = await response.json();
        catalog = (Array.isArray(payload.articles) ? payload.articles : []).map(article => ({
          ...article,
          searchableText: SCPDocsSearch.searchableText(article),
        }));
        if (catalog.length === 0) throw new Error("empty catalog");
        form.querySelectorAll("input, select, button").forEach(control => { control.disabled = false; });
        presetButtons.forEach(button => { button.disabled = false; });
        render();
      } catch (_) {
        status.textContent = "記事カタログを読み込めませんでした。時間をおいて再読み込みしてください。";
      }
    }

    form.addEventListener("submit", event => {
      event.preventDefault();
      readControls();
      render(true);
    });
    for (const control of [kind, objectClass, length, minimumScore, sort]) {
      control.addEventListener("change", () => {
        readControls();
        render(true);
      });
    }
    for (const button of presetButtons) {
      button.addEventListener("click", () => {
        state.mode = state.mode === button.dataset.searchPreset ? "" : button.dataset.searchPreset;
        state.page = 1;
        render(true);
      });
    }
    reset.addEventListener("click", () => {
      state = SCPDocsSearch.parseState(new URLSearchParams());
      render(true);
    });
    window.addEventListener("popstate", () => {
      state = SCPDocsSearch.parseState(new URLSearchParams(window.location.search));
      render();
    });

    start();
  })();
}
