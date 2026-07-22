# 评审报告：《冥想 App 对程序员工作效率的因果影响：一项随机对照实验》

## 元信息

| 字段 | 值 |
|---|---|
| 评审对象类型 | 报告论文（学术 RCT 摘要） |
| 评审日期 | 2026-07-21 |
| 文档来源 | 对话粘贴（用户口述论文摘要） |
| 文档体量 | 约 150 字，4 个核心要素（设计 / 干预 / 结局 / 统计） |
| 评审模式 | 红队 + 建设性 双视角 |
| 评审者 | expert-reviewer skill (v1.0)，由主会话执行（Claude.ai fallback） |

---

## 总览

### 总体评分

| 维度 | 分数 (0-10) | 一句话说明 |
|---|---:|---|
| 论证严谨性 | 2 | 从"15% 差异 p=0.04"到"因果性提升"的推理桥梁存在多个未检验的 warrant |
| 证据充分性 | 2 | 关键信息缺失：盲法 / power / pre-registration / 多重比较 / 心理测量学 / 数据开放 |
| 决策质量 | 3 | 从一个 8 周个体实验直接推广到"企业应该订阅"的政策建议，跨度太大 |
| 视角覆盖 | 4 | 实验设计视角 OK，但缺统计学家、复现研究者、企业决策者、伦理视角 |
| 文档质量 | 4 | 摘要含必要结构，但缺关键细节（样本来源 / 招募 / 失访 / 分析集） |
| **综合** | **3.0** | **Weak-Critical 边界：投稿会被要求"major revision"，直接发表将引发 methodological critique** |

### 一句话结论

> 这篇论文的核心论证链有两处致命跳跃——从"自评问卷"到"工作效率"，从"统计显著"到"因果性"——任何一个被审稿人深究都足以导致拒稿或撤稿风险。

### 问题分布

| 严重等级 | 数量 | 占比 |
|---|---:|---:|
| 🔴 Critical | 4 | 26.7% |
| 🟠 High | 5 | 33.3% |
| 🟡 Medium | 4 | 26.7% |
| 🟢 Low | 2 | 13.3% |
| **合计** | **15** | **100%** |

---

## 详细问题清单

### 问题 #1：因果声明过强——"自评问卷"不等于"工作效率"

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：反对者/竞争对手（拒稿审稿人）
- **原文引用**：
  > "8 周后用自评问卷测'感知到的生产力'。结果：实验组得分比对照组高 15%（p=0.04），说明冥想 App 因果性地提升了程序员工作效率。"
  >
  > —— 用户摘要第 3-4 句
- **方法论依据**：Toulmin 论证拆解 — Warrant 检查（出处：`references/methodology-foundations.md` §3）。Walton 因果型 argumentation scheme 的 critical question "因果方向是否反了？是否有第三方变量？"（出处：`references/methodology-foundations.md` §4.2）
- **🟥 红队视角**：
  
  拒稿审稿人会立刻识别这里的偷换：测量的是**感知到的生产力**（subjective self-report），结论却用了**工作效率**（objective performance）这个完全不同的构念。这是心理学经典混淆——积极情绪（冥想可能引发）会让受试者**自评更高**，但客观产出（commit 数 / bug 率 / 任务完成时间）可能完全没变。Hawthorne effect + placebo + demand characteristics 三重作用足以解释 15% 的自评差异。**审稿人会写："authors conflate subjective perception with objective outcome; the title and conclusion overclaim."**
  
- **🟩 建设性视角**：
  
  - **标题改写**：把"工作效率"改为"感知到的生产力"（perceived productivity）；或保留"工作效率"但补充客观指标（如代码 commit 数、PR 合并时长、bug 率、Jira 任务完成数）
  - **方法补强**：加一个客观行为数据采集 arm（从 GitHub / Jira / 自建时间追踪工具拉数据），即使 8 周内只能拿到部分样本也比纯自评强
  - **结论限缩**：删除"工作效率"四字，改为"自我感知的生产力"

### 问题 #2：盲法缺失——对照组知道自己"不被治疗"

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 4 DECISIONS
- **视角**：反对者/竞争对手（拒稿审稿人）
- **原文引用**：
  > "实验组用我们的冥想 App 8 周，对照组不用。"
  >
  > —— 用户摘要第 2 句
