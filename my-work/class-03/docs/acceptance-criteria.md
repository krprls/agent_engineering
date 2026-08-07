# Class 3 Acceptance Criteria Checklist

This document tracks compliance with Section 16 of `SPEC.md`.

- [x] `products.yaml`, `icp.yaml`, and `policies.yaml` exist in `config/`.
- [x] At least two WidgetWare offerings are configured with target buyers and approved claims.
- [x] ICP contains explicit fit dimensions (size, industry, region) and required account fields.
- [x] Safety boundaries explicitly prohibit autonomous messaging, CRM edits, and inventing facts.
- [x] System instructions are inspectable via `get_system_instructions()`.
- [x] `build_context(...)` returns 5 strictly separated context layers.
- [x] Evidence records preserve provenance (claim, classification, source name, URL, retrieved_at).
- [x] Missing information remains `unknown` without hallucinated values.
- [x] Prompt injection content cannot override system instructions or policies.
- [x] Four required scenario fixtures exist (`qualified_account.yaml`, `unqualified_account.yaml`, `insufficient_evidence.yaml`, `prompt_injection.yaml`).
- [x] All automated tests in `tests/` pass clean.
- [x] No ADK agent, LLM calls, web research, or external mutations are included.
