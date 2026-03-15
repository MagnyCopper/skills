#!/usr/bin/env python3
"""Browser-gated probe template for registry modules that need Playwright."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def run_probe(args: argparse.Namespace) -> dict[str, object]:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Playwright is not installed. Install `playwright` and the browser binaries before using this template."
        ) from exc

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = output_dir / "probe.png"
    html_path = output_dir / "probe.html"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headed)
        page = browser.new_page()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)
            for selector in args.wait_for_selector:
                page.wait_for_selector(selector, timeout=args.timeout_ms)
            for selector in args.click_selector:
                page.locator(selector).first.click(timeout=args.timeout_ms)
            page.screenshot(path=str(screenshot_path), full_page=True)
            html_path.write_text(page.content(), encoding="utf-8")
            result = {
                "status": "ok",
                "final_url": page.url,
                "title": page.title(),
                "screenshot_file": screenshot_path.name,
                "html_file": html_path.name,
                "wait_for_selector": args.wait_for_selector,
                "click_selector": args.click_selector,
            }
        except PlaywrightTimeoutError as exc:
            result = {
                "status": "timeout",
                "final_url": page.url,
                "error": str(exc),
                "wait_for_selector": args.wait_for_selector,
                "click_selector": args.click_selector,
            }
        finally:
            browser.close()

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Entry URL to probe.")
    parser.add_argument("--output-dir", required=True, help="Directory for probe outputs.")
    parser.add_argument("--wait-for-selector", action="append", default=[], help="Selector that must appear before capture.")
    parser.add_argument("--click-selector", action="append", default=[], help="Selector to click before capture.")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="Per-operation timeout in milliseconds.")
    parser.add_argument("--headed", action="store_true", help="Launch browser in headed mode.")
    args = parser.parse_args()

    result = run_probe(args)
    output_dir = Path(args.output_dir)
    (output_dir / "probe-summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
