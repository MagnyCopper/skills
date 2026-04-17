# Cross-Validation & Verification Templates

These templates apply to Stage 2 (CORROBORATE) and Stage 3 (VERIFY) regardless of country.

## Stage 2 — Cross-Validation

### Wikipedia Lookup

```
# W-1: Wikipedia search
"<company_name>" site:wikipedia.org

# W-2: Specific language Wikipedia
"<company_name>" site:<lang>.wikipedia.org

# W-3: If Wikipedia article found, extract "Website" or "Official site" from infobox
```

Wikipedia infobox fields to check:
- `website`
- `homepage`
- `url`
- `official site`

### LinkedIn / Business Directory

```
# L-1: LinkedIn company page
"<company_name>" site:linkedin.com/company

# L-2: Bloomberg company profile
"<company_name>" site:bloomberg.com

# L-3: Crunchbase
"<company_name>" site:crunchbase.com
```

These sources often link to the official company website.

### Knowledge Graph / Search Features

When using built-in web_search, look for:
- Knowledge panel results (often show official website directly)
- "Official site" sitelinks in search results
- Featured snippets that reference the company website

## Stage 3 — Verification Queries

### Page Content Verification

After fetching a candidate domain's homepage, check for:

```
# V-1: Title tag contains company name
<title> contains <company_name> (or significant portion)

# V-2: Footer copyright
"© <year> <company_name>" or "© <company_name>"

# V-3: JSON-LD structured data
<script type="application/ld+json"> containing "@type": "Organization" with matching "name"

# V-4: About/Contact page
Navigate to /about, /about-us, /company, /contact and check for company name + address
```

### WHOIS / DNS Verification (if bash available)

```bash
# D-1: WHOIS lookup
whois <domain> | grep -i "registrant\|organization"

# D-2: DNS resolution
dig <domain> A +short
dig <domain> MX +short

# D-3: Check if domain resolves
curl -sI https://<domain> | head -5
```
