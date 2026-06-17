# Hill-Climbing Log: company-registry-finder

Methodology: TDD + Hill-Climbing per PLAN.md §3.
Scoring: three-tier per tests/eval.py (name_match +1, regnum_match +1 on non-empty, empty=N/A).
Target: ≥95% of achievable max (139).

## Subset for iterations (12 rows, diverse coverage)

| Row ID | raw_name | Why selected |
|---|---|---|
| 001 | Dowa Holdings（同和控股） | HK simple case, CJK hints |
| 002 | PPM Pure Metals GmbH（德国） | DE Handelsregister format |
| 006 | Dowa Electronics Materials Co., Ltd. (日本) | JP 法人番号 |
| 009 | Recylex S.A. (法国) | FR SIRET |
| 017 | Materion Corporation (美国) | US rename (formerly Brush) |
| 020 | Alfa Aesar (美国) | US acquisition case |
| 027 | 英飞凌科技股份公司 (Infineon、德国) | DE, CJK input |
| 033 | 德州仪器公司 (Texas Instruments) | US DE, CJK disambiguation |
| 039 | Nexperia B.V. (闻泰科技子公司) | NL, subsidiary hint |
| 047 | 住友电气工业株式会社 (Sumitomo Electric) | JP, empty regnum in GT |
| 052 | Hitachi Metals, Ltd. | JP rename (→ Proterial) |
| 055 | Umicore | BE KBO format |

---

## Baseline (Climb 0)

Date: 2026-06-17
Files: 12/12 written (001, 002, 006, 009, 017, 020, 027, 033, 039, 047, 052, 055)

| Metric | Score |
|---|---|
| Name matches | 11/12 (91.7%) |
| Regnum matches | 9/11 non-empty (81.8%) |
| **Total** | **20/23 (87.0%)** |

**Failures:**
- Row 002 (PPM Pure Metals GmbH): agent returned successor `PPM High Purity Metals GmbH` (HRB 34553) instead of original entity `PPM Pure Metals GmbH` (HRB 6090) which is in liquidation but still registered. Root cause: disambiguation rule "return current surviving entity" applied too aggressively to liquidation cases.
- Row 017 (Materion Corporation): name matched but `registration_number` left blank. Agent could not verify DE file number 1129752 on Delaware SoS live search, and did not fall back to OpenCorporates/LEI. Root cause: no explicit fallback rule when official registry search returns no results.

**Successful cases (notable):**
- Row 001 (Dowa HK): correct CJK name + HK CR 2246023
- Row 006 (Dowa JP): correct JP 法人番号, full-width DOWA normalized correctly
- Row 009 (Recylex FR): correct SIRET despite judicial reorganization context
- Row 020 (Alfa Aesar US): correct acquisition resolution to THERMO FISHER SCIENTIFIC CHEMICALS INC. / 232543453
- Row 027 (Infineon DE): correct Handelsregister München HRB 126492
- Row 033 (Texas Instruments US): correct DE file number 368223 via LEI fallback
- Row 039 (Nexperia NL): correct KvK 66264111, did not collapse to parent Wingtech
- Row 047 (Sumitomo JP): correct JP name in Japanese script, empty GT regnum handled
- Row 052 (Hitachi Metals JP): correct rename to 株式会社プロテリアル / 3010401038783
- Row 055 (Umicore BE): correct KBO 0401.574.852

---

## Climb 1: Fix liquidation-overreach + add registry-fallback rule

**Hypothesis:** Two targeted fixes to prompt.md will recover rows 002 and 017:
1. Add rule: "If input name exactly matches a registered entity (even in liquidation), return that entity. Only follow successor chains when entity is formally dissolved/deregistered."
2. Add rule: "When official registry search returns no results after 2 attempts, use OpenCorporates API or GLEIF LEI database as fallback for registration number verification."


**Result:** KEEP ✅
- Subset score: 20/23 → **23/23 (100%)**
- Name matches: 11→12/12, Regnum matches: 9→11/11
- Row 002: returned PPM Pure Metals GmbH (HRB 6090) correctly per rule #13
- Row 017: returned Materion Corporation / 1129752 via GLEIF LEI fallback (rule #14). Bonus finding: GLEIF LEI revealed 1129752 is an Ohio entity number, not Delaware as originally assumed.
- prompt.md updated with MUST DO rules 13 (liquidation≠dissolution) and 14 (OpenCorporates/GLEIF LEI fallback)

---

## Climb 2: Scale to full 72-row test set

**Strategy:** Process remaining 60 rows (rows 3-5, 7-8, 10-16, 18-19, 21-26, 28-32, 34-38, 40-46, 48-51, 53-54, 56-72) in parallel batches of 12. Identify new failure patterns for subsequent climbs.
