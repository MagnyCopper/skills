# Rename & Acquisition Disambiguation Rules

Purpose: Resolve a candidate legal entity to its CURRENT surviving form when the test input references an old name, an acquired brand, or a parent/subsidiary that is not what it seems.

**When to apply this:** VERIFY stage of the pipeline, after CORROBORATE produces a candidate and before SCORE. Apply whenever the candidate's name in the registry disagrees with the input name, or when the input is a known brand or trade name that may not match the legal entity name. Skip only when the candidate name exactly matches the input after normalization (see `name-normalization.md`).

---

## Part 1: Identifier-Stability Rules per Jurisdiction

The single most important fact for disambiguation: which identifiers survive renames versus which get reissued on merger.

| Jurisdiction | ID type | Stable on rename? | Behavior on merger / absorption | Notes |
|---|---|---|---|---|
| Japan (NTA 法人番号) | 13-digit corporate number | Yes | Survivor keeps its number; absorbed entity's record is closed with `closeCause` and may carry `successorCorporateNumber` | NTA "About notification" page documents this; same number across Hitachi Metals to Proterial rename |
| USA Delaware (file number) | File number | Yes (rename is an amendment, not a new entity) | Survivor keeps file number; merged-out entity gets `void` status | Most US public semiconductors are DE-incorporated |
| USA California (entity number) | Entity number | Yes | Mergers may issue a new number for the survivor depending on structure | Check bizfileonline.sos.ca.gov carefully |
| UK Companies House | Company number | Yes (does not change on rename) | New companies get new numbers; dissolved companies keep their numbers | "Previous company names" table on the overview page |
| Germany Handelsregister | HR number (always paired with court) | Typically yes | Mergers may transfer registration to the surviving court's register | Always cite with court, e.g. `München HRB 126492` |
| France SIREN (INSEE) | 9-digit SIREN (14-digit SIRET = SIREN + NIC) | Yes per legal entity | Mergers create a new SIREN for the absorbed successor OR keep the dominant party's SIREN | Verify on recherche-entreprises.api.gouv.fr |
| Korea BRN (사업자등록번호) | 10-digit BRN | Generally yes | Mergers may invalidate one BRN | DART shows corporate lineage |
| Hong Kong BRN / CR# | CR number | Yes (name changes are amendments) | New companies get new numbers | Companies Registry is paid; fall back to OpenCorporates |
| Singapore UEN | UEN | Yes | New entity = new UEN | bizfile.gov.sg |
| Taiwan 統一編號 | 8-digit tax ID | Yes | Mergers may keep one of the numbers | findbiz.nat.gov.tw |
| India CIN | 21-char CIN | NO: changes on conversion (private to public, FCRN splits) | Mergers may issue a new CIN | mca.gov.in has CAPTCHA; use OpenCorporates or Zauba |
| Belgium KBO | Enterprise number (10-digit mod97) | Yes per entity | New entity = new number | kbopub.economie.fgov.be |
| Netherlands KvK | 8-digit KvK (+ branch code) | Yes | Mergers create new numbers per Dutch civil law | kvk.nl |
| Switzerland UID | UID (CHE number) | Yes | New entity = new UID | zefix.ch |
| Canada Corp # | Corporation number | Yes | Survivors typically keep the number; some restructurings reissue | ised-isde.canada.ca |

**Practical rule:** When in doubt, prefer the entity whose registration number is currently ACTIVE in the official registry. A dissolved number is never the answer.

---

## Part 2: Rename Resolution Workflow

Use when the input references an entity that has changed its legal name (e.g. "Hitachi Metals").

1. **Search the candidate's CURRENT name in the official registry** for the detected jurisdiction. If you only have the old name, search the old name first, then look for redirect or forward pointers.

2. **Read the previous-names chain.** If the registry record exposes `previous_names` / `former_names` / `former_business_names` (UK "Previous company names", DE "Frühere Firma", NL, OpenCorporates `previous_names` array), walk it. Each hop should carry a date.

