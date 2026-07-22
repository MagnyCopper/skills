# 评审报告：AWS 实时通知系统架构方案（API Gateway → Lambda → DynamoDB → Streams → Lambda → SNS → 3×SQS → 3×Lambda → FCM/SES/SNS）

## 元信息

| 字段 | 值 |
|---|---|
| 评审对象类型 | 技术架构设计（含部分业务/资源约束） |
| 评审日期 | 2026-07-22 |
| 文档来源 | 对话粘贴（用户自然语言描述的架构方案） |
| 文档体量 | 约 220 字英文 / 1 段架构描述 + 4 句约束 |
| 评审模式 | 红队 + 建设性 双视角（默认） |
| 评审者 | expert-reviewer skill (v1.0) |
| 对象类型路由 | 加载 `references/technical-architecture-review.md`（ATAM + ADR 反向审计 + Cognitive Dimensions + AWS Well-Architected 6 支柱） |

---

## 总览

### 总体评分

| 维度 | 分数 (0-10) | 一句话说明 |
|---|---|---|
| 论证严谨性 | 2 | 关键决策（为什么 serverless、为什么这条链路）几乎无 backing，多个核心 claim 无 warrant |
| 证据充分性 | 2 | 没有任何容量计算、成本估算、SLO 目标、失败率目标；只给了"10M/天"一个数字 |
| 决策质量 | 2 | "我们选 serverless 因为不想管服务器"——典型把偏好当论证；无 alternatives、无 kill criteria |
| 视角覆盖 | 2 | 只有 builder 视角；安全/运维/成本/合规/用户体验视角全部缺席 |
| 文档质量 | 3 | 描述了链路但无架构图、无数据契约、无 SLA；术语"SNS"两次出现指代不同服务造成认知歧义 |
| **综合** | **2.2 / 10（Critical）** | **方向（事件驱动 + serverless）合理，但当前描述无法支撑 10M/天的生产承诺；多个 Critical 缺口需在动工前补齐，否则上线即翻车。** |

**综合评分量表对照**：0-2 `Critical`——根本性失败，需重写。

### 一句话结论

> 在 2 名工程师、3 个月、1000 万/天规模的约束下，这份方案最致命的问题不是"会不会做出来"，而是**"做出来之后怎么知道它在不在正常工作"——可观测性、幂等性、失败恢复三项几乎完全缺失，这意味着系统第一次出问题就会是用户先发现、而不是工程师先发现**。

### 问题分布

| 严重等级 | 数量 | 占比 |
|---|---|---|
| 🔴 Critical | 7 | 24% |
| 🟠 High | 12 | 41% |
| 🟡 Medium | 8 | 28% |
| 🟢 Low | 2 | 7% |
| **合计** | **29** | **100%** |

---

## 详细问题清单

> 每个问题包含 7 个字段：严重等级 / 发现阶段 / 视角 / 原文引用 / 方法论依据 / 🟥 红队视角 / 🟩 建设性视角。

---

### 问题 #1：缺少幂等性设计，Lambda 至少一次投递会产生重复通知

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "DynamoDB Streams triggers another Lambda → that Lambda publishes to SNS → SNS fans out to 3 SQS queues ... each queue has a dedicated Lambda consumer that calls the downstream service"

  —— 架构描述段（链路无幂等键、无去重步骤）

- **方法论依据**：AWS Well-Architected Reliability 支柱 + Pattern/Anti-pattern Catalogs（出处：`references/technical-architecture-review.md` §4 / §5）。核心提问："系统在部分失败时如何表现？是否暗合 Missing Idempotency 反模式？"

- **🟥 红队视角**：
  DynamoDB Streams 与 SQS 都是**至少一次投递**（at-least-once）。当 consumer Lambda 因超时/限流重试时，同一条通知会被发到 FCM/SES/SMS 两次甚至多次。我会作为"愤怒用户"投诉：为什么我的手机收到 3 条一模一样的推送？为什么营销邮件发两遍触发我退订？最恶毒的情况：交易类 SMS 被重复发送，用户误以为账户被扣了两次而打客服——直接放大运营成本。在 10M/天规模下，即使只有 0.1% 的重复率也是每天 1 万条垃圾通知。

- **🟩 建设性视角**：
  显式加一段："**幂等性**：每条通知在写入 DynamoDB 时生成 `notification_id`（ULID），所有下游 consumer 在调用 FCM/SES/SMS 前先用 `notification_id + channel` 在 DynamoDB 或 Redis 做去重写入（conditional put）。FCM 的 `message_id`、SES 的 `MessageId`、SMS 端的 vendor message ID 都要落库以支持对账。" 把这条变成一条 ADR：ADR-003《幂等性策略》。

---

### 问题 #2：没有死信队列（DLQ）与重试策略，下游失败即静默丢消息

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "each queue has a dedicated Lambda consumer that calls the downstream service (FCM for push, email for SES, SMS for SNS)"

  —— 全文未提及 DLQ、未提及 maxReceiveCount、未提及重试退避策略

- **方法论依据**：ATAM 失败模式枚举 + AWS Well-Architected Reliability（出处：`references/technical-architecture-review.md` §1 / §4）。核心提问："失败模式枚举了吗？降级策略在哪？"

- **🟥 红队视角**：
  FCM 会限流（HTTP 429）；SES 会因为 bounce/complaint 被 sandbox；SMS 运营商网关会随机 503。这些在 10M/天规模下是**确定性**事件而非小概率。SQS 默认 `maxReceiveCount` 用尽后消息直接消失（如果是标准队列）或无限重试阻塞队列（如果是 FIFO）。我会作为"业务方"质问：双十一那天发了 1000 万通知，报表说 700 万成功，剩下 300 万去哪了？没有任何 DLQ 意味着这些丢失**无法追溯、无法重放、无法补偿**。

- **🟩 建设性视角**：
  补充一节《失败处理》：①每个 SQS 配 DLQ（`<channel>-dlq`），`maxReceiveCount = 5`；②Lambda consumer 用指数退避 + jitter；③DLQ 触发 SNS 告警 + 落到一张 `failed_notifications` 表供人工/补发消费；④对 SES bounce/complaint 单独建一条反馈链路（SES → SNS → Lambda → 标记用户不可达）。这条必须在 3 个月时间表内排进 MVP。

---

### 问题 #3：2 工程师 × 3 个月 × 10M/天 = 资源—规模严重错配

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 4 DECISIONS（Pre-mortem）
- **视角**：决策者/投资人 Decision-maker
- **原文引用**：

  > "Team is 2 engineers, we have 3 months to get to production. ... We expect about 10 million notifications per day at peak."

- **方法论依据**：Pre-mortem（Klein 2007）+ Outside-In / Reference Class Forecasting（出处：`references/bias-checks.md` §1 / §8；`references/methodology-foundations.md` §5）。核心提问："同类规模系统的实际交付数据是什么？这次为什么特殊？"

- **🟥 红队视角**：
  Reference class：一个日活 10M 通知、多通道、含可观测性与降级路径的生产系统，行业经验值是 **5-8 名工程师 × 6-9 个月**（含 on-call、安全评审、合规）。2 人 × 3 个月达到 MVP（不含监控/DR/合规）勉强可能，达到"production"几乎不可能。我会作为投资人直接拒：这个时间表意味着会跳过安全评审、跳过压测、跳过混沌测试，10M 流量一上来必爆。更糟的是 2 人都在写代码，没人做 SRE，上线后第一个 incident 就会 100% 占用他们——再没人修 bug，进入死亡螺旋。

- **🟩 建设性视角**：
  把"production"重新定义：MVP 只接 1 个通道（建议先做 push，因为合规最轻），目标 1M/天而非 10M/天；3 个月后扩到 2 通道 + 5M/天；6 个月才碰 10M/天 + SMS（最重合规）。或者把预算前置花在 1 名合同制 SRE + 1 名 QA 上，比多写代码更值。把这条写进 ADR-001《范围与里程碑》。

