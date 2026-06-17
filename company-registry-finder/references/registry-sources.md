# Registry Sources (16 jurisdictions)

Reference table of official company registries used by the `company-registry-finder` DISCOVER stage.

## How to use this file

Load this during DISCOVER to route a lookup to the correct official registry by jurisdiction. Prefer the official URL first. If the "Free public search?" column says no, or the "Anti-bot / access notes" column flags a blocker, fall back to the listed 3rd-party aggregator (OpenCorporates unless noted). Use the Jurisdiction code map at the bottom to build OpenCorporates API calls.

## Official registries

| Country (EN / local) | Official registry (EN + local name) | Public lookup URL | Free public search? | Best 3rd-party aggregator | Anti-bot / access notes |
|---|---|---|---|---|---|
| Japan (日本) | National Tax Agency Corporate Number Publication Site / 国税庁法人番号公表サイト | https://www.houjin-bangou.nta.go.jp/ | Yes (13-digit corporate number) | OpenCorporates | JS-heavy; render with a browser |
| USA (multi-state) | Delaware Div. of Corporations; California Sec. of State; New York Dept. of State; Massachusetts Corporations Div. | DE: https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx<br>CA: https://bizfileonline.sos.ca.gov/search/business<br>NY: https://apps.dos.ny.gov/publicInquiry/ (verify)<br>MA: https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx | Free per state | OpenCorporates | Texas SOSDirect is paid; most US public semiconductors are DE-incorporated, so default to DE |
| UK | Companies House | https://find-and-update.company-information.service.gov.uk/search/companies | Yes (8-char company number) | OpenCorporates, Endole | API key required for the Companies House API; 600 req / 5 min limit |
| Germany (Deutschland) | Registerportal der Länder / Handelsregister | https://www.handelsregister.de/rp_web/normalesuche/welcome.xhtml | Yes (format "Amtsgericht X HRB 12345") | OpenCorporates, North Data | Registry warns against data mining; outputs are PDFs |
| France | INSEE Sirene / Répertoire Sirene | Search: https://recherche-entreprises.api.gouv.fr/search?q=<br>API: https://api.insee.fr/api-sirene/ | Yes (SIREN 9 / SIRET 14 digits) | OpenCorporates, Pappers | Full INSEE Sirene API needs a key; the recherche-entreprises endpoint is keyless |
| Korea (한국) | DART (전자공시시스템) + Hometax | https://englishdart.fss.or.kr/dsbb001/main.do | Partial (BRN 10 digits, "XXX-XX-XXXXX") | OpenCorporates | Hometax BRN lookup needs login; DART public disclosure covers listed companies |
| Hong Kong (香港) | Companies Registry / 公司註冊處 | https://www.cr.gov.hk/en/electronic/e-servicesportal/e-search.htm | Paid subscription (BRN 8 digits) | OpenCorporates | Gated; fall back to OpenCorporates + Wikipedia + press releases |
| Singapore | Bizfile / ACRA | https://www.bizfile.gov.sg/ | Free basic (UEN, alphanumeric 9-10 chars) | OpenCorporates | Full profiles are paid |
| Taiwan (台灣) | 商工登記公示資料查詢服務 / MOEA | https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do?request_locale=en | Yes (統一編號 8 digits) | OpenCorporates | Blocks scripted requests (403 on curl); works in a browser; prefers Chinese search terms |
| India | MCA / Ministry of Corporate Affairs | https://www.mca.gov.in/content/mca/global/en/mca/fo-llp-services/findCinFinalSingleCom.html | Yes but CAPTCHA (CIN 21 chars) | OpenCorporates, Zauba Corp | Use OpenCorporates or Zauba as primary |
| Canada | Corporations Canada + Canada's Business Registries | https://ised-isde.canada.ca/cc/lgcy/fdrlCrpSrch.html | Partial (federal corp # 7 digits, BN 9 digits) | OpenCorporates | ISED terms forbid automated mining; scraping is not allowed |
| Belgium (België) | KBO/BCE Public Search / Banque Carrefour des Entreprises | https://kbopub.economie.fgov.be/kbopub-m/search.exact?lang=en | Yes (10 digits, "0xxx.xxx.xxx", mod97 checksum) | OpenCorporates, Companyweb | Clean public endpoint, no login |
| Netherlands (Nederland) | KVK Handelsregister | Search: https://www.kvk.nl/en/search/<br>API: https://api.kvk.nl/api/v2/zoeken | Yes (8 digits) | OpenCorporates, North Data | KVK API returns 401 without an API key |
| Switzerland (Schweiz) | ZEFIX / Zentraler Firmenindex | Web: https://www.zefix.ch/en/search/entity/welcome<br>REST: https://www.zefix.admin.ch/ZefixPublicREST/ | Yes (UID "CHE-123.456.789", 9 digits + checksum) | OpenCorporates, Moneyhouse | Free web search and free REST API |
| Luxembourg | LBR / RCS (Registre de Commerce et des Sociétés) | https://www.lbr.lu/mjrcs-web-front/ | Free search (format "RCS B12345") | OpenCorporates | Document access requires login |
| Kazakhstan (Қазақстан) | eGov + stat.gov.kz BIN/IIN search | eGov: https://egov.kz/cms/en/services/business_registration/e_032<br>stat: https://stat.gov.kz/en/juridical/ | Not anonymous (BIN 12 digits) | OpenCorporates | eGov requires login / EDS; stat.gov.kz is open but lighter on detail |

