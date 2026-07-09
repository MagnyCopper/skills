你需要从企业官网（包含其子页面）中提取并整合一个严格的 JSON 对象，包含以下业务字段：

```json
{
  "company_name": {
    "english_name": "",
    "short_names": []
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
  ],
  "branch_entities": [
    {
      "branch_type": "",
      "branch_type_standardized": "",
      "branch_name": "",
      "country_or_region": "",
      "country_or_region_standardized": "",
      "address": "",
      "phone": "",
      "fax": "",
      "email": "",
      "website": ""
    }
  ]
}
```

## 字段说明

### company_name 字段说明：
- `company_name` 为公司名称对象。
- `company_name.english_name` 用于存储公司英文全称，优先保留网页原始写法。
- `company_name.short_names` 为数组，用于逐条存储公司简称、品牌简称、证券简称或不同语言版本简称。
- `company_name.short_names` 必须按条逐一存储，每个数组元素只对应一个简称，例如 `["Kidswell", "キッズウェル・バイオ"]`。
- 若网页仅披露一个简称，也必须以数组形式存储；若未披露则保留为 `[]`。

### 主体层级联系字段说明：
> [!IMPORTANT]
> **主体层级联系字段的原则**
> - 顶层的 `address`、`email`、`contact`、`fax` 等字段，**仅保留母公司主体层级、总部或主要办公场所公开披露的信息**。
> - 不要将分支机构、各地区办事处、门店网点的专属联系方式填入顶层的总部联系字段中。
> - 在分类存储时，只改变字段归属，不改变字段值本身的原始表达方式。
- `address`：应尽量区分不同类型地址。无法明确归类的地址放入 `other_addresses`。
- `email`：应尽量区分不同类型邮箱。无法明确归类的邮箱放入 `other_emails`。
- `contact`：应尽量区分不同类型联系电话。无法明确归类的号码放入 `other_contacts`。
- `fax`：传真号码单独提取，不放在 `contact` 对象下，并且必须使用数组存储。

### 其它基础信息字段说明：
- `company_intro`：企业简介、公司概况、公司介绍等简要信息。
- `business_scope`：经营范围、主营业务、核心业务、产品与服务范围等信息。
- `registration_date`：企业注册日期、成立日期、incorporation date、establishment date 等，但前提是该日期明确对应企业法人主体本身。不要将产品发布、人员任职等时间误填。

### personnel_info.executives 数组高管字段说明：
- 每个高管对象必须且仅包含以下七个字段：
  - `name`：人员姓名
  - `title`：完整职位头衔
  - `position`：职位代码，例如 CEO、CFO、CTO、COO；如果没有明确职位代码则为 `""`
  - `birth_date`：出生日期
  - `appointment_date`：任职日期、就职日期、上任日期或该岗位任期开始日期
  - `gender`：性别
  - `biography`：人员简介

### shareholders 数组股东字段说明：
- 每个股东对象必须且仅包含以下十二个字段：
  - `shareholder_name`：股东名称
  - `shareholder_id`：股东标识号、注册号或其他识别编号
  - `shareholder_type`：股东类型，例如自然人、法人、机构、政府实体、基金等
  - `shareholding_date`：持股日期、出资日期、认缴日期、入股日期等
  - `subscribed_amount`：认缴金额，**必须为纯数字**（见下方数值字段规则）
  - `subscribed_currency`：认缴币种
  - `paid_in_amount`：实缴金额，**必须为纯数字**（见下方数值字段规则）
  - `paid_in_currency`：实缴币种
  - `shareholding_ratio`：持股比例或股权比例，**必须为纯数字**（见下方数值字段规则）
  - `country`：股东所属国家或司法辖区
  - `correspondence_address`：股东通讯地址或邮寄地址
  - `shareholding_content`：股东持股内容说明，例如出资内容、股份类别、持股备注等

### branch_entities 数组分支机构字段说明：
> [!IMPORTANT]
> **分支机构收集的原则**
> - 该字段仅采集“分支机构”，**必须排除**总部、总办、主办公地或母公司主联系点，两者保持清晰互斥。
> - `branch_entities` 可以包含两类条目：`实体分支机构条目`（分公司、办事处、门店、网点、服务中心等）与 `官方分支入口条目`（国家/地区站点入口、品牌站点入口、子公司入口等）。
> - 如果某条目既不是实体分支机构，也不是明确的官方分支入口，则不纳入结果。
- `branch_type`：官网原始分支类型值；若官网未明确给出原始标签，则保留抽取到的原始分类表达。
- `branch_type_standardized`：标准化后的分支类型，只能输出以下值之一：`office`、`branch`、`store`、`service_center`、`regional_site`、`country_site`、`brand_site`、`subsidiary_site`。
- `branch_name`：分支机构名称、门店名称、站点名称、品牌名称或页面原始条目名称；只有官网明确披露条目名称时才填写。若页面仅披露地点标签或城市名（如 "Hong Kong"）而未给出正式名称，则保留为 `""`，不要用地点字段代替名称字段。如果是 `country_site` 等入口条目，官网原始入口名称可以直接写入该字段。
- `country_or_region`：官网原始国家、地区或司法辖区值。
- `country_or_region_standardized`：标准化后的国家地区短码。
  - 普通国家或地区：统一使用 2 位 ISO 标准短码，例如 `CN`（中国大陆）、`HK`（中国香港）、`GB`（英国）、`JP`（日本）、`SG`（新加坡）等。
  - 美国各州：**必须**转换为 4 位特殊地区码，格式为 **`US` + 2位美国邮政官方州名缩写（USPS Code）**，常用映射对照如下（英文/中文名均适用）：
    - 特拉华州 (Delaware) ➡️ `USDE`
    - 纽约州 (New York) ➡️ `USNY`
    - 得克萨斯州 (Texas) ➡️ `USTX`
    - 加利福尼亚州 (California) ➡️ `USCA`
    - 罗德岛州 (Rhode Island) ➡️ `USRI`
    - 华盛顿州 (Washington State) ➡️ `USWA`
    - 马萨诸塞州 (Massachusetts) ➡️ `USMA`
    - 佛罗里达州 (Florida) ➡️ `USFL`
    - 伊利诺伊州 (Illinois) ➡️ `USIL`
    - 新泽西州 (New Jersey) ➡️ `USNJ`
    - 其他州同样遵循 `US + USPS两位州码` 规则。若美国分支只提到了国家 `United States / US` 而未指明具体州，则输出为 `US`。
