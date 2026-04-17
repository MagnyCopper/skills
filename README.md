# skills
AI Agent 技能仓库

## 可用技能

- `homepage-info-extractor/`：从官网首页与必要子页面原文提取指定字段，并写入 `results/<YYYYMMDD>/<skill-name>/` 下的结果文件。
- `company-domain-finder/`：根据企业名称和国家/地区，通过多源搜索和验证找到企业官网域名。输出为固定 JSON 格式，存放在 `results/<YYYYMMDD>/company-domain-finder/<company_id>.json`。
- `overseas-registry-source-research/`：研究特定国家/地区/行业的官方数据源和第三方数据源。

## 输出约定

- 结果存放在 `results/<YYYYMMDD>/<skill-name>/`。
- 日期格式为 `YYYYMMDD`。
- 主页信息抽取：若字段包含多条记录（如高管列表），在主表下方新增独立表格，并在主表对应行注明"见下方表格"。
- 域名查找：输出为 JSON 文件，key 固定不变，`official_domain` 为唯一最佳结果或 `null`。
