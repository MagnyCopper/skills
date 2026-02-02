# 结果

- Skill: homepage-info-extractor
- 日期: YYYYMMDD
- 目标网址: https://example.com
- 来源页面:
  - https://example.com

## 字段

| 字段 | 提取文本（原文） | 来源网址 | 来源定位器 |
| --- | --- | --- | --- |
| 字段A | 与官网一致的原文文本 | https://example.com/about | css=main h1 |
| 字段B | 另一段原文文本 | https://example.com | xpath=//footer//a[1] |
| 多条记录示例 | 见下方“多条记录表格示例” | https://example.com/team | css=table.team |

### 多条记录表格示例

| 职位 | 姓名 | 来源网址 | 来源定位器 |
| --- | --- | --- | --- |
| 职位1 | 姓名1 | https://example.com/team | css=table.team |
| 职位2 | 姓名2 | https://example.com/team | css=table.team |
