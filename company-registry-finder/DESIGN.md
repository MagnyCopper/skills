# Design Spec: `company-registry-finder`

- **Status**: Draft (pending user review)
- **Created**: 2026-06-17
- **Author**: Sisyphus
- **Methodology**: TDD + Hill-Climbing
- **Sibling skill**: `company-domain-finder` (mirrors pipeline + schema shape)

---

## 1. Problem Statement

Given a company's informal name (often with parenthetical country/industry hints, possibly abbreviated, possibly outdated due to rename/acquisition), produce:

1. The **standard legal registered name** (in local script, as filed at the registry)
2. The **registered jurisdiction + address**
3. The **official registration number** (with country-specific format)
4. **Evidence chain** proving the result (official registry URL, locator, snippet)

Hard cases the skill MUST resolve:
- **Renames**: Hitachi Metals → プロテリアル (2022); Navitas → Navitas Semiconductor Corporation
- **Acquisitions/absorptions**: Neo Performance Materials (formerly CITIC Envirotech); Alfa Aesar (acquired by Thermo Fisher → legal entity `THERMO FISHER SCIENTIFIC CHEMICALS INC.`)
- **Disambiguation**: Sigma-Aldrich has multiple entities (`SIGMA-ALDRICH CORPORATION` vs `SIGMA-ALDRICH, INC.`); brand vs legal entity (Soitec not 圣戈班)
- **Multi-jurisdiction**: same name in different countries
- **Always return the current surviving entity**, never a dissolved predecessor

---

## 2. I/O Contract

### 2.1 Input (single company)

```json
{
  "id": "WV",
  "raw_name": "Dowa Holdings（同和控股）",
  "country_hint": null,
  "industry_hint": null
}
```

`id` is required and used as the output filename. `raw_name` is required. Hints are optional but strongly recommended — they materially affect routing.

### 2.2 Output JSON

Written to: `results/<YYYYMMDD>/company-registry-finder/<id>.json`

```json
{
  "id": "WV",
  "input": {
    "raw_name": "Dowa Holdings（同和控股）",
    "country_hint": "Hong Kong",
    "industry_hint": null,
    "parsed_hints": {
      "detected_country": "Hong Kong",
      "detected_script": "mixed",
      "detected_language_hints": ["ja", "zh-Hant"]
    }
  },
  "result": {
    "standard_name": "中國同和控股集團有限公司",
    "registered_jurisdiction": "Hong Kong",
    "registered_address": "...",
    "registration_number": "2246023",
    "registration_number_type": "HK-CR",
    "entity_status": "active",
    "former_names": [],
    "successor_entity": null
  },
  "verification": {
    "confidence_level": "A",
    "relationship_to_target": "same_entity",
    "name_match_evidence": "...",
    "regnum_match_evidence": "...",
    "address_match_evidence": "...",
    "contradictions": []
  },
  "evidence_sources": [
    {
      "url": "https://www.cr.gov.hk/...",
      "locator": "Companies Registry > Public Search > Result row 1",
      "snippet": "...",
      "kind": "official_registry",
      "accessed_at": "2026-06-17T..."
    }
  ],
  "search_methods": ["web_search", "wikipedia", "opencorporates", "cr.gov.hk"],
  "search_queries_used": ["Dowa Holdings Hong Kong", "同和控股 site:cr.gov.hk"],
  "timestamp": "2026-06-17T..."
}
```

### 2.3 Confidence levels

| Level | Meaning |
|---|---|
| **A** | Official registry confirms **all three**: name + number + address |
| **B** | Official registry confirms **2 of 3** (typically name + number) |
| **C** | Only third-party corroboration (OpenCorporates, Wikipedia, news); no registry hit |
| **D** | Single source, or guessed, or unverified rename chain |

`confidence_level < C` MUST trigger a DISCOVER retry with refined queries.

### 2.4 `relationship_to_target` enum

```
same_entity                       // direct match
former_name_of_current_entity     // rename case (e.g. Hitachi Metals → Proterial)
acquired_absorbed_by_current      // acquisition case (e.g. Alfa Aesar → Thermo Fisher Chem)
subsidiary_of_target              // wrong direction; reject
parent_or_group_entity            // wrong direction; reject
branch_or_local_office            // wrong level; reject
same_name_different_jurisdiction  // ambiguity; reject
brand_or_product_name             // not a legal entity; reject
dissolved_no_successor            // dead end; reject
unknown                           // retry
```

Only `same_entity`, `former_name_of_current_entity`, `acquired_absorbed_by_current` may advance to SCORE; the rest must trigger retry or null result.

---

## 3. Pipeline (5 stages)

```
PARSE → DISCOVER → CORROBORATE → VERIFY → SCORE
```

### 3.1 PARSE

