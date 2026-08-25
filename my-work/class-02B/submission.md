# Class 02B Submission: Build Multi-Agent Systems with ADK 2.x

## Student Information
- **Name**: AI Agent Engineer
- **GitHub Repository**: https://github.com/krprls/agent_engineering
- **Branch / Commit**: main

---

# 1. Executive Summary & Verification

This submission demonstrates the complete implementation of multi-agent architectures using Google ADK 2.x, covering parent-child delegation, session state management, iterative loops (`LoopAgent`), and parallel fan-out/gather workflows (`ParallelAgent`).

### Automated Testing Evidence Output
Running `python scripts/validate_starter.py` and `python scripts/check_progress.py`:

```text
google-adk: 2.6.0
Starter imports: OK
Sequential baseline: OK
Validation passed. No model API call was made.

Task 2 delegation: PASS
Task 3 session-state tool: PASS
Task 4 sequential baseline: PASS ['writers_room', 'preproduction_team', 'file_writer']
Task 5 loop: PASS
Task 6 parallel fan-out/gather: PASS
```

---

# 2. Implemented Components & Topology Evidence

## Task 2 — Parent and Sub-Agent Delegation Topology
- **Implementation File**: `parent_and_subagents/agent.py`
- **Code Wiring**: Attached `sub_agents=[travel_brainstormer, attractions_planner]` to `root_agent` (`steering`) in `parent_and_subagents/agent.py`.
- **Explicit Transfer Rules**: Added explicit routing instructions to `steering`:
  - Send user to `travel_brainstormer` if they need help deciding their travel destination.
  - Send user to `attractions_planner` if they know what country they wish to visit.
- **Trace Evidence & Trial Observations**:
  - **Trial 1 Prompt**: `"I want to go on a vacation for shopping, food, and viewing historical art, but I am not sure which country to visit."`
    - *Observed Agent Transfer*: `[steering]` ➔ `[travel_brainstormer]`. `travel_brainstormer` generated country options (Italy, France, Japan, Spain).
  - **Trial 2 Prompt**: `"I would like to visit Japan."`
    - *Observed Agent Transfer*: `[steering]` ➔ `[attractions_planner]`. `attractions_planner` recommended famous Japanese attractions.

## Task 3 — Session State & State-Writing Tool
- **Implementation File**: `parent_and_subagents/agent.py`
- **Tool Implementation**: Implemented `save_attractions_to_state(tool_context: ToolContext, attractions: List[str]) -> dict[str, str]` tool. Added `tools=[save_attractions_to_state]` to `attractions_planner`.
- **State Templating**: Configured `attractions_planner` instructions with `{attractions?}` optional state templating.
- **Trace Evidence & Trial Observations**:
  - **Trial 1 Prompt**: `"I would like to visit Japan. Suggest some famous attractions, and please save Fushimi Inari Shrine and Kinkaku-ji to my travel list."`
    - *Observed Tool Execution*: `save_attractions_to_state` called, producing `state_delta` = `{"attractions": ["Fushimi Inari Shrine", "Kinkaku-ji"]}`.
  - **Trial 2 Prompt**: `"What attractions are currently saved on my travel list?"`
    - *Observed State Retrieval*: `attractions_planner` read state variable `{attractions?}` and rendered the saved list across turns:
      - *Fushimi Inari Shrine*
      - *Kinkaku-ji*

## Task 4 — SequentialAgent Baseline
- **Implementation File**: `workflow_agents/agent.py`
- **Sequence Wiring**: `film_concept_team = SequentialAgent(name="film_concept_team", sub_agents=[researcher, screenwriter, file_writer])`. Executed 3-stage baseline sequence.

## Task 5 — Iterative Refinement with LoopAgent
- **Implementation File**: `workflow_agents/agent.py`
- **Loop Component Wiring**:
  - Imported `from google.adk.tools import exit_loop`.
  - Implemented `critic` agent with tools `[append_to_state, exit_loop]` evaluating `PLOT_OUTLINE` against `RESEARCH` across 4 cinematic criteria.
  - Wrapped `researcher`, `screenwriter`, and `critic` in `writers_room = LoopAgent(name="writers_room", description="Iterates through research and writing to improve a movie plot outline.", sub_agents=[researcher, screenwriter, critic], max_iterations=5)`.
  - Updated `film_concept_team` to start with `writers_room`.
- **Trace Evidence & Trial Observations**:
  - **Trial Prompt**: `"Ada Lovelace"`
    - *Observed Loop Execution*: Cycled through `researcher` ➔ `screenwriter` ➔ `critic`. `critic` inspected `PLOT_OUTLINE` against historical research, appended feedback to `CRITICAL_FEEDBACK` on pass 1, and called `exit_loop` on pass 2 once criteria were satisfied, terminating loop execution cleanly before hitting `max_iterations=5`.

