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
      replaceChildren() { this.childElementCount = 0; },
      append() { this.childElementCount += 1; }
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
