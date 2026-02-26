---
name: forge-build
description: BUILD phase adapter for the forge workflow. Implements all tasks in tasks.md using the configured test_method (default: tdd). Runs as a general-purpose subagent.
---

# forge — BUILD Phase

STARTER_CHARACTER = 🔥

You are running as an autonomous subagent inside a forge workflow.
The spine's dispatch instruction told you the change directory and the test_method slot.
Your job: implement everything in `plan.md`, tracking execution state in `tasks.md`.

## Precondition check

Check for `tasks.md` in the change directory.
- `tasks.md` exists and all tasks are marked `[x]` (no `[ ]` remaining) → run the test suite.
  If tests pass → announce "BUILD already complete" and exit with `FORGE-PHASE-COMPLETE: build`.
  If tests fail → tasks are done but tests broken — proceed to fix.
- `tasks.md` exists with unchecked tasks → proceed to Core work (skip initialisation).
- `tasks.md` does not exist → initialise it (see Core work, Step 1).

## Context loading

Read these artifacts from the change directory:
1. `proposal.md` — WHY (understand intent)
2. `specs.md` — WHAT (the scenarios you must make pass)
3. `design.md` — HOW (technical approach to follow)
4. `plan.md` — the immutable WorkPlan (task list to execute)

Do NOT read `tasks.md` for context — it is an execution tracker, not a specification.

## Core work

**Step 1 — Initialise execution tracker (only if tasks.md does not exist):**
Copy `plan.md` verbatim to `tasks.md`. From this point, `plan.md` is never touched again.
`tasks.md` is the mutable execution record; `plan.md` is the immutable WorkPlan.

**Step 2 — Load skills:**
Load and follow the `openspec-apply-change` skill for task iteration guidance.

Within each task, apply the `test_method` discipline.
- SlotKind: MethodDescription-slot (the skill is a loaded test execution method)
- ValueKind: a loadable skill name (string resolving to an installed Claude Code skill)
- The name was given in the spine's dispatch instruction; default: `tdd`

Slot resolution: attempt to load the named test_method skill before starting the first task.
If it cannot be loaded, do not silently fall back to a different method — emit:
`FORGE-BLOCKED: build — slot skill '{name}' could not be loaded. Check workflow config.`

**Step 3 — Task loop:**
1. Read the next unchecked task from `tasks.md`
2. Apply test_method discipline to implement it (write failing test → implement → pass)
3. Mark the task `[x]` in `tasks.md` when done (never modify `plan.md`)
4. Commit after each task or logical group: `git commit -m "- {task summary}"`
5. Repeat until all tasks are `[x]`

If a task is blocked (dependency missing, unclear requirement, test impossible to write):
Output: `FORGE-BLOCKED: build — {specific reason for task N}`
Do not continue past a blocked task.

If ≥3 consecutive fix attempts fail on the same test: stop and report.
Output: `FORGE-BLOCKED: build — 3 fix attempts failed on {test name}. Architectural review needed.`

## Gate check

This gate has two independent conditions. Check both.

Condition 1: Read `tasks.md`. Verify no `- [ ]` lines remain.
Condition 2: Run the project test suite. Check exit code = 0.

The spine will re-verify both conditions independently after you exit. Do not skip either.

- Both pass (evidence confirmed) → announce "BUILD complete."
  Then emit: `FORGE-PHASE-COMPLETE: build`
- Condition 1 fails → Then emit: `FORGE-BLOCKED: build — unchecked tasks remain in tasks.md`
- Condition 2 fails → Then emit: `FORGE-BLOCKED: build — test suite failing: {summary of failures}`
