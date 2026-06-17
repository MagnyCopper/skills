# Registration Number Formats by Jurisdiction

Per-jurisdiction format, length, and checksum reference used in VERIFY (validate candidates) and SCORE (detect contradictions, infer jurisdiction). Focus is on FORMAT and CHECKSUM, not source URLs (see `registry-sources.md` for those).

How to use: when a candidate number is scraped from a registry, (1) normalize it per the "Normalization for comparison" rules, (2) run the jurisdiction-specific validation pseudocode, (3) if it fails checksum or shape, treat the candidate as low-confidence or contradicting. If a country hint is missing, use the "Multi-format detection cheatsheet" to guess the jurisdiction before validating.

Uncertainty policy: every checksum below is either verified against the test set / known public vector, or explicitly marked `uncertain`. Do not invent algorithms.

---

## Japan (JP): 法人番号 / Corporate Number

- Format: 13 digits, no separators. Leading digit encodes entity class (1-5 for-profit, 6 foreign, 7 unincorporated, 8 national, 0/9 structurally impossible as check).
- Length: exactly 13.
- Checksum: weighted-sum, verified. Leading digit is the check digit (range 0-8 only).
- Example: `4010001099184` (DOWAエレクトロニクス, validates). Also `8010001034971`, `2010001008650`.
- Caveat: test-set `9130001000052` (ROHM) FAILS the checksum and a leading `9` is impossible, so it is a test-set anomaly. The checksum is a strong typo detector.
- Validation:
```python
def jp_valid(num):
    d = [int(c) for c in num]
    if len(d) != 13 or not num.isdigit(): return False
    total = 0
    for p in range(2, 14):           # positions 2..13
        w = 1 if (14 - p) % 2 == 1 else 2   # rightmost(13)=1, alternate
        q = d[p-1] * w
        total += q - 9 if q >= 10 else q    # digit-sum two-digit products
    return ((9 - total % 9) % 9) == d[0]
```

## Delaware, USA (us_de): File Number

- Format: numeric, no separators. Historically 6-7 digits; now often 7-8.
- Length: 6-8 digits (variable). Leading zeros common and significant.
- Checksum: none.
- Example: `2817630` (AXT), `3732137` (Sigma-Aldrich Corp), `368223` (Texas Instruments), `365492` (Coherent).
- Caveat: a few test-set US rows carry 9-10 digit values (e.g. `232543453`, `122003890`, `0801181025`) that do NOT fit the Delaware shape. These may be Delaware file numbers that have grown, or identifiers from another state. Flag as `shape-mismatch` rather than trusting blindly.

## California, USA (us_ca): Entity / File Number

- Format: Entity Number is 7 digits, optionally prefixed `C` (corp) or `F` (foreign). A separate file-number style carries a hyphenated check suffix.
- Length: 7-12 chars depending on sub-type.
- Checksum: none for the 7-digit entity number. The `-N` suffixed form is a tax/seller-account style with an internal check digit, NOT publicly documented as a stable mod-11. Treat as `uncertain`.
- Example: `E0589082014-8` (ALB Materials) normalizes to `e05890820148`; `34601186F` (Galvotec) carries an `F` foreign marker.
- Caveat: `E0589082014-8` is more likely a California tax/seller account than a corporate entity number. When a clean 7-digit entity number is available, prefer it.

## New York, USA (us_ny): DOS ID

- Format: numeric, no separators.
- Length: typically 6-7 digits (older IDs can be shorter).
- Checksum: none.
- Example: `46622` (Indium Corporation).

## United Kingdom (GB): Companies House Number

