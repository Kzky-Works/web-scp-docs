(() => {
  "use strict";

  const ROUTE_ID = /^[0-9a-f]{24}$/;
  const LANGUAGE_MAP = {
    en: "EN", es: "ES", fr: "FR", ja: "JP", ko: "KO",
    pl: "PL", ru: "RU", zh: "CN", th: "TH", de: "DE"
  };
  const LANGUAGE_ORDER = ["EN", "ES", "FR", "JP", "KO", "PL", "RU", "CN", "TH", "DE"];
  const ALLOWED_HOSTS = new Set([
    "scp-wiki.wikidot.com", "scp-int.wikidot.com", "lafundacionscp.wikidot.com",
    "fondationscp.wikidot.com", "scp-jp.wikidot.com", "scpko.wikidot.com",
    "scp-pl.wikidot.com", "scpfoundation.net", "scp-ru.wikidot.com",
    "scp-wiki-cn.wikidot.com", "scp-th.wikidot.com", "scp-wiki-de.wikidot.com"
  ]);

  const status = document.querySelector("#status");
  const detail = document.querySelector("#detail");
  const appLink = document.querySelector("#open-app");
  const webLink = document.querySelector("#open-web");
  const languages = document.querySelector("#languages");
  const languageLinks = document.querySelector("#language-links");

  function decodeSource(value) {
    if (!value) return null;
    try {
      const base64 = value.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(value.length / 4) * 4, "=");
      return decodeURIComponent(Array.from(atob(base64), c => `%${c.charCodeAt(0).toString(16).padStart(2, "0")}`).join(""));
    } catch (_) {
      return null;
    }
  }

  function safeURL(raw) {
    try {
      const url = new URL(raw);
      if (!["http:", "https:"].includes(url.protocol) || !ALLOWED_HOSTS.has(url.hostname.toLowerCase())) return null;
      return url.href;
    } catch (_) {
      return null;
    }
  }

  async function routeIDForURL(raw) {
    const normalized = safeURL(raw);
    if (!normalized) return null;
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(normalized));
    return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("").slice(0, 24);
  }

  function preferredLanguage(versions) {
    const remembered = localStorage.getItem("scpdocs.preferredArticleLanguage");
    if (remembered && versions[remembered]) return remembered;
    for (const tag of navigator.languages || [navigator.language]) {
      const code = LANGUAGE_MAP[String(tag || "").toLowerCase().split("-")[0]];
      if (code && versions[code]) return code;
    }
    return null;
  }

  function renderLanguages(versions) {
    languageLinks.replaceChildren();
    for (const language of LANGUAGE_ORDER) {
      const target = safeURL(versions[language]);
      if (!target) continue;
      const link = document.createElement("a");
      link.href = target;
      link.textContent = language;
      link.hreflang = language.toLowerCase();
      link.addEventListener("click", () => localStorage.setItem("scpdocs.preferredArticleLanguage", language));
      languageLinks.append(link);
    }
    languages.hidden = languageLinks.childElementCount === 0;
  }

  function appURL(params) {
    const query = new URLSearchParams();
    query.set("id", params.get("id"));
    if (params.get("source")) query.set("source", params.get("source"));
    return `scpdocs://open?${query.toString()}`;
  }

  function isIOSBrowser() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent)
      || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  }

  function revealDestinations(destination, params) {
    appLink.href = appURL(params);
    appLink.hidden = false;
    webLink.href = destination;
    webLink.hidden = false;

    if (!isIOSBrowser()) {
      window.location.replace(destination);
    }
  }

  async function run() {
    const params = new URLSearchParams(window.location.search);
    const identifier = String(params.get("id") || "").toLowerCase();
    if (!ROUTE_ID.test(identifier)) throw new Error("The shared article link is invalid.");
    const decodedFallback = safeURL(decodeSource(params.get("source")));
    const fallback = decodedFallback && await routeIDForURL(decodedFallback) === identifier ? decodedFallback : null;

    let route = null;
    try {
      const shardURL = new URL(`../routes/${identifier.slice(0, 2)}.json`, window.location.href);
      const response = await fetch(shardURL, { cache: "no-cache" });
      if (response.ok) route = (await response.json()).routes?.[identifier] || null;
      if (route && await routeIDForURL(route.sourceURL) !== identifier) route = null;
    } catch (_) {
      route = null;
    }

    const versions = route?.versions || {};
    const selected = preferredLanguage(versions);
    const destination = safeURL(versions[selected])
      || safeURL(route?.original?.url)
      || safeURL(versions.EN)
      || fallback;
    if (!destination) throw new Error("No official article URL is available yet.");

    renderLanguages(versions);
    if (isIOSBrowser()) {
      status.textContent = "Open this SCP article";
      detail.textContent = "In X, tap Open in SCP docs below. If X blocks it, use the browser menu to open this page in Safari.";
    } else {
      status.textContent = "Opening the SCP article…";
      detail.textContent = selected ? `Selected ${selected} from your language preference.` : "Opening the available original version.";
    }
    revealDestinations(destination, params);
  }

  run().catch(error => {
    status.textContent = "Unable to open this link";
    detail.textContent = error.message;
  });
})();
