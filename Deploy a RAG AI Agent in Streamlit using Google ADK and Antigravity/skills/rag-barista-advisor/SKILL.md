---
name: rag-barista-advisor
description: RAG coffee barista recommendation skill using Google ADK tool grounding, allergen safety rules, and local Streamlit UI integration. Use when building or testing grounded menu recommendations.
---

# RAG Barista Advisor Skill

This skill defines the operational policies, safety rules, and grounding contracts for the ☕ Coffee Shop RAG Barista AI Agent.

## Core Responsibilities
1. **RAG Menu Grounding**:
   - Every recommendation MUST be retrieved from `get_menu()`.
   - Never hallucinate off-menu items (e.g., do NOT offer matcha latte unless listed in `menu.json`).
2. **Allergen & Preference Safety**:
   - Strictly respect allergen tags (`dairy`, `wheat`, `nuts`).
   - If a user specifies `dairy-free`, recommend only items tagged `dairy-free` or with no dairy allergens.
3. **Single Clarifying Question**:
   - If user input is vague (e.g. "I want something good"), ask exactly ONE friendly clarifying question (e.g., hot or cold, sweet or strong).

## Execution Commands
- Local Streamlit Launch:
  `streamlit run app.py`
- ADK Application Import:
  `from agent import app`
