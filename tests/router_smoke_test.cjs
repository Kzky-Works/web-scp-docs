const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const routerSource = fs.readFileSync(path.join(__dirname, "..", "open", "router.js"), "utf8");

function encodedSource(value) {
  return Buffer.from(value, "utf8").toString("base64url");
}

async function runRouter({ search, languages = ["en-US"], route = null, ios = false, safari = false }) {
  const elements = new Map();
  for (const id of ["status", "detail", "open-app", "open-web", "open-store", "languages", "language-links"]) {
    elements.set(`#${id}`, {
      hidden: true,
      childElementCount: 0,
      listeners: {},
      addEventListener(name, callback) { this.listeners[name] = callback; },
      children: [],
      replaceChildren() { this.childElementCount = 0; this.children = []; },
      append(child) { this.childElementCount += 1; this.children.push(child); }
    });
  }

  const location = {
    href: `https://scpdocs.link/open/${search}`,
    search,
    replaced: null,
    replace(value) { this.replaced = value; }
  };
  const identifier = new URLSearchParams(search).get("id");
  const sandbox = {
    Array,
    crypto,
    Error,
    Set,
    TextEncoder,
    Uint8Array,
    URL,
    URLSearchParams,
    atob,
    decodeURIComponent,
    document: {
      hidden: false,
      querySelector(selector) { return elements.get(selector); },
      createElement() { return { addEventListener() {} }; },
      addEventListener() {}
    },
    fetch: async () => ({
      ok: true,
      json: async () => ({ routes: route ? { [identifier]: route } : {} })
    }),
    localStorage: {
      getItem() { return null; },
      setItem() {}
    },
    navigator: {
      language: languages[0],
      languages,
      maxTouchPoints: ios ? 5 : 0,
      platform: ios ? "iPhone" : "MacIntel",
      userAgent: ios
        ? (safari
          ? "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 Version/26.0 Mobile/15E148 Safari/604.1"
          : "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148")
        : "Desktop test"
    },
    window: {
      clearTimeout,
      location,
      setTimeout
    }
  };

  vm.runInNewContext(routerSource, sandbox, { filename: "router.js" });
  for (let index = 0; index < 100; index += 1) {
    if (location.replaced || !elements.get("#open-web").hidden || elements.get("#status").textContent === "Unable to open this link") break;
    await new Promise(resolve => setTimeout(resolve, 5));
  }
  return { elements, location };
}

test("selects an available article matching the browser language", async () => {
  const id = "a3ecd8849da128f3d092c004";
  const result = await runRouter({
    search: `?id=${id}`,
    languages: ["ja-JP", "en-US"],
    route: {
      sourceURL: "https://scp-wiki.wikidot.com/scp-173",
      original: { language: "EN", url: "https://scp-wiki.wikidot.com/scp-173" },
      versions: {
        EN: "https://scp-wiki.wikidot.com/scp-173",
        JP: "https://scp-jp.wikidot.com/scp-173"
      }
    }
  });

  assert.equal(result.location.replaced, "https://scp-jp.wikidot.com/scp-173");
  assert.equal(result.elements.get("#detail").textContent, "Selected JP from your language preference.");
});

test("uses the signed official source fallback while route shards lag", async () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = encodedSource("https://scp-wiki.wikidot.com/scp-173");
  const result = await runRouter({ search: `?id=${id}&source=${source}` });

  assert.equal(result.location.replaced, "https://scp-wiki.wikidot.com/scp-173");
});

test("offers a direct article deep link in iOS in-app browsers", async () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = encodedSource("https://scp-wiki.wikidot.com/scp-173");
  const result = await runRouter({
    search: `?id=${id}&source=${source}`,
    languages: ["ja-JP", "en-US"],
    ios: true,
    route: {
      sourceURL: "https://scp-wiki.wikidot.com/scp-173",
      original: { language: "EN", url: "https://scp-wiki.wikidot.com/scp-173" },
      versions: {
        EN: "https://scp-wiki.wikidot.com/scp-173",
        JP: "https://scp-jp.wikidot.com/scp-173"
      }
    }
  });

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#status").textContent, "Open this article in SCP docs");
  assert.equal(result.elements.get("#open-app").hidden, false);
  assert.equal(result.elements.get("#open-app").href, `scpdocs://open?id=${id}&source=${source}`);
  assert.equal(result.elements.get("#open-store").hidden, false);
  assert.equal(result.elements.get("#open-web").href, "https://scp-jp.wikidot.com/scp-173");

  let prevented = false;
  result.elements.get("#open-app").listeners.click({
    preventDefault() { prevented = true; }
  });
  assert.equal(prevented, true);
  assert.equal(result.location.replaced, `scpdocs://open?id=${id}&source=${source}`);
});

