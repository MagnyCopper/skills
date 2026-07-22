#!/usr/bin/env python3
"""Grade all runs in iteration-2 against assertions. Output: grading.json per run."""
import json
import re
from pathlib import Path

WORKSPACE = Path("/Users/han/Projects/skills/expert-reviewer-workspace/iteration-2")

def load_assertions(eval_dir):
    with open(eval_dir / "eval_metadata.json") as f:
        return json.load(f)["assertions"]

def load_report(eval_dir, config):
    p = eval_dir / config / "outputs" / "review-report.md"
    if not p.exists():
        return ""
    return p.read_text()

def grade_assertion(text, assertion):
    t = text.lower()
    a = assertion.lower()
    
    if "元信息" in assertion:
        passed = ("元信息" in t) or ("metadata" in t) or ("评审对象类型" in t) or ("| 字段 |" in t and ("对象" in t or "日期" in t))
        return passed, "Metadata table presence check"
    
    if "critical" in a and "至少" in a:
        passed = ("critical" in t) or ("🔴" in t) or ("致命" in t) or ("p0" in t)
        return passed, "Critical section presence check"
    
    if "红队" in assertion and "建设性" in assertion:
        has_red = ("🟥" in t) or ("红队" in t) or ("red team" in t)
        has_con = ("🟩" in t) or ("建设性" in t) or ("constructive" in t)
        passed = has_red and has_con
        return passed, f"Red team={has_red}, Constructive={has_con}"
    
    if "原文引用" in assertion:
        passed = (">" in text) or ("原文" in t) or ("引用" in t) or ("用户" in t and "原话" in t)
        return passed, "Blockquote/原文 presence"
    
    if "方法论依据" in assertion and "出处" in assertion:
        passed = ("方法论" in t) or ("references/" in t) or ("出处" in t)
        return passed, "Methodology reference check"
    
    if "显式引用至少" in assertion and "方法论" in assertion:
        methods = ["atam", "toulmin", "walton", "paul-elder", "pbr", "perspective", "adr", 
                   "casp", "cochrane", "grade", "prisma", "cognitive dimensions", "pyramid",
                   "mece", "sequoia", "reference class", "pre-mortem", "premortem",
                   "key assumptions", "ach", "sift", "red team", "diátaxis", "diataxis",
                   "jensen", "noise", "well-architected", "devils", "devil's"]
        found = [m for m in methods if m in t]
        passed = len(found) >= 2
        return passed, f"Found methods: {found[:5]}"
    
    if "paul-elder" in a or "8 要素" in assertion:
        passed = ("paul-elder" in t) or ("8 要素" in t) or ("8 elements" in t)
        return passed, "Paul-Elder mention"
    
    if "5 视角" in assertion or ("视角" in assertion and "覆盖" in assertion):
        passed = ("5 视角" in t) or ("视角覆盖" in t) or ("实现者" in t and "维护者" in t and "反对者" in t)
        return passed, "5 perspectives coverage"
    
    if "toulmin" in a:
        passed = ("toulmin" in t) or ("claim" in t and "warrant" in t)
        return passed, "Toulmin presence"
    
    if "pre-mortem" in a or "premortem" in a:
        passed = ("pre-mortem" in t) or ("premortem" in t) or ("前置尸检" in t)
        return passed, "Pre-mortem presence"
    
    if "key assumptions" in a:
        passed = ("key assumptions" in t) or ("关键假设" in t)
        return passed, "Key Assumptions Check"
    
    if "评审者自评" in assertion:
        passed = ("自评" in t) or ("self-assessment" in t) or ("self-evaluation" in t) or ("未覆盖" in t and "偏倚" in t)
        return passed, "Self-evaluation section"
    
    # Issue-specific keyword checks
    keywords_map = {
        "kafka": ["kafka"],
        "容量": ["容量", "qps", "11"],
        "回滚": ["回滚", "rollback", "saga", "tcc"],
        "熔断": ["熔断", "circuit", "sentinel", "hystrix"],
        "监控": ["监控", "observability", "可观测"],
        "缓存": ["缓存", "cache", "redis"],
        "dlq": ["dlq", "dead letter", "死信"],
        "幂等": ["幂等", "idempot"],
        "冷启动": ["cold start", "冷启动"],
        "成本": ["成本", "cost", "费用"],
        "灾难恢复": ["disaster", "灾难恢复", "multi-region", "多区域", "dr"],
        "顺序": ["ordering", "顺序", "fifo"],
        "限流": ["rate limit", "throttle", "限流"],
        "why now": ["why now", "时机", "为什么现在"],
        "competition": ["竞争", "competit", "resume", "jobscan", "teal", "rezi"],
        "市场": ["市场", "tam", "sam", "som"],
        "单位经济": ["单位经济", "ltv", "cac", "churn"],
        "pmf": ["pmf", "product-market", "产品市场"],
        "合规": ["合规", "compliance", "隐私", "privacy"],
        "定价": ["定价", "pricing"],
        "因果": ["因果", "causal", "自评"],
        "盲法": ["盲法", "blind", "placebo"],
        "pre-registration": ["pre-registration", "预注册", "preregister"],
        "power": ["power", "样本量", "underpower"],
        "多重比较": ["多重比较", "multiple comparison", "p-hack", "harking"],
        "开放数据": ["开放数据", "open data", "复现", "reproduc"],
        "心理测量": ["心理测量", "psychometric", "cronbach"],
        "过度推广": ["过度推广", "generaliz", "外部效度"],
        "8 周": ["8 周", "8 week", "随访", "follow-up", "novelty"],
        "baseline": ["baseline", "依据", "工单"],
        "数据隐私": ["隐私", "privacy", "openai", "gdpr", "pii"],
        "失败退化": ["失败", "退化", "fallback", "兜底"],
        "3 工程师": ["3 工程师", "reference class", "planning fallacy", "乐观偏差"],
        "真正痛点": ["真痛点", "痛点", "jtbd", "ux"],
        "兜底": ["兜底", "human", "接管", "人工"],
        "机会成本": ["机会成本", "转型", "裁员"],
        "私有化": ["私有化", "azure", "开源", "llama", "qwen"],
    }
    
    for key, kws in keywords_map.items():
        if key in a:
            found = [kw for kw in kws if kw in t]
            passed = len(found) > 0
            return passed, f"Keywords found: {found[:3]}"
    
    # Default: check if assertion keywords appear
    keywords = re.findall(r'[\w\u4e00-\u9fff]+', assertion)[:3]
    found = [k for k in keywords if k.lower() in t]
    passed = len(found) >= 1
    return passed, f"Default keyword check: {found}"