---

### 问题 #4："实时"未定义 SLA，整条链路的延迟预算无依据

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 1 PARSE（Paul-Elder：Concepts + Question at issue）
- **视角**：用户/客户 User
- **原文引用**：

  > "real-time notification system"

  —— 标题即用"real-time"，但全文无 P50/P99 延迟目标

- **方法论依据**：Paul-Elder 的 Concepts / Question at issue + ATAM 的 quality attribute 必须可量化（出处：`references/methodology-foundations.md` §1；`references/technical-architecture-review.md` §1）。核心提问："每个 quality attribute 有可量化目标吗？"

- **🟥 红队视角**：
  "Real-time"在工程上是**有定义**的术语——软实时通常指 P99 < 1s，硬实时是毫秒级。但本方案 5 跳链路（API Gateway → Lambda → DynamoDB → Streams → Lambda → SNS → SQS → Lambda）：仅 DynamoDB Streams 自身就有 **秒级**延迟（Streams 内部轮询间隔），加上 Lambda cold start（数百毫秒到数秒）+ SQS long polling（最多 20s），最坏情况端到端延迟可达 **30 秒以上**。我会作为竞品写一篇对比文："他们也叫实时，我们 P99 200ms。"——一刀切走用户。

- **🟩 建设性视角**：
  把"real-time"换成具体数字，并解释依据：例如"业务可接受 P95 ≤ 5s，P99 ≤ 30s；交易类通知必须 P99 ≤ 2s"。然后**反向分配延迟预算**到每一跳：API Gateway 50ms / 写 Lambda 100ms / DynamoDB write 50ms / Streams 1-5s / fanout Lambda 200ms / SNS+SQS 500ms / consumer Lambda 1s / downstream 1s。这张表会立刻暴露"Streams 是瓶颈"——可能直接换成 Kinesis 或 DynamoDB Streams + enhanced fan-out。

---

### 问题 #5：移动端直接调 API Gateway，无任何鉴权/限流/输入校验描述

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 2 PERSPECTIVES（反对者/竞争对手视角）
- **视角**：反对者/竞争对手 Adversary
- **原文引用**：

  > "mobile clients call API Gateway → a Lambda function writes the notification to DynamoDB"

  —— 全文未提及 auth、未提及 IAM/Cognito、未提及 WAF、未提及 throttling

- **方法论依据**：AWS Well-Architected Security 支柱 + Red Team Analysis（出处：`references/technical-architecture-review.md` §4；`references/bias-checks.md` §5）。核心提问："零信任？数据加密？权限最小化？审计日志？"

- **🟥 红队视角**：
  我是攻击者，看到"mobile clients call API Gateway"且没有任何 auth 描述，第一反应：是不是直接暴露了无认证 endpoint？哪怕用了 API Key 也是 client-side 可逆向的。攻击路径：①扒 APK 找 endpoint；②直接 POST 伪造 notification_id 把任意内容推到任意用户（钓鱼/诈骗 SMS）；③100 个 IP 并发刷 API Gateway → 撑爆下游 Lambda → DynamoDB 写入限流 → 全平台拒绝服务。10M/天 = 平均 116 QPS，攻击者用一台 VPS 就能 10 倍超量。SMS 通道尤其危险：每条短信几分钱，攻击者刷一晚能让 AWS 账单上 6 位数。

- **🟩 建设性视角**：
  加一段《安全模型》：①API Gateway 用 Cognito/JWT 鉴权，每个用户只能给**自己**发通知或必须由授权的 server-side 调用（注意：通常 notification 系统的调用方是后端服务，不是终端用户——这点要在 PRD 里澄清"调用方到底是谁"）；②API Gateway 配 usage plan + throttling（per-key 限流）；③前置 WAF 防常见注入；④所有 Lambda IAM role 最小权限；⑤DynamoDB 开 point-in-time recovery；⑥notification payload 不存敏感 PII，或加密字段。把这条变成 ADR-005《安全与限流》。

---

### 问题 #6："Not sure if we need any monitoring beyond CloudWatch default"——可观测性是最大盲区

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "We're not sure if we need any monitoring beyond CloudWatch default dashboards."

- **方法论依据**：AWS Well-Architected Operational Excellence 支柱 + Cognitive Dimensions 的 Hidden Dependencies（出处：`references/technical-architecture-review.md` §4 / §3）。核心提问："部署/监控/事件响应流程在哪？runbook 在哪？"

- **🟥 红队视角**：
  CloudWatch default dashboards 只给 Lambda invocations / errors / duration 的聚合视图。**它不会告诉你**：①某条特定通知卡在哪一跳（无 distributed tracing）；②FCM 投递成功率掉到 80%（无业务指标）；③DLQ 在堆积（无告警）；④单条 SMS 因为运营商返回"号码不存在"但 Lambda 视为成功（无 downstream visibility）。我会作为 incident 复盘者写：周一用户投诉周末没收到通知，工程师打开 CloudWatch 看到一片绿色，因为 Lambda error=0，但实际是下游 FCM 返回 4xx 被 Lambda 当成业务正常处理了——**绿色仪表盘 + 大规模 silent failure** 是 serverless 最经典的翻车模式。

- **🟩 建设性视角**：
  强制 4 件最小事，3 个月内必须做完：①**X-Ray distributed tracing**，每条 notification 携带 trace ID 贯穿 5 跳；②**结构化日志**（JSON），关键字段 `notification_id / channel / user_id / status / latency_ms`，便于 CloudWatch Logs Insights 查询；③**业务指标自定义**：投递成功率、P95/P99 端到端延迟、DLQ 深度、下游 4xx/5xx 分布——用 CloudWatch Metric Math 或埋点到 Datadog；④**告警**：SLO 烧穿率告警（错误预算耗尽 50% / 100%）、DLQ 深度 > 阈值、单 channel 成功率 < 95%。这条单独写 ADR-007《可观测性策略》。

---

### 问题 #7："SNS"一词两次出现指代不同 AWS 服务，是设计层的认知陷阱

- **严重等级**：🔴 Critical
- **发现阶段**：Stage 1 PARSE（Paul-Elder：Concepts）
- **视角**：维护者 Maintainer（也波及所有后续视角）
- **原文引用**：

  > "...that Lambda publishes to **SNS** → **SNS** fans out to 3 SQS queues ... SMS) → each queue has a dedicated Lambda consumer that calls the downstream service (... SMS for **SNS**)"

  —— 同一段中"SNS"既指中央 pub/sub 总线，又指 SMS 通道下游服务（AWS SNS SMS）

- **方法论依据**：Cognitive Dimensions of Notations 的 Consistency + Role-Expressiveness（出处：`references/technical-architecture-review.md` §3）。核心提问："相似语义有相似语法？每部分目的可见？一眼看出干啥？"

- **🟥 红队视角**：
  这不是文案问题，是**设计问题**。当 2 名工程师 6 个月后回头看自己的 Terraform，会面对 `sns_topic` 和 `sns_sms` 两个资源，IAM policy 里 `sns:Publish` 到底授给谁？事故复盘时口头讨论"SNS 挂了"是哪个 SNS？更恶毒的是：AWS SNS（pub/sub）和 AWS SNS SMS 是**同一个 AWS 服务**的两种使用方式——你方案里"SNS fans out to SQS for SMS, then SMS Lambda calls SNS for SMS"是**两个 SNS topic + 一段 SMS API**，逻辑上 SMS 那条链路其实是 SNS → SQS → Lambda → SNS，这条路径在新人读架构图时会 100% 误读。

- **🟩 建设性视角**：
  ①在文档里把两个 SNS 显式命名：`NotificationFanoutTopic`（中央总线）vs `SmsSenderService`（下游通道），永远不再用裸词"SNS"；②**更激进的改法**：SMS 通道不一定要走 SNS SMS——评估 Pinpoint SMS、Twilio、AWS End User Messaging SMS（2024 年起新服务，SNS SMS 在被弱化）；③画一张架构图，每个节点一个 unambiguous 名字。

