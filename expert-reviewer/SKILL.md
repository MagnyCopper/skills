---
name: expert-reviewer
description: "对一份文档（技术/架构设计、业务/产品方案、报告/论文）执行结构化专家评审，同时给出红队挑刺视角与建设性改进建议。当用户说'帮我评审这份文档'、'看看这个设计有没有问题'、'审一下这份方案'、'挑挑刺'、'找找漏洞'、'review 这份 PRD'、'这份报告站得住脚吗'、'这个商业计划有什么问题'、'红队这份设计'、'adversarial review'、'critique this'、'tear this apart'、'find holes in'、'stress-test this proposal' 时使用本技能。也适用于用户没有显式说'评审'但明显希望被批判性审视一份材料的场景，例如'你觉得这个方案靠谱吗'、'我老板发给我这个设计，你觉得怎么样'、'帮我看看这个 PRD 有没有遗漏'。"
---

# Expert Reviewer

对一份文档执行**结构化专家评审**，每个发现的问题同时给出**红队挑刺视角**（如果这个文档被对手攻击，弱点在哪）与**建设性改进建议**（如果是你写，会怎么改）。

## 为什么是"视角化提问"而不是"开放地找问题"

50 年的评审方法学演化（Fagan Inspection → Parnas Active Design Reviews → Perspective-Based Reading → ATAM → CIA Structured Analytic Techniques）共同指向同一个结论：**开放地"读文档找问题"效果很差**。专业评审者不会这样工作。

专家评审者实际做的事是：**轮流从不同 stakeholder 的视角出发，提预先设计的高质量问题**。本技能的核心就是把这件事结构化。

具体证据见 `references/methodology-foundations.md` 与 `references/bias-checks.md`。

---

## Do Not Use This Skill

- 用户只是要求**简单总结**或**翻译**一份文档 → 用普通工具即可
- 用户要的是**事实核查**（一个具体 claim 是否为真） → 走 fact-checking 流程，不是评审
- 用户要的是**改写、优化、重写**一份文档 → 是写作类任务，不是评审
- 用户要的是**逐行代码审查**找 bug → 用 code review 类工具
- 用户明确说"只要夸夸它" / "只要正反馈" → 不属于评审场景

---

## 工作流（5 阶段，一次贯通）

```
PARSE → PERSPECTIVES → ARGUMENTS → DECISIONS → REPORT
```

### Stage 1 — PARSE（解析与归一化）

1. **接收输入**：支持 4 种形式
   - 本地文件路径（`.md` / `.docx` / `.pdf` / `.txt` / 其他可读文本）
   - URL（抓取后转纯文本，长文档只取与评审最相关的前 N 段）
   - 对话里粘贴的长文本
   - 仅口述、无文档（用户用自然语言描述一个 idea / 决策 / 商业计划）

2. **自动检测对象类型**（用于后续路由到专用 references）：
   - **技术/架构设计**：出现架构图、接口定义、数据流、系统设计、技术选型、模块划分
   - **业务/产品方案**：出现市场、客户、收入、竞争、PMF、用户画像、商业模式、ROI
   - **报告/论文**：出现摘要、引言、方法、结果、结论、参考文献、统计检验、实验

   检测不确定时**默认走"报告/论文"路径**（最通用），并在报告开头声明检测依据，让用户能一句"不是，这是 X"覆盖。

3. **Paul-Elder 8 要素拆解**（把文档结构显式化）：

   | 要素 | 自问 |
   |---|---|
   | Purpose 目的 | 这份文档想达成什么？目的是否清晰？ |
   | Question at issue 关键问题 | 文档试图回答的核心问题是什么？ |
   | Information 信息 | 用了哪些信息/数据？还缺哪些？ |
   | Inference 推断 | 从信息到结论的推理链条是什么？ |
   | Assumption 假设 | 哪些是显式假设？哪些是隐含假设？ |
   | Concepts 概念 | 使用了哪些核心概念？定义是否一致？ |
   | Implications 含义 | 结论若成立，会带来什么后果？ |
   | Point of view 视角 | 作者从什么视角写作？还缺哪些视角？ |

### Stage 2 — PERSPECTIVES（视角化提问）

默认扮演 **5 个 stakeholder 视角**，每个视角预设 5-10 个问题（完整问题库见 `assets/templates/perspective-questions.md`）。每视角独立扫描全文，不交叉影响——这是 Parnas Active Design Reviews 的核心：**让评审者做肯定断言而非被动挑错**。

