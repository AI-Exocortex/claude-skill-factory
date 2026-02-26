---
name: forge-explore
description: EXPLORE phase adapter for the forge workflow. Thinking-partner mode before any OpenSpec change exists. Explores problem space, then creates the change container to transition into PROPOSE.
---

# forge — EXPLORE Phase

STARTER_CHARACTER = 🔥

Loaded by the forge spine when no OpenSpec change is found in the working directory.
This is the only forge phase that creates infrastructure rather than artifacts.

## Mode (conversation method — no infrastructure during this phase)

Act as a thinking partner — curious, not prescriptive. Do not implement code.
Do not create OpenSpec artifacts during exploration. The change container is created
only in the Transition step below, which is the Work that completes this phase.

Explore the problem space:
- Ask clarifying questions one at a time
- Investigate the codebase to map relevant structure
- Surface constraints, dependencies, and unknowns
- Compare approaches and their tradeoffs
- Visualise systems and flows with ASCII diagrams

For trivial tasks: compress to 2–3 exchanges confirming scope, constraints, and
absence of hidden dependencies. Mandatory but proportional.

## Readiness detection

After each exchange, assess whether these conditions hold:
- Core problem understood
- Key constraints and success criteria surfaced
- No major unknowns that would block specification

When conditions hold, propose:
"I think we have enough to proceed. Shall I open a forge change?"

## Transition to PROPOSE

On user confirmation:

1. Derive a kebab-case name from the conversation.
   Propose: "I'll name this `{name}` — good, or want something else?"
   Apply correction if given. One exchange maximum.

2. Run: `openspec new change {confirmed-name}`
   Expected: OpenSpec scaffolds the change directory.

3. Announce: "Change `{name}` created. EXPLORE complete."
   Output: `FORGE-PHASE-COMPLETE: explore`
   Return control to the forge spine.

## If invoked via /forge new

Worktree is already created. Skip to Mode above.
