# company-registry-finder 技术契约

本文档是 `company-registry-finder` 技能的运行时技术契约。它定义输入/输出 schema、五阶段流水线、置信度与关系枚举、强制规则，以及两个端到端示例。`SKILL.md` 是入口，本文件是细则。字段名必须与 `assets/templates/output-template.json` 完全一致，规范化必须与 `tests/eval.py` 等价。

---

## 1. 输入 schema

单次调用处理一家公司。输入字段如下。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 输出文件名。批量运行取测试集行号（3 位零填充，如 `001`）；单次运行取用户传入 id。 |
| `raw_name` | string | 是 | 非正式公司名，可能含括号国家/行业提示、缩写、旧称。原样读取，不要修改。 |
| `country_hint` | string \| null | 否 | 国家/地区提示（如 `Japan`、`美国`、`HK`）。强烈建议提供，直接决定 DISCOVER 路由。 |
| `industry_hint` | string \| null | 否 | 行业提示（如 `semiconductor`、`化学`）。辅助消歧。 |

`input.parsed_hints` 由 PARSE 阶段填充，不属于外部输入。

---

## 2. 输出 schema

写入 `results/<YYYYMMDD>/company-registry-finder/<id>.json`。所有字段名必须与 `output-template.json` 一致。未取得值时：字符串填 `""`，数组填 `[]`，可空对象填 `null`。不要省略字段。

### 2.1 顶层

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 透传输入 id。 |
| `input` | object | 回显输入与 PARSE 结果（见 §2.2）。 |
| `result` | object | 核验后的结果实体。无结果时各字段为空串/`null`，不要把整个对象置 `null`。 |
| `verification` | object | 核验证据与置信度（见 §2.4）。 |
| `evidence_sources` | array | 证据来源列表（见 §2.5）。 |
| `search_methods` | array[string] | 使用过的检索方法，如 `web_search`、`wikipedia`、`opencorporates`、`houjin-bangou.nta.go.jp`。 |
| `search_queries_used` | array[string] | 实际用过的查询串。 |
| `timestamp` | string | ISO 8601 写入时间戳。 |

### 2.2 `input`

| 字段 | 类型 | 说明 |
|---|---|---|
| `raw_name` | string | 原样透传。 |
| `country_hint` | string \| null | 原样透传。 |
| `industry_hint` | string \| null | 原样透传。 |
| `parsed_hints.detected_country` | string \| null | PARSE 推断的国家/地区（ISO alpha-2 或 `HK`/`TW`）。 |
| `parsed_hints.detected_script` | string \| null | 主文字脚本：`latin`、`cjk`、`hangul`、`mixed`。 |
| `parsed_hints.detected_language_hints` | array[string] | BCP 47 风格语言提示，如 `["ja","zh-Hant"]`。 |

### 2.3 `result`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `standard_name` | string | 是 | **当前注册法定名称**，本地脚本，如登记系统所载。 |
| `registered_jurisdiction` | string | 是 | ISO 3166-1 alpha-2 国家码；`HK`（香港）与 `TW`（台湾）作为覆盖值使用。美国统一填 `US`，州级信息放到 `registration_number_type`。 |
| `registered_address` | string | 是 | 当前注册办公地址（非历史地址）。无则 `""`。 |
| `registration_number` | string | 是 | 注册号。其 `normalize_regnum()` 结果必须等于官方登记记录的规范化形式。**不要**做美化重排（如把 `2246023` 补零成 `02246023`），否则会偏离评分器。 |
| `registration_number_type` | string | 是 | 注册号类型枚举（见下表）。 |
| `entity_status` | string | 是 | 枚举：`active`、`dissolved`、`merged`、`unknown`。 |
| `former_names` | array | 是 | `{name, changed_on}` 列表。无则 `[]`。 |
| `successor_entity` | object \| null | 是 | `{standard_name, registration_number, jurisdiction}` 或 `null`。 |

`registration_number_type` 允许值：