- **方法论依据**：Cochrane RoB 2 领域 2"偏离既定干预"（出处：`references/paper-academic-review.md` §4）。CASP RCT checklist（出处：同上 §3）。
- **🟥 红队视角**：
  
  没有 active control（如 relaxation audio / sham meditation），对照组完全知道自己"不被治疗"。这会触发 **resentful demoralization**（对照组觉得"被忽视"→ 自评更低）和 **placebo effect in treatment group**（实验组觉得"我在做正经事"→ 自评更高）。两个效应叠加可以**单独解释 15% 差异**，干预本身的因果作用根本无法分离。**这是 Cochrane RoB 评级为 High risk 的直接原因。**
  
- **🟩 建设性视角**：
  
  - **方案 A（理想）**：用 active placebo control，如让对照组每天听 15 分钟"中性白噪音/放松音频"，让两组都"做点什么"
  - **方案 B（务实）**：在 analysis 阶段控制 demand characteristics，至少在干预前后测**预期效应**（"你觉得冥想会有效吗？"），把高期望被试单独分析
  - **方案 C（最低要求）**：在 limitations 章节真诚承认这是单盲设计的核心限制，而不是默认读者不会发现

### 问题 #3：pre-registration 缺失 + p=0.04 边缘显著 → HARKing 高度可疑

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 4 DECISIONS
- **视角**：反对者/竞争对手（拒稿审稿人 / 复现研究者）
- **原文引用**：
  > "结果：实验组得分比对照组高 15%（p=0.04），说明冥想 App 因果性地提升了程序员工作效率。"
  >
  > —— 用户摘要第 4 句
- **方法论依据**：Replication Crisis Reforms（出处：`references/paper-academic-review.md` §7）。Walton 统计显著性型 argumentation scheme（出处：`references/methodology-foundations.md` §4.4）
- **🟥 红队视角**：
  
  - **p=0.04 是"边缘显著"**——任何样本量或分析选择的微小变化都可能让 p 跳过 0.05。在没有 pre-registration 的情况下，读者**无法排除**作者事后选择最有利的分析（HARKing：Hypothesizing After Results are Known）。
  - **多重比较风险极高**：摘要没说测了几个结局变量。如果测了"生产力、压力、专注、睡眠、情绪、满意度"6 个变量，按 Bonferroni 校正后 α 应为 0.0083，p=0.04 远未显著。**没有声明 = 默认有此风险。**
  - **复现危机后**：心理学顶刊（Psychological Science / Nature Human Behaviour）现在要求 pre-registration 或至少 open data，否则直接 desk reject。
  
- **🟩 建设性视角**：
  
  - **立即可改**：在 OSF（Open Science Framework）或 AsPredicted 上 retroactively pre-register 当前分析，公开数据 + 代码
  - **报告效应量 + 95% CI**：不要只报 p 值。例如"d = 0.4 [0.05, 0.75]"比"p = 0.04"信息量大得多
  - **报告所有测量的结局**：在补充材料里列出所有测过的变量 + 是否显著，让读者自己判断多重比较风险
  - **预注册**：未来研究在数据收集前预注册 hypothesis + analysis plan

### 问题 #4：样本量 100 是否经过 power analysis？

- **严重等级**：🟠 High
- **发现阶段**：Stage 4 DECISIONS
- **视角**：决策者/投资人（此处=研究资助方 / 期刊编辑）
- **原文引用**：
  > "我们招募了 100 名程序员"
  >
  > —— 用户摘要第 1 句
- **方法论依据**：CASP RCT checklist "样本量是否足够？"（出处：`references/paper-academic-review.md` §3）。Replication Crisis power analysis 检查项。
- **🟥 红队视角**：
  
  摘要没说 100 这个数怎么来的。如果没有事先 power analysis，100 只是"随便选的整数"。如果预期效应量 d=0.4（小到中等），要达到 80% power 在 α=0.05 下需要约 200 人/组 = 400 人总数。100 人（50/50）只能可靠检测 d ≥ 0.57 的效应。**"15% 差异 p=0.04"可能正是 underpowered + 偶然波动的产物。**
  
- **🟩 建设性视角**：
  
  - 用 G*Power 或 R `pwr.t.test` 跑事后 power analysis，报告"如果效应量真是 X，本研究有 Y% power"
  - 在 limitations 承认 underpowered 风险
  - 未来研究：基于本次效应量做正式 power analysis 再扩样

### 问题 #5：开放数据/代码缺失——复现性差

