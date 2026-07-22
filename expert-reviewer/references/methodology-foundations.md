# 通用层方法论

> 始终加载。核心洞见：50 年评审方法学共识 = **视角化提问优于开放挑刺**。

## 1. Paul-Elder 8 Elements of Thought

出处：Paul & Elder, *The Miniature Guide to Critical Thinking*。任何文档可拆为 8 思维要素：

| 要素 | 评审提问 |
|---|---|
| Purpose 目的 | 目的清晰？有隐藏目的？ |
| Question 关键问题 | 核心问题被显式提出？ |
| Information 信息 | 信息可靠？缺哪些？ |
| Inference 推断 | 推理合规（演绎/归纳/溯因）？ |
| Assumption 假设 | **隐含假设**有哪些？关键路径上的？ |
| Concepts 概念 | 定义一致？被滥用？ |
| Implications 含义 | 二阶/三阶效应考虑了？ |
| Point of view 视角 | 缺哪些视角？ |

9 知识标准：Clarity / Accuracy / Precision / Relevance / Depth / Breadth / Logic / Significance / Fairness。

局限：描述性框架（告诉问什么，不告诉怎么问）——结合 Toulmin/Walton 用。

## 2. Perspective-Based Reading (PBR)

出处：Basili et al., *Empirical Software Engineering* 1996。NASA/Bosch 控制实验验证。

核心：让多个评审者**各自从不同 stakeholder 视角**阅读，每视角用预设问题集，**不交叉影响**（Parnas Active Design Reviews 约束）。每视角结束时先输出**肯定断言**（"在以下方面 OK"），再列问题。

为什么优于开放挑刺：专注单一维度 / 避免盲区 / 肯定断言比否定挑刺更严肃 / 多视角交叉发现盲区。

5 默认视角问题集见 `assets/templates/perspective-questions.md`。

## 3. Toulmin Argument Model

出处：Toulmin, *The Uses of Argument*, Cambridge UP 1958。任何论证可拆 6 要素：

| 要素 | 评审提问 |
|---|---|
| Claim 结论 | 清晰？可证伪？被充分支持？ |
| Data 数据 | 来源可靠？样本有偏？cherry-picked？ |
| Warrant 推理依据 | 从 data 到 claim 的推理是什么？**被显式检验过**？ |
| Backing 支撑 | 理论/先例/常识？可靠？ |
| Qualifier 限定词 | 有合理限定（可能/往往）？还是过度绝对？ |
| Rebuttal 反例 | 承认反例？有效反驳？还是忽略？ |

典型失败：Warrant 被默认 / Backing 缺失 / Qualifier 过度绝对 / Rebuttal 被忽略 / Claim 含糊不可证伪。

## 4. Walton Argumentation Schemes

出处：Walton, Reed, Macagno, *Argumentation Schemes*, Cambridge UP 2008。60+ 论证型式，每种有 matching critical questions。评审最常用 10 种：

| Scheme | 关键 critical questions |
|---|---|
| 专家意见型 | 真的是该领域专家？利益冲突？其他专家同意？原话准确？ |
| 因果型 | 相关还是因果？第三方变量？方向反了？Bradford Hill 标准？ |
| 类比型 | 关键属性真相似？重要不相似被忽略？反向类比成立？ |
| 统计型 | 样本有偏？基线率？效应量 vs 统计显著？p-hacking？ |
| 成本-收益型 | 隐性成本（机会/维护/退出）？负面收益？时间分布？最坏情况？ |
| 流行型 | "很多人"具体多少？独立判断还是从众？是目标用户？持续还是趋势？ |
| 后果型 | 后果概率？严重程度？反事实？滑坡谬误？ |
| 承诺型 | 相同语境？新信息让承诺失效？scope 被扩大？ |
| 实践型 | A 真能达成 G？副作用？更好的 B？G 本身值得？ |
| 道德型 | 谁的价值观？一致还是双标？更高阶价值观被忽略？ |

## 5. Pre-mortem

出处：Gary Klein, *Performing a Project Premortem*, HBR 2007。

核心：假设方案**已经失败**。反向归因——最可能的失败原因是什么？克服事后归因偏倚和乐观偏差。

操作：列出 5-8 个最可能失败原因（按概率排序）→ 检查文档是否已预防 → 未预防 = Critical/High。

典型失败原因：资源不足 / 依赖失败 / 市场变化 / 执行失败 / 技术失败 / 对手反击 / 黑天鹅。

与风险评估区别：Pre-mortem 是"未来已确定失败"视角，不是"评估各种概率"——视角切换更有效。

## 6. Diátaxis 文档分类学

出处：[Procida, Diátaxis](https://diataxis.fr/)。技术文档分 4 类：

| 类别 | 目的 | 写作规范 |
|---|---|---|
| Tutorials 教程 | 学习（让读者会做） | 任务驱动、step-by-step、最小例子 |
| How-to guides 操作指南 | 完成具体任务 | 目标驱动、步骤明确、覆盖变体 |
| Reference 参考 | 查询信息 | 描述性、结构化、不引导、不解释 |
| Explanation 解释 | 理解（深化认知） | 论辩性、提供视角、讨论 trade-off |

评审：先判断文档应属哪类 → 对照写作规范 → 类别错位（如 tutorial 写成 reference）= Medium/High。

## 方法论 × 评审阶段

| 阶段 | 主用 | 辅助 |
|---|---|---|
| Stage 1 PARSE | Paul-Elder | Diátaxis |
| Stage 2 PERSPECTIVES | PBR（5 视角） | — |
| Stage 3 ARGUMENTS | Toulmin | Walton critical questions |
| Stage 4 DECISIONS | Pre-mortem | CIA SAT（见 bias-checks.md） |
| Stage 5 REPORT | — | Diátaxis（文档质量） |