---

### 问题 #8：无成本估算，serverless 在 10M/天规模下账单可能爆炸

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（决策者/投资人视角）
- **视角**：决策者/投资人 Decision-maker
- **原文引用**：

  > "We chose serverless because we don't want to manage servers. ... We expect about 10 million notifications per day at peak."

- **方法论依据**：AWS Well-Architected Cost Optimization 支柱 + Toulmin 的 Backing 缺失（出处：`references/technical-architecture-review.md` §4；`references/methodology-foundations.md` §3）。核心提问："单位经济？长期成本？idle 资源？这个 Claim 的 backing 在哪？"

- **🟥 红队视角**：
  我会做粗算：10M 通知/天 × 30 天 = 3 亿/月。Lambda 调用次数：写 Lambda 1 次 + fanout Lambda 1 次 + 3 个 consumer Lambda 各 1 次 = 5 次/通知 → 15 亿次 Lambda 调用/月。即便按最便宜档 ~$0.20/百万，仅 Lambda 就是 $300/月（看似便宜）。但**SNS 消息** 3 亿条 ≈ $180/月；**SQS** 3 亿 API 请求 ≈ $135/月；**DynamoDB** 写 3 亿 + Streams 3 亿 ≈ 数百到上千美元；**FCM 免费、SES $0.10/1000 = $30000/月**（这才是大头！3 亿封邮件）；**SMS** 按国家 $0.006-$0.05/条，按美国均价 $0.0064 → 3 亿条 = **$1.92M/月**。如果 SMS 占比 30% 就是 $576K/月。我会作为 CFO 直接砍项目：你们以为省了服务器钱，结果短信费比服务器贵 100 倍。

- **🟩 建设性视角**：
  在动工前必须有一张《单位经济表》：每通知成本 = Lambda×5 + DynamoDB write + Streams read + SNS publish + SQS×3 + downstream vendor cost。按 push / email / SMS 三通道分别给数，假设通道比例（如 70/20/10）算月成本。然后**回答两个问题**：①月账单是否在业务能承受范围？②哪些通道该用更便宜替代（如 SMS 改 Pinpoint 或换国家走本地运营商）。

---

### 问题 #9：无 alternatives 考虑，每个关键决策都是"我们选 X"而非"我们比较了 X/Y/Z"

- **严重等级**：🟠 High
- **发现阶段**：Stage 3 ARGUMENTS（Toulmin：Warrant / Backing 缺失）
- **视角**：决策者/投资人 Decision-maker
- **原文引用**：

  > "We chose serverless because we don't want to manage servers." （唯一一处显式理由）

  —— 全文未提 ECS/Fargate、Kinesis、EventBridge、Step Functions、AppSync 等任何替代方案

- **方法论依据**：ADR 反向审计 + Devil's Advocacy（出处：`references/technical-architecture-review.md` §2；`references/bias-checks.md` §4）。核心提问："Alternatives 至少 2-3 个？为什么不是 B/C？"

- **🟥 红队视角**：
  这条链路里至少有 4 个决策没有 alternatives：
  ①为什么 DynamoDB Streams 而不是 Kinesis Data Streams？（Kinesis 在高吞吐 + 低延迟上更强）
  ②为什么 fanout 用 SNS→SQS 而不是 EventBridge？（EventBridge 原生支持内容路由、schema registry）
  ③为什么 fanout Lambda 不直接调 3 个 consumer，要插一层 SNS？（如果不需要订阅解耦，多一跳没收益）
  ④为什么每个 channel 单独一个 SQS+Lambda？合并成一个 Lambda 内 fan-out 会怎样？（少 3 套资源）
  我会作为评审委员会一票否决：连 alternatives 都没列的 ADR，本质上是"按感觉选的"，6 个月后想换方案时不知道当初为什么这么选。

- **🟩 建设性视角**：
  写至少 4 条 ADR：ADR-001《为什么 serverless 不是 ECS Fargate》、ADR-002《为什么 DynamoDB Streams 不是 Kinesis》、ADR-003《为什么 SNS+SQS 不是 EventBridge》、ADR-004《为什么 3 个独立 consumer 不是 1 个 fan-out Lambda》。每条至少给 2 个 alternatives + 选定理由 + 后果（正面 + 负面）。即使最终结论是"我们懒，选最熟的"，也要写下来。

---

### 问题 #10：Lambda cold start 与"real-time"承诺冲突，无 provisioned concurrency 计划

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "real-time notification system ... a Lambda function writes ... DynamoDB Streams triggers another Lambda ... Lambda consumer"

  —— 5 处 Lambda，无一处提及 provisioned concurrency / warmup

- **方法论依据**：ATAM 性能场景走查 + AWS Well-Architected Performance Efficiency（出处：`references/technical-architecture-review.md` §1 / §4）。核心提问："能 scale？瓶颈识别？资源利用率？"

- **🟥 红队视角**：
  Lambda cold start 在 JVM/Node 大依赖下可达 1-3 秒，Python 也要数百毫秒。最恶毒场景：流量突增（例如营销推送瞬间触发），3 个 consumer Lambda 同时冷启动，并发实例数瞬间从 0 跳到几百——AWS 默认 account-level 并发限制 1000，2 个就被卡死。DynamoDB Streams Lambda 还有 batch window，进一步加延迟。我会作为用户：从下单一刻到收到 push，等了 8 秒，这叫实时？

- **🟩 建设性视角**：
  ①对延迟敏感的写 Lambda 和 fanout Lambda 启用 **Provisioned Concurrency**（最小成本换稳定延迟）；②用 Lambda **Provisioned Concurrency Configurations** + Application Auto Scaling 应对峰值；③在 ADR 里写明 cold start 预算（如 P99 cold start ≤ 500ms）；④对 DynamoDB Streams Lambda 用 **enhanced fan-out + parallelization factor** 提升吞吐。

---

### 问题 #11：DynamoDB Streams 24 小时保留期 = 故障期间数据丢失窗口

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "DynamoDB Streams triggers another Lambda → that Lambda publishes to SNS"

  —— 未提及 Streams 保留期、未提及 PITR、未提及备份

- **方法论依据**：Pre-mortem + AWS Well-Architected Reliability（出处：`references/bias-checks.md` §1；`references/technical-architecture-review.md` §4）。核心提问："假设方案失败，最可能原因？降级路径在哪？"

- **🟥 红队视角**：
  DynamoDB Streams **硬上限 24 小时**。如果 fanout Lambda 因为 IAM 配置错误 / SNS 限流 / 代码 bug 持续失败超过 24 小时，所有未被处理的通知**永久丢失**——DynamoDB 主表数据还在，但"哪些通知要发"这件事丢了。真实场景：周五晚 8 点 fanout Lambda 开始 5xx，DLQ 没配，告警没接——周一上午工程师上班发现 200 万条通知消失了，且**无法从主表重建**（除非主表有 `is_sent` 状态字段——但方案里没说有）。

- **🟩 建设性视角**：
  ①DynamoDB 主表加 `status: PENDING|SENT|FAILED` + `sent_at` 字段，作为**重放数据源**——即使 Streams 丢数据，仍能从主表扫 PENDING 行重放；②开 Point-in-Time Recovery（35 天回放）；③把"Streams 处理延迟 > 1 小时"列为告警；④写一个 batch replayer 脚本，从主表扫 PENDING 重投。

---

### 问题 #12：链路 5+ 跳 + 无 correlation ID，单条失败无法定位

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "API Gateway → Lambda → DynamoDB → Streams → Lambda → SNS → SQS → Lambda → downstream"

  —— 9 个组件，无 correlation ID / trace ID 描述

- **方法论依据**：Cognitive Dimensions 的 Hidden Dependencies + AWS Well-Architected Operational Excellence（出处：`references/technical-architecture-review.md` §3 / §4）。核心提问："依赖关系可见？改字段影响哪些下游？事件响应流程？"