- **严重等级**：🟠 High
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：维护者（此处=学术社区 / 复现研究者）
- **原文引用**：摘要全文未提及数据/代码可用性
- **方法论依据**：Replication Crisis Reforms 的"Open Data / Open Code"检查项（出处：`references/paper-academic-review.md` §7）
- **🟥 红队视角**：
  
  没有数据/代码公开，独立研究者无法：(a) 验证统计计算；(b) 重新分析检查 robustness；(c) 加入 meta-analysis。复现危机后，这是 publication 的基本要求。不公开 = 默认有问题。
  
- **🟩 建设性视角**：
  
  - 数据脱敏后上传 OSF / Zenodo / GitHub
  - 分析代码上传 GitHub（R Markdown / Jupyter notebook）
  - 实验材料（问卷条目 / 冥想 App 内容）公开
  - 在论文末尾加 "Data and code availability" 段落

### 问题 #6：8 周随访期过短——长期效应未知

- **严重等级**：🟠 High
- **发现阶段**：Stage 4 DECISIONS
- **视角**：决策者/投资人（企业 HR 决策者）
- **原文引用**：
  > "实验组用我们的冥想 App 8 周"
  >
  > —— 用户摘要第 2 句
- **方法论依据**：Pre-mortem（出处：`references/bias-checks.md` §1）— 假设方案失败，最可能原因之一是"短期效应不能持续"
- **🟥 红队视角**：
  
  冥想类干预有**著名的 novelty effect**——前几周因为新鲜感效应显著，之后逐渐衰减。心理学文献中冥想干预的 6 个月 follow-up 大多看不到持续效应。8 周结论**无法支持"企业应该订阅"**这种长期政策建议——企业花钱订阅期望的是 12+ 个月的持续生产力提升，不是 8 周新鲜感。
  
- **🟩 建设性视角**：
  
  - 加 3 个月 / 6 个月 follow-up 测量
  - 报告 adherence（实际使用频率），区分"持续使用者" vs "放弃者"亚组效应
  - 修改结论为"短期内显著，长期效应需要进一步研究"

### 问题 #7：自评问卷的心理测量学属性未报告

- **严重等级**：🟠 High
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：实现者（此处=研究方法学家）
- **原文引用**：
  > "用自评问卷测'感知到的生产力'"
  >
  > —— 用户摘要第 3 句
- **方法论依据**：CASP RCT checklist "结局测量是否可靠？"（出处：`references/paper-academic-review.md` §3）
- **🟥 红队视角**：
  
  没说用了什么问卷。如果是已发表的量表（如 WWB / BBQ），应报告 Cronbach α、test-retest reliability、construct validity。如果是自编问卷，**未经验证的工具测出来的"显著差异"没有任何意义**——可能是测量误差的系统性偏差。
  
- **🟩 建设性视角**：
  
  - 报告问卷的来源、条目数、内部一致性（α 系数）
  - 如果是自编，做 pilot study 验证 psychometric properties
  - 至少在补充材料附完整问卷

### 问题 #8：从"个体实验"到"企业政策"的过度推广

- **严重等级**：🟠 High
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：决策者/投资人（企业决策者 / 政策制定者）
- **原文引用**：
  > "结论：企业应该为员工提供冥想 App 订阅。"
  >
  > —— 用户摘要末句
- **方法论依据**：GRADE Indirectness（出处：`references/paper-academic-review.md` §2）— PICO 的 P（population）和 setting 是否匹配。Walton 推广型 argumentation scheme。
- **🟥 红队视角**：
  
  从"100 名自愿报名的程序员在实验环境下用 8 周"推广到"所有企业应该订阅"，跨越了至少 4 个外部效度边界：
  1. **selection bias**：自愿报名者本就更有冥想倾向，结果不能推广到非自愿员工
  2. **setting**：实验环境 vs 真实工作压力下的依从性差异
  3. **outcome**：自评 vs 真实绩效
  4. **time horizon**：8 周 vs 企业年度决策
  
  **审稿人会写："the policy recommendation is not warranted by a single short-term RCT with self-selected participants."**
  
- **🟩 建设性视角**：
  
  - 删除"企业应该"政策建议
  - 改为"在自评生产力维度上观察到短期显著差异；推广到企业政策需要 cluster-randomized trial + 长期 follow-up + 客观绩效指标"
  - 或加一个 implementation study arm：在企业真实环境跑 6 个月 pilot

