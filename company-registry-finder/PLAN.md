# company-registry-finder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `company-registry-finder` skill that, given a company's informal name + optional country/industry hints, returns its current registered legal name, jurisdiction, address, and registration number — resolving rename/acquisition chains to the surviving entity.

**Architecture:** Single-company-input → JSON-output skill mirroring sibling `company-domain-finder`. 5-stage pipeline (PARSE → DISCOVER → CORROBORATE → VERIFY → SCORE). TDD + hill-climbing against a 72-row frozen test set (`tests/companyName.txt`), 3-tier scoring (name +1, regnum +1, empty=N/A), target ≥95% of achievable max (139).

**Tech Stack:** Markdown (skill definition), Python 3 (`tests/eval.py`), bash (`tests/run-eval.sh`). No build system. No external deps for eval (stdlib only).

**Spec reference:** `company-registry-finder/DESIGN.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `company-registry-finder/SKILL.md` | Trigger description, workflow, hard rules — the entry point the skill loader reads |
| `company-registry-finder/prompt.md` | Full technical contract: pipeline, schema, examples, MUST/MUST NOT rules |
| `company-registry-finder/assets/templates/output-template.json` | Canonical JSON skeleton agents copy and fill |
| `company-registry-finder/references/registry-sources.md` | 16-country official + 3rd-party source table |
| `company-registry-finder/references/number-formats.md` | Per-jurisdiction reg-number format + checksum rules |
| `company-registry-finder/references/disambiguation-rules.md` | Rename/acquisition patterns + identifier-stability rules |
| `company-registry-finder/references/name-normalization.md` | Case-fold, CJK width, punctuation, jurisdiction-prefix stripping |
| `company-registry-finder/tests/companyName.txt` | Frozen 72-row test set (copy of temp/companyName.txt) |
| `company-registry-finder/tests/eval.py` | Three-tier scorer: reads JSON outputs + ground truth, prints score breakdown |
| `company-registry-finder/tests/run-eval.sh` | Orchestrator: for each row → invoke skill → eval → report |

Runtime output: `results/<YYYYMMDD>/company-registry-finder/<row-id>.json` (e.g. `001.json` ... `072.json`).

---

## Phase 1: Parallel Scaffolding (6 independent tasks — dispatch in parallel)

> **Dispatch note:** Tasks 1–6 have NO interdependencies. Fire all 6 in parallel via `task(category=..., load_skills=[...], run_in_background=true)`.

---

### Task 1: `tests/eval.py` — the scorer (RED gate)

**Files:**
- Create: `company-registry-finder/tests/eval.py`
- Create: `company-registry-finder/tests/companyName.txt` (copy of `temp/companyName.txt`)

**Category:** `quick`

- [ ] **Step 1.1: Copy the frozen test set**

```bash
cp temp/companyName.txt company-registry-finder/tests/companyName.txt
diff temp/companyName.txt company-registry-finder/tests/companyName.txt && echo OK
```

Expected: `OK` (files identical)

- [ ] **Step 1.2: Write `eval.py` with stdlib only**

```python
#!/usr/bin/env python3
"""Three-tier scorer for company-registry-finder.

Reads:
  - tests/companyName.txt        (ground truth: raw_name<TAB>std_name<TAB>regnum)
  - results/<YYYYMMDD>/company-registry-finder/<id>.json  (predictions, id = 3-digit row number)

Score:
  - name_match    = 1 if normalize(pred.standard_name) == normalize(gt_std_name) else 0
  - regnum_match  = None if gt_regnum empty (skip), else 1/0 by normalized equality
  - total = sum(name_match) + sum(regnum_match where not None)

Normalization (must match PARSE-stage normalize in the skill):
  - lowercase
  - NFC unicode normalize
  - strip leading/trailing whitespace
  - collapse internal whitespace to single space
  - remove all of: , . - _ / ( ) 【 】 ［ ］ 「 」 ' " & ; :
  - fold full-width ASCII (ff) to half-width (ASCII)
  - strip jurisdiction prefixes/suffixes for regnum:
      "München HRB 126492" -> "hrb 126492"
      "Stendal HRB 6090"   -> "hrb 6090"
      "CHE-123.456.789"    -> "123456789"
      "0401.574.852"       -> "0401574852"
      "U24203UP2024PTC202623" -> lowercased unchanged
  - strip leading zeros ONLY for pure-numeric non-checksum numbers (configurable)
"""
import json
import sys
import unicodedata
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_SET = Path(__file__).resolve().parent / "companyName.txt"
RESULTS_DIR = REPO_ROOT / "results"

