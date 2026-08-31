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
