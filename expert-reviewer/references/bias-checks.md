# 偏倚检查方法

> Stage 4 DECISIONS 时加载（文档含决策/推荐时）。核心：结构性对抗认知偏倚需要工具化。

## 1. Pre-mortem 前置尸检

出处：Klein, HBR 2007（详见 `methodology-foundations.md` §5）。假设方案**已失败**，反向归因。列 5-8 个最可能失败原因 → 检查预防 → 未预防 = Critical/High。

## 2. Key Assumptions Check 关键假设检查

出处：[CIA Tradecraft Primer](https://www.cia.gov/resources/ci/)；Heuer, *Psychology of Intelligence Analysis*。

核心：显式化所有**关键假设**（尤其**隐含**的）。对每个假设填表：

| 假设 | 显式/隐含 | 概率（高/中/低） | 依据 | 失败退化路径 |

重点挑战：隐含假设 / 概率中等的 / 失败退化路径缺失的。

典型隐含假设：市场持续增长 / 用户按预期使用 / 核心依赖持续维护 / 监管不变 / 竞争对手不反击 / 关键人留下 / 宏观经济稳定。

## 3. Analysis of Competing Hypotheses (ACH)

出处：Heuer, *Psychology of Intelligence Analysis*；CIA Tradecraft Primer。

核心：人类倾向**满意即可**（找到第一个看似合理假设就停）。ACH 强制**同时考虑所有合理假设**，找**诊断性证据**（能区分假设的），而非**支持性证据**（与某假设一致的）。

操作：
1. 识别文档核心主张（假设 A）
2. 构造 2-3 个**竞争假设**（B、C）
3. 列所有证据 → 对每条问"与哪个假设一致？"
4. 找**诊断性证据**（A 一致但 B/C 不一致的）
5. 文档只有"全一致"证据 = 脆弱（无法证伪其他假设）→ High

## 4. Devil's Advocacy 魔鬼倡导者

出处：CIA Tradecraft Primer。

核心：**真诚地**尝试论证**相反结论**。在什么条件下相反结论才对？文档忽略了哪些支持相反结论的证据？文档论证是否在相反结论下也能成立（如是则论证无诊断性）？

与 Red Team 区别：Devil's Advocacy 聚焦**结论本身**的反驳；Red Team 模拟**真实对手**的攻击（含动机/资源/手段）。

## 5. Red Team Analysis 红队分析

出处：CIA Tradecraft Primer；[Wikipedia Red Team](https://en.wikipedia.org/wiki/Red_team)。

核心：模拟**真实对手**（竞争对手/黑客/监管者/攻击者），从对手视角攻击方案。

操作：识别对手类型 → 问对手的**动机/资源/攻击路径** → 检查文档预防 → 未预防 = High/Critical。

业务版 Red Team 5 角色详见 `business-product-review.md` §5。

## 6. What If Analysis 反事实推演

出处：CIA Tradecraft Primer。

核心：构造**反事实场景**（"如果用户数比预期高 10 倍？""如果核心依赖停服 30 天？""如果竞争对手今天发布免费版？"）。和 Pre-mortem 互补——Pre-mortem 假设失败归因，What If 假设条件变化。

## 7. High Impact / Low Probability 高影响低概率

出处：CIA Tradecraft Primer。

核心：人类倾向**低估小概率高影响事件**。主动找这类事件：概率 < 5% 但 > 0.1% + 影响 Critical + 预防成本低 → 即使概率小也形成问题。

典型：核心供应商破产 / 关键团队集体离职 / 监管一夜变更 / 黑客 0day / 自然灾害 / 地缘政治 / 疫情。

## 8. Outside-In Thinking 外部视角思考

出处：CIA Tradecraft Primer；与 Kahneman 的 **Reference Class Forecasting** 高度相关（见 `business-product-review.md` §4）。

核心：人类倾向**内部视角**（"我们的特殊情况"）。**外部视角**（"同类项目的统计规律"）更准。找到文档的量化预测 → 问**外部 reference class** 是什么 → 预测显著高于 reference class 中位数 → 文档是否解释为什么这次特殊？

## 9. Noise Decision Hygiene 决策卫生

出处：Kahneman, Sibony, Sunstein, *Noise: A Flaw in Human Judgment*, 2021。

核心：评审者间存在**随机变异性**（noise）——同一文档不同评审者结论不同。Decision hygiene 清单：
1. **独立判断**：与其他评审者讨论前先独立形成结论
2. **延迟直觉**：先做事实判断，再做整体判断（避免锚定）
3. **相对判断**：先判断"这个比那个好/差"，再做绝对评分
4. **汇总独立判断**：用聚合（平均）而非讨论达成共识
5. **偏好事实判断**：分解为可验证子判断再综合

对 expert-reviewer 的启示：报告末尾"评审者自评"= decision hygiene 一部分；5 视角不交叉影响 = decision hygiene 实现。

## 10. Confirmation Bias Counters 确认偏倚对抗

出处：[Wikipedia Confirmation Bias](https://en.wikipedia.org/wiki/Confirmation_bias)；Nickerson 1998。

核心：人类倾向**寻找/解释/记忆支持已有观点的证据**。评审者也不例外。

对抗：**主动找 3 个反例** / **Steelman 对手观点**（最强版本复述再攻击）/ **Red Team 自己** / **预注册评审维度**（读完文档前定维度）/ **盲审**（遮蔽作者/单位）。

评审者自检：是否在**选择性引用**原文？**过度解读**模糊表述？**忽视**与预期相反的证据？

## 偏倚检查清单

| # | 检查 | 方法 |
|---|---|---|
| 1 | 假设方案失败，最可能原因？ | Pre-mortem |
| 2 | 所有关键假设是否显式？ | Key Assumptions Check |
| 3 | 是否有竞争假设？证据有诊断性？ | ACH |
| 4 | 文档结论的相反结论是否成立？ | Devil's Advocacy |
| 5 | 真实对手最可能的攻击路径？ | Red Team |
| 6 | 反事实场景下的表现？ | What If |
| 7 | 小概率高影响事件？ | High Impact / Low Probability |
| 8 | 预测是否经外部视角校准？ | Outside-In / RCF |
| 9 | 评审者自身是否有 noise？ | Decision Hygiene |
| 10 | 是否选择性引用证据？ | Confirmation Bias Counters |
