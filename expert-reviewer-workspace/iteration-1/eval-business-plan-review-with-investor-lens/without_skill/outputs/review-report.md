# Sequoia BP Review — AIResume Inc.

**Reviewer lens**: Late-stage seed investor applying Sequoia-style diligence.
**Verdict**: Pass as written. Salvageable with a near-total rewrite. Do not send this version.

---

## Executive Summary

The plan combines a real problem with a commodity solution, an undefended competitive position, and a 12-month projection that is off by 1–2 orders of magnitude. The $2M ask at a $10M cap is internally inconsistent with both the team size and the year-1 revenue claim. A Sequoia partner would pass within five minutes — most likely on the $20M ARR line alone, before any of the deeper issues surface.

This is a real market with real pain, but as presented it is a GPT wrapper with no moat, no traction, no GTM, and a team without a clear unfair advantage.

---

## Critical Issues

### 1. The financial projection is not credible

**Claim**: 100K paying users and $20M ARR within 12 months.

**Math check**: $20M ARR ÷ ($19 × 12) ≈ 87,720 paying subscribers held all year. The arithmetic is internally consistent. The problem is the assumption set behind it.

To reach 100K paying users in 12 months from a 2-person, $2M team you need one or more of:

- **2–5M free signups** assuming best-in-class 2–5% free-to-paid conversion. In B2C SaaS this is a Year-3 outcome, not Year-1.
- **$3–5M+ in paid acquisition spend** — more than the entire raise, before payroll, infra, or AI API costs.
- **A sustained viral coefficient K > 1 for 12 months**, which is implausible for utilitarian document-generation SaaS.

**Reference points**: Rezi took ~4 years to cross 100K cumulative users (free + paid). Jobscan took 5+ years. Teal has been operating since 2019 and is estimated at well under $10M ARR. A $20M ARR Year-1 target in this category is not aspirational — it is a credibility-killing error.

**Required fix**: Provide a month-by-month funnel (signups → activations → paid), assumed free-to-paid conversion rate, CAC by channel, and gross margin net of LLM API costs. A credible Year-1 target is **$500K–$2M ARR**.

---

### 2. Zero defensible moat

The product as described is one prompt: *"Rewrite this resume for this JD, optimized for ATS keywords."* The characteristics:

- Buildable by a competent engineer in a weekend.
- No proprietary training data.
- No network effects.
- No switching costs (users leave the moment they have a resume they like — which is the entire point of the product).
- No exclusive distribution.

**Direct competitors already shipping**: Teal, Rezi, Jobscan, Resume Worded, Kickresume, Simplify, Sonara, Grammarly's job tools, LinkedIn's native AI features, and — most dangerously — ChatGPT and Claude themselves, which already do this for $20/month and already have hundreds of millions of paying users.

**Required fix**: Articulate the moat explicitly. The only viable paths are: (a) deep workflow integration with a specific buyer segment you can own, (b) a proprietary data flywheel where usage improves outcomes measurably, or (c) B2B distribution (universities, bootcamps, outplacement firms, RTO providers). None of these appear in the current plan.

---

### 3. Top-down TAM is a red flag

*"Global job seekers, hundreds of millions annually"* is not a market size — it is a population statistic. Sequoia (and any serious VC) wants three numbers:

- **TAM**: total addressable, realistically defined.
- **SAM**: the slice you can actually serve in 3 years given geography, language, and willingness to pay.
- **SOM**: the slice you can plausibly capture in 12–18 months given your channel, team, and budget.

**Credible SOM example**: *"300K new US/UK English-speaking tech-job seekers per year who already pay for ≥1 job-search tool. We target 5% in Year 1 = 15K paying users ≈ $3.4M ARR."*

**Required fix**: Replace population statistics with a bottom-up SOM grounded in a specific geography, segment, and willingness-to-pay assumption.

---

### 4. Unit economics don't work in B2C job-seeker SaaS

This is the single most underestimated problem in the category:

- **Retention**: Average user churns in 2–4 months (they get a job — your success = your churn).
- **LTV at $19/mo × 3 months ≈ $57** before any CAC.
- **CAC in B2C SaaS**: typically $30–$80 for qualified traffic.
- **Gross margin after LLM API costs**: 60–70% at best (each resume generation is token-intensive).

