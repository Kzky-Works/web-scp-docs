#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from reading_locale_copy import READING_LOCALES, THEME_COPY


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT.parent / "data-scp-docs" / "list"
ASSET_ROOT = ROOT / "assets"
ITEMS_PER_THEME = 12

NATIVE_MANIFEST = {
    "en": "manifest_scp-foundation.json", "fr": "manifest_scp-fr.json",
    "ru": "manifest_scp-ru.json", "ko": "manifest_scp-ko.json",
    "es": "manifest_scp-es.json", "pl": "manifest_scp-pl.json",
    "cs": "manifest_scp-cs.json", "de": "manifest_scp-de.json",
    "it": "manifest_scp-it.json", "pt": "manifest_scp-pt.json",
    "th": "manifest_scp-th.json", "vn": "manifest_scp-vn.json",
    "cn": "manifest_scp-cn.json", "zh-tr": "manifest_scp-zh-tr.json",
    "tr": "manifest_scp-tr.json",
}

MANIFEST_KIND = {
    "manifest_tales.json": "tale", "manifest_canons.json": "canon",
    "manifest_gois.json": "goi", "manifest_jokes.json": "joke",
    "manifest_recent.json": "recent", "manifest_scp-int.json": "translation",
    "manifest_scp-international.json": "translation",
}

ICONIC = {
    "horror": ["scp-087", "scp-096", "scp-106", "scp-1981", "scp-2316", "scp-2718", "scp-2852", "scp-3001", "scp-3999", "scp-4666", "scp-783", "scp-1733"],
    "emotional": ["scp-348", "scp-1281", "scp-1762", "scp-2265", "scp-2295", "scp-3001", "scp-4999", "scp-5031", "scp-6001", "scp-1287", "scp-1230", "scp-2420"],
    "mind": ["scp-055", "scp-2521", "scp-2316", "scp-2718", "scp-3002", "scp-3309", "scp-3519", "scp-3936", "scp-3125", "scp-4000", "scp-5000", "scp-5999"],
    "scifi": ["scp-093", "scp-2000", "scp-2624", "scp-2935", "scp-3001", "scp-3000", "scp-3200", "scp-4823", "scp-5000", "scp-6001", "scp-7000", "scp-7999"],
    "starter": ["scp-173", "scp-049", "scp-055", "scp-076", "scp-087", "scp-093", "scp-096", "scp-3008", "scp-348", "scp-682", "scp-914", "scp-999"],
}


def route_url(url: str) -> str:
    route_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    source = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    return f"open/?id={route_id}&source={source}"


def load_manifest(branch: str, filename: str, kind: str) -> list[dict[str, Any]]:
    path = DATA_ROOT / branch / filename
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    metadata = payload.get("metadata", {})
    rows = []
    for entry in payload.get("entries", []):
        article_id = str(entry.get("i", "")).strip().lower()
        title = str(entry.get("t", "")).strip()
        url = str(entry.get("u", "")).strip()
        if not article_id or not title or not url.startswith(("http://", "https://")):
            continue
        if url.startswith("http://"):
            url = "https://" + url.removeprefix("http://")
        meta = metadata.get(article_id, {})
        tags = [str(value) for value in meta.get("g", []) if isinstance(value, str)]
        rows.append({
            "id": article_id, "title": title, "url": url, "openUrl": route_url(url),
            "kindKey": kind, "score": int(meta.get("os") or 0),
            "characters": int(meta.get("cc") or 0), "tags": tags[:8],
            "objectClass": next((tag for tag in tags if tag in {
                "safe", "euclid", "keter", "thaumiel", "neutralized", "explained",
                "pending", "apollyon", "archon", "ticonderoga", "esoteric-class",
            }), None),
            "createdAt": int(meta["ct"]) if meta.get("ct") is not None else None,
        })
    return rows


def ranked(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda item: (item["score"], item.get("createdAt") or 0, item["id"]), reverse=True)


