#!/usr/bin/env python3
"""Probe search and pagination boundaries for registry source validation."""

from __future__ import annotations

import argparse
import json
import time
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


def parse_csv_values(raw: str | None, cast=str) -> list[Any]:
    if not raw:
        return []
    values = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        values.append(cast(item))
    return values


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


def issue_request(
    url: str,
    headers: dict[str, Any],
    query_params: dict[str, Any],
    timeout: float,
) -> dict[str, Any]:
    final_url = merge_query_params(url, query_params)
    request = Request(
        final_url,
        headers={str(key): str(value) for key, value in headers.items()},
        method="GET",
    )
    started = time.time()
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            elapsed = round(time.time() - started, 3)
            record: dict[str, Any] = {
                "url": response.geturl(),
                "status": response.status,
                "elapsed_seconds": elapsed,
                "content_type": response.headers.get("Content-Type"),
                "response_bytes": len(body),
            }
            if "json" in (response.headers.get("Content-Type") or "").lower():
                payload = json.loads(body.decode("utf-8"))
                record["json"] = payload
            return record
    except HTTPError as exc:
        return {
            "url": final_url,
            "status": exc.code,
            "elapsed_seconds": round(time.time() - started, 3),
            "error": str(exc),
        }
    except URLError as exc:
        return {
            "url": final_url,
            "status": "url-error",
            "elapsed_seconds": round(time.time() - started, 3),
            "error": str(exc),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Search endpoint URL.")
    parser.add_argument("--output", required=True, help="JSON file for probe output.")
    parser.add_argument("--headers-json", help="JSON object for request headers.")
    parser.add_argument("--query-json", help="JSON object for static query parameters.")
    parser.add_argument("--query-param", required=True, help="Name of search query parameter.")
    parser.add_argument("--queries", required=True, help="Comma-separated search values to test.")
    parser.add_argument("--page-size-param", help="Name of page-size parameter.")
    parser.add_argument("--page-sizes", help="Comma-separated page-size values.")
    parser.add_argument("--offset-param", help="Name of offset or page-depth parameter.")
    parser.add_argument("--offsets", help="Comma-separated offset values.")
    parser.add_argument("--items-path", help="Dotted path to item list in JSON responses.")
    parser.add_argument("--count-path", help="Dotted path to reported total count in JSON responses.")
    parser.add_argument("--rate-probe-count", type=int, default=0, help="Burst request count for rate-limit probing.")
    parser.add_argument("--rate-probe-interval", type=float, default=0.0, help="Delay between burst requests.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds.")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = parse_json_dict(args.headers_json, "headers")
    base_query = parse_json_dict(args.query_json, "query params")
    queries = parse_csv_values(args.queries, str)
    page_sizes = parse_csv_values(args.page_sizes, int) or [None]
    offsets = parse_csv_values(args.offsets, int) or [None]

    runs: list[dict[str, Any]] = []
    max_successful_page_size: int | None = None
    max_successful_offset: int | None = None
    first_non_200_status: Any = None

    for query_value in queries:
        for page_size in page_sizes:
            for offset in offsets:
                request_query = dict(base_query)
                request_query[args.query_param] = query_value
                if args.page_size_param and page_size is not None:
                    request_query[args.page_size_param] = page_size
                if args.offset_param and offset is not None:
                    request_query[args.offset_param] = offset

                result = issue_request(args.url, headers, request_query, args.timeout)
                run_record: dict[str, Any] = {
                    "query_params": request_query,
                    "status": result["status"],
                    "elapsed_seconds": result["elapsed_seconds"],
                    "content_type": result.get("content_type"),
                    "response_bytes": result.get("response_bytes"),
                    "url": result["url"],
                }
                payload = result.get("json")
                if payload is not None:
                    if args.items_path:
                        try:
                            items = extract_path(payload, args.items_path)
                            run_record["item_count"] = len(items) if isinstance(items, list) else None
                        except KeyError as exc:
                            run_record["items_path_error"] = str(exc)
                    if args.count_path:
                        try:
                            run_record["reported_total"] = extract_path(payload, args.count_path)
                        except KeyError as exc:
                            run_record["count_path_error"] = str(exc)

                if result["status"] == 200:
                    if page_size is not None:
                        max_successful_page_size = max(
                            page_size,
                            max_successful_page_size or page_size,
                        )
                    if offset is not None:
                        max_successful_offset = max(
                            offset,
                            max_successful_offset or offset,
                        )
                elif first_non_200_status is None:
                    first_non_200_status = result["status"]

                if "error" in result:
                    run_record["error"] = result["error"]
                runs.append(run_record)

    rate_probe: list[dict[str, Any]] = []
    if args.rate_probe_count > 0 and queries:
        baseline_query = dict(base_query)
        baseline_query[args.query_param] = queries[0]
        if args.page_size_param and page_sizes and page_sizes[0] is not None:
            baseline_query[args.page_size_param] = page_sizes[0]
        if args.offset_param and offsets and offsets[0] is not None:
            baseline_query[args.offset_param] = offsets[0]

        for iteration in range(args.rate_probe_count):
            result = issue_request(args.url, headers, baseline_query, args.timeout)
            rate_probe.append(
                {
                    "iteration": iteration + 1,
                    "status": result["status"],
                    "elapsed_seconds": result["elapsed_seconds"],
                    "url": result["url"],
                }
            )
            if "error" in result:
                rate_probe[-1]["error"] = result["error"]
            if result["status"] != 200:
                break
            if args.rate_probe_interval > 0:
                time.sleep(args.rate_probe_interval)

    output = {
        "url": args.url,
        "queries": queries,
        "page_sizes": page_sizes,
        "offsets": offsets,
        "runs": runs,
        "rate_probe": rate_probe,
        "summary": {
            "max_successful_page_size": max_successful_page_size,
            "max_successful_offset": max_successful_offset,
            "first_non_200_status": first_non_200_status,
            "first_rate_probe_failure_iteration": next(
                (item["iteration"] for item in rate_probe if item["status"] != 200),
                None,
            ),
        },
    }
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
