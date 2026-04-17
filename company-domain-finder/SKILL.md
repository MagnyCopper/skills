---
name: company-domain-finder
description: >
  Find a company's official website domain given its name and country/region through multi-source search and verification.
  Use this skill whenever you need to discover, verify, or look up a company's official web presence. This includes:
  - Explicit requests: "find company website", "look up official domain", "企业官网", "公司域名", "find homepage URL",
    "what's the URL of X", "这家公司的网址是什么"
  - Implicit intent: the user provides a company ID + name + country/region and expects a domain result,
    asks "帮我在网上找到这家公司", "where can I find this company online", "check this company's web presence"
  - Domain verification: confirming whether a given domain belongs to a specific company
  Even if the user doesn't explicitly say "domain" or "website", if they provide company identification details
  and seem to want web presence information, use this skill.
---

# Company Domain Finder

Given a company name + country/region (+ optional internal ID), discover the company's official website domain through multi-source search and verification.

## Input Contract

Required (provided by user each conversation):

| Field | Description |
|---|---|
| `company_id` | Internal company identifier |
| `company_name` | Company name (may be Chinese, English, or local language) |
| `country_or_region` | Country or region (may be Chinese name, English name, or ISO code) |

The user provides exactly one company per conversation.

## Output Contract

Write results to: `results/<YYYYMMDD>/company-domain-finder/<company_id>.json`

The JSON file must use the exact keys defined in [assets/templates/output-template.json](assets/templates/output-template.json). Every key must be present and stable across invocations. Return **exactly one** best domain in `official_domain` — no candidates array. Arrays default to `[]`, strings default to `""` or `null` as specified in the template.

## Core Pipeline (4 stages)

Execute these stages in order. Each stage may produce candidate domains. Do not skip stages unless tools are unavailable.

### Stage 1: DISCOVER — Primary Search

The goal is to produce an initial set of candidate domains.

1. **Detect available tools.** Check which search tools exist in the current environment:
   - `web_search` / `WebSearch` / `websearch` / `google_web_search` (built-in search)
   - `web_fetch` / `WebFetch` / `webfetch` (page content retrieval)
   - `microsoft_playwright-mcp_browser_*` (Playwright MCP browser automation)
   - `bash` (shell access for curl, whois, dig)

2. **Select search engine(s).** Based on the country/region, choose engines that give the best coverage:
   - Chinese companies or Chinese-language names: **Baidu** as primary, Google/Bing as secondary
   - All other regions: **Google** or **Bing** as primary (via built-in web_search), DuckDuckGo as fallback
   - If built-in search is unavailable: use `curl` to access DuckDuckGo HTML (`https://html.duckduckgo.com/html/?q=<query>`)

3. **Craft search queries.** At the start of this stage, read [references/search-strategies/README.md](references/search-strategies/README.md) to identify the regional strategy file for the target country, then read that file for country-specific query templates. At minimum, execute 3 different query patterns:
   - Exact name + "official site" / "official website"
   - Exact name + country-specific ccTLD filter
   - Exact name + country context keyword

