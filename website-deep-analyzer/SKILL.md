---
name: website-deep-analyzer-enhanced
description: 用于通过 Playwright 或等效浏览器方式抓取企业官网，并按照当前 prompt schema 提取企业信息、补全缺失字段、保存原始页面与结果文件的技能。
---

# 技能说明：website-deep-analyzer-enhanced

当用户要求你分析某个企业官网时，必须先读取同目录下的 `prompt.md`，然后严格按照其中定义的最新 JSON 结构输出结果。

## 工作原则

- 输出必须严格遵循 `prompt.md` 的字段结构。
- 任一字段无法提取时，必须保留为空字符串 `""`、空数组 `[]` 或对应的空对象字段，不得省略字段。
- 抓取字段时优先保存网页原始值，并尽量保留网页原始展示格式。
- 除非 schema 明确要求拆分、分类或结构化，否则不要主动翻译、改写、标准化或重组原始内容。
- 所有结果都必须能追溯到保存下来的原始页面或原始接口响应。

## 输出目录

所有输出文件必须保存在：

```txt
./temp/<website_name>/
```

`website_name` 转换规则：

- 去掉 `https://` 或 `http://`
- 去掉结尾 `/`
- 将 `.` 替换为 `_`
- 例如：`https://www.databricks.com/` -> `www_databricks_com`

## 页面抓取规则

- 给定 URL 后，优先从原始输入页面开始抓取。
- 必须先完整检查原始输入 URL 及其同语言、同站内页面。
- 在原始输入 URL 尚未完成检查前，不得主动跳转到 `/en`、`/zh`、`/jp` 或其他语言版本页面。
- 先在原始页面及其同语言、同站内页面中查找信息，不要默认跳转到 `/en`、`/zh` 或其他语言版本。
- 仅在原始页面无法支撑目标字段，且站内明确存在其他必要详情页时，再继续访问相关子页面。
- 应优先访问官网主体页面、公司介绍页、联系方式页、IR 页面、管理层页面、股东页面及官网披露文档。
- 对于同一主域名下的深层详情页，也必须主动补查，例如 `/about/officer`、`/about/management`、`/about/corporate-information`、`/ir/faq` 这类页面；不能只停留在一级导航页。
- 访问多个页面时，必须按顺序保存原始文件，如 `raw.html`、`raw_01.html`、`raw_02.html`。

## 下钻深度规则

- 不得只依赖首页、落地页或一级导航页完成提取。
- 当以下任一字段仍为空或明显不完整时，必须继续在同域内下钻搜索并访问更深层页面：
  - `company_name`
  - `company_intro`
  - `business_scope`
  - `registration_date`
  - `address`
  - `email`
  - `contact`
  - `fax`
  - `personnel_info.executives`
  - `shareholders`
- 下钻优先顺序应至少覆盖：
  - 公司资料页，如 `about`、`company info`、`corporate information`、`corporate data`
  - 管理层/董事页，如 `officer`、`board`、`management`、`leadership`
  - 联系方式页，如 `contact`、`contact us`
  - 投资者关系页，如 `ir`、`faq`、`stock`、`shareholder`
  - 治理页，如 `corporate governance`
  - 报告和披露文件，如 `annual report`、`corporate report`、`factsheet`、`pdf`
