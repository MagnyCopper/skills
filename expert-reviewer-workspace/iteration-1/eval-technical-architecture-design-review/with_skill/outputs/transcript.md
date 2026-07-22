# Transcript — Expert Reviewer Skill 执行记录

## 任务

按 expert-reviewer skill 的 5 阶段工作流评审一份"双 11 大促微服务订单系统"设计（口述形式），输出 review-report.md + transcript.md。

## 加载的文件

### 1. Skill 主文件（必读）

- `/Users/han/Projects/skills/expert-reviewer/SKILL.md` —— 全文 290 行

### 2. 对象类型路由加载（PARSE 阶段检测为"技术/架构设计"）

按 SKILL.md "对象类型路由" 表，技术/架构设计类型应加载：

- `references/technical-architecture-review.md`（219 行）—— ATAM + ADR 反向审计 + Cognitive Dimensions + Well-Architected + Pattern Catalogs + Diátaxis
- `references/methodology-foundations.md`（305 行）—— Paul-Elder + PBR + Toulmin + Walton + Pre-mortem + Diátaxis
- `references/source-evaluation.md`（203 行）—— SIFT + Lateral Reading + CRAAP + Reuters/Snopes/PolitiFact + IFCN
- `references/bias-checks.md`（285 行）—— Pre-mortem + Key Assumptions + ACH + Devil's Advocacy + Red Team + What If + HILP + Outside-In + Noise + Confirmation
- `assets/templates/perspective-questions.md`（121 行）—— 5 视角预设问题库
- `assets/templates/review-report-template.md`（214 行）—— 完整输出模板

**未加载**：

- `references/business-product-review.md` —— 对象类型不匹配
- `references/paper-academic-review.md` —— 对象类型不匹配

## 5 阶段执行记录

### Stage 1 — PARSE

- **输入形式**：对话口述（无文件路径/URL）
- **文档体量**：约 130 字，一段自然语言
- **对象类型检测**：技术/架构设计（依据：出现"微服务订单系统"、"Spring Cloud / Gateway / Nacos / OpenFeign"、"订单流程"、"双 11 大促"）
- **Paul-Elder 8 要素拆解**：仅 Information（技术栈+流程顺序）部分覆盖；Purpose（双 11）模糊；Question / Inference / Assumption / Implications / POV 均缺失或薄弱。详见报告"Paul-Elder 8 要素覆盖"表。

### Stage 2 — PERSPECTIVES（5 视角独立扫描）

按 perspective-questions.md 的 5 视角各 8 个问题独立扫描，**未交叉影响**：

- 视角 1 实现者：发现 ADR 缺失、分布式事务未指定、分库分表缺失、OpenFeign 无容错配置、Kafka 角色未定
- 视角 2 维护者：发现可观测性缺失、对账缺失、降级路径缺失、灰度/回滚缺失、Nacos 单点
- 视角 3 用户/客户：发现失败订单体验未定义、P99 RT 隐含过高、QPS 目标未提
- 视角 4 反对者/竞争对手：发现无幂等（重放）、无限流（恶意流量）、无鉴权（越权）、无审计（内部作恶）、库存超卖
- 视角 5 决策者/投资人：发现无 ROI、无容量规划、无放弃条件、无 SLA 承诺

按 Parnas Active Design Reviews 原则，每视角先做"肯定断言"（哪些是 OK 的），再列问题。本报告为节省篇幅把 OK 部分隐含在"建设性视角"里。

### Stage 3 — ARGUMENTS（Toulmin + Walton）

选 3 个核心论证做 Toulmin 拆解（详见报告"核心论证的 Toulmin 拆解"）：

1. 用同步调用 + 回滚能支撑双 11（Claim 模糊 + Warrant 错误 + Backing 缺失）
2. 如果中间失败就回滚（Warrant 错误——跨库无原子回滚）
3. 三服务各一库 = 微服务（缺 Backing + 缺 Rebuttal）

Walton critical questions 选用了：

- 实践型（论证 #1）
- 因果型（论证 #2）
- 专家意见型（论证 #3）

### Stage 4 — DECISIONS

文档包含决策/推荐（"应该用同步调用 + 回滚"），强制走三项检查：

