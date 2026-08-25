---
name: renewal-advisor
description: Specialist guidance for enterprise software contract renewals, discount approval routing, renewal process timing, risk escalations, official renewal briefs, and deterministic quote calculations. Excludes general technical product troubleshooting.
---

# Renewal Advisor

Provides policy-grounded guidance for enterprise software contract renewals, discount approvals, timeline milestones, risk escalations, official renewal briefs, and quote calculations.

## When to use

Use this skill when handling enterprise contract renewal requests, including:
- Determining required discount approval bands and designated approvers.
- Finding required actions based on renewal date timelines (days before renewal).
- Managing risk escalations for high churn risk accounts, regulated customers, or contract term changes (e.g., auto-renewal removal).
- Generating approval-ready renewal briefs using official templates.
- Performing deterministic quote arithmetic for dollar discounts and net ARR.

## When not to use

Do not use this skill for:
- General technical troubleshooting or software product defect support.
- Non-renewal sales inquiries or net-new customer contract creation.
- Answering questions about internal compliance frameworks or SOC 2 control IDs not contained in the supplied policy references.
- Making or approving ungrounded recovery time (RTO) or service-level promises not in signed contracts.

## Required inputs

To evaluate renewal requests accurately, gather the following input details:
- **Customer Name**: Name of the enterprise customer.
- **Renewal ARR**: Current Annual Recurring Revenue (USD).
- **Requested Discount**: Percentage discount requested (0%–100%).
- **Renewal Timing**: Days remaining until contract renewal date.
- **Churn Risk**: Risk classification (Low, Medium, High).
- **Special Terms / Requests**: Non-standard legal, compliance, or commercial requests (e.g., auto-renewal removal).

If required inputs for policy evaluation or calculation are missing, ask the user to provide them for missing input handling before proceeding.

## Procedure

1. **Inspect Request Inputs**: Check if the user prompt provides necessary details (ARR, discount %, timing, churn risk, special terms). Prompt the user if essential details are missing.
2. **Selective Resource Loading**: Apply minimum resource loading to determine the minimum L3 resource(s) required to answer the query:
   - For discount thresholds and approvers: load `references/discount-policy.md`.
   - For timeline actions and commercial rules: load `references/renewal-process.md`.
   - For risk escalation, regulated status, or auto-renewal removal: load `references/risk-escalation.md`.
   - For official brief generation: load `assets/renewal-brief-template.md` along with necessary policy references.
   - For net ARR and dollar discount calculations: execute `scripts/calculate_quote.py`.
3. **Execute Quote Calculator**: When requested to calculate net ARR or dollar discount, run `scripts/calculate_quote.py --arr <ARR> --discount-percent <DISCOUNT>` using local code execution. Never calculate discount math manually.
4. **Apply Policy & Status Rules**: Ground every conclusion in loaded L3 resources. Maintain strict status distinction using **requested**, **routed**, or **approved**. Never collapse "requested" or "routed" into "approved".
5. **Format Response & Citations**: Present a concise, structured response. Cite every policy rule using its exact relative file path, e.g., `[Source: references/discount-policy.md]`.
6. **Handle Unsupported Questions**: If an answer or control ID is not present in the supplied resources, state clearly that the provided sources do not support it for unsupported questions and provide the appropriate escalation route.

## Resource routing map

Map each query type to the exact minimum L3 resource path required:

| Query Type | L3 Resource Path |
| --- | --- |
| Discount approval bands & approvers | `references/discount-policy.md` |
| Renewal timeline & milestone actions | `references/renewal-process.md` |
| Churn risk, regulated terms, legal changes & unsupported questions | `references/risk-escalation.md` |
| Renewal brief formatting | `assets/renewal-brief-template.md` |
| Net ARR and dollar discount arithmetic | `scripts/calculate_quote.py` |

## Minimum-resource rule

Enforce minimum resource loading: load only the minimum L3 resources strictly required for the immediate query. Avoid loading unnecessary files. For single-topic questions (e.g., only discount approval), load only the corresponding single reference file.

## Output contract

- **Citations**: Append the relative path source citation `[Source: relative/path.md]` to cite all factual policy assertions.
- **Status Terminology**: Standardize status updates to **requested**, **routed**, or **approved**.
- **No Unapproved Commitments**: Do not describe any requested discount or contract term change as approved until explicit confirmation from all designated authorities is established.

## Unsupported and missing-source behavior

If asked for information not present in the L3 resources (such as specific SOC 2 control IDs, 24-hour recovery time promises, or non-existent policy exceptions):
- State explicitly that the supplied sources do not support the request for unsupported questions.
- Escalate to the appropriate department (e.g., Security, Legal, Service Reliability, or Policy Owner) per `references/risk-escalation.md`.
- Never fabricate, guess, or assume missing control IDs, approval authorities, or policy rules.

## Examples

### Positive

**Prompt**: "The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?"  
**Behavior**: Load only `references/discount-policy.md`. State that a 12% discount falls into the >10%–15% band requiring VP Sales and Finance Business Partner approval. Cite `[Source: references/discount-policy.md]`.

### Negative

**Prompt**: "Give me the exact SOC 2 control ID that allows us to promise a 24-hour recovery time."  
**Behavior**: Load `references/risk-escalation.md`. State that the supplied sources do not support or contain SOC 2 control IDs or 24-hour recovery time promises. Escalate the request to Legal and Service Reliability. Cite `[Source: references/risk-escalation.md]`.

### Ambiguous

**Prompt**: "A customer asked for a renewal discount. What should I do?"  
**Behavior**: Handle missing input details: Ask the CSM to provide the renewal ARR and the requested discount percentage so the exact approval band and required approvers can be determined from policy.
