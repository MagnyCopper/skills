# References 导航

> expert-reviewer skill 的方法论详解库。按 SKILL.md 的对象类型路由加载。
> 每个 references 文件聚焦一个方法论家族，包含：核心思想、出处、操作步骤、关键提问、局限。

## 文件索引

| 文件 | 用途 | 加载时机 |
|---|---|---|
| `methodology-foundations.md` | 通用层方法论详解（Toulmin / Walton / Paul-Elder / Pre-mortem） | Stage 3-4 时必读 |
| `technical-architecture-review.md` | 技术/架构专用方法 | 对象类型=技术架构时 |
| `business-product-review.md` | 业务/产品专用方法 | 对象类型=业务产品时 |
| `paper-academic-review.md` | 论文/报告专用方法 | 对象类型=报告论文时 |
| `source-evaluation.md` | 证据链验证（SIFT / Lateral Reading / CRAAP） | Stage 3 + Stage 5 |
| `bias-checks.md` | 偏倚检查（CIA SAT / ACH / Noise hygiene） | Stage 4 |

## 加载优先级

1. `methodology-foundations.md` — 始终加载（通用层）
2. `<对象类型>-review.md` — 按检测到的对象类型加载
3. `source-evaluation.md` — 始终加载
4. `bias-checks.md` — 仅当文档含决策/推荐时加载
