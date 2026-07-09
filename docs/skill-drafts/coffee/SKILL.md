---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Strategy-codex operator cadence and tempo. Primary trigger: coffee. Step 2 = hub A-D only (Confirm / Test / Deepen / Reframe), each line naming one specific repo-grounded suggested action (not bare labels). Default attention inferred from hub letter (CONDUCTOR-COMPRESSION-SPEC §4). Legacy master slugs redirect to coffee. Before Step 1, Recent rhythm. Signing-off: same A-D action menu; closeout in Step 1. Coffee also acts as the default checkpointed re-entry ritual."
category: operator-coherence
status: active
scope_class: repo-governed
---

# Coffee

**Preferred activation (operator):** say the exact phrase **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D** hub menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

`coffee` is also the default checkpointed re-entry ritual. In a fresh chat, it should resume from the most recent authoritative checkpoint on disk, using cadence and handoff state to recover orientation. If more than one plausible checkpoint exists, prefer the latest on-disk authority and surface the ambiguity instead of guessing. This is a checkpoint, not a transfer seal: it restores continuity, but it does not commit, push, or generate a bridge packet.

**Coffee Hub Menu (terminology):** **`coffee` Step 2** fixed **A–D** hub (**Confirm / Test / Deepen / Reframe**) is the **Coffee Hub Menu**. Each line is **`Letter. Label — specific suggested action`** grounded in Step 1 (paths, scripts, slices, falsifiers); seeds from `scripts/assess_session_load.py`. **Default attention from hub (Phase 2):** infer silently — **A** *(none)*, **B** `precision pass`, **C** `hold tension`, **D** `one object only`; override with plain phrase in same message (`C stakes pass`, `D long arc pass`). Full matrix: [CONDUCTOR-COMPRESSION-SPEC §4](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#4-attention-model--default-from-hub-primary). **Legacy conductor slugs** (`toscanini`, `karajan`, …) **redirect** to **`coffee`** + hub — [conductor SKILL redirect](../conductor/SKILL.md). Layer map: [CONDUCTOR-LAYER-MAP.md](../../../docs/skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md).

**Legacy label compatibility:** Older checks and notes may still refer to **Steward / Engineer / Statecraft / Singularity** as the coffee hub. Treat those as compatibility residue only. Live coffee now chooses a **learning action first**, then routes into the owning downstream territory only if that action needs a specific bench.

**Downstream routing law:** `statecraft` and `singularity` remain the two primary operator channels in the repo, but they are no longer the top-level coffee choices. `Confirm`, `Test`, `Deepen`, and `Reframe` decide the kind of next move; downstream routing decides where that move belongs.

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Do not overload each run with every possible obligation or stale thread.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.
- **Encoded workflow first:** Before giving generic elicitation, ad hoc process advice, or a fresh workaround, check whether the repo already defines a coded ritual for the task. If it does, route through that path first.
- **Deviation rule:** Only improvise when the coded path is missing, broken, or explicitly out of scope, and say why you are deviating.
- **Canonical examples:** Statecraft promotion: archive -> synthesis -> notes -> essays. Fork revive only: stage -> approve -> process via gate. Root-layout migration should repair path assumptions rather than invent compatibility directories.
- **Strategy-codex deprecation guard:** Do not route active coffee work through `companion-self` template sync or Grace-Mar-vs-template reconciliation unless the operator explicitly asks for that legacy/archive lane. Bare **A. Confirm** means validate the live slice on strategy-codex-native terms, not reopen legacy stewardship assumptions.

## Relation to dream

`coffee` and `dream` form a biological-cognitive pair:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)
- **Attention / work-pass (Phase 2):** Hub pick + default attention phrase replaces standalone conductor stance. Log optional `attention=` on `coffee_pick` only when overriding hub default.
- **Active arc (legacy):** Historical `coffee_pick picked=conductor conductor=<slug>` rows remain read-only in cadence rollups.
- **`coffee_close`** = post-branch receipt (extended Phase 1+): `picked`, `outcome`, `readiness`, optional `object_ref`, `falsify`, `verdict`, `attention`, `loops`, artifacts. WORK telemetry only.

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` § *Cadence choreography* for the day's sequence and data handoff.

**Coffee -> dream handoff (Phase 3):** Substantive passes need **extended `coffee_close`** with `object_ref` + `falsify` when honest. **`coffee_conductor_outcome` is deprecated** — do not log new outcome lines for strategy-codex; legacy rows remain read-only in rollups. Dream reads **`work_pass_rollup_24h`** from extended closes.

<a id="conductor-only-no-coffee"></a>

## Legacy conductor triggers (redirect — Phase 2 compression)

**Do not** open standalone Conductor or Conductor Action Menu on new sessions.

When the operator says **`toscanini`**, **`furtwangler`**, **`karajan`**, **`kleiber`**, **`bernstein`**, **`conductor`**, or **`conductor <name>`**:

1. **Redirect once:** Conductor is compressed into **`coffee`** + hub letter + default attention — [CONDUCTOR-COMPRESSION-SPEC §10](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#10-operator-cheat-sheet).
2. Run **`coffee`** Step 1 if not already done this turn.
3. Offer **Coffee Hub Menu A–D** with default attention on recommended line (from `assess_session_load.py`).
4. Run matching **object ritual** ([§5](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#5-migration-table-and-object-rituals)) — not Allegro/Andante/Scherzo/Finale.

**Open loops (replaces `build_conductor_revisit_block`):** Step 1 **Recent rhythm** prose; bootstrap **Open loops** when `coffee_close` carries `loops=`; live **72h watch** / daily sheets when statecraft is active — advisory, not a second menu.

**Close:** [extended `log_coffee_close.py`](../../../scripts/log_coffee_close.py) + [CONDUCTOR-CLOSE-TEMPLATE.md](../../../codex/CONDUCTOR-CLOSE-TEMPLATE.md) when notebook paste helps. **`verdict=promote|shaped`** → mandatory RLJ append ([recursive-learn](../recursive-learn/SKILL.md)).

**`bravo` / `weak`:** [§5.4 compression spec](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#54-bravo--weak-on-object-rituals) — not coffee-hub **B** unless operator picks Test.

**Legacy read-only:** [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md), [conductor SKILL](../conductor/SKILL.md) redirect stub, cadence `picked=conductor` rows.

<a id="hub-e-auto-continue"></a>

**Removed:** Standalone Conductor continuation, auto-continue movement letters, and Conductor action MCQ — use hub pick + object ritual steps instead.

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**.

**Fresh chat default:** If `coffee` is the first command in a new strategy-codex chat, resolve a Python executable **before** any coffee script runs. Do not assume `python`, `python3`, or `py` is on `PATH`.

**Python resolution order for new-chat coffee:**

1. Prefer a repo-local virtualenv interpreter when present:
   `../../../.venv/Scripts/python.exe`
2. Otherwise prefer a working shell executable in this order: `python3`, then `python`, then `py -3`.
3. If none of those resolve, load the Codex bundled workspace runtime and use its Python:
   `C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
