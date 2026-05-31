# PRD — Structured FIFO Logging (`FifoLineRotatingHandler` + event schema)

> **Status:** Phase 1 mandatory design document. Implemented in Phase 2 (see playbook §4, prompt task 3).
> **Owner module:** `src/cosmos77_ex02/shared/logging_setup.py` + `src/cosmos77_ex02/shared/fifo_handler.py`.
> **Config of record:** `config/logging_config.json` (FIFO knobs), with secondary references to `config/setup.json` (`paths.logs_dir`) and `config/gatekeeper.json` (cost events). All values are config-driven (rule 4); this document pins the exact configured values and forbids inventing new ones.

This document specifies the **audit log** for the AI Agent Debate. The grader clones the repo, runs one debate, and must be able to **reconstruct the entire run from the logs alone** — every `claude -p` agent call, every routed message, every dollar of cost, every watchdog restart, and the final verdict. Logs are append-only, machine-parseable JSON-lines, FIFO-rotated so disk usage is bounded, and scrubbed of any secret-like material before a byte hits disk.

This PRD maps primarily to acceptance criterion **A11** ("structured FIFO logs (20×500, config-driven)") and supports **A6** (every JSON message is logged and monitorable), **A8** (the verdict is logged), and **A15** (README evidence and the cost section are sourced from these logs). It is a sibling of `docs/PRD_gatekeeper.md` (cost-event source + `scrub()` owner), `docs/PRD_ipc_protocol.md` (message shape), `docs/PRD_orchestrator.md` (turn/transcript events), and `docs/PRD_watchdog.md` (restart events).

---

## 1. Goals and non-goals

### 1.1 Goals
- **G1 — Full-run auditability.** Given only `logs/*.log`, a grader can replay the timeline: which agent was invoked, with which prompt fingerprint, what it returned, its token/USD cost, each routed message, each retry/rejection, each restart, and the final verdict. Maps to **A11**, **A15**.
- **G2 — Bounded, predictable disk usage.** Exactly **20 files × 500 lines max** (config-driven), oldest dropped first (FIFO). Maps to **A11**.
- **G3 — Machine-parseable.** One JSON object per line (JSON-lines / NDJSON). `jq` and a 10-line Python reader can analyze a run. Maps to **A6**.
- **G4 — Secret-safe.** No API keys, tokens, session credentials, or `.env` values are ever written. Maps to rule 9 and the "cyber layer" requirement in playbook §3 task 9.
- **G5 — Zero hardcoded knobs.** File count, lines-per-file, directory, encoding, and levels come from `config/logging_config.json`. Maps to rule 4.
- **G6 — Deterministic and testable.** Rotation behavior is unit-testable with a `tmp_path` directory and **no real I/O beyond the temp dir**; no live `claude` calls (rules 6, 17).

### 1.2 Non-goals
- **Not** the canonical debate artifact. The graded transcript is `transcripts/session_001.json`, owned by `docs/PRD_orchestrator.md`. Logs are the *operational audit trail* alongside it; they overlap but serve different consumers (machine ops vs. human transcript).
- **Not** a metrics/observability backend (no Prometheus, no OpenTelemetry). Out of scope for HW2.
- **Not** log shipping, compression, or remote sinks. Local files only.
- **Not** time-based or byte-based rotation — rotation is strictly **line-count** based (see §4), because the unit of a debate audit is the event, not the wall clock or byte.

---

## 2. Stakeholders and consumers

| Consumer | Need from logs | How they read |
|---|---|---|
| **Grader (Dr. Yoram Segal / agent)** | Prove the debate ran end-to-end: 10 pings/side, every message child→judge→child, ≥1 citation/turn, no tie, budget respected. | `tail`, `jq`, or the menu's "Tail logs" action (option [5], see `docs/PRD_terminal_menu.md`). |
| **SDK / `SDK.tail_logs(n)`** | Return the last *N* log lines for the menu. | Reads newest file(s) in FIFO order. |
| **`SDK.cost_report()`** | Aggregate `cost` events into total USD / tokens / cost-per-ping. | Filters `event == "cost"`. Cross-ref `docs/PRD_gatekeeper.md`. |
| **Developers (Abdallah, Tasneem)** | Debug a stalled or rejected turn. | Filter by `event`, `ping_no`, `agent`. |
| **CI** | Never sees live logs; tests assert rotation invariants on a temp dir. | `tests/unit/test_shared/test_logging_setup.py`. |

---

## 3. Configured values (pinned — do not invent)

