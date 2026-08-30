const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "..", "assets", "reading-lists.js"), "utf8");
const readingLists = vm.runInNewContext(`${source}\nSCPDocsReadingLists;`, { URL });

test("builds the installed-app URL from the signed article route", () => {
  const article = { openUrl: "open/?id=a3ecd8849da128f3d092c004&source=c2Nw" };
  assert.equal(
    readingLists.articleAppURL(article, "https://scpdocs.link/reading-ja.html"),
    "scpdocs://open?id=a3ecd8849da128f3d092c004&source=c2Nw",
  );
});

test("opening the app does not send the browser to the official wiki", () => {
  const article = { openUrl: "open/?id=a3ecd8849da128f3d092c004&source=c2Nw" };
  const pageLocation = { href: "https://scpdocs.link/reading-ja.html" };

  readingLists.openArticleInApp(article, pageLocation);

  assert.equal(
    pageLocation.href,
    "scpdocs://open?id=a3ecd8849da128f3d092c004&source=c2Nw",
  );
});
