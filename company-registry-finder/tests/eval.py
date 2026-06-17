#!/usr/bin/env python3
"""Three-tier scorer for company-registry-finder."""

import json
import re
import sys
import unicodedata
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_SET = Path(__file__).resolve().parent / "companyName.txt"
RESULTS_DIR = REPO_ROOT / "results"

NAME_PUNCT_RE = re.compile(r"[,\.\-_/\(\)\[\]【】［］「」'\"&;:·•]")
WS_RE = re.compile(r"\s+")
CHE_PREFIX_RE = re.compile(r"^che[-.\s]*", re.IGNORECASE)
LEADING_REGNUM_PREFIX_RE = re.compile(
    r"^(?:amtsgericht\s+\w+|münchen|stendal|jena|berlin|hamburg|frankfurt|hrb|hra|gnr|vr|pr|fa)\b[\s:,-]*",
    re.IGNORECASE,
)


def fold_full_width(s):
    chars = []
    for ch in s:
        code = ord(ch)
        if code == 0x3000:
            chars.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:
            chars.append(chr(code - 0xFEE0))
        else:
            chars.append(ch)
    return "".join(chars)


def normalize_name(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", str(s))
    s = fold_full_width(s)
    s = s.lower()
    s = NAME_PUNCT_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip()
    return s


def normalize_regnum(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", str(s))
    s = fold_full_width(s)
    s = s.lower()
    while True:
        updated = LEADING_REGNUM_PREFIX_RE.sub("", s)
        if updated == s:
            break
        s = updated.lstrip()
    s = CHE_PREFIX_RE.sub("", s)
    s = s.replace(".", "").replace("-", "")
    s = WS_RE.sub("", s).strip()
    return s


def load_ground_truth():
    rows = []
    try:
        lines = TEST_SET.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"error reading ground truth: {exc}", file=sys.stderr)
        sys.exit(2)

    for idx, line in enumerate(lines, start=1):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            print(f"invalid ground truth row {idx}: expected at least 2 tab-separated columns", file=sys.stderr)
            sys.exit(2)
        raw_name = parts[0]
        gt_std_name = parts[1]
        gt_regnum = parts[2] if len(parts) >= 3 else ""
        rows.append(
            {
                "row": idx,
                "id": f"{idx:03d}",
                "raw_name": raw_name,
                "gt_std_name": gt_std_name,
                "gt_regnum": gt_regnum,
            }
        )
    return rows


def load_prediction(row_id, run_date):
    path = RESULTS_DIR / run_date / "company-registry-finder" / f"{row_id}.json"
    if not path.exists():
        return None, "missing"
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh), None
    except (OSError, json.JSONDecodeError):
        return None, "schema_error"


def score_row(row, run_date):
    pred, reason = load_prediction(row["id"], run_date)
    if pred is None:
        if row["gt_regnum"].strip() == "":
            regnum_match = None
        else:
            regnum_match = 0
        return {
            **row,
            "pred_name": None,
            "pred_regnum": None,
            "name_match": 0,
            "regnum_match": regnum_match,
            "reason": reason,
        }

    try:
        result = pred["result"]
        pred_name = result["standard_name"]
        pred_regnum = result.get("registration_number")
    except (KeyError, TypeError, AttributeError):
        if row["gt_regnum"].strip() == "":
            regnum_match = None
        else:
            regnum_match = 0
        return {
            **row,
            "pred_name": None,
            "pred_regnum": None,
            "name_match": 0,
            "regnum_match": regnum_match,
            "reason": "schema_error",
        }

    name_match = 1 if normalize_name(pred_name) == normalize_name(row["gt_std_name"]) else 0
    if row["gt_regnum"].strip() == "":
        regnum_match = None
    else:
        regnum_match = 1 if normalize_regnum(pred_regnum) == normalize_regnum(row["gt_regnum"]) else 0

    return {
        **row,
        "pred_name": pred_name,
        "pred_regnum": pred_regnum,
        "name_match": name_match,
        "regnum_match": regnum_match,
        "reason": "ok",
    }


def score(run_date):
    rows = load_ground_truth()
    scored = []
    name_matches = 0
    regnum_matches = 0
    regnum_possible = 0

    for row in rows:
        if row["gt_regnum"].strip() != "":
            regnum_possible += 1
        scored_row = score_row(row, run_date)
        scored.append(scored_row)
        name_matches += scored_row["name_match"]
        if scored_row["regnum_match"] is not None:
            regnum_matches += scored_row["regnum_match"]

    total = name_matches + regnum_matches
    achievable_max = len(rows) + regnum_possible

    return {
        "run_date": run_date,
        "total_rows": len(rows),
        "name_matches": name_matches,
        "regnum_possible": regnum_possible,
        "regnum_matches": regnum_matches,
        "total_score": total,
        "achievable_max": achievable_max,
        "name_pct": (name_matches / len(rows) * 100.0) if rows else 0.0,
        "regnum_pct": (regnum_matches / regnum_possible * 100.0) if regnum_possible else 0.0,
        "total_pct": (total / achievable_max * 100.0) if achievable_max else 0.0,
        "per_row": scored,
    }


def print_report(result, verbose=False, failures_only=False):
    print(
        "Name matches {}/{} ({:.2f}%), Regnum matches {}/{} ({:.2f}%), TOTAL: {} / {} ({:.2f}%)".format(
            result["name_matches"],
            result["total_rows"],
            result["name_pct"],
            result["regnum_matches"],
            result["regnum_possible"],
            result["regnum_pct"],
            result["total_score"],
            result["achievable_max"],
            result["total_pct"],
        )
    )

    if not verbose and not failures_only:
        return

    print()
    print("--- Per-row ---")
    for row in result["per_row"]:
        if failures_only and row["name_match"] == 1 and row["regnum_match"] in (1, None):
            continue
        regnum_str = "N/A" if row["regnum_match"] is None else str(row["regnum_match"])
        print(f"  [{row['id']}] name={row['name_match']} regnum={regnum_str}  reason={row['reason']}")
        print(f"        raw:      {row['raw_name'][:60]}")
        print(f"        gt_name:  {row['gt_std_name'][:60]}")
        if row.get("pred_name"):
            print(f"        pred:     {row['pred_name'][:60]}")
        if row["gt_regnum"]:
            print(f"        gt_reg:   {row['gt_regnum']}")
            if row.get("pred_regnum"):
                print(f"        pred_reg: {row['pred_regnum']}")


def main():
    if len(sys.argv) < 2:
        print("usage: eval.py <YYYYMMDD> [--verbose] [--failures-only]", file=sys.stderr)
        sys.exit(2)

    run_date = sys.argv[1]
    verbose = "--verbose" in sys.argv[2:]
    failures_only = "--failures-only" in sys.argv[2:]

    result = score(run_date)
    print_report(result, verbose=verbose, failures_only=failures_only)


if __name__ == "__main__":
    main()