## Task 6 — Parallel Fan-Out and Gather (ParallelAgent)
- **Implementation File**: `workflow_agents/agent.py`
- **Parallel Component Wiring**:
  - Implemented `box_office_researcher` (`output_key="box_office_report"`) and `casting_agent` (`output_key="casting_report"`).
  - Wrapped both independent branch agents in `preproduction_team = ParallelAgent(name="preproduction_team", sub_agents=[box_office_researcher, casting_agent])`.
  - Inserted `preproduction_team` into `film_concept_team`: `sub_agents=[writers_room, preproduction_team, file_writer]`.
  - Updated `file_writer` instruction to gather `{box_office_report?}` and `{casting_report?}` from state alongside `{PLOT_OUTLINE?}` and save the output document to `movie_pitches/<title>.txt`.
- **Trace Evidence & Trial Observations**:
  - **Trial Prompt**: `"Ada Lovelace"`
    - *Observed Fan-Out*: Concurrently executed `box_office_researcher` and `casting_agent` writing to distinct state keys `box_office_report` and `casting_report`.
    - *Observed Gather*: `file_writer` gathered both report keys and saved the comprehensive pitch to `movie_pitches/Ada_Lovelace_movie_pitch.txt`.

---

# 3. Final Architecture Topology

```text
greeter (Root Agent)
└── film_concept_team (SequentialAgent)
    ├── writers_room (LoopAgent, max 5)
    │   ├── researcher (Wikipedia -> state["research"])
    │   ├── screenwriter -> state["PLOT_OUTLINE"]
    │   └── critic -> exit_loop when ready
    ├── preproduction_team (ParallelAgent - Fan Out)
    │   ├── box_office_researcher -> state["box_office_report"]
    │   └── casting_agent -> state["casting_report"]
    └── file_writer (Gather Step) -> movie_pitches/<title>.txt
```

---

# 4. Learning Reflections & Conceptual Answers

### 1. Why does `description` help an LLM parent choose a child agent?
> The parent agent evaluates user input against the `description` metadata of all registered `sub_agents` to determine which child agent possesses the appropriate domain specialization. A clear, distinct description allows the model's routing mechanism to delegate turns accurately without embedding child instructions into the parent prompt.

### 2. How do you distinguish tool capability from instruction policy?
> A **tool** defines mechanical *capability*—what the agent is authorized to execute or modify (e.g., calling `save_attractions_to_state` or `exit_loop`). An **instruction policy** defines *when* and *why* the agent should invoke that tool (e.g., "When the user provides selected attractions, call save_attractions_to_state").

### 3. How does `state_delta` work in ADK session state?
> When a tool modifies `tool_context.state`, ADK generates a `state_delta` event recording the key-value changes. This delta updates the centralized session state, making new data immediately available to all agents within the same session across multiple turns.

### 4. What is `{key?}` state templating?
> The `{key?}` syntax dynamically injects session state values into agent instructions. The trailing `?` makes the key optional, preventing runtime template errors if the state key has not yet been populated in earlier turns.

### 5. What is the difference between LLM transfer and deterministic sequence?
> **LLM Transfer** (`sub_agents` on an LLM agent) relies on the model to dynamically choose if and when to transfer control based on conversation intent. A **Deterministic Sequence** (`SequentialAgent`) executes sub-agents in a fixed, predefined linear order regardless of conversation intent.

### 6. Why do loops need both an exit condition and a hard cap?
> An **exit condition** (`exit_loop`) allows the loop to terminate early as soon as quality criteria are satisfied, preventing unnecessary model calls. A **hard cap** (`max_iterations=5`) provides a safety bound that guarantees the loop will terminate even if the critic never triggers an exit, preventing infinite loops and runaway API billing.

### 7. How do you identify work that is safe to run in parallel?
> Work is safe to run in parallel (`ParallelAgent`) when sub-tasks depend on the same prior state (e.g., `PLOT_OUTLINE`) but do not depend on each other's intermediate outputs. In Class 02B, `box_office_researcher` and `casting_agent` both read `PLOT_OUTLINE` independently and write to distinct state keys.

### 8. How does `output_key` enable a later gather stage?
> `output_key` directs an agent to write its entire response payload into a designated session state key (e.g., `box_office_report`). In a subsequent stage, a downstream agent (`file_writer`) can read multiple distinct `output_key` fields from state (`{box_office_report?}`, `{casting_report?}`), gathering parallel branch outputs into a unified final document.