def unique(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    result = []
    for row in rows:
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        result.append(row)
    return result


def mix(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    longest = max((len(group) for group in groups), default=0)
    for index in range(longest):
        for group in groups:
            if index < len(group):
                output.append(group[index])
    return unique(output)


def build_pools(branch: str) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    native = ranked(load_manifest(branch, NATIVE_MANIFEST[branch], "native"))
    main_name = "manifest_scp-foundation.json" if branch == "en" else "manifest_scp-main.json"
    translations = ranked(load_manifest(branch, main_name, "native" if branch == "en" else "translation"))
    extras: dict[str, list[dict[str, Any]]] = {}
    for filename, kind in MANIFEST_KIND.items():
        extras.setdefault(kind, []).extend(load_manifest(branch, filename, kind))
    extras = {kind: ranked(unique(rows)) for kind, rows in extras.items()}
    all_rows = unique(native + translations + sum(extras.values(), []))
    by_id = {row["id"]: row for row in all_rows}
    popular = mix(native[:30], translations[:30])
    iconic = {
        key: [by_id[article_id] for article_id in ids if article_id in by_id]
        for key, ids in ICONIC.items()
    }
    fallback = popular + ranked(all_rows)
    pools = {
        "starter": unique(iconic["starter"] + popular),
        "community": popular,
        "local": native,
        "local_more": native[12:] + native[:12],
        "horror": unique(iconic["horror"] + native[5:] + translations),
        "short": ranked(row for row in all_rows if 900 <= row["characters"] <= 6500),
        "long": ranked(row for row in all_rows if row["characters"] >= 18000),
        "emotional": unique(iconic["emotional"] + native[8:] + translations),
        "mind": unique(iconic["mind"] + native[10:] + translations),
        "scifi": unique(iconic["scifi"] + native[4:] + translations),
        "tales": extras.get("tale", []),
        "world": mix(extras.get("canon", []), extras.get("goi", [])),
        "underread": ranked(row for row in all_rows if 4 <= row["score"] <= 50),
        "funny": unique(extras.get("joke", []) + native[6:] + translations),
        "history": unique(native[3:] + extras.get("tale", []) + translations),
        "folklore": unique(native + extras.get("tale", []) + translations),
        "interactive": unique(native[2:] + translations + extras.get("tale", [])),
        "campus": unique(native[7:] + translations + extras.get("tale", [])),
        "recent": extras.get("recent", []),
    }
    for key, rows in pools.items():
        pools[key] = unique(rows + fallback)[:ITEMS_PER_THEME]
    return pools, by_id


def build_locale(locale: str, spec: dict[str, Any]) -> dict[str, Any]:
    pools, by_id = build_pools(spec["branch"])
    themes = []
    selected_ids = []
    for theme_id in spec["theme_order"]:
        label, title, description = THEME_COPY[locale][theme_id]
        article_ids = [row["id"] for row in pools[theme_id]]
        themes.append({
            "id": theme_id, "label": label, "title": title,
            "description": description or spec["choose_copy"], "articleIds": article_ids,
        })
        selected_ids.extend(article_ids)
    articles = [by_id[article_id] for article_id in dict.fromkeys(selected_ids)]
    for article in articles:
        article.pop("createdAt", None)
        if article.get("objectClass") is None:
            article.pop("objectClass", None)
    return {
        "schemaVersion": 2, "locale": locale, "updatedAt": date.today().isoformat(),
        "references": [{"label": label, "url": url} for label, url in spec["references"]],
        "ui": {key: spec[key] for key in ["number_locale", "article_word", "error", "kind_labels"]},
        "themes": themes, "articles": articles,
    }


def main() -> None:
    for locale, spec in READING_LOCALES.items():
        if locale == "ja":
            continue
        payload = build_locale(locale, spec)
        target = ASSET_ROOT / f"recommendations-{locale.lower()}.json"
        target.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"wrote {locale}: {len(payload['themes'])} themes, {len(payload['articles'])} articles")


if __name__ == "__main__":
    main()
