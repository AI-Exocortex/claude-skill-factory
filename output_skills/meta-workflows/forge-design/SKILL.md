---
name: forge-design
description: DESIGN phase adapter for the forge workflow. Writes design.md using the configured design_method slot skill (default: collaborative-design). Runs in-context.
---

# forge — DESIGN Phase

STARTER_CHARACTER = 🔥

Loaded by the forge spine after SPECIFY completes.
The `design_method` slot skill name is already in context (named by the spine).

## Precondition check

Read `design.md` in the change directory.
- Exists and is non-empty → announce "DESIGN already complete"
  and exit with `FORGE-PHASE-COMPLETE: design`.
- Missing or empty → proceed.

## Context loading

Read `proposal.md` and `specs.md` from the change directory.
Summarise the WHY (proposal) and WHAT (specs) before starting design work,
so the design conversation has full grounding in what was decided.

## Core work

Invoke the `design_method` slot skill.
- SlotKind: MethodDescription-slot (the skill is a loaded design method)
- ValueKind: a loadable skill name (string resolving to an installed Claude Code skill)
- The name was announced by the spine before this adapter loaded; default: `collaborative-design`

Slot resolution: attempt to load the named skill. If it cannot be loaded (not installed,
name misspelled), do not silently fall back — emit:
`FORGE-BLOCKED: design — slot skill '{name}' could not be loaded. Check workflow config.`

Tell it: the OpenSpec change contains `proposal.md` and `specs.md` as inputs; the output
must be written to `design.md`. The design is the HOW document — technical decisions,
approach, architecture, key tradeoffs considered and rejected.

For trivial tasks: a single sentence ("Use standard REST endpoint, no new dependencies")
is a valid, complete design. The design must exist; its length is proportional to complexity.

After the slot skill completes, confirm `design.md` is written.

## Gate check

Verify `design.md` exists in the change directory and is non-empty.
(This is independent evidence — do not rely on slot skill completion as confirmation.)

- Gate passes (evidence confirmed) → announce "DESIGN complete."
  Then emit: `FORGE-PHASE-COMPLETE: design`
- Gate fails (evidence missing/empty) → announce "DESIGN incomplete — design.md is missing or empty."
  Then emit: `FORGE-BLOCKED: design — design.md missing or empty`