### 问题 #9：分配隐藏（allocation concealment）未报告

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 4 DECISIONS
- **视角**：实现者（研究方法学家）
- **原文引用**：摘要只说"随机分两组"，未说分配隐藏机制
- **方法论依据**：Cochrane RoB 2 领域 1"随机化过程"（出处：`references/paper-academic-review.md` §4）
- **🟥 红队视角**：
  
  "随机"不等于"分配隐藏"。如果招募者知道下一个分组（如用透明信封 / 简单交替），可以系统性把"更可能有效的"受试者分到实验组。这是 selection bias 的常见来源。
  
- **🟩 建设性视角**：
  
  - 报告随机化方法（computer-generated / stratified / block）
  - 报告分配隐藏机制（central allocation / sealed opaque envelopes）
  - 在方法学补充材料附 CONSORT flow diagram

### 问题 #10：失访率 / ITT 分析未报告

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 4 DECISIONS
- **视角**：实现者
- **原文引用**：摘要未报告失访
- **方法论依据**：Cochrane RoB 2 领域 3"缺失结局数据"（出处：`references/paper-academic-review.md` §4）
- **🟥 红队视角**：
  
  冥想类干预的失访率通常 20-40%（人们坚持不下去）。如果失访非随机（实验组里"觉得没用"的人退出更多），只分析完成者（per-protocol）会高估效应。ITT（intention-to-treat）分析是 RCT 的金标准。
  
- **🟩 建设性视角**：
  
  - 报告失访率 + 失访原因
  - 同时报 ITT 和 per-protocol 分析
  - 用 multiple imputation 处理缺失数据

### 问题 #11：基线特征平衡未报告

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：实现者
- **原文引用**：摘要未报告两组基线特征
- **方法论依据**：CASP RCT checklist "两组在基线是否相似？"（出处：`references/paper-academic-review.md` §3）
- **🟥 红队视角**：
  
  如果实验组基线就比对照组更"正念倾向 / 更乐观 / 更健康"，后测差异可能不是干预造成的。Table 1（baseline characteristics）是 RCT 标准要求。
  
- **🟩 建设性视角**：
  
  - 加 Table 1 报告基线特征（年龄 / 性别 / 工龄 / 基线量表分数）
  - 如有不平衡，在 analysis 中作为 covariate

### 问题 #12：受试者招募渠道未报告

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：用户/客户（此处=外部效度评估者）
- **原文引用**：
  > "我们招募了 100 名程序员"
  >
  > —— 用户摘要第 1 句
- **方法论依据**：GRADE Indirectness — Population 直接性评估（出处：`references/paper-academic-review.md` §2）
- **🟥 红队视角**：
  
  通过冥想兴趣社群招募的样本 ≠ 真实企业员工总体。如果是"在网上发广告招募对冥想感兴趣的程序员"，外部效度极有限。
  
- **🟩 建设性视角**：
  
  - 报告招募渠道（社交媒体 / 公司内推 / 患者注册库等）
  - 报告筛选 / 排除标准
  - 在 limitations 承认 selection bias

### 问题 #13：效应量 + 95% CI 未报告

- **严重等级**：🟢 Low
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：实现者
- **原文引用**：
  > "实验组得分比对照组高 15%（p=0.04）"
  >
  > —— 用户摘要第 4 句
- **方法论依据**：Walton 统计型 argumentation scheme（出处：`references/methodology-foundations.md` §4.4）
- **🟥 红队视角**：
  
  "15% 差异"在不知道基线均值和标准差的情况下没意义。如果基线均值是 100，差异 15 分，但 SD 也是 15，那 d=1.0（大效应）。如果 SD=30，那 d=0.5（中等效应）。p=0.04 + n=100 通常意味着 d ≈ 0.4（中等偏小）。
  
- **🟩 建设性视角**：
  
  报告 Cohen's d + 95% CI，让读者自己判断效应的临床/实际意义。

### 问题 #14：CONSORT 流程图缺失

- **严重等级**：🟢 Low
- **发现阶段**：Stage 5 REPORT
- **视角**：实现者
- **原文引用**：摘要未附流程图
- **方法论依据**：PRISMA（同源）+ CONSORT（针对 RCT）的报告完整性要求（出处：`references/paper-academic-review.md` §1）
- **🟥 红队视角**：
  
  没有 CONSORT flow diagram，读者无法追踪：招募了多少 → 筛选排除多少 → 随机分配多少 → 失访多少 → 最终分析多少。这是 RCT 投稿的最低要求。
  