- Format: 8 chars. Most are 8 digits (leading zeros significant). Prefix forms: `SC` (Scotland), `NI` (Northern Ireland), `OC` (old), `LP`/`NL`/`SL`/SO` (limited partnerships), `OE`/`GE` (overseas). Prefix locates the sub-jurisdiction within the UK.
- Length: 8 chars (some early prefixes plus shorter numerics are zero-padded to 8).
- Checksum: none. The prefix is the only structural signal.
- Example: `03745726` (IQE PLC), `02641768` (Photek).
- Caveat: keep leading zeros. `03745726` != `3745726`.

## Germany (DE): Handelsregister

- Format: `[Court] [Register-type] [number]`, e.g. `München HRB 126492`. Register types: `HRA` (sole trader/partnership), `HRB` (GmbH/AG/etc.), `GnR` (Genossenschaft), `VR` (Verein), `PR` (Partnerschaft). Court = Amtsgericht location (city).
- Length: numeric core is variable (4-7 digits typical).
- Checksum: none.
- Example: `Stendal HRB 6090` (PPM Pure Metals), `München HRB 126492` (Infineon), `Jena HRB 111272` (Geratherm Medical).
- Caveat (CRITICAL for matching): `eval.py` `normalize_regnum()` only strips the bare city names `münchen|stendal|jena|berlin|hamburg|frankfurt`, plus the generic `amtsgericht <word>` form. Any OTHER bare city (Dresden, Leipzig, Düsseldorf, ...) is NOT stripped and survives into the normalized form. To maximize match probability, emit DE numbers either as bare `<number>` or as `Amtsgericht <City> HRB <number>`; avoid bare non-allowlisted city names.

## France (FR): SIREN / SIRET

- Format: SIREN = 9 digits (Luhn). SIRET = 14 digits = SIREN + 5-digit NIC (establishment), no extra checksum (validating the SIREN prefix is enough).
- Length: 9 (SIREN) or 14 (SIRET).
- Checksum: Luhn on the 9-digit SIREN, verified.
- Example: `54209770400317` (Recylex SIRET, SIREN `542097704` passes Luhn), `38471190900034` (Soitec SIRET, SIREN `384711909` passes).
- Validation:
```python
def siren_valid(num):
    d = [int(c) for c in num]
    if len(d) != 9: return False
    total = 0
    for i, c in enumerate(reversed(d)):
        c = c * 2 if i % 2 == 1 else c
        total += c - 9 if c > 9 else c
    return total % 10 == 0
```

## Korea (KR): 사업자등록번호 (BRN)

- Format: 10 digits, displayed `XXX-XX-XXXXX`.
- Length: 10.
- Checksum: weighted-sum mod 10, verified against the public algorithm (e.g. Naver `220-81-62517` validates). Weights for digits 1-9: `[1,3,7,1,3,7,1,3,5]`, plus an extra `floor(d9*5/10)` term.
- Example (test set): `210111-0058935` (Sigetronics). FLAG: this is 13 digits, NOT a 10-digit BRN. It is almost certainly a 법인등록번호 (corporate registration number, 13 digits), which has a different, less consistently documented checksum. Treat the test-set KR value as `shape-mismatch` against the canonical BRN.
- Validation:
```python
def kr_brn_valid(num):
    d = [int(c) for c in num]
    if len(d) != 10: return False
    w = [1,3,7,1,3,7,1,3,5]
    s = sum(d[i]*w[i] for i in range(9)) + (d[8]*5)//10
    return ((10 - s % 10) % 10) == d[9]