- Strip parenthetical/bracketed hints from `raw_name`: `Dowa Holdings（同和控股）` → name=`Dowa Holdings`, hints={`同和控股`, country candidate `Japan/Hong Kong`}.
- Detect script and language of remaining text.
- Detect country hints via keyword table (日本/Japan → JP; 美国/USA → US; 德国/Germany → DE; etc.).
- Detect industry hints (半导体/semiconductor, 化学/chemicals, etc.).
- Normalize the cleaned name (full-width → half-width, case-fold, strip punctuation) for downstream comparison.

### 3.2 DISCOVER

Generate ≥3 candidate entities from independent sources:

- **Web search** — `"<cleaned_name>" official site`, `<cleaned_name> registry`, `<cleaned_name> 法人番号 / Companies House / Handelsregister / etc.`
- **Wikipedia** — first paragraph for rename/acquisition signals ("formerly", "renamed", "acquired by", "merged")
- **OpenCorporates** — search by name + jurisdiction_code
- **Country-specific official registry** (when country_hint is known or heuristically detected):
  - JP: `houjin-bangou.nta.go.jp`
  - US-DE: `icis.corp.delaware.gov`
  - US-CA: `bizfileonline.sos.ca.gov`
  - UK: `find-and-update.company-information.service.gov.uk`
  - DE: `handelsregister.de`
  - FR: `recherche-entreprises.api.gouv.fr`
  - KR: `englishdart.fss.or.kr`
  - HK: `cr.gov.hk` (paid — fall back to OpenCorporates)
  - SG: `bizfile.gov.sg`
  - TW: `findbiz.nat.gov.tw`
  - IN: `mca.gov.in` (CAPTCHA — fall back to OpenCorporates / Zauba)
  - CA: `ised-isde.canada.ca`
  - BE: `kbopub.economie.fgov.be`
  - NL: `kvk.nl`
  - CH: `zefix.ch`
  - LU: `lbr.lu`
  - KZ: OpenCorporates (eGov requires login)

Each candidate records: candidate_name, candidate_number, candidate_jurisdiction, source_url, snippet.

### 3.3 CORROBORATE

A candidate advances only if **≥2 independent sources** agree on `name` OR `registration_number`. Sources are independent if they have different `kind` (e.g. `official_registry` + `wikipedia` counts; `wikipedia` + `news` does NOT, because news often cites Wikipedia).

### 3.4 VERIFY

Hit the **official registry page** for the candidate's jurisdiction. Apply rename/acquisition resolution rules (see `references/disambiguation-rules.md`):

- Check `entity_status` (active / dissolved / merged)
- If `former_names` field exists on the registry record, walk the chain to the current name
- If dissolved with successor, follow `successorCorporateNumber` (JP) / equivalent
- For acquisition cases, identify whether the target was absorbed (return survivor) or remains a subsidiary (return subsidiary)
- Confirm `registration_number` matches the registry-record number after normalization
- Confirm `registered_address` is the current registered office, not a historical one

### 3.5 SCORE

- Assign `confidence_level` per the table in §2.3.
- If `<C`, retry DISCOVER with:
  - Alternative spellings (romanization variants, e.g. `プロテリアル` ↔ `Proterial` ↔ `旧 日立金属`)
  - Old name as query (for rename cases)
  - Parent company as query (for subsidiary cases)
- If still `<C` after 2 retries, output best guess with `confidence_level=D` and document contradictions.

---

## 4. References (precompiled — sources already gathered)

| File | Contents |
|---|---|
| `references/registry-sources.md` | 16-country table: official registry name + URL + free? + best 3rd-party + anti-bot notes |
| `references/number-formats.md` | Per-jurisdiction reg-number format + checksum rules (JP 13-digit Luhn, BE mod97, KR BRN, TW 統一編號, IN CIN 21-char, US state variance, etc.) |
| `references/disambiguation-rules.md` | Rename/acquisition patterns + identifier-stability rules (JP/DE/UK numbers stable across renames) |
| `references/name-normalization.md` | Case-fold, strip punctuation, normalize CJK full/half-width, script detection |

Sources for these files are the librarian outputs from `bg_8c6a5ec6` and `bg_85d8acce`.

---

## 5. Eval Harness (TDD + Hill-Climbing)

### 5.1 Test set

`tests/companyName.txt` — copy of `temp/companyName.txt`. Format is **3-column TSV** (no ID column): `raw_name<TAB>ground_truth_standard_name<TAB>ground_truth_registration_number`. Eval uses **row number (1-indexed, zero-padded to 3 digits)** as the output `<id>` (e.g. `001.json`, `072.json`). Total rows: 72. Rows with empty `ground_truth_regnum`: **5** (rows 5, 8, 46, 47, 48).

### 5.2 Three-tier scoring (`tests/eval.py`)

