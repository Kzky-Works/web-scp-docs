(() => {
  "use strict";

  const ROUTE_ID = /^[0-9a-f]{24}$/;
  const SOURCE = /^[A-Za-z0-9_-]+$/;
  const STORE_URL = "https://apps.apple.com/app/scp-docs/id6765882660";
  const FALLBACK_DELAY_MS = 900;

  const launcher = document.querySelector("#launcher");
  const openButton = document.querySelector("#open-app");
  const backLink = document.querySelector("#back-to-article");
  const error = document.querySelector("#error");

  function requestParameters() {
    const incoming = new URLSearchParams(window.location.search);
    const identifier = String(incoming.get("id") || "").toLowerCase();
    const source = incoming.get("source");
    if (!ROUTE_ID.test(identifier) || (source && (source.length > 2048 || !SOURCE.test(source)))) return null;

    const params = new URLSearchParams();
    params.set("id", identifier);
    if (source) params.set("source", source);
    return params;
  }

  function appURL(params) {
    return `scpdocs://open?${params.toString()}`;
  }

  function articleURL(params) {
    const target = new URL("../open/", window.location.href);
    target.search = params.toString();
    return target.href;
  }

  let fallbackTimer = null;

  function cancelFallback() {
    if (fallbackTimer !== null) {
      window.clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }
  }

  function tryOpenApp(params) {
    cancelFallback();
    try {
      window.location.replace(appURL(params));
    } catch (_) {
      // Some embedded browsers reject custom schemes synchronously. The
      // fallback still needs to remain available in that case.
    }
    fallbackTimer = window.setTimeout(() => {
      if (!document.hidden) window.location.replace(STORE_URL);
    }, FALLBACK_DELAY_MS);
  }

  function run() {
    const params = requestParameters();
    launcher.hidden = false;
    if (!params) {
      error.hidden = false;
      openButton.hidden = true;
      backLink.hidden = true;
      return;
    }

    backLink.href = articleURL(params);
    openButton.addEventListener("click", () => tryOpenApp(params));
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) cancelFallback();
    });
    window.addEventListener("pagehide", cancelFallback);

    // X blocks the first page's custom-scheme link in some contexts. A fresh
    // HTTPS landing page plus this navigation mirrors the proven OneLink flow.
    tryOpenApp(params);
  }

  run();
})();
