# 技术/架构设计文档专用评审方法

> 当对象类型 = 技术架构设计 时加载。核心：**强制 tradeoff 显式化** + **反向审计 ADR** + **6 支柱覆盖检查**。

## 1. ATAM 场景驱动评审

出处：Kazman, Klein, Barbacci, SEI CMU — [Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-atam/)。

核心：架构评审不能开放问"好不好"——必须基于**具体场景**评审。每场景对应 quality attribute（性能/可用性/可改性/安全/...）。tradeoff 显式化后才能判断。

操作：
1. 识别文档中显式/隐含的 quality attributes
2. 为每个 quality attribute 构造 3-5 个**具体场景**（如：双 11 流量峰值 10000 QPS 持续 1h / 单 AZ 宕机 5 分钟内切换 / 新增支付方式开发+测试 ≤2 周 / 内部员工账号被盗无法访问生产数据）
3. 对每场景走查架构：能否满足？瓶颈在哪？
4. 找 tradeoff：满足 A 是否牺牲 B？tradeoff 是否显式承认？
5. 找 risk：架构无法满足的场景 = Critical

典型问题清单：文档是否枚举关键场景？每个 quality attribute 有**可量化目标**（如 "P99 < 100ms"）？有容量规划？失败模式枚举？降级策略？第三方依赖 SLO 与本系统 SLO 匹配？（如依赖 99.9% 但承诺 99.99% = SLA 风险）

## 2. ADR 反向审计

出处：Nygard, *Documenting Architecture Decisions*；[ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar/techniques/architecture-decision-records)；[Fowler bliki](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)。

核心：每个架构决策应有 ADR——context + decision + alternatives + consequences + compliance。**反向审计**所有显式和隐式决策，让作者补齐。

ADR 字段：

| 字段 | 内容 |
|---|---|
| Title | 决策一句话标题 |
| Status | Proposed / Accepted / Deprecated / Superseded |
| Context | 为什么需要？约束和考虑？ |
| Decision | 决策内容（"我们决定..."） |
| Alternatives | 考虑过的其他选项（**至少 2-3 个，最常缺失**） |
| Consequences | 正面 + 负面 + 风险 |
| Compliance | 如何验证决策被执行？ |

典型失败：**没有任何 alternatives** → High（"为什么不是 B/C？"）；缺 context → 难理解；缺 consequences → 决策风险未知。

## 3. Cognitive Dimensions of Notations

出处：Green & Petre — [Cognitive Dimensions Resource Site](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/)。

核心：评价**信息制品**（API、DSL、配置、schema、架构图）的认知成本。14 维度，评审时选最相关 5-7 个：

| 维度 | 评审提问 |
|---|---|
| Abstraction Gradient | 抽象/具体层次过渡平滑？ |
| Consistency | 相似语义有相似语法？ |
| Error-Proneness | 易犯错？错误易发现？ |
| Hidden Dependencies | 依赖关系可见？改字段影响哪些下游？ |
| Premature Commitment | 被迫在信息不足时做决定？ |
| Progressive Evaluation | 能部分完成、中途检查？能 dry-run？ |
| Role-Expressiveness | 每部分目的可见？一眼看出干啥？ |
| Viscosity 黏度 | 修改成本？改一字段动几文件？ |

API 设计 7 个最相关：Abstraction Gradient / Consistency / Error-Proneness / Hidden Dependencies / Role-Expressiveness / Viscosity / Working-Step。

## 4. AWS / Azure Well-Architected 框架

出处：[AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)；[Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/)。

6 支柱：

| 支柱 | 评审提问 |
|---|---|
| Operational Excellence | 部署/监控/事件响应流程？runbook？ |
| Security | 零信任？数据加密？权限最小化？审计日志？ |
| Reliability | RTO/RPO？容量冗余？降级路径？ |
| Performance Efficiency | 能 scale？瓶颈识别？资源利用率？ |
| Cost Optimization | 单位经济？长期成本？idle 资源？ |
| Sustainability | 能耗？碳足迹？资源循环？ |

即使非云架构，6 支柱**思维方式**（"是否考虑了运营/安全/可靠性/..."）仍适用。

## 5. Pattern / Anti-pattern Catalogs

出处：Fowler, *PoEAA*；[arXiv SOA anti-patterns](https://dl.acm.org/doi/10.1145/3180155.3180215)。

常见 microservices anti-patterns（嗅觉库）：Cyclic dependency / Shared database / Too many standards / ESB misuse / Nanoservices / Monolithic database / Hard-coded service address / **Sync chain**（同步链过长）/ Shared persistence / API versioning neglect。

评审：通读架构图 → 对照 anti-pattern 列表 → 发现暗合时形成 High 问题 → 但必须结合 context 评审（某些 anti-pattern 在特定场景是合理 tradeoff）。

## 技术/架构文档评审清单

| # | 检查 | 主用方法 |
|---|---|---|
| 1 | 文档是否枚举关键**场景**？ | ATAM |
| 2 | 每个 quality attribute 有**可量化目标**？ | ATAM |
| 3 | 文档是否有显式 **ADR**？ | ADR 反向审计 |
| 4 | 隐式决策（"我们用 X"）解释了**为什么**？ | ADR 反向审计 |
| 5 | 关键 notation 的 **Cognitive Dimensions** OK？ | CDN |
| 6 | 是否考虑 **6 支柱**（运营/安全/可靠/性能/成本/可持续）？ | Well-Architected |
| 7 | 是否暗合某个 **anti-pattern**？ | Pattern catalogs |
| 8 | 失败模式 / 降级路径 / 容量规划是否覆盖？ | ATAM + Well-Architected |
| 9 | 第三方依赖 SLO 与本系统 SLO 匹配？ | ATAM |