## OpenCorporates API patterns

- Search by name: `https://api.opencorporates.com/v0.4/companies/search?q={name}&jurisdiction_code={jurisdiction}`
- Lookup by number: `https://api.opencorporates.com/v0.4/companies/{jurisdiction}/{company_number}`
- Human-readable entity page: `https://opencorporates.com/companies/{jurisdiction}/{company_number}`
- Rate limits: 200 requests/month and 50/day on the default free tier. Pagination is 30/page (up to 100/page via `per_page`).
- Auth: v0.4 API endpoints require an API key (free tier available). The unauthenticated HTML entity pages return 403 to curl; load them in a browser or use the API instead.

## Practical access notes

**Paid / login-only (use the free aggregator fallback):**
- Hong Kong Companies Registry: full e-search needs a paid subscription. OpenCorporates covers HK CR numbers.
- Luxembourg LBR/RCS: search is free, document access requires login.
- Texas SOSDirect: paid. Default to Delaware for US public companies.
- Korea Hometax: BRN lookup needs login. DART public disclosure is open and covers listed companies.

**CAPTCHA / anti-bot (use a browser or the aggregator):**
- India MCA: CAPTCHA on every search. Use OpenCorporates or Zauba Corp.
- Canada CBR (ISED): terms forbid automated mining. Use OpenCorporates.
- Germany Handelsregister: warns against data mining; outputs are PDFs.
- Taiwan findbiz: blocks scripted requests (403 on curl). Works in a browser, prefers Chinese search terms.
- OpenCorporates HTML entity pages: 403 to curl. Use the API or a browser.

**Best "free but partial" sources (good for CORROBORATE; confirm on the official registry for SCORE):**
- Singapore Bizfile: free basic search, paid full profiles.
- France Recherche des Entreprises: free, keyless; the full Sirene API needs a key.
- Netherlands KVK: free search; the KVK API needs a key (401 without).
- Switzerland ZEFIX: free web search and free REST API.
- Japan NTA Corporate Number site: free, 13-digit numbers.

## Jurisdiction code map

Country to OpenCorporates `jurisdiction_code` for the API patterns above.

| Country / region | jurisdiction_code |
|---|---|
| Japan | `jp` |
| USA (Delaware) | `us_de` |
| USA (California) | `us_ca` |
| USA (New York) | `us_ny` |
| USA (Massachusetts) | `us_ma` |
| United Kingdom | `gb` |
| Germany | `de` |
| France | `fr` |
| South Korea | `kr` |
| Hong Kong | `hk` |
| Singapore | `sg` |
| Taiwan | `tw` |
| India | `in` |
| Canada | `ca` |
| Belgium | `be` |
| Netherlands | `nl` |
| Switzerland | `ch` |
| Luxembourg | `lu` |
| Kazakhstan | `kz` |

OpenCorporates uses ISO 3166-1 alpha-2 for country-level codes (`gb`, not `uk`) and `us_<state>` for US states. A missing or wrong code returns an empty result rather than an error, so verify the code against the API before relying on it.
