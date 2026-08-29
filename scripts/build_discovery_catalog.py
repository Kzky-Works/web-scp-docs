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
    "manifest_canons.json": "Canon",
    "manifest_gois.json": "GoI",
    "manifest_jokes.json": "Joke SCP",
    "manifest_scp-ex.json": "SCP-EX",
    "manifest_scp001-proposals.json": "SCP-001提言",
    "manifest_collaboration.json": "共同制作",
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

OBJECT_CLASS_TAGS = (
    "safe", "euclid", "keter", "thaumiel", "neutralized", "explained",
    "pending", "apollyon", "archon", "ticonderoga", "decommissioned",
    "esoteric-class",
)


def _route_url(url: str) -> str:
    route_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    source = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    return f"open/?id={route_id}&source={source}"


def _display_tags(tags: list[str]) -> list[str]:
    visible = [tag for tag in tags if tag not in STRUCTURAL_TAGS and len(tag) <= 24]
    return visible[:10]


def _object_class(tags: set[str]) -> str | None:
    return next((tag for tag in OBJECT_CLASS_TAGS if tag in tags), None)


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
    if score >= 20 and (kind in {"Tale", "Canon", "GoI"} or tags & WORLD_TAGS):
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
            modes = _modes(kind, score, characters, created_at, tag_set)
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
            object_class = _object_class(tag_set)
            if object_class:
                candidate["objectClass"] = object_class
            if created_at is not None:
                candidate["createdAt"] = created_at
            existing = articles.get(url)
            if existing is None or score > existing["score"]:
                articles[url] = candidate

    return list(articles.values()), generated_at


def build_catalog(branch_dir: Path) -> dict[str, Any]:
    candidates, generated_at = load_candidates(branch_dir)
    articles = sorted(candidates, key=lambda article: (article["kind"], article["id"]))
    mode_counts = {
        mode: sum(mode in article["modes"] for article in articles)
        for mode in MODE_ORDER
    }
    kind_counts = {
        kind: sum(article["kind"] == kind for article in articles)
        for kind in dict.fromkeys(MANIFESTS.values())
    }
    object_class_counts = {
        object_class: sum(article.get("objectClass") == object_class for article in articles)
        for object_class in OBJECT_CLASS_TAGS
    }
    return {
        "schemaVersion": 2,
        "catalogGeneratedAt": max(generated_at) if generated_at else None,
        "source": "SCP Docs public JP catalog snapshot",
        "articleCount": len(articles),
        "kindCounts": kind_counts,
        "objectClassCounts": object_class_counts,
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