- **🟩 建设性视角**：
  
  在 Figure 1 附标准 CONSORT flow diagram。

### 问题 #15：利益冲突未声明

- **严重等级**：🟢 Low
- **发现阶段**：Stage 5 REPORT
- **视角**：反对者/竞争对手
- **原文引用**：摘要未声明利益冲突
- **方法论依据**：ICFN 自检（出处：`references/source-evaluation.md` §5）+ 期刊投稿标准
- **🟥 红队视角**：
  
  如果作者与冥想 App 厂商有利益关系（持股 / 受资助 / 是开发者），结果可信度大幅降低。摘要里没看到声明 = 红旗。
  
- **🟩 建设性视角**：
  
  在论文末尾加 "Conflict of Interest" 声明段，明示所有潜在利益关系。

---

## 结构化发现汇总

### Paul-Elder 8 要素覆盖

| 要素 | 文档是否充分处理 | 缺口说明 |
|---|---|---|
| Purpose 目的 | ✅ | 目的清晰：测冥想 App 对生产力的影响 |
| Question at issue 关键问题 | ⚠️ | 问题表述混淆了"感知生产力" vs "工作效率" |
| Information 信息 | ❌ | 缺失：失访、基线、招募、psychometric 属性 |
| Inference 推断 | ❌ | 从自评差异到"工作效率因果性提升"推理不合规 |
| Assumption 假设 | ❌ | 隐含假设"自评=客观"未检验 |
| Concepts 概念 | ⚠️ | "生产力"概念使用前后不一致 |
| Implications 含义 | ❌ | 未考虑过度推广的伦理后果 |
| Point of view 视角 | ⚠️ | 缺统计学家 / 复现研究者 / 政策视角 |

### 5 视角覆盖

| 视角 | 关键发现 | 最高严重等级 |
|---|---|---|
| 实现者（方法学家） | 心理测量学 / 分配隐藏 / 失访 / 基线平衡 / 效应量 / CONSORT 均缺 | 🔴 Critical（问题 #2、#7） |
| 维护者（学术社区） | 数据/代码不公开，无法复现 | 🟠 High（问题 #5） |
| 用户/客户（外部效度） | 招募渠道未说，selection bias 限制推广 | 🟡 Medium（问题 #12） |
| 反对者/竞争对手（审稿人） | 因果声明过强 / 盲法缺失 / HARKing 风险 / 过度推广 | 🔴 Critical（问题 #1、#2、#3、#8） |
| 决策者/投资人（编辑 / 企业） | underpowered / 8 周随访不足 / 政策建议过强 | 🟠 High（问题 #4、#6、#8） |

### 核心论证的 Toulmin 拆解

#### 论证 #1："冥想 App 因果性地提升了程序员工作效率"

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | 冥想 App 因果性提升程序员工作效率 | ❌ Claim 过强，与测量不匹配 |
| Data 数据 | 实验组 vs 对照组自评得分差异 15%，p=0.04 | ⚠️ 数据存在但分析不充分 |
| Warrant 推理依据 | "组间差异 = 干预的因果效应"（隐含） | ❌ Warrant 在缺盲法 + 缺分配隐藏时不成立 |
| Backing 支撑 | 缺失 | ❌ 没有任何 backing |
| Qualifier 限定词 | 缺失（用了绝对词"因果性地"） | ❌ 应该用"在自评维度上观察到短期差异" |
| Rebuttal 反例 | 完全缺失（未承认 placebo / Hawthorne / novelty effect） | ❌ |

**Walton critical questions**（因果型 scheme）：
- 相关性 ≠ 因果性：✅ 文档未答 — 自评差异可能由 placebo 解释
- 第三方变量：✅ 文档未答 — 实验组可能基线就更乐观
- 因果方向：✅ 文档未答 — 也可能"更乐观的人更愿意完成冥想"

### Cochrane RoB 2 五领域评估

| 领域 | 评级 | 理由 |
|---|---|---|
| 1. 随机化过程 | ⚠️ Some concerns | 随机化方法未报告，分配隐藏未报告 |
| 2. 偏离既定干预 | 🔴 High | 无盲法，对照组知道自己不被治疗 |
| 3. 缺失结局数据 | ⚠️ Some concerns | 失访率未报告，ITT 分析未报告 |
| 4. 结局测量 | 🔴 High | 自评问卷 + 无盲法 = 测量偏倚高 |
| 5. 结果选择 | ⚠️ Some concerns | 无 pre-registration，多重比较未声明 |

