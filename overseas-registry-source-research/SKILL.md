---
name: overseas-registry-source-research
description: Use when researching overseas registry sources and producing a verifiable multi-source strategy with authority-level source selection and per-product MCP/download validation.
---

# Overseas Registry Source Research

## Purpose
针对指定国家/地区，系统调研官方与关键第三方企业数据源，逐源完成可复现验证，并输出“数据源组合”下载方案。目标是同时优化：
- 更新最即时
- 数据量最大
- 信息披露维度最全面

本技能的本质目标是：以“企业（Company/Entity）”为统一主轴，整合多个 `Authority Source` 及其 `Data Product` 的披露字段，构建企业多维度信息视图（而非孤立的数据抓取清单）。

## Source Hierarchy Standard (Required)
本技能强制使用两层定义，避免概念混淆：
- `Authority Source`（主数据源/机构级来源）
  - 例：Companies House、税务局、统计局、证券监管机构、政府开放数据平台
- `Data Product`（子数据产品/同机构下入口）
  - 例：bulk basic snapshot、PSC snapshot、accounts daily、search web、public API

规则：
1. “数据源数量”优先按 `Authority Source` 统计。
2. 同一机构下多个入口默认归为同一个 `Authority Source`。
3. 逐项 MCP 实测、脚本下载、1000条测试的执行颗粒度按 `Data Product` 进行。
4. 报告必须同时展示：
   - `Authority Source` 汇总视图
   - `Data Product` 执行视图
5. 数据整合与评分必须以“企业主轴”进行：每个 `Data Product` 都要说明其如何映射到企业实体（例如 Company Number、注册号、名称+地址匹配）。

## Enterprise-Centric Integration Rule (Required)
所有分析、测试与结论必须围绕“企业维度整合”展开：
1. 先定义企业主键策略（优先官方注册号；缺失时使用名称/地址/时间等辅助键）。
2. 每个 `Data Product` 必须声明其在企业维度中的角色：
   - `identity`（主体识别）
   - `status`（状态与生命周期）
   - `governance`（高管/股东/受益所有人）
   - `financials`（财报/财务文档）
   - `compliance_docs`（申报/可购买文档）
3. 组合推荐必须回答：该组合如何在企业主轴上实现“更全维度覆盖”，而不是只比较下载便利性。

## Runtime Compatibility
可在以下代理/CLI 环境使用，且不依赖单一平台私有能力：
- Codex
- Claude Code
- Gemini CLI
- OpenCode

## Encoding Standard
- 所有输入/输出文件统一使用 UTF-8。
- 结果中包含中文时必须可读、无乱码。
- 新增或修改文件默认保持 UTF-8（无 BOM）。

## Input
- `country_or_region`：目标国家/地区名称（必填）
- `target_language`：报告语言，默认中文
- `template_path`：报告模板路径，默认 `overseas-registry-source-research/assets/templates/registry-research-template.md`
- `generated_at`：报告生成日期（`YYYY-MM-DD`），默认执行当天日期（执行环境本地时区）
- `sample_size`：每个数据产品的预下载规模，默认 `1000`
- `time_limit_or_budget`：可选，用于限制验证深度

## Required Coverage Dimensions
下载方案设计与可行性评估时，必须覆盖以下维度并标注“可获取/部分可获取/不可获取”：
- 企业工商注册信息：名称、曾用名、多语言名、注册号、税号、办公地址、经营范围、所属行业、成立日期、注销日期、登记状态、法人/法定代表人
- 分支机构信息
- 高管/团队成员信息
- 股东/董事会成员信息
- 可购买文件（企业档案、年报、章程、变更文件、证明文件等）：文件类型、获取方式、价格/计费、是否需要登录或实名

## Required Tools
- 联网搜索（优先官方与权威来源）
- 浏览器自动化（优先 Playwright MCP）
- Python（必须，用于下载测试脚本实现）

## Tool Fallback Rules
- 若无 Playwright MCP，可使用等价自动化工具。
- 若自动化工具不可用，可人工取证降级，但必须提供可复现证据，并在报告中标注 `自动化未验证`。

## Source Discovery Standard (Required)
先找机构级来源，再拆产品级入口：

### Step A: Authority Source Discovery
- 必须先列出候选 `Authority Source`，并按优先级筛选：
  - 公司注册/工商主管机构
  - 税务主管机构
  - 政府开放数据平台
  - 证券/金融监管机构
  - 统计机构
- 每个 `Authority Source` 必须记录：机构名称、职责范围、主域名、法律/许可边界。

