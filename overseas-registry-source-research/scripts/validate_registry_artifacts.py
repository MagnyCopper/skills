#!/usr/bin/env python3
"""Validate output naming and file presence for registry research artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_module_spec(raw: str) -> tuple[str, str]:
    if ":" not in raw:
        raise argparse.ArgumentTypeError("Module spec must be SOURCE_ID:MODULE_ID")
    source_id, module_id = raw.split(":", 1)
    if not source_id or not module_id:
        raise argparse.ArgumentTypeError("Module spec must be SOURCE_ID:MODULE_ID")
    return source_id, module_id


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", default="results", help="Root results directory.")
    parser.add_argument("--date", required=True, help="Result date in YYYYMMDD.")
    parser.add_argument("--slug", required=True, help="Country or region slug.")
    parser.add_argument(
        "--skill-name",
        default="overseas-registry-source-research",
        help="Skill directory name under the date directory.",
    )
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        type=parse_module_spec,
        help="Selected module in SOURCE_ID:MODULE_ID form. Repeat per module.",
    )
    parser.add_argument(
        "--boundary-module",
        action="append",
        default=[],
        type=parse_module_spec,
        help="Module that must have a boundary-probe artifact. Repeat per module.",
    )
    parser.add_argument("--allow-extra-markdown", action="store_true", help="Allow Markdown files beyond the main report.")
    parser.add_argument("--output-json", help="Optional JSON output path.")
    args = parser.parse_args()

    result_dir = Path(args.results_root) / args.date / args.skill_name
    reversed_dir = Path(args.results_root) / args.skill_name / args.date
    report_path = result_dir / f"{args.slug}-registry-source-research.md"

    checks: list[dict[str, object]] = []

    def record(ok: bool, label: str, detail: str) -> None:
        checks.append({"ok": ok, "label": label, "detail": detail})

    record(result_dir.is_dir(), "result_dir_exists", str(result_dir))
    record(not reversed_dir.exists(), "no_reversed_dir", str(reversed_dir))
    record(report_path.is_file(), "main_report_exists", str(report_path))

    if result_dir.is_dir():
        markdown_files = sorted(path.name for path in result_dir.glob("*.md"))
        extra_markdown = [name for name in markdown_files if name != report_path.name]
        record(
            args.allow_extra_markdown or not extra_markdown,
            "single_main_markdown",
            ", ".join(extra_markdown) if extra_markdown else "ok",
        )

        for source_id, module_id in args.module:
            script_name = f"{args.slug}-{source_id}-{module_id}-download-sample.py"
            sample_glob = f"{args.slug}-{source_id}-{module_id}-test-dataset-*"
            script_path = result_dir / script_name
            sample_matches = sorted(path.name for path in result_dir.glob(sample_glob))
            record(script_path.is_file(), f"script_exists:{source_id}:{module_id}", str(script_path))
            record(bool(sample_matches), f"sample_exists:{source_id}:{module_id}", ", ".join(sample_matches) or sample_glob)

        for source_id, module_id in args.boundary_module:
            boundary_path = result_dir / f"{args.slug}-{source_id}-{module_id}-boundary-probe.json"
            record(
                boundary_path.is_file(),
                f"boundary_probe_exists:{source_id}:{module_id}",
                str(boundary_path),
            )

    failures = [check for check in checks if not check["ok"]]
    output = {
        "result_dir": str(result_dir),
        "report_path": str(report_path),
        "checks": checks,
        "failure_count": len(failures),
    }

    if args.output_json:
        output_path = Path(args.output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    else:
        print(json.dumps(output, indent=2))

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
