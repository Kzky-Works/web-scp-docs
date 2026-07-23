const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const launcherSource = fs.readFileSync(path.join(__dirname, "..", "launch", "launcher.js"), "utf8");

function runLauncher(search, { rejectCustomScheme = false } = {}) {
  const listeners = new Map();
  const documentListeners = new Map();
  const windowListeners = new Map();
  const elements = new Map();
  for (const id of ["launcher", "open-app", "back-to-article", "error"]) {
    elements.set(`#${id}`, {
      hidden: id === "launcher" || id === "error",
      addEventListener(name, callback) { listeners.set(`${id}:${name}`, callback); }
    });
  }

  const navigation = [];
  let timer = null;
  const location = {
    href: `https://scpdocs.link/launch/${search}`,
    search,
    replace(value) {
      if (rejectCustomScheme && String(value).startsWith("scpdocs:")) throw new Error("Blocked scheme");
      navigation.push(value);
    }
  };
  const document = {
    hidden: false,
    querySelector(selector) { return elements.get(selector); },
    addEventListener(name, callback) { documentListeners.set(name, callback); }
  };
  const window = {
    location,
    addEventListener(name, callback) { windowListeners.set(name, callback); },
    clearTimeout(value) { if (timer === value) timer = null; },
    setTimeout(callback, delay) {
      timer = { callback, delay };
      return timer;
    }
  };

  vm.runInNewContext(launcherSource, {
    URL,
    URLSearchParams,
    document,
    window
  }, { filename: "launcher.js" });

  return {
    document,
    documentListeners,
    elements,
    listeners,
    navigation,
    timer: () => timer,
    windowListeners
  };
}

test("automatically attempts the article deep link and exposes a retry button", () => {
  const id = "a3ecd8849da128f3d092c004";
  const source = Buffer.from("https://scp-wiki.wikidot.com/scp-173", "utf8").toString("base64url");
  const result = runLauncher(`?id=${id}&source=${source}`);
  const expected = `scpdocs://open?id=${id}&source=${source}`;

  assert.deepEqual(result.navigation, [expected]);
  assert.equal(result.elements.get("#launcher").hidden, false);
  assert.equal(result.elements.get("#open-app").hidden, false);
  assert.equal(
    result.elements.get("#back-to-article").href,
    `https://scpdocs.link/open/?id=${id}&source=${source}`
  );
  assert.equal(result.timer().delay, 900);

  result.listeners.get("open-app:click")();
  assert.deepEqual(result.navigation, [expected, expected]);
});

test("falls back to the App Store when the app did not take focus", () => {
  const result = runLauncher("?id=a3ecd8849da128f3d092c004");

  result.timer().callback();
  assert.deepEqual(result.navigation, [
    "scpdocs://open?id=a3ecd8849da128f3d092c004",
    "https://apps.apple.com/app/scp-docs/id6765882660"
  ]);
});

test("keeps the App Store fallback when the embedded browser rejects the scheme", () => {
  const result = runLauncher("?id=a3ecd8849da128f3d092c004", { rejectCustomScheme: true });

  assert.equal(result.timer().delay, 900);
  result.timer().callback();
  assert.deepEqual(result.navigation, ["https://apps.apple.com/app/scp-docs/id6765882660"]);
});

test("cancels the store fallback after the app takes focus", () => {
  const result = runLauncher("?id=a3ecd8849da128f3d092c004");

  result.document.hidden = true;
  result.documentListeners.get("visibilitychange")();
  assert.equal(result.timer(), null);
  assert.deepEqual(result.navigation, ["scpdocs://open?id=a3ecd8849da128f3d092c004"]);
});

test("rejects malformed launch links without navigating", () => {
  const result = runLauncher("?id=not-a-route");

  assert.deepEqual(result.navigation, []);
  assert.equal(result.elements.get("#error").hidden, false);
  assert.equal(result.elements.get("#open-app").hidden, true);
  assert.equal(result.elements.get("#back-to-article").hidden, true);
  assert.equal(result.timer(), null);
});
