# 业务/产品方案专用评审方法

> 当对象类型 = 业务/产品 时加载。核心：**反向假设检验** + **MECE 分解** + **投资人评审视角** + **行为经济学去偏**。

## 1. MECE 反向分解

出处：McKinsey；Minto, *The Pyramid Principle*。

核心：MECE = Mutually Exclusive, Collectively Exhaustive。任何分解（市场分块/客户分群/收入构成/风险分类）都应 MECE。**反向审计**：把文档的分解还原，检查是否 MECE。

典型失败：不互斥（"付费用户和活跃用户"——付费用户可能也活跃）/ 不穷尽（"北美、欧洲、亚洲"——非洲南美大洋洲？）/ 分解标准不一致（同一层混用维度）。

## 2. Pyramid Principle 反向审计

出处：Minto, *The Pyramid Principle*。

核心：商业文档应**结论先行**，论据支撑结论，子论据支撑论据——金字塔结构。**反向审计**：还原金字塔检查是否成立。

评审操作：
1. **找顶层结论**：核心主张是什么？一句话能说清？找不到 = Critical；模糊 = High
2. **找论据层**：直接论据 3-5 个？0 个 = Critical（无支撑）；1-2 个 = High（不足）；> 7 个 = Medium（没分组）
3. **检查 MECE**：论据间 MECE？
4. **检查纵向支持**：每论据真支撑顶层？
5. **检查横向关系**：论据间是并列/递进/因果？文档说清？

典型失败：结论埋没（藏在第 N 段）/ 结论模糊（"提升业务"而非"年 GMV X→Y"）/ 论据堆砌（20 条没分组）/ 逻辑跳跃（论据到结论有未显式 warrant）/ 结论与论据脱节。

## 3. YC / Sequoia / a16z 投资人评审清单

出处：[Sequoia, *Writing a Business Plan*](https://www.sequoiacap.com/article/business-plan-template/)；[a16z](https://a16z.com)；[YC Startup Library](https://www.ycombinator.com/library)。

Sequoia Business Plan **10 段落**（评审每段都检查）：

| # | 段落 | 评审提问 |
|---|---|---|
| 1 | Company Purpose | 一句话能说清公司要做什么？ |
| 2 | Problem | 客户痛点？为什么现有方案不够？ |
| 3 | Solution | 怎么解决？为什么**现在**能解决？ |
| 4 | **Why Now** | 为什么是现在？过去为什么不行？未来会不会太晚？**最常省略** |
| 5 | Market Size | TAM/SAM/SOM？计算依据？ |
| 6 | **Competition** | 直接/间接竞争对手？为什么你能赢？**最常省略** |
| 7 | Product | 核心功能？差异化？路线图？ |
| 8 | Business Model | 怎么赚钱？单位经济（LTV/CAC）？定价？ |
| 9 | Team | 创始人背景？为什么这团队？ |
| 10 | Financials | 收入/成本/利润预测？融资需求？ |

**Marc Andreessen PMF 补充**：团队声称的 PMF 是否真有？依据（用户增长/留存/NPS/付费意愿）？没有 PMF 文档承认还是默认有？找 PMF 路径？多久没找到就换方向？

## 4. Reference Class Forecasting

出处：Kahneman & Lovallo, *Timid Choices and Bold Forecasts*, Management Science 2003；Kahneman, *Thinking, Fast and Slow*。

核心：人类预测项目成功率时**严重乐观偏差**（planning fallacy）。校准方法 = 找一类**相似历史项目**，用实际结果分布校准当前预测。

操作：
1. 找文档的**所有量化预测**（收入/用户数/上线时间/成本/转化率）
2. 对每个预测问：**内部视角依据**（团队自己算的）？**外部视角**（reference class）？参考了哪些相似项目？相似项目**实际结果分布**？
3. 缺外部视角 → High
4. 预测显著高于 reference class 中位数 → High（除非强力 backing）

典型 reference class：YC 同期公司存活率/增长率 / 相似定位产品首年销量 / 相似规模工程项目工期 / 同行业同阶段融资轮退出率。

## 5. Red Teaming 业务版

出处：[Wikipedia Red Team](https://en.wikipedia.org/wiki/Red_team)；CIA Tradecraft Primer。

业务版 5 个攻击角色：

| 角色 | 攻击问题 |
|---|---|
| **直接竞争对手** | 复制核心功能 + 价格战 / 锁定供应商 / 挖关键人 / 监管投诉 |
| **替代品厂商** | 用不同技术路线解决同一用户痛点（不需复制方案） |
| **监管者** | 找合规漏洞 / 数据合规 / 反垄断 / 行业许可 |
| **不满客户** | 公开吐槽 / 集体诉讼 / 竞品引流 |
| **离职员工/内鬼** | 数据泄露 / 商业秘密带走 / 负面媒体爆料 |

操作：扮演每角色 → 列 3-5 个最可能攻击路径 → 检查文档预防 → 未预防 = High/Critical。

## 6. 经典战略框架作为评审镜头

出处：Porter, *Five Competitive Forces*, HBR；[Christensen Institute on JTBD](https://www.christenseninstitute.org)；[Strategyzer BMC](https://www.strategyzer.com)。

不是"套用"，而是作为**评审镜头**——从每镜头看文档，发现一类特定问题。

- **Porter's Five Forces**：买方议价 / 供方议价 / 新进入者威胁 / **替代品威胁**（用户能否用完全不同方案解决同一痛点？）/ 行业竞争强度
- **Jobs-to-be-Done (JTBD)**：用户"雇佣"产品来**做什么工作**？功能性/情感性/社会性维度？现有替代方案做得不够的是什么？文档功能真的做好这份工作？
- **Business Model Canvas**：9 模块（客户细分/价值主张/渠道/客户关系/收入来源/核心资源/核心活动/核心伙伴/成本结构）是否覆盖？模块间**自洽**？（高端价值主张 + 廉价渠道 = 不自洽）

## 业务/产品方案评审清单

| # | 检查 | 主用方法 |
|---|---|---|
| 1 | 顶层结论**一句话能说清**？ | Pyramid |
| 2 | 论据 **MECE**？ | MECE |
| 3 | Sequoia **10 段落**都覆盖？ | Sequoia rubric |
| 4 | **PMF 主张**的依据？ | Andreessen |
| 5 | 量化预测用**外部视角**校准？ | RCF |
| 6 | 5 个 **Red Team 角色**攻击预防？ | Red Teaming |
| 7 | **Five Forces** 中最薄弱的力？ | Porter |
| 8 | **JTBD** 描述清晰？ | JTBD |
| 9 | **BMC** 9 模块覆盖且自洽？ | BMC |
| 10 | 团队/融资/财务与方案**匹配**？ | Sequoia 段 9-10 |
