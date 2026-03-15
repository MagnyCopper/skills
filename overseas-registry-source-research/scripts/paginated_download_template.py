#!/usr/bin/env python3
"""Raw pagination template for registry modules that expose page or offset traversal."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
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


def extract_path(payload: Any, dotted_path: str | None) -> Any:
    if not dotted_path:
        return payload
    current = payload
    for token in dotted_path.split("."):
        if isinstance(current, dict) and token in current:
            current = current[token]
            continue
        raise KeyError(f"Path component {token!r} not found")
    return current


def merge_query_params(url: str, query_params: dict[str, Any]) -> str:
    parts = urlsplit(url)
    merged = dict(parse_qsl(parts.query, keep_blank_values=True))
    for key, value in query_params.items():
        if value is None:
            continue
        merged[str(key)] = str(value)
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(merged), parts.fragment)
    )


def content_suffix(content_type: str | None) -> str:
    if not content_type:
        return ".bin"
    content_type = content_type.lower()
    if "json" in content_type:
        return ".json"
    if "csv" in content_type:
        return ".csv"
    if "html" in content_type:
        return ".html"
    if "zip" in content_type:
        return ".zip"
    if "pdf" in content_type:
        return ".pdf"
    return ".bin"


def build_request(
    url: str,
    method: str,
    headers: dict[str, Any],
    query_params: dict[str, Any],
    body_bytes: bytes | None,
) -> Request:
    final_url = merge_query_params(url, query_params)
    header_values = {str(key): str(value) for key, value in headers.items()}
    return Request(final_url, data=body_bytes, headers=header_values, method=method.upper())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Base endpoint URL.")
    parser.add_argument("--output-dir", required=True, help="Directory for raw page responses.")
    parser.add_argument("--pages", type=int, required=True, help="Number of requests to issue.")
    parser.add_argument("--method", default="GET", help="HTTP method. Default: GET.")
    parser.add_argument("--query-json", help="Static JSON object for query parameters.")
    parser.add_argument("--headers-json", help="Static JSON object for request headers.")
    parser.add_argument("--body-file", help="Optional request body file.")
    parser.add_argument("--page-param", help="Name of page parameter.")
    parser.add_argument("--start-page", type=int, default=1, help="Starting page number.")
    parser.add_argument("--offset-param", help="Name of offset parameter.")
    parser.add_argument("--start-offset", type=int, default=0, help="Starting offset value.")
    parser.add_argument("--page-size-param", help="Name of page-size parameter.")
    parser.add_argument("--page-size", type=int, default=100, help="Page-size value when supported.")
    parser.add_argument("--items-path", help="Dotted path to the item array inside JSON responses.")
    parser.add_argument("--stop-on-empty", action="store_true", help="Stop when extracted item list is empty.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    headers = parse_json_dict(args.headers_json, "headers")
    base_query = parse_json_dict(args.query_json, "query params")
    body_bytes = Path(args.body_file).read_bytes() if args.body_file else None

    summary: dict[str, Any] = {
        "url": args.url,
        "pages_requested": args.pages,
        "pages_saved": [],
    }

    for index in range(args.pages):
        query_params = dict(base_query)
        if args.page_param:
            query_params[args.page_param] = args.start_page + index
        if args.offset_param:
            query_params[args.offset_param] = args.start_offset + (index * args.page_size)
        if args.page_size_param:
            query_params[args.page_size_param] = args.page_size

        request = build_request(args.url, args.method, headers, query_params, body_bytes)
        page_record: dict[str, Any] = {
            "request_index": index,
            "query_params": query_params,
        }
        try:
            with urlopen(request, timeout=args.timeout) as response:
                body = response.read()
                suffix = content_suffix(response.headers.get("Content-Type"))
                response_path = output_dir / f"page-{index:04d}{suffix}"
                response_path.write_bytes(body)

                page_record.update(
                    {
                        "status": response.status,
                        "content_type": response.headers.get("Content-Type"),
                        "response_file": response_path.name,
                        "response_bytes": len(body),
                    }
                )

                if args.items_path and "json" in (response.headers.get("Content-Type") or "").lower():
                    payload = json.loads(body.decode("utf-8"))
                    items = extract_path(payload, args.items_path)
                    item_count = len(items) if isinstance(items, list) else None
                    page_record["item_count"] = item_count
                    if args.stop_on_empty and item_count == 0:
                        summary["pages_saved"].append(page_record)
                        break
        except HTTPError as exc:
            page_record.update({"status": exc.code, "error": str(exc)})
            summary["pages_saved"].append(page_record)
            break
        except URLError as exc:
            page_record.update({"status": "url-error", "error": str(exc)})
            summary["pages_saved"].append(page_record)
            break

        summary["pages_saved"].append(page_record)

    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
