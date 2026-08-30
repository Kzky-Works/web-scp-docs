const SCPDocsReadingLists = (() => {
  "use strict";

  function articleAppURL(article, baseURL) {
    const route = new URL(article.openUrl, baseURL);
    return `scpdocs://open?${route.searchParams.toString()}`;
  }

  function openArticleInApp(article, pageLocation) {
    pageLocation.href = articleAppURL(article, pageLocation.href);
  }

  return { articleAppURL, openArticleInApp };
})();

if (typeof document !== "undefined") {
  (() => {
    "use strict";

    const themeList = document.querySelector("#reading-theme-list");
    if (!themeList) return;

    const panel = document.querySelector("#reading-list-panel");
    const status = document.querySelector("#reading-list-status");
    const references = document.querySelector("#reading-list-references");
    const total = document.querySelector("#reading-list-total");

    function isAppleMobile() {
      return /iPad|iPhone|iPod/.test(navigator.userAgent)
        || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    }

    function configureArticleLink(link, article) {
      link.href = isAppleMobile()
        ? SCPDocsReadingLists.articleAppURL(article, window.location.href)
        : article.url;
      if (!isAppleMobile()) {
        link.target = "_blank";
        link.rel = "noopener noreferrer";
      }
      link.addEventListener("click", event => {
        if (!isAppleMobile()) return;
        event.preventDefault();
        SCPDocsReadingLists.openArticleInApp(article, window.location);
      });
    }

    function detail(article) {
      const score = Number(article.score || 0);
      const parts = [article.kind];
      if (article.objectClass) parts.push(article.objectClass);
      if (article.characters) parts.push(`${Number(article.characters).toLocaleString("ja-JP")}文字`);
      parts.push(`Wiki ${score > 0 ? "+" : ""}${score}`);
      return parts.join(" · ");
    }

    function articleRow(article, index) {
      const item = document.createElement("li");
      item.className = "reading-list-article";

      const number = document.createElement("span");
      number.className = "reading-list-number";
      number.textContent = String(index + 1).padStart(2, "0");

      const content = document.createElement("div");
      const file = document.createElement("p");
      file.className = "reading-list-file";
      file.textContent = article.id;
      const heading = document.createElement("h4");
      const link = document.createElement("a");
      link.textContent = article.title;
      configureArticleLink(link, article);
      heading.append(link);
      const meta = document.createElement("p");
      meta.className = "reading-list-meta";
      meta.textContent = detail(article);
      content.append(file, heading, meta);

      item.append(number, content);
      return item;
    }

    function renderTheme(theme, articlesByID) {
      const resolved = theme.articleIds.map(id => articlesByID.get(id)).filter(Boolean);
      const header = document.createElement("div");
      header.className = "reading-list-header";
      const copy = document.createElement("div");
      const label = document.createElement("p");
      label.className = "section-label";
      label.textContent = theme.label;
      const heading = document.createElement("h3");
      heading.textContent = theme.title;
      const description = document.createElement("p");
      description.textContent = theme.description;
      copy.append(label, heading, description);
      const count = document.createElement("p");
      count.className = "reading-list-count";
      count.textContent = `${resolved.length.toLocaleString("ja-JP")}記事`;
      header.append(copy, count);

      const list = document.createElement("ol");
      list.className = "reading-list-articles";
      list.replaceChildren(...resolved.map(articleRow));
      panel.replaceChildren(header, list);

      for (const button of themeList.querySelectorAll("button[data-reading-theme]")) {
        button.setAttribute("aria-pressed", String(button.dataset.readingTheme === theme.id));
      }
    }

    function render(payload, catalog) {
      const themes = Array.isArray(payload.themes) ? payload.themes : [];
      if (themes.length === 0 || catalog.length === 0) throw new Error("empty reading data");
      const articlesByID = new Map(catalog.map(article => [article.id, article]));
      const buttons = themes.map(theme => {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.readingTheme = theme.id;
        button.setAttribute("aria-pressed", "false");
        const label = document.createElement("strong");
        label.textContent = theme.label;
        const count = document.createElement("span");
        count.textContent = `${theme.articleIds.length.toLocaleString("ja-JP")}記事`;
        button.append(label, count);
        button.addEventListener("click", () => renderTheme(theme, articlesByID));
        return button;
      });
      themeList.replaceChildren(...buttons);
      if (total) total.textContent = themes.length.toLocaleString("ja-JP");

      const sourceLinks = (Array.isArray(payload.references) ? payload.references : []).map(reference => {
        const link = document.createElement("a");
        link.href = reference.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = `${reference.label} ↗`;
        return link;
      });
      references.replaceChildren(...sourceLinks);
      renderTheme(themes[0], articlesByID);
    }

    async function start() {
      try {
        const [catalogResponse, recommendationsResponse] = await Promise.all([
          fetch("assets/discovery-ja.json", { cache: "no-cache" }),
          fetch("assets/recommendations-ja.json", { cache: "no-cache" }),
        ]);
        if (!catalogResponse.ok || !recommendationsResponse.ok) throw new Error("reading data unavailable");
        const catalogPayload = await catalogResponse.json();
        const recommendations = await recommendationsResponse.json();
        render(recommendations, Array.isArray(catalogPayload.articles) ? catalogPayload.articles : []);
      } catch (_) {
        status.textContent = "テーマ別の記事を読み込めませんでした。時間をおいて再読み込みしてください。";
      }
    }

    start();
  })();
}
