# Class 02C Submission — Observe, Record, Play, and Replay an ADK Agent

## Student Information
- **Name**: AI Agent Engineer
- **GitHub Repository**: https://github.com/krprls/agent_engineering
- **Class**: Class 02C — OpenTelemetry & Google Cloud Trace
- **Authentication Mode**: Option B (Google AI Studio API Key + Application Default Credentials for Telemetry)

---

# 1. Executive Summary & Verification

This lab demonstrates end-to-end observability, session event recording, local playback, and OpenTelemetry trace replay for a Google ADK multi-agent system (`workflow_agents`).

### Progress Check Verification (`python scripts/check_progress.py` & `validate_starter.py`)

```text
google-adk: 2.6.0
Golden package imports: OK
Workflow topology reachable: OK
Validation passed. No model API call was made.
Task 2 delegation: PASS ['travel_brainstormer', 'attractions_planner']
Task 3 session-state tool: PASS
Task 4 sequential baseline: PASS ['writers_room', 'preproduction_team', 'file_writer']
Task 5 loop: PASS ['researcher', 'screenwriter', 'critic']
Task 6 parallel fan-out/gather: PASS ['box_office_researcher', 'casting_agent']
All checkpoints PASS. This is the completed golden application.
```

---

# 2. Lab Execution & Telemetry Evidence

## Task 1 — Package & Environment Installation
- Installed `google-adk[otel-gcp]==2.6.0` in an isolated virtual environment (`.venv`).
- Verified all starter imports and progress checkpoints (100% PASS).

## Task 2 & 3 — Authentication & Google Cloud Trace Preparation
- Configured `.env` with `GOOGLE_GENAI_USE_VERTEXAI=FALSE`, `GOOGLE_API_KEY`, and `MODEL=gemini-3.6-flash`.
- Selected Google Cloud Project `gen-lang-client-0856775829`.
- Enabled GCP services: `cloudtrace.googleapis.com`, `logging.googleapis.com`, and `monitoring.googleapis.com`.
- Verified Application Default Credentials: `Application Default Credentials: OK`.

## Task 4 & 5 — Native Telemetry API Server Launch & App Discovery
- Started ADK API Server with native OpenTelemetry export:
  `./class-02C-work/start_api_server.sh gen-lang-client-0856775829` (`OTEL_SERVICE_NAME=class-02c-live`).
- Confirmed application discovery (`curl http://127.0.0.1:8000/list-apps`):
  `["parent_and_subagents", "shared", "workflow_agents"]`.

## Task 6 — Workflow Execution & Event Recording
- Executed `run_and_record.sh "Ada Lovelace"` on session `class02c-20260825-223858`.
- Generated 22 ordered ADK session events recorded into `class-02C-work/events.jsonl` (79 KB).
- Produced movie pitch document: `movie_pitches/Poetical_Science.txt`.
- Sequence of agent activations observed:
  1. `greeter` (prompt capture)
  2. `researcher` (fact gathering from Wikipedia into `state["research"]`)
  3. `screenwriter` (drafting `PLOT_OUTLINE`)
  4. `critic` (evaluating draft, appending feedback)
  5. `researcher` ➔ `screenwriter` ➔ `critic` (loop pass 2, calling `exit_loop`)
  6. `box_office_researcher` & `casting_agent` (parallel fan-out)
  7. `file_writer` (gathering reports and saving final pitch)

## Task 8 & 9 — ADK Event Inspection & Local Playback
- Inspection utility (`show_events.sh`) categorized events by timestamp, author, part types, and state deltas.
- Local playback (`play_events.sh events.jsonl 0.20`) re-played the recorded event sequence without contacting Gemini or re-executing tool side effects.

## Task 10 & 11 — Telemetry Replay to Google Cloud Trace
- Ran dry-run preview: `python class-02C-work/replay_events.py events.jsonl --dry-run` (`Would replay 22 events`).
- Exported telemetry replay trace to GCP:
  `python class-02C-work/replay_events.py events.jsonl --project-id "gen-lang-client-0856775829" --speed 4` (`OTEL_SERVICE_NAME=class-02c-replay`).
- Verified replay output: `Replayed 22 events to Google Cloud Trace in project gen-lang-client-0856775829`.

---

# 3. Live Trace vs. Replay Trace Analysis

| Metric / Dimension | Live Execution Trace (`class-02c-live`) | Replay Trace (`class-02c-replay`) |
|---|---|---|
| **Data Source** | Real ADK runtime & agent execution | Reconstructed from `events.jsonl` file |
| **Span Structure** | Native runtime, agent hierarchy, model calls, tools | One reconstructed span per recorded ADK event |
| **Latency & Timing** | True operational latency & API durations | Scaled relative event timing (`--speed 4`) |
| **Side Effects** | Calls Gemini API, queries Wikipedia, writes pitch text file | Zero model calls, zero external API calls, zero file IO |
| **Identifiers** | Original live execution trace & span IDs | Newly generated replay trace and span IDs |
| **Cost & Safety** | Consumes API tokens and quota | 100% offline, zero token cost |

---

# 4. Conceptual Reflection Answers

1. **Which live span consumed the most time?**
   > Model generation spans (`google_genai.generate_content`) and sequential workflow stages—specifically screenwriter plot generation and Wikipedia factual research.

2. **Where can you see the loop repeat?**
   > In the `writers_room` (`LoopAgent`) trace span hierarchy, where the sequence `researcher` ➔ `screenwriter` ➔ `critic` iterated twice before the critic invoked `exit_loop`.

3. **Where can you see parallel fan-out and join?**
   > Inside `preproduction_team` (`ParallelAgent`), where `box_office_researcher` and `casting_agent` executed concurrently in parallel, followed by `file_writer` gathering both state outputs.

4. **Which ADK Events changed state?**
   > Event 5 (greeter prompt state), Event 11 (`research` gathered by researcher), Event 14 (`PLOT_OUTLINE` generated by screenwriter), Event 18 (`box_office_report`), and Event 19 (`casting_report`).

5. **Why are the replay trace IDs and durations different?**
   > Replay generates a new trace context upon emission and uses scaled relative timing (`--speed 4`) rather than repeating real network delays.

6. **Why is telemetry replay safer and cheaper than rerunning the agent?**
   > Replay makes zero calls to LLM APIs (zero token cost) and executes no external tools, preventing accidental state mutations, API charges, or file overwrites.

7. **What debugging questions require the live trace rather than the replay?**
   > Diagnosing real model latency, network performance bottlenecks, API rate limits (HTTP 429 errors), live exception stack traces, and token consumption metrics.