| 视角 | 关注维度 | 示例问题 |
|---|---|---|
| **实现者 Implementer** | 可行性、资源、技术债、依赖 | "实现这个方案需要哪些前置条件？文档里都说了吗？" |
| **维护者 Maintainer** | 长期演化、可观测性、降级路径 | "3 年后谁来维护？文档里写了吗？" |
| **用户/客户 User/Customer** | 体验、价值、痛点、放弃条件 | "目标用户是谁？文档里描述得够具体能反驳吗？" |
| **反对者/竞争对手 Adversary/Competitor** | 弱点、可攻击面、可证伪点 | "如果我是竞争对手，看到这份文档会做什么？" |
| **决策者/投资人 Decision-maker/Investor** | ROI、机会成本、放弃条件、风险 | "什么数据出现就证明这个方案错了？文档里说了吗？" |

**为什么 5 个视角**：少于 5 个会留盲区（少一个利益相关方）；多于 5 个会重复（同一视角换名字）。如果用户 prompt 里要求增加某视角（如"加上法务视角"），按需扩展。

### Stage 3 — ARGUMENTS（论证拆解）

对文档中**最重要的 3-5 个核心论证**做 Toulmin 拆解 + Walton critical questions 攻击。完整方法论见 `references/methodology-foundations.md`。

**Toulmin 拆解**每个论证为：

```
Claim（结论） ← 这是评审者要追问"凭什么的"地方
   ↑
Warrant（推理依据） ← 这是评审者要追问"为什么这个依据成立"的地方
   ↑
Backing（支撑） ← 这是评审者要追问"这个支撑从哪里来"的地方
   ↑
Data（数据/证据） ← 这是评审者要追问"数据可靠吗"的地方

旁路：
Qualifiers（限定词） ← "可能"、"往往"、"几乎总是" — 限定词是否准确？
Rebuttals（反例） ← 文档是否承认了反例？反例是否被反驳？
```

**Walton critical questions** 按 argumentation scheme 选择匹配的攻击问题。最常见的几种：
- **专家意见型论证**：专家是否真的是该领域？是否有利益冲突？其他专家是否同意？
- **因果型论证**：相关性 ≠ 因果性。是否有第三方变量？方向是否反了？
- **类比型论证**：类比的两个事物在关键属性上是否真的相似？
- **统计型论证**：样本是否有偏？基线率是多少？效应量是否显著？
- **成本-收益型论证**：是否漏算了隐性成本？机会成本是否考虑了？

### Stage 4 — DECISIONS（决策质量与偏倚检查）

如果文档**包含决策或推荐**（不只是描述事实），强制走以下三个检查。完整方法论见 `references/bias-checks.md`。

1. **Pre-mortem（前置尸检）**：假设这个方案**已经失败了**，反向归因——最可能的失败原因是什么？文档里是否已经预防了这些？

2. **Key Assumptions Check**：列出方案依赖的**所有关键假设**（显式 + 隐含）。逐一标注：
   - 这个假设是否被显式检验过？
   - 假设成立的概率是多少？依据是什么？
   - 假设失败时方案的退化路径是什么？

3. **Analysis of Competing Hypotheses (ACH)**：当文档提出"原因是 X"或"应该选方案 X"时，强制列出**至少 2 个竞争假设/方案**，并问：哪些证据能**区分**这些假设？文档是否提供的是"支持性证据"还是"诊断性证据"？（支持性证据：与 X 一致；诊断性证据：能区分 X 与非 X）

### Stage 5 — REPORT（输出）

#### 输出路径与命名

`results/<YYYYMMDD>/expert-reviewer/<doc-slug>.md`

- `<YYYYMMDD>` = 当日日期，如 `20260721`
- `<doc-slug>` 推导规则（按优先级）：
  1. 用户在 prompt 里显式提供的标签
  2. 本地文件去扩展名的文件名（如 `proposal.pdf` → `proposal`）
  3. URL 的主域名（如 `https://example.com/post` → `example-com-post`）
  4. 粘贴文本的前 30 个字符（去标点空格，连字符连接）
  5. 兜底：`review-<YYYYMMDD-HHMMSS>`

#### 报告结构

完整模板见 `assets/templates/review-report-template.md`。骨架：