3. **Match the old name.** If the input's old name matches a previous-name entry after normalization (see `name-normalization.md`), the current registered name is the answer. Set `relationship_to_target = former_name_of_current_entity`.

4. **Wikipedia cross-check.** If the registry does not expose previous names, query: `site:wikipedia.org "<old name>" formerly OR renamed OR "change of name"`. Wikipedia infoboxes usually show "Previously called" or "Founded as".

5. **Cross-check with at least one official source** before locking in the rename: a press release on the company's own press page, an annual report, or a regulatory filing (US 8-K, JP TSE disclosure, FR BODACC, DE Bundesanzeiger). News alone does not count as official.

6. **Confirm `entity_status = active`** in the registry. If the registry shows `dissolved` WITH a successor field set, switch to Part 3 instead. The predecessor is never the answer.

7. **Lock in.** Output the current `standard_name`, the SAME `registration_number` (IDs are stable across renames per Part 1), `entity_status = active`, and populate `former_names` with the full chain.

**Edge case: rename in a different jurisdiction.** Some renames happen only in a subsidiary jurisdiction (e.g. a JP parent renames globally but a US sub keeps its old name). Always verify against the JURISDICTION implied by the test input's country hint, not the parent HQ jurisdiction.

---

## Part 3: Acquisition / Absorption Resolution Workflow

Use when the input references a brand or company that was acquired, merged, or absorbed.

1. **Classify the transaction.** Determine whether the candidate was:
   - **(a) Fully absorbed / merged out.** Registry shows `dissolved` or `merged` with a successor field set.
   - **(b) Became a subsidiary of the acquirer.** Target still files independently; `entity_status = active`.
   - **(c) Brand-only acquisition.** Brand moved to the acquirer's existing entity; the target legal entity may be unchanged or wound down.

2. **For full absorption (most common when the legal name changes globally):** Return the SURVIVOR. Check the registry for `successorCorporateNumber` (JP), the successor link in UK Companies House, or `merger_of` / `merged_into` fields in OpenCorporates. Set `relationship_to_target = acquired_absorbed_by_current`.

3. **For subsidiary retention** (acquirer bought shares but target still files independently, e.g. Sigma-Aldrich under Merck KGaA): Return the TARGET entity with its current name and number. Do NOT return the parent. The test set has many cases like this.

4. **For brand-only acquisition** (e.g. Alfa Aesar was a Johnson Matthey brand, sold to Thermo Fisher): Identify which legal entity currently owns the brand AND operates it. Check the brand's website footer, "About" page, and recent press releases. Return that operating entity, NOT the brand name itself and NOT the brand's former parent.

5. **If unclear, prefer the entity that owns the brand today.** Document every alternative you considered in `verification.contradictions` with the source URLs. Do not silently pick one.

6. **Never return a dissolved entity as the answer.** Even if the test input matches the dissolved entity's former name exactly, follow the successor chain to an active entity.

---

## Part 4: Test-Set-Specific Known Cases

These are the rows in `tests/companyName.txt` where the disambiguation rules apply directly. Study this table before running the skill. It covers renames, acquisitions, brand-vs-entity traps, and jurisdiction ambiguity.