| 值 | 管辖区 | 形态 |
|---|---|---|
| `JP-法人番号` | 日本 | 13 位数字 |
| `US-DE-FileNumber` | 美国特拉华 | 6 至 8 位数字 |
| `US-CA-EntityNumber` | 美国加州 | 7 位，可带 `C`/`F` 前缀 |
| `US-NY-DOS_ID` | 美国纽约 | 6 至 7 位数字 |
| `GB-CompaniesHouse` | 英国 | 8 字符，可带 `SC`/`NI`/`OC` 前缀 |
| `DE-Handelsregister` | 德国 | `Amtsgericht <City> HRB <n>` |
| `FR-SIRET` | 法国 | 14 位（SIREN 9 + NIC 5） |
| `KR-BRN` | 韩国 | 10 位 |
| `HK-CR` | 中国香港 | 8 位 BR/CR 号 |
| `SG-UEN` | 新加坡 | 9 至 10 位字母数字 |
| `TW-統一編號` | 台湾 | 8 位 |
| `IN-CIN` | 印度 | 21 字符 CIN |
| `CA-CorpNumber` | 加拿大 | 7 位联邦号或 9 位 BN |
| `BE-KBO` | 比利时 | 10 位，mod97 |
| `NL-KvK` | 荷兰 | 8 位 KvK |
| `CH-UID` | 瑞士 | `CHE-123.456.789` |
| `LU-RCS` | 卢森堡 | `RCS B12345` |
| `KZ-BIN` | 哈萨克斯坦 | 12 位 BIN |

其他美国州按 `US-<STATE>-<TYPE>` 模式扩展，如 `US-MA-EntityNumber`。

### 2.4 `verification`

| 字段 | 类型 | 说明 |
|---|---|---|
| `confidence_level` | string | 枚举 `A`/`B`/`C`/`D`（见 §4）。**必填，不得省略。** |
| `relationship_to_target` | string | 枚举（见 §5）。**必填。** |
| `name_match_evidence` | string | 名称匹配证据：哪个来源、哪个页面、原文片段。 |
| `regnum_match_evidence` | string | 注册号匹配证据。 |
| `address_match_evidence` | string | 地址匹配证据。无则 `""`。 |
| `contradictions` | array[string] | 冲突与备选说明，每条尽量带来源 URL。无则 `[]`。 |

### 2.5 `evidence_sources[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `url` | string | 证据页 URL。只引用 `references/registry-sources.md` 已收录的官方/聚合域名，或可信新闻/维基 URL。 |
| `locator` | string | 页内定位，如 `Companies Registry > Public Search > Result row 1`。 |
| `snippet` | string | 原文摘录。 |
| `kind` | string | 枚举：`official_registry`、`third_party`、`news`、`wikipedia`、`regulatory_filing`。 |
| `accessed_at` | string | ISO 8601 访问时间戳。 |

任何非 null 结果，`evidence_sources` 至少 1 条。

---

## 3. 流水线细则

### 3.1 PARSE（解析）

剥离 `raw_name` 中的括号/方括号提示，检测国家、行业、文字脚本，并按 `references/name-normalization.md` 规范化清洗后的名称。规范化必须与 `tests/eval.py` 的 `normalize_name` / `normalize_regnum` 逐字节等价：NFC 折叠、全角转半角、小写、标点转空格（名称）或去前缀去分隔（注册号）。举例：`Dowa Holdings（同和控股）` 剥离后清洗名为 `Dowa Holdings`，提示含 `同和控股`（CJK），`detected_script=mixed`，`detected_language_hints=["ja","zh-Hant"]`。名称里的 `AXT, INC.` 规范化为 `axt inc`。

### 3.2 DISCOVER（发现）

采用**三层递进**策略，逐层扩大搜索范围：

**Tier 1：API 自动查询（快速覆盖上市公司/大型企业）**
- GLEIF LEI API（`api.gleif.org/api/v1/lei-records?filter[entity.legalName]=<name>`，免费无 key）：覆盖全球上市公司。返回 `legalName`、`jurisdiction`、`registeredAs`（注册号）、`status`。**注意**：GLEIF 可能返回错误管辖区（如 Indium Corporation 有 DE 文件号但实际在 NY 注册），需在 VERIFY 阶段确认正确的注册州。
- gBizINFO（`info.gbiz.go.jp`）：覆盖所有日本注册法人，是 JP 企业的**首选数据源**（比 NTA 更易查询）。
- Creditsafe / datalog.co.uk：覆盖美国/欧洲企业，返回注册号与注册州。