```python
def score_row(predicted, ground_truth_name, ground_truth_regnum):
    name_score = 1 if normalize(predicted.standard_name) == normalize(ground_truth_name) else 0

    if ground_truth_regnum.strip() == "":
        regnum_score = None  # N/A — no penalty, no bonus
    else:
        regnum_score = 1 if normalize(predicted.registration_number) == normalize(ground_truth_regnum) else 0

    return name_score, regnum_score

# Total = Σ(name_score) + Σ(regnum_score where not None)
# Report: name_accuracy, regnum_accuracy_on_nonempty, total_score, per_row_breakdown
```

`normalize()` is the SAME function used in PARSE — case-fold, strip whitespace/punctuation, fold CJK width, strip jurisdiction prefixes/suffixes (e.g. `"München HRB 126492"` ↔ `"HRB 126492"`).

### 5.3 Hill-climbing protocol

| Step | Artifact | Gate |
|---|---|---|
| 0 | `tests/eval.py` + frozen test set | eval runs on empty outputs, returns 0 |
| 1 (RED) | Minimal `SKILL.md` + `prompt.md` that only does web search + Wikipedia | baseline > 0 |
| 2 | Add PARSE-stage country-hint extraction | score ↑ |
| 3 | Add per-country official registry URLs to DISCOVER | score ↑ |
| 4 | Add rename/acquisition rules to VERIFY (Hitachi Metals→Proterial, Neo Perf→CITIC, Alfa Aesar→Thermo Fisher) | score ↑ |
| 5 | Add name-normalization rules (case/punctuation/CJK width/jurisdiction-prefix stripping) | score ↑ |
| 6 | Add disambiguation for multi-entity cases (Sigma-Aldrich entities, brand≠entity) | score ↑ |
| 7 | Add multi-language query expansion (JP/EN/CJK cross-search) | score ↑ |
| 8 | Add reg-number checksum validation as contradiction detector | score ↑ |

**Stop conditions** (any one):
- 8 climbs completed
- Score ≥ 95% of achievable max
- 2 consecutive climbs with no improvement

### 5.4 Achievable max

Achievable max = `(# rows) + (# rows with non-empty regnum)`.
- # rows = 72
- # rows with non-empty regnum = 72 − 5 = 67
- **Achievable max = 72 + 67 = 139**

**95% target = ~132.**

Note on duplicates: the test set has some duplicate inputs (e.g. FLOSFIA appears 5×, AXT 2×). Eval scores **per-row** (deterministic skill → same input yields same output → duplicates contribute consistently). Achievable max stays 139.

---

## 6. Directory Layout (final)

```
company-registry-finder/
├── SKILL.md                              # Trigger + workflow + hard rules
├── prompt.md                             # Full technical contract (schema, pipeline, examples)
├── DESIGN.md                             # This file
├── assets/templates/output-template.json
├── references/
│   ├── registry-sources.md
│   ├── number-formats.md
│   ├── disambiguation-rules.md
│   └── name-normalization.md
└── tests/
    ├── companyName.txt
    ├── eval.py
    └── run-eval.sh
```

Output (runtime, not in repo): `results/<YYYYMMDD>/company-registry-finder/<id>.json`

---

## 7. Out of Scope (explicit)

- No batch endpoint. Skill processes one company per invocation; batch is external loop.
- No paid APIs (Bloomberg, D&B, S&P Capital IQ). Free sources only.
- No PDF filing extraction. If registry exposes only PDFs, accept lower confidence.
- No persistent cache. Each invocation hits sources fresh.
- No Chinese (mainland) companies — test set is all foreign; 中国大陆 skill is a separate concern.

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| HK Companies Registry is paid | Fall back to OpenCorporates + Wikipedia + official press releases |
| India MCA has CAPTCHA | Use OpenCorporates / Zauba as primary |
| Texas SOS requires login | Default to Delaware (most US public semiconductors are DE-incorporated) |
| OpenCorporates rate limit (50/day) | Cache responses within a single eval run; use jurisdiction_code filter to reduce calls |
| Rename chains >2 hops | Cap at 3 hops; if unresolved, return `confidence_level=D` |
| CJK normalization drift | Use the SAME `normalize()` function in eval and in PARSE |

---

## 9. Acceptance Criteria (definition of done)

1. ✅ All 8 hill-climbing iterations executed (or stop condition met)
2. ✅ `tests/eval.py` reports `total_score ≥ 110` (~95% of achievable max 116)
3. ✅ All `references/*.md` files have valid URLs (no 404s on the registry roots)
4. ✅ `SKILL.md` + `prompt.md` + `output-template.json` are internally consistent (no schema drift)
5. ✅ At least 1 worked example in `prompt.md` showing the rename case (Hitachi Metals → プロテリアル)
6. ✅ Manual spot-check on 5 random rows confirms JSON correctness