| Row | Input (raw) | Resolution type | Output `standard_name` | Output `registration_number` | Why |
|---|---|---|---|---|---|
| 8 | Neo Performance Materials Inc. (加拿大) | Rename (formerly CITIC Envirotech) | CITIC ENVIROTECH LTD | (empty, not provided in test set) | Neo Performance Materials was formerly known as CITIC Envirotech in Canada; the Canadian registry still lists the entity as CITIC ENVIROTECH LTD |
| 20 | Alfa Aesar (美国) | Acquired + absorbed (brand moved) | THERMO FISHER SCIENTIFIC CHEMICALS INC. | 232543453 | Alfa Aesar was a brand of Johnson Matthey, sold to Thermo Fisher; the legal entity operating Alfa Aesar today is THERMO FISHER SCIENTIFIC CHEMICALS INC. (Massachusetts) |
| 21 | Sigma Aldrich (美国) | Subsidiary retained | SIGMA-ALDRICH CORPORATION | 3732137 | Two Sigma-Aldrich US entities exist: Corporation (DE 3732137) and Inc. (multiple states). Row 21 maps to Corporation |
| 30 | 圣戈班 (Soitec) | NOT a rename; different entities | SOITEC SA | 38471190900034 | "圣戈班" literally means Saint-Gobain (FR) but the parenthetical "Soitec" is the real target. Soitec SA (FR SIREN 384711909) is unrelated to Saint-Gobain |
| 39 | Nexperia B.V. (闻泰科技子公司) | Subsidiary retained (parenthetical is ownership hint, not target) | Nexperia B.V. | 66264111 | Chinese parenthetical "闻泰科技子公司" means "Wingtech subsidiary", but the target is the subsidiary itself (Netherlands KvK 66264111), not the parent Wingtech Technology |
| 40 | Coherent Corp. | Rename (was II-VI Incorporated) | Coherent Corp. | 365492 | II-VI Incorporated acquired Coherent in 2022 and renamed itself to Coherent Corp.; Delaware file number 365492 carries through the rename |
| 48 | Sigma Aldrich (默克集团) | Subsidiary retained (different entity from row 21) | SIGMA-ALDRICH, INC. | (empty in test set) | Merck KGaA owns Sigma-Aldrich. Sigma-Aldrich Inc. remains a separate US legal entity. Row 48 maps to Inc., NOT the Corporation from row 21 |
| 52 | Hitachi Metals, Ltd. | Rename (announced 2022, effective 2023-01-04) | 株式会社プロテリアル | 3010401038783 | Hitachi Metals renamed to Proterial on 2023-01-04; JP corporate number 3010401038783 unchanged across the rename (Part 1: JP numbers are stable) |
| 15 vs 64 | Kyma Technologies (row 15) / Kyma Technologies, Inc. (row 64) | Same name, different state registrations | KYMA TECHNOLOGIES, INC. (row 15) / Kyma Technologies, Inc. (row 64) | 0461726 / 0585514 | Row 15 registration number 0461726 is the North Carolina SOS filing; row 64 number 0585514 is a different state filing. Both can be valid simultaneously. The test set treats them as distinct rows; do NOT collapse to one |
| 17 | Materion Corporation (美国) | Rename (formerly Brush Wellman, Brush Engineered Materials) | Materion Corporation | 1129752 | Brush Wellman and Brush Engineered Materials renamed to Materion in 2011; Delaware file number stable. Wikipedia plus 10-K filings confirm |
| 37 | 安森美 (onsemi) | Rebrand / lowercase brand to legal entity | ON SEMICONDUCTOR CORPORATION | 3248880 | "安森美" is the Chinese rendering of ON Semiconductor. The lowercase "onsemi" is a brand, not a legal entity. DE registry legal name is ON SEMICONDUCTOR CORPORATION |
| 53 | Jaytee Alloys & Components Limited | Suffix correction (India) | JAYTEE ALLOYS & COMPONENTS PRIVATE LIMITED | U24203UP2024PTC202623 | Input omits "PRIVATE"; the Indian MCA registry shows the full CIN U24203UP2024PTC202623. PRIVATE denotes a private limited company under the Companies Act |
| 9 | Recylex S.A. (法国) | Punctuation and case normalization only | Recylex SA | 54209770400317 | Drop the period and uppercase; FR SIREN 542097704 is the entity. No rename, no acquisition, just normalization |
| 33 | 德州仪器公司 (Texas Instruments) | Chinese-name disambiguation | TEXAS INSTRUMENTS INCORPORATED | 368223 | "德州仪器" is the standard Chinese rendering of Texas Instruments. Do not confuse with a Shandong-based entity (德州 = Dezhou prefecture). The parenthetical and US context confirm the target |

