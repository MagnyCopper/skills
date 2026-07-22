# Transcript: expert-reviewer skill run

## Input

User requested a structured expert review of a short business plan intended for Sequoia:

> 公司：AIResume Inc.  
> 目的：用 AI 帮求职者优化简历  
> 问题：求职者写简历难、不知道怎么写才能过 ATS（Applicant Tracking System）  
> 解决方案：用户上传旧简历 + 目标岗位 JD，AI 生成定制化简历，自动匹配 ATS 关键词  
> 市场规模：全球求职市场巨大，每年有数亿求职者  
> 商业模式：SaaS 订阅，$19/月  
> 团队：我（CEO，前字节产品经理）+ 联创（CTO，前阿里工程师）  
> 融资：seeking $2M seed round at $10M cap  
> 我们预计 12 个月内达到 10 万付费用户，年化收入 $20M。

## Skill and reference files loaded

Loaded `/Users/han/Projects/skills/expert-reviewer/SKILL.md` in full.

Document type was detected as **业务/产品方案** because the input includes market, customer problem, solution, business model, team, financing, and financial forecast.

Per the skill routing and the user's explicit instruction, loaded these files:

1. `/Users/han/Projects/skills/expert-reviewer/references/business-product-review.md`
2. `/Users/han/Projects/skills/expert-reviewer/references/methodology-foundations.md`
3. `/Users/han/Projects/skills/expert-reviewer/references/source-evaluation.md`
4. `/Users/han/Projects/skills/expert-reviewer/references/bias-checks.md`
5. `/Users/han/Projects/skills/expert-reviewer/assets/templates/perspective-questions.md`
6. `/Users/han/Projects/skills/expert-reviewer/assets/templates/review-report-template.md`

## Workflow stages executed

### Stage 1 — PARSE

- Parsed the input as a short business/product plan, not a full deck.
- Applied Paul-Elder 8 elements:
  - Purpose: clear at idea level, incomplete as investor pitch.
  - Question at issue: implicit fundability and scalability.
  - Information: heavily missing.
  - Inference: major leap from broad market to 10 万付费用户 / $20M 年化收入.
  - Assumptions: many implicit assumptions around willingness to pay, ATS keyword effectiveness, churn, CAC, and competition.
  - Concepts: ATS, SaaS, ARR/annualized revenue; precision gaps found.
  - Implications: risks and second-order effects mostly absent.
  - Point of view: founder-heavy; missing investor, user, competitor, and compliance views.

### Stage 2 — PERSPECTIVES

Ran the default 5 stakeholder perspectives from `perspective-questions.md`:

1. Implementer: checked feasibility, LLM cost, architecture, data handling.
2. Maintainer: checked privacy, observability, model quality, long-term upkeep.
3. User/Customer: checked target segment, JTBD, pricing, churn, user validation.
4. Adversary/Competitor: checked direct competitors, ChatGPT substitutes, copyability, moat.
5. Decision-maker/Investor: checked ROI, CAC/LTV, Why Now, GTM, milestones, stop criteria.

Each perspective produced at least one positive assertion and a list of issues in the final report's 5-perspective summary.

### Stage 3 — ARGUMENTS

Used Toulmin + Walton critical questions on 4 core claims:

1. AIResume can reach 10 万付费用户 and $20M annualized revenue in 12 months.
2. ATS keyword matching is the core value users will pay for.
3. $19/month SaaS subscription is the right business model.
4. “全球求职市场巨大，每年有数亿求职者” supports a large opportunity.

Main decision: treated these as business claims requiring backing, not as facts. Because the source text gives no external citations, SIFT was used to flag missing provenance rather than to perform live external fact-checking.

### Stage 4 — DECISIONS

Applied:

- Pre-mortem: identified likely failure modes, including ChatGPT substitution, CAC, churn, privacy, and weak outcome proof.
- Key Assumptions Check: listed 8 assumptions, including willingness to pay, growth feasibility, ATS matching effectiveness, LLM costs, and compliance.
- ACH: compared the document's optimistic growth hypothesis against competing hypotheses: demand exists but monetization is weak; or the correct model is not B2C SaaS.

### Stage 5 — REPORT

Wrote the final report to:

`/Users/han/Projects/skills/expert-reviewer-workspace/iteration-1/eval-business-plan-review-with-investor-lens/with_skill/outputs/review-report.md`

The report follows the required template sections:

- Metadata
- Overview and score
- Severity distribution
- Detailed issue list
- Paul-Elder summary
- 5-perspective summary
- Toulmin decomposition
- Key assumptions
- Pre-mortem
- ACH
- Reviewer self-assessment
- Methodology appendix

## Scope and emphasis decisions

- Emphasis was set to **investor lens / Sequoia pitch readiness**, because the user said the plan is intended for Sequoia.
- No external live web research was performed. The skill required SIFT-style source evaluation; the input had no citations, so the review flags absence of sources and reference-class backing instead of verifying every market claim externally.
- Competitor examples were used to stress-test the missing competition section, but the report explicitly states that current competitor features/pricing were not live-verified.
- The output focuses on critique and revision direction, not rewriting the pitch deck, because the task was “审一下” rather than “重写”.
- Dual-perspective output was included for every issue: red team + constructive.
- Three-evidence rule was followed for every issue: original quote, methodology basis, and severity level.
