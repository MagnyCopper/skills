# Data Source Section Template

Use this template for each selected Data Product section in the final combined report.

## Data Source Section: `<authority_id>` / `<product_id>`

### 1. Basic Info
- country_or_region: `<country_or_region>`
- authority_source: `<authority_name>`
- data_product: `<product_name>`
- product_id: `<product_id>`
- source_homepage_url: `<source_homepage_url>`
- product_entry_url: `<product_entry_url>`
- authority_scope: `<authority_scope>`
- legal_or_license_boundary: `<license_or_terms>`

### 2. Enterprise-Centric Positioning
- primary_enterprise_key: `<company_number_or_registry_id>`
- fallback_keys: `<name/address/date/...>`
- product_role: `identity | status | governance | financials | compliance_docs`
- incremental_value_on_enterprise_axis: `<what_new_dimensions_added>`

### 3. MCP Validation Record (Required)
- test_date: `<YYYY-MM-DD>`
- method: `Playwright MCP / equivalent automation / manual fallback`
- access_chain_result: `success / failed`
- query_pagination_result: `<how_query_and_pagination_work>`
- auth_requirement: `anonymous / registration / KYC / paid`
- anti_bot_or_rate_limit: `<rate_limit_or_captcha>`
- evidence:
  - page_url: `<url>`
  - locator: `<button/section/query-param/api-path>`
  - artifacts: `<screenshot/log/path>`

### 4. Data Loading Analysis
- acquisition_mode: `API / bulk package / web search / document service`
- endpoint_or_download_url: `<endpoint_or_download_url>`
- request_params: `<params>`
- response_shape: `<json/csv/schema_summary>`
- update_cycle_evidence: `<page label or metadata field>`

### 5. Download Test (`sample_size=<N>`)
- script_file: `<country>-<authority-id>-<product-id>-download-sample.py`
- sample_file: `<country>-<authority-id>-<product-id>-test-dataset-<N>.<ext>`
- result: `success / failed`
- downloaded_count: `<count>`
- throughput_and_duration: `<records_per_sec / duration>`
- retry_and_resume_strategy: `<strategy>`

### 6. Field-Level Dimensions
| field | meaning | availability | free_or_paid | prerequisite | source_locator |
|---|---|---|---|---|---|
| `<field_1>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |
| `<field_2>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |

### 7. Required Coverage Dimensions Mapping
- business_registration_core: `<available/partial/unavailable>` + note
- branches: `<available/partial/unavailable>` + note
- executives_team: `<available/partial/unavailable>` + note
- shareholders_board: `<available/partial/unavailable>` + note
- purchasable_documents: `<available/partial/unavailable>` + note

### 8. Single-Source Conclusion
- executability_rating: `high / medium / low`
- key_risks: `<risk_1>; <risk_2>`
- best_use_case: `initialization / incremental / backfill / verification`
- include_in_combo: `yes / no`
- inclusion_reason: `<reason>`

### 9. Position in Final Combo
- role_in_primary_combo: `<role>`
- role_in_fallback_combo: `<role>`
- conflict_priority: `<authority-level priority>`
