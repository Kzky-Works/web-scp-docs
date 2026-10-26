const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "..", "assets", "analytics.js"), "utf8");
const analytics = vm.runInNewContext(`${source}\nSCPDocsAnalyticsCore;`, { URL });

test("uses the existing SCP Docs web measurement ID", () => {
  assert.equal(analytics.MEASUREMENT_ID, "G-5M5Q6SML03");
  assert.equal(analytics.isAnalyticsHost("scpdocs.link"), true);
  assert.equal(analytics.isAnalyticsHost("127.0.0.1"), false);
  assert.equal(analytics.isAnalyticsHost("kzky-works.github.io"), false);
});

test("removes search parameters and fragments from measured page URLs", () => {
  assert.equal(
    analytics.analyticsPageURL("https://scpdocs.link/discover-ja.html?q=scp-173&tag=horror#results"),
    "https://scpdocs.link/discover-ja.html",
  );
  assert.equal(
    analytics.analyticsPagePath("https://scpdocs.link/discover-ja.html?q=scp-173"),
    "/discover-ja.html",
  );
});

test("keeps ordinary SCP searches but drops likely personal contact data", () => {
  assert.equal(analytics.safeSearchTerm("  ＳＣＰ－１７３  "), "SCP-173");
  assert.equal(analytics.safeSearchTerm("reader@example.com"), "");
  assert.equal(analytics.safeSearchTerm("https://example.com/article"), "");
  assert.equal(analytics.safeSearchTerm("090-1234-5678"), "");
});

test("limits recorded search terms", () => {
  assert.equal(analytics.safeSearchTerm("a".repeat(120)).length, 80);
});

// All contact values are synthetic; nothing is transmitted by this VM fixture.
for (const [name, prefixLength, contact] of [
  ["email", 70, "reader@example.com"],
  ["URL", 77, "https://example.com/article"],
  ["telephone", 75, "090-1234-5678"],
  ["full-width email", 70, "ｒｅａｄｅｒ＠ｅｘａｍｐｌｅ．ｃｏｍ"],
]) {
  test(`drops ${name} when the 80-character boundary would split it`, () => {
    const input = "あ".repeat(prefixLength) + " " + contact;
    assert.equal(analytics.safeSearchTerm(input), "");
  });
}

test("drops contact data beyond the measured 80-code-unit prefix", () => {
  assert.equal(analytics.safeSearchTerm("あ".repeat(300) + " reader@example.com"), "");
});

test("omits normalized analytics inputs above 4096 code units", () => {
  assert.equal(analytics.safeSearchTerm("a".repeat(4097)), "");
  assert.equal(analytics.safeSearchTerm("a".repeat(4096)), "a".repeat(80));
});

function submitSyntheticSearch(query, { granted = true, formID = "catalog-search" } = {}) {
  const listeners = {};
  const scripts = [];
  const window = {
    location: { href: "https://scpdocs.link/discover-ja.html", pathname: "/discover-ja.html", hostname: "scpdocs.link" },
    localStorage: { getItem: () => granted ? "granted" : "denied" },
  };
  const document = {
    documentElement: { lang: "ja" },
    title: "Synthetic page",
    querySelector: () => null,
    addEventListener: (type, callback) => { listeners[type] = callback; },
    head: { append: script => scripts.push(script) },
    createElement: () => ({ listeners: {}, addEventListener(type, callback) { this.listeners[type] = callback; } }),
  };
  const form = { id: formID };
  vm.runInNewContext(source, {
    URL, window, document,
    FormData: class { get() { return query; } },
  });
  listeners.DOMContentLoaded();
  if (granted) {
    // Fake script completion only; no browser, sockets, or Google request exists.
    scripts[0].listeners.load();
  }
  listeners.submit({ target: { closest: () => form } });
  const events = (window.dataLayer || []).filter(args => args[0] === "event" && args[1] === "search");
  return { events, scripts };
}

test("production submit handler omits a split email from both search forms", () => {
  for (const formID of ["catalog-search", "home-search"]) {
    const { events } = submitSyntheticSearch("あ".repeat(70) + " reader@example.com", { formID });
    assert.equal(events.length, 1);
    assert.equal(Object.hasOwn(events[0][2], "search_term"), false);
    assert.equal(events[0][2].search_has_term, false);
    assert.equal(events[0][2].search_source, formID === "catalog-search" ? "catalog" : "home");
  }
});

test("production submit handler retains bounded ordinary search terms", () => {
  const { events } = submitSyntheticSearch("a".repeat(120));
  assert.equal(events.length, 1);
  assert.equal(events[0][2].search_term, "a".repeat(80));
  assert.equal(events[0][2].search_has_term, true);
});

test("production submit handler records nothing after denied consent initializes", () => {
  const { events, scripts } = submitSyntheticSearch("scp-173", { granted: false });
  assert.equal(events.length, 0);
  assert.equal(scripts.length, 0);
});
