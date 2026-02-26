---
name: forge-close
description: CLOSE phase adapter for the forge workflow. Archives the OpenSpec change, merges branch or creates PR. Runs as a general-purpose subagent.
---

# forge — CLOSE Phase

STARTER_CHARACTER = 🔥

You are running as an autonomous subagent inside a forge workflow.
The spine's dispatch instruction told you the change directory.
Your job: close out the change cleanly.

## Precondition check

Run `openspec status`. If the change is already archived:
- Announce "CLOSE already complete" and exit with `FORGE-PHASE-COMPLETE: close`.

## Context loading

Read `review.md` from the change directory.
If verdict is FAIL, announce:
"CLOSE blocked — review.md contains FAIL verdict. Resolve review findings before closing."
Output: `FORGE-BLOCKED: close — review failed, resolve before closing`
Do not proceed.

## Core work

Two steps in sequence:

**Step A: Archive the change**

Load and follow the `openspec-archive-change` skill.
This preserves the decision history (proposal, specs, design, tasks) in the OpenSpec archive.

**Step B: Integrate the branch**

Load and follow the `superpowers:finishing-a-development-branch` skill.
This guides the decision to merge, create a PR, or clean up the branch.

Follow its instructions for the appropriate integration path.

## Gate check

Two independent conditions:

Condition 1: Run `openspec status`. Verify the change is archived.
Condition 2: Verify the branch is merged (check git log) OR a PR exists (check gh pr list).

- Both pass → announce "CLOSE complete. The forge workflow is finished."
  Output: `FORGE-PHASE-COMPLETE: close`
- Condition 1 fails → Output: `FORGE-BLOCKED: close — change not archived`
- Condition 2 fails → Output: `FORGE-BLOCKED: close — branch not merged and no PR found`
