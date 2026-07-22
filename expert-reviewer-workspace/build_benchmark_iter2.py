#!/usr/bin/env python3
"""Build benchmark.json for iteration-2. Schema-compliant."""
import json
import statistics
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path("/Users/han/Projects/skills/expert-reviewer-workspace/iteration-2")
SKILL_PATH = Path("/Users/han/Projects/skills/expert-reviewer")

with open(SKILL_PATH / "evals/evals.json") as f:
    evals_meta = json.load(f)
eval_map = {e["id"]: e for e in evals_meta["evals"]}

dir_to_id = {
    "eval-technical-architecture-design-review": 1,
    "eval-business-plan-review-with-investor-lens": 2,
    "eval-research-paper-review-statistical-rigor": 3,
    "eval-adhoc-idea-critique-no-document": 4,
    "eval-english-serverless-architecture-review": 5,
}

runs = []
for dir_name, eval_id in dir_to_id.items():
    eval_dir = WORKSPACE / dir_name
    eval_meta = eval_map[eval_id]
    eval_name_short = dir_name.replace("eval-", "")
    
    for config in ["with_skill", "without_skill"]:
        grading_path = eval_dir / config / "grading.json"
        timing_path = eval_dir / config / "timing.json"
        
        if not grading_path.exists():
            print(f"SKIP: missing grading.json for {dir_name}/{config}")
            continue
        
        with open(grading_path) as f:
            grading = json.load(f)
        
        time_seconds = None
        tokens = None
        if timing_path.exists():
            with open(timing_path) as f:
                timing = json.load(f)
            time_seconds = timing.get("total_duration_seconds")
            tokens = timing.get("total_tokens")
        
        summary = grading.get("summary", {})
        expectations = grading.get("expectations", [])
        
        run = {
            "eval_id": eval_id,
            "eval_name": eval_meta.get("name", eval_name_short),
            "configuration": config,
            "run_number": 1,
            "result": {
                "pass_rate": summary.get("pass_rate", 0.0),
                "passed": summary.get("passed", 0),
                "failed": summary.get("failed", 0),
                "total": summary.get("total", 0),
                "time_seconds": time_seconds or 0.0,
                "tokens": tokens or 0,
                "tool_calls": 0,
                "errors": 0,
            },
            "expectations": [
                {"text": e["text"], "passed": e["passed"], "evidence": e.get("evidence", "")}
                for e in expectations
            ],
            "notes": [],
        }
        runs.append(run)
        print(f"{dir_name:55} {config:15} → pass_rate={summary.get('pass_rate', 0):.1%}")

def stats(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
    return {
        "mean": statistics.mean(vals),
        "stddev": statistics.stdev(vals) if len(vals) > 1 else 0.0,
        "min": min(vals),
        "max": max(vals),
    }

ws_pass = [r["result"]["pass_rate"] for r in runs if r["configuration"] == "with_skill"]
wos_pass = [r["result"]["pass_rate"] for r in runs if r["configuration"] == "without_skill"]
ws_time = [r["result"]["time_seconds"] for r in runs if r["configuration"] == "with_skill" and r["result"]["time_seconds"] > 0]
wos_time = [r["result"]["time_seconds"] for r in runs if r["configuration"] == "without_skill" and r["result"]["time_seconds"] > 0]

ws_pr_mean = statistics.mean(ws_pass) if ws_pass else 0
wos_pr_mean = statistics.mean(wos_pass) if wos_pass else 0

benchmark = {
    "metadata": {
        "skill_name": "expert-reviewer",
        "skill_path": str(SKILL_PATH),
        "executor_model": "glm-5.2 (Sisyphus-Junior, category=unspecified-high/quick)",
        "analyzer_model": "glm-5.2 (main session, heuristic grader)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evals_run": [1, 2, 3, 4, 5],
        "runs_per_configuration": 1,
    },
    "runs": runs,
    "run_summary": {
        "with_skill": {
            "pass_rate": stats(ws_pass),
            "time_seconds": stats(ws_time) if ws_time else {"mean": 0, "stddev": 0, "min": 0, "max": 0},
            "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0},
        },
        "without_skill": {
            "pass_rate": stats(wos_pass),
            "time_seconds": stats(wos_time) if wos_time else {"mean": 0, "stddev": 0, "min": 0, "max": 0},
            "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0},
        },
        "delta": {
            "pass_rate": f"+{ws_pr_mean - wos_pr_mean:.2f}",
            "time_seconds": "+0",
            "tokens": "+0",
        },
    },
    "notes": [
        f"Skill improves pass rate by {ws_pr_mean - wos_pr_mean:+.1%} on average ({ws_pr_mean:.1%} vs {wos_pr_mean:.1%})",
        "Iteration-2 changes: references slimmed from 1318 → 641 lines (-51%), total skill from 2392 → 1493 lines (-38%)",
        "Added eval 5 (English serverless architecture input) to test cross-language generalization",
        "n=1 per cell. Statistics are descriptive, not inferential.",
    ],
}

out_path = WORKSPACE / "benchmark.json"
with open(out_path, "w") as f:
    json.dump(benchmark, f, indent=2, ensure_ascii=False)

print(f"\nWrote: {out_path}")
print(f"\n=== SUMMARY ===")
print(f"with_skill pass_rate:    {ws_pr_mean:.1%} (range {min(ws_pass):.1%}–{max(ws_pass):.1%})")
print(f"without_skill pass_rate: {wos_pr_mean:.1%} (range {min(wos_pass):.1%}–{max(wos_pass):.1%})")
print(f"Delta: {ws_pr_mean - wos_pr_mean:+.1%}")