- **🟥 红队视角**：
  用户投诉"我没收到这条通知"，工程师拿到 `notification_id`，要去 9 个服务的日志里 grep——X-Ray 没接，每个服务日志格式不同，时间戳不对齐。最坏情况：API Gateway 日志保留 7 天，CloudWatch Logs retention 没配，事故发生 8 天后无法复盘。我会作为 SRE：解决一个用户工单需要 2 小时翻日志，2 名工程师 1 天能处理 16 单，每天 1% 出错率就是 10 万单——直接破产。

- **🟩 建设性视角**：
  ①每个 notification 在 API Gateway 入口生成 `correlation_id`（UUID v7 含时间戳），贯穿所有 9 个组件；②全部 Lambda 接 Lambda Powertools（Python/TypeScript/Java 都有）的 tracer + logger + metrics，自动注入；③CloudWatch Logs retention 按合规要求配置（建议 90 天）；④建一个"通知生命周期"查询页：输入 `notification_id` 看到完整时间线（哪个组件何时收到、何时返回、状态码）。

---

### 问题 #13：无 DR / 多 AZ / 多区域策略，单 AZ 故障即部分降级

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（反对者/竞争对手视角）
- **视角**：反对者/竞争对手 Adversary
- **原文引用**：

  全文未提及 region / AZ / DR / RTO / RPO。

- **方法论依据**：ATAM 可用性场景 + AWS Well-Architected Reliability（出处：`references/technical-architecture-review.md` §1 / §4）。核心提问："RTO/RPO？容量冗余？降级路径？"

- **🟥 红队视角**：
  AWS 单 region 内单 AZ 故障历史上发生过多次（us-east-1 2017/2021/2023）。DynamoDB 是多 AZ 复制的，但 Lambda 部署、SQS 队列、SNS topic 都在单 region。如果 region 级故障（如 2023 us-east-1 持续 4 小时），整个通知系统停摆。对"实时通知"业务，4 小时停摆可能意味着错过交易确认、错过 OTP 验证——下游业务直接受牵连。

- **🟩 建设性视角**：
  ①明确 RTO/RPO：例如"RTO ≤ 1h, RPO ≤ 5min"；②DynamoDB Global Table 跨 2 region；③Lambda 函数在 2 region 部署，Route 53 health check 切换；④或者承认"我们接受单 region 风险，因为业务允许 4h 停摆"——但要写进 ADR 让 stakeholder 知情。

---

### 问题 #14：合规盲区——SMS/Email 通道未提 CAN-SPAM / GDPR / TCPA / 合规退订

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（用户/客户 + 扩展法律视角）
- **视角**：用户/客户 User（叠加扩展视角 Legal/Compliance）
- **原文引用**：

  > "email for SES, SMS for SNS"

  —— 未提及用户偏好、退订、合规审计、consent 管理

- **方法论依据**：AWS Well-Architected Security + Pre-mortem 中"监管一夜变更"类（出处：`references/technical-architecture-review.md` §4；`references/bias-checks.md` §1）。核心提问："监管/合规风险？PR 危机预案？"

- **🟥 红队视角**：
  美国 SMS：未获明确 consent 给用户发短信违反 **TCPA**，每条 $500-$1500 法定赔偿，集体诉讼可达百万美元。Email：CAN-SPAM 要求每封营销邮件有退订链接 + 物理地址，违者每封 $46580 罚款（FTC 2024 标准）。欧盟 GDPR：未获 opt-in 给用户发通知 = €2000 万或全球营收 4%。SES 自带 bounce/complaint 处理，但需要你**主动**接 SNS 通知 + 标记用户。本方案没任何 consent 管理、退订链路、suppression list。我会作为原告律师：找 10 个客户做集体诉讼，2 工程师团队根本没有法务资源应对。

- **🟩 建设性视角**：
  ①PRD 第一条就是《合规要求》：列出覆盖国家 + 适用法规（CAN-SPAM/GDPR/TCPA/PIPL）；②建 `user_notification_preferences` 表（per-channel opt-in/opt-out + 时间戳 + 来源）；③SES bounce/complaint → SNS → Lambda → 自动加入 suppression list；④SMS 通过注册 A2P 10DLC / Toll-Free 号码（美国）+ 用户回复 STOP 自动退订；⑤营销类通知必须经过"模板审批 + 法务 review"流程。

---

### 问题 #15：AWS SNS SMS 服务在被弱化，应评估替代品

- **严重等级**：🟠 High
- **发现阶段**：Stage 3 ARGUMENTS（隐含 Backing 过时）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "SMS for SNS"（隐含 Backing："AWS SNS 是合适的 SMS 服务"）

- **方法论依据**：SIFT + Lateral Reading（出处：`references/source-evaluation.md` §1 / §2）。核心提问："Trace claims to origin：这个 Backing 在 2026 年是否仍然成立？"

- **🟥 红队视角**：
  AWS 2024 年起推出 **AWS End User Messaging SMS**（独立服务，原 SNS SMS 的演进路径），SNS SMS 文档已开始引导用户迁移。原生 SNS SMS 在多国支持、sender ID、合规报告上不如 Pinpoint / Twilio / MessageBird。我会作为竞品：你们还在用 SNS SMS，我们用 Pinpoint，支持每国本地号码、合规报告、双向 SMS、A/B 模板——你们做不了。

- **🟩 建设性视角**：
  ①在 ADR-006《SMS vendor 选择》里至少比较：AWS End User Messaging SMS、Pinpoint、Twilio、MessageBird；②判断标准：覆盖国家、单价、合规报告、双向 SMS、sender ID、本地号码支持；③如果只用美国，AWS End User Messaging SMS 够；如果跨多国，Twilio 几乎是行业标准。

---

### 问题 #16：无部署 / 回滚 / 灰度策略，2 人团队变更风险极高

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  全文未提及 CI/CD、未提及 Lambda alias/weighted traffic shifting、未提及 canary。

- **方法论依据**：AWS Well-Architected Operational Excellence + Cognitive Dimensions 的 Viscosity（出处：`references/technical-architecture-review.md` §4 / §3）。核心提问："部署/事件响应流程？变更成本？"

- **🟥 红队视角**：
  2 人团队最大风险：一个工程师改 fanout Lambda 代码，发版 5 分钟后发现 bug——但 Lambda 已经全量切换，所有新通知都走了坏版本。回滚靠 git revert + 重新部署，期间 5 分钟通知全部进 DLQ 或丢失。没有 canary、没有 traffic shifting、没有 automatic rollback。一周一次发版，3 个月内至少会有 2-3 次"晚上加班回滚"事件。

- **🟩 建设性视角**：
  ①Lambda 用 alias + weighted traffic shifting（CodeDeploy 集成），canary 10% → 50% → 100%，每阶段配 CloudWatch alarm 触发自动回滚；②DynamoDB schema 变更走"expand → migrate → contract"模式，绝不破坏性变更；③基础设施全部 Terraform/SAM IaC，git 管控；④CI/CD 流水线必须有压测 stage（即使简单 load test 也好）。

---

### 问题 #17：API Gateway 无 rate limiting 描述，外部刷量可直接撑爆账单

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（反对者/竞争对手视角）
- **视角**：反对者/竞争对手 Adversary
- **原文引用**：

  > "mobile clients call API Gateway"

  —— 未提 usage plan、未提 throttling、未提 WAF rate-based rule

- **方法论依据**：AWS Well-Architected Security + Reliability + Red Team（出处：`references/technical-architecture-review.md` §4；`references/bias-checks.md` §5）。核心提问："威胁建模？攻击面？"

- **🟥 红队视角**：
  接 #5：即便加了 auth，单个被盗 token 仍可发 1000 QPS 攻击。SMS 每条 $0.0064，1 小时刷 1000 QPS = 360 万条 = $23000。如果攻击者用一个被盗账号持续刷一周，账单 7 位数。这是 serverless 系统的"经济学 DoS"——不需要打挂服务，只要打爆钱包。