```markdown
# 评审报告：<doc-title>

## 元信息
- 评审对象类型：<技术架构 | 业务产品 | 报告论文 | 混合>
- 评审日期：<YYYY-MM-DD>
- 文档来源：<路径/URL/粘贴/口述>
- 评审模式：红队 + 建设性 双视角

## 总览
### 总体评分与一句话结论
<评分：critical(0-2)/weak(3-5)/solid(6-8)/strong(9-10)>
<一句话结论：读完这份文档，评审者最想对作者说的一件事>

### 问题分布
| 严重等级 | 数量 | 占比 |
|---|---|---|
| Critical | N | X% |
| High | N | X% |
| Medium | N | X% |
| Low | N | X% |

## 详细问题清单

### 问题 #1：<一句话标题>
- **严重等级**：<Critical | High | Medium | Low>
- **发现阶段**：<PARSE | PERSPECTIVES | ARGUMENTS | DECISIONS>
- **视角**：<实现者 | 维护者 | ...>
- **原文引用**：<blockquote + 段落定位（如 "§3.2 第 2 段" 或文件:行 或 XPath）>
- **方法论依据**：<方法论名 + 核心提问 + 出处 references 文件>
- **🟥 红队视角**：<如果这份文档被对手攻击，这里的弱点是什么>
- **🟩 建设性视角**：<如果是你写，会怎么改>

### 问题 #2：...

## 结构化发现汇总

### Paul-Elder 8 要素覆盖
<表格：8 要素 × 是否被文档充分处理 × 缺口说明>

### 5 视角覆盖
<表格：5 视角 × 主要发现 × 严重等级>

### 核心论证的 Toulmin 拆解
<对 3-5 个核心论证的拆解表>

### 关键假设清单（Key Assumptions Check 产出）
<表格：假设 × 显式/隐含 × 概率 × 失败退化路径>

## 评审者自评
- 本份评审**没有覆盖到**的方面：
- 本份评审**存在偏倚**的可能来源：
- 如果只能改一件事，建议改：
```

#### 三证据齐全规则（**绝对约束**）

每个评审问题都必须包含三项证据，缺一不可：

1. **原文引用**：直接引用文档原文（用 `>` blockquote）+ 段落定位（章节号 / 段号 / 文件:行 / XPath / 时间戳）。文档无原文可引用（如口述场景）时，引用用户原话。
2. **方法论依据**：标注本问题基于哪个方法论提出 + 核心提问是什么 + 出处 references 文件路径。
3. **严重等级**：四档（Critical / High / Medium / Low），定义见下。

**严重等级定义**：

| 等级 | 含义 | 示例 |
|---|---|---|
| **Critical** | 不修复会导致方案根本性失败、被对手直接击穿、或论文被拒 | 致命逻辑漏洞、未承认的关键假设、数据造假 |
| **High** | 不修复会显著削弱方案的说服力或可行性 | 论证跳跃、关键数据缺失、未考虑主要风险 |
| **Medium** | 修复后能明显提升质量，但不修复不致命 | 视角缺失、表达歧义、次要假设未检验 |
| **Low** | 锦上添花的改进 | 措辞、格式、可读性、术语一致性 |

#### 双视角同时输出规则

每个问题必须同时给出：

- **🟥 红队视角**：假设你是对手 / 竞争对手 / 拒稿审稿人 / 黑客，看到这一段会怎么攻击？
- **🟩 建设性视角**：假设你是合作者 / 共同作者 / 教练，会怎么帮作者改？

不要只给其中之一。两种语气都要直接、不绕弯、不空话。

---

## 对象类型路由

PARSE 阶段检测到对象类型后，**强制加载对应 references 文件**，按其中的专用方法论评审：

| 对象类型 | references 文件 | 核心方法 |
|---|---|---|
| 技术/架构设计 | `references/technical-architecture-review.md` | ATAM 场景驱动 + Cognitive Dimensions of Notations + ADR 反向审计 |
| 业务/产品方案 | `references/business-product-review.md` | MECE 反向分解 + Pyramid Principle + YC/Sequoia 投资人评审 + Reference Class Forecasting |
| 报告/论文 | `references/paper-academic-review.md` | PRISMA 报告完整性 + GRADE 证据确定性 + CASP/JBI 设计特定 checklist + Cochrane 偏倚评估 |

对象类型为"混合"时（如一份论文风格的商业白皮书），同时加载最相关的 2 个 references 文件并标注每条发现来自哪个视角。

---

## 证据链通用规则

