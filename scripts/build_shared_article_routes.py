#!/usr/bin/env python3
"""Build small static route shards for SCP docs shared article links."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = 1
ROUTE_ID_HEX_LENGTH = 24
ALLOWED_LANGUAGES = ("EN", "ES", "FR", "JP", "KO", "PL", "RU", "CN", "TH", "DE")
ALLOWED_HOSTS = {
    "scp-wiki.wikidot.com",
    "scp-int.wikidot.com",
    "lafundacionscp.wikidot.com",
    "fondationscp.wikidot.com",
    "scp-jp.wikidot.com",
    "scpko.wikidot.com",
    "scp-pl.wikidot.com",
    "scpfoundation.net",
    "scp-ru.wikidot.com",
    "scp-wiki-cn.wikidot.com",
    "scp-th.wikidot.com",
    "scp-wiki-de.wikidot.com",
}


def normalize_url(raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if host == "scp-ru.wikidot.com":
        host = "scpfoundation.net"
    if host not in ALLOWED_HOSTS:
        return ""
    path = parsed.path.rstrip("/") or "/"
    scheme = "http" if host == "scp-th.wikidot.com" else "https"
    return f"{scheme}://{host}{path}"


def route_id(source_url: str) -> str:
    normalized = normalize_url(source_url)
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:ROUTE_ID_HEX_LENGTH]


def build_routes(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    routes: dict[str, dict[str, Any]] = {}
    for raw_entry in payload.get("entries") or []:
        if not isinstance(raw_entry, dict):
            continue
        source_url = normalize_url(raw_entry.get("sourceURL"))
        identifier = route_id(source_url)
        if not source_url or not identifier:
            continue

        versions: dict[str, str] = {}
        for raw_version in raw_entry.get("versions") or []:
            if not isinstance(raw_version, dict):
                continue
            language = str(raw_version.get("language") or "").upper()
            url = normalize_url(raw_version.get("url"))
            if language in ALLOWED_LANGUAGES and url:
                versions[language] = url

        raw_original = raw_entry.get("original") if isinstance(raw_entry.get("original"), dict) else {}
        original_language = str(raw_original.get("language") or "EN").upper()
        original_url = normalize_url(raw_original.get("url")) or source_url
        versions.setdefault("EN", source_url)
        route = {
            "sourceURL": source_url,
            "original": {"language": original_language, "url": original_url},
            "versions": {language: versions[language] for language in ALLOWED_LANGUAGES if language in versions},
        }
        existing = routes.get(identifier)
        if existing is not None and existing["sourceURL"] != source_url:
            raise ValueError(f"route ID collision: {identifier}: {existing['sourceURL']} != {source_url}")
        routes[identifier] = route
    return routes


def write_shards(routes: dict[str, dict[str, Any]], output_dir: Path, generated_at: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for existing in output_dir.glob("*.json"):
        existing.unlink()

    shards: dict[str, dict[str, dict[str, Any]]] = {}
    for identifier, route in routes.items():
        shards.setdefault(identifier[:2], {})[identifier] = route

    for prefix, shard_routes in sorted(shards.items()):
        payload = {
            "schemaVersion": SCHEMA_VERSION,
            "generatedAt": generated_at,
            "routes": {key: shard_routes[key] for key in sorted(shard_routes)},
        }
        (output_dir / f"{prefix}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    index = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": generated_at,
        "routeCount": len(routes),
        "shards": sorted(shards),
    }
    (output_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with args.source.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("translation manifest root must be an object")
    routes = build_routes(payload)
    write_shards(routes, args.output, str(payload.get("generatedAt") or ""))
    print(f"OK: wrote {len(routes)} routes to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