- **🟩 建设性视角**：
  ①API Gateway usage plan：每 token 默认 10 RPS，1000 RPD；②per-user 业务限流（每天最多发 X 条通知）在写 Lambda 里实现，用 DynamoDB 计数器；③WAF rate-based rule 在 IP 层兜底；④成本告警：单日 AWS 账单超阈值触发 SNS 通知 + Lambda 自动 disable SMS 通道。

---

### 问题 #18：DynamoDB 作为主表无 TTL / retention 策略，3 个月后存储成本失控

- **严重等级**：🟠 High
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "a Lambda function writes the notification to DynamoDB"

  —— 未提 TTL、未提归档、未提冷热分层

- **方法论依据**：AWS Well-Archetected Cost Optimization + Reliability（出处：`references/technical-architecture-review.md` §4）。核心提问："单位经济？长期成本？容量规划？"

- **🟥 红队视角**：
  10M 通知/天 × 365 天 = 36.5 亿行/年。DynamoDB 按存储计费，假设每行 1KB，年增 3.6TB——年成本数千美元。3 年后是 10TB+，每次查询都贵。如果通知包含 payload（消息正文），单行可能 5-10KB，成本 × 10。

- **🟩 建设性视角**：
  ①DynamoDB 表开 **TTL**（如 90 天），过期自动删除；②超长保留的归档走 DynamoDB → S3（用 DynamoDB Streams + Lambda 同步到 S3 + Athena 查询）；③字段分层：热数据（status / sent_at）留主表，冷数据（payload / 内容）拆到 S3 引用。

---

### 问题 #19：未提及 FIFO vs Standard SQS 选择，影响顺序性与去重

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "SNS fans out to 3 SQS queues"

  —— 未说明 Standard 还是 FIFO

- **方法论依据**：ATAM + Cognitive Dimensions 的 Premature Commitment（出处：`references/technical-architecture-review.md` §1 / §3）。核心提问："被迫在信息不足时做决定？质量属性目标？"

- **🟥 红队视角**：
  Standard SQS：best-effort 顺序 + 至少一次 + 偶尔重复。FIFO SQS：严格顺序 + exactly-once + 3000 QPS 上限。如果业务对"用户先收到 OTP 再收到 welcome"这种顺序敏感，Standard 会出问题。如果只是营销通知，Standard 完全够。方案没说通知类型，无法判断。

- **🟩 建设性视角**：
  在 PRD 里分类通知：transactional（OTP、订单确认）vs marketing（促销、周报）。Transactional 用 Standard + 应用层去重（`notification_id`）就够；除非真有"严格顺序"需求（罕见），否则不上 FIFO（吞吐受限且贵 10 倍）。

---

### 问题 #20：3 个 consumer Lambda 共享 account-level 并发池，峰值会互相挤压

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "each queue has a dedicated Lambda consumer that calls the downstream service (FCM for push, email for SES, SMS for SNS)"

- **方法论依据**：ATAM 容量规划 + What If Analysis（出处：`references/technical-architecture-review.md` §1；`references/bias-checks.md` §6）。核心提问："反事实：流量突增时各组件如何表现？"

- **🟥 红队视角**：
  10M/天峰值 1000+ QPS。3 个 consumer 同时拉取，瞬时并发可能各 200-500 instances，总并发 1500+。AWS 默认 account-level Lambda soft limit 是 1000，超了被 throttle，部分 invocation 进队列等。SMS consumer 因下游慢导致 backlog，把 account quota 占满，把 push consumer 也拖死——**单一通道问题级联到所有通道**。

- **🟩 建设性视角**：
  ①给每个 consumer Lambda 设 **reserved concurrency**（如 push: 600, email: 300, sms: 100），互不抢占；②在 ADR 里写明峰值并发预算；③监控 3 个 consumer 的 concurrency utilization，触发告警时申请 quota 提升。

---

### 问题 #21：无压测 / 故障注入计划，"3 个月上线"未预留验证时间

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "we have 3 months to get to production"

  —— 未提压测、未提 chaos engineering、未提负荷测试时间表

- **方法论依据**：AWS Well-Architected Operational Excellence + Reliability + Pre-mortem（出处：`references/technical-architecture-review.md` §4；`references/bias-checks.md` §1）。核心提问："测试策略覆盖关键路径？"

- **🟥 红队视角**：
  没有 10M/天的真实负荷测试，"3 个月上线"意味着上线当天才是第一次全量压测——可能直接打挂。Lambda concurrency / DynamoDB WCU / SQS throughput / FCM rate limit 都没有实战数据。

- **🟩 建设性视角**：
  时间表里强制留 3-4 周做：①负荷测试（Artillery / k6 / Locust 模拟 1000 QPS 持续 1h）；②chaos 实验（手动 kill 一个 consumer Lambda、inject 50% FCM 5xx、断 SQS）；③soak test（24-72h 持续中等流量看内存泄漏 / DynamoDB hot partition）。

---

### 问题 #22：未提及通知内容模板系统，多通道文案变更会非常痛

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（用户/客户视角）
- **视角**：用户/客户 User
- **原文引用**：

  全文未提及模板、本地化、A/B 测试。

- **方法论依据**：Paul-Elder 的 Implications + Cognitive Dimensions 的 Viscosity（出处：`references/methodology-foundations.md` §1；`references/technical-architecture-review.md` §3）。核心提问："二阶效应？文案改动成本？"

- **🟥 红队视角**：
  营销文案每周改，多语言、多通道、A/B 变体——如果模板硬编码在 Lambda，每次改都要发版 + 走 canary，2 工程师被运营需求淹没。如果不同通道文案不同（push 90 字、email HTML、SMS 160 字符），三套模板要同步改，错一个就出事故。

- **🟩 建设性视角**：
  ①模板存 DynamoDB 单独表或 S3 + 版本号；②用 Liquid / Handlebars / Jinja 模板引擎；③建 admin API 让运营自助改模板；④按 channel + locale + variant 维度组织；⑤PRD 里区分 system 模板（开发改）和 marketing 模板（运营改）。

---

### 问题 #23：未定义"投递成功"的口径，业务报表会无法对账

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（决策者/投资人视角）
- **视角**：决策者/投资人 Decision-maker
- **原文引用**：

  全文未定义"成功"——是 Lambda 调用成功？还是 downstream API 返回 200？还是用户真的收到？

- **方法论依据**：Paul-Elder 的 Concepts + Precision（出处：`references/methodology-foundations.md` §1）。核心提问："定义一致？精度够？"

- **🟥 红队视角**：
  业务方问"昨天通知成功率多少？"——如果只看 Lambda error rate = 0%，回答"100% 成功"，但实际 FCM 返回 `UNREGISTERED`（设备已卸载）占 15%、SES 进入 spam folder 占 10%、SMS 运营商吞掉占 5%。**业务定义的成功 ≠ Lambda 调用成功**。报表口径不对，所有决策（用户活跃度、营销 ROI）都失真。

- **🟩 建设性视角**：
  定义 4 个状态：`DELIVERED_TO_VENDOR`（downstream 200）/ `DELIVERED_TO_DEVICE`（FCM delivery receipt）/ `OPENED`（push 回传打开事件）/ `FAILED`。每个 channel 定义不同"成功"：push 看 delivered，email 看 SES delivery + open，SMS 看 carrier delivery receipt。

---

### 问题 #24：移动客户端调用方角色不清——是发通知还是收通知？

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 1 PARSE（Paul-Elder：Question at issue）
- **视角**：用户/客户 User
- **原文引用**：

  > "mobile clients call API Gateway → a Lambda function writes the notification to DynamoDB"

  —— 这句话本身有歧义：mobile client 是"发起通知"还是"触发被通知的事件"？

- **方法论依据**：Paul-Elder 的 Clarity / Question at issue（出处：`references/methodology-foundations.md` §1）。核心提问："核心问题被显式提出？表述清晰？"

- **🟥 红队视角**：
  通常 notification 系统的调用方是**后端业务服务**（订单服务通知"已发货"），而不是 mobile client 自己。如果是 mobile client 调 API Gateway 写通知，那含义是"用户 A 给用户 B 发消息"——那是 IM/聊天系统，不是 notification 系统。两种系统的安全模型、限流策略、合规要求完全不同。这份方案没说清，可能整个安全设计都建立在错误前提上。

- **🟩 建设性视角**：
  在 PRD 第一节明确：调用方 = 后端业务服务（B2B）vs mobile client（B2C 用户对用户）。安全模型、限流、auth 完全不同。最常见场景：mobile client 不直连 notification 服务，而是通过业务 API 间接触发。

---

### 问题 #25：未提及团队 on-call / incident response 流程

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（维护者视角）
- **视角**：维护者 Maintainer
- **原文引用**：

  全文未提 on-call、未提 incident runbook、未提 PagerDuty / Opsgenie。

- **方法论依据**：AWS Well-Architected Operational Excellence（出处：`references/technical-architecture-review.md` §4）。核心提问："runbook？事件响应流程？"

- **🟥 红队视角**：
  2 工程师 + 系统每天 10M 流量，意味着每天至少几次"小事故"。没有 on-call 轮换，意味着两个工程师 7×24 都要接电话——3 个月内必出 burnout。事故发生时没有 runbook，靠脑子记步骤——凌晨 3 点脑子不在线。

- **🟩 建设性视角**：
  ①写 5 个最常见 incident 的 runbook（DLQ 堆积、FCM 限流、DynamoDB throttle、Lambda error spike、SMS 失败率高）；②配 PagerDuty / Opsgenie，告警自动 routing；③2 人轮 on-call，每周轮换；④上线前做一次桌面演练（tabletop exercise）。

---

### 问题 #26：未提及 provisioned WCU/RCU 或 on-demand 容量模式选择

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  > "Lambda function writes the notification to DynamoDB"

  —— 未说明 on-demand vs provisioned、未提 partition key 设计

- **方法论依据**：ATAM 容量规划 + AWS Well-Architected Performance Efficiency（出处：`references/technical-architecture-review.md` §1 / §4）。核心提问："容量规划？瓶颈识别？"

- **🟥 红队视角**：
  10M 写/天 + Streams 读 + 5 个 Lambda 读取状态字段 = 高读写比。如果 partition key 设计不当（如用 `date` 做分区），10M 写集中在少数 partition → hot partition → throttle。容量模式选错（provisioned 但峰值预估错 / on-demand 但稳态成本高）。

- **🟩 建设性视角**：
  ①partition key 用高基数（`notification_id`），避免热点；②初期用 on-demand 容量模式（避免 provisioned 估算错），稳定后切 provisioned 省成本；③GSI 设计谨慎（每个 GSI 都是写入放大）。

---

### 问题 #27：未提及 Lambda 函数大小 / 部署包优化，cold start 会放大

- **严重等级**：🟡 Medium
- **发现阶段**：Stage 2 PERSPECTIVES（实现者视角）
- **视角**：实现者 Implementer
- **原文引用**：

  5 个 Lambda 函数，未提 dependency 优化、未提 layer 共享。

- **方法论依据**：ATAM 性能 + Cognitive Dimensions 的 Viscosity（出处：`references/technical-architecture-review.md` §1 / §3）。核心提问："性能瓶颈？变更成本？"

- **🟥 红队视角**：
  5 个 Lambda 各自打包 AWS SDK + HTTP client + JSON 库，部署包可能 10-50MB，cold start 加剧。共用代码（auth、logging、idempotency）复制 5 份，bug 修一处要发版 5 次。

- **🟩 建设性视角**：
  ①公共代码（logging / tracing / idempotency / retry）抽 Lambda Layer 共享；②AWS SDK 用 modular import（只引需要的 service）；③监控每个 Lambda 的 cold start 占比，超 10% 启用 provisioned concurrency。

---

### 问题 #28：术语描述含混，多处需要读者脑补

- **严重等级**：🟢 Low
- **发现阶段**：Stage 1 PARSE（Paul-Elder：Clarity）
- **视角**：维护者 Maintainer
- **原文引用**：

  > "SNS fans out to 3 SQS queues (one per channel: push, email, SMS)"

  —— "channel" 一词指代 notification channel（push/email/sms）还是 SQS 通道？读者要脑补。

- **方法论依据**：Diátaxis 文档分类学 + Cognitive Dimensions 的 Role-Expressiveness（出处：`references/methodology-foundations.md` §6；`references/technical-architecture-review.md` §3）。核心提问："类别对吗？每部分目的可见？"

- **🟥 红队视角**：
  没有 architecture diagram、没有数据流图、没有 sequence diagram，全靠文字描述。新工程师入职第一天看完只懂 70%，剩下 30% 靠问。

- **🟩 建设性视角**：
  ①画一张 architecture diagram（draw.io / Excalidraw），AWS 服务用官方 icon；②每个组件标注 input/output 数据契约（什么触发它、它输出什么）；③加一段 sequence diagram 描述典型 notification 从入口到投递的完整路径。

---

### 问题 #29："serverless because we don't want to manage servers" 是无效论证

- **严重等级**：🟢 Low
- **发现阶段**：Stage 3 ARGUMENTS（Toulmin：Warrant 弱）
- **视角**：决策者/投资人 Decision-maker
- **原文引用**：

  > "We chose serverless because we don't want to manage servers."

- **方法论依据**：Toulmin 论证拆解 + Walton 成本-收益型 critical questions（出处：`references/methodology-foundations.md` §3 / §4）。核心提问："是否漏算隐性成本？机会成本考虑？"

- **🟥 红队视角**：
  Serverless ≠ 不运维。你要运维：Lambda concurrency / DynamoDB capacity / SQS DLQ / IAM policy / CloudWatch alarm / SLO budget / X-Ray sampling / cost optimization / cold start / vendor API 限流。这些"serverless 运维"在某种程度上比 EC2 运维更难——因为很多内部不可观测。

- **🟩 建设性视角**：
  改成具体论证："serverless 让我们在 2 人团队规模下无需管理 OS patching / 容量预留 / 容器编排，把精力集中在业务逻辑——但代价是冷启动延迟 + vendor lock-in + 可观测性挑战，详见 ADR-001。"

---

## 结构化发现汇总

### Paul-Elder 8 要素覆盖

| 要素 | 文档是否充分处理 | 缺口说明 |
|---|---|---|
| Purpose 目的 | ⚠️ | "real-time notification system" 大方向清楚，但"实时"未量化、调用方角色未澄清 |
| Question at issue 关键问题 | ❌ | 核心问题（如何可靠投递多通道通知 + 如何知道投递成功）未显式提出 |
| Information 信息 | ❌ | 只给 10M/天 + 2 人 + 3 月三个数；缺 latency SLO、failure rate target、cost budget、channel 比例、通知类型分布 |
| Inference 推断 | ❌ | 从"想要通知系统"到"这条链路"中间推理完全缺省；每个组件选择都无 warrant |
| Assumption 假设 | ❌ | 大量隐含假设（idempotency、retry、DLQ、auth、compliance、cost ceiling）全部缺席 |
| Concepts 概念 | ⚠️ | "real-time" "SNS" "channel" 等核心术语定义不清或冲突 |
| Implications 含义 | ❌ | 完全未讨论二阶效应（成本爆炸、合规风险、on-call 烧人） |
| Point of view 视角 | ❌ | 只有 builder 视角；SRE / 安全 / 法务 / 业务方 / 用户视角全部缺席 |

### 5 视角覆盖

