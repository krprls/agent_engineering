# Class 02A Submission

## Student
- Name: AI Agent Engineer
- GitHub: https://github.com/krprls/agent_engineering
- Branch / commit: main

---

# Baseline observations

## L1
At L1, the agent receives only the skill name (`renewal-advisor`) and description from the `SKILL.md` YAML frontmatter. Prior to engineering, the description was a generic placeholder string, which indicated that a skill existed but provided zero domain guidance or boundary definitions for routing decisions.

## L2
Before completing `SKILL.md`, all L2 instruction sections contained unfinished placeholder markers. As a result:
1. The agent lacked systematic procedures for progressive disclosure and selective resource loading.
2. The agent had no explicit references to exact L3 file paths (`references/discount-policy.md`, etc.), leading to path guessing or ungrounded answers.
3. No citation rules or strict status state terminology (**requested**, **routed**, **approved**) were enforced.
4. The agent lacked clear safety refusal boundaries for unsupported compliance questions.

## L3
Without explicit L2 resource routing instructions, the agent either failed to load the necessary L3 references or loaded extraneous files. Selective disclosure requires L2 to map intent directly to exact L3 file paths so that only the minimal required evidence or script is loaded into context.

---

# Final trace evidence

## Case A
- Predicted L3: `references/discount-policy.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `references/discount-policy.md`
- Final result: Identified >10%-15% discount band requiring VP Sales & Finance Business Partner approval. Cited `[Source: references/discount-policy.md]`.
- Unnecessary resources loaded: None (`references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, and `scripts/calculate_quote.py` were correctly avoided).

## Case B
- Predicted L3: `references/renewal-process.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `references/renewal-process.md`
- Final result: Matched 75-day window to 90-61 day timeline requiring internal account review to identify churn risks and commercial constraints. Cited `[Source: references/renewal-process.md]`.
- Unnecessary resources loaded: None (`references/discount-policy.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, and `scripts/calculate_quote.py` were correctly avoided).

## Case C
- Predicted L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Final result: Cross-resource routing: 18% discount -> CRO & Finance Director; 10 days & high churn -> Executive sponsor & Renewal Desk; Regulated & auto-renewal removal -> Legal & Security.
- Unnecessary resources loaded: None (`assets/renewal-brief-template.md` and `scripts/calculate_quote.py` were correctly avoided).

## Case D
- Predicted L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Final result: Populated official renewal brief template accurately using policy rules. Maintained clear status labels (**requested**, **routed**).
- Unnecessary resources loaded: None (`scripts/calculate_quote.py` avoided since dollar math was not explicitly requested).

## Case E
- Predicted L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Final result: Executed `calculate_quote.py --arr 92000 --discount-percent 12` returning `$11,040.00` discount and `$80,960.00` net ARR; identified VP Sales & Finance BP approval.
- Unnecessary resources loaded: None (`references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md` were correctly avoided).

## Case F
- Predicted L3: `references/risk-escalation.md`
- Observed L1: `renewal-advisor`: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
- Observed L2: `SKILL.md` loaded successfully.
- Observed L3: `references/risk-escalation.md`
- Final result: Recognized request as unsupported by policy sources; refused to invent SOC 2 control ID or 24-hr recovery promise; routed to Legal & Service Reliability.
- Unnecessary resources loaded: None (`references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` were correctly avoided).

---

# What I learned

## Skill vs resource
A **skill** (defined in `SKILL.md`) is a reusable package of domain-specific instructions, procedures, workflow rules, and resource maps that teaches the agent how to analyze queries and locate policy evidence. A **resource** (such as files in `references/`, `assets/`, or `scripts/`) contains the ground-truth detailed facts or executable code loaded dynamically by the skill only when required.

## L1 → L2 → L3 progressive disclosure
Progressive disclosure structures information into three tiers:
1. **L1 Metadata**: Compact YAML frontmatter loaded into prompt context for initial skill discovery.
2. **L2 Instructions**: Detailed procedure and resource routing map loaded when the skill is selected.
3. **L3 Resources**: Target evidence files or executable scripts loaded on-demand for specific questions.

## Why minimum-resource loading matters
Loading only the minimum necessary L3 files keeps the model's context window clean and focused, reduces token consumption and API cost, speeds up model inference, and eliminates hallucinations or interference caused by irrelevant policy rules.

## Why deterministic math belongs in a script
LLMs perform arithmetic probabilistically and can make calculation errors on complex monetary amounts. Offloading financial math to a deterministic Python script (`calculate_quote.py`) guarantees 100% precision and auditability.

## Why safe abstention can be a correct answer
When queried for facts outside the provided policies (such as ungrounded SOC 2 control IDs or 24-hour RTO guarantees), refusing to hallucinate and correctly routing the query to human authorities (Legal, Security, Reliability) preserves system safety, trust, and compliance integrity.
