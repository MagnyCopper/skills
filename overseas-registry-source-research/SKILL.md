---
name: overseas-registry-source-research
description: Use when the user wants to research company registry or business registration sources for a country or region, compare official registries with local and global third-party providers, test download feasibility, search behavior, or access limits, or design a repeatable acquisition plan with sample files and reproducible evidence.
---

# Overseas Registry Source Research

Turn a country-level registry-source question into an acquisition feasibility study.

The goal is not to produce a site list or a narrative report. The goal is to find as many relevant sources as practical, validate what they expose, measure whether they can be downloaded or traversed, save small real artifacts, and recommend executable acquisition strategies.

## Do Not Use This Skill

- The user only needs a single-company lookup result.
- The user only needs homepage field extraction from one site. Use `homepage-info-extractor`.
- The user only wants a pure legal memo without source testing or acquisition validation.

## Priority Order

When time or budget is constrained, keep this order:

1. Sweep official sources.
2. Sweep local third-party sources.
3. Sweep global third-party sources.
4. Prove at least one minimum runnable download path with real artifacts.
5. Expand background and descriptive coverage only as needed to explain the acquisition decision.

Do not skip local third-party research just because a global provider is easier to name. If local third-party sources are missing, weak, or non-executable, say so with evidence.

## Input Contract

Required:

- `country_or_region`: reader-facing country or region name
- `country_or_region_slug`: lowercase letters, numbers, hyphens only

Optional:

- `target_language`: default `中文`
- `generated_at`: default current date in `YYYY-MM-DD`
- `sample_size`: default `1000`; treat this as the target upper bound for one module sample, not a hard quota when the source is paid, capped, or otherwise constrained
- `template_path`: default `overseas-registry-source-research/assets/templates/registry-research-template.md`
- `time_limit_or_budget`: use to limit paid-source exploration or test depth
- `validation_depth`: default `deep`; use `minimum-runnable` only when the user explicitly wants the smallest viable proof

## Output Contract

Write results to this exact directory:

- `results/<YYYYMMDD>/overseas-registry-source-research/`

Do not reverse the nesting into `results/overseas-registry-source-research/<YYYYMMDD>/`.

Produce exactly one main report:

- `<country-or-region-slug>-registry-source-research.md`

For each selected module, produce:

- `<country-or-region-slug>-<source-id>-<module-id>-download-sample.py`
- `<country-or-region-slug>-<source-id>-<module-id>-test-dataset-<actual-sample-size>.<ext>` or a same-name directory when the source returns many raw files

For each selected module that uses search, pagination, or browser-gated access, also produce:

- `<country-or-region-slug>-<source-id>-<module-id>-boundary-probe.json`

Optional helper artifact:

- `<country-or-region-slug>-download-sample.py`

Hard rules:

- Use the fixed template at `assets/templates/registry-research-template.md`.
- Keep template-covered content inside the one main report. Do not split the analysis into extra Markdown files such as `sources.md`, `feasibility.md`, or `plan.md`.
- Use `temp/` only as a working directory, never as the final delivery directory.
- Keep sample files in the source's original downloadable format whenever possible.
- When a source cannot legally, safely, or economically reach the target `sample_size`, save the largest real raw sample you could obtain within constraints and state the actual size plus blocker evidence.
- If the user asks for minimum runnable validation, shrink breadth last, not first. Still include official sweep, local third-party sweep, and at least one tested runnable path.

## Naming Rules

- `source_id`: lowercase letters, numbers, hyphens only, for example `israel-companies-authority`
- `module_id`: lowercase letters, numbers, hyphens only, for example `company-search`
- Within one `source_id`, every `module_id` must be unique

## Shared Terminology

- `数据源`: source at institution or platform level, such as a registry authority, tax authority, open-data portal, local reseller, or global provider
- `模块`: concrete executable entry under one source, such as an API, bulk package, search page, detail page, or document service

Use these fixed coverage dimensions:

- 主体识别
- 状态与生命周期
- 治理信息
- 财务信息
- 合规文档

Use these fixed third-party classes:

- `当地第三方`: provider focused on the same country or region, or clearly operating with local registry coverage and local commercial context
- `国际第三方`: global or multi-country provider not primarily local to the target jurisdiction

## Execution Gates

Follow this order. Do not skip a gate.

### Gate 1: Build the minimum country background

Collect only what is necessary to interpret acquisition feasibility:

- registry governance level
- enterprise registration flow
- identifier systems tied to company lookup or download

Do not turn this section into general country research. Keep it lean.

### Gate 2: Sweep official sources first

Check at least these official categories. If one does not exist or is not relevant, record evidence:

1. company registry or corporate affairs authority
2. tax authority
3. government open-data portal
4. securities or financial regulator
5. statistical agency

For each official source, record:

- institution name
- scope of responsibility
- main domain
- legal or license boundary
- access prerequisites

### Gate 3: Sweep third-party sources in the correct order

Do this in two passes:

1. local third-party sweep
2. global third-party sweep

For every third-party source, record:

- provider name
- class: `当地第三方` or `国际第三方`
- target-country relevance
- access model: anonymous, signup, subscription, sales contact, KYC
- legal or license boundary
- whether it is selected

If a global provider is selected ahead of a local one, explain why with evidence. Acceptable reasons include:

- no credible local provider found
- local provider has materially weaker coverage
- local provider fails executable validation
- local provider exceeds budget or legal boundary

### Gate 4: Build a full module census before selection

For each source under consideration, treat module discovery as a census task, not a shortlist task. List all enterprise-related modules you can find before choosing any of them.

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

Search or lookup modules have special handling:

- If a name or identifier search module exists, test it even if it will not be selected later.
- If no such module exists, write `未发现名称或编号检索模块` and attach search-path evidence.

For every discovered module row, always include:

- module URL or direct landing page URL
- availability status: `可用`, `部分可用`, `不可用`, or `未验证`
- download-feasibility status: `可执行`, `受限`, `不可执行`, or `未验证`
- concrete reason when the module is not fully usable

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

#### Search and collision testing requirements

For every search-capable module, state and test:

- supported search keys: name, registration number, tax number, address, officer, or others
- fuzzy-search behavior: prefix, contains, approximate, phonetic, or unsupported
- whether collision-style traversal can approach full coverage
- the hard boundary numbers behind that judgment

Collision-style traversal can include:

- keyword enumeration
- registration-number range walking
- page walking
- alphabet or prefix partitioning

If collision-style traversal is not feasible, show the boundary that breaks it, such as result caps, captchas, hard rate limits, or legal restrictions. If the limit is only documented or indirectly observed, label that clearly rather than presenting it as directly verified.

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
2. `第三方组合方案`: the best executable third-party-led combination, respecting local-before-global priority, or an explicit `无可执行第三方主组合` verdict with evidence
3. `备选方案`: at most one fallback combination
4. `最小可运行路径`: the smallest real path that already proves download feasibility

Use default scoring weights unless the user specifies otherwise:

- 时效性 `0.4`
- 规模 `0.3`
- 覆盖度 `0.3`

If two third-party choices score similarly, prefer the local provider.

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

Additional rules:

- Update-frequency claims must be backed by a page or API response.
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
- Did you sweep official sources first?
- Did you sweep local third-party sources before global ones?
- Did you build module census lists before selecting modules?
- Does every source card show module census status and per-source module counts?
- Does every discovered module row include a module URL, availability status, download-feasibility status, and a reason when not fully usable?
- Did you test search modules or explicitly prove they do not exist?
- Did you record actual boundary numbers instead of only qualitative statements?
- Does every selected module have a download script and a real sample artifact?
- Does every applicable selected module have a boundary-probe artifact?
- Are sample files preserved in original source format?
- Did you avoid extra scattered Markdown outputs?
- Does every key judgment include reproducible evidence?