**综合 RoB 评级：High Risk of Bias** — 不能作为"高确定性证据"使用。

### Pre-mortem 产出

假设 12 个月后这篇论文被撤稿或被复现失败研究挑战。最可能的原因：

| 失败原因 | 概率 | 文档是否预防 |
|---|---|---|
| 复现实验失败（效应不复现） | 高 | ❌ |
| 暴露未声明利益冲突 | 中 | ❌ |
| 数据分析暴露 HARKing | 中 | ❌ |
| 长期 follow-up 显示效应消失 | 高 | ❌ |
| Meta-analysis 把本研究降级为 low quality | 高 | ❌ |

### Key Assumptions Check 关键假设清单

| # | 假设 | 显式/隐含 | 概率 | 失败退化路径 |
|---|---|---|---|---|
| 1 | "感知生产力" = "工作效率" | 隐含 | 低 | 整篇结论作废 |
| 2 | 自评无系统性偏倚 | 隐含 | 低（已知 placebo / Hawthorne） | 效应量被高估 |
| 3 | 样本 100 足够 | 隐含 | 中（取决于真实效应量） | underpowered，结论不稳定 |
| 4 | 8 周效应可推广到长期 | 隐含 | 低（novelty effect 已知） | 政策建议失效 |
| 5 | 实验室环境 = 真实工作环境 | 隐含 | 中 | 外部效度有限 |
| 6 | 冥想 App 是"治疗"而非"放松工具" | 隐含 | 中 | 适用范围错位 |

---

## 评审者自评

### 本份评审**没有覆盖到**的方面

- **干预内容**：冥想 App 的具体设计（内容 / 时长 / 引导方式）未评估
- **理论框架**：未评估作者是否引用了冥想 / 正念的心理学理论基础
- **比较标准**：未与同类冥想干预 RCT（如 Headspace / Calm 的发表研究）做横向对比
- **质性数据**：未考虑是否应该加质性访谈补充量化结果
- **统计具体计算**：未独立重算 p 值（无原始数据）

### 本份评审**存在偏倚**的可能来源

- **方法论偏重**：评审者倾向严格 methodological critique，可能低估"探索性研究"的早期价值
- **复现危机敏感性**：评审者对心理学 RCT 持较高怀疑阈值，可能比常规审稿人更严
- **企业政策视角**：评审者对企业应用场景持保守态度，可能高估"过度推广"风险

### 如果只能改一件事

> 把标题和结论里的"工作效率"全部改为"自我感知的生产力"，并在 limitations 显式承认：(a) 单盲设计 placebo 风险；(b) 8 周短期不能推广到长期；(c) 自选样本不能推广到企业员工总体。仅这一项修改就能避免最严重的拒稿风险。

---

## 附录：评审使用的方法论清单

| 方法论 | 出处 references 文件 | 在本报告中使用的位置 |
|---|---|---|
| Paul-Elder 8 elements of thought | `references/methodology-foundations.md` | Stage 1 PARSE；8 要素覆盖 |
| Perspective-Based Reading | `references/methodology-foundations.md` | Stage 2 PERSPECTIVES；5 视角覆盖 |
| Toulmin argument model | `references/methodology-foundations.md` | Stage 3 ARGUMENTS；论证 #1 拆解 |
| Walton argumentation schemes | `references/methodology-foundations.md` | Stage 3 ARGUMENTS；因果型 + 统计型 critical questions |
| Pre-mortem (Klein 2007) | `references/bias-checks.md` | Stage 4 DECISIONS；Pre-mortem 产出 |
| Key Assumptions Check (CIA SAT) | `references/bias-checks.md` | Stage 4 DECISIONS；关键假设清单 |
| CASP RCT checklist | `references/paper-academic-review.md` | 多处；问题 #2、#4、#7、#11 |
| Cochrane RoB 2 | `references/paper-academic-review.md` | 5 领域评估 |
| GRADE Indirectness | `references/paper-academic-review.md` | 问题 #8、#12 |
| Replication Crisis Reforms | `references/paper-academic-review.md` | 问题 #3、#5 |
| SIFT / IFCN 自检 | `references/source-evaluation.md` | 问题 #15 利益冲突 |
