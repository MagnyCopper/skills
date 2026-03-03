# 😀 <国家/地区名称>

# 概况

## **基本信息**

- 简称：<简称>
- 所属洲：<所属洲>
- 首都：<首都（本地语言/英文）>
- 官方语言：<官方语言>
- 货币：<货币名称, 代码>
- 国土面积：<面积 + 单位>
- 人口：<人口规模 + 年份>
- 企业总量：<企业总量 + 口径 + 年份>

证据来源：
- URL：<url>
- 定位：<页面栏目/表格名/接口字段>

## **政治体制**

<填写与企业登记制度相关的政治/行政层级背景；保持客观、可验证>

证据来源：
- URL：<url>
- 定位：<页面栏目/法条章节>

## **经济概况**

<填写与企业分布、行业结构、监管环境相关的经济背景>

证据来源：
- URL：<url>
- 定位：<页面栏目/统计表>

## **地理与自然资源**

<如与企业注册数据获取无明显关联，可精简；若无映射可删除本节>

证据来源（如保留）：
- URL：<url>
- 定位：<页面栏目>

## **文化与社会**

<如与企业登记/披露制度无明显关联，可精简；若无映射可删除本节>

证据来源（如保留）：
- URL：<url>
- 定位：<页面栏目>

## **国际地位**

<填写该国在国际组织中的角色（仅保留与企业披露、跨境合规相关信息）>

证据来源：
- URL：<url>
- 定位：<页面栏目>

# 数据源调研

## 调研元数据

- country_or_region: `<country_or_region>`
- report_language: `<target_language>`
- generated_at: `<YYYY-MM-DD>`
- sample_size: `<sample_size>`

## 企业工商注册流程

<按“机构层级 -> 流程步骤 -> 输出编号/凭证”描述。建议用箭头流程表达>

```markdown
<步骤1> -> <步骤2> -> <步骤3> -> <正式运营>
```

字段要求：
- 主管机构（中央/州省/地方）
- 关键节点（设立、税务登记、许可）
- 每步输出（编号、证书、状态）
- 是否可在线办理

证据来源：
- URL：<url>
- 定位：<按钮名/流程页标题/接口路径>

## 各种编号说明

> 说明：本章默认保留。若目标国家不存在对应编号体系，删除无映射小节即可。

### CNPJ（可替换为“国家级法人/税务编号”）

> 若目标国家无此概念，请删除本小节并在章节末说明“无对应国家级法人税号体系”。

#### 定义

<填写编号官方定义，尽量引用原文短句>

#### 功能与用途

1. <用途1>
2. <用途2>
3. <用途3>

#### 管理机构与覆盖范围

- 管理机构：<机构名>
- 覆盖对象：<企业/组织类型>
- 管理目的：<税务/统计/监管>

#### CNPJ编号结构

- 编号长度：<位数>
- 结构：<各段含义>
- 示例：`<示例编号>`

#### CNPJ的官方用途

- <银行开户/纳税申报/合同签署等>

证据来源（本小节统一填写）：
- URL：<url>
- 定位：<法条/官方说明页>

### NIRE（可替换为“州省级企业登记号/商业登记号”）

> 若目标国家无分层登记号体系，请删除本小节。

#### 定义

<填写编号官方定义>

#### 主管机构

<填写负责签发该编号的机构>

#### NIRE编号结构

- 编号长度：<位数>
- 结构：<各段含义>
- 示例：`<示例编号>`

#### NIRE的功能与法律效力

<说明该编号是否代表企业“法律成立”、适用层级与效力范围>

#### NIRE 与 CNPJ 的关系

| 比较维度 | NIRE（或本国对应编号） | CNPJ（或本国对应编号） |
|---|---|---|
| 管理机构 | <填写> | <填写> |
| 管理层级 | <填写> | <填写> |
| 性质 | <填写> | <填写> |
| 编号长度 | <填写> | <填写> |
| 获得顺序 | <填写> | <填写> |
| 法律依据 | <填写> | <填写> |

#### NIRE的常见用途

1. <用途1>
2. <用途2>
3. <用途3>

