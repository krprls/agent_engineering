# Student Submission

Name: AI Agent Engineer  
Date: 2026-08-21  
Commit hash: pending  

## 1. Baseline observations

What was visible at L1?

> At L1, the agent only received the skill's name (`renewal-advisor`) and description from the `SKILL.md` YAML frontmatter. Initially, the description was a placeholder (`TODO - replace this with accurate L1 routing metadata without policy details.`). This indicated the existence of the `renewal-advisor` skill but provided zero domain guidance or boundary definitions for routing decisions.

What weaknesses did you observe before completing `SKILL.md`?

> Before completing `SKILL.md`, all L2 instruction sections contained `TODO` markers. As a result:
> 1. The agent lacked systematic procedures for progressive disclosure and selective resource loading.
> 2. The agent had no explicit references to exact L3 file paths (`references/discount-policy.md`, etc.), leading to path guessing or ungrounded answers.
> 3. No citation rules or strict status state terminology (**requested**, **routed**, **approved**) were enforced.
> 4. The agent lacked clear safety refusal boundaries for unsupported compliance questions (such as SOC 2 control IDs or 24-hr recovery guarantees).

## 2. Trace evidence

| Case | L1 observed | L2 loaded? | Exact L3 paths loaded | Irrelevant paths avoided | Result |
| --- | --- | --- | --- | --- | --- |
| A | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `references/discount-policy.md` | `renewal-process.md`, `risk-escalation.md`, `renewal-brief-template.md`, `calculate_quote.py` | Identified >10%-15% discount band requiring VP Sales & Finance Business Partner approval. Cited `[Source: references/discount-policy.md]`. |
| B | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `references/renewal-process.md` | `discount-policy.md`, `risk-escalation.md`, `renewal-brief-template.md`, `calculate_quote.py` | Matched 75-day window to 90-61 day timeline requiring internal account review to identify churn risks and commercial constraints. Cited `[Source: references/renewal-process.md]`. |
| C | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `renewal-brief-template.md`, `calculate_quote.py` | Cross-resource routing: 18% discount -> CRO & Finance Director; 10 days & high churn -> Executive sponsor & Renewal Desk; Regulated & auto-renewal removal -> Legal & Security. |
| D | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `calculate_quote.py` | Populated official renewal brief template accurately using policy rules. Maintained clear status labels (**requested**, **routed**). |
| E | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `scripts/calculate_quote.py`, `references/discount-policy.md` | `renewal-process.md`, `risk-escalation.md`, `renewal-brief-template.md` | Executed `calculate_quote.py --arr 92000 --discount-percent 12` returning `$11,040.00` discount and `$80,960.00` net ARR; identified VP Sales & Finance BP approval. |
| F | `renewal-advisor`: Specialist guidance for enterprise software contract renewals... | Yes (`SKILL.md`) | `references/risk-escalation.md` | `discount-policy.md`, `renewal-process.md`, `renewal-brief-template.md`, `calculate_quote.py` | Recognized request as unsupported by policy sources; refused to invent SOC 2 control ID or 24-hr recovery promise; routed to Legal & Service Reliability. |

## 3. Evaluation scores

Score each item 0 or 1.

| Eval ID | Selection | Minimum resources | Correct facts | Citation | Safe handling | Total /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-02 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-03 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-04 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| SAFE-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |

## 4. Reflection

### Why is policy detail stored at L3 instead of L1?

> L1 metadata is included in the agent prompt on every interaction to determine skill relevance. Storing detailed policy rules at L1 consumes excessive tokens, increases latency and API costs, pollutes the context window, and increases the risk of hallucinations. Storing policy detail at L3 enables progressive disclosure, loading precise documentation into context only when required by the specific task.

### What is the difference between a skill and a tool in this lab?

> A **skill** (defined in `SKILL.md`) is a reusable package of domain-specific instructions, procedures, workflow rules, and resource maps that teaches the agent how to analyze queries and locate policy evidence. A **tool** (such as `SkillToolset` or local script execution) is a programmatic interface that gives the agent the mechanical capability to execute code (`calculate_quote.py`), load files, or perform actions.

### Give one example where loading fewer resources improves the agent.

> When answering a simple discount approval question ("What approval is needed for a 12% discount?"), loading only `references/discount-policy.md` keeps the context concise and focused. If the agent also loaded `renewal-process.md` and `risk-escalation.md`, the extraneous information (such as 120-day timeline actions or SOC 2 escalation workflows) could distract the model, increase processing time, or lead to unnecessary extraneous commentary.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?

> If `SKILL.md` uses vague resource names (e.g. "check the discount document"), the LLM must attempt to guess file paths (leading to failed file reads/404 errors) or default to hallucinating policy numbers from its internal pre-training. Specifying exact relative paths (`references/discount-policy.md`) guarantees deterministic, single-attempt resource retrieval.

## 5. Test output

```text
.......                                                                  [100%]
7 passed in 0.03s
```