All from `config/logging_config.json` unless noted. These are the **single source of truth**; the handler reads them and never falls back to literals except as last-resort defaults documented in §4.4.

| Key | Path in config | Value | Meaning |
|---|---|---|---|
| Max files | `handlers.fifo_file.max_files` (and `fifo.max_files`) | **20** | Keep the newest 20 rotated files; drop the oldest. |
| Max lines/file | `handlers.fifo_file.max_lines_per_file` (and `fifo.max_lines_per_file`) | **500** | Rotate the active file when it reaches 500 written lines. |
| Directory | `handlers.fifo_file.directory` | **`logs`** | Log directory (mirrors `config/setup.json` → `paths.logs_dir`). |
| Encoding | `handlers.fifo_file.encoding` | **`utf-8`** | English-only output (rule: English; matches `constants.DEFAULT_ENCODING`). |
| File handler level | `handlers.fifo_file.level` | **`DEBUG`** | The audit file captures everything from DEBUG up. |
| Console level | `handlers.console.level` | **`INFO`** | Operator-facing console is quieter than the file. |
| File formatter | `handlers.fifo_file.formatter` | **`jsonl`** | `format: "%(message)s"` — the record *is* the JSON line. |
| Console formatter | `handlers.console.formatter` | **`standard`** | Human-readable `%(asctime)s \| %(levelname)-7s \| %(name)s \| %(message)s`. |
| Handler class | `handlers.fifo_file.class` | **`cosmos77_ex02.shared.fifo_handler.FifoLineRotatingHandler`** | The custom handler specified in this PRD. |
| Primary logger | `loggers.cosmos77_ex02` | level `DEBUG`, handlers `["console","fifo_file"]`, `propagate: false` | All package logging flows here. |
| Schema version | `schema_version` | **`1.00`** | Validated against `version.py` (rule 10). |

**Derived ceiling:** worst-case **20 × 500 = 10,000 lines** of audit retained at any moment. A full 10-ping debate (see §7 for the event budget) produces on the order of a few hundred to ~1,000 lines, so a single session fits comfortably inside the FIFO window without dropping its own start — but rotation is still proven by tests with tightened values.

**Pinned dependent values referenced by events:** `pings_per_side = 10`, `max_words_per_turn = 180`, `require_citation_per_turn = true`, `per_call_timeout_seconds = 120`, `watchdog_keepalive_seconds = 15`, `max_restarts_per_agent = 3` (from `config/setup.json`); `budget_usd_max = 5.00`, `per_call_usd_max = 0.50`, `warn_at_fraction = 0.8`, `hard_stop = true` (from `config/gatekeeper.json`).

---

## 4. `FifoLineRotatingHandler` — behavioral spec

`FifoLineRotatingHandler` lives in `src/cosmos77_ex02/shared/fifo_handler.py` (split out of `logging_setup.py` to respect the 150-line cap, rule 1). It subclasses `logging.Handler` (not `RotatingFileHandler`, because stock rotation is byte-based and the trigger and retention policy differ; see ADR-LOG-001).

### 4.1 File naming and the FIFO order
- Active (current) file: **`logs/debate.log`**.
- Rotated files: **`logs/debate.log.1` … `logs/debate.log.{max_files-1}`**, i.e. up to `logs/debate.log.19`.
- `.log.1` is the **most recent** rotation; the higher the suffix, the older the file. The oldest retained file is `.log.19`. This is the conventional `RotatingFileHandler` numbering, kept so `tail`/`jq` users and `SDK.tail_logs()` have predictable names.

> **"FIFO" clarification.** Rotation is First-In-First-Out by **age of the line stream**: the oldest *lines* (oldest files) are evicted first when the retention window is full. The active file is written in chronological (append) order; on rollover the active file becomes `.log.1` and everything shifts up by one suffix; whatever would become `.log.20` is **deleted**, never kept. Newest 20 files survive, oldest dropped.

### 4.2 The rotation trigger (line-count, not bytes)
1. The handler maintains an in-memory `self._line_count` for the active file, initialized on `open` by counting existing newline characters in `debate.log` (so restarts mid-file do not under-count; see §4.4 restart handling).
2. On every `emit(record)`:
   - Format the record to a single line (the formatter guarantees one logical line; see §4.5 newline guard).
   - If `self._line_count >= max_lines_per_file` (**500**) *before* writing, perform a **rollover** (§4.3), then write into the fresh active file.
   - Write the line + `"\n"`, flush, and increment `self._line_count`.
3. A record that itself contains an embedded newline is sanitized to a single physical line *before* the count check (§4.5), so one `emit` == exactly one counted line. This keeps the 500-line invariant exact and the "one JSON object per line" promise intact.