PUNCT_RE = re.compile(r"[,\.\-/_\(\)\[\]【】［］「」'\"&;:·•]")
WS_RE = re.compile(r"\s+")

# Known jurisdiction-prefix patterns to strip from registration numbers
JURIS_PREFIX_RE = re.compile(
    r"\b(?:Amtsgericht\s+\w+|München|Stendal|Jena|Berlin|Hamburg|Frankfurt|HRB|HRA|GnR|VR|PR|Fa)\b",
    re.IGNORECASE,
)
CHE_PREFIX_RE = re.compile(r"^CHE[-.\s]*", re.IGNORECASE)
DOTDASH_RE = re.compile(r"[.\-]")

def normalize_name(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFC", s)
    # fold full-width to half-width
    s = s.translate(str.maketrans({i: chr(i - 0xFEE0) for i in range(0xFF01, 0xFF5E)})).translate(str.maketrans({0x3000: " "}))
    s = PUNCT_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip().lower()
    return s

def normalize_regnum(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFC", s)
    s = s.translate(str.maketrans({i: chr(i - 0xFEE0) for i in range(0xFF01, 0xFF5E)})).translate(str.maketrans({0x3000: " "}))
    s = JURIS_PREFIX_RE.sub(" ", s)
    s = CHE_PREFIX_RE.sub("", s)
    # Keep dots/dashes for BE format "0401.574.852"? No — strip for robustness
    s = DOTDASH_RE.sub("", s)
    s = WS_RE.sub("", s).strip().lower()
    return s

def load_ground_truth():
    rows = []
    with open(TEST_SET, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            raw_name = parts[0]
            std_name = parts[1]
            regnum = parts[2] if len(parts) >= 3 else ""
            rows.append({
                "row": i,
                "id": f"{i:03d}",
                "raw_name": raw_name,
                "gt_std_name": std_name,
                "gt_regnum": regnum,
            })
    return rows

def load_prediction(row_id: str, run_date: str):
    p = RESULTS_DIR / run_date / "company-registry-finder" / f"{row_id}.json"
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def score(run_date: str):
    rows = load_ground_truth()
    total_name = 0
    total_regnum_possible = 0
    total_regnum_scored = 0
    per_row = []
    for r in rows:
        pred = load_prediction(r["id"], run_date)
        if pred is None:
            per_row.append({**r, "pred_name": None, "pred_regnum": None,
                            "name_match": 0, "regnum_match": None, "reason": "missing"})
            continue
        try:
            pred_name = pred["result"]["standard_name"]
            pred_regnum = pred["result"]["registration_number"] or ""
        except (KeyError, TypeError):
            per_row.append({**r, "pred_name": None, "pred_regnum": None,
                            "name_match": 0, "regnum_match": None, "reason": "schema_error"})
            continue

        name_match = 1 if normalize_name(pred_name) == normalize_name(r["gt_std_name"]) else 0
        total_name += name_match

        if r["gt_regnum"].strip() == "":
            regnum_match = None  # N/A
        else:
            total_regnum_possible += 1
            regnum_match = 1 if normalize_regnum(pred_regnum) == normalize_regnum(r["gt_regnum"]) else 0
            total_regnum_scored += regnum_match

        per_row.append({**r, "pred_name": pred_name, "pred_regnum": pred_regnum,
                        "name_match": name_match, "regnum_match": regnum_match, "reason": "ok"})

    name_acc = total_name / len(rows)
    regnum_acc = total_regnum_scored / total_regnum_possible if total_regnum_possible else 0.0
    total = total_name + total_regnum_scored
    achievable = len(rows) + total_regnum_possible

    return {
        "run_date": run_date,
        "total_rows": len(rows),
        "name_matches": total_name,
        "name_accuracy": round(name_acc, 4),
        "regnum_possible": total_regnum_possible,
        "regnum_matches": total_regnum_scored,
        "regnum_accuracy_on_nonempty": round(regnum_acc, 4),
        "total_score": total,
        "achievable_max": achievable,
        "pct_of_max": round(total / achievable * 100, 2) if achievable else 0.0,
        "per_row": per_row,
    }

def main():
    if len(sys.argv) < 2:
        print("usage: eval.py <YYYYMMDD> [--verbose] [--failures-only]", file=sys.stderr)
        sys.exit(2)
    run_date = sys.argv[1]
    verbose = "--verbose" in sys.argv
    failures_only = "--failures-only" in sys.argv

    result = score(run_date)

    print(f"=== Eval run: {result['run_date']} ===")
    print(f"Rows: {result['total_rows']}")
    print(f"Name matches:    {result['name_matches']}/{result['total_rows']} ({result['name_accuracy']*100:.2f}%)")
    print(f"Regnum matches:  {result['regnum_matches']}/{result['regnum_possible']} ({result['regnum_accuracy_on_nonempty']*100:.2f}%)")
    print(f"TOTAL: {result['total_score']} / {result['achievable_max']}  ({result['pct_of_max']}%)")

    if verbose or failures_only:
        print("\n--- Per-row ---")
        for r in result["per_row"]:
            if failures_only and r["name_match"] == 1 and (r["regnum_match"] in (1, None)):
                continue
            regnum_str = "N/A" if r["regnum_match"] is None else r["regnum_match"]
            print(f"  [{r['id']}] name={r['name_match']} regnum={regnum_str}  reason={r['reason']}")
            print(f"        raw:      {r['raw_name'][:60]}")
            print(f"        gt_name:  {r['gt_std_name'][:60]}")
            if r.get("pred_name"):
                print(f"        pred:     {r['pred_name'][:60]}")
            if r["gt_regnum"]:
                print(f"        gt_reg:   {r['gt_regnum']}")
                if r.get("pred_regnum"):
                    print(f"        pred_reg: {r['pred_regnum']}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 1.3: Verify the harness runs and reports 0 (no predictions exist yet)**

Run: `python3 company-registry-finder/tests/eval.py 20260617`
Expected: prints header, all zeros, `0 / 139  (0.0%)`. This is the **RED** state confirming the harness works.

- [ ] **Step 1.4: Commit**

```bash
git add company-registry-finder/tests/
git commit -m "Add eval.py harness + frozen test set for company-registry-finder"
```

---

### Task 2: `assets/templates/output-template.json`

**Files:**
- Create: `company-registry-finder/assets/templates/output-template.json`

**Category:** `quick`

- [ ] **Step 2.1: Write the template**

```json
{
  "id": "",
  "input": {
    "raw_name": "",
    "country_hint": null,
    "industry_hint": null,
    "parsed_hints": {
      "detected_country": null,
      "detected_script": null,
      "detected_language_hints": []
    }
  },
  "result": {
    "standard_name": "",
    "registered_jurisdiction": "",
    "registered_address": "",
    "registration_number": "",
    "registration_number_type": "",
    "entity_status": "",
    "former_names": [],
    "successor_entity": null
  },
  "verification": {
    "confidence_level": "",
    "relationship_to_target": "",
    "name_match_evidence": "",
    "regnum_match_evidence": "",
    "address_match_evidence": "",
    "contradictions": []
  },
  "evidence_sources": [
    {
      "url": "",
      "locator": "",
      "snippet": "",
      "kind": "",
      "accessed_at": ""
    }
  ],
  "search_methods": [],
  "search_queries_used": [],
  "timestamp": ""
}
```

- [ ] **Step 2.2: Validate JSON parses**

Run: `python3 -c "import json; json.load(open('company-registry-finder/assets/templates/output-template.json'))"`
Expected: no output, exit 0.

- [ ] **Step 2.3: Commit**

```bash
git add company-registry-finder/assets/templates/output-template.json
git commit -m "Add output-template.json skeleton for company-registry-finder"
```

---

### Task 3: `references/registry-sources.md`

**Files:**
- Create: `company-registry-finder/references/registry-sources.md`

**Category:** `writing`

**Source material:** Librarian output from `bg_8c6a5ec6` (the 16-country table). Pass the FULL table content to the writing agent.

- [ ] **Step 3.1: Write the markdown reference**

Content MUST include the full 16-country table with columns: Country | Official registry (EN + local) | Public lookup URL | Free public search? | Best 3rd-party | Anti-bot notes. Plus a separate "OpenCorporates API patterns" subsection.

- [ ] **Step 3.2: Verify all root URLs return 200 (manual spot check)**

Run for each URL root: `curl -sI <url> | head -1`
Fix any 404s before committing.

- [ ] **Step 3.3: Commit**

```bash
git add company-registry-finder/references/registry-sources.md
git commit -m "Add 16-country registry-sources.md reference"
```

---

### Task 4: `references/number-formats.md`

**Files:**
- Create: `company-registry-finder/references/number-formats.md`

**Category:** `writing`

- [ ] **Step 4.1: Write per-jurisdiction format + checksum reference**

Content MUST cover for each of 16 countries:
- Format regex or pattern
- Length
- Checksum algorithm (if any — JP corporate number, BE mod97, KR BRN, TW 統一編號)
- Example from the test set
- Validation pseudocode

- [ ] **Step 4.2: Commit**

```bash
git add company-registry-finder/references/number-formats.md
git commit -m "Add number-formats.md with per-jurisdiction reg-number rules"
```

---

### Task 5: `references/disambiguation-rules.md`

**Files:**
- Create: `company-registry-finder/references/disambiguation-rules.md`

**Category:** `writing`

**Source material:** Librarian output from `bg_85d8acce`. Pass the FULL content.

- [ ] **Step 5.1: Write the rename/acquisition playbook**

Content MUST cover:
- Identifier-stability rules per jurisdiction (JP 法人番号, DE file number, UK company number — all stable across renames)
- Rename resolution workflow (search old name → registry → previous_names field → current name)
- Acquisition resolution workflow (absorbed → return survivor; subsidiary → return subsidiary)
- Test-set-specific known cases table:
  - Hitachi Metals → 株式会社プロテリアル (3010401038783)
  - Neo Performance Materials → CITIC ENVIROTECH LTD (Canadian registry)
  - Alfa Aesar → THERMO FISHER SCIENTIFIC CHEMICALS INC. (232543453)
  - Sigma-Aldrich → multiple entities (corporation vs inc)
  - Navitas Semiconductor → Navitas Semiconductor Corporation
  - Soitec not Saint-Gobain (different entities)
- Query templates for each pattern

- [ ] **Step 5.2: Commit**

```bash
git add company-registry-finder/references/disambiguation-rules.md
git commit -m "Add disambiguation-rules.md with rename/acquisition playbook"
```

---

### Task 6: `references/name-normalization.md`

**Files:**
- Create: `company-registry-finder/references/name-normalization.md`

**Category:** `writing`

- [ ] **Step 6.1: Write the normalization spec**

Content MUST be a 1-to-1 mirror of the `normalize_name()` and `normalize_regnum()` functions in `tests/eval.py` (Task 1). This is the CONTRACT that the skill's PARSE stage must implement at runtime.

- [ ] **Step 6.2: Commit**

```bash
git add company-registry-finder/references/name-normalization.md
git commit -m "Add name-normalization.md spec mirroring eval.py"
```

---

## Phase 2: Baseline Skill (GREEN — depends on Phase 1)

> **Dispatch note:** Sequential. Phase 1 must be merged before starting.

---

### Task 7: Write minimal `SKILL.md` + `prompt.md` (GREEN baseline)

**Files:**
- Create: `company-registry-finder/SKILL.md`
- Create: `company-registry-finder/prompt.md`

**Category:** `writing` with `load_skills=["writing-skills"]`

- [ ] **Step 7.1: Write `SKILL.md`**

Frontmatter (YAML):
```yaml
---
name: company-registry-finder
description: Use when looking up a company's official registered legal name, registered jurisdiction/address, and registration number. Resolves renames and acquisitions to the current surviving entity. Coverage: JP, US (multi-state), UK, DE, FR, KR, HK, SG, TW, IN, CA, BE, NL, CH, LU, KZ.
---
```

Body MUST include (mirroring `company-domain-finder/SKILL.md` style):
1. **最高优先级：文件保存规则** — `mkdir -p results/<YYYYMMDD>/company-registry-finder/`, write `<id>.json` per row
2. **强制规则：法人主体归属验证** — only registry-confirmed candidates advance
3. **执行步骤** — the 5-stage pipeline (PARSE → DISCOVER → CORROBORATE → VERIFY → SCORE) with one paragraph each, referencing the `references/*.md` files
4. **改名/收购特别规则** — must resolve to current surviving entity; reference `disambiguation-rules.md`
5. **资源参考** — links to all `references/*.md` and `assets/templates/output-template.json`
6. Point to `prompt.md` as the technical contract

- [ ] **Step 7.2: Write `prompt.md`**

The full technical contract. MUST include:
1. Input schema (3 fields: id, raw_name, country_hint, industry_hint)
2. Output schema (copy from `output-template.json`, document every field's allowed values)
3. Pipeline detail per stage with concrete examples
4. `confidence_level` enum table (A/B/C/D definitions)
5. `relationship_to_target` enum (10 values)
6. `evidence_sources[].kind` enum (official_registry, third_party, news, wikipedia, regulatory_filing)
7. **MUST DO** rules (≥10): always check entity_status, always walk rename chain, require ≥2 independent sources, use country_hint for registry routing, etc.
8. **MUST NOT DO** rules (≥10): never return dissolved entity without survivor, never return brand as legal entity, never use Wikipedia as sole source for confidence ≥B, never confuse subsidiary with parent, etc.
9. Worked example 1: simple case (row 1: Dowa Holdings → 中國同和控股集團有限公司)
10. Worked example 2: rename case (row 52: Hitachi Metals → 株式会社プロテリアル, JP 3010401038783)

- [ ] **Step 7.3: Self-review**

Verify:
- All `references/*.md` files are cited from SKILL.md
- Schema in prompt.md matches output-template.json EXACTLY (no field drift)
- At least 2 worked examples present

- [ ] **Step 7.4: Commit**

```bash
git add company-registry-finder/SKILL.md company-registry-finder/prompt.md
git commit -m "Add SKILL.md + prompt.md baseline for company-registry-finder"
```

---

### Task 8: Run baseline eval (record baseline score)

**Files:** None (runs the skill against the test set)

**Owner:** Sisyphus (orchestrator — not delegatable, requires live tool use)

- [ ] **Step 8.1: Pick a representative subset**

Don't run all 72 rows yet. Pick 12 diverse rows covering: simple direct match (1), rename case (52), acquisition case (20), ambiguous (48), each major jurisdiction (JP/US/UK/DE/FR/KR/HK/SG/TW/IN/CA/BE).

Suggested subset: rows 1, 2, 6, 9, 17, 20, 27, 33, 39, 47, 52, 55.

- [ ] **Step 8.2: For each subset row, manually invoke the skill**

Using the skill's instructions, execute the pipeline and write the JSON output to `results/<YYYYMMDD>/company-registry-finder/<id>.json`.

- [ ] **Step 8.3: Run eval on the subset**

```bash
python3 company-registry-finder/tests/eval.py <YYYYMMDD> --verbose
```

- [ ] **Step 8.4: Record baseline**

Write to `company-registry-finder/HILLCLIMB.md`:
```
## Baseline (12-row subset)
Total: X / ~24 (Y%)
Name matches: X/12
Regnum matches: X/(non-empty count)
Failures: [list row IDs]
```

- [ ] **Step 8.5: Commit**

```bash
git add company-registry-finder/HILLCLIMB.md
git commit -m "Record baseline eval for company-registry-finder (12-row subset)"
```

---

## Phase 3: Hill-Climbing Iterations (8 climbs — sequential, eval-driven)

> **Protocol per climb:** Each climb is ONE targeted improvement. After modification, re-run eval on the SAME 12-row subset. **Keep change only if score strictly increases.** If score regresses or stays flat, revert.
>
> After all 8 climbs (or stop condition), re-run eval on FULL 72-row test set for final score.

Each climb is documented in `company-registry-finder/HILLCLIMB.md` with:
- Hypothesis (what improvement, expected effect)
- Diff summary (which file(s) modified, what rule added)
- Before/after score on subset
- Decision: KEEP / REVERT
- If REVERT: which commit to roll back to

---

### Climb 1: PARSE-stage country-hint extraction

**Hypothesis:** Many rows embed country in parentheses (`（日本）`, `(加拿大)`, `(美国)`). Extracting this hint lets DISCOVER hit the right jurisdiction-specific registry first.

**Modify:** `prompt.md` §PARSE — add explicit country-keyword table:
```
日本/Japan/JP/（日本） → JP
美国/USA/US/United States/（美国） → US
德国/Germany/DE/（德国） → DE
英国/UK/（英国） → GB
法国/France/（法国） → FR
韩国/Korea/（韩国） → KR
香港/Hong Kong/HK → HK
新加坡/Singapore/SG → SG
台湾/Taiwan/TW → TW
印度/India/IN → IN
加拿大/Canada/CA → CA
比利时/Belgium/BE → BE
荷兰/Netherlands/NL → NL
瑞士/Switzerland/CH → CH
哈萨克斯坦/Kazakhstan/KZ → KZ
```

**Expected effect:** +2–4 name matches (better registry routing → fewer wrong-jurisdiction candidates).

- [ ] **Step C1.1:** Modify prompt.md PARSE section
- [ ] **Step C1.2:** Re-run subset eval
- [ ] **Step C1.3:** Decision + commit/revert
- [ ] **Step C1.4:** Append entry to HILLCLIMB.md

---

### Climb 2: Per-country official registry URLs in DISCOVER

**Hypothesis:** Adding the exact registry URL per jurisdiction to DISCOVER (instead of relying on generic web search) directly hits the authoritative source.

**Modify:** `prompt.md` §DISCOVER — embed the per-country URL table from `references/registry-sources.md` inline (or add a "DISCOVER routing table" section that explicitly says "if country_hint=X, hit URL=Y first").

**Expected effect:** +2–3 regnum matches (official registry is the only source that reliably exposes the registration number).

- [ ] Steps C2.1–C2.4: same protocol as Climb 1.

---

### Climb 3: Rename/acquisition rules in VERIFY

**Hypothesis:** Currently misses Hitachi Metals→プロテリアル, Neo Performance→CITIC, Alfa Aesar→Thermo Fisher. Adding explicit rules will resolve these.

**Modify:** `prompt.md` §VERIFY — add subsection "Rename/acquisition resolution" with the workflow:
1. If registry record has `former_names` → walk to current
2. If Wikipedia first paragraph contains "formerly" / "renamed" / "acquired by" → treat as rename hint, search for current entity
3. Cross-check via `references/disambiguation-rules.md`

Plus inline-examples for the 3 known cases.

**Expected effect:** +3 name matches + 3 regnum matches (resolves rows 8, 20, 52).

- [ ] Steps C3.1–C3.4.

---

### Climb 4: Name normalization (case/punctuation/CJK width)

**Hypothesis:** Some near-misses are due to case differences (`AXT, INC.` vs `AXT, INC`), CJK full-width vs half-width, trailing punctuation. Applying the same `normalize_name()` rules the eval uses.

**Modify:** `prompt.md` §PARSE and §SCORE — reference `references/name-normalization.md` and require the agent to apply normalization before comparing candidate names.

**Expected effect:** +1–2 name matches.

- [ ] Steps C4.1–C4.4.

---

### Climb 5: Disambiguation for multi-entity cases

**Hypothesis:** Sigma-Aldrich has multiple entities (Corporation vs Inc), Navitas Semiconductor (Corp vs the bare name), etc. Need disambiguation logic.

**Modify:** `prompt.md` §CORROBORATE — add rule:
- If candidate search returns ≥2 same-name entities in the same jurisdiction, prefer the one matching `industry_hint` and `country_hint`
- If still tied, prefer the one with longer operating history (earliest registration date)
- Document the choice in `verification.contradictions`

**Expected effect:** +1–2 name matches (rows 28, 48, 21).

- [ ] Steps C5.1–C5.4.

---

### Climb 6: Multi-language query expansion

**Hypothesis:** For JP/KR/CJK companies, querying in both English and local script finds better results (e.g., `Hitachi Metals` English page may not show the rename, but `日立金属` or `プロテリアル` will).

**Modify:** `prompt.md` §DISCOVER — add rule: "For JP/KR/CN/TW targets, run queries in BOTH English and local script. Use Wikipedia's lang-link to bridge."

**Expected effect:** +1–2 matches on JP rows.

- [ ] Steps C6.1–C6.4.

---

### Climb 7: Registration-number checksum validation as contradiction detector

**Hypothesis:** Some predictions have a syntactically invalid registration number (wrong checksum). Detecting this in VERIFY can trigger a retry.

**Modify:** `prompt.md` §VERIFY — add rule: "Validate registration number against `references/number-formats.md` checksum rules. If invalid, demote confidence to D and retry DISCOVER."

**Expected effect:** +1–2 regnum matches (catches hallucinated numbers).

- [ ] Steps C7.1–C7.4.

---

### Climb 8: Evidence-source diversity requirement

**Hypothesis:** Some predictions rely on a single source, increasing wrong-answer risk. Requiring ≥2 independent source kinds for confidence ≥B improves precision.

**Modify:** `prompt.md` §SCORE — tighten rule: "confidence_level=B requires evidence from ≥2 different `kind` values; confidence_level=A requires ≥1 `official_registry` source."

**Expected effect:** Higher precision, possibly slight recall drop on hard cases. Net expected +1–2.

- [ ] Steps C8.1–C8.4.

---

### Stop conditions

After each climb, check:
- ✅ 8 climbs completed → STOP
- ✅ Subset score ≥ 95% of subset achievable max → STOP, run full eval
- ✅ 2 consecutive climbs with no improvement → STOP, run full eval

---

## Phase 4: Final Acceptance

### Task 9: Full 72-row eval

**Owner:** Sisyphus

- [ ] **Step 9.1:** For all 72 rows, invoke the skill and write JSON outputs
- [ ] **Step 9.2:** Run full eval
```bash
python3 company-registry-finder/tests/eval.py <YYYYMMDD> --verbose > results/<YYYYMMDD>/company-registry-finder/eval-report.txt
```
- [ ] **Step 9.3:** Verify acceptance criteria
  - `total_score ≥ 132` (95% of 139)
  - If short, identify failing rows and document in HILLCLIMB.md as known-limitations

- [ ] **Step 9.4:** Commit
```bash
git add results/<YYYYMMDD>/ company-registry-finder/HILLCLIMB.md
git commit -m "Final eval: company-registry-finder reaches X% (target 95%)"
```

---

### Task 10: Manual spot-check + worked-example polish

- [ ] **Step 10.1:** Pick 5 random rows; manually verify JSON correctness (paths valid, evidence URLs live, schema matches template)
- [ ] **Step 10.2:** Polish `prompt.md` worked examples based on actual outputs from this run
- [ ] **Step 10.3:** Final commit

---

## Self-Review (post-write)

**Spec coverage check:**
- §1 Problem statement → Task 7 (SKILL.md), Task 5 (disambiguation), Climb 3 ✓
- §2 I/O contract → Task 2 (template), Task 7 (prompt) ✓
- §3 Pipeline → Task 7 (prompt), Climbs 1-8 ✓
- §4 References → Tasks 3-6 ✓
- §5 Eval → Tasks 1, 8, 9 ✓
- §6 Directory layout → all tasks ✓
- §7 Out of scope → Task 7 (documented in prompt) ✓
- §8 Risks → addressed in Climb strategies ✓
- §9 Acceptance → Task 9 ✓

**No placeholders:** every step has concrete code/commands.

**Type consistency:** `normalize_name` / `normalize_regnum` defined in Task 1, referenced in Climb 4 and `name-normalization.md` (Task 6). `confidence_level`, `relationship_to_target`, `evidence_sources[].kind` enums consistent across Task 2, Task 7, Climbs 7-8.

---

## Execution Handoff

Plan saved to `company-registry-finder/PLAN.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task with review between tasks. Fast iteration, clear boundaries.
2. **Inline Execution** — I execute tasks in this session via executing-plans, with batch checkpoints.

**Recommendation:** Subagent-Driven for Phase 1 (6 parallel tasks), then I (Sisyphus) take over Phase 2-4 inline because they require live tool use (web search, browser, eval runs) that doesn't delegate cleanly.