### Step A2: Third-Party Source Discovery
- 必须并行调研第三方 `Authority Source`（如聚合检索、企业征信、商业数据库、API经销平台）。
- 每个第三方 `Authority Source` 必须记录：
  - 平台名称、平台类型、主域名
  - 数据来源透明度（自采/官方转引/不透明）
  - 法律/许可边界（ToS、转售限制、商用限制）
  - 初步风险等级（低/中/高）
- 第三方入选前必须回答：
  - 是否对企业主轴维度有增量贡献？
  - 是否存在可执行访问路径（搜索/API/下载）？
  - 合规边界是否可验证？

### Step B: Data Product Discovery
- 在每个入选 `Authority Source` 下，枚举可执行 `Data Product`：
  - 批量下载包
  - API
  - 搜索页面
  - 文档/文件服务入口
- 每个 `Data Product` 必须有唯一 `product_id`。

### Step C: Inclusion Rule
- 是否“入选”由 `Data Product` 决定（可执行性与价值），
- 但“来源归属”必须回挂到 `Authority Source`，禁止把同机构产品写成多个独立机构来源。
- 入选判断必须增加一条：该 `Data Product` 是否对“企业主轴维度覆盖”有增量价值（无增量则不入选）。

## Mandatory Per-Product Validation Rule
对“所有入选 Data Product”必须逐个完成以下闭环，缺一不可：
1. MCP 页面访问与链路实测（入口、查询、分页、限制、鉴权）
2. 数据加载链路分析（接口/下载包/参数/返回结构）
3. 编写该 `product_id` 专属 Python 下载脚本
4. 完成 `sample_size`（默认1000）测试下载并落盘
5. 输出该 `product_id`“可提供数据维度说明”（字段级）

禁止仅对最终主方案做一次测试。必须是“每个入选 product 都有脚本 + 样本 + 维度说明”。

## Reporting Field Conventions (Required)
为避免模板字段口径漂移，以下字段使用统一判定：
- `风险等级`：按执行稳定性与合规风险综合判断，取值 `低/中/高`
  - 低：可稳定访问，限制轻，合规边界清晰
  - 中：存在限频/登录/偶发反爬，或许可边界部分不明确
  - 高：强反爬/高门槛/许可不清晰或高法律风险
- `合作洽谈`：是否建议进入商务合作流程，取值 `Y/N`
  - Y：免费边界不足或长期依赖且对业务关键
  - N：公开可得且可持续，或不具备合作价值
- `generated_at`：报告实际生成日期，不得留空。
- `generated_at` 时区：使用执行环境本地时区；若任务另有要求，需在报告元数据显式声明。

## Workflow
1. 接收 `country_or_region`，定义术语映射（公司注册、税务登记、受益所有人等）。
2. 先完成模板前置章节（必填）：
   - `概况`（基本信息、政治体制、经济概况；地理/文化可按映射保留或删除）
   - `企业工商注册流程`
   - `各种编号说明`（按国家概念映射保留/删除 CNPJ/NIRE/CPF 小节）
3. 填写 `调研元数据`（`country_or_region/target_language/generated_at/sample_size`）。
4. 执行 `Source Discovery Standard`：先 Authority，后 Product。
5. 对每个入选 `product_id`，执行 `Mandatory Per-Product Validation Rule` 全流程。
6. 产出对比矩阵（必填，含两层）：
   - Authority 级对比
   - Product 级对比（覆盖、主键、更新周期、获取方式、速率限制、门槛、合规、自动化稳定性）
7. 产出字段级合并策略（必填）：
   - 每个关键字段给出 `primary product` 与 `fallback product`
   - 同时给出 `authority-level` 冲突优先级
8. 产出“企业主轴维度映射表”（必填）：
   - 每个关键维度对应的主产品/备产品
   - 主键映射方式与冲突处理
   - 维度缺口与补齐路径
9. 生成“下载可行性分析报告”（必填）：
   - 先按 Authority 汇总
   - 再按 Product 逐项说明实测结果
   - 最后输出“组合决策结论”
10. 生成“完整下载方案结论”（必填）：
   - 仅给出 1 个 `Primary Combo` 与最多 1 个 `Fallback Combo`
   - 明确初始化、增量、回查、重试/断点续传、吞吐与时长估算
   - 标注各组合对 `Required Coverage Dimensions` 的覆盖与缺口补齐路径
11. 生成字段覆盖矩阵文件（必填）：逐字段列出 primary/fallback、更新周期、可得性状态。
12. 先按模板章节完成 `combined-report`，再拆分并输出其余必交付文件，确保单一事实来源一致。
13. 按模板章节顺序落盘，避免把嵌入式内容拆成独立附录。

## Combination Decision Rule (Required)
在“下载可行性分析报告”中必须给出“数据源组合推荐”，并使用固定评分框架：
- 评分维度（必须同时出现）：
  - `timeliness`（更新即时性）
  - `volume`（数据量规模）
  - `coverage`（披露维度完整度）