This is structurally LTV/CAC-negative unless retention is fixed or the model shifts.

**Required fix**: Show the LTV/CAC math explicitly. Address retention head-on. The most credible pivots are: (a) reposition as a recurring career-management subscription (not a one-shot resume tool), or (b) move upmarket to B2B where annual contracts solve the churn problem.

---

### 5. Geographic and segment confusion

- Founders are ex-ByteDance and ex-Alibaba → implies China context.
- ATS as a filtering mechanism is primarily a **US/Western** concept; Chinese recruiting platforms (Boss直聘, 拉勾, 猎聘) filter on different signals.
- $19/month is a US/EU price point, not a Chinese consumer price point (Chinese consumers expect ¥9.9–¥29 one-time).
- No beachhead is named.

**Required fix**: Pick one beachhead and own it. *"Global from day one"* in a seed pitch translates to *"winning nowhere."*

---

### 6. Team lacks the unfair advantage Sequoia funds

Ex-ByteDance PM + ex-Alibaba engineer is, in 2026, an extremely common founder profile. Sequoia-backed seed founders typically have at least one of:

- **Deep domain expertise** — years inside recruiting, HR tech, or an ATS vendor.
- **A prior exit or scaling experience** with metrics attached.
- **A unique distribution advantage** — existing audience, partnerships, or owned channel.
- **Technical depth that creates a real moat** (proprietary data pipelines, evaluation infra, model work).

The plan provides no metrics from prior roles, no domain credentials, and no stated unfair advantage.

**Required fix**: Either (a) add a third founder with HR-tech / recruiting domain depth, or (b) demonstrate 6–12 months of proprietary customer insight you've gathered that competitors lack. "We built a v0 and talked to 100 users" would be a start; that work is not visible in the plan.

---

### 7. Round structure mismatches Sequoia's actual behavior

- **$2M is below Sequoia's typical seed check** (currently $3–5M+, often more for category leads).
- **$10M cap** on no revenue, no traction, no team depth is aggressive for the 2026 market — comparable profiles are clearing $5–8M cap post-correction.
- Sequoia has largely avoided two-person B2C LLM-wrapper seeds in the current cycle; their recent consumer AI bets favor founders with prior traction, owned distribution, or unique technical depth.

**Required fix**: If Sequoia is the genuine target, you need either (a) 6 months of explosive organic-growth traction, or (b) a more appropriate investor profile: pre-seed funds, operating angels, or HR-tech specialists (Reach Capital, GSV, Owl Ventures, Rethink).

---

## What's salvageable

The plan gets a few things right:

- **The problem is real and persistent** — ATS optimization is genuinely painful, well-documented, and durable.
- **The $19/month price point** is appropriate for the category and matches incumbent behavior.
- **SaaS subscription** is the right model (one-time purchases are worse).
- **A two-person technical founding team** can ship a credible v1.

These do not save the deal as presented, but they suggest a viable seed-stage company at a lower valuation with much more realistic milestones.

---

## Recommendation

**Do not send this version to Sequoia.** The $20M ARR claim is a 60-second filter-out, and the absence of any competitive or moat analysis ends the meeting if one happens.

Before sending, the plan must include:

1. **Bottom-up SOM** for a specific beachhead segment (geography + buyer + WTP).
2. **12-month plan with realistic targets**: 5–15K paying users, $1–3M ARR, with month-by-month funnel assumptions.
3. **Explicit competitive map** (Teal, Rezi, Jobscan, Resume Worded, LinkedIn, ChatGPT) and a stated defensibility thesis.
4. **LTV/CAC and retention** assumptions with sensitivity ranges.
5. **GTM channel** named and defended — organic SEO, TikTok/Reels, university partnerships, B2B pilots, etc.
6. **Why you** — the specific insight, distribution edge, or domain depth no one else has.
7. **Use of funds** breakdown: payroll, infra/API, GTM, runway to next round.

If you cannot answer #3 and #6 convincingly, this is **not a venture-backable business** at this stage. It may still be a profitable bootstrapped tool — that is a legitimate path, just not the path you're pitching.

---

## One-line summary for the founder

Real problem, commodity solution, no moat, no traction, projections off by ~10–20× — rewrite from scratch with bottom-up numbers, a named competitor, a defensible thesis, and honest unit economics before this goes to any tier-1 VC.