> **Boundary rule (must be tested):** writing the 500th line fills the active file; the **501st** `emit` triggers rollover first, so no file ever exceeds `max_lines_per_file`. The unit test asserts `wc -l` on every rotated file is `<= 500`.

### 4.3 Rollover algorithm (keep newest `max_files`, drop oldest)
On rollover (active file is full):
1. Close the active file handle.
2. **Cascade the suffixes from oldest to newest** so we never overwrite a file we still need:
   - If `logs/debate.log.{max_files-1}` (i.e. `.log.19`) exists, **delete it** (this is the FIFO eviction of the oldest line stream).
   - For `i` from `max_files-2` down to `1` (i.e. 18 → 1): if `debate.log.{i}` exists, rename it to `debate.log.{i+1}`.
   - Rename the active `debate.log` → `debate.log.1`.
3. Open a new empty `debate.log`, reset `self._line_count = 0`.
4. Emit an internal `event: "log_rotated"` line as the first line of the new file (see §6.7) so the audit trail itself records that a rotation happened and which file was dropped — this prevents "silent gaps" from confusing the grader.

This guarantees the invariant: **at most `max_files` (20) files exist**, and they are always the **newest** ones; the oldest is dropped on each rollover.

### 4.4 Initialization, defaults, and restart behavior
- `__init__(self, directory, max_files, max_lines_per_file, encoding="utf-8", level=logging.DEBUG)` — every parameter is supplied by `dictConfig` from `config/logging_config.json`. **No literals**; the only defaults are last-resort fallbacks (`max_files=20`, `max_lines_per_file=500`, `encoding="utf-8"`) used solely if a key is somehow absent, and a `WARNING` is logged when a fallback is taken (rule 4 compliance is still satisfied because config always supplies them).
- On construction the handler `mkdir -p`'s `directory` (idempotent), opens `debate.log` in append mode, and **counts existing lines** to seed `self._line_count`. Because the orchestrator + watchdog may **restart** child processes (up to `max_restarts_per_agent = 3`), several processes can target the same log directory; see §8 for the multiprocess concurrency policy.
- Schema/version: `logging_setup.init_logging()` validates `schema_version == VERSION` ("1.00") via `version.validate_config_version()` before `dictConfig` runs; a mismatch raises a clear error rather than logging into a misversioned schema.

### 4.5 Line integrity (the "one event = one line" guard)
- The `jsonl` formatter is `"%(message)s"`; loggers are expected to pass an **already-serialized JSON string** as the message (see §5 emit helpers).
- The handler defensively `.replace("\n", "\\n").replace("\r", "\\r")` on the formatted string before writing, so even a multi-line `content` field (e.g., a debater turn with line breaks) collapses to exactly one physical line. JSON string-escaping during serialization already handles this; the handler guard is belt-and-suspenders so the line count and `jq` parsing never break.
- Empty/blank records are not written (no empty lines pollute the count).

### 4.6 Failure isolation
- Logging must **never crash the debate.** `emit` wraps its body so that an `OSError` (disk full, permission) routes to `self.handleError(record)` (standard `logging` behavior) and the debate continues. A failed write does not increment the line count.
- `close()` flushes and closes the active handle and is idempotent (safe to call on `atexit` and on watchdog teardown).

### 4.7 ADR-LOG-001 (recorded here, referenced from `docs/PLAN.md`)
**Decision:** implement a bespoke `FifoLineRotatingHandler` subclassing `logging.Handler` rather than reusing `logging.handlers.RotatingFileHandler`.
**Rationale:** (1) the spec's unit of rotation is **lines (500)**, not bytes, and stock `RotatingFileHandler` only rotates by byte size; (2) we need an explicit, testable FIFO eviction that emits a `log_rotated` audit event; (3) line-count integrity ties directly to the "one JSON event per line" contract. **Alternative considered:** wrap `RotatingFileHandler` with a byte estimate — rejected because line counts would be approximate and untestable to the exact 500 boundary the grader can check with `wc -l`.

---

## 5. How events are emitted (the logging API)

To keep call sites uniform and avoid duplication (rule 3), `logging_setup.py` exposes thin helpers that **build the event dict, scrub it, serialize to JSON, and log it** at the right level. Every module logs through the package logger `cosmos77_ex02` (so it inherits the `fifo_file` + `console` handlers and `propagate: false`).

```python
def log_event(event: str, **fields: object) -> None:
    """Emit one scrubbed JSON-lines audit event on the package logger.

    Always adds ts, schema_version, and event; scrubs every string value
    via Gatekeeper.scrub() before serialization. One call == one log line.
    """
```

