# Name and Registration-Number Normalization

Exact rules for normalizing company names and registration numbers before comparison. This is the canonical reference for the PARSE stage.

> **CRITICAL CONTRACT.** This file is the single source of truth for normalization. It MUST stay byte-for-byte equivalent in behavior to the `normalize_name()` and `normalize_regnum()` functions in `tests/eval.py`. If the skill's PARSE stage deviates from this file, the eval scorer will fail to match. Any change to either side requires a matching change to the other in the same commit (see Sync protocol at the bottom).

## Shared preprocessing

Applied first to both names and registration numbers, in this order.

1. If the input is `None`, return the empty string `""`.
2. Coerce to `str`.
3. Unicode NFC composition: `unicodedata.normalize("NFC", s)`.
4. Full-width ASCII folding, codepoint by codepoint:
   - `U+3000` (ideographic space) becomes `U+0020` (ASCII space).
   - Any codepoint in the range `U+FF01` to `U+FF5E` becomes `chr(code - 0xFEE0)` (the matching ASCII character).
   - All other codepoints pass through unchanged.

After these four steps, the name-specific OR regnum-specific rules below apply. Lowercasing happens inside each branch, not here.

## Name normalization (`normalize_name`)

Apply shared preprocessing, then:

1. Lowercase the whole string (ASCII-folded first, so full-width letters lowercase correctly).
2. Replace each occurrence of any character in this set with a single ASCII space:
   `,` `.` `-` `_` `/` `(` `)` `[` `]` `【` `】` `［` `］` `「` `」` `'` `"` `&` `;` `:` `·`(U+00B7) `•`(U+2022)
   - Each matched character becomes exactly one space. Two adjacent punctuation characters become two spaces, which the next step collapses.
   - Smart/curly quotes, em dashes, en dashes, and the ideographic comma `、` (U+3001) are NOT in this set and NOT produced by folding, so they pass through untouched. (Full-width comma `，` U+FF0C and full-width dot `．` U+FF0E DO fold to ASCII and then get stripped.)
3. Collapse every run of one or more whitespace characters (`\s+`) to a single ASCII space.
4. Strip leading and trailing whitespace.

The replacement is a single regex substitution on the character class, followed by one whitespace collapse and strip. There is exactly one pass per step.

## Registration-number normalization (`normalize_regnum`)

Apply shared preprocessing, then:

1. Lowercase the whole string.
2. Iteratively strip leading jurisdiction and register-type prefixes. Repeat the following until the string stops changing:
   - Match (case-insensitive) at the START of the string only, one of:
     - `amtsgericht` immediately followed by one or more whitespace characters and then one "word" (run of word characters `\w+`),
     - or one of the literal court or register tokens: `münchen`, `stendal`, `jena`, `berlin`, `hamburg`, `frankfurt`, `hrb`, `hra`, `gnr`, `vr`, `pr`, `fa`.
   - The match must be followed by a word boundary `\b`. This means `hrb126492` does NOT match (no boundary between `b` and `1`), but `hrb 126492` does.
   - Any trailing run of whitespace, colons, commas, or dashes (`[\s:,-]*`) immediately after the boundary is consumed as part of the match.
   - Remove the entire matched span (token plus trailing separators) by replacing it with the empty string.
   - Then `.lstrip()` the result, and loop. The loop is what lets `München HRB 126492` strip both `München ` and `hrb ` in two passes.
3. Strip a leading Swiss prefix: match `che` at the start (case-insensitive) followed by any combination of `-`, `.`, or whitespace, and remove the whole match.
4. Remove every `.` and every `-` from the entire remaining string, anywhere.
5. Collapse every run of whitespace to the EMPTY string (concatenate, do not insert a separator). Then strip leading and trailing whitespace.

Two important consequences: regnums are concatenated without any internal separator, and the prefix strip is leading-anchored only. A token like `hrb` appearing in the middle of the string (after a non-stripped leading token) will NOT be removed.

## Worked examples

Every example below was verified against `tests/eval.py` on the day this file was written.

