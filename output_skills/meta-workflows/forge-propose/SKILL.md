---
name: forge-propose
description: PROPOSE phase adapter for the forge workflow. Writes proposal.md (the WHY document) inside an OpenSpec change container. Runs in-context after EXPLORE.
---

# forge — PROPOSE Phase

STARTER_CHARACTER = 🔥

Loaded by the forge spine after EXPLORE completes. The OpenSpec change container
now exists. The EXPLORE conversation is in context — use it.

## Precondition check

Run `openspec status` or read the change directory.
- `proposal.md` exists and is non-empty → announce "PROPOSE already complete" and exit
  with `FORGE-PHASE-COMPLETE: propose`.
- Missing or empty → proceed.

## Context loading

The EXPLORE conversation is still in context. No files to read yet.
Summarise what was established in EXPLORE: problem, constraints, success criteria.

## Core work

Guide the user to write `proposal.md`. The proposal is the WHY document:
- What problem does this change solve?
- Why now, why this approach?
- What does success look like?
- What is explicitly out of scope?

For trivial tasks, the proposal can be 2–3 sentences covering these points.
Write it together, then use `openspec` to write to `proposal.md`:

Run `openspec continue` or write directly to the artifact path shown by `openspec status`.

The artifact must be saved before proceeding.

## Gate check

Verify `proposal.md` exists in the change directory and is non-empty.
(This is independent evidence — do not rely on slot skill completion as confirmation.)

- Gate passes (evidence confirmed) → announce "PROPOSE complete."
  Then emit: `FORGE-PHASE-COMPLETE: propose`
- Gate fails (evidence missing/empty) → announce "PROPOSE incomplete — proposal.md is missing or empty."
  Then emit: `FORGE-BLOCKED: propose — proposal.md missing or empty`
