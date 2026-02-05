---
name: homepage-info-extractor
description: 从机构或企业官网精准提取指定数据（如名称、历史、联系方式、人员）并输出为标准 Excel 扁平化报告。适用于需要进行专业网页抓取或官网信息抽取任务，且要求严格原文提取、提供可验证的 XPath 来源以及遵守特定字段逻辑的场景。
---

# 官网信息提取

从指定官网执行**原文信息提取**，并将结果以 Excel 扁平化视图进行保存。

## 核心工作流

1.  **初始化**：读取 [EXTRACTION_FIELDS.md](references/EXTRACTION_FIELDS.md) 明确目标字段及逻辑。
2.  **页面访问**：使用 `browser_navigate` (Playwright) 访问目标官网。
    *   **资源拦截**：必须严格阻止 `stylesheet` (CSS), `image`, `media`, `font` 加载。
3.  **智能寻址与深度发现**（Level 1）：分析首页导航、页脚、Sitemap，遍历高概率子页面。
4.  **外部搜索引擎补救**（Level 2 - **仅用于发现内部链接**）：
    *   若核心字段缺失，使用 `google_web_search` 搜索 `site:<目标域名> <关键词>`。
    *   **域名隔离原则（核心约束）**：
        *   **禁止**从搜索结果中的第三方网站（如维基、百度百科、第三方报道）提取任何数据。
        *   **仅允许**点击并进入搜索结果中属于 **目标域名 (Official Domain)** 的链接进行提取。
        *   如果搜索结果中没有任何链接指向目标域名，则该字段必须保持留空。
5.  **原文提取**：必须逐字记录官网文本，记录来源 URL 和精确的 XPath。
6.  **数据完整性规则**：
    *   **留空规则**：未找到原文的字段，其文本、URL 和 XPath 三列必须全部留空。
    *   **别名表 (6254)**：仅处理英文全称、繁体全称、简体全称、简称和曾用名。
    *   **人员表 (6489)**：全量提取。
7.  **输出结果与备注**：生成报告并填写末尾的“提取备注与困难”章节。

## 输出与归档要求

- **存储路径**：`/Users/han/Projects/skills/results/YYYYMMDD/`。
- **命名规范**：`<目标官网域名>+YYYYMMDD.md`。
- **独立性**：一个官网一个文件。

## 资源参考

- **字段逻辑定义**：详见 [references/EXTRACTION_FIELDS.md](references/EXTRACTION_FIELDS.md)。
- **输出模板**：详见 [assets/templates/template-table.md](assets/templates/template-table.md)。