# 报告/论文专用评审方法

> 当对象类型 = 报告论文 时加载。核心：**报告完整性** + **证据确定性** + **偏倚评估** + **论证严谨性**。

## 1. PRISMA 2020 报告完整性

出处：[PRISMA 2020 Statement](https://www.prisma-statement.org/prisma-2020-statement)；[Page et al., BMJ 2021](https://www.bmj.com/content/372/bmj.n71)。

核心：系统综述/meta-analysis 报告应包含 27 条目。评审任何**综述类**文档可用 PRISMA 检查完整性（即使非医学综述）。

精简条目表：

| 类别 | 条目 | 评审重点 |
|---|---|---|
| Title/Abstract | 1-2 | 是否标明研究设计？ |
| Background | 3 | 背景与目的清晰？ |
| Methods - Eligibility | 4-5 | 纳入/排除标准清晰？ |
| Methods - Information Sources | 6-7 | 数据库/注册库/其他来源列全？ |
| Methods - Search | 8 | **完整检索式**附出？**最常缺失** |
| Methods - Selection | 9 | 多人独立筛选？分歧如何解决？ |
| Methods - Data Collection | 10-11 | 数据提取流程标准化？ |
| Methods - Risk of Bias | 12-14 | 用了什么偏倚评估工具？ |
| Methods - Synthesis | 15-16 | 综合方法？定性/定量？meta-analysis 模型？ |
| Results - Selection | 17 | **流程图**？筛选漏斗？**最常缺失** |
| Results - Study Characteristics | 18 | 纳入研究特征表？ |
| Results - Risk of Bias | 19-20 | 偏倚评估结果？ |
| Results - Synthesis | 21-23 | 各研究结果 + 综合结果 + 异质性？ |
| Discussion | 24a-c | 主要发现 / 局限 / 结论 |
| Other | 25-27 | 注册 / protocol / 支持 |

**流程图缺失**（条目 17）和**检索式缺失**（条目 8）是最常见 Critical 问题。

适用：✅ 系统综述/meta-analysis/scoping review/rapid review / 任何"综合多个研究/数据源"的报告；❌ 单一原始研究（用 CASP/JBI）。

## 2. GRADE 证据确定性

出处：[GRADE Working Group](https://www.gradeworkinggroup.org/)；[Guyatt et al., BMJ 2008](https://www.bmj.com/content/336/7652/1049)。

核心：评价**证据体**（body of evidence）的确定性，不是单个研究。

| 升级因素 | 评审提问 |
|---|---|
| Effect size 大 | RR > 2 或 < 0.5？ |
| Dose-response | 剂量-反应关系？ |
| Plausible confounding | 残余混杂会**减弱**而非增强观察效应？ |

| 降级因素 | 评审提问 |
|---|---|
| Risk of Bias | 纳入研究有方法学缺陷？ |
| Inconsistency | 各研究结果方向一致？ |
| Indirectness | PICO 匹配？人群/干预/对照/结局直接？ |
| Imprecision | 置信区间过宽？样本量足够？ |
| Publication Bias | 漏斗图不对称？小样本研究系统性更乐观？ |

最终证据等级：High / Moderate / Low / Very Low。文档声称 High 但实际只到 Low = Critical。

## 3. CASP / JBI 设计特定 checklist

出处：[CASP](https://casp-uk.net/casp-tools-checklists/)；[JBI](https://jbi.global/critical-appraisal-tools)。

核心：不同研究设计有不同偏倚来源。用**设计匹配 checklist** 评审比通用评审更准。

按研究设计路由：

| 研究设计 | 关键检查项 |
|---|---|
| **RCT 随机对照** | 随机化 / 盲法 / 分配隐藏 / 失访 / ITT 分析 |
| **Systematic Review** | 检索策略 / 选择过程 / 偏倚评估 / 综合 |
| **Cohort 队列** | 暴露测量 / 随访完整性 / 混杂控制 |
| **Case-Control** | 病例定义 / 对照匹配 / 暴露回忆偏倚 |
| **Qualitative** | 研究设计 / 招募 / 数据收集 / 伦理 / 价值 |
| **Diagnostic Test** | 金标准 / 盲法 / 重复性 |
| **Economic Evaluation** | 视角 / 成本效益测量 / time horizon / 敏感性分析 |

设计不明 = Critical（不知道是什么设计就评审是危险的）。

## 4. Cochrane 偏倚评估

出处：[Cochrane Handbook](https://training.cochrane.org/handbook/current)；[RoB 2](https://www.riskofbias.info/welcome/rob-2-0-tool) for RCTs；[ROBINS-I](https://www.riskofbias.info/welcome/robins-i-tool) for non-randomized。

**RoB 2 (RCT) 5 领域**：随机化过程 / 偏离既定干预（盲法？）/ 缺失结局数据（失访率？ITT？）/ 结局测量（测量者盲法？）/ 结果选择（事后选择有利？）。

**ROBINS-I (非随机) 7 领域**：混杂 / 参与者选择 / 干预分类 / 偏离既定干预 / 缺失数据 / 结局测量 / 结果选择。

每领域打分 Low risk / Some concerns / High risk。综合：全 Low → Low；有 Some concerns → Some concerns；任一 High → High。文档声称 high quality 但 RoB 显示 High = Critical。

## 5. Toulmin 论文版 + Walton 学术型 scheme

Toulmin 通用模型见 `methodology-foundations.md` §3。论文评审特定关注：

- **Data**：采集规范？样本量充分？经 IRB？
- **Warrant**：统计方法合适？假设满足？
- **Backing**：引用充分？引了相反观点？
- **Rebuttal**：局限性章节真诚？还是走过场？

Walton 学术型 scheme：

| Scheme | 关键检查 |
|---|---|
| **学术权威型** | X 真的是该领域权威？期刊同行评审？引原文还是二次转述？断章取义？ |
| **文献综述型** | 检索系统（参考 PRISMA）？cherry-picked（只引支持不引反对）？"已有研究"多少？是否过时？ |
| **统计显著性型** | 效应量 vs 统计显著？样本过大（微小效应也 p<0.05）？多重比较调整（Bonferroni/FDR）？pre-registered？ |
| **推广型** | 样本代表总体？有 selection bias？总体边界？过度推广？外部效度依据？ |

## 6. SIFT + Lateral Reading 引用链验证

完整 SIFT 见 `source-evaluation.md`。论文评审时特别关注引用链：

1. **引用真实性**：引用真存在？（Wineburg & McGrew 研究：专业 fact-checker **逐条核查**引用）
2. **引用准确性**：被引论文真说了文档声称它说的话？
3. **引用代表性**：只引支持自己观点？引了相反观点？
4. **引用时效性**：引了过时论文？最新进展覆盖？
5. **自引比例**：作者自引过高（> 30%）= 中等严重
6. **掠夺性期刊**：引用来自可靠期刊？

抽查 5-10 条关键引用用 SIFT 验证。不真实 = Critical；不准确（断章取义/误读）= High；单方面引用 = High。

## 7. Replication Crisis 检查

出处：[Open Science Framework](https://osf.io/)；[Center for Open Science](https://www.cos.io/)；[Stanford Encyclopedia](https://plato.stanford.edu/entries/scientific-reproducibility/)。

核心：心理学/生物医学/经济学等多领域存在**复现危机**——大量已发表研究无法独立复现。评审要主动检查**复现危机后的改革措施**：

| 检查项 | 评审提问 |
|---|---|
| **Pre-registration** | 假设/设计/分析在数据收集**前**预注册？(OSF / AsPredicted) |
| **Registered Reports** | 以 Registered Report 形式投稿？（同行评审在数据收集前） |
| **Open Data** | 原始数据公开？可下载？ |
| **Open Code** | 分析代码公开？ |
| **Open Materials** | 实验材料公开？ |
| **Power Analysis** | 样本量经事先功效分析？基于什么效应量？ |
| **Multiple Comparison Correction** | Bonferroni / FDR 校正？ |
| **Effect Size + CI** | 报告效应量 + 置信区间（不只 p 值）？ |
| **Independent Replication** | 被独立复现？或主动承认未被复现？ |

文档声称"突破性发现"但无任何改革措施 = High/Critical。

## 报告/论文评审清单

| # | 检查 | 主用方法 |
|---|---|---|
| 1 | 研究设计清晰？ | CASP/JBI |
| 2 | 设计匹配的偏倚评估？ | Cochrane RoB / ROBINS-I |
| 3 | 综述类 PRISMA 完整？ | PRISMA |
| 4 | 证据体确定性 GRADE？ | GRADE |
| 5 | 核心论证 Toulmin 完整？ | Toulmin |
| 6 | 学术权威型论证 Walton 检查？ | Walton |
| 7 | 引用链真实/准确/代表？ | SIFT + Lateral Reading |
| 8 | 复现危机改革措施？ | Open Science |
| 9 | 局限性章节真诚？ | Walton |
| 10 | 统计方法合适？ | CASP / Walton |