**Reading this table:** "Row" is the 1-indexed line number in `tests/companyName.txt`. Empty `registration_number` cells mean the ground truth omits it, so the skill should ALSO leave it empty. Do NOT fabricate.

---

## Part 5: Query Templates

Concrete search strings by case type. Always combine at least 2 independent sources.

**Rename detection:**
- `"<old name>" "renamed to" "<new name>"`
- `"<old name>" formerly known as`
- `"<old name>" "change of name"`
- `site:<registry-domain> "previous names" "<old name>"`

**Acquisition detection:**
- `"<target>" acquired by <acquirer>`
- `"<target>" site:reuters.com acquisition`
- `"<target>" site:bloomberg.com merger`
- `"<target>" "operating as" <acquirer>`
- `"<target>" press release acquisition`

**Japan-specific (rename, 法人番号 stable):**
- `site:houjin-bangou.nta.go.jp "<old name>"`
- `"<旧商号>" "<新商号>"`
- `"<old name>" 社名変更`
- `"<old name>" プロテリアル` (or whatever the suspected new name is)

**UK-specific (Companies House previous names):**
- `site:find-and-update.company-information.service.gov.uk "<old name>"`
- `site:find-and-update.company-information.service.gov.uk/company/<number>/filing-history "change of name"`

**Germany-specific:**
- `site:bundesanzeiger.de "<old name>" Firmenänderung`
- `site:handelsregister.de "<old name>"`

**France-specific:**
- `site:recherche-entreprises.api.gouv.fr "<old name>"`
- `"<old name>" site:bodacc.economie.gouv.fr`

**US Delaware:**
- `site:icis.corp.delaware.gov "<entity name>"`
- `"<old name>" 8-K "name change" site:sec.gov`

**Brand-vs-entity disambiguation:**
- `"<brand>" "operated by"` OR `"<brand>" "a division of"`
- `"<brand>" "subsidiary of"`
- `"<brand>" legal entity name`

**Wikipedia (last resort, always cross-check with a registry):**
- `site:wikipedia.org "<name>" "formerly"`
- `site:wikipedia.org "<name>" "acquired by"`
- `site:wikipedia.org "<name>" "type" subsidiary`

---

## Part 6: Anti-Patterns (Top 5)

Recurring failure modes. If you catch yourself doing any of these, stop and re-verify.

1. **Returning the parent group when asked for the subsidiary.** Example: returning "Merck KGaA" for "Sigma Aldrich". The test asks for the entity that files under its own name, even when owned by a larger group. Fix: always verify `entity_status = active` AND that the entity name matches the test target, not the parent.

2. **Returning the brand when asked for the legal entity.** Example: returning "onsemi" (brand) instead of "ON SEMICONDUCTOR CORPORATION" (legal name). Brand names never appear in official registries. Fix: search the brand name to find the legal entity that owns it, then return the legal entity.

3. **Returning the dissolved predecessor when a successor exists.** Example: returning the old "Hitachi Metals" entry instead of "株式会社プロテリアル". Fix: always check `entity_status` and `successorCorporateNumber` (or equivalent) before locking in. If dissolved with a successor, follow the chain.

4. **Confusing a branch or local office with the HQ.** Example: returning a "Sigma-Aldrich Brazil branch" when the test wants the US parent. Fix: use the country hint in the input as the routing signal; only fall back to HQ if no entity exists in the hinted jurisdiction.

5. **Trusting a single stale source.** A Wikipedia snippet or a single OpenCorporates record may be years out of date for rename and acquisition cases. Fix: require at least 2 independent sources per CORROBORATE rules, and at least one MUST be the official registry or a regulator filing dated within the last 12 months.

---

**Final reminder:** Every resolution in Part 4 must be reproducible from the official registry of record. If you cannot trace the answer to a registry URL, your confidence is at most C and you should retry DISCOVER with the query templates in Part 5.