- `address`：该分支机构对应的具体地址。
- `phone`：该分支机构对应的专属电话。
- `fax`：该分支机构对应的专属传真。
- `email`：该分支机构对应的专属邮箱。
- `website`：该分支条目明确对应的官方链接、地区站链接、子站链接或详情页链接。

---

## 数组存储规则
- 所有数组字段都必须按条逐一存储，每个数组元素只对应一条独立信息，不能把多条内容合并到同一个字符串中。
- 对于 `other_addresses`、`other_emails`、`other_contacts`、`fax`、`executives`、`shareholders`、`branch_entities` 这类字段，均使用数组形式逐条记录。

---

## 数值字段规则（适用于 `subscribed_amount`、`paid_in_amount`、`shareholding_ratio`）
这三个字段在数据库中为 `decimal` 类型，因此输出值**必须为可直接解析为数字的纯数值字符串**，不得包含任何非数字字符（数字、小数点、负号除外）。
1. **金额字段**（`subscribed_amount`、`paid_in_amount`）：
   - ✅ 正确示例：`"10000000"`、`"500000.00"`、`"1234567.89"`
   - ❌ 错误示例：`"人民币1000万元"`、`"USD 10,000,000"`、`"1000万"`、`"¥500,000"`、`"10M"`
   - 必须将中文数量词转换为完整数字，例如：`"1000万"` → `"10000000"`，`"1.5亿"` → `"150000000"`
   - 必须去除千位分隔符（逗号）以及货币符号（¥、$、€ 等）与货币名称（人民币、USD 等），币种信息应写入对应的 `subscribed_currency` 或 `paid_in_currency` 字段。
2. **比例字段**（`shareholding_ratio`）：
   - ✅ 正确示例：`"50.00"`、`"33.33"`、`"100"`、`"0.5"`
   - ❌ 错误示例：`"50%"`、`"百分之五十"`
   - 必须去除百分号 `%` 并直接输出百分比数值本身，若原文为小数形式表示比例（如 `0.5`），保持原始数值 `"0.5"`。
3. **通用规则**：若网页未披露对应数值，保留为空字符串 `""`，不得填入 `"0"` 或 `"N/A"`。

---

## 日期字段规则（适用于 `registration_date`、`birth_date`、`appointment_date`、`shareholding_date`）
这些日期相关的字段，在输出值时必须满足以下标准化格式要求：
1. **完整日期**：如果网页中同时披露了年、月、日，**必须**标准化为 `yyyy-MM-dd` 格式。
   - ✅ 正确示例：`"2026-07-08"`、`"1985-12-05"`
   - ❌ 错误示例：`"2026/07/08"`、`"2026年7月8日"`、`"July 8, 2026"`、`"08-07-2026"`
2. **仅含年月**：如果网页中仅披露了年份和月份（缺失具体日期），**必须**标准化为 `yyyy-MM` 格式，切勿强行捏造日期补齐天数。
   - ✅ 正确示例：`"2026-07"`、`"1985-12"`
   - ❌ 错误示例：`"2026-07-01"`（若原文未提及，不得补充 `-01` 等尾缀）、`"2026/7"`、`"2026年7月"`
3. **仅含年份**：如果网页中仅披露了年份，输出为 `yyyy` 格式（如 `"2026"`），不要强行补充月或日。
4. **日本年号/本地历法换算**：如果网页中使用的是非公元纪年，例如日本年号（如 令和、平成、昭和纪年）或其它本地历法，**必须换算为公元纪年**输出。
   - ✅ 正确示例：`"令和6年7月8日"` ➡️ `"2024-07-08"`，`"平成30年10月"` ➡️ `"2018-10"`，`"昭和60年"` ➡️ `"1985"`
5. **空值处理**：若网页未披露对应日期，统一保留为空字符串 `""`，不得填入 `"N/A"`、`"0"`、`"0000-00-00"` 等。

---

## 结果值清洗规则
- `result.json` 中的字符串值不应保留原始网页中的多余换行符 `\n`、连续空行或无意义缩进。
- 在不改变原始内容含义的前提下，应将字段值整理为单行或紧凑格式，使用单个空格连接原本被换行拆开的内容。
- 地址、公司简介、经营范围、高管人员简介等简介型、长正文字段，应尽可能保留官网原始完整内容，不应默认只截取首句、标题或摘要句，但要做好去换行清洗。
- 若官网以表格、列表、卡片、地图结果、筛选结果、下拉选项、地区选择器等形式披露分支条目，应优先完整收录所有可识别条目，再做格式清洗。