- 每个候选组合都要有可追溯证据与分数。
- 默认权重（可按任务声明调整）：
  - timeliness: 0.4
  - volume: 0.3
  - coverage: 0.3
- 输出：
  - `Primary Combo`：综合最优（最即时 + 最大量 + 最全面）
  - `Fallback Combo`：主组合不可用时的次优方案

强制补充：组合结论必须明确说明“在企业主轴上新增了哪些维度覆盖”，并给出仍未覆盖维度与原因。

## Template Mapping Rules
以 `overseas-registry-source-research/assets/templates/registry-research-template.md` 为唯一基准模板，按其现有章节结构直接填充，不再要求额外独立章节。

必须完整填充以下模板章节（可按模板规则删除无映射小节）：
- `概况`
- `数据源调研`（含调研元数据、企业工商注册流程、编号说明、官方数据源、三方数据源）
- `下载方案（必填）`
- `交付产物与落盘路径（必填）`

其中，逐 `Data Product` 的字段必须在模板内嵌块填写：
- `Data Product 明细模板（官方通用，必填）`
- `Data Product 明细模板（三方通用，必填）`

并且“每个数据源（Data Product）章节”必须严格使用：
- `registry-research-template.md` 内置的 `Data Product 明细模板（官方通用）` 与 `Data Product 明细模板（三方通用）`

最终报告中的数据源部分，禁止使用自由格式叙述替代模板字段。

## Output
结果统一存放：
`results/overseas-registry-source-research/<YYYYMMDD>/`

最少输出以下文件：
- `<country-or-region>-数据源调研方案.md`
- `<country-or-region>-数据下载可行性分析报告.md`
- `<country-or-region>-sources.md`
- `<country-or-region>-field-coverage-matrix.md`
- `<country-or-region>-combined-report.md`

并且对每个入选 `product_id` 都要输出：
- `<country-or-region>-<authority-id>-<product-id>-download-sample.py`
- `<country-or-region>-<authority-id>-<product-id>-test-dataset-<sample_size>.<ext>` 或目录形式
- `<country-or-region>-<authority-id>-<product-id>-dimensions.md`

可选聚合脚本（建议）：
- `<country-or-region>-download-sample.py`（统一调度各 product 脚本）

## Working Directory Rules
- 过程文件统一写入：
  `temp/overseas-registry-source-research/<YYYYMMDD>/<country-or-region>/`
- `temp/` 产物不得替代最终交付；最终文件必须落盘到 `results/...`。

## Evidence Rules
- 每条关键结论必须可追溯到具体来源页面。
- 每个核心字段说明需给出来源 URL 与页面定位（栏目名、按钮名、查询参数或接口路径）。
- 涉及“免费可得字段”时需写明前提（匿名可查/注册后可查/限频等）。
- 无法确认时标注 `未验证`，禁止臆测。
- 更新周期结论必须有来源证据（页面标注或接口元数据字段）。
- `合作洽谈` 的 `Y/N` 判断必须附证据（至少一条：计费页、条款页、访问限制说明或商务页面链接）。

## Quality Checklist
- 是否已填写 `generated_at` 且格式为 `YYYY-MM-DD`？
- 是否完成模板前置章节：`概况`、`企业工商注册流程`、`各种编号说明`（无映射处已按规则删除）？
- 是否先完成了 Authority Source 级筛选，再做 Product 级入选？
- 是否把同机构的多个产品正确归并到同一个 Authority Source？
- 是否对每个入选 `product_id` 都完成了 MCP 实测？
- 是否对每个入选 `product_id` 都提供了独立 Python 脚本？
- 是否对每个入选 `product_id` 都完成了 `sample_size` 下载测试并落盘？
- 是否对每个入选 `product_id` 都输出了可披露维度说明？
- 是否完成“企业主轴维度映射表”，并明确每个产品对企业维度的增量贡献？
- 是否在可行性报告中先 Authority 汇总、再 Product 逐项说明，并给出组合评分与推荐？
- 是否给出唯一 `Primary Combo` 与最多一个 `Fallback Combo`？
- 是否覆盖并标注 `Required Coverage Dimensions` 的可得性状态？
- 是否按统一口径填写了 `风险等级` 与 `合作洽谈`？
- 若模板中填写了“三方数据源-各类企业覆盖情况”，是否给出样本选择依据与来源证据；若未填写是否注明原因？
- 是否说明免费边界、许可条款与合规限制？

## Notes
- 默认优先输出“可执行方案”，不是泛泛资讯汇总。
- 若用户未提供模板，先按本技能结构输出，再进行二次模板映射。
