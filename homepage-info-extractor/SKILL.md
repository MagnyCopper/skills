---
name: homepage-info-extractor
description: 根据用户提供的机构或企业官网入口与字段清单，从官网首页及必要子页面中原文提取指定字段，并将结果按固定表格模板输出到项目 results 目录。适用于需要精准、逐字来源提取、且只允许原文、不做加工的官网信息抽取任务。
---

# 主页信息提取

按以下流程从指定官网中**原文提取**字段，并保存到 `/Users/han/Projects/skills/results/<skill-name>+YYYYMMDD.md`。

## 必要输入

- 官网入口 URL（每次由用户提供）
- 字段清单（每次由用户提供，字段会变化）
- 输出模板：固定使用 `assets/templates/template-table.md`

## 严格规则

- 只允许**原文提取**，禁止改写、总结、翻译、归一化。
- 不推测缺失字段。找不到的字段写 `NOT FOUND`，并列出已检查页面。
- 尽量保持原有标点与换行。
- 每个字段必须记录来源网址和定位器（CSS 或 XPath）。
- 若字段包含多条记录（如高管/人员列表），在主表下方新增独立表格逐条拆分，保持原文顺序，并在主表该字段的“提取文本（原文）”写明“见下方表格”。

## 浏览与上下文节省

- 使用 Playwright 进行页面访问与 DOM 提取。
- 阻止无关资源加载以节省上下文：
  - 阻止：images、media、fonts
  - 允许：document、script、stylesheet、xhr/fetch
- 只访问必要页面：
  1) 先访问首页
  2) 若字段缺失，仅跟进相关导航（如：关于我们、公司、联系、投资者、新闻、法务）

## 操作流程

1) 确认输入（URL、字段清单）。
2) 以资源拦截方式加载首页。
3) 从首页提取可找到的字段。
4) 若仍有缺失字段，打开最相关子页面继续提取。
5) 为每个字段记录：
   - 原文文本
   - 来源网址
   - 来源定位器（CSS 或 XPath）
6) 使用固定模板输出到 `/Users/han/Projects/skills/results/<skill-name>+YYYYMMDD.md`。

## 输出要求

- 文件名：`<skill-name>+YYYYMMDD.md`
- 目录：`/Users/han/Projects/skills/results/`
- 模板：`assets/templates/template-table.md`（不得改结构）
