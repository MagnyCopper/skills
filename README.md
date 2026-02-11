# skills
AI Agent 技能仓库

## 可用技能

- `homepage-info-extractor/`：从官网首页与必要子页面原文提取指定字段，并写入 `results/<YYYYMMDD>/<skill-name>/` 下的结果文件。

## 输出约定

- 结果存放在 `results/<YYYYMMDD>/<skill-name>/`。
- 日期格式为 `YYYYMMDD`。
- 若字段包含多条记录（如高管列表），在主表下方新增独立表格，并在主表对应行注明“见下方表格”。
