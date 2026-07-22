# 评审报告模板

> 这是 `expert-reviewer` skill 的输出模板。
> 替换 `<>` 包裹的字段；删除不适用的章节并标注"不适用（原因）"。
> 保持表格、blockquote、严重等级标记的格式不变——下游工具按结构解析。

---

# 评审报告：<doc-title 或 一句话主题>

## 元信息

| 字段 | 值 |
|---|---|
| 评审对象类型 | <技术架构 \| 业务产品 \| 报告论文 \| 混合（说明）> |
| 评审日期 | <YYYY-MM-DD> |
| 文档来源 | <本地路径 / URL / 对话粘贴 / 口述> |
| 文档体量 | <N 字 / N 页 / N 段> |
| 评审模式 | 红队 + 建设性 双视角（默认） |
| 评审者 | expert-reviewer skill (v1.0) |

## 总览

### 总体评分

| 维度 | 分数 (0-10) | 一句话说明 |
|---|---|---|
| 论证严谨性 | <分数> | <一句话> |
| 证据充分性 | <分数> | <一句话> |
| 决策质量 | <分数> | <一句话> |
| 视角覆盖 | <分数> | <一句话> |
| 文档质量 | <分数> | <一句话> |
| **综合** | **<加权平均>** | **<一句话结论>** |

**综合评分量表**：
- 0-2 `Critical`：根本性失败，需重写
- 3-5 `Weak`：有结构性问题，需重大修订
- 6-8 `Solid`：方向对但需打磨
- 9-10 `Strong`：可发表/可执行，仅微调

### 一句话结论

> <读完这份文档，评审者最想对作者说的一件事——直接、不绕弯>

### 问题分布

| 严重等级 | 数量 | 占比 |
|---|---|---|
| 🔴 Critical | <N> | <X%> |
| 🟠 High | <N> | <X%> |
| 🟡 Medium | <N> | <X%> |
| 🟢 Low | <N> | <X%> |
| **合计** | **<N>** | **100%** |

---

## 详细问题清单

> 每个问题必须包含 7 个字段：严重等级 / 发现阶段 / 视角 / 原文引用 / 方法论依据 / 🟥 红队视角 / 🟩 建设性视角。
> 三证据齐全（原文 + 方法论 + 严重等级）是绝对约束。

### 问题 #1：<一句话标题，陈述句>

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 3 ARGUMENTS
- **视角**：反对者/竞争对手
- **原文引用**：

  > "<直接引用文档原文>"
  >
  > —— §<章节号> 第 <N> 段（或 文件:行 / XPath / 时间戳）

- **方法论依据**：Toulmin 论证拆解 — 核心提问："这个 Claim 的 Warrant 是否被显式检验？"（出处：`references/methodology-foundations.md` §Toulmin）

- **🟥 红队视角**：

  <如果我是对手/竞争对手/拒稿审稿人/黑客，看到这一段会怎么攻击。具体到"我会引用哪个反例 / 哪个数据 / 哪个论证反例"。>

- **🟩 建设性视角**：

  <如果我是合作者/共同作者/教练，会怎么帮作者改。具体到"加一句什么 / 删一句什么 / 把这段重写成什么样"。>

### 问题 #2：<标题>

（同上结构）

### 问题 #N：...

---

## 结构化发现汇总

### Paul-Elder 8 要素覆盖

| 要素 | 文档是否充分处理 | 缺口说明 |
|---|---|---|
| Purpose 目的 | ✅/⚠️/❌ | <说明> |
| Question at issue 关键问题 | ✅/⚠️/❌ | <说明> |
| Information 信息 | ✅/⚠️/❌ | <说明> |
| Inference 推断 | ✅/⚠️/❌ | <说明> |
| Assumption 假设 | ✅/⚠️/❌ | <说明> |
| Concepts 概念 | ✅/⚠️/❌ | <说明> |
| Implications 含义 | ✅/⚠️/❌ | <说明> |
| Point of view 视角 | ✅/⚠️/❌ | <说明> |

图例：✅ 充分处理 / ⚠️ 部分处理 / ❌ 缺失或薄弱

### 5 视角覆盖

