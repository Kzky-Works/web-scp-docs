const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "..", "assets", "discovery.js"), "utf8");
const search = vm.runInNewContext(`${source}\nSCPDocsSearch;`, { URL, URLSearchParams });

const articles = [
  {
    id: "scp-178",
    title: "3-D Specs",
    kind: "翻訳SCP",
    objectClass: "euclid",
    score: 120,
    characters: 4_200,
    tags: ["眼鏡", "視覚"],
    modes: ["popular", "short"],
  },
  {
    id: "scp-178-jp",
    title: "ことばのない記事",
    kind: "SCP-JP",
    objectClass: "keter",
    score: 45,
    characters: 18_000,
    tags: ["反ミーム"],
    modes: ["long", "strange"],
  },
];

function state(overrides = {}) {
  return {
    query: "",
    kind: "",
    objectClass: "",
    length: "",
    minimumScore: 0,
    sort: "relevance",
    mode: "",
    page: 1,
    ...overrides,
  };
}

test("normalizes full-width input and typographic hyphens", () => {
  assert.equal(search.normalize(" ＳＣＰ－１７８ "), "scp-178");
});

test("bare number matches nearby article IDs while qualified ID is specific", () => {
  assert.deepEqual(search.filterArticles(articles, state({ query: "178" })).map(article => article.id), [
    "scp-178",
    "scp-178-jp",
  ]);
  assert.deepEqual(search.filterArticles(articles, state({ query: "scp-178-jp" })).map(article => article.id), [
    "scp-178-jp",
  ]);
});

test("combines kind, object class, length, score, and preset filters", () => {
  const filtered = search.filterArticles(articles, state({
    kind: "翻訳SCP",
    objectClass: "euclid",
    length: "short",
    minimumScore: 100,
    mode: "popular",
  }));
  assert.deepEqual(filtered.map(article => article.id), ["scp-178"]);
});

test("search state round-trips through URL parameters", () => {
  const original = state({ query: "反ミーム", kind: "SCP-JP", objectClass: "keter", page: 2 });
  const restored = search.parseState(search.stateParameters(original));
  assert.equal(JSON.stringify(restored), JSON.stringify(original));
});

test("builds the installed-app URL from the signed article route", () => {
  const article = { openUrl: "open/?id=a3ecd8849da128f3d092c004&source=c2Nw" };
  assert.equal(
    search.articleAppURL(article, "https://scpdocs.link/discover-ja.html"),
    "scpdocs://open?id=a3ecd8849da128f3d092c004&source=c2Nw",
  );
});
