# Repository Guidelines

## 项目结构与模块组织
本仓库按 **skill（技能）** 组织，每个技能为根目录下的一个文件夹。

- `README.md`：仓库总览。
- `homepage-info-extractor/`：当前技能实现。
- `homepage-info-extractor/SKILL.md`：技能定义与执行规范。
- `homepage-info-extractor/assets/templates/template-table.md`：主页信息抽取固定模板。
- `homepage-info-extractor/references/`：参考资料。
- `results/`：结果输出目录。产物放在 `results/<YYYYMMDD>/<skill-name>/` 下（如不存在可创建）。

示例：`results/20260202/homepage-info-extractor/example.com.md`。

## 构建、测试与开发命令
仓库未配置构建系统或自动化测试。

开发中建议使用轻量命令：

- `rg --files`：快速列出文件。
- `rg "pattern" homepage-info-extractor/`：检索技能内容。
- `ls results/`：检查结果文件与命名。

## 编码风格与命名规范
- 文档使用简洁 Markdown，标题清晰。
- 默认使用 ASCII 字符。
- 技能目录使用 **kebab-case**（如 `homepage-info-extractor/`）。
- 输出路径固定：`results/<YYYYMMDD>/<skill-name>/...`。
- 非必要不新增无关脚手架或配置。

## 测试指南
未使用测试框架，采用人工校验：

- Markdown 渲染正常。
- 文档中的路径真实存在。
- 输出路径符合约定。
- 技能说明前后逻辑一致。

对抽取任务，需确认字段为原文摘录，并可追溯到来源 URL 与定位器。

## 提交与合并请求规范
提交信息建议使用简短祈使句，例如：

- `Add homepage info extractor skill`
- `Update extraction template wording`

PR 建议包含：

- 变更内容与目的。
- 受影响文件路径。
- 若影响产物生成，附示例输出路径。

## Agent 专用说明
- 每个技能必须在独立目录内定义 `SKILL.md`。
- 执行主页信息抽取时，严格遵循 `homepage-info-extractor` 规则：仅保留原文、记录来源 URL 与定位器、使用固定模板 `homepage-info-extractor/assets/templates/template-table.md`。