| 视角 | 关键发现 | 最高严重等级 |
|---|---|---|
| 实现者 Implementer | <bullet 列表> | <等级> |
| 维护者 Maintainer | <bullet 列表> | <等级> |
| 用户/客户 User/Customer | <bullet 列表> | <等级> |
| 反对者/竞争对手 Adversary | <bullet 列表> | <等级> |
| 决策者/投资人 Decision-maker | <bullet 列表> | <等级> |

### 核心论证的 Toulmin 拆解

> 选 3-5 个文档中最重要的论证拆解。如果文档少于 3 个论证，按实际数量。

#### 论证 #1：<一句话标题>

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | <文档原文> | ✅/⚠️/❌ <说明> |
| Data 数据 | <文档原文或缺失> | ✅/⚠️/❌ <说明> |
| Warrant 推理依据 | <显式或隐式> | ✅/⚠️/❌ <说明> |
| Backing 支撑 | <显式或缺失> | ✅/⚠️/❌ <说明> |
| Qualifier 限定词 | <"可能/往往/几乎总是"，或缺失> | ✅/⚠️/❌ <说明> |
| Rebuttal 反例 | <文档承认的反例，或缺失> | ✅/⚠️/❌ <说明> |

**Walton critical questions**（按 argumentation scheme 选择）：
- <问题 1 + 文档是否回答>
- <问题 2 + 文档是否回答>

### 关键假设清单（Key Assumptions Check 产出）

| # | 假设 | 显式/隐含 | 概率 | 依据 | 失败退化路径 |
|---|---|---|---|---|---|
| 1 | <假设内容> | 显式/隐含 | 高/中/低 | <来源> | <方案失败时怎么办> |
| 2 | ... | | | | |

### Pre-mortem 产出

> 假设方案已经失败。最可能的失败原因是什么？

| 失败原因 | 概率 | 文档是否已预防 | 改进建议 |
|---|---|---|---|
| <原因 1> | 高/中/低 | ✅/❌ | <建议> |
| <原因 2> | | | |

### ACH（竞争假设分析）

> 仅当文档提出"原因是 X"或"应该选方案 X"时产出。

| 证据 \ 假设 | 假设 A：文档主张 | 假设 B：竞争假设 1 | 假设 C：竞争假设 2 |
|---|---|---|---|
| 证据 1 | 一致/不一致/N/A | 一致/不一致/N/A | 一致/不一致/N/A |
| 证据 2 | | | |
| **诊断性** | <能区分假设吗？> | | |

---

## 评审者自评

### 本份评审**没有覆盖到**的方面

- <方面 1>
- <方面 2>

### 本份评审**存在偏倚**的可能来源

- <偏倚 1，如"评审者偏重实证证据，可能低估纯理论论证的价值">
- <偏倚 2>

### 如果只能改一件事

> <最关键的一条改进建议>

---

## 追问记录

> 用户在初版报告后追问时追加。每次追问一个章节。

### 追问 1：<用户原话或一句话主题>

**用户请求**：<verbatim>

**修订内容**：<增量修订的发现 / 调整 / 加强论证>

**对原报告的影响**：
- 新增问题 #<N>：<标题>
- 修订问题 #<M> 的严重等级：<原 → 新>，原因 <说明>
- 撤销问题 #<K>：原因 <说明>

---

## 附录：评审使用的方法论清单

> 让读者知道这份评审是怎么做出来的，便于复核。

| 方法论 | 出处 references 文件 | 在本报告中使用的位置 |
|---|---|---|
| Paul-Elder 8 elements of thought | `references/methodology-foundations.md` | Stage 1 PARSE |
| Perspective-Based Reading | `references/methodology-foundations.md` | Stage 2 PERSPECTIVES |
| Toulmin argument model | `references/methodology-foundations.md` | Stage 3 ARGUMENTS |
| Walton argumentation schemes | `references/methodology-foundations.md` | Stage 3 ARGUMENTS |
| Pre-mortem (Klein 2007) | `references/bias-checks.md` | Stage 4 DECISIONS |
| Key Assumptions Check (CIA SAT) | `references/bias-checks.md` | Stage 4 DECISIONS |
| Analysis of Competing Hypotheses | `references/bias-checks.md` | Stage 4 DECISIONS |
| SIFT (Caulfield) | `references/source-evaluation.md` | Stage 3 + Stage 5 |
| <对象类型专用方法> | `references/<对象类型>-review.md` | 全程 |
