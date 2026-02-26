---
name: forge-specify
description: SPECIFY phase adapter for the forge workflow. Writes specs.md using the configured spec_format slot skill (default: bdd-with-approvals). Runs in-context.
---

# forge — SPECIFY Phase

STARTER_CHARACTER = 🔥

Loaded by the forge spine after PROPOSE completes.
The `spec_format` slot skill name is already in context (named by the spine).

## Precondition check

Read `specs.md` in the change directory.
- Exists and contains ≥1 WHEN/THEN block → announce "SPECIFY already complete"
  and exit with `FORGE-PHASE-COMPLETE: specify`.
- Missing or does not contain WHEN/THEN → proceed.

## Context loading

Read `proposal.md` from the change directory.
Summarise the WHY before starting specification work, so the spec conversation
has full grounding.

## Core work

Invoke the `spec_format` slot skill.
- SlotKind: MethodDescription-slot (the skill is a loaded specification method)
- ValueKind: a loadable skill name (string resolving to an installed Claude Code skill)
- The name was announced by the spine before this adapter loaded; default: `bdd-with-approvals`

Slot resolution: attempt to load the named skill. If it cannot be loaded (not installed,
name misspelled), do not silently fall back — emit:
`FORGE-BLOCKED: specify — slot skill '{name}' could not be loaded. Check workflow config.`

Tell it: the OpenSpec change contains `proposal.md` as input; the output must be
written to `specs.md` in WHEN/THEN/AND format. Each scenario should be independently
verifiable and expressed in domain language (not technical/implementation language).

For trivial tasks: a single WHEN/THEN scenario is a valid, complete specification.

After the slot skill completes, confirm `specs.md` is written.

## Gate check

Verify `specs.md` exists in the change directory and contains ≥1 WHEN/THEN block.
Use grep or read the file to confirm.
(This is independent evidence — do not rely on slot skill completion as confirmation.)

- Gate passes (evidence confirmed) → announce "SPECIFY complete."
  Then emit: `FORGE-PHASE-COMPLETE: specify`
- Gate fails (evidence missing/insufficient) → announce "SPECIFY incomplete — specs.md missing or contains no WHEN/THEN scenarios."
  Then emit: `FORGE-BLOCKED: specify — specs.md missing or no WHEN/THEN found`