test("offers the article deep link after the page is opened in Safari", async () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = encodedSource("https://scp-wiki.wikidot.com/scp-173");
  const result = await runRouter({
    search: `?id=${id}&source=${source}`,
    ios: true,
    safari: true
  });

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#status").textContent, "Open this article in SCP docs");
  assert.equal(result.elements.get("#open-app").hidden, false);
  assert.equal(result.elements.get("#open-app").href, `scpdocs://open?id=${id}&source=${source}`);
  assert.equal(result.elements.get("#open-store").hidden, false);
});

test("does not pass an unverified source fallback to the app", async () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = encodedSource("https://scp-wiki.wikidot.com/scp-096");
  const result = await runRouter({
    search: `?id=${id}&source=${source}`,
    ios: true,
    safari: true,
    route: {
      sourceURL: "https://scp-wiki.wikidot.com/scp-173",
      original: { language: "EN", url: "https://scp-wiki.wikidot.com/scp-173" },
      versions: { EN: "https://scp-wiki.wikidot.com/scp-173" }
    }
  });

  assert.equal(result.elements.get("#open-app").href, `scpdocs://open?id=${id}`);
});

test("does not redirect malformed links", async () => {
  const result = await runRouter({ search: "?id=not-a-route" });

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#status").textContent, "Unable to open this link");
});

test("rejects an official fallback that does not match the route id", async () => {
  const source = encodedSource("https://scp-wiki.wikidot.com/scp-096");
  const result = await runRouter({ search: `?id=a3ecd8849da128f3d092c004&source=${source}` });

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#status").textContent, "Unable to open this link");
});

const additionalVersions = {
  EN: "https://scp-wiki.wikidot.com/scp-173",
  JP: "https://scp-jp.wikidot.com/scp-173",
  IT: "https://fondazionescp.wikidot.com/scp-173",
  PT: "https://scp-pt-br.wikidot.com/scp-173",
  VN: "https://scp-vn.wikidot.com/scp-173",
  CS: "https://scp-cs.wikidot.com/scp-173",
  CN: "https://scp-wiki-cn.wikidot.com/scp-173",
  "ZH-TR": "https://scp-zh-tr.wikidot.com/scp-173",
  TR: "https://scpvakfi.wikidot.com/scp-173",
  ID: "https://scp-id.wikidot.com/scp-173"
};
test("keeps all supplied official versions and selects each added locale without crossing Chinese identities", async () => {
  for (const [locale, code] of [["en-US", "EN"], ["ja-JP", "JP"], ["it-IT", "IT"],
    ["pt-BR", "PT"], ["vi-VN", "VN"], ["cs-CZ", "CS"], ["zh-CN", "CN"],
    ["zh-Hant", "ZH-TR"], ["zh-TW", "ZH-TR"], ["tr-TR", "TR"], ["id-ID", "ID"]]) {
    const result = await runRouter({search: "?id=a3ecd8849da128f3d092c004", languages: [locale],
      route: {sourceURL: additionalVersions.EN, original: {language: "EN", url: additionalVersions.EN},
        versions: additionalVersions}});
    assert.equal(result.elements.get("#open-web").href, additionalVersions[code], locale);
    const links = result.elements.get("#language-links").children;
    assert.equal(links.length, Object.keys(additionalVersions).length);
    assert.equal(links.find(link => link.textContent === "PT/BR").href, additionalVersions.PT);
    assert.equal(links.find(link => link.textContent === "CN").href, additionalVersions.CN);
    assert.equal(links.find(link => link.textContent === "ZH-TR").href, additionalVersions["ZH-TR"]);
  }
});
test("retains compatibility with legacy PT/BR route keys", async () => {
  const result = await runRouter({search: "?id=a3ecd8849da128f3d092c004", languages: ["pt-BR"],
    route: {sourceURL: additionalVersions.EN, versions: {"PT/BR": additionalVersions.PT}}});
  assert.equal(result.elements.get("#open-web").href, additionalVersions.PT);
});
test("renders the five supplied SCP-020-IT versions and selects the Italian original", async () => {
  const sourceURL = "https://scp-int.wikidot.com/scp-020-it";
  const originalURL = "https://fondazionescp.wikidot.com/scp-020-it";
  const versions = {EN: sourceURL, IT: originalURL,
    ES: "https://lafundacionscp.wikidot.com/scp-020-it",
    FR: "https://fondationscp.wikidot.com/scp-020-it",
    CN: "https://scp-wiki-cn.wikidot.com/scp-020-it"};
  const result = await runRouter({search: "?id=036e1e5b862dad3c8600d9f4", languages: ["it-IT"],
    route: {sourceURL, original: {language: "IT", url: originalURL}, versions}});
  assert.equal(result.elements.get("#open-web").href, originalURL);
  const links = result.elements.get("#language-links").children;
  assert.equal(links.length, 5);
  assert.equal(links.find(link => link.textContent === "IT").href, originalURL);
});