4. **Collect candidate domains.** From search results, extract unique domains. Normalize to full URL format (add `https://` if missing, strip trailing paths to get the root domain). Deduplicate by registrable domain. If the first round returns no relevant results, see the [Search Failure Handling](#search-failure-handling) section below.

### Stage 2: CORROBORATE — Cross-Validation

Narrow candidates by cross-checking with additional sources.

1. **Wikipedia check.** Search for the company on Wikipedia (any language edition). If a Wikipedia article exists, extract the "Website" or "Official site" field from the infobox. This is a strong signal.

2. **Second engine check.** If Stage 1 used one engine, run at least one query on a different engine to see if the same domain appears.

3. **Knowledge graph signals.** Look for knowledge panel results, LinkedIn company pages, or business directory listings that reference an official website.

4. **Rank candidates.** Domains that appear across multiple sources rank higher.

### Stage 3: VERIFY — Domain Verification

Confirm that the best candidate domain actually belongs to the target company.

For the top candidate (and optionally 1-2 runner-ups for cross-checking):

1. **Fetch the homepage.** Use `web_fetch` or Playwright MCP to retrieve the candidate domain's homepage content.

2. **Check for company name match.** Look for the company name in:
   - Page `<title>`
   - Footer copyright notice
   - About or Contact page content
   - Organization structured data (JSON-LD `@type: Organization`)

3. **Check for country/region consistency.** The site should be relevant to the stated country. Signals include:
   - Site language matches the country
   - Address or phone numbers on the site match the country
   - Legal entity name in Impressum/Legal/About matches

4. **Optional deep verification** (if Playwright MCP is available):
   - Navigate to the About/Contact page and check for company name + address
   - Check if the domain has a valid SSL certificate
   - Use `bash` to run `whois <domain>` or `dig <domain>` if available, and check registrant info

### Stage 4: SCORE — Select the Single Best Result

After verification, select the **single most accurate domain** as the final result.

**Selection priority (in order):**

1. Domain confirmed by 2+ independent sources (search engine + Wikipedia/knowledge graph) AND page content matches company name AND country is consistent → `high` confidence
2. Domain confirmed by 1 strong source (e.g., Wikipedia infobox) AND page content partially matches → `medium` confidence
3. Domain appears in search results but could not be fully verified → `low` confidence

Assign the `confidence_level` and `official_domain` accordingly.

If no domain can be found with reasonable confidence, set `official_domain` to `null` and `confidence_level` to `null`.

## Tool Priority and Graceful Degradation

The skill must work with varying tool availability. Follow this priority:

```
Priority 1 (required):  built-in web_search
Priority 2 (strongly recommended): web_fetch
Priority 3 (enhances confidence): Playwright MCP browser automation
Priority 4 (fallback search): curl + DuckDuckGo HTML via bash
Priority 5 (domain validation): whois / dig / nslookup via bash
```

If Priority 1 is unavailable, fall back to Priority 4. If Priority 2 is unavailable, skip page content verification (confidence will be lower). Priority 3 and 5 are optional enhancements.

## Country/Region Resolution

The input `country_or_region` may be in Chinese (e.g., "德国"), English (e.g., "Germany"), or ISO code (e.g., "DE"). Resolve it to a canonical form before selecting search strategies. If cross-validation through official registries is needed, read [references/country-registries.md](references/country-registries.md) to find the appropriate registry URL and lookup method.

## Company Name Handling

The input `company_name` may be in Chinese, English, or the local language.

- If the name is in Chinese and the country is non-Chinese: also search for the company's English or local-language name. Try to discover the original language name from initial search results.
- If the name is in English and the country is non-English: also search with the local-language name if discoverable.
- If the name is in the local language: use it directly with local search engines.

Do not translate company names yourself. Instead, use search results to discover alternative names.

## Output Rules

1. **Always write the JSON file**, even if no domain is found (`official_domain` = `null`).
2. **Every key in the JSON must be present.** No missing keys.
3. **`official_domain`** is the single best domain (full URL), or `null` if not found.
4. **`confidence_level`** reflects the evidence quality for the selected domain.
5. **`evidence_sources`** must include at least one URL or method description explaining why this domain was chosen.
6. **`search_methods`** lists the actual methods used (not planned methods).
7. **`search_queries_used`** lists the actual search queries executed.
8. **`timestamp`** is ISO 8601 format.
9. **Domain format**: always return full URL with `https://` scheme (e.g., `https://www.siemens.com`). If only `http://` is available, use that. If the domain redirects (e.g., `siemens.com` → `www.siemens.com`), use the final resolved URL.

## Example

**Input:**

| company_id | company_name | country_or_region |
|---|---|---|
| 1608750612 | Mubadala | 阿联酋 |

**Pipeline trace:**

1. **DISCOVER**: web_search `"Mubadala" official site` → found `mubadala.com` in results
2. **CORROBORATE**: Wikipedia article "Mubadala Investment Company" confirms `www.mubadala.com` in infobox
3. **VERIFY**: web_fetch `mubadala.com` → page title "Mubadala", footer "© Mubadala Investment Company PJSC"
4. **SCORE**: 2 independent sources + name match + country consistent → `high`

**Output file:** `results/20260417/company-domain-finder/1608750612.json`

```json
{
  "company_id": "1608750612",
  "company_name": "Mubadala",
  "country_or_region": "阿联酋",
  "official_domain": "https://www.mubadala.com/",
  "confidence_level": "high",
  "evidence_sources": [
    "https://en.wikipedia.org/wiki/Mubadala_Investment_Company — infobox website field",
    "https://www.mubadala.com/ — page title and footer copyright confirm company name"
  ],
  "search_methods": ["web_search", "wikipedia", "page_verify"],
  "search_queries_used": [
    "\"Mubadala\" official site",
    "\"Mubadala\" UAE official website",
    "\"Mubadala\" site:wikipedia.org"
  ],
  "timestamp": "2026-04-17T10:30:00+08:00"
}
```

## Search Failure Handling

If Stage 1 queries return no relevant results, try these steps before giving up:

1. **Simplify the query** — remove quotes, try the name without legal suffixes (e.g., "Ltd", "GmbH", "Inc", "SA", "AG")
2. **Try the local-language name** — if the company is from a non-English country, search for the name in the local language
3. **Switch search engines** — if Google returned nothing, try Bing or DuckDuckGo
4. **Broaden the scope** — search for the company name without "official site" qualifiers, and look for LinkedIn or Wikipedia results that may mention the website
5. **If all attempts fail**, proceed to Stage 4 with `official_domain: null`. Set `confidence_level` to `null` and briefly note in `evidence_sources` what was tried and why it failed (e.g., "3 queries across 2 engines returned no matching results").

## Search Strategies Reference

Country-specific query templates are organized by region in [references/search-strategies/](references/search-strategies/). Read `README.md` first to locate the correct regional file. Cross-validation and verification templates (Stage 2 & 3) are in [references/search-strategies/cross-validation.md](references/search-strategies/cross-validation.md).

## Country Registry Reference

Country-specific company registry sources for cross-validation are in [references/country-registries.md](references/country-registries.md). Read this file when Stage 2 results are ambiguous and registry confirmation would help.

## Output Template

The exact JSON structure is defined in [assets/templates/output-template.json](assets/templates/output-template.json). Before writing the output file, read this template to confirm all required fields are present in your result.

## Pre-Output Checklist

Before writing the JSON file:

- [ ] Was at least one search query executed?
- [ ] Were at least 2 different query patterns tried?
- [ ] Was cross-validation attempted (Wikipedia or second engine)?
- [ ] Was domain verification attempted for the top candidate?
- [ ] Is every JSON key present?
- [ ] Does `official_domain` contain the single best result (or `null` if none)?
- [ ] Is the file saved to `results/<YYYYMMDD>/company-domain-finder/<company_id>.json`?