证据来源（本小节统一填写）：
- URL：<url>
- 定位：<法条/官方说明页>

### CPF（可替换为“自然人税号/身份证号（与企业关联维度）”）

> 若目标国家个人编号与企业登记无公开关联，或不可合法采集，请删除本小节。

#### 定义

<填写编号官方定义>

#### 功能与用途

1. <用途1>
2. <用途2>
3. <用途3>

#### CPF编号结构

- 编号长度：<位数>
- 结构：<各段含义>
- 示例：`<示例编号>`

#### 外国人如何注册 CPF（官方流程）

<若无外国人适用路径，写“未验证/不适用”>

证据来源（本小节统一填写）：
- URL：<url>
- 定位：<官方办事页/流程说明>

## 官方数据源

### 说明

<先列 Authority Source（机构级），再列 Data Product（产品级）。>

Authority Source 字段：
- 机构名称
- 职责范围
- 主域名
- 法律/许可边界

Data Product 字段：
- product_id
- 获取方式（API/批量包/检索页/文档服务）
- 更新周期
- 主键（企业主轴映射）
- 详细必填项：见下方 `### Data Product 明细模板（官方通用，必填）`

### **总结**

| Authority Source | Data Product | 调研结果 | 披露数据维度 | 是否可用 | 访问门槛 | 合规备注 | 风险等级 | 合作洽谈 |
|---|---|---|---|---|---|---|---|---|
| <机构A> | <产品A1> | <结果> | <维度> | <Y/N> | <匿名/注册/付费/KYC> | <备注> | <低/中/高（官方可选）> | <Y/N（官方可选）> |
| <机构B> | <产品B1> | <结果> | <维度> | <Y/N> | <匿名/注册/付费/KYC> | <备注> | <低/中/高（官方可选）> | <Y/N（官方可选）> |

### Data Product 明细模板（官方通用，必填）

Data Product 明细（逐项填写；每个 `product_id` 重复一块）：

- product_id: `<product_id>`
- product_name: `<product_name>`
- test_date: `<YYYY-MM-DD>`
- method: `<Playwright MCP / equivalent automation / manual fallback>`
- acquisition_mode: `<API/批量包/检索页/文档服务>`
- product_entry_url: `<url>`
- endpoint_or_download_url: `<url>`
- request_params: `<params>`
- response_shape: `<json/csv/schema>`
- update_cycle_evidence: `<更新周期 + 证据>`
- primary_enterprise_key: `<企业主键>`
- fallback_keys: `<name/address/date/...>`
- product_role: `<identity/status/governance/financials/compliance_docs>`
- query_pagination_result: `<分页方式/限制>`
- auth_requirement: `<anonymous/registration/KYC/paid>`
- anti_bot_or_rate_limit: `<限频/验证码/封禁策略>`
- MCP访问链路：`<success/failed>` + `<url + locator + artifacts>`
- 下载脚本：`<country>-<authority-id>-<product-id>-download-sample.py`
- 样本数据：`<country>-<authority-id>-<product-id>-test-dataset-<sample_size>.<ext>`（或目录）
- 下载测试：`<success/failed>`; downloaded_count=`<count>`; throughput/duration=`<rps/duration>`

字段级维度明细（可按需扩展）：

| field | meaning | availability | free_or_paid | prerequisite | source_locator |
|---|---|---|---|---|---|
| `<field_1>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |
| `<field_2>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |

Required Coverage 五维映射：
- business_registration_core: `<available/partial/unavailable>` + note
- branches: `<available/partial/unavailable>` + note
- executives_team: `<available/partial/unavailable>` + note
- shareholders_board: `<available/partial/unavailable>` + note
- purchasable_documents: `<available/partial/unavailable>` + note

- 可提供维度：
  - `identity（主体识别）`: `<available/partial/unavailable>`
  - `status（状态与生命周期）`: `<available/partial/unavailable>`
  - `governance（高管与治理）`: `<available/partial/unavailable>`
  - `financials（财务与报表）`: `<available/partial/unavailable>`
  - `compliance_docs（合规与申报文档）`: `<available/partial/unavailable>`
