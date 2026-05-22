---
name: company-domain-finder
description: "Use when discovering or verifying a company's official website domain, especially when the target legal entity has a country or jurisdiction."
---

# Company Domain Finder

本技能用于查找企业官方网站域名，并判断候选域名对应的**法人主体**是否就是用户传入的目标企业。

核心目标不是"找到同名品牌网站"，而是"找到目标国家/地区下目标法人主体可下载、可采信的官网域名"。

---

## ⚠️ 最高优先级：文件保存规则（绝对约束）

**你必须完成以下两件事，缺一不可：**

1. **先创建目录**：根据传入的 `wdcode` 参数，执行 `mkdir -p temp/aidomain/<wdcode>/` 创建目录。
2. **必须写文件**：搜索完成后，必须将结果 JSON 保存到 `temp/aidomain/<wdcode>/domain.json` 文件中，绝不能使用默认路径，也不能只在对话中输出。

必须阅读并严格遵守同目录下的 `prompt.md` 中定义的技术契约（输入参数、JSON 输出 Schema 以及置信度 A-D 评级标准）。

## 强制规则：法人主体归属验证

候选 URL 只有通过法人主体归属验证后，才能进入 `domains`。

`domains` 输出的是域名结果，不是证据页面 URL。任何 About、Contact、Legal、Privacy、办公室页面等长路径 URL 只能作为核验证据，不能直接当作最终域名结果展示。

以下情况即使域名真实、品牌匹配、搜索排名靠前，也不能作为可下载官网输出：

- 网站主体是外国母公司、上市母公司或集团总部，而用户要的是某个国家/地区子公司、分支机构或本地法人。
- 网站主体是子公司、关联公司、经销商、品牌站、产品站，而不是用户传入的目标法人。
- 网站只在第三方目录里被列为 website，但官网页面本身没有法人主体、注册地址、注册号或明确运营主体证据。
- 法律声明、隐私政策、服务条款、页脚版权、投资者关系页面或工商/证券资料显示网站属于其他国家/地区或其他法人。
- 同名公司存在于多个国家/地区，候选域名无法证明归属于 `country` 下的目标企业。

所有搜索到的候选 URL（包括不符合目标法人的）都应放入 `domains` 数组中，通过置信度 `confidence_level` 的 A/B/C/D 评级以及 `accept_for_download` 来区分它们，不要直接丢弃。

## 执行步骤

1. **创建输出目录**：按用户 prompt 中指定的路径，先执行 `mkdir -p` 创建目录。

2. **搜索候选域名**
   - 使用精确公司名搜索：`"company_name" official website`、`"company_name" domain`。
   - 加入目标国家/地区：`"company_name" "country" website`。
   - 按国家/地区加入本地注册号关键词（Singapore UEN/ACRA，Australia ABN/ACN，UK Companies House，India CIN/GSTIN，France SIREN/SIRET 等）。
   - 检查权威来源：官方工商系统、证券交易所公告、年报、LEI、LinkedIn、Bloomberg、Wikipedia、当地商业目录。

3. **抓取并核验网站内容**
   - 优先查看首页、About/About Us、Contact、Legal notice、Terms、Privacy Policy、Imprint、Footer、Investor Relations。
   - 提取法人名称、国家/地区、注册号、注册地址、办公地址、邮箱域名、版权归属、母子公司关系描述。

4. **执行法人主体归属验证**
   - 至少满足一个强证据，或两个相互独立的中等证据，且不能存在强冲突。
   - 强证据：官网明确出现目标法人完整名称；注册号匹配；法律页面显示运营主体就是目标法人；官方登记资料绑定域名；注册地址匹配。
   - 中等证据：About 页面出现目标法人名称+国家/地区+业务描述；办公室页面信息匹配；可信第三方绑定域名；LinkedIn/年报印证。
   - 强冲突：法律主体显示为其他国家公司；About 页面只介绍集团/母公司；候选站明确是集团站/品牌站/经销商站。

5. **关系分类**（为每个候选 URL 标注 `relationship_to_target`）：
   `same_entity`、`local_entity_operated_site`、`foreign_parent_or_group_site`、`subsidiary_or_affiliate_site`、`branch_or_representative_office`、`same_name_different_jurisdiction`、`brand_or_product_site`、`directory_only_unverified`、`unknown`。

6. **写入结果文件**：将包含 `domains` 的 JSON 数据写入到 `temp/aidomain/<wdcode>/domain.json`，写入后确认文件已存在。


## 全球企业特别规则

当企业为跨国集团时，必须以 `country` 为准。如果候选域名对应外国母公司/集团站而非目标国家法人自身的网站，必须拒绝。