Specialized convenience wrappers (each ≤ a few lines, all delegating to `log_event`) keep call sites readable:
`log_agent_call(...)`, `log_message(msg: ProtocolMessage)`, `log_cost(...)`, `log_rejection(...)`, `log_restart(...)`, `log_verdict(verdict)`, `log_run_start(...)`, `log_run_end(...)`.

- `log_message` accepts a `ProtocolMessage` (see `docs/PRD_ipc_protocol.md`) and projects its fields into the `message` event (§6.2) — it does **not** re-validate; validation is the protocol layer's job.
- `log_cost` is called by the Gatekeeper after each `account()` (see `docs/PRD_gatekeeper.md`) so cost truth lives in one place and `SDK.cost_report()` reads it back from `event == "cost"` lines.
- Levels: routine events at `INFO`/`DEBUG` (file captures both; console shows `INFO`+); `rejection`, `restart`, `budget_warn`, `budget_stop` at `WARNING`/`ERROR` so they surface on the console too.

---

## 6. Event schema (JSON-lines)

Every line is a single JSON object. **Common envelope fields present on every event:**

| Field | Type | Required | Description |
|---|---|---|---|
| `ts` | string (ISO-8601, UTC, `...Z`) | yes | Event timestamp, e.g. `2026-05-31T09:14:02.314Z`. |
| `schema_version` | string | yes | `"1.00"` (matches `version.py`). |
| `event` | string (enum) | yes | One of: `run_start`, `agent_call`, `message`, `cost`, `rejection`, `restart`, `verdict`, `log_rotated`, `budget_warn`, `budget_stop`, `run_end`. |
| `session` | string | yes | Session id, e.g. `session_001` (aligns with the transcript filename). |
| `pid` | int | yes | OS process id of the emitter (proves the 3-process / restart model, A1). |
| `level` | string | yes | Log level name (`DEBUG`…`ERROR`). |

The event-specific payloads below extend the envelope.

### 6.1 `agent_call` — one `claude -p` invocation (A9, A7)
| Field | Type | Description |
|---|---|---|
| `agent` | `"judge" \| "pro" \| "con"` | Caller role (`constants.ROLES`). |
| `phase` | string | e.g. `opening`, `rebuttal`, `verdict`. |
| `ping_no` | int | 1…10 (or 0 for setup). |
| `skill` | string | Skill file name, e.g. `skill_pro.md` (not its contents). |
| `prompt_chars` | int | Length of the rendered prompt (size only — **never** the prompt text, to avoid leaking injected secrets or bloating logs). |
| `prompt_sha256` | string | Hex digest of the rendered prompt for reproducibility without storing it. |
| `allowed_tools` | list[string] | e.g. `["WebSearch"]` — proves the mandatory web tool is enabled (A7). |
| `timeout_s` | int | `120` (`per_call_timeout_seconds`). |
| `outcome` | `"ok" \| "timeout" \| "error" \| "retry"` | Result class. |
| `duration_ms` | int | Wall-clock for the subprocess call. |
| `session_id` | string \| null | The `claude` JSON `session_id` (opaque; not a secret, but passed through `scrub()` regardless). |

### 6.2 `message` — a routed protocol message (A5, A6)
Projection of `ProtocolMessage` (see `docs/PRD_ipc_protocol.md`):
| Field | Type | Description |
|---|---|---|
| `msg_id` | string | Message id. |
| `sender` | role | `pro`/`con`/`judge`. |
| `recipient` | role | Routing target — **always** `judge` for child output, never child→child (A5). |
| `turn_type` | `"opening" \| "rebuttal" \| "closing"` | `constants.TURN_TYPES`. |
| `ping_no` | int | 1…10. |
| `word_count` | int | Validated ≤ `max_words_per_turn` (**180**). |
| `citations` | list[string] | ≥ 1 when `require_citation_per_turn` is true; logging the count + URLs proves A7. |
| `content_chars` | int | Size of `content`. |
| `content_sha256` | string | Digest of `content`. The **full text** lives in the transcript (`docs/PRD_orchestrator.md`); logs keep a digest + size to stay bounded and avoid duplicating the transcript. |
| `tokens` | int | Token count for the turn. |
| `cost_usd` | float | Per-message cost (mirrors the `cost` event). |

> **Routing audit:** because every `message` event carries `sender`/`recipient`, a grader can `jq 'select(.event=="message") | [.sender,.recipient]'` and confirm **no `pro→con` or `con→pro`** edge ever appears — every edge is `*→judge` or `judge→*` (A5). This is the log-side mirror of `protocol.is_through_father(history)`.