| 视角 | 关键发现 | 最高严重等级 |
|---|---|---|
| 实现者 Implementer | 无 ADR、无 alternatives、无幂等、无 DLQ、无冷启动方案、无压测计划 | 🔴 Critical（#1, #10, #21） |
| 维护者 Maintainer | 监控缺失、无 tracing、无部署策略、DynamoDB Streams 24h 数据丢失风险、无 on-call | 🔴 Critical（#2, #6, #11, #12） |
| 用户/客户 User | 无 SLA、无合规退订、无模板系统、调用方角色歧义 | 🔴 Critical（#4, #14, #22, #24） |
| 反对者/竞争对手 Adversary | 无 auth、无限流、无 DR、可被经济学 DoS、SNS SMS 服务弱化 | 🔴 Critical（#5, #13, #15, #17） |
| 决策者/投资人 Decision-maker | 2 人×3 月严重错配、无成本估算、无 kill criteria、serverless 论证薄弱 | 🔴 Critical（#3, #8, #9, #29） |

### 核心论证的 Toulmin 拆解

#### 论证 #1：Serverless 是合理选型

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | "We chose serverless" | ⚠️ 清晰但无 backing |
| Data 数据 | "we don't want to manage servers" | ❌ 单一动机，非数据；无团队规模/技能矩阵/预算约束支撑 |
| Warrant 推理依据 | "不想管服务器 → serverless 是唯一选择" | ❌ 隐含且错误——ECS Fargate、App Runner、Cloud Run 都不用管服务器 |
| Backing 支撑 | 无 | ❌ 完全缺失 |
| Qualifier 限定词 | 无 | ❌ 绝对化选择，无 trade-off 承认 |
| Rebuttal 反例 | 无 | ❌ 完全未承认冷启动、vendor lock-in、可观测性挑战等反例 |

**Walton critical questions**（成本-收益型论证）：
- "是否漏算隐性成本？"——是：可观测性工具、cold start provisioned concurrency、DynamoDB on-demand 溢价、SMS vendor 成本都未算（**文档未回答**）
- "机会成本？"——未列 ECS Fargate、Kinesis、EventBridge 等替代（**文档未回答**）

#### 论证 #2：DynamoDB Streams → Lambda → SNS → SQS 链路是合理的 fan-out 设计

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | "这条 5 跳链路实现通知 fan-out" | ⚠️ 描述属实但无理由 |
| Data 数据 | （链路描述本身） | ⚠️ 只有结构描述，无性能/成本/可靠性数据 |
| Warrant 推理依据 | "Streams + SNS + SQS = 解耦 + 可扩展"（隐含） | ⚠️ Warrant 没被显式检验，且 SNS→SQS 一跳是否必要存疑 |
| Backing 支撑 | 无 | ❌ 无 throughput / latency / cost 对比 |
| Qualifier 限定词 | 无 | ❌ 没说"在 X 条件下才合理" |
| Rebuttal 反例 | 无 | ❌ 未承认 DynamoDB Streams 24h 限制、未承认 fanout Lambda 可省略 |

**Walton critical questions**（实践型论证）：
- "A 真能达成 G（解耦）？副作用？"——副作用：多 2 跳延迟 + 多 2 个 failure point，未承认（**文档未回答**）
- "更好的 B？"——EventBridge 原生 fan-out、SNS 直连 Lambda、DynamoDB Streams 直连 3 个 Lambda，都更短（**文档未回答**）

#### 论证 #3：CloudWatch default dashboards 足够监控

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | "我们不确定是否需要 CloudWatch default 之外的东西" | ❌ 把无知当结论 |
| Data 数据 | 无 | ❌ 完全无依据 |
| Warrant 推理依据 | "default dashboards 应该够"（隐含） | ❌ 没检验过 default 包含什么 |
| Backing 支撑 | 无 | ❌ |
| Qualifier 限定词 | "Not sure if" | ⚠️ 至少承认不确定，但未推进到验证 |
| Rebuttal 反例 | 无 | ❌ |

**Walton critical questions**（专家意见型——这里连专家都算不上）：
- "default dashboard 真的覆盖分布式追踪 + 业务指标 + 告警吗？"——不覆盖（**文档未回答**）

#### 论证 #4：2 人团队 × 3 个月可交付 10M/天 production 系统

| 要素 | 内容 | 评审 |
|---|---|---|
| Claim 结论 | "we have 3 months to get to production" | ❌ 把约束当可达性论证 |
| Data 数据 | 2 人 + 3 月 + 10M/天 | ⚠️ 数据本身真实，但无 reference class 对照 |
| Warrant 推理依据 | "3 个月够"（隐含） | ❌ 无 backing |
| Backing 支撑 | 无 | ❌ 没列同类项目交付数据 |
| Qualifier 限定词 | 无 | ❌ 绝对化承诺 |
| Rebuttal 反例 | 无 | ❌ |

**Walton critical questions**（统计型 + 实践型）：
- "reference class 是什么？"——同类多通道 notification 系统行业经验 5-8 人 × 6-9 月（**文档未引用**）
- "为什么这次比 reference class 快 3 倍？"——未解释（**文档未回答**）

### 关键假设清单（Key Assumptions Check 产出）

| # | 假设 | 显式/隐含 | 概率 | 依据 | 失败退化路径 |
|---|---|---|---|---|---|
| 1 | Lambda + SQS + Streams 的至少一次投递不会造成用户可见的重复 | 隐含 | 低 | AWS 文档明确 at-least-once | 应用层 idempotency（方案未提） |
| 2 | 下游服务（FCM/SES/SMS）持续可用且不严重限流 | 隐含 | 中 | FCM/SES 历史可用性 99.5%+，但限流常见 | DLQ + 退避重试（方案未提） |
| 3 | DynamoDB Streams 在 24h 内必然被消费 | 隐含 | 中 | 取决于 fanout Lambda 健康度 | 主表 status 字段重放（方案未提） |
| 4 | AWS account Lambda 并发配额够 10M/天峰值 | 隐含 | 中 | 默认 1000，需提前申请提升 | reserved concurrency（方案未提） |
| 5 | 2 工程师可独立 on-call 10M/天系统而不 burnout | 隐含 | 低 | 行业经验：on-call 至少 3-4 人轮换 | 引入第 3-4 人或托管 SRE（方案未提） |
| 6 | AWS 账单在业务可承受范围 | 隐含 | 中 | SES/SMS 在 10M 规模月成本可达 6 位数美元 | 单位经济表 + 成本告警（方案未提） |
| 7 | 通知内容不违反 CAN-SPAM/TCPA/GDPR | 隐含 | 中 | 取决于业务类型和 consent 管理 | consent 管理 + suppression list（方案未提） |
| 8 | 单 region 部署足够，无 region 级故障风险 | 隐含 | 中 | AWS 历史 region 级故障每年 1-2 次 | 多 region 或主动接受 RTO 4h（方案未提） |
| 9 | CloudWatch default 够用 | 显式 | 低 | AWS 文档：default 仅聚合指标 | X-Ray + 业务指标 + 告警（方案未提） |
| 10 | 通知调用方是 mobile client 本身 | 隐含 | 低 | 通常 notification 调用方是后端服务 | 澄清调用方角色 + 重设安全模型（方案未提） |

### Pre-mortem 产出

> 假设方案已经上线并在 6 个月后失败。最可能的失败原因是什么？

| 失败原因 | 概率 | 文档是否已预防 | 改进建议 |
|---|---|---|---|
| 1. 短信/邮件账单爆炸，CFO 砍项目 | 高 | ❌ | 上线前单位经济表 + 成本硬上限告警 |
| 2. 重复通知导致用户投诉潮 / 集体诉讼 | 高 | ❌ | 应用层 idempotency 必做 |
| 3. SMS 合规违规（TCPA/CAN-SPAM）被监管罚款 | 中 | ❌ | consent 管理 + 法务 review + suppression list |
| 4. 一次发版引入 bug，全量通知发错内容 | 中 | ❌ | canary + 自动回滚 + 模板审批流程 |
| 5. 2 工程师 burnout / 离职，知识断层 | 高 | ❌ | 招第 3 人 / 招合同 SRE / 强制文档化 |
| 6. DLQ 堆积无人发现，静默丢失大量通知 | 高 | ❌ | DLQ 深度告警 + on-call runbook |
| 7. AWS 单 region 故障，业务方 SLA 违约 | 中 | ❌ | 多 region DR 或主动接受风险并 ADR |
| 8. 经济学 DoS——被盗 token 刷 SMS 把账单打到 7 位数 | 中 | ❌ | 多层限流 + 成本告警自动 disable SMS |
| 9. 监控盲区，silent failure 持续数周才被发现 | 高 | ❌ | 业务指标 + SLO 烧穿率告警 |
| 10. Lambda concurrency throttle 级联到所有通道 | 中 | ❌ | reserved concurrency per channel |

