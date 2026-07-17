# Narrative Systems Local Cadence

Every assistant response to the operator in this workspace should include
multiple-choice options for what to do next. Keep the menu concise and
grounded in the current task.

When the operator says `coffee`, read
`docs/skill-drafts/coffee/SKILL.md` completely and follow it.

When the operator says `dream`, read
`docs/skill-drafts/dream/SKILL.md` completely and follow it.

When the operator says `harness audit`, run
`tools/run.ps1 harness` read-only and summarize the
five stations, actionable findings, and coverage gaps. Do not synchronize,
edit, or retire any control during the audit.

These are repository-local contracts. Do not synchronize them into global
Codex skills. Their handoff is advisory cadence state, never research evidence.