**Tier 2：Wikipedia + 官方登记系统（覆盖知名企业）**
- JP：`houjin-bangou.nta.go.jp`（法人番号公表サイト），可按 13 位号码验证名称与状态。
- GB：Companies House（`find-and-update.company-information.service.gov.uk`）。
- DE：`handelsregister.de`。
- FR：`recherche-entreprises.api.gouv.fr`。
- TW：`findbiz.nat.gov.tw`。
- Wikipedia 首段：捕捉 `"formerly"`、`"renamed"`、`"acquired by"`、`"merged"` 等改名/收购信号。**注意**：Wikipedia 搜索可能返回错误页面（如搜索 "Mitsubishi Electric" 可能返回地铁车辆页面），必须核对页面内容与目标公司匹配。

**Tier 3：Web 搜索（覆盖中小企业/私有公司）**
- 使用 `websearch_web_search_exa` 搜索 `"<company name> <jurisdiction> registration number"` 或 `"<company name> 法人番号"`（JP）。
- 搜索结果中的 gBizINFO 页面（`info.gbiz.go.jp/hojin/ichiran?hojinBango=<number>`）是 JP 企业注册号的可靠来源。
- SEC EDGAR 文件（`sec.gov`）是美国上市公司的可靠注册号来源。

**多管辖区消歧规则**：当同一公司在多个州/国家有注册时，返回与 `country_hint` 或行业背景最匹配的注册实体，不要返回任意一个。例如 Indium Corporation 应返回 NY DOS ID 46622（注册州），而非 DE 文件号 2787375（仅在 DE 有登记代理）。

**括号覆盖规则**：当 `raw_name` 的括号内容与主名指向不同实体时（如 `圣戈班 (Soitec)`），括号内的名称是真实目标，主名仅提供背景。

### 3.3 CORROBORATE（印证）

候选只有在 ≥2 个**独立来源**就名称或注册号达成一致时才推进。独立的判定标准是来源 `kind` 不同：`official_registry` + `wikipedia` 算独立；`wikipedia` + `news` 不算（新闻常援引维基）。OpenCorporates 与官方登记系统若数据同源，视为同一 `kind` 口径下的印证，需要再补一个不同 `kind` 的来源。

### 3.4 VERIFY（核验）

命中候选管辖区的官方登记页面，按 `references/disambiguation-rules.md` 解析改名/收购链。必做项：核对 `entity_status`（active/dissolved/merged）；若登记记录暴露 `former_names`/`previous_names`，走链匹配旧名；若已解散且带后继者字段（JP 的 `successorCorporateNumber`、GB 的后继链接），跟随到存续实体；按 `references/number-formats.md` 校验注册号格式与校验位（JP 加权和、FR Luhn、BE mod97、KR 加权和、TW 加权和等）。确认 `registered_address` 是当前注册办公地址，而非历史地址。

### 3.5 SCORE（评分）

按 §4 赋予 `confidence_level`。低于 C 时用改写后的查询重试 DISCOVER：换拼写/罗马化变体、用旧名查询（改名案）、用母公司查询（子公司案）。最多重试 2 次。仍低于 C 时，以最佳猜测落盘，`confidence_level=D`，并把所有冲突写入 `verification.contradictions`。

---

## 4. `confidence_level` 表

| 级别 | 含义 |
|---|---|
| **A** | 官方登记系统确认**全部三项**：名称 + 注册号 + 地址。 |
| **B** | 官方登记系统确认**三选二**（通常是名称 + 注册号）。 |
| **C** | 仅有第三方印证（OpenCorporates、Wikipedia、新闻），无官方登记命中。 |
| **D** | 单一来源、猜测、或改名链未经验证。 |

`confidence_level < C` 必须触发一次用改写查询的 DISCOVER 重试。

---

## 5. `relationship_to_target` 枚举

