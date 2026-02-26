---
name: forge-plan
description: PLAN phase adapter for the forge workflow. Reads proposal, specs, and design artifacts, then writes plan.md as an immutable task checklist (WorkPlan). Runs as a general-purpose subagent.
---

# forge — PLAN Phase

STARTER_CHARACTER = 🔥

You are running as an autonomous subagent inside a forge workflow.
The spine's dispatch instruction told you the change directory and slot skill.
Your only output is `plan.md` in the change directory.
`plan.md` is an immutable WorkPlan — once written, it is never modified.

## Precondition check

Read `plan.md` in the change directory.
- Exists and contains ≥1 task item → announce "PLAN already complete"
  and exit with `FORGE-PHASE-COMPLETE: plan`.
- Missing or empty → proceed.

## Context loading

Read these artifacts from the change directory in order:
1. `proposal.md` — understand the WHY
2. `specs.md` — understand the WHAT (scenarios)
3. `design.md` — understand the HOW (technical approach)

Summarise what you understand before writing tasks, to surface any gaps.

## Core work

Write a task checklist to `plan.md` covering the full implementation of the specs.

Task writing principles (from superpowers:writing-plans):
- Each task is 2–5 minutes of focused work
- "Write failing test" = one task; "Run test to verify fail" = another task
- Each task is a `- [ ]` checkbox line
- Group related tasks under headings
- Include: setup tasks, test tasks, implementation tasks, commit tasks
- Every scenario in specs.md must be covered by at least one task
- Reference the test_method that will be used (named by the spine in the dispatch instruction)

Write directly to `plan.md` using the Write tool. Do NOT use openspec CLI for this —
write the file directly so the task format is under your control.
Do NOT create or modify `tasks.md` — that is BUILD's responsibility.

## Gate check

Two independent evidence checks — run both before emitting any signal:

1. **Carrier check**: `plan.md` exists and contains ≥1 line matching `- [ ]`.
2. **Semantic check**: Cross-reference tasks against `specs.md` — every WHEN/THEN
   scenario must be traceable to ≥1 task. If scenarios remain uncovered, add tasks
   before proceeding.

- Both checks pass (evidence confirmed) → announce "PLAN complete."
  Then emit: `FORGE-PHASE-COMPLETE: plan`
- Either check fails (evidence missing/insufficient) → announce "PLAN incomplete —
  plan.md missing, has no tasks, or leaves specs scenarios uncovered."
  Then emit: `FORGE-BLOCKED: plan — plan.md missing, no tasks, or uncovered scenarios`