- 对于首页上出现但未展开的栏目，必须继续进入对应详情页核查，而不是仅依据首页摘要填值。
- 对于列表页、聚合页、导航页、入口页，若字段仍不充分，必须继续进入列表中的详情页。
- 对于团队页、董事页、管理层页、投资组合页、新闻页、FAQ 页等列表型页面，若列表项本身可点击进入详情页，则必须继续进入详情页核查，不能只停留在列表页。
- 对于人物信息，若列表页仅提供姓名、职务、地区、标签等简略信息，而详情页存在完整人物简介、履历、加入时间、负责领域等内容，则必须以详情页为准补全 `biography`、`title` 及其他相关字段。
- 对于公司简介、业务介绍、股东信息、治理信息也是同样原则：列表页或摘要页只作为线索，最终应尽量下钻到叶子页面或正式披露页面取值。
- 对于团队/管理层列表页，必须先完整枚举页面中所有成员条目，再开始逐个下钻，不能只抓到部分成员后停止。
- 若同一团队页可见 20 人、30 人或更多成员，最终结果至少应反映该列表页中全部可识别成员；不能因为只补了少数详情页而遗漏其余成员。
- 对于已枚举出的成员，只要存在对应详情页链接、可推断详情页 URL、或可通过站内搜索定位到详情页，都应尽量逐个补查。
- 若少数成员无法定位详情页，仍需保留其列表页中的姓名和职务，不得整人遗漏。
- 若同一类信息在多个层级页面都有披露，应优先采用最接近正式公司资料、IR 披露、董事/高管详情页的值。
- 若页面存在中英文或多语言版本，应优先沿原始语言版本继续下钻；只有原始语言版本明确无法支撑字段时，才允许补查其他语言版本。
- 补查其他语言版本时，必须满足三个条件：
  - 原始语言版本已完成首页、相关栏目页、相关详情页的检查
  - 待提取字段在原始语言版本中仍为空、明显不完整，或页面无法正常访问
  - 其他语言版本与当前主公司主体明显对应，不会引入子公司或地区站点混淆
- 若其他语言版本与原始语言版本信息冲突，默认以原始语言版本为准；只有当原始语言版本缺失而其他语言版本为官网明确披露时，才允许补入。
- 对于 `personnel_info`、`shareholders`、`registration_date` 这类容易漏抓的字段，必须至少额外检查一个公司资料页或 IR 资料页，不能仅凭首页判定为空。
- 对于 `personnel_info.executives`，默认应执行“两跳检查”：
  - 第一跳：团队/董事/管理层列表页，拿到人员清单
  - 第二跳：进入每位人员的详情页，尽可能补全 `title`、`biography` 及其他字段
- 只有在详情页不存在、无法访问或页面明确没有更多信息时，才允许退回列表页值。
- 停止下钻前，必须确认目标字段不是“因为没有继续进入详情页而遗漏”，而是真的未公开披露。

## 原始文件保存

- HTML 页面保存为 `.html`
- API 响应保存为 `.json`
- 必须生成 `sources.txt`，记录原始文件与 URL 的对应关系

示例：

```txt
raw.html -> https://www.example.com/
raw_01.html -> https://www.example.com/about
raw_01.json -> https://api.example.com/data
```

## 字段提取规则

### company_name

- 输出结果中必须包含 `company_name` 对象。
- `company_name.english_name`：存储公司英文全称，优先保留网页原始写法。
- `company_name.short_names`：存储公司简称数组，逐条记录不同语言、不同写法或不同场景下的简称。
- `company_name.short_names` 中每个元素只允许对应一个简称，不能把多个简称拼接进同一个字符串。
- 若网页仅出现一个简称，也必须按数组形式存储，例如 `["Kidswell"]`。
- 若未明确披露英文全称，则 `company_name.english_name` 保留 `""`；若未明确披露简称，则 `company_name.short_names` 保留 `[]`。

### company_intro 与 business_scope

- 不再保留单一 `description`。
- `company_intro`：公司简介、公司概况、企业介绍、品牌定位等简要信息。
- `business_scope`：经营范围、主营业务、业务板块、产品与服务范围等信息。
- 若原文混合了两类内容，应尽量拆分后分别填入两个字段。
- `company_intro` 必须优先来自公司介绍正文、概述文案、定位文案等真实内容，不能直接使用导航菜单、站点标题或页头栏目名。
- `business_scope` 必须优先来自业务介绍正文、业务板块标题、主营业务内容等真实内容，不能直接使用导航菜单、面包屑或栏目导航文本。
- 对于 `company_intro` 与 `business_scope`，只要官网存在连续正文描述，应尽可能完整收录相关原始内容，不应默认只取首句或短摘要。
- 若同一字段对应多段连续正文，应在去除噪音与重复后尽量完整保留，而不是人为压缩成一句话。

### registration_date

- `registration_date` 仅在日期明确对应企业注册、设立、成立、incorporation、establishment 等法人主体信息时填写。
- 必须优先使用官网页面明确披露的原始字段值，例如 `設立`、`成立日期`、`Established`、`Incorporated` 等。
- 不要将产品发布日期、网页发布时间、人员任职时间误填为 `registration_date`。
- 若同一页面同时存在母公司与子公司信息，必须优先匹配当前主公司主体，不得误取子公司的注册日期。
- 若无法确认日期对应当前主公司主体，则保留为空，不做推断填值。

