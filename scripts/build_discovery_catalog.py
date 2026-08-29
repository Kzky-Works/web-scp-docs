#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRANCH_DIR = ROOT.parent / "data-scp-docs" / "list" / "jp"
DEFAULT_OUTPUT = ROOT / "assets" / "discovery-ja.json"

MANIFESTS = {
    "manifest_scp-jp.json": "SCP-JP",
    "manifest_scp-main.json": "翻訳SCP",
    "manifest_scp-int.json": "SCP-INT",
    "manifest_tales.json": "Tale",
}

STRUCTURAL_TAGS = {
    "jp", "en", "scp", "tale", "ハブ", "メタデータ", "合作", "合同編集",
    "注目記事", "注目の翻訳記事", "ページタイプ", "著者ページ",
}

EERIE_TAGS = {
    "ホラー", "クリーピーパスタ", "認識災害", "精神影響", "記憶影響",
    "死体", "敵対的", "捕食", "幻覚", "情報災害",
}

STRANGE_TAGS = {
    "異次元", "現実改変", "時間", "空間", "概念", "反ミーム", "ミーム",
    "ポータル", "夢界", "超次元",
}

WORLD_TAGS = {
    "世界オカルト連合", "日本生類創研", "壊れた神の教会", "蒐集院", "サーキック",
    "東弊重工", "パラウォッチ", "オネイロイ", "are-we-cool-yet", "mc&d",
}

MODE_ORDER = ("popular", "short", "long", "eerie", "strange", "world", "hidden", "recent")
MODE_LIMIT = 160


def _route_url(url: str) -> str:
    route_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    source = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    return f"open/?id={route_id}&source={source}"


def _display_tags(tags: list[str]) -> list[str]:
    visible = [tag for tag in tags if tag not in STRUCTURAL_TAGS and len(tag) <= 24]
    return visible[:10]


def _modes(kind: str, score: int, characters: int, created_at: int | None, tags: set[str]) -> list[str]:
    modes: list[str] = []
    if score >= 100:
        modes.append("popular")
    if 1_000 <= characters <= 6_500 and score >= 20:
        modes.append("short")
    if characters >= 20_000 and score >= 25:
        modes.append("long")
    if score >= 20 and tags & EERIE_TAGS:
        modes.append("eerie")
    if score >= 20 and tags & STRANGE_TAGS:
        modes.append("strange")
    if score >= 20 and (kind == "Tale" or tags & WORLD_TAGS):
        modes.append("world")
    if 15 <= score <= 80 and not tags & {"注目記事", "注目の翻訳記事"}:
        modes.append("hidden")
    if created_at is not None:
        modes.append("recent")
    return modes


def load_candidates(branch_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    articles: dict[str, dict[str, Any]] = {}
    generated_at: list[str] = []

    for filename, kind in MANIFESTS.items():
        path = branch_dir / filename
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("generatedAt"):
            generated_at.append(str(payload["generatedAt"]))
        metadata = payload.get("metadata", {})
        for entry in payload.get("entries", []):
            article_id = str(entry.get("i", "")).lower()
            title = str(entry.get("t", "")).strip()
            url = str(entry.get("u", "")).strip()
            if not article_id or not title or not url.startswith("https://scp-jp.wikidot.com/"):
                continue
            meta = metadata.get(article_id, {})
            score = int(meta.get("os") or 0)
            characters = int(meta.get("cc") or 0)
            created_at = int(meta["ct"]) if meta.get("ct") is not None else None
            raw_tags = [str(tag) for tag in meta.get("g", []) if isinstance(tag, str)]
            tag_set = set(raw_tags)
            if "ハブ" in tag_set or score < 10 or characters < 500:
                continue
            modes = _modes(kind, score, characters, created_at, tag_set)
            if not modes:
                continue
            candidate = {
                "id": article_id,
                "title": title,
                "url": url,
                "openUrl": _route_url(url),
                "kind": kind,
                "score": score,
                "characters": characters,
                "tags": _display_tags(raw_tags),
                "modes": modes,
            }
            if created_at is not None:
                candidate["createdAt"] = created_at
            existing = articles.get(url)
            if existing is None or score > existing["score"]:
                articles[url] = candidate

    return list(articles.values()), generated_at


def build_catalog(branch_dir: Path) -> dict[str, Any]:
    candidates, generated_at = load_candidates(branch_dir)
    selected: dict[str, dict[str, Any]] = {}
    mode_counts: dict[str, int] = {}

    for mode in MODE_ORDER:
        pool = [article for article in candidates if mode in article["modes"]]
        if mode == "recent":
            pool.sort(key=lambda article: (article.get("createdAt", 0), article["score"]), reverse=True)
        elif mode == "hidden":
            pool.sort(key=lambda article: (article["score"], article["characters"]), reverse=True)
        else:
            pool.sort(key=lambda article: (article["score"], -article["characters"]), reverse=True)
        pool = pool[:MODE_LIMIT]
        mode_counts[mode] = len(pool)
        for article in pool:
            if article["url"] not in selected:
                selected[article["url"]] = {**article, "modes": []}
            selected[article["url"]]["modes"].append(mode)

    undersized = {mode: count for mode, count in mode_counts.items() if count < 12}
    if undersized:
        raise ValueError(f"discovery modes need at least 12 articles: {undersized}")

    articles = sorted(selected.values(), key=lambda article: (article["kind"], article["id"]))
    return {
        "schemaVersion": 1,
        "catalogGeneratedAt": max(generated_at) if generated_at else None,
        "source": "SCP Docs public JP catalog snapshot",
        "modeCounts": mode_counts,
        "articles": articles,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the lightweight Japanese article-discovery catalog.")
    parser.add_argument("--branch-dir", type=Path, default=DEFAULT_BRANCH_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    catalog = build_catalog(args.branch_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(catalog['articles'])} articles to {args.output}")


if __name__ == "__main__":
    main()