| 值 | 含义 | 可推进到 SCORE？ |
|---|---|---|
| `same_entity` | 直接匹配 | 是 |
| `former_name_of_current_entity` | 改名案，输入是当前实体的旧名 | 是 |
| `acquired_absorbed_by_current` | 收购/吸收案，目标已被当前实体吸收 | 是 |
| `subsidiary_of_target` | 方向反了（候选是目标的子公司） | 否，重试或 null |
| `parent_or_group_entity` | 方向反了（候选是母公司/集团） | 否 |
| `branch_or_local_office` | 层级错（分支机构/办事处） | 否 |
| `same_name_different_jurisdiction` | 同名异国，无法定位 | 否 |
| `brand_or_product_name` | 不是法人主体，是品牌/产品 | 否 |
| `dissolved_no_successor` | 死胡同，已解散无后继 | 否 |
| `unknown` | 关系不明 | 重试 |

只有 `same_entity`、`former_name_of_current_entity`、`acquired_absorbed_by_current` 可以推进到 SCORE 并写入 `result`。其余触发重试，或产出 null 结果。

---

## 6. MUST DO 规则

1. **先建目录再写文件**：`mkdir -p results/<YYYYMMDD>/company-registry-finder/`，然后写 `<id>.json`。
2. **无结果也要落盘**：写符合 schema 的 null 结果文件，不要只输出到对话。
3. **PARSE 必须提取国家提示**：从括号/方括号/上下文推断 `country_hint`，填入 `input.parsed_hints.detected_country`。
4. **比较前必须规范化**：名称与注册号按 `references/name-normalization.md` 规范化，行为与 `tests/eval.py` 等价。
5. **DISCOVER 优先官方登记系统**：按检测到的管辖区路由到 `references/registry-sources.md` 的官方源。
6. **B 及以上需要 ≥2 个独立 `kind` 来源**：`wikipedia` + `news` 不算独立。
7. **VERIFY 必须核对 `entity_status`**：改名/收购按 `references/disambiguation-rules.md` 走链，绝不返回已解散前身。
8. **注册号按 `references/number-formats.md` 校验**：发出的形式经 `normalize_regnum` 后必须等于官方记录。禁止美化补零或重排。
9. **非 null 结果必须带 `evidence_sources`**：至少 1 条，含 URL、定位器、原文片段、`kind`、访问时间。
10. **冲突必须记录**：任何冲突或被否决的备选写入 `verification.contradictions`，尽量带来源 URL。
11. **以 `output-template.json` 为骨架**：字段名与类型逐一对齐，不增不减。
12. **低于 C 必须重试**：用改写查询重试 DISCOVER，最多 2 次。
13. **清算不等于解散**：如果输入名与注册系统中的实体精确匹配，即使该实体处于 liquidation（清算）状态，也必须返回该实体本身（`entity_status` 标为 `active` 或 `dissolved` 视实际状态而定）。只有在实体被**正式注销/解散（formally dissolved/deregistered）**且有 `successor_entity` 时才走后继链。清算中的实体仍是合法存续的注册主体。
14. **官方登记系统搜索失败时回退**：当官方登记系统在 2 次尝试后仍无结果，必须使用 OpenCorporates API (`api.opencorporates.com/v0.4/companies/search?q=<name>&jurisdiction_code=<code>`) 或 GLEIF LEI 数据库 (`search.gleif.org`) 作为注册号验证的回退源。在 `evidence_sources` 中标注 `kind` 为 `third_party` 或 `regulatory_filing`（GLEIF LEI 属监管文件级别）。

---

## 7. MUST NOT DO 规则