### 6.3 `cost` — Gatekeeper accounting (A11, A15 cost section)
| Field | Type | Description |
|---|---|---|
| `agent` | role | Who incurred the cost. |
| `ping_no` | int | For cost-per-ping projections. |
| `call_cost_usd` | float | `total_cost_usd` from this `claude -p` JSON. |
| `input_tokens` / `output_tokens` | int | From the result `usage`. |
| `cumulative_usd` | float | Running total tracked by the Gatekeeper. |
| `budget_usd_max` | float | `5.00` (echoed for self-describing logs). |
| `fraction_used` | float | `cumulative_usd / budget_usd_max`. |
| `per_call_usd_max` | float | `0.50` (ceiling check). |

`SDK.cost_report()` sums `call_cost_usd` and reads the last `cumulative_usd`. See `docs/PRD_gatekeeper.md`.

### 6.4 `rejection` — a turn rejected and retried (A4, A7, A10)
| Field | Type | Description |
|---|---|---|
| `agent` | role | Whose turn was rejected. |
| `ping_no` | int | Which ping. |
| `reason` | `"missing_citation" \| "over_word_limit" \| "no_rebuttal" \| "off_position" \| "agreement_drift" \| "schema_invalid"` | Enforcement reason (judge/orchestrator). |
| `detail` | string | Human-readable note (e.g., `"word_count=204 > 180"`), scrubbed. |
| `attempt` | int | Retry attempt index. |
| `retry_scheduled` | bool | Whether a redo was requested. |

Logged at `WARNING`. This is the auditable proof that citation-less / over-length / non-rebutting turns are caught and retried, not silently accepted.

### 6.5 `restart` — watchdog killed and respawned a process (A11)
| Field | Type | Description |
|---|---|---|
| `agent` | role | Which child was restarted. |
| `dead_pid` | int | The terminated process id. |
| `new_pid` | int \| null | The respawned process id (null if max restarts hit). |
| `cause` | `"stall" \| "crash" \| "timeout"` | Why. `stall` = no heartbeat for `watchdog_keepalive_seconds` (**15s**). |
| `restart_index` | int | 1…`max_restarts_per_agent` (**3**). |
| `replayed_context_ping_no` | int | Which context was replayed so the debate continues. |

See `docs/PRD_watchdog.md`. Logged at `WARNING` (or `ERROR` when `restart_index` exceeds the cap and the run aborts).

### 6.6 `verdict` — the final, no-tie judgment (A8)
| Field | Type | Description |
|---|---|---|
| `winner` | `"pro" \| "con"` | Never a tie (validated by `Verdict`, see `docs/PRD_judge_agent.md`). |
| `pro_score` | int | e.g. `80`. |
| `con_score` | int | e.g. `73`; **must differ** from `pro_score`. |
| `margin` | int | `abs(pro_score - con_score)` — must be `> 0`. |
| `justification_chars` | int | Size of the written justification. |
| `justification_sha256` | string | Digest; full justification lives in the transcript + README. |
| `decided_at` | string | ISO-8601 timestamp. |

A grader confirms **no tie** with `jq 'select(.event=="verdict") | .pro_score != .con_score'` → `true` (A8).

### 6.7 `log_rotated` — internal FIFO audit (G1, §4.3)
| Field | Type | Description |
|---|---|---|
| `rotated_to` | string | New name of the file that was just filled, e.g. `debate.log.1`. |
| `dropped_file` | string \| null | The oldest file deleted (e.g. `debate.log.19`) or `null` if the window wasn't yet full. |
| `files_retained` | int | Current count, ≤ `max_files` (20). |

### 6.8 `run_start` / `run_end` — debate boundaries
`run_start`: `topic`, `pro_position`, `con_position`, `pings_per_side` (10), `max_words_per_turn` (180), `budget_usd_max` (5.00), `config_versions` (the three `"1.00"` versions). `run_end`: `outcome` (`"completed" \| "aborted_budget" \| "aborted_watchdog"`), `total_pings`, `total_cost_usd`, `winner`, `duration_s`.

### 6.9 `budget_warn` / `budget_stop` — Gatekeeper thresholds (A11)
`budget_warn` fires once when `fraction_used >= warn_at_fraction` (**0.8**); `budget_stop` fires when `cumulative_usd >= budget_usd_max` (**5.00**) and `hard_stop` is true, recording that the debate aborted cleanly. Both carry `cumulative_usd`, `budget_usd_max`, `fraction_used`. Logged at `WARNING`/`ERROR`.