def grade_run(eval_dir, config):
    assertions = load_assertions(eval_dir)
    text = load_report(eval_dir, config)
    
    if not text:
        return {
            "expectations": [{"text": a, "passed": False, "evidence": "Report file not found"} for a in assertions],
            "summary": {"passed": 0, "failed": len(assertions), "total": len(assertions), "pass_rate": 0.0}
        }
    
    results = []
    passed_count = 0
    for a in assertions:
        passed, evidence = grade_assertion(text, a)
        results.append({"text": a, "passed": passed, "evidence": evidence})
        if passed:
            passed_count += 1
    
    return {
        "expectations": results,
        "summary": {
            "passed": passed_count,
            "failed": len(assertions) - passed_count,
            "total": len(assertions),
            "pass_rate": passed_count / len(assertions) if assertions else 0.0
        }
    }


def main():
    eval_dirs = sorted([d for d in WORKSPACE.iterdir() if d.is_dir() and d.name.startswith("eval-")])
    all_results = []
    
    for eval_dir in eval_dirs:
        for config in ["with_skill", "without_skill"]:
            print(f"Grading: {eval_dir.name} / {config}")
            result = grade_run(eval_dir, config)
            
            out_path = eval_dir / config / "grading.json"
            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            pr = result["summary"]["pass_rate"]
            print(f"  → pass_rate: {pr:.1%} ({result['summary']['passed']}/{result['summary']['total']})")
            all_results.append({
                "eval_name": eval_dir.name.replace("eval-", ""),
                "config": config,
                "pass_rate": pr,
                "passed": result["summary"]["passed"],
                "total": result["summary"]["total"],
            })
    
    print("\n=== SUMMARY ===")
    print(f"{'Eval':<55} {'with_skill':<15} {'without_skill':<15}")
    print("-" * 85)
    eval_names = sorted(set(r["eval_name"] for r in all_results))
    for ename in eval_names:
        ws = next((r for r in all_results if r["eval_name"] == ename and r["config"] == "with_skill"), None)
        wos = next((r for r in all_results if r["eval_name"] == ename and r["config"] == "without_skill"), None)
        ws_str = f"{ws['pass_rate']:.1%} ({ws['passed']}/{ws['total']})" if ws else "N/A"
        wos_str = f"{wos['pass_rate']:.1%} ({wos['passed']}/{wos['total']})" if wos else "N/A"
        print(f"{ename:<55} {ws_str:<15} {wos_str:<15}")
    
    ws_rates = [r["pass_rate"] for r in all_results if r["config"] == "with_skill"]
    wos_rates = [r["pass_rate"] for r in all_results if r["config"] == "without_skill"]
    if ws_rates and wos_rates:
        ws_mean = sum(ws_rates)/len(ws_rates)
        wos_mean = sum(wos_rates)/len(wos_rates)
        print(f"\nMean with_skill: {ws_mean:.1%}")
        print(f"Mean without_skill: {wos_mean:.1%}")
        print(f"Delta: +{ws_mean - wos_mean:.1%}")


if __name__ == "__main__":
    main()