1. **绝不返回 `entity_status=dissolved` 的实体而不提供 `successor_entity`**。已解散前身永远不是答案。
2. **绝不把品牌名当法人主体返回**：`onsemi` 是品牌，`ON SEMICONDUCTOR CORPORATION` 才是法定名。
3. **`confidence_level >= B` 时，不得把 Wikipedia 作为唯一来源**。
4. **不得混淆子公司与母公司**：用 `country_hint` 与注册号共同定位目标层级；返回目标本身，不是它的所有者。
5. **不得编造注册号**：无法核验时留空并降级，不要凑数。
6. **不得省略 `verification.confidence_level`**，且值只能取 `A`/`B`/`C`/`D`。
7. **不得写到规定路径以外**：只能是 `results/<YYYYMMDD>/company-registry-finder/<id>.json`。
8. **即使候选置信度很高，也不得跳过 VERIFY 阶段**：官方登记页面的核验是必经步骤。
9. **改名/收购判定不得仅凭单篇新闻报道**：需官方登记系统、监管文件（US 8-K、JP TSE 披露、FR BODACC、DE Bundesanzeiger）或公司自身新闻稿背书。
10. **不得做音译、罗马化或法定后缀归一**：`Ltd` 与 `Limited` 保持不同；CJK 按本地脚本输出。
11. **不得对注册号做美化补零或重排**：例如不要把 `2246023` 改成 `02246023`，否则偏离评分器的精确匹配。
12. **不得用 `as any` / 类型抑制式做法绕过 schema 校验**：字段类型必须与 `output-template.json` 完全一致。（此为原则性规则：任何代码实现都不得对 schema 字段做类型强转或抑制。）

---

## 8. 工作示例 1：简单案例（行 1，HK）

**输入：**

```json
{"id":"001","raw_name":"Dowa Holdings（同和控股）","country_hint":null,"industry_hint":null}
```

**PARSE**：剥离 `（同和控股）`，清洗名为 `Dowa Holdings`。提示含 CJK `同和控股`，`detected_script=mixed`，`detected_language_hints=["ja","zh-Hant"]`。`同和控股` 是 Dowa Holdings 的中文写法；结合 HK 存续实体为目标，`detected_country=HK`。

**DISCOVER**：路由到 HK Companies Registry（`cr.gov.hk`，付费，回退 OpenCorporates）。查询 `Dowa Holdings Hong Kong`、`同和控股 site:cr.gov.hk`、`opencorporates "Dowa Holdings" hk`。命中 HK CR 记录：`中國同和控股集團有限公司`，CR 号 `2246023`。Wikipedia 与公司年报印证同一 HK 主体。

**CORROBORATE**：OpenCorporates（`third_party`，转发 HK CR 数据）与公司年度报告（`regulatory_filing`）就名称与 CR 号一致，满足 ≥2 个独立 `kind`。

**VERIFY**：CR 号 `2246023` 形态符合 HK BRN（8 位，本例为去前导零的 7 位，按评分器规范化口径原样发出）。`entity_status=active`，无 `former_names`，无后继者。无改名/收购链需要走。地址取自最新年报的注册办公地址。

**SCORE**：官方登记数据（经 OpenCorporates 转发）加监管文件确认名称 + 号码 + 地址，赋 `confidence_level=A`，`relationship_to_target=same_entity`。

**输出（节选）：**

```json
{
  "id": "001",
  "input": {
    "raw_name": "Dowa Holdings（同和控股）",
    "country_hint": null,
    "industry_hint": null,
    "parsed_hints": {
      "detected_country": "HK",
      "detected_script": "mixed",
      "detected_language_hints": ["ja", "zh-Hant"]
    }
  },
  "result": {
    "standard_name": "中國同和控股集團有限公司",
    "registered_jurisdiction": "HK",
    "registered_address": "",
    "registration_number": "2246023",
    "registration_number_type": "HK-CR",
    "entity_status": "active",
    "former_names": [],
    "successor_entity": null
  },
  "verification": {
    "confidence_level": "A",
    "relationship_to_target": "same_entity",
    "name_match_evidence": "OpenCorporates HK 记录名称 = 中國同和控股集團有限公司，与输入同和控股对应",
    "regnum_match_evidence": "HK CR 2246023，OpenCorporates 转发自 cr.gov.hk",
    "address_match_evidence": "",
    "contradictions": []
  },
  "evidence_sources": [
    {
      "url": "https://opencorporates.com/companies/hk/2246023",
      "locator": "OpenCorporates HK entity page",
      "snippet": "中國同和控股集團有限公司, CR 2246023",
      "kind": "third_party",
      "accessed_at": "2026-06-17T00:00:00Z"
    }
  ],
  "search_methods": ["web_search", "wikipedia", "opencorporates"],
  "search_queries_used": ["Dowa Holdings Hong Kong", "同和控股 site:cr.gov.hk"],
  "timestamp": "2026-06-17T00:00:00Z"
}
```

