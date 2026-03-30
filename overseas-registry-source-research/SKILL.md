---
name: overseas-registry-source-research
description: Use when the user wants to research official data sources and third-party data sources from a country, region, sector, regulator, target population, or other user-provided brief, and needs evidence-backed acquisition validation with executable artifacts rather than a narrative-only memo.
---

# Overseas Source Research

Turn a user-provided research brief into a data-source acquisition feasibility study.

The goal is not to produce a site list or a narrative report. The goal is to identify the most relevant official and third-party sources for the brief, verify what they expose, measure whether they can be traversed or downloaded, save small real artifacts, and recommend executable acquisition strategies.

## Do Not Use This Skill

- The user only needs a single lookup result from one source.
- The user only needs homepage field extraction from one site. Use `homepage-info-extractor`.
- The user only wants a pure legal, policy, or market memo without source testing or acquisition validation.
- The user only wants a generic web search summary with no artifact generation, access-path testing, or feasibility judgment.

## Priority Order

When time or budget is constrained, keep this order:

1. Parse the brief and define the research target clearly.
2. Sweep official sources.
3. Sweep local or domain-native third-party sources.
4. Sweep broader or global third-party sources.
5. Prove at least one minimum runnable acquisition path with real artifacts.
6. Expand descriptive background only as needed to explain the acquisition decision.

Do not skip local or domain-native third-party research just because a global provider is easier to name. If local or domain-native third-party sources are missing, weak, or non-executable, say so with evidence.

## Input Contract

Required:

- `research_brief`: a natural-language description of the data-source question, including the target geography, target object, filters, and desired data where available

Optional:

- `brief_slug`: lowercase letters, numbers, hyphens only; if missing, derive from the main research target
- `country_or_region`: reader-facing geography name when the brief is geography-bound
- `target_language`: default `中文`
- `generated_at`: default current date in `YYYY-MM-DD`
- `sample_size`: default `1000`; treat this as the target upper bound for one module sample, not a hard quota when the source is paid, capped, or otherwise constrained
- `template_path`: default `overseas-registry-source-research/assets/templates/registry-research-template.md`
- `time_limit_or_budget`: use to limit paid-source exploration or test depth
- `validation_depth`: default `deep`; use `minimum-runnable` only when the user explicitly wants the smallest viable proof
- `scoring_weights`: optional override for strategy synthesis

## Output Contract

Write results to this exact directory:

- `results/<YYYYMMDD>/overseas-registry-source-research/`

Do not reverse the nesting into `results/overseas-registry-source-research/<YYYYMMDD>/`.

Produce exactly one main report:

- `<brief-slug>-source-research.md`

For each selected module, produce:

- `<brief-slug>-<source-id>-<module-id>-download-sample.py`
- `<brief-slug>-<source-id>-<module-id>-test-dataset-<actual-sample-size>.<ext>` or a same-name directory when the source returns many raw files

For each selected module that uses search, pagination, or browser-gated access, also produce:

- `<brief-slug>-<source-id>-<module-id>-boundary-probe.json`

Optional helper artifact:

- `<brief-slug>-download-sample.py`

Hard rules:

- Use the fixed template at `assets/templates/registry-research-template.md`.
- Keep template-covered content inside the one main report. Do not split the analysis into extra Markdown files such as `sources.md`, `feasibility.md`, or `plan.md`.
- Use `temp/` only as a working directory, never as the final delivery directory.
- Keep sample files in the source's original downloadable format whenever possible.
- When a source cannot legally, safely, or economically reach the target `sample_size`, save the largest real raw sample you could obtain within constraints and state the actual size plus blocker evidence.
- If the user asks for minimum runnable validation, shrink breadth last, not first. Still include official sweep, third-party sweep, and at least one tested runnable path.

## Naming Rules

- `brief_slug`, `source_id`, `module_id`: lowercase letters, numbers, hyphens only
- Within one `source_id`, every `module_id` must be unique

## Shared Terminology

- `研究简述`: the user-provided brief that defines the target geography, object, filters, and desired data
- `数据源`: source at institution or platform level, such as a regulator, authority, public portal, exchange, association, open-data platform, local reseller, specialist vendor, or global provider
- `模块`: concrete executable entry under one source, such as an API, bulk package, search page, detail page, filing page, document service, export endpoint, or downloadable dataset
- `官方数据源`: a source controlled by a government, regulator, court, exchange, official registry, public body, or other authoritative institution directly tied to the brief
- `第三方数据源`: a non-official source that republishes, aggregates, indexes, enriches, or sells relevant data
- `当地第三方`: provider focused on the same country, region, or domain context as the brief
- `广域第三方`: broader multi-country or cross-market provider not primarily local to the target context

Do not force a fixed coverage model up front. Derive the relevant coverage dimensions from the brief after parsing it. Typical dimensions can include identity, qualification or license status, disclosure documents, market activity, enforcement history, ownership, product inventory, transaction data, or other brief-specific categories.