### 6.10 Worked example lines (illustrative)
```json
{"ts":"2026-05-31T09:14:00.001Z","schema_version":"1.00","event":"run_start","session":"session_001","pid":40111,"level":"INFO","topic":"Is social media a net positive for society?","pings_per_side":10,"max_words_per_turn":180,"budget_usd_max":5.0}
{"ts":"2026-05-31T09:14:03.880Z","schema_version":"1.00","event":"agent_call","session":"session_001","pid":40113,"level":"INFO","agent":"pro","phase":"opening","ping_no":1,"skill":"skill_pro.md","prompt_chars":1420,"prompt_sha256":"9f2c…","allowed_tools":["WebSearch"],"timeout_s":120,"outcome":"ok","duration_ms":7321,"session_id":"a1b2…"}
{"ts":"2026-05-31T09:14:03.901Z","schema_version":"1.00","event":"message","session":"session_001","pid":40113,"level":"INFO","msg_id":"m-001","sender":"pro","recipient":"judge","turn_type":"opening","ping_no":1,"word_count":171,"citations":["https://www.pewresearch.org/…"],"content_chars":1024,"content_sha256":"7ade…","tokens":612,"cost_usd":0.0143}
{"ts":"2026-05-31T09:14:03.902Z","schema_version":"1.00","event":"cost","session":"session_001","pid":40111,"level":"INFO","agent":"pro","ping_no":1,"call_cost_usd":0.0143,"input_tokens":410,"output_tokens":202,"cumulative_usd":0.0143,"budget_usd_max":5.0,"fraction_used":0.0029,"per_call_usd_max":0.5}
{"ts":"2026-05-31T09:15:10.550Z","schema_version":"1.00","event":"rejection","session":"session_001","pid":40111,"level":"WARNING","agent":"con","ping_no":2,"reason":"missing_citation","detail":"citations=[] but require_citation_per_turn=true","attempt":1,"retry_scheduled":true}
{"ts":"2026-05-31T09:18:42.110Z","schema_version":"1.00","event":"restart","session":"session_001","pid":40111,"level":"WARNING","agent":"con","dead_pid":40114,"new_pid":40140,"cause":"stall","restart_index":1,"replayed_context_ping_no":2}
{"ts":"2026-05-31T09:32:55.700Z","schema_version":"1.00","event":"verdict","session":"session_001","pid":40111,"level":"INFO","winner":"pro","pro_score":80,"con_score":73,"margin":7,"justification_chars":640,"justification_sha256":"c4f1…","decided_at":"2026-05-31T09:32:55Z"}
{"ts":"2026-05-31T09:32:55.900Z","schema_version":"1.00","event":"run_end","session":"session_001","pid":40111,"level":"INFO","outcome":"completed","total_pings":20,"total_cost_usd":0.41,"winner":"pro","duration_s":1135}
```

---

## 7. Event budget per debate (sizing the FIFO window)

For one configured run (`pings_per_side = 10`, so **20 turns** total, child→judge→child):

| Event | Count (typical) | Notes |
|---|---|---|
| `run_start` / `run_end` | 2 | One each. |
| `agent_call` | ~22–60+ | ≥1 per turn (20), +verdict call, + retries (each rejection adds one). |
| `message` | ~21+ | 20 debater turns + verdict; +relay messages if logged. |
| `cost` | ~22–60+ | One per `claude -p` call (mirrors `agent_call`). |
| `rejection` | 0–N | One per rejected/retried turn (bounded by retry policy). |
| `restart` | 0–6 | Up to `max_restarts_per_agent` (3) × 2 children. |
| `verdict` | 1 | No tie. |
| `log_rotated` | 0–N | Only if a file fills (500 lines). |

A clean run lands well under one rotated file; a noisy run (many retries/restarts) may rotate once or twice — still inside the 20-file window, so **a full session never evicts its own `run_start`** under normal operation. Tests force rotation with tiny config values (e.g. `max_lines_per_file=3`, `max_files=2`) to prove the invariants without generating 10k real lines.

---

## 8. Multiprocess concurrency policy

Three OS processes exist (judge/father, pro, con; A1) and the watchdog respawns children. Concurrency strategy for the shared `logs/` directory:

- **Single-writer model (chosen).** Only the **judge/father process** owns the `FifoLineRotatingHandler` and writes `debate.log`. Children (pro/con) **do not write the audit log directly**; they emit `ProtocolMessage`s and heartbeats over the `multiprocessing.Queue` to the father (see `docs/PRD_orchestrator.md`), and the father logs the corresponding events. This sidesteps multi-process file interleaving and keeps the exact line-count invariant (§4.2) trivially correct, because there is exactly one writer and one `self._line_count`.
- Children may still log to **console** for live operator visibility (the `console` handler is process-local and not line-counted), but the **authoritative FIFO file is father-only**. The `pid` field on every event records the *originating* process (carried in the queued message), so the audit still shows three distinct pids and restart pids even though one process performs the write.
- **ADR-LOG-002 (referenced in `docs/PLAN.md`):** single-writer father-owned log over per-process log files. Rejected alternative: one log file per process (e.g. `debate.pro.log`) — rejected because it complicates the "newest 20 files" FIFO accounting and makes the grader stitch three timelines together. The single father log gives one ordered, auditable timeline.

---

## 9. Secret scrubbing (the cyber layer)

**Requirement (rule 9 + playbook §3 task 9):** no key, token, or credential is ever written to a log. Although the project uses the `claude` CLI Max-subscription login with **no API key**, defense-in-depth still scrubs because (a) a user might place a `WEB_SEARCH_API_KEY` in `.env` for the fallback search backend, and (b) LLM-generated debate text could echo a string that *looks* like a secret.

### 9.1 Single source of truth
Scrubbing reuses **`Gatekeeper.scrub(text)`** from `src/cosmos77_ex02/shared/gatekeeper.py` (see `docs/PRD_gatekeeper.md`) — logging does **not** define a second redactor (rule 3, no duplication). `log_event` calls `scrub()` on **every string value** in the event dict (recursively for lists/nested dicts) immediately before JSON serialization, so redaction happens at the boundary, not at each call site.

### 9.2 What gets redacted (patterns, replaced with `***REDACTED***`)
- Anthropic-style keys: `sk-ant-…` and generic `sk-[A-Za-z0-9_-]{16,}`.
- Bearer tokens: `Bearer\s+[A-Za-z0-9._\-]+`.
- Generic `KEY=`, `TOKEN=`, `SECRET=`, `PASSWORD=` assignments (value redacted).
- Any value whose **env name** appears in `.env` (e.g. the literal value of `WEB_SEARCH_API_KEY`) — the Config loader supplies the set of `.env` values to redact by literal match.
- High-entropy long hex/base64 blobs over a length threshold are flagged conservatively (with care not to nuke legitimate URLs/citations).

### 9.3 What is deliberately *not* logged (avoid the need to scrub)
- **Full rendered prompts** → only `prompt_chars` + `prompt_sha256` (§6.1).
- **Full turn content** → only `content_chars` + `content_sha256` (§6.2); full text lives in the transcript.
- **Raw `claude -p` stdout** → only the typed, projected fields (cost, tokens, session_id).

Storing **size + SHA-256** instead of raw text gives reproducibility/audit (you can verify a transcript line hashes to the logged digest) while structurally preventing secret leakage and keeping lines short — supporting the bounded-disk goal G2.

### 9.4 Test obligation
`tests/unit/test_shared/test_logging_setup.py` (and a `scrub` test in `test_gatekeeper.py`) must assert: a fake `sk-ant-test-XXXX` placed in an event field is written as `***REDACTED***`; a `.env`-sourced fake `WEB_SEARCH_API_KEY` value is redacted; and a normal citation URL is **not** mangled.

---

## 10. Functional requirements → acceptance criteria

| ID | Requirement | Acceptance criterion |
|---|---|---|
| **L-1** | FIFO file handler keeps exactly newest 20 files × ≤500 lines, oldest dropped, config-driven. | **A11** |
| **L-2** | Every `claude -p` call emits an `agent_call` event (with `allowed_tools` proving WebSearch). | **A7**, **A9**, **A11** |
| **L-3** | Every routed message emits a `message` event; logs prove all edges go through the judge. | **A5**, **A6** |
| **L-4** | Every Gatekeeper accounting emits a `cost` event; `SDK.cost_report()` is reconstructable from logs. | **A11**, **A15** |
| **L-5** | Every rejected/retried turn emits a `rejection` event with a reason. | **A4**, **A7**, **A10** |
| **L-6** | Every watchdog kill/respawn emits a `restart` event. | **A11** |
| **L-7** | The final verdict emits a `verdict` event with unequal scores (no tie). | **A8** |
| **L-8** | All log values are scrubbed of secrets before write. | rule 9 (cyber) |
| **L-9** | All knobs come from `config/logging_config.json`; schema version validated. | rule 4, rule 10 |
| **L-10** | Rotation/eviction invariants are unit-tested on a temp dir with mocked I/O; no live LLM calls. | rules 6, 17 |
| **L-11** | `SDK.tail_logs(n)` returns the last N events in chronological order across the FIFO files. | **A12** (menu option [5]) |