- 维度增量说明：`<该 product 对企业主轴新增了什么>`
- executability_rating: `<high/medium/low>`
- key_risks: `<risk_1>; <risk_2>`
- best_use_case: `<initialization/incremental/backfill/verification>`
- role_in_primary_combo: `<role>`
- role_in_fallback_combo: `<role>`
- conflict_priority: `<authority-level priority>`
- 是否纳入组合：`yes/no`；纳入原因：`<reason>`

#### 巴西联邦税务局（可替换为：官方数据源A）

> 若本国不存在联邦税务局对应机构，请改名为本国实际机构；若无映射可删除。

- authority_id: `<authority_id>`
- authority_name: `<官方机构名称>`
- domain: `<主域名>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 证据：<url + locator>
- Data Product 明细：按上方 `### Data Product 明细模板（官方通用，必填）` 逐个 `product_id` 填写。

#### 国家统一平台（可替换为：官方数据源B）

- authority_id: `<authority_id>`
- authority_name: `<平台名称>`
- domain: `<主域名>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 证据：<url + locator>
- Data Product 明细：按上方 `### Data Product 明细模板（官方通用，必填）` 逐个 `product_id` 填写。

#### 国家开放数据门户（可替换为：官方数据源C）

- authority_id: `<authority_id>`
- authority_name: `<平台名称>`
- domain: `<主域名>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 证据：<url + locator>
- Data Product 明细：按上方 `### Data Product 明细模板（官方通用，必填）` 逐个 `product_id` 填写。

#### 巴西证券交易委员会（可替换为：证券/金融监管机构）

- authority_id: `<authority_id>`
- authority_name: `<监管机构名称>`
- domain: `<主域名>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 证据：<url + locator>
- Data Product 明细：按上方 `### Data Product 明细模板（官方通用，必填）` 逐个 `product_id` 填写。

#### 圣保罗州工商局（可替换为：地方登记机构）

- authority_id: `<authority_id>`
- authority_name: `<地方机构名称>`
- domain: `<主域名>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 证据：<url + locator>
- Data Product 明细：按上方 `### Data Product 明细模板（官方通用，必填）` 逐个 `product_id` 填写。

## 三方数据源

### 说明

<与“官方数据源”保持同构：先列第三方 Authority Source（平台级），再列 Data Product（产品级）；并补充第三方特有风险字段。>

第三方 Authority Source 字段：
- 平台名称
- 平台类型（聚合检索/企业征信/商业数据库/API经销）
- 主域名
- 数据来源透明度（自采/官方转引/不透明）
- 许可与使用边界（ToS、转售限制、商用限制）

第三方 Data Product 字段：
- product_id
- 获取方式（API/批量包/检索页/文档服务）
- 更新周期
- 主键（企业主轴映射）
- 风险等级（低/中/高）
- 详细必填项：见下方 `### Data Product 明细模板（三方通用，必填）`

### 总结

| Authority Source | Data Product | 调研结果 | 披露数据维度 | 是否可用 | 访问门槛 | 合规备注 | 风险等级 | 合作洽谈 |
|---|---|---|---|---|---|---|---|---|
| <第三方机构A> | <产品A1> | <结果> | <维度> | <Y/N> | <匿名/注册/付费/KYC> | <ToS/许可说明> | <低/中/高> | <Y/N> |
| <第三方机构B> | <产品B1> | <结果> | <维度> | <Y/N> | <匿名/注册/付费/KYC> | <ToS/许可说明> | <低/中/高> | <Y/N> |

各类企业覆盖情况

| 公司名称 | 注册号 | 所属行业 | 公司类型 | 简介 | 注册地 | <数据源A可覆盖> |
|---|---|---|---|---|---|---|
| <样本1> | <编号> | <行业> | <类型> | <简介> | <地区> | <Y/N> |
| <样本2> | <编号> | <行业> | <类型> | <简介> | <地区> | <Y/N> |

#### CNPJa（可替换为：第三方 Authority Source A）

> 若目标国家无可用第三方来源可删除本小节，但需在“三方数据源-总结”标记“暂未发现可用来源”。