4. Reuse that resolved interpreter for the entire coffee flow in the current chat (`operator_coffee.py`, warmup scripts, handoff scripts, cadence helpers, and ad hoc `pytest` checks).
5. If no interpreter is available even after the bundled-runtime fallback, say so explicitly and fall back to manual read-only reconstruction of the coffee checkpoint.

After resolution, use the executable first-command bootstrap with the resolved interpreter:

```bash
<python_cmd> scripts/operator_coffee.py -u strategy-codex --mode first-command
```

This prints a **Coffee Bootstrap Brief** first, then runs an **inline fast Step 1** (one Python process, one shared `git status` scan — typically seconds, not minutes). The brief includes git state, cadence rhythm, and hub recommendation; **Repo identity**, **gh auth**, and **pytest subprocess probes** are skipped in fast mode (use `--verbose` for full underlying blocks, `--subprocess` for the legacy subprocess chain). Ordinary in-thread `coffee`, `coffee light`, `coffee minimal`, and signing-off behavior stay unchanged.

<a id="harness-hang-recovery"></a>

### Harness hang recovery (Windows / long threads)

**Symptom:** `Read`, `Shell`, or `Glob` returns *Interrupted by the user after ~300000ms+* with no stdout — usually a **harness timeout**, not operator cancel and not a repo script failure.

**Do not** retry the same parallel batch (full `operator_coffee.py` + multiple reads + grep).

**Fast recovery (same turn must still show Step 2 hub menu):**

1. Operator may say **`fast tools`** or **`read only`** — then **Read/Write + one Shell only** ([agent-tool-latency-discipline.mdc](../../rules/agent-tool-latency-discipline.mdc)).
2. Step 0 rhythm — one Shell:
   ```bash
   python3 scripts/cadence_recent_rhythm.py --ritual coffee
   ```
3. Step 1 ship snapshot — one Shell:
   ```bash
   python3 scripts/operator_handoff_check.py --fast
   ```