```

## Hong Kong (HK): BR / CR Number

- Format: 8 digits (Business Registration Number = first 8 of the CR number). Leading zeros significant.
- Length: 8.
- Checksum: none.
- Example: `2246023` (中國同和控股集團). Caveat: this is 7 digits, almost certainly leading-zero-stripped from `02246023`. When emitting, zero-pad to 8.
- Ambiguity: a bare 8-digit number is indistinguishable from UK/CA/NL/TW without a country hint.

## Singapore (SG): UEN

- Format: 9-10 chars, alphanumeric. Three families: (a) legacy 8-9 digit ACRA local entity, (b) 10-char `nTnnnnnnX` style (e.g. `201912345K`) ending in a mod-11 check letter, (c) foreign-company `F` or `T` prefixes. Check letter uses an alphabet map with mod-11 weighted sum.
- Length: 8, 9, or 10.
- Checksum: mod-11 check letter for the 10-char business/UEN form. Documented but variant by entity type.
- Example: NONE clean in the test set. The task-suggested `16753878` is the TW Uniform Number of the Taiwanese firm 艾德康科技 (Atecom), NOT a Singaporean UEN. Do not use it as an SG exemplar.
- Caveat: `uncertain` on which 10-char sub-format applies without the entity type. Validate shape only unless the UEN family is known.

## Taiwan (TW): 統一編號 (Uniform Business Number)

- Format: 8 digits.
- Length: 8.
- Checksum: weighted sum, weights `[1,2,1,2,1,2,4,1]`, verified. Two-digit products are digit-summed. The 7th digit (weight 4) has a special rule: when its product >= 10, EITHER the digit-sum OR the raw product may be used; the number is valid if either choice makes the total divisible by 10.
- Example: `16753878` (Atecom, validates via the 7th-digit special rule: product 28 digit-summed to 10, total 40).
- Validation:
```python
def tw_valid(num):
    d = [int(c) for c in num]
    if len(d) != 8: return False
    w = [1,2,1,2,1,2,4,1]
    base = 0
    for i in range(8):
        if i == 6: continue
        p = d[i]*w[i]
        base += (p//10 + p%10) if p >= 10 else p
    p7 = d[6]*4
    s7 = (p7//10 + p7%10) if p7 >= 10 else p7
    return ((base + s7) % 10 == 0) or ((base + p7) % 10 == 0)
```

## India (IN): CIN

- Format: 21 chars. Structure: `[L|U][5 digits PPP code][2-letter state][4 digits][6-digit class/type letters embedded][6 digits]`. Example `U24203UP2024PTC202623`: `U` (manufacturing), `24203` (nic), `UP` (Uttar Pradesh), `2024`, `PTC` (private limited), `202623`.
- Length: exactly 21.
- Checksum: none.
- Example: `U24203UP2024PTC202623` (Jaytee Alloys & Components).
- Caveat: `LLPIN` (Limited Liability Partnership ID) is a 7-char alpha + 3 digits variant; flag if seen.

## Canada (CA): Federal Corporation Number / BN

- Format: Federal Corporation Number is 7 digits, no checksum. Business Number (BN) is 9 digits + a 4-character program identifier suffix (e.g. `RC0001` for corporate tax).
- Length: 7 (federal) or 9+4 (BN).
- Checksum: none on the federal number. BN has a mod-10-ish internal check but it is `uncertain` and not consistently enforced; do not rely on it.
- Example: `1060690-1` (5N Plus). Caveat: `1060690` is 7 digits + a `-1` suffix, which is the Quebec NEQ (Numéro d'entreprise du Québec) shape `7digits-D` rather than a federal 7-digit number. Flag sub-jurisdiction (Quebec vs federal) when present.

## Belgium (BE): KBO / BCE

- Format: 10 digits, displayed `0xxx.xxx.xxx`. Leading zero significant (the 2008 reform added it).
- Length: 10.
- Checksum: mod-97, verified via the legacy rule `97 - (int(first_8) % 97) == int(last_2)`. For numbers whose first digit is 1 or 2 (newer range), the variant uses `int('2' + first_8)` if the plain form fails.
- Example: `0401.574.852` (Umicore, normalizes to `0401574852`, base `04015748` check `52` validates).
- Validation:
```python
def be_valid(num):                 # num = 10 digit string
    if len(num) != 10 or not num.isdigit(): return False
    base, chk = int(num[:8]), int(num[8:10])
    if 97 - base % 97 == chk: return True
    return 97 - int('2' + num[:8]) % 97 == chk   # newer 1xx/2xx range
```

## Netherlands (NL): KvK Number

- Format: 8 digits (KvK/Vestigingsnummer). Note: the RSIN (legal-entity tax id) is 9 digits with a mod-11 check; do not confuse the two.
- Length: 8 (KvK) or 9 (RSIN).
- Checksum: none on the 8-digit KvK. RSIN has mod-11 (weights 9..2 descending, `sum % 11 == 0`).
- Example: `66264111` (Nexperia), `33194537` (STMicroelectronics N.V.). Both are 8-digit KvK, no checksum to apply.

## Switzerland (CH): UID / IDE

- Format: `CHE-123.456.789` (9 digits after the `CHE-` prefix).
- Length: 9 digits + prefix.
- Checksum: simple mod-11 on the 9 digits (weights descending). `uncertain`: the official UID uses an EAN-like check, but public references conflict; verify against the registry before flagging a contradiction.
- Example: none in the test set. Documented for completeness.
- Caveat: `CHE` is the ISO country prefix; the SECO registry is authoritative.

## Luxembourg (LU): RCS Number

- Format: `RCS [B|R|...][number]`, e.g. `RCS B12345`. `B` = SARL/SA, other letters for other entity types.
- Length: variable (prefix + numeric core).
- Checksum: none.
- Example: none in the test set. Documented for completeness.

## Kazakhstan (KZ): BIN

- Format: 12 digits. Structure: `YYMM` (registration date) + 1 entity-type digit + 5-6 digit serial + check digit.
- Length: 12.
- Checksum: `uncertain` (no simple public reference). The check digit exists but the algorithm is not consistently published; do not invent one. Validate shape only.
- Example: none in the test set (Pavlodar Alumina Plant row has an empty regnum). Documented for completeness.

---

## Multi-format Detection Cheatsheet

Given an unknown number (after stripping whitespace), guess jurisdiction by shape BEFORE validating. Always confirm with the country hint when available.

| Shape (regex, post-normalization) | Likely jurisdiction | Confirm via |
|---|---|---|
| `^\d{13}$` | JP | JP checksum (leading digit 0-8) |
| `^\d{14}$` | FR SIRET | Luhn on first 9 |
| `^\d{10}$` | KR BRN | KR weighted checksum |
| `^\d{9}$` | FR SIREN / BE / NL RSIN / CA BN | Luhn (FR) or mod-97 (BE) |
| `^\d{8}$` | GB / HK / NL KvK / TW / CA | TW checksum; else need hint |
| `^\d{7}$` | US-NY / CA federal / HK (stripped) | no checksum; need hint |
| `^\d{6,8}$` | US-DE | no checksum |
| `^[a-z]\d{8}$` | US-CA (foreign/`F`/`E` marker) | no checksum |
| `^[a-z]{2}\d{6,}$` | GB with prefix (SC/NI/OC/LP) | prefix = sub-jurisdiction |
| `.*hrb.*` / `.*hra.*` / `amtsgericht` | DE | strip court + register type |
| `^\d{3}\.\d{3}\.\d{3}$` | BE | mod-97 (pre-normalization) |
| `^che-?\d{3}\.?\d{3}\.?\d{3}$` | CH | mod-11 (uncertain) |
| `^[lu]\d{5}.{10}$` (21 chars) | IN CIN | shape only |
| `^\d{4}\d{4}\d{4}$` = 12 digits | KZ BIN | shape only (no checksum) |

Tie-breakers when multiple shapes match: prefer the country hint. Without a hint, a passing checksum beats no checksum (JP > FR > KR > TW > BE > shape-only).

---

## Normalization for Comparison

Two regnums are considered equal by `tests/eval.py` iff `normalize_regnum(a) == normalize_regnum(b)`. To stay consistent with the scorer, apply EXACTLY this pipeline (do not add steps, do not reorder):

1. NFC unicode normalization.
2. Fold full-width ASCII (U+FF01..U+FF5E) to half-width; map U+3000 ideographic space to ASCII space.
3. Lowercase.
4. Loop until stable: strip a LEADING token matching `^(amtsgericht\s+\w+|münchen|stendal|jena|berlin|hamburg|frankfurt|hrb|hra|gnr|vr|pr|fa)\b[\s:,-]*` (case-insensitive), then re-lstrip. This repeats so `Stendal HRB 6090` -> `6090` and `München HRB 126492` -> `126492`.
5. Strip a leading `che` prefix (with optional `-`, `.`, or whitespace): `CHE-123.456.789` -> `123456789`.
6. Delete every `.` and every `-` (do NOT delete other punctuation, letters, or digits).
7. Delete ALL whitespace, then strip.

Reference behavior on test-set values (verify any change to this doc against these):

- `Stendal HRB 6090` -> `6090`
- `München HRB 126492` -> `126492`
- `CHE-123.456.789` -> `123456789`
- `0401.574.852` -> `0401574852`
- `E0589082014-8` -> `e05890820148` (the `e` survives; only `-` is removed)
- `210111-0058935` -> `2101110058935`
- `1060690-1` -> `10606901`
- `U24203UP2024PTC202623` -> `u24203up2024ptc202623`
- `34601186F` -> `34601186f`

Consequences an agent must know:

- Leading zeros are PRESERVED (only `.`, `-`, whitespace, and the listed prefixes are removed). Never strip leading zeros when emitting.
- A bare German city NOT in the allowlist (`dresden`, `leipzig`, `düsseldorf`, ...) is NOT stripped, so `Dresden HRB 12345` normalizes to `dresdenhrb12345` and will NOT match `Amtsgericht Dresden HRB 12345` (-> `12345`). Emit either bare `<number>` or the full `Amtsgericht <City> HRB <number>` form.
- The scorer keeps letters (`e`, `f`, `u`, state codes). Do not strip alphanumeric markers a human might consider cosmetic.
- When two scraped candidates normalize differently but refer to the same entity (e.g. one with a UK prefix, one without), they will be scored as a mismatch. Pick the form most likely to equal the ground-truth normalized form.