无论对象类型，**所有引用的事实/数据/外部声明**都要按 SIFT 方法验证（见 `references/source-evaluation.md`）：

1. **Stop**：遇到文档里的关键事实/数字/引用，先停一下，不要默认相信
2. **Investigate the source**：这个事实/数字来自哪里？文档是否给了出处？出处可靠吗？
3. **Find better coverage**：其他来源是否一致？是否有更权威的来源？
4. **Trace claims to origin**：能否追溯到原始来源？中间是否有失真？

文档里的"据说"、"业内人士透露"、"行业惯例"等无出处声明是 **High 严重等级问题**，除非有 backing。

---

## 追问机制

输出报告后，**保持评审上下文**，允许用户：

- **挑战评审结论**："你在第 3 点是不是太严了？" / "这点我不同意，理由是 X"
  - 评审者应**回应挑战**，要么修正结论（承认过严/过宽），要么加强论证（说明为什么坚持）
- **请求深挖**："再深挖一下 bias 检查" / "把 PERSPECTIVES 阶段的'反对者'视角展开"
  - 评审者**增量修订**原报告（不重新生成），在对应章节后追加 "## 追问 N：<标题>"
- **请求重新看某段**："重新看一下 §4 那段，我改过了"
  - 评审者**只针对该段**重新跑相关阶段，输出 "## 修订 N：针对 §4 的复评"
- **请求加视角**："加上法务视角"
  - 评审者**只跑新视角**，把发现合并进原报告

**绝不**因为追问而重新生成整份报告——浪费 token 且丢失原报告的演进轨迹。

---

## 工作原则（why, not just what）

1. **解释 why，而不是堆 MUST**。本 SKILL.md 大量使用"为什么"段落（如"为什么 5 个视角"），目的是让模型理解方法论的精神而不是机械执行步骤。如果遇到不在预设步骤内的情况，模型应基于"视角化提问 + 显式化假设 + 网络化验证"的精神自行决策。

2. **肯定断言优于挑刺**。Parnas Active Design Reviews 的洞见：评审者做"这段是否满足 X 要求"的**肯定断言**比"找找这段有什么毛病"的**否定挑刺**效果好得多。在 PERSPECTIVES 阶段，每个视角结束时输出一行 "本视角下，文档在以下方面是 OK 的：<列表>"，再列出问题。

3. **方法论的目的是暴露假设，不是套用框架**。不要为了用 Toulmin 而用 Toulmin。如果某个核心论证天然适合 Pre-mortem 而不适合 Toulmin 拆解，按 Pre-mortem 处理。references 文件是工具箱，不是清单。

4. **避免评审者自身的偏倚**。每份报告末尾的"评审者自评"是必须的——评审者也是人（或 LLM），有偏好、有盲点。声明本份评审可能存在哪些偏倚，让读者校准。

5. **直接、不绕弯、不空话**。每个问题描述要能让作者**立刻定位 + 立刻判断是否同意**。避免"建议进一步考虑"这类空话。

6. **不同对象类型的语气不同**。技术文档可以更直接犀利；业务文档要承认不确定性；论文要尊重学术规范（如不轻易怀疑数据造假，但严格检查方法学）。

---

## 资源参考

| 文件 | 用途 | 何时读 |
|---|---|---|
| `assets/templates/review-report-template.md` | 完整输出模板 | Stage 5 REPORT 时必读 |
| `assets/templates/perspective-questions.md` | 5 视角的预设问题库 | Stage 2 PERSPECTIVES 时必读 |
| `references/methodology-foundations.md` | 通用层方法论详解（Toulmin / Walton / Paul-Elder / Pre-mortem） | Stage 3-4 时必读 |
| `references/technical-architecture-review.md` | 技术/架构专用方法（ATAM / CDN / ADR 反向审计） | 对象类型=技术架构时必读 |
| `references/business-product-review.md` | 业务/产品专用方法（MECE / Pyramid / YC rubric / RCF） | 对象类型=业务产品时必读 |
| `references/paper-academic-review.md` | 论文/报告专用方法（PRISMA / GRADE / CASP / Cochrane） | 对象类型=报告论文时必读 |
| `references/source-evaluation.md` | 证据链验证（SIFT / Lateral Reading / CRAAP） | Stage 3 ARGUMENTS 与 Stage 5 REPORT 时必读 |
| `references/bias-checks.md` | 偏倚检查（CIA SAT / ACH / Noise decision hygiene） | Stage 4 DECISIONS 时必读 |