4. Synthesize **Recent rhythm** prose from cadence output; paste handoff **Ship receipt** block.
5. Run `python3 scripts/assess_session_load.py -u strategy-codex` when feasible; use **Annotated menu** seeds plus Step 1 slices to build the **action hub menu** (see [Step 2 — Hub menu](#coffee-step-2-hub)).
6. Emit the full **Coffee Hub Menu — Reply A–D** immediately — **four action lines**, not bare labels. **Do not** end on “starting now.”

**Signing-off under hang:** skip heavy `operator_coffee.py --mode closeout`; use `--fast` handoff only unless the operator explicitly asks for full closeout.

**Operator finish phrase:** **`fast tools and finish <task>`** = bounded Read/Write first, then **one** combined git or validator Shell for the named task.

For Step 0 recent rhythm, prefer the shared executable formatter in `scripts/cadence_recent_rhythm.py --ritual coffee` over manual log synthesis. `scripts/coffee_bootstrap_brief.py` already delegates to that helper. It reads `coffee_close` receipts first, names readiness / artifact anchors / repeated unresolved loops, and keeps the first screen free of timestamp walls.

### Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `operator_coffee.py` appends a new **`coffee`** line at the **end** of a successful run, so the log must be read **before** those commands if the rhythm read is to exclude this session.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 4** such lines already in the file. If there are fewer than four, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply. When a recent `coffee_close` exists, prefer it over the preceding `coffee` start line for the same branch because the close receipt says what actually happened.
3. **Synthesize in plain prose** — **2–4 short sentences** for a human, **not** a telemetry dump: **do not** lead with a wall of `key=value` pairs. **Companion-facing UX:** label this block **Recent rhythm** (or prose only); **do not** put **dates, UTC, or clock times** in this prose (use order and light anchors like "after dream," "then bridge," "earlier today" without timestamps). **Must anchor in specifics** from those four lines — name what actually happened (e.g. **bridge** with **commit refs** if present, **coffee** **work-start** vs **standard**, **coffee_close** readiness/runtime/artifacts/unresolved loop signal when present, **coffee_pick** / **conductor** when present, legacy **`thanks`** **park** text when non-empty, **dream** pass/fail or integrity/governance in ordinary words, **harvest** packet vs not). **Avoid** generic process filler that could apply without reading the file. Do **not** paste raw log lines unless they are already very short.

   **Cadence voice:** Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided, end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen, grounded, and ready** — not debriefed. Name what was learned or decided, not what was executed. No commit hashes, no process names — warm, direct, future-facing.
4. In the reply, place **Recent rhythm:** at the **top** of Step 1 content (immediately before script output / warmup paste). Same rule for **signing-off** Step 1 (before `operator_coffee.py --mode closeout` or handoff-only flow).

If the file is missing or empty below the anchor, state that under **Recent rhythm** and continue Step 1.

### Step 1 — Automated actions (one flow, two weights)
### Statecraft C - router-first statecraft routing
**Detect intent**
**Operator intent (strategy-codex default):** **coffee -> C - Statecraft** does **not** auto-run daily brief, `check streams`, bookshelf elicitation, or archived Tri-Frame. It presents a router-first repo-root statecraft entry:

- **A. Deploy** - route to `state-deploy` when lane ownership is unresolved.
- **B. Compact** - route to [statecraft/compact/README.md](../../../statecraft/compact/README.md) when the object is already cross-lane, objection-shaped, or mechanism-shaped.
- **C. Speaker-Bridge** - route to `statecraft-bridge` only when Persia/Iran ownership is already clear and the unresolved question is retrieval profile rather than lane ownership.
- **D. Lane Direct** - open the secondary lane menu only when ownership is already clear:
  - **A. America** - route to [America](../../../statecraft/america/README.md) when the drafting problem is hegemonic order under strain, legitimacy, burden-sharing, and bounded command.
  - **B. China** - route to [China](../../../statecraft/china/README.md) when the drafting problem is continuity, energy stability, industrial rhythm, and anti-chaos order management.
  - **C. Persia** - route to [Persia](../../../statecraft/persia/README.md) when the drafting problem is dignity, sovereignty, chokepoint leverage, recognition, and sanctions endurance.
  - **D. Russia** - route to [Russia](../../../statecraft/russia/README.md) when the drafting problem is strategic depth, disruption, recognition, and optionality without entrapment.

After routing, treaty frameworks, policy papers, negotiation briefs, and Richelieu/Bismarck stress tests become the next drafting moves inside the chosen path rather than the first coffee submenu.

**Statecraft grounding:** convert sources into instruments, not commentary. When source material matters, name the actor, interest, institutional carrier, leverage point, and proposed instrument before drafting. When a draft needs historical, civilizational, or empire-pattern grounding, prefer [civ-state](../../../statecraft/states/README.md) as the active Civilization and Empire source base; keep `ph-civ` public-facing and `CIV-MEM` legacy/provenance-only. Useful sheets include [speaker-insight-to-policy-memo.md](../../../statecraft/sheets/speaker-insight-to-policy-memo.md), [comprehensive-power-vs-coercive-center.md](../../../statecraft/sheets/comprehensive-power-vs-coercive-center.md), and [sovereignty-under-acceleration.md](../../../essays/sovereignty-under-acceleration.md).

**AI essay routing cue:** when a new session reopens AI-adjacent writing, prefer **D. Singularity** for mediation, anthropology, authorship, synthetic judgment, human formation, and acceleration-substrate questions. Prefer **C. Statecraft** for office, legitimacy, authority, Rome, civilizational carry, settlement, and command questions. In this repo, **Barnes on AI** is `statecraft`-only and should not reopen as a generic singularity AI essay.

When the operator asks for the daily main-stream update (Davis, Diesen, Alkorshid/Dialogue Works, Napolitano/Judging Freedom, Mercouris), route that through the explicit **`check streams`** skill, not through Coffee C by default. `cognition streams` remains a legacy alias.

When the operator asks for daily brief, Polymarket/polling, **`periodic-statecraft-review`** / legacy `last30days`, or broad current-events judgment, use explicit daily-brief / strategy / check-streams routes. When the operator names a specific recent event for statecraft analysis, verify the unstable fact pattern, name the crisis object, then route through `state-deploy` or the owning lane rather than opening a separate event skill.

Bookshelf/museum identity knowledge (archive) elicitation, survey work, and Record candidates are explicit routes outside Statecraft unless the operator asks to turn source knowledge into a policy/treaty instrument. Never merge Record material from Coffee C; preserve WORK-only boundaries.
**Signing-off Step 1** — handoff-weighted (same trigger **`coffee`**, not a second ritual name):

```bash
python3 scripts/operator_coffee.py -u strategy-codex --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u strategy-codex`. Include the output in your reply. Add a **short paragraph**: what moved today, what is parked, gate + Jiang carryovers, suggested re-entry prompt. Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

If the operator **explicitly** wants **both** full warmup **and** signing-off in one message, run work-start then append handoff (rare).

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup includes a last-dream block from `last-dream.json` (**"Last dream (night handoff)"** when there is something to read out, or a **one-line "quiet handoff"** when `integrity` / `governance` / digest counts are clean and there are no followups). A successful dream may add **`last_coffee_echo`**: a single warm line from the 24h cadence rollup that ties yesterday's `coffee` into morning startup, plus one line **`Dream -> coffee action:`** naming the recommended learning move (**A Confirm / B Test / C Deepen / D Reframe**). Treat those as operational hints only, never as policy or Record authority. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, explicit daily brief / intel defer line when relevant, optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message. Coffee now recommends a learning action first; downstream `statecraft` or `singularity` routing only appears when that action needs a specific bench.

**Memory observability:** `operator_coffee.py` may print a single **`Memory observability:`** line after lane hints when the derived continuity dashboard is `watch`, `stale`, or `missing`. Do not paste the full dashboard into coffee. If the line is absent, treat memory observability as quiet/ok for this run. The dashboard is WORK-derived only; it does not edit MEMORY, the Record, or the gate.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

### Dashboard nudge (Phases 1–3 aggregators — mandatory after Step 1)

The operator starts with **`coffee`** and cannot be expected to remember when to run Repo Surgeon, Statecraft War Room, or Operator Command Deck. After Step 1 script output and **before** the Coffee Hub Menu, emit a short **Dashboard nudge** block (3–5 lines).

**SSOT:** [docs/operator-dashboard-when-to-use.md](../../../docs/operator-dashboard-when-to-use.md)

**Rules:**

1. **Always** suggest **Command Deck** on work-start / reorientation `coffee` — default companion to the hub menu (`python3 scripts/operator_command_deck.py --max-next-actions 5` → open `runtime/artifacts/operator-command-deck/latest.md`).
2. Suggest **at most one** drill-down dashboard when Step 1 signals match (War Room for statecraft/intake/daily; Surgeon for docs ship / integrity / hub **B**).
3. Each line: tool name + **because** + optional one-line command. **Do not** paste full `latest.md` unless the operator asks.
4. When the operator picks a hub letter or says **`run deck`** / **`run war room`** / **`run surgeon`**, **run that script same turn** and summarize (exit code + top findings/actions).

**Example shape (adapt to live Step 1 — not a fixed template):**

```text
**Dashboard nudge**
- **Command Deck** — dirty tree + ranked next actions; run `python3 scripts/operator_command_deck.py --max-next-actions 5` and keep `latest.md` open beside this thread.
- **War Room** — statecraft slice uncommitted; run if you pick **C — Deepen** (`python3 scripts/statecraft_war_room.py --latest-days 7`).
```

Signing-off `coffee`: nudge Deck regenerate after closeout for tomorrow's on-disk cockpit (optional one line).

**Done when:** Script output is Step 1 context only. The assistant-facing reply is not complete until Recent rhythm is at the top, the **Dashboard nudge** block is present (unless operator said **`no menu`** / **`no options`**), and the full **Coffee Hub Menu - Reply A-D** follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

<a id="coffee-step-2-hub"></a>

### Step 2 — Hub menu (four action lines)

Immediately **after** Step 1 content, output the **hub** menu — **four lines** (**A–D**). Each line names the **learning action** **and** one **specific suggested action** for this session.

**Required line shape:**

```text
**A. Confirm** — <one concrete repo-grounded action>
```

Same pattern for **B. Test**, **C. Deepen**, **D. Reframe**. Use an em dash (`—`) between label and action.

**One option per line:** Each hub letter is **its own line** — not multiple letters on one line and not a single paragraph. If a chosen learning action later opens a bounded downstream menu, that second-layer menu is separate from this rule.

**How to word the action (mandatory):**

1. **Seed from scripts:** Run `python3 scripts/assess_session_load.py -u strategy-codex` (or read the **Session load** / **Annotated menu** block when `operator_coffee.py` already ran). Use `option_weights[A|B|C|D].note` as the **learning-action seed** for that letter.
2. **Instantiate from Step 1:** Translate each seed into a **single executable move** using live context from Step 1 — handoff **Uncommitted slices**, recent commits, **Suggested push**, dream **Learning action**, **open loops**, **artifact anchors**, and thread-local work. Name **paths**, **scripts**, **commits/slices**, or **falsifiers** where honest.
3. **Recommended letter:** When Step 1 prints `Recommended default: X`, mark that hub line with `*(recommended)*` after the label. When `assess_session_load` supplies **default attention**, echo it on the recommended line only (e.g. `**D. Reframe** *(recommended)* — one object only — …`). Override only when operator named a phrase in the same message (`C stakes pass`).

**Good action clauses (session-specific):**

- `Commit the ph-civ drift slice (~73 files) separately from the ahead-1 tooling commit, then push when slices are clean.`
- `Run python3 scripts/check_academy_mirror_sync.py --mirror ph-civ to falsify whether ship-ready still matches live drift.`

**Forbidden on the hub list:**

- Bare labels with no action clause (`A. Confirm` alone).
- Generic seeds copied verbatim with no repo anchor (`validate follow-through when prior judgment still looks right` with no path, slice, or script).
- Extra hub lines, micro-hints rows, fork shorthand, or F/G/Xavier/Dev tags **under** the four lines.

**Letter-collision:** There is no Conductor Action Menu on new sessions. If a downstream bounded submenu uses A–D letters, **label** it explicitly (e.g. Statecraft router, Singularity menu).

**Do not** append master-slug rows under the four hub lines; legacy conductor triggers redirect to [compression spec §10](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#10-operator-cheat-sheet).

**Hub menu (example shape — actions must match the live session, not this sample):**

```text
**Coffee Hub Menu — reply A–D**

**A. Confirm** — Commit the wip-slice-commits stack: separate ph-civ drift from the ahead-1 tooling commit, then push when slices are clean.
**B. Test** — Run `python3 scripts/check_academy_mirror_sync.py --mirror ph-civ` to falsify whether ship-ready still matches live drift.
**C. Deepen** — Populate `public/civ-state/` via `sync_public_civ_state_mirror.py` and read `public/README.md` until the two-mirror workflow is clear enough to act.
**D. Reframe** *(recommended)* — Pick one live object only: ph-civ drift commit, civ-state populate, or push-only the committed slice — not all three.
```

**Hub lines end at D:** the coffee hub is four action lines only. Legacy conductor slugs redirect to hub + attention ([Legacy conductor triggers](#conductor-only-no-coffee)).

**Mission-control note:** the coffee hub now chooses a **learning action** first. Downstream territories such as steward, engineer, statecraft, or singularity are second-layer consequences after the operator picks Confirm, Test, Deepen, or Reframe.

**Pope Leo split cue:** if the live object is `Pope Leo on AI`, singularity owns mediation, anthropology, synthetic judgment, authorship, and human formation. If the governing nouns become papal office, legitimacy, Rome, authority, or civilizational burden-bearing, route back across the handoff into `statecraft` rather than widening the singularity branch.

When hub **D** is chosen, reply with a bounded **Singularity menu - reply A-D** unless the operator already named a specific Singularity artifact:

- **A. Frontier pulse** - name the current acceleration from the latest Innermost Loop / Moonshots sheet.
- **B. Agent control plane** - map who holds objective, memory, permissions, rollback, and accountability.
- **C. Alignment/substrate warning** - test substrate capture, displacement, or misaligned delegation risk.
- **D. Reuse artifact** - produce an agency map, bridge question, warning card, or strategy note.

**Legacy Capitalist / bookshelf product use:**

- Bookshelf may support offer design, teaching angles, grace-gems packaging, course/product framing, or public copy.
- Do **not** use D or C as the default route for museum knowledge section A bookshelf recursion; route that to explicit `elicit-knowledge`, survey, or bookshelf membrane workflows unless the operator asks to convert bookshelf material into a statecraft artifact.
- **Catalog stance membrane** (`bookshelf-membrane-round.json` + `build_bookshelf_membrane_candidates.py`) remains secondary and scripted: use it only when the operator requests catalog organization or a pressing organizational membrane issue applies.

**Legacy Capitalist routing:** commercial, bookshelf-product, grace-gems, offer, and `skill-write` work no longer owns coffee D. Route explicit commercial or write-shaped requests by named lane/request outside coffee, or through **B. Engineer** when the operator asks for implementation. Use **C. Statecraft** only when the requested output is treaty, policy, negotiation, institutional, sanctions, alliance, sovereignty, or state-interest shaped.

**Catalog stance membrane (scripted path only — branch 2 above):**

- Session is **multi-round**: 5–10 MCQs per round when using the scripted stance round artifact.
- After each round, ask continue/stop.
- On stop, produce:
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-REPORT.md`
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`
- Output is draft-only; no direct writes to `recursion-gate.md` unless explicitly requested.

**Write-shaped** work is **not** an extra letter - it routes by explicit **`write`** / **`skill-write`** / commercial request, or when the operator says **`write`** / **`skill-write`** without **`coffee`**. Do not add a separate micro-hints row.

**Standalone Conductor:** the coffee hub ends at D. Direct Conductor activation uses a master name, `conductor`, or the standalone conductor skill.

**Step 1 context for B / D:** `operator_coffee.py` prints **`Lane context (for hub B / D — Engineer & Singularity hints)`** — two lines from `scripts/coffee_lane_next_hints.py` (work-dev + singularity-academy). Use when choosing **B**, **D**, or when wording those lines.

**Step 1 context for standalone Conductor:** After lane hints, `operator_coffee.py` prints the four-line coffee hub only; Conductor is handled separately.

**Default recommendation line:** Step 1 may print `Session load: … (recommended: X)` and `Recommended default: X — say "go" to accept, or pick another hub letter.` When present, surface that line once before or after the hub menu; the matching hub line also carries `*(recommended)*`. The hub menu still remains **four action lines** only — never bare labels. For **Conductor** emphasis outside the hub, say **once** that **`conductor`** / master name works **without** opening **`coffee`** ([§ Conductor session](#conductor-only-no-coffee)). **Not** micro-hints under the hub list.

**Quick reference (modes):**

- **A. Confirm / Steward** — **boundary hygiene** \| **integrity/exports** \| **git/ship** \| **gate** (fork revive only). **Default if the operator says `A` only:** **git/ship** when worktree pressure; else **boundary hygiene**. **`A gate`** only when operator revives fork ([`grace-mar-instance-boundary.md`](../../../docs/grace-mar-instance-boundary.md)). **`A integrity`** / **`A git`** / **`A ship`** → that track; **`A both`** / **`A all`** as in [menu-reference — Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`. Template-sync work is legacy/archive-only unless named explicitly. *(Legacy hub letter **B**.)*

- **B. Engineer** — **work-dev + skills/meta** (not git/ship or full membrane audits — those are **A**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **B**. **work-cici** ops when engineering-shaped. **When hub B is chosen:** After **one short orientation line**, deliver **Engineer next moves** — **3–5 options** labeled **A through E** (**or A–D** if four), **each option its own line**, under an explicit heading such as **`Engineer menu — reply A–E`** — **not** `B1`–`B5` and not unlabeled lists. Each new submenu **restarts letters from A**; disambiguate from the **Coffee hub** with the menu title (same idea as **letter-collision** labeling for Conductor action MCQ vs hub). Each line is a **repo-grounded** plausible next step (work-dev wedge, script, CI, **skills** path) — **enumeration only** until the operator picks. Use Step 1 **`Lane context (for hub B / D)`** and [workspace.md](../../../docs/skill-work/work-dev/workspace.md) § **Next actions** when helpful. **Detail:** [menu-reference § Engineer (B) — detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) *(legacy letter **Build** / old hub **A**).*

- **C. Statecraft** - Opens the repo-root statecraft routing front door. Do **not** auto-run daily brief, `check streams`, bookshelf elicitation, or archived Tri-Frame before this submenu. Output one short orientation sentence using deployer pressure grammar, then:
  - `Statecraft router - reply A-D`
  - `A. Deploy - lane ownership unresolved`
  - `B. Compact - cross-lane or objection-shaped object`
  - `C. Speaker-Bridge - Persia/Iran speaker-heavy object after ownership is clear`
  - `D. Lane Direct - ownership already clear`
  - exact CIV-STATE follow-on is also valid here: **`civ-state`** opens the upstream CIV-STATE bench for `Frame / Retrieve / Promote / Review`, rather than routing directly into lanes or book-writing (legacy alias: `statecraft civ-state`)

  Use recommendation law:
  - recommend **A** when ownership is still unsettled
  - recommend **B** when the object is already multi-actor and mechanism-shaped
  - recommend **C** only when Persia/Iran ownership is already clear and the remaining uncertainty is Marandi-vs-Parsi retrieval
  - recommend **D** when the lane is already explicit

  Branch behavior:
  - **A** routes directly to `state-deploy`
  - **B** opens [statecraft/compact/README.md](../../../statecraft/compact/README.md)
  - **C** routes to `statecraft-bridge`, but if ownership is still unresolved it must hand back to `state-deploy`
  - **D** opens:
    - `Lane Direct - reply A-D`
    - `A. America - hegemonic order under strain`
    - `B. China - civilizational stabilizer`
    - `C. Persia - deep civilization, dignity, leverage, recognition`
    - `D. Russia - strategic depth, disruption, optionality`

  After a lane-direct pick, route to the corresponding lane front door: [America](../../../statecraft/america/README.md), [China](../../../statecraft/china/README.md), [Persia](../../../statecraft/persia/README.md), or [Russia](../../../statecraft/russia/README.md). Then open the lane's transcript-grounded intake menu first. The live intake law is `Statecraft Archive -> Statecraft Synthesis -> host law -> bridge if needed -> lane drafting`. Outside coffee, direct fast paths still belong to `state-deploy` for lane selection and `state-america`, `state-china`, `state-persia`, or `state-russia` for lane-owned drafting. Treaty frameworks, policy papers, negotiation briefs, and Richelieu/Bismarck stress tests remain downstream drafting moves after intake and routing. **Statecraft source use:** sources become instruments. Use [statecraft.md](../../../statecraft/statecraft.md), [METHOD.md](../../../statecraft/METHOD.md), [civ-state](../../../statecraft/states/README.md), [treaty-framework.md](../../../statecraft/templates/treaty-framework.md), [policy-paper.md](../../../statecraft/templates/policy-paper.md), [negotiation-brief.md](../../../statecraft/templates/negotiation-brief.md), [richelieu.md](../../../statecraft/lenses/richelieu.md), and [bismarck.md](../../../statecraft/lenses/bismarck.md) after intake and routing. Current-events watches, daily briefs, and stream checks remain explicit routes; specific recent-event analysis should start with brief verification plus `state-deploy` or a direct lane handoff before becoming a statecraft artifact. **Post-intake closeout:** after archive land, run sync check then intake queue report per [menu-reference — Statecraft intake closeout](../../../docs/skill-work/work-coffee/menu-reference.md#statecraft-intake-closeout) before daily synthesis or ship. *(Legacy hub **C - Strategist / daily brief** is compatibility-only.)*

- **D. Singularity** - **singularity-academy** WORK module: agency under acceleration, agent control planes, alignment/substrate/displacement tests, and reusable strategy artifacts. When hub D is chosen, open a bounded **Singularity menu - reply A-D** or recommend one default from that module.

- **Conductor** — standalone only; not part of the coffee hub.

**Composition benchmark note:** Coffee only routes to Conductor/Kleiber; it does **not** run benchmarks directly or add a standalone benchmark hub item. In V1, Strategy-codex composition benchmarks run only from the resolved **Kleiber** Conductor Action Menu as fixed **D. Finale** (`Run composition benchmark`) per [kleiber-composition-benchmark.md](../../../docs/skill-work/work-dev/kleiber-composition-benchmark.md).

**Exit / re-offer:** After **A**, **B**, or **D**, re-offer the full **coffee** hub **A–D** after the current branch settles. If a standalone Conductor turn was opened, stay on the Conductor track rather than re-offering coffee in the same reply. After **C**, exit to normal workflow unless **`stay in coffee`**. After **A** (Steward), see [menu-reference § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) *(legacy docs may still say **B** for Steward → read **A**).* Synonyms **`A+ship`** / **`EXECUTE`** → **Implement now** on steward track. **Decision-fatigue rule:** after a hub branch opens one submenu, the next assistant turn should execute the selected item, recommend one default, or report the blocker rather than opening another broad menu.

**Ending discipline:** When `coffee` or a downstream branch ends in a bounded menu or MCQ, stop on that menu. Do **not** append open-ended closers such as "if you want" after the menu; the choice list is the operator-facing close.

Legacy **A-G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe historical workloads. Current map: Statecraft -> C; Build -> B; Steward -> A; singularity-academy module -> D. Daily Brief / `check streams`, museum identity knowledge (archive) elicitation, Book / Jiang / Predictive History, and commercial / teaching bookshelf work now route by explicit request unless the operator asks to turn them into a statecraft artifact. Symphony conductors are standalone by `conductor` / master name without `coffee`.

**Done when:** The operator has picked **A-D** (or a named standalone Conductor), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

<a id="cadence-audit"></a>

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required. The line always includes **`cursor_model=…`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "…"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **A**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:
`python3 scripts/log_cadence_event.py --kind coffee_pick -u strategy-codex --ok --kv picked=A learning_action=confirm --cursor-model "<from Cursor UI>"`
(`learning_action=` values: `confirm`, `test`, `deepen`, `reframe`.) For **hub** picks: **`picked=A`..`D`**. Legacy **`picked=conductor`** rows remain read-only. **Closure after a substantive pass (Phase 3):** `python3 scripts/log_coffee_close.py -u strategy-codex --picked D --outcome partial --readiness execution_ready --object-ref docs/path.md --falsify one-line-test` — do **not** append new `coffee_conductor_outcome` for strategy-codex. Optional: `scripts/log_operator_choice.py --context COFFEE --picked A` for `session-transcript.md`.

**After a selected coffee branch materially settles**, append a **`coffee_close`** receipt when it would help the next coffee or dream understand the real outcome:
`python3 scripts/log_coffee_close.py -u strategy-codex --picked B --outcome partial --readiness execution_ready --artifact scripts/example.py --loop recurring-loop-slug --next run-tests`
For conductor-backed closes, add `--picked conductor --conductor <slug> --conductor-state open|closed`. `readiness=orientation` means live but not actionable; `execution_ready` means ready to implement; `ship_ready` means ready for staging/commit review; `blocked` means do not claim progress until repaired.

## Related files

- `docs/skill-work/work-cadence/README.md` — **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — cadence, survey track, signing-off add-ons; legacy **A–G** workload tables (map to the current coffee Step 2 above)
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `.cursor/skills/thanks/SKILL.md` — **`thanks`** **deprecated** for the single-operator workflow; prefer **conductor** or **`coffee` light/minimal`
- `docs/skill-work/work-politics/polling-and-markets.md` - KY-4 polling by explicit request, not Coffee C by default.
- `docs/skill-work/work-strategy/daily-brief-minds-menu.md` - archived Tri-Frame **three minds** (Barnes / Mearsheimer / Mercouris) by explicit synthesis request, not Coffee C by default.
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
- `.cursor/skills/state-deploy/SKILL.md` - verified named recent events now dissolve into lane deployment rather than opening a separate event function.
- `.cursor/skills/elicit-knowledge/SKILL.md` - explicit MCQs toward museum knowledge section A / gate staging, outside Coffee C unless converted into a statecraft artifact.
