const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const launcherSource = fs.readFileSync(path.join(__dirname, "..", "launch", "launcher.js"), "utf8");

function runLauncher(search) {
  const elements = new Map();
  for (const id of ["launcher", "open-app", "open-store", "back-to-article", "error"]) {
    elements.set(`#${id}`, {
      hidden: id === "launcher" || id === "error"
    });
  }

  const location = {
    href: `https://scpdocs.link/launch/${search}`,
    search,
    replaced: null,
    replace(value) { this.replaced = value; }
  };

  vm.runInNewContext(launcherSource, {
    URL,
    URLSearchParams,
    document: {
      querySelector(selector) { return elements.get(selector); }
    },
    window: { location }
  }, { filename: "launcher.js" });

  return { elements, location };
}

test("shows direct app, store, and article-option links without automatic navigation", () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = Buffer.from("https://scp-wiki.wikidot.com/scp-173", "utf8").toString("base64url");
  const result = runLauncher(`?id=${id}&source=${source}`);

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#launcher").hidden, false);
  assert.equal(result.elements.get("#open-app").href, `scpdocs://open?id=${id}&source=${source}`);
  assert.equal(
    result.elements.get("#back-to-article").href,
    `https://scpdocs.link/open/?id=${id}&source=${source}`
  );
  assert.equal(result.elements.get("#open-store").hidden, false);
});

test("rejects malformed launch links without navigating", () => {
  const result = runLauncher("?id=not-a-route");

  assert.equal(result.location.replaced, null);
  assert.equal(result.elements.get("#error").hidden, false);
  assert.equal(result.elements.get("#open-app").hidden, true);
  assert.equal(result.elements.get("#open-store").hidden, true);
  assert.equal(result.elements.get("#back-to-article").hidden, true);
});
