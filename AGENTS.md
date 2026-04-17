# Repository Guidelines

## Project Structure & Module Organization
This repository is organized around **skills**, each stored as a top-level directory.

- `README.md`: repository overview.
- `homepage-info-extractor/`: extract specified fields from company official homepages.
  - `homepage-info-extractor/SKILL.md`: canonical skill definition and workflow.
  - `homepage-info-extractor/assets/templates/template-table.md`: fixed output template for homepage extraction tasks.
  - `homepage-info-extractor/references/`: supporting reference material.
- `company-domain-finder/`: find a company's official website domain given its name and country/region.
  - `company-domain-finder/SKILL.md`: skill definition with 4-stage pipeline (DISCOVER → CORROBORATE → VERIFY → SCORE).
  - `company-domain-finder/assets/templates/output-template.json`: fixed JSON output template.
  - `company-domain-finder/references/search-strategies/`: country-specific search query templates organized by region.
  - `company-domain-finder/references/country-registries.md`: official company registries by country for cross-validation.
- `overseas-registry-source-research/`: research official data sources from a country/region/sector.
- `results/`: generated outputs. Store files under `results/<YYYYMMDD>/<skill-name>/` (create directories if missing).

Example output paths:
- `results/20260202/homepage-info-extractor/example.com.md`
- `results/20260417/company-domain-finder/1608750612.json`

## Build, Test, and Development Commands
No build system or automated test runner is configured.

Use lightweight CLI checks during development:

- `rg --files`: list repository files quickly.
- `rg "pattern" <skill-name>/`: search skill content.
- `ls results/`: verify generated artifact directories and naming.

## Coding Style & Naming Conventions
- Write documentation in concise Markdown with clear headings.
- Prefer ASCII by default.
- Use **kebab-case** for skill directory names (e.g., `homepage-info-extractor/`).
- Keep generated result paths deterministic: `results/<YYYYMMDD>/<skill-name>/...`.
- Avoid adding unrelated scaffolding (scripts, configs) unless required by a task.

## Testing Guidelines
There is no formal test framework. Validate changes by manual checks:

- Markdown renders correctly.
- Paths referenced in docs exist.
- Output paths match the required pattern.
- Skill instructions remain internally consistent.

For extraction tasks, verify fields are copied from source text exactly and traceable to source URL/locator.

For domain finder tasks, verify the JSON output matches the template schema and the domain is verifiable.

## Commit & Pull Request Guidelines
Commit history is lightweight, so use short imperative commit messages, e.g.:

- `Add homepage info extractor skill`
- `Update extraction template wording`
- `Add company-domain-finder skill`

PRs should include:

- What changed and why.
- Affected file paths.
- Example output path when result generation behavior changes.

## Agent-Specific Instructions
- Define each skill inside its own directory with a `SKILL.md` file.
- For homepage extraction, follow the `homepage-info-extractor` rules strictly: original text only, include source URL and locator, and use the fixed template at `homepage-info-extractor/assets/templates/template-table.md`.
- For domain finding, follow the `company-domain-finder` pipeline: always execute all 4 stages, return exactly one best domain, and use the fixed JSON template at `company-domain-finder/assets/templates/output-template.json`.