### address

- 所有地址统一归入 `address` 对象。
- 应尽量区分 `registered_address`、`office_address`、`headquarters_address`、`mailing_address`、`business_address`。
- 无法明确分类但有效的地址放入 `other_addresses`。
- `other_addresses` 必须为数组，且按条逐一存储。
- `address` 字段中不应包含电话号码、传真号码、邮箱地址或其他联系方式内容。
- 若网页在同一段文本中同时披露地址与 `TEL`、`FAX`、`Phone`、`电话`、`传真` 等信息，写入 `address` 前必须先将联系方式剥离。
- 最终地址字段只保留地址正文及必要地址说明，不保留 `TEL(...)`、`FAX(...)` 等联系方式片段。

### email

- 所有邮箱统一归入 `email` 对象。
- 应尽量区分 `general_email`、`support_email`、`sales_email`、`investor_relations_email`、`media_email`、`careers_email`。
- 无法明确分类的邮箱放入 `other_emails`。
- `other_emails` 必须为数组，且按条逐一存储。
- 默认只保留公司主体层级公开披露的邮箱地址。
- 分支机构、生产基地、工厂、区域办公室、办事处、子公司或具体园区对应的邮箱地址，不应写入最终结果，除非用户明确要求保留分支机构联系方式。

### contact

- 所有电话和联系方式统一归入 `contact` 对象。
- 应尽量区分 `general_phone`、`support_phone`、`sales_phone`、`investor_relations_phone`、`media_phone`。
- 无法明确分类的号码放入 `other_contacts`。
- `other_contacts` 必须为数组，且按条逐一存储。
- 从地址文本中剥离出的电话号码也必须写入 `contact`，而不是丢弃。
- 默认只保留公司主体层级公开披露的电话号码。
- 分支机构、生产基地、工厂、区域办公室、办事处、子公司或具体园区对应的电话，不应写入最终结果，除非用户明确要求保留分支机构联系方式。

### fax

- 传真号码必须单独提取到顶层字段 `fax`。
- `fax` 必须为数组。
- 每个数组元素只允许存储一个传真号码。
- 不要将传真放入 `contact` 对象。
- 从地址文本中剥离出的传真号码必须写入 `fax`。
- 默认只保留公司主体层级公开披露的传真号码。
- 分支机构、生产基地、工厂、区域办公室、办事处、子公司或具体园区对应的传真，不应写入最终结果，除非用户明确要求保留分支机构联系方式。

### personnel_info

- `personnel_info.executives` 必须为数组。
- 每个高管对象仅包含：
  - `name`
  - `title`
  - `position`
  - `birth_date`
  - `appointment_date`
  - `gender`
  - `biography`
- 仅在网页明确披露时填写 `birth_date`、`appointment_date`、`gender`、`biography`。
- `biography` 一旦官网存在明确人物简介正文，应尽可能完整保留原始简介内容，不应默认只截取首句。

### shareholders

- `shareholders` 必须为数组。
- 每个股东对象仅包含：
  - `shareholder_name`
  - `shareholder_id`
  - `shareholder_type`
  - `shareholding_date`
  - `subscribed_amount`（纯数字，见下方规则）
  - `subscribed_currency`
  - `paid_in_amount`（纯数字，见下方规则）
  - `paid_in_currency`
  - `shareholding_ratio`（纯数字，见下方规则）
  - `country`
  - `correspondence_address`
  - `shareholding_content`
- 多个股东必须逐个拆分成独立对象。
- **数值字段约束**：`subscribed_amount`、`paid_in_amount`、`shareholding_ratio` 在数据库中为 `decimal` 类型，必须输出纯数字字符串，不得包含任何单位、货币符号、百分号或文字描述：
  - 金额字段：将 `"人民币1000万元"` 转换为 `"10000000"`，币种写入对应的 currency 字段；去除千位分隔符、货币符号、数量词（万、亿、億 等）
  - 比例字段：将 `"50%"` 转换为 `"50"`，去除百分号 `%`
  - 未披露时保留为空字符串 `""`，不得填 `"0"` 或 `"N/A"`
  - 最终值必须能被 `parseFloat()` 或 `Decimal()` 直接解析为数字

