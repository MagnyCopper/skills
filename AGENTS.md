# Repository Guidelines

## 项目结构与模块组织
- 根目录文档：`README.md`。
- 技能以目录形式存放在根目录（当前为 `homepage-info-extractor/`）。
- 每个技能目录包含 `SKILL.md` 以及资源文件（例如 `homepage-info-extractor/assets/templates/template-table.md`）。
- 生成结果统一写入 `results/`，命名规则为 `results/<skill-name>+YYYYMMDD.md`。

## 构建、测试与开发命令
- 本仓库未定义构建或运行命令。
- 日常查看可使用命令行工具，例如 `rg --files` 以列出文件。

## 编码风格与命名规范
- 文档使用 Markdown，标题简洁清晰。
- 默认使用 ASCII 字符。
- 目录命名：技能目录使用 kebab-case（如 `homepage-info-extractor/`）。
- 输出命名：`results/<skill-name>+YYYYMMDD.md`（示例：`results/homepage-info-extractor+20260202.md`）。

## 测试指南
- 未配置自动化测试框架。
- 通过人工检查验证：Markdown 渲染、路径、标题与命名规则是否正确。

## 提交与合并请求规范
- 提交历史较少，未体现严格规范。建议使用简短、祈使句式的摘要（示例：“Add homepage info extractor skill”）。
- 合并请求建议包含：
  - 清晰的变更说明。
  - 新增或更新的模板及其路径。
  - 如影响结果生成，提供示例输出文件名。

## Agent 专用说明
- 技能必须在技能目录内以 `SKILL.md` 定义。
- 若执行主页信息抽取，严格遵循技能规则：仅原文、记录来源 URL 与定位器、使用固定模板 `homepage-info-extractor/assets/templates/template-table.md`。