---

## 9. 工作示例 2：改名案例（行 52，JP）

**输入：**

```json
{"id":"052","raw_name":"Hitachi Metals, Ltd.","country_hint":null,"industry_hint":null}
```

**PARSE**：无括号提示，清洗名 `Hitachi Metals, Ltd.`（规范化为 `hitachi metals ltd`）。`detected_script=latin`，`detected_language_hints=["en"]`。由 "Hitachi" 推断 `detected_country=JP`。

**DISCOVER**：路由到 JP `houjin-bangou.nta.go.jp`。查询 `"Hitachi Metals" 法人番号`、`Hitachi Metals renamed Proterial`、`site:houjin-bangou.nta.go.jp "日立金属"`。Wikipedia 首段给出信号："formerly Hitachi Metals, renamed Proterial on 2023-01-04"。NTA 法人番号站点命中法人番号 `3010401038783`，当前名 `株式会社プロテリアル`。

**CORROBORATE**：Wikipedia（`wikipedia`）与 NTA 法人番号站点（`official_registry`）就旧名 `日立金属`/`Hitachi Metals` 到当前 `株式会社プロテリアル`、号码 `3010401038783` 一致。Proterial 官方新闻稿（`regulatory_filing`）载明 2023-01-04 改名生效。

**VERIFY**：按 `disambiguation-rules.md` Part 1，JP 法人番号跨改名稳定。Part 2 走改名链：登记记录 `former_names` 含 `株式会社日立金属`，`changed_on=2023-01-04`，与输入旧名匹配。`entity_status=active`，无 `successorCorporateNumber`（非合并，仅改名）。法人番号 `3010401038783` 通过 JP 加权和校验。锁定当前实体。

**SCORE**：官方登记系统（NTA）确认名称 + 号码，赋 `confidence_level=A`，`relationship_to_target=former_name_of_current_entity`，`former_names=[{name:"株式会社日立金属", changed_on:"2023-01-04"}]`。

**输出（节选）：**

```json
{
  "id": "052",
  "input": {
    "raw_name": "Hitachi Metals, Ltd.",
    "country_hint": null,
    "industry_hint": null,
    "parsed_hints": {
      "detected_country": "JP",
      "detected_script": "latin",
      "detected_language_hints": ["en"]
    }
  },
  "result": {
    "standard_name": "株式会社プロテリアル",
    "registered_jurisdiction": "JP",
    "registered_address": "",
    "registration_number": "3010401038783",
    "registration_number_type": "JP-法人番号",
    "entity_status": "active",
    "former_names": [
      {"name": "株式会社日立金属", "changed_on": "2023-01-04"}
    ],
    "successor_entity": null
  },
  "verification": {
    "confidence_level": "A",
    "relationship_to_target": "former_name_of_current_entity",
    "name_match_evidence": "NTA 法人番号 3010401038783 旧商号 株式会社日立金属 = 输入 Hitachi Metals 的日文形式",
    "regnum_match_evidence": "法人番号 3010401038783，JP 加权和校验通过，跨改名稳定",
    "address_match_evidence": "",
    "contradictions": []
  },
  "evidence_sources": [
    {
      "url": "https://www.houjin-bangou.nta.go.jp/",
      "locator": "NTA 法人番号公表サイト > 3010401038783",
      "snippet": "株式会社プロテリアル, 旧商号 株式会社日立金属",
      "kind": "official_registry",
      "accessed_at": "2026-06-17T00:00:00Z"
    }
  ],
  "search_methods": ["web_search", "wikipedia", "houjin-bangou.nta.go.jp"],
  "search_queries_used": ["Hitachi Metals renamed Proterial", "site:houjin-bangou.nta.go.jp 日立金属"],
  "timestamp": "2026-06-17T00:00:00Z"
}
```