- authority_id: `<authority_id>`
- authority_name: `<第三方平台名称>`
- platform_type: `<聚合检索/企业征信/商业数据库/API经销>`
- domain: `<主域名>`
- data_source_transparency: `<自采/官方转引/不透明>`
- legal_or_license_boundary: `<ToS/转售限制/商用限制>`
- data_products: `<product_id 列表>`
- 可提供维度：<identity（主体识别）/status（状态与生命周期）/governance（高管与治理）/financials（财务与报表）/compliance_docs（合规与申报文档）>
- 访问门槛：<匿名/注册/付费/KYC>
- anti_bot_or_rate_limit: `<限频/验证码/封禁策略>`
- 风险等级：<低/中/高>
- 证据：<url + locator + artifacts>
- Data Product 明细：按下方 `### Data Product 明细模板（三方通用，必填）` 逐个 `product_id` 填写。

### Data Product 明细模板（三方通用，必填）

Data Product 明细（逐项填写；每个 `product_id` 重复一块）：

- product_id: `<product_id>`
- product_name: `<product_name>`
- test_date: `<YYYY-MM-DD>`
- method: `<Playwright MCP / equivalent automation / manual fallback>`
- acquisition_mode: `<API/批量包/检索页/文档服务>`
- product_entry_url: `<url>`
- endpoint_or_download_url: `<url>`
- request_params: `<params>`
- response_shape: `<json/csv/schema>`
- update_cycle_evidence: `<更新周期 + 证据>`
- primary_enterprise_key: `<企业主键>`
- fallback_keys: `<name/address/date/...>`
- product_role: `<identity/status/governance/financials/compliance_docs>`
- query_pagination_result: `<分页方式/限制>`
- auth_requirement: `<anonymous/registration/KYC/paid>`
- anti_bot_or_rate_limit: `<限频/验证码/封禁策略>`
- MCP访问链路：`<success/failed>` + `<url + locator + artifacts>`
- 下载脚本：`<country>-<authority-id>-<product-id>-download-sample.py`
- 样本数据：`<country>-<authority-id>-<product-id>-test-dataset-<sample_size>.<ext>`（或目录）
- 下载测试：`<success/failed>`; downloaded_count=`<count>`; throughput/duration=`<rps/duration>`

字段级维度明细（可按需扩展）：