### Name examples

| Input | Output | Why |
|---|---|---|
| `AXT, INC.` | `axt inc` | comma and dot become spaces, collapsed |
| `AXT, INC` | `axt inc` | comma becomes space, collapsed |
| `SIGMA-ALDRICH, INC.` | `sigma aldrich inc` | hyphen, comma, dot each become spaces |
| `JAYTEE ALLOYS & COMPONENTS PRIVATE LIMITED` | `jaytee alloys components private limited` | `&` becomes space |
| `Foo·Bar•Baz` | `foo bar baz` | middle dot U+00B7 and bullet U+2022 become spaces |
| `AXT　INC` | `axt inc` | ideographic space U+3000 folded, then collapsed |
| `ＡＸＴ，ＩＮＣ．` | `axt inc` | full-width `，` (U+FF0C) and `．` (U+FF0E) fold to ASCII `,` and `.`, which then become spaces |


### Names that pass through unchanged

These have no ASCII punctuation, no full-width characters, and no whitespace to collapse, so the only effect is lowercasing (and these are already CJK with no case).

| Input | Output |
|---|---|
| `中國同和控股集團有限公司` | `中國同和控股集團有限公司` |
| `株式会社プロテリアル` | `株式会社プロテリアル` |
| `ラサ工業株式会社` | `ラサ工業株式会社` |
| `시지트로닉스` | `시지트로닉스` |

### Registration-number examples

| Input | Output | Notes |
|---|---|---|
| `München HRB 126492` | `126492` | two passes: strips `München `, then strips `hrb ` |
| `Stendal HRB 6090` | `6090` | two passes: `Stendal `, then `hrb ` |
| `Jena HRB 111272` | `111272` | two passes: `Jena `, then `hrb ` |
| `CHE-123.456.789` | `123456789` | CHE prefix stripped, dots removed |
| `0401.574.852` | `0401574852` | no prefix matched, dots removed |
| `U24203UP2024PTC202623` | `u24203up2024ptc202623` | only lowercased, no prefix or separators |
| `210111-0058935` | `2101110058935` | dash removed |
| `E0589082014-8` | `e05890820148` | lowercased, dash removed |
| `2246023` | `2246023` | unchanged |
| `556965-1937` | `5569651937` | dash removed |
| `1060690-1` | `10606901` | dash removed |
| `54209770400317` | `54209770400317` | unchanged |

## Non-goals

Normalization deliberately does NOT do any of the following. Do not add these in the PARSE stage, or the eval will diverge.

- Does NOT transliterate or romanize scripts. Latin, CJK, and Hangul stay as-is next to each other.
- Does NOT strip or expand legal-entity suffixes (`Ltd`, `Inc`, `GmbH`, `Corp`, `AG`, `SA`, `Co., Ltd.`, `B.V.`, `K.K.`, `plc`). These carry legal-entity meaning and must survive.
- Does NOT collapse variants such as `Limited` to `Ltd`, or `Corporation` to `Corp`. Different strings stay different.
- Does NOT remove leading zeros from numeric IDs. `0401.574.852` keeps its leading `0` (as `0401574852`), and a hypothetical `007` stays `007`. Leading zeros can be jurisdictionally significant.
- Does NOT do fuzzy, phonetic, acronym, or substring matching. After normalization the comparison is exact string equality, full stop.
- Does NOT normalize `&` to `and` or vice versa. `&` becomes a space and `and` stays `and`, so `AT&T` and `AT and T` would compare differently from `ANDT`. Match the source text.
- Does NOT strip whitespace inside the regnum branch: it collapses whitespace to empty, so any spaces inside the number are concatenated out, not kept.

## Sync protocol

If you modify `normalize_name()` or `normalize_regnum()` in `tests/eval.py`, you MUST update this file in the same commit, and vice versa. CI should run a parity check that exercises both implementations against a shared table of inputs and expected outputs, and fail the build on any mismatch. When adding a new normalization rule, add at least one worked example in the tables above that exercises it, and confirm the example passes against eval.py.
