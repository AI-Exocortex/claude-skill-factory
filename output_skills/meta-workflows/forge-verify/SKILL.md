---
name: forge-verify
description: VERIFY phase adapter for the forge workflow. Reviews all code against specs and design, writes review.md as evidence artifact. Runs as a superpowers:code-reviewer subagent.
---

# forge — VERIFY Phase

STARTER_CHARACTER = 🔥

You are running as a superpowers:code-reviewer subagent inside a forge workflow.
The spine's dispatch instruction told you the change directory.
Your job: review the implementation and write `review.md` as the evidence artifact.

## Precondition check

Read `review.md` in the change directory.
- Exists and is non-empty → announce "VERIFY already complete"
  and exit with `FORGE-PHASE-COMPLETE: verify`.
- Missing or empty → proceed.

## Context loading

Read these artifacts from the change directory:
1. `proposal.md` — the WHY (review against original intent)
2. `specs.md` — the WHAT (every scenario must be implemented)
3. `design.md` — the HOW (implementation must follow the design decisions)
4. `tasks.md` — verify all tasks are checked
5. All changed code files (check git diff against the base branch)

## Core work

Invoke `superpowers:requesting-code-review` for structured review guidance.

Review the implementation against:
- Every scenario in specs.md: is it implemented and testable?
- Every design decision in design.md: was it followed?
- Every task in tasks.md: is it checked and actually done?
- Code quality: no regressions, tests are meaningful, no hardcoded values

Write findings to `review.md` in this structure:
```
# Review: {change-name}

## Verdict: PASS | FAIL | PASS WITH NOTES

## Scenarios coverage
[one line per scenario from specs.md: ✓ implemented / ✗ missing]

## Design compliance
[one line per decision from design.md: ✓ followed / ✗ deviated — {reason}]

## Issues found
[list any blocking issues or improvements]

## Summary
[1-2 sentences]
```

If blocking issues found: note them clearly in the review. The verdict is FAIL.
Still write review.md — the file's existence is the evidence carrier regardless of verdict.

## Gate check

Verify `review.md` exists in the change directory and is non-empty.
(This is independent evidence — file existence is the evidence carrier, not the
subagent's FORGE-PHASE-COMPLETE claim. Check the file directly.)

- Gate passes (evidence confirmed) → announce "VERIFY complete."
  Then emit: `FORGE-PHASE-COMPLETE: verify`
- Gate fails (evidence missing/empty) → announce "VERIFY incomplete — review.md not written."
  Then emit: `FORGE-BLOCKED: verify — review.md missing`

Note: if review.md contains verdict FAIL, the spine will surface the issues to the user.
The gate passes (file exists) but the user must address review findings before CLOSE.