Also derive the record model from the brief before designing the sweep. The target may be entity-level, event-level, document-level, transaction-level, case-level, or another shape. Do not default to an entity-registry mental model when the brief is really about penalties, procurement events, court cases, filings, notices, or other non-entity records.

## Execution Gates

Follow this order. Do not skip a gate.

### Gate 0: Parse the brief into an operational research target

Before searching sources, extract and state all of these from the brief:

- target geography or jurisdiction
- target object or population
- mandatory filters or eligibility conditions
- desired data outputs
- likely official institutions
- likely third-party provider types
- derived coverage dimensions
- record model: entity, event, document, transaction, case, or other
- likely executable acquisition paths

Also resolve whether the brief depends on status edges such as licensed vs applying, active vs inactive, current vs historical, federal vs state vs municipal, or domestic vs cross-border. If such distinctions matter, make them explicit before source selection.

If the brief is ambiguous, choose the narrowest reasonable interpretation that still satisfies the user request, and state that interpretation in the report.

### Gate 1: Build the minimum background needed to interpret the brief

Collect only what is necessary to interpret acquisition feasibility:

- the institutional or market structure behind the brief
- the authority chain or disclosure chain that governs the target data
- the identifiers, licenses, documents, or classifications that connect the brief to concrete retrieval paths

Do not turn this section into broad country, sector, or industry research. Keep it lean.

### Gate 2: Sweep official sources first

Identify the official source categories implied by the brief. Typical categories may include:

1. primary regulator or licensing authority
2. official register or roster
3. government open-data portal
4. exchange, court, tribunal, procurement, or gazette platform
5. statistical, supervisory, or disclosure institution

Do not mechanically reuse a fixed category list when the brief implies different official channels.

When the target jurisdiction has parallel authorities at multiple levels, such as federal and state or central and municipal, do not declare the official sweep complete until you have checked whether those parallel levels materially affect coverage.

For each official source, record:

- institution name
- role in the brief
- main domain
- legal or license boundary
- access prerequisites
- whether it is authoritative for the target data

### Gate 3: Sweep third-party sources in the correct order

Do this in two passes:

1. local or domain-native third-party sweep
2. broader or global third-party sweep

For every third-party source, record:

- provider name
- class: `当地第三方` or `广域第三方`
- relevance to the brief
- access model: anonymous, signup, subscription, sales contact, KYC
- legal or license boundary
- whether it is selected

If a broader provider is selected ahead of a local or domain-native one, explain why with evidence. Acceptable reasons include:

- no credible local or domain-native provider found
- local or domain-native provider has materially weaker coverage
- local or domain-native provider fails executable validation
- local or domain-native provider exceeds budget or legal boundary

If you conclude that no credible local or domain-native provider exists, record the search path that led to that conclusion, including provider categories checked, representative search queries, and the stop condition. Do not make a shallow "none found" claim without search-path evidence.

### Gate 4: Build a full module census before selection

For each source under consideration, treat module discovery as a census task, not a shortlist task. List all modules relevant to the brief before choosing any of them.

Do not:

- pick only the easiest 1 or 2 modules
- split one institution into many fake sources
- ignore search modules only because bulk download looks easier

For every source card, report all of these:

- module census status: `complete` or `partial`
- discovered module count
- usable module count
- partially usable module count
- unusable module count
- unverified module count
- selected module count

If the census is not complete, label it `partial`, explain the stop condition, and avoid language that implies full coverage.

Search, lookup, and filter modules have special handling:

- If a search or lookup module exists, test it even if it will not be selected later.
- If no such module exists, write `未发现可执行检索模块` and attach search-path evidence.

For every discovered module row, always include:

- module URL or direct landing page URL
- relation to the brief
- URL liveness status: reachable, redirected, blocked, dead, or unverified
- availability status: `可用`, `部分可用`, `不可用`, or `未验证`
- download-feasibility status: `可执行`, `受限`, `不可执行`, or `未验证`
- concrete reason when the module is not fully usable

Do not list a module URL as if it were valid without checking whether it resolves to meaningful content. If the URL is dead, redirected to a generic page, login wall, or marketing shell, record that explicitly.

Preferred reason labels when applicable:

- `无公开入口`
- `仅产品页/仅营销页`
- `需登录`
- `需付费`
- `需KYC`
- `验证码/反爬`
- `403/封禁`
- `TLS/连接失败`
- `无结构化返回`
- `链路不稳定`
- `与简述不匹配`
- `未完成验证`

### Gate 5: Run the validation loop for every selected module

Each selected module must complete this loop:

1. access-path test
2. request and response analysis
3. boundary testing
4. downloader generation
5. real sample download
6. field-to-dimension mapping
7. usage verdict

Do not stop at qualitative conclusions.

#### Boundary testing requirements

Whenever applicable, measure and report actual values for:

- auth boundary: anonymous, signup, subscription, KYC
- maximum verified page size
- maximum verified offset or page depth
- single-query result cap
- rate-limit threshold or burst behavior
- captcha or anti-bot trigger point
- cursor or token expiry behavior
- date window, file window, or package-size limit
- response format and packaging