- **Pre-mortem**：列 10 个最可能失败原因（详见报告 Pre-mortem 表）
- **Key Assumptions Check**：列 10 个关键假设（8 个隐含，3 个错误）
- **ACH**：构造 4 个竞争假设（A 同步回滚 / B TCC / C Saga / D Outbox），诊断性分析指出 D 与"已有 Kafka + 双 11 削峰"诊断性最强

### Stage 5 — REPORT

按 review-report-template.md 输出，严格保留：

- 元信息表
- 总览（评分 + 一句话结论 + 问题分布表）
- 详细问题清单（每个问题 7 字段：严重等级 / 发现阶段 / 视角 / 原文引用 / 方法论依据 / 🟥 红队视角 / 🟩 建设性视角）
- 结构化发现汇总（Paul-Elder / 5 视角 / Toulmin / 关键假设 / Pre-mortem / ACH）
- 评审者自评（未覆盖 / 偏倚来源 / 如果只能改一件事）
- 附录（方法论清单）

**三证据齐全规则自查**：每个问题均含 (1) 原文引用 + 段落定位（用户原文 + 缺失字段说明），(2) 方法论依据（方法名 + 核心提问 + references 路径），(3) 严重等级（四档）。✅ 通过。

**双视角同时输出自查**：每个问题均含 🟥 红队视角 + 🟩 建设性视角。✅ 通过。

## 关于范围与重点的决策

### 决策 1：对象类型判为"技术/架构设计"，不走"混合"路径

依据：用户原文 100% 是技术架构描述（栈选型 + 流程 + 容量目标），无业务/产品/学术元素。

### 决策 2：以"双 11 大促"为评审锚点，放大容量/一致性/可靠性维度权重

用户显式说"越严越好"+ 显式说"支撑双 11 大促"，且双 11 同类系统（淘宝/京东）公开历史故障丰富。这给评审者一个强锚点，可对照真实 reference class 评判。

### 决策 3：Critical 等级判定标准从严

因为用户说"越严越好"，且涉及"扣余额"等资金场景，所有"未预防则双 11 必然发生严重事故"的问题均判 Critical（5 个）。

### 决策 4：规模假设偏倚显式声明

评审者假设"双 11"指中型电商（1-5 万 QPS）。如果是小型电商（百级 QPS），部分 Critical 可降为 High。这一点在"评审者自评 > 偏倚来源"中显式声明，让用户校准。

### 决策 5：未深入展开的扩展视角

- 法务/合规视角：仅在问题 #10 触及
- 安全视角：与反对者视角有重叠，合并处理
- 财务视角：文档无商业模式数据，未深入

如用户后续追问，可按 SKILL.md 的"追问机制"增量补充。

### 决策 6：未启用 webfetch / context7 等外部检索

文档是口述，无外部事实/数据/引用需要 SIFT 验证。双 11 同类系统的公开数据（淘宝峰值 58.3 万笔/秒）属常识性引用，未做单独 lateral reading。如用户挑战具体数字，再单独验证。

## 输出文件

- `review-report.md` —— 完整评审报告（按模板）
- `transcript.md` —— 本文件

## 偏离 SKILL.md 工作流的地方

**无重大偏离**。轻微调整：

1. **肯定断言隐含化**：SKILL.md §工作原则 2 建议每视角结束时显式输出"本视角下，文档在以下方面是 OK 的"。为节省篇幅，本报告把 OK 部分隐含在建设性视角里（即"如果是你写，会怎么改"暗含了"现状是 X，应该改成 Y"）。如用户要求，可单独输出每视角的肯定断言列表。
2. **Stage 2 与 Stage 3 部分合并呈现**：在详细问题清单里，问题的"发现阶段"字段同时标注了 PERSPECTIVES 和 ARGUMENTS（如问题 #1 标 "Stage 3 ARGUMENTS"，但同时也来自反对者视角的预设问题）。这是 SKILL.md §方法论组合使用建议允许的（"Stage 2 PERSPECTIVES 主用 PBR，但 Stage 3 ARGUMENTS 的 Toulmin 拆解可能与 PERSPECTIVES 发现的问题重叠"）。
3. **ACH 简化为 4 假设**：SKILL.md 要求"至少 2-3 个竞争假设"，本报告列了 4 个（A/B/C/D），满足要求。