### ACH（竞争假设分析）

> 文档核心主张："serverless + 这条 5 跳链路是合理选型"。检验它。

| 证据 \ 假设 | 假设 A：文档主张（serverless 5 跳） | 假设 B：ECS Fargate + Kinesis + Worker | 假设 C：精简 serverless（去 SNS→SQS 一跳） |
|---|---|---|---|
| 团队规模 2 人 + 不想管 OS | 一致（serverless 真省 OS 运维） | 不一致（Fargate 仍需镜像/任务管理） | 一致（同样 serverless） |
| 10M/天峰值延迟敏感 | 不一致（5 跳 + cold start 难保证 P99） | 一致（Kinesis 低延迟 + 常驻 worker） | 一致（少 2 跳，延迟减半） |
| 多通道解耦需求 | 一致（SNS+SQS 解耦） | 一致（Kinesis + 多 consumer） | 一致（Streams + 多 Lambda consumer） |
| 可观测性需求 | 一致（serverless 工具链成熟） | 一致（同样有 X-Ray/CloudWatch） | 一致 |
| 单位经济 | 不一致（5 跳 × 5 个 Lambda invocation 成本叠加） | 一致（常驻 worker 摊薄成本） | 一致（少 2 跳省钱） |
| 2 人维护复杂度 | 不一致（5 跳 = 9 个组件要 debug） | 不一致（要管 Kinesis） | 一致（少 2 组件） |
| **诊断性** | 假设 A 在 4/6 维度不一致，B/C 都更一致 | — | — |

**结论**：文档只给了"支持性证据"（serverless 不用管 OS），完全没给"诊断性证据"（为什么 serverless 5 跳比 B/C 好）。按 ACH 方法，假设 A 不应被采纳——B 或 C 在多个维度更优。

---

## 评审者自评

### 本份评审**没有覆盖到**的方面

- **具体业务场景**：用户没说通知内容是什么（OTP？营销？交易？系统告警？），不同业务对 latency / compliance / cost 权重不同。本评审默认按"通用通知系统"批评，可能某些场景下某条 Critical 实际是 Low。
- **现有代码库 / 已有基础设施**：方案描述是 greenfield，但若团队已有 AWS 组织 / Datadog 账号 / Cognito pool，部分 High 问题（监控、auth）可能已半解决。
- **更细的 AWS 服务限额与 pricing**：本评审的数字（如 SMS $0.0064/条）是公开参考价，实际签约价、Volume Discount、AWS Activate credit 等可能显著不同。
- **团队技能背景**：2 人是否资深 AWS 工程师？是否有 prior 经验？若两人都是 AWS Hero 级别，部分 Pre-mortem 概率可能高估。
- **跨境/特定地区要求**：未深挖中国、欧盟、印度等地区的本地化合规（PIPL、当地 SMS carrier 等）。
- **替代架构的完整设计**：本评审指出问题多，但未给出完整的"修正版架构图"——这超出评审范围（评审 ≠ 重写）。

### 本份评审**存在偏倚**的可能来源

1. **可观测性偏重**：评审者（expert-reviewer skill）的训练数据中 SRE / DevOps 视角权重高，可能把可观测性问题评得过严。实际很多早期产品在没有完整监控下也活下来了。
2. **Pre-mortem 灾难化倾向**：Pre-mortem 方法本身会让人过度聚焦失败模式，可能低估"业务真的活了，监控后补"这条路径的可行性。
3. **大公司经验偏倚**：评审方法学（ATAM / ADR / Well-Architected）源自大组织实践，对 2 人早期团队的部分要求（完整 ADR / 多 region DR / formal on-call）可能过严——startup 阶段接受技术债是合理的。
4. **AWS 服务细节时效性**：SNS SMS vs End User Messaging SMS 的迁移状态、Lambda concurrency 默认值等，可能在 2026 年已有变化——评审者基于 2024-2025 知识。
5. ** confirmation bias**：评审者一旦在第一遍读出"7 个 Critical"，后续扫描可能过度寻找支持性证据，可能漏掉文档"其实做对了"的地方。

### 如果只能改一件事

> **先解决可观测性（#6）+ 幂等性（#1）+ DLQ（#2）三件最小事，再写一行业务代码。** 因为这三件决定了"系统能不能被信任"——监控不可信则无法判断其他问题严重程度；幂等性失败则用户体验崩塌；DLQ 缺失则失败不可恢复。其他 26 个问题可以在 3 个月窗口内分批处理，但这三件必须在 MVP 第一天就到位。

---

## 附录：评审使用的方法论清单

| 方法论 | 出处 references 文件 | 在本报告中使用的位置 |
|---|---|---|
| Paul-Elder 8 elements of thought | `references/methodology-foundations.md` §1 | Stage 1 PARSE、Paul-Elder 8 要素覆盖表 |
| Perspective-Based Reading | `references/methodology-foundations.md` §2 | Stage 2 PERSPECTIVES、5 视角覆盖表 |
| Toulmin argument model | `references/methodology-foundations.md` §3 | Stage 3 ARGUMENTS、4 个核心论证拆解、问题 #9 / #29 |
| Walton argumentation schemes | `references/methodology-foundations.md` §4 | Stage 3、Walton critical questions 在每个 Toulmin 拆解下 |
| Pre-mortem (Klein 2007) | `references/methodology-foundations.md` §5；`references/bias-checks.md` §1 | Stage 4、问题 #3、Pre-mortem 产出表 |
| Diátaxis 文档分类学 | `references/methodology-foundations.md` §6 | 问题 #28 |
| ATAM 场景驱动评审 | `references/technical-architecture-review.md` §1 | 问题 #4 / #10 / #13 / #19 / #20 / #26 / #27 |
| ADR 反向审计 | `references/technical-architecture-review.md` §2 | 问题 #1 / #9 / #15 |
| Cognitive Dimensions of Notations | `references/technical-architecture-review.md` §3 | 问题 #7 / #12 / #16 / #22 / #27 / #28 |
| AWS Well-Architected 6 支柱 | `references/technical-architecture-review.md` §4 | 问题 #1 / #2 / #5 / #6 / #8 / #11 / #13 / #14 / #16 / #17 / #18 / #21 / #25 / #26 |
| Pattern / Anti-pattern Catalogs | `references/technical-architecture-review.md` §5 | 问题 #1（Missing Idempotency 反模式） |
| SIFT Method | `references/source-evaluation.md` §1 | 问题 #15（Trace AWS 服务演进） |
| Lateral Reading | `references/source-evaluation.md` §2 | 问题 #15 |
| Key Assumptions Check (CIA SAT) | `references/bias-checks.md` §2 | Stage 4、关键假设清单 |
| Analysis of Competing Hypotheses | `references/bias-checks.md` §3 | Stage 4、ACH 表 |
| Devil's Advocacy | `references/bias-checks.md` §4 | 问题 #9 |
| Red Team Analysis | `references/bias-checks.md` §5 | 问题 #5 / #13 / #17 |
| What If Analysis | `references/bias-checks.md` §6 | 问题 #20 |
| Outside-In / Reference Class Forecasting | `references/bias-checks.md` §8 | 问题 #3 |
| Confirmation Bias Counters | `references/bias-checks.md` §10 | 评审者自评 |
