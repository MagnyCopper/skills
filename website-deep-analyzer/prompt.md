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
  ]
}
```

`company_name` 字段说明：
- `company_name` 为公司名称对象。
- `company_name.english_name` 用于存储公司英文全称，优先保留网页原始写法。
- `company_name.short_names` 为数组，用于逐条存储公司简称、品牌简称、证券简称或不同语言版本简称。
- `company_name.short_names` 必须按条逐一存储，每个数组元素只对应一个简称，例如 `["Kidswell", "キッズウェル・バイオ"]`。
- 若网页仅披露一个简称，也必须以数组形式存储；若未披露则保留为 `[]`。

结果值清洗补充规则：
- `result.json` 中的字符串值不应保留原始网页中的多余换行符 `\n`、连续空行或无意义缩进。
- 在不改变原始内容含义的前提下，应将字段值整理为单行或紧凑格式，使用单个空格连接原本被换行拆开的内容。
- 地址、简介、经营范围、人员简介等字段同样不应在最终 `result.json` 中保留原始 HTML 换行。
- `company_intro` 必须优先提取公司简介、公司定位、公司概述等正文内容，不能使用导航词、菜单项、页面标题拼接结果代替。
- `business_scope` 必须优先提取主营业务、业务板块、经营范围、产品与服务范围等正文内容，不能使用导航菜单、面包屑或页头栏目名代替。
- 对于 `company_intro`、`business_scope`、`personnel_info.executives[].biography` 这类简介型字段，应尽可能保留官网原始完整内容，不应默认只截取首句、标题句或摘要句。
- 若官网页面存在多段连续正文来描述公司简介、经营范围或人物简介，应优先完整收录相关正文，再做格式清洗；除非内容明显属于导航、页脚、无关说明或重复噪音。

**说明**：
- 所有字段在提取时，应优先存储网页中的原始值，并尽量保留网页原始展示格式。
- 除非字段规则明确要求拆分、归类或结构化，否则不要主动改写原文、翻译原文、标准化日期格式、统一电话号码格式或重组地址格式。
- 如果网页中的字段值本身带有换行、分隔符、括号、国家区号、大小写、职位全称或其他格式信息，应尽量按原始形式保留。
- `company_intro`：企业简介、公司概况、公司介绍等简要信息。
- `business_scope`：经营范围、主营业务、核心业务、产品与服务范围等信息。
- `registration_date`：企业注册日期、成立日期、incorporation date、establishment date 等，但前提是该日期明确对应企业法人主体本身。
- `address`：应尽量区分不同类型地址。无法明确归类的地址放入 `other_addresses`。
- `email`：应尽量区分不同类型邮箱。无法明确归类的邮箱放入 `other_emails`。
- `contact`：应尽量区分不同类型联系电话或联络方式。无法明确归类的号码放入 `other_contacts`。
- `fax`：传真号码单独提取，不放在 `contact` 对象下，并且必须使用数组存储。
- 所有数组字段都必须按条逐一存储，每个数组元素只对应一条独立信息，不能把多条内容合并到同一个字符串中。
- 对于 `other_addresses`、`other_emails`、`other_contacts`、`fax` 这类字段，应使用数组形式逐条记录，例如 `["item 1", "item 2"]`。
- 在分类存储时，只改变字段归属，不改变字段值本身的原始表达方式。
- `executives` 数组中的每个高管对象必须且仅包含以下七个字段：
  - `name`：人员姓名
  - `title`：完整职位头衔
  - `position`：职位代码，例如 CEO、CFO、CTO、COO；如果没有明确职位代码则为 `""`
  - `birth_date`：出生日期
  - `appointment_date`：任职日期、就职日期、上任日期或该岗位任期开始日期
  - `gender`：性别
  - `biography`：人员简介
- `shareholders` 数组中的每个股东对象必须且仅包含以下十二个字段：
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

**数值字段规则（适用于 `subscribed_amount`、`paid_in_amount`、`shareholding_ratio`）**：

这三个字段在数据库中为 `decimal` 类型，因此输出值**必须为可直接解析为数字的纯数值字符串**，不得包含任何非数字字符（数字、小数点、负号除外）。

具体要求：
1. **金额字段**（`subscribed_amount`、`paid_in_amount`）：
   - ✅ 正确示例：`"10000000"`、`"500000.00"`、`"1234567.89"`
   - ❌ 错误示例：`"人民币1000万元"`、`"USD 10,000,000"`、`"1000万"`、`"¥500,000"`、`"10M"`
   - 必须将中文数量词转换为完整数字，例如：`"1000万"` → `"10000000"`，`"1.5亿"` → `"150000000"`，`"50億"` → `"5000000000"`
   - 必须去除千位分隔符（逗号），例如：`"10,000,000"` → `"10000000"`
   - 必须去除货币符号（¥、$、€、£、₹ 等），币种信息应写入对应的 `subscribed_currency` 或 `paid_in_currency` 字段
   - 必须去除货币名称（人民币、USD、RMB、美元、日元 等），币种信息应写入对应的 currency 字段
   - 若原文为 `"人民币1000万元"`，则 `subscribed_amount` 应为 `"10000000"`，`subscribed_currency` 应为 `"人民币"` 或 `"CNY"`
2. **比例字段**（`shareholding_ratio`）：
   - ✅ 正确示例：`"50.00"`、`"33.33"`、`"100"`、`"0.5"`
   - ❌ 错误示例：`"50%"`、`"百分之五十"`、`"50パーセント"`
   - 必须去除百分号 `%` 及其他百分比表示符号
   - 直接输出百分比数值本身，例如：`"50%"` → `"50"`，`"33.33%"` → `"33.33"`
   - 若原文为小数形式表示比例（如 `0.5` 表示 50%），应保持原始数值 `"0.5"`，不做转换
3. **通用规则**：
   - 若网页未披露对应数值，保留为空字符串 `""`，不得填入 `"0"` 或 `"N/A"`
   - 最终值必须满足：去除引号后，能被任意编程语言的 `parseFloat()` 或 `Decimal()` 直接解析为数字