## 数组存储规则

- 所有数组字段都必须按条逐一存储。
- 每个数组元素只对应一条独立信息。
- 不允许把多条内容合并进同一个字符串。
- 适用于 `company_name.short_names`、`other_addresses`、`other_emails`、`other_contacts`、`fax`、`executives`、`shareholders` 等数组字段。

## 结果值清洗规则

- 最终写入 `result.json` 的字符串值不得保留原始网页中的多余换行符 `\n`、连续空行或无意义缩进。
- 在不改变原始含义的前提下，应将多行文本压缩为单行或紧凑格式，使用单个空格连接原本被换行拆开的内容。
- 地址、公司简介、经营范围、人员简介等字段同样适用该规则。
- “去换行”仅是格式清洗，不代表可以删减正文内容；简介、经营范围、人物简介等字段应尽量保留完整信息量。

## 最终输出

- 最终结果必须保存到 `./temp/<website_name>/result.json`
- 文件内容必须是纯 JSON，不得带 markdown 包裹
- 所有字段必须完整保留

示例：

```json
{
  "company_name": {
    "english_name": "Kidswell Bio Corporation",
    "short_names": ["Kidswell Bio"]
  },
  "address": {
    "registered_address": "",
    "office_address": "",
    "headquarters_address": "",
    "mailing_address": "",
    "business_address": "",
    "other_addresses": []
  },
  "email": {
    "general_email": "",
    "support_email": "",
    "sales_email": "",
    "investor_relations_email": "",
    "media_email": "",
    "careers_email": "",
    "other_emails": []
  },
  "contact": {
    "general_phone": "",
    "support_phone": "",
    "sales_phone": "",
    "investor_relations_phone": "",
    "media_phone": "",
    "other_contacts": []
  },
  "fax": [],
  "company_intro": "",
  "business_scope": "",
  "registration_date": "",
  "personnel_info": {
    "executives": [
      {
        "name": "",
        "title": "",
        "position": "",
        "birth_date": "",
        "appointment_date": "",
        "gender": "",
        "biography": ""
      }
    ]
  },
  "shareholders": [
    {
      "shareholder_name": "",
      "shareholder_id": "",
      "shareholder_type": "",
      "shareholding_date": "",
      "subscribed_amount": "",
      "subscribed_currency": "",
      "paid_in_amount": "",
      "paid_in_currency": "",
      "shareholding_ratio": "",
      "country": "",
      "correspondence_address": "",
      "shareholding_content": ""
    }
  ]
}
```

## 结束前检查

- `result.json` 已生成且 JSON 格式正确
- 原始页面或接口响应已保存
- `sources.txt` 已记录全部源文件与 URL
- 最终结果严格符合 `prompt.md` 的最新 schema
## 自动化闭环补充规则

- 目标不是“抓到几个高分页面”，而是“对字段完整性负责”。如果关键字段仍为空或明显不完整，必须继续下钻，而不是提前停止。
- 默认执行递归抓取：从原始 URL 开始，优先同语言、同主体、同主域页面，按字段价值继续扩展到二级、三级页面。
- 对 `team`、`leadership`、`management`、`officer`、`board`、`people` 这类人员页，必须执行“列表页全量枚举 + 详情页逐个补全”。
- 详情页补全时，至少要尝试补 `title`、`position`、`biography`、`appointment_date`、`birth_date`、`gender`。没有披露才留空，不是因为没继续进详情页。
- 只要列表页里能识别出成员，就不能漏人；即使个别成员没有详情页，也必须保留其列表页姓名与职务。
- 对 `registration_date`、`shareholders`、`personnel_info` 这类高价值字段，至少要检查一个资料页和一个深层详情页或 IR 页，不能只看首页后留空。
- 如果站点存在动态加载、登录墙、强反爬、地区封锁、TLS/证书异常，允许无法一次性自动完成；这时必须明确标注“自动化受阻原因”，不能把缺失误报成“官网未披露”。
- 如果站点可正常访问且页面内容已公开披露，则应优先通过自动递归抓取完成，不应依赖人工逐页点名补录。
