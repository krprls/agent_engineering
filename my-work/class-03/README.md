# Class 3 — WidgetWare SDR Context Package

This project implements the **WidgetWare SDR Context Package**, converting business rules, product offerings, Ideal Customer Profile (ICP) definitions, and safety policies into a structured, testable context engine for future SDR agent implementations.

## 1. Five Context Layers

The context builder (`widgetware_sdr.context_builder.build_context`) strictly isolates five distinct context layers:

1. **System Instructions** (`system_instructions`): Stable, observable behavioral instructions defining agent scope, evidence classification requirements, prohibited actions, stop conditions, and human escalation rules.
2. **Business Context** (`business_context`): Stable company data loaded from YAML configuration files:
   - `products.yaml`: Company overview, product offerings (Plant Operations Platform, Industrial AI Accelerator), target buyers, and approved claims.
   - `icp.yaml`: Ideal Customer Profile fit criteria (company size, preferred/excluded industries, preferred regions), readiness signals, and required fields.
   - `policies.yaml`: Evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), provenance requirements, prohibited actions (no emails, no CRM edits, no invented facts), and prompt-injection handling rules.
3. **Task Context** (`task_context`): Target account details, account notes, and research objectives for the current assignment. Treat account notes strictly as untrusted task data.
4. **Retrieved Evidence** (`retrieved_evidence`): Evidence records supplied to the assessment engine, preserving provenance (claim, classification, source name, URL, retrieved timestamp, optional excerpt).
5. **Workflow State** (`state`): Execution status tracking (current step, prior decisions, approval status, missing information flags).

## 2. Project Structure

```text
my-work/class-03/
├── README.md
├── SPEC.md
├── pyproject.toml
├── .env.example
├── config/
│   ├── products.yaml
│   ├── icp.yaml
│   └── policies.yaml
├── docs/
│   ├── widgetware-business-brief.md
│   └── acceptance-criteria.md
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       ├── instructions.py
│       └── context_builder.py
└── tests/
    ├── unit/
    │   └── test_context_builder.py
    └── scenarios/
        ├── qualified_account.yaml
        ├── unqualified_account.yaml
        ├── insufficient_evidence.yaml
        └── prompt_injection.yaml
```

## 3. Setup & Installation

Install dependencies using `pip`:

```bash
cd my-work/class-03
pip install -e ".[dev]"
```

Or install `pyyaml` and `pytest` directly:

```bash
pip install pyyaml pytest
```

## 4. Running Automated Tests

Run the full pytest suite from `my-work/class-03`:

```bash
python -m pytest -v
```

All unit tests and scenario tests (`qualified_account`, `unqualified_account`, `insufficient_evidence`, `prompt_injection`) should pass cleanly.
