# Combined Research and Download Plan Template

## Report Metadata
- country_or_region: `<country_or_region>`
- report_language: `<target_language>`
- generated_at: `<YYYY-MM-DD>`
- sample_size: `<sample_size>`

## Authority Source Summary
- authority_id: `<authority_id>`
  - authority_name: `<authority_name>`
  - scope: `<scope>`
  - domains: `<domain list>`
  - legal_boundary: `<legal/licensing notes>`

## Data Product Sections (Required)
Repeat one full section per selected product, using:
`overseas-registry-source-research/assets/templates/source-section-template.md`

## Enterprise-Centric Merge Strategy
- primary_key_strategy: `<strategy>`
- fallback_key_strategy: `<strategy>`
- dimension_merge_rules: `<rules>`
- authority_conflict_priority: `<priority order>`

## Combo Scoring and Recommendation
- scoring_weights: `timeliness=0.4, volume=0.3, coverage=0.3`
- candidate_combos: `<list with evidence and scores>`
- Primary Combo: `<only one>`
- Fallback Combo: `<zero or one>`
- remaining_gaps_and_reasons: `<gaps>`

## Final Download Plan
- initialization_plan: `<full load plan>`
- incremental_plan: `<delta plan>`
- backfill_plan: `<backfill plan>`
- retry_resume_plan: `<retry/resume plan>`
- throughput_eta_estimate: `<estimate>`
