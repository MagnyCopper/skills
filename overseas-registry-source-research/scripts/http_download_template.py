#!/usr/bin/env python3
"""Minimal raw HTTP downloader template for registry source validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen


def parse_json_dict(raw: str | None, label: str) -> dict[str, Any]:
    if raw is None:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{label} must decode to a JSON object")
    return value


def merge_query_params(url: str, query_params: dict[str, Any]) -> str:
    if not query_params:
        return url
    parts = urlsplit(url)
    merged = dict(parse_qsl(parts.query, keep_blank_values=True))
    for key, value in query_params.items():
        if value is None:
            continue
        merged[str(key)] = str(value)
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(merged), parts.fragment)
    )


def build_request(args: argparse.Namespace) -> Request:
    headers = {str(key): str(value) for key, value in parse_json_dict(args.headers_json, "headers").items()}
    query_params = parse_json_dict(args.query_json, "query params")
    payload = None
    if args.body_file:
        payload = Path(args.body_file).read_bytes()
    final_url = merge_query_params(args.url, query_params)
    return Request(final_url, data=payload, headers=headers, method=args.method.upper())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Endpoint or download URL.")
    parser.add_argument("--output", required=True, help="Path for the raw downloaded file.")
    parser.add_argument("--method", default="GET", help="HTTP method. Default: GET.")
    parser.add_argument("--headers-json", help="JSON object for request headers.")
    parser.add_argument("--query-json", help="JSON object for query parameters.")
    parser.add_argument("--body-file", help="Optional request body file for POST or PUT flows.")
    parser.add_argument("--metadata-output", help="Optional JSON file for response metadata.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds.")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    request = build_request(args)
    with urlopen(request, timeout=args.timeout) as response:
        body = response.read()
        output_path.write_bytes(body)

        if args.metadata_output:
            metadata_path = Path(args.metadata_output)
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata = {
                "url": response.geturl(),
                "status": response.status,
                "content_type": response.headers.get("Content-Type"),
                "content_length": len(body),
                "output_file": str(output_path),
            }
            metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
