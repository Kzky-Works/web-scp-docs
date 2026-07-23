(() => {
  "use strict";

  const ROUTE_ID = /^[0-9a-f]{24}$/;
  const SOURCE = /^[A-Za-z0-9_-]+$/;

  const launcher = document.querySelector("#launcher");
  const appLink = document.querySelector("#open-app");
  const storeLink = document.querySelector("#open-store");
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

  function run() {
    const params = requestParameters();
    launcher.hidden = false;
    if (!params) {
      error.hidden = false;
      appLink.hidden = true;
      storeLink.hidden = true;
      backLink.hidden = true;
      return;
    }

    appLink.href = appURL(params);
    backLink.href = articleURL(params);
  }

  run();
})();