### Non-functional requirements
- **NFR-1 Bounded disk:** ≤ 10,000 lines retained (20×500).
- **NFR-2 Robustness:** a logging failure never aborts the debate (§4.6).
- **NFR-3 Determinism:** rotation and scrubbing are pure given inputs; tests seed nothing live and mock the filesystem to `tmp_path` (rule 17).
- **NFR-4 Performance:** synchronous, flush-per-line writes are acceptable — log volume is small (≤ low thousands of lines/run) and the bottleneck is the multi-second `claude -p` call, not disk.
- **NFR-5 English-only:** UTF-8, English event names and details (project rule).

---

## 11. Testing strategy (TDD, Phase 2)

Tests in `tests/unit/test_shared/test_logging_setup.py` (and helpers), all using `tmp_path` and a **tightened config** so rotation is provable cheaply:

1. **Rotation at the line cap:** write `max_lines_per_file` lines → active file has exactly that many; write one more → rollover occurs, active file restarts at 1 line.
2. **Newest-N retention / oldest dropped (FIFO):** with `max_files=2`, write enough to force 3 rollovers → assert only `debate.log`, `debate.log.1`, `debate.log.2` patterns within the window, the oldest is deleted, and a `log_rotated` event records `dropped_file`.
3. **No file exceeds the cap:** `wc -l` (line count) on every file ≤ `max_lines_per_file`.
4. **One event == one line:** an event whose field contains `"\n"` still produces exactly one physical line and increments the count by one.
5. **JSON-lines validity:** every written line `json.loads` cleanly and carries the common envelope (`ts`, `schema_version`, `event`, `session`, `pid`, `level`).
6. **Schema version guard:** a mismatched `schema_version` raises before `dictConfig`.
7. **Restart line-count seeding:** re-opening an existing partially-filled `debate.log` seeds `_line_count` from the file so the next rollover is at the correct absolute boundary.
8. **Scrub integration:** secret-like fields are redacted (delegates to `Gatekeeper.scrub`); citation URLs survive intact.
9. **Failure isolation:** a simulated `OSError` on write routes to `handleError` and does not raise out of `emit`.

No test invokes the real `claude` CLI or writes outside `tmp_path` (rules 6, 17).

---

## 12. File layout and the 150-line cap

| File | Responsibility | Cap |
|---|---|---|
| `src/cosmos77_ex02/shared/fifo_handler.py` | `FifoLineRotatingHandler` (rotation + FIFO eviction + line guard + `log_rotated`). | ≤150 lines (rule 1) |
| `src/cosmos77_ex02/shared/logging_setup.py` | `init_logging()` (load+validate `logging_config.json`, run `dictConfig`), `log_event` + the typed `log_*` wrappers, scrub integration. | ≤150 lines (rule 1) |
| `config/logging_config.json` | All knobs (already authored in Phase 0). | n/a |
| `src/cosmos77_ex02/shared/gatekeeper.py` | Owns `scrub()` (reused, not duplicated). | ≤150 lines (see `docs/PRD_gatekeeper.md`) |

Splitting the handler out of `logging_setup.py` is the deliberate response to the 150-line cap; both stay well under by keeping event-dict construction in tiny `log_*` wrappers.

---

## 13. Cross-references
- `docs/PRD_gatekeeper.md` — owns `scrub()` and emits `cost` / `budget_warn` / `budget_stop` events (§6.3, §6.9, §9).
- `docs/PRD_ipc_protocol.md` — defines `ProtocolMessage`, the source of `message` events (§6.2) and the child→judge→child routing this log audits (A5).
- `docs/PRD_orchestrator.md` — owns `transcripts/session_NNN.json` (the human artifact that the SHA-256 digests in §6 reference) and emits turn-level events.
- `docs/PRD_watchdog.md` — source of `restart` events (§6.5).
- `docs/PRD_judge_agent.md` — defines `Verdict`, the source of the no-tie `verdict` event (§6.6, A8).
- `docs/PRD_terminal_menu.md` — menu option [5] "Tail logs" and [6] "Cost report" consume these logs via the SDK (L-11, L-4).
- `docs/PLAN.md` — ADR-LOG-001 (bespoke line-rotating handler) and ADR-LOG-002 (single-writer father-owned log) are registered there.