| field | meaning | availability | free_or_paid | prerequisite | source_locator |
|---|---|---|---|---|---|
| `<field_1>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |
| `<field_2>` | `<desc>` | `<available/partial/unavailable>` | `<free/paid>` | `<condition>` | `<url + locator>` |

Required Coverage 五维映射：
- business_registration_core: `<available/partial/unavailable>` + note
- branches: `<available/partial/unavailable>` + note
- executives_team: `<available/partial/unavailable>` + note
- shareholders_board: `<available/partial/unavailable>` + note
- purchasable_documents: `<available/partial/unavailable>` + note

- 可提供维度：
  - `identity（主体识别）`: `<available/partial/unavailable>`
  - `status（状态与生命周期）`: `<available/partial/unavailable>`
  - `governance（高管与治理）`: `<available/partial/unavailable>`
  - `financials（财务与报表）`: `<available/partial/unavailable>`
  - `compliance_docs（合规与申报文档）`: `<available/partial/unavailable>`
- 维度增量说明：`<该 product 对企业主轴新增了什么>`
- executability_rating: `<high/medium/low>`
- key_risks: `<risk_1>; <risk_2>`
- best_use_case: `<initialization/incremental/backfill/verification>`
- role_in_primary_combo: `<role>`
- role_in_fallback_combo: `<role>`
- conflict_priority: `<authority-level priority>`
- 风险等级：`<低/中/高>`
- 是否纳入组合：`yes/no`；纳入原因：`<reason>`

## 下载方案（必填）

> 参考组合结论，仅保留 `Primary Combo` 与最多一个 `Fallback Combo`。

全局合并策略（跨官方+三方）：
- primary_key_strategy: `<优先官方注册号；无则名称+地址+时间等辅助键>`
- fallback_key_strategy: `<降级匹配策略>`
- dimension_merge_rules: `<字段级主备映射与冲突处理>`
- authority_conflict_priority: `<authority_1 > authority_2 > authority_3>`

组合评分与推荐：
- scoring_weights: `timeliness=0.4, volume=0.3, coverage=0.3`（如调整需说明）

| combo_id | 组合构成（authority/product） | timeliness | volume | coverage | 总分 | 证据 |
|---|---|---|---|---|---|---|
| `<combo_A>` | `<a1/p1 + a2/p2>` | `<0-100>` | `<0-100>` | `<0-100>` | `<score>` | `<evidence refs>` |
| `<combo_B>` | `<...>` | `<0-100>` | `<0-100>` | `<0-100>` | `<score>` | `<evidence refs>` |

- Primary Combo: `<authority/product 组合>`
- Fallback Combo（可空）: `<authority/product 组合>`
- sample_size: `<N>`
- remaining_gaps_and_reasons: `<仍未覆盖维度与原因>`

初始化下载方案（initialization_plan）：
- 目标：`<全量首拉范围>`
- 执行顺序：`<按 authority/product 顺序>`
- 产物：`<全量数据文件/分区目录>`
- 失败回滚策略：`<策略>`

增量下载方案（incremental_plan）：
- 增量标记：`<更新时间字段/版本号/流水号>`
- 调度频率：`<每小时/每日/每周>`
- 去重与幂等：`<主键+哈希/UPSERT 规则>`
- 增量产物：`<增量文件/变更日志>`

回查补数方案（backfill_plan）：
- 触发条件：`<字段缺失/接口失败/时间窗重算>`
- 回查窗口：`<T-7/T-30/自定义>`
- 优先级：`<关键字段优先级>`

重试与断点续传（retry_resume_plan）：
- 重试策略：`<指数退避/固定间隔/最大重试次数>`
- 断点续传键：`<分页游标/offset/token>`
- 限流与封禁应对：`<sleep/并发控制/代理策略>`

吞吐与时长估算（throughput_eta_estimate）：
- 单产品吞吐：`<records/s>`
- 组合总吞吐：`<records/s>`
- 首次全量预计时长：`<h/d>`
- 日常增量预计时长：`<min/h>`

运行命令（可选）：

```bash
python <country-or-region>-download-sample.py
```

## 交付产物与落盘路径（必填）

结果目录（最终交付）：
- `results/overseas-registry-source-research/<YYYYMMDD>/`

最少输出文件：
- `<country-or-region>-数据源调研方案.md`
- `<country-or-region>-数据下载可行性分析报告.md`
- `<country-or-region>-sources.md`
- `<country-or-region>-field-coverage-matrix.md`
- `<country-or-region>-combined-report.md`

每个入选 `product_id` 额外输出：
- `<country-or-region>-<authority-id>-<product-id>-download-sample.py`
- `<country-or-region>-<authority-id>-<product-id>-test-dataset-<sample_size>.<ext>`（或目录）
- `<country-or-region>-<authority-id>-<product-id>-dimensions.md`

可选聚合脚本：
- `<country-or-region>-download-sample.py`

过程目录（非最终交付）：
- `temp/overseas-registry-source-research/<YYYYMMDD>/<country-or-region>/`
- 说明：`temp/` 文件不能替代 `results/...` 最终交付。

目录示例：

```text
results/overseas-registry-source-research/<YYYYMMDD>/
  <country>-数据源调研方案.md
  <country>-数据下载可行性分析报告.md
  <country>-sources.md
  <country>-field-coverage-matrix.md
  <country>-combined-report.md
  <country>-<authority1>-<product1>-download-sample.py
  <country>-<authority1>-<product1>-test-dataset-<sample_size>.csv
  <country>-<authority1>-<product1>-dimensions.md
```

交付核对清单：
- [ ] 已生成 5 个基础报告文件
- [ ] 每个入选 `product_id` 都有脚本文件
- [ ] 每个入选 `product_id` 都有样本数据文件/目录
- [ ] 每个入选 `product_id` 都有维度说明文件
- [ ] `temp/` 过程文件已与 `results/` 最终文件区分