Measure actual values where safe, legal, and technically practical. Use documented vendor limits to complement live tests, and do not brute-force past published limits, login walls, paywalls, captchas, or protective controls merely to force a number.

If one metric does not apply, mark it `N/A` and explain why. If it applies but you could not safely or legally verify it, mark it `未验证`, record the blocker evidence, and report the highest safely verified value if you have one. Do not leave it blank.

For hard numeric boundary metrics, such as maximum page size, maximum offset, single-query cap, rate threshold, captcha trigger point, or token expiry, do not use `推断` as a substitute for a measured number. Use `已验证` with the measured value, or `未验证` with blocker evidence. `推断` is allowed only for contextual judgments that are not hard numeric limits.

#### Search and traversal testing requirements

For every search-capable module, state and test:

- supported search keys
- filter or faceting behavior
- fuzzy-search behavior when applicable
- whether traversal can approach useful coverage
- the hard boundary numbers behind that judgment

Traversal can include:

- keyword enumeration
- identifier range walking
- page walking
- alphabet or prefix partitioning
- filter slicing

If traversal is not feasible, show the boundary that breaks it, such as result caps, captchas, hard rate limits, weak identifiers, or legal restrictions. If the limit is only documented or indirectly observed, label that clearly rather than presenting it as directly verified.

Even when a module is not selected, still give it a clear usability verdict, direct URL, and unusable or constrained reason in the source-level module census.

### Gate 6: Generate scripts and save artifacts

Before writing a downloader from scratch, inspect `scripts/` and adapt the closest template.

Bundled templates:

- `scripts/http_download_template.py`: single-endpoint raw download skeleton
- `scripts/paginated_download_template.py`: page or offset-based raw download skeleton
- `scripts/search_boundary_probe.py`: search and pagination boundary probe
- `scripts/playwright_probe_template.py`: browser-gated source probe skeleton
- `scripts/validate_registry_artifacts.py`: output-structure validator

For each selected module, save:

- module-specific download script
- real sample artifact in original format
- boundary probe output when boundary testing applies

### Gate 7: Synthesize acquisition strategies

The final report must include all of these sections:

1. `官方主方案`: the best official-only executable path
2. `第三方组合方案`: the best executable third-party-led combination, respecting local-before-broad priority, or an explicit `无可执行第三方主组合` verdict with evidence
3. `备选方案`: at most one fallback combination
4. `最小可运行路径`: the smallest real path that already proves download feasibility

Use default scoring weights unless the user specifies otherwise:

- 时效性 `0.4`
- 规模 `0.3`
- 覆盖度 `0.3`

If two third-party choices score similarly, prefer the local or domain-native provider.

## Evidence Rules

Every key claim must include:

- source URL
- locator such as page section, button, parameter, endpoint path, or response field
- access prerequisite such as anonymous, signup, paid, KYC, or rate-limited
- test date

Explicit labels:

- `已验证`: tested directly
- `未验证`: not confirmed
- `推断`: inference based on evidence, not directly confirmed

Do not use `推断` to present an unmeasured hard boundary value as if it were an operational limit.

Additional rules:

- Coverage, update-frequency, and authority claims must be backed by a page, API response, filing page, dataset page, or equivalent source evidence.
- `合作洽谈` must be only `Y` or `N`, backed by pricing, terms, access-restriction, or sales-contact evidence.
- Legal and licensing claims should cite terms, copyright, robots, pricing, or portal-policy pages when available.
- Every discovered module row must show a direct module URL plus enough evidence to explain why it is usable, partially usable, unusable, or still unverified.

## Output Template

Always start from `assets/templates/registry-research-template.md`.

The template's section order, tables, and checklist are part of the contract. Keep the final report concise, but do not delete required sections. If the bottleneck is executable validation, spend the effort there rather than padding descriptive prose.

## Pre-Submission Checklist

- Did you write to `results/<YYYYMMDD>/overseas-registry-source-research/`?
- Is there exactly one main report Markdown?
- Does the main report include both `官方主方案` and `第三方组合方案`, even when the third-party outcome is `无可执行第三方主组合`?
- Did you parse the brief into a clear operational target before sweeping sources?
- Did you sweep official sources first?
- Did you sweep local or domain-native third-party sources before broader providers?
- Did you build module census lists before selecting modules?
- Does every source card show module census status and per-source module counts?
- Does every discovered module row include a module URL, relation to the brief, URL liveness status, availability status, download-feasibility status, and a reason when not fully usable?
- Did you test search modules or explicitly prove they do not exist?
- Did you record actual boundary numbers instead of only qualitative statements?
- Did you avoid presenting inferred numeric limits as if they were directly verified?
- Does every selected module have a download script and a real sample artifact?
- Does every applicable selected module have a boundary-probe artifact?
- Are sample files preserved in original source format?
- Did you avoid extra scattered Markdown outputs?
- Does every key judgment include reproducible evidence?
