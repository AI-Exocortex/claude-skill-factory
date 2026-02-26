---
name: forge
description: Unified full-SDLC development workflow. Orchestrates all phases from exploration to merge using OpenSpec for artifact management. Invoke at session start to detect current phase or begin new work.
---

# forge — The Spine

STARTER_CHARACTER = 🔥

Unified software development workflow — from exploration to merge.
Phases: EXPLORE → PROPOSE → SPECIFY → DESIGN → PLAN → BUILD → VERIFY → CLOSE
All phases mandatory. Hard gates. No skipping.

---

## On every session start

### Step 1: Read forge configuration

Look for a `workflow:` block in CLAUDE.md (project root). Extract:
- `slots.design_method` (default: `collaborative-design`)
- `slots.spec_format` (default: `bdd-with-approvals`)
- `slots.test_method` (default: `tdd`)
- All `hooks.before_*` and `hooks.after_*` lists (default: all empty)

If no `workflow:` block found, use all defaults silently.

### Step 2: Detect current phase

Run `openspec status` in the current directory.

**No open change found** → phase is EXPLORE. Proceed to EXPLORE.

**Change found** → determine phase from artifact presence:

| Artifacts present | Current phase |
|------------------|--------------|
| none | PROPOSE |
| proposal.md | SPECIFY |
| proposal.md + specs.md | DESIGN |
| proposal.md + specs.md + design.md | PLAN |
| all above + plan.md, no tasks.md | BUILD (not started) |
| all above + plan.md + tasks.md with `[ ]` | BUILD (in progress) |
| all above + plan.md + tasks.md (all `[x]`) | VERIFY |
| all above + review.md | CLOSE |
| change is archived | DONE |

Announce: "Found change `{name}`, currently in {PHASE} — ready to continue?"
Wait for user confirmation before proceeding.

### Step 3: Phase execution

For each phase, execute this sequence:

```
1. Run before_{phase} hooks (in order from config)
   — If any hook outputs a line starting with "BLOCKED:", halt and surface to user.
2. Dispatch the phase (in-context or subagent — see below).
3. Run after_{phase} hooks (in order from config).
   — Hooks read their input from the filesystem (artifacts produced by the phase).
4. Verify gate independently (see gate table — do not skip this step).
5. If gate fails, halt and surface the specific failure to the user.
6. Advance to the next phase.
```

---

## Phase dispatch

### In-context phases (EXPLORE, PROPOSE, SPECIFY, DESIGN)

Before loading the adapter, announce the configured slots in context:
"Entering {PHASE}. Configured slots: design_method={value}, spec_format={value}, test_method={value}."

Then load the phase skill:
- EXPLORE → load `forge-explore`
- PROPOSE → load `forge-propose`
- SPECIFY → load `forge-specify`
- DESIGN  → load `forge-design`

After the adapter outputs `FORGE-PHASE-COMPLETE: {phase}`, continue to gate verification.

### Autonomous phases (PLAN, BUILD, VERIFY, CLOSE)

Launch a Task tool subagent with this instruction:
"You are acting as the forge {PHASE} performer (TransformerRole: forge-{phase}-agent,
 BoundedContext: forge-workflow). Load the `forge-{phase}` skill — it contains your
 full instructions. The OpenSpec change is at `{change_dir}`.
 Configured slot skill: `{relevant_slot}`."

Agent types and turn budgets:

| Phase | Agent type | `max_turns` |
|-------|-----------|-------------|
| PLAN | `general-purpose` | 30 |
| BUILD | `general-purpose` | 100 |
| VERIFY | `superpowers:code-reviewer` | 40 |
| CLOSE | `general-purpose` | 25 |

Always set `max_turns` explicitly. Budget exhaustion produces no signal; the failure
protocol below catches this identically to a missing signal.

After the subagent completes, run after-hooks and verify the gate independently.
The subagent's `FORGE-PHASE-COMPLETE` signal is input — not sufficient alone.

**Subagent failure protocol** — handle these cases before running after-hooks:

- **No signal emitted** (subagent completed but output contains neither
  `FORGE-PHASE-COMPLETE` nor `FORGE-BLOCKED`): treat as a failure. Announce:
  "Subagent for {PHASE} exited without a phase signal. Halting."
  Surface the subagent's raw output to the user for diagnosis. Do not advance.

- **Malformed signal** (output contains `FORGE-PHASE-COMPLETE` or `FORGE-BLOCKED`
  but the phase name doesn't match the dispatched phase): treat as a failure.
  Announce: "Subagent emitted unexpected signal: {raw signal}. Expected phase: {PHASE}."
  Do not advance.

- **FORGE-BLOCKED received**: halt immediately. Announce the blocked reason to the
  user. Wait for resolution before re-dispatching the phase.

---

## Gate verification (spine-side, independent)

Always verify gates by reading the filesystem directly, not by trusting phase signals.

| Phase | Spine-side gate verification |
|-------|---------------------------|
| EXPLORE | openspec change container exists (`openspec status` shows a change) |
| PROPOSE | Read `proposal.md` — exists and non-empty |
| SPECIFY | Read `specs.md` — exists and contains `WHEN` |
| DESIGN | Read `design.md` — exists and non-empty |
| PLAN | Read `plan.md` — exists and contains ≥1 task item |
| BUILD | Read `tasks.md` — exists and no `- [ ]` lines remain; run test suite — exit code 0 |
| VERIFY | Read `review.md` — exists and non-empty |
| CLOSE | `openspec status` shows archived; `git log` or `gh pr list` confirms integration |

If BUILD gate fails, run the test suite yourself and report the specific failures.
If VERIFY review.md contains "Verdict: FAIL", surface the issues to the user before CLOSE.

---

## Hook execution

For each hook skill name in `hooks.before_{phase}` or `hooks.after_{phase}`:
1. Load the skill by name.
2. Let it run.
3. If its output contains a line starting with `BLOCKED:`, halt.
   Announce: "Hook `{skill-name}` blocked the workflow: {reason}"
   Wait for user to resolve before continuing.

Hook skills MUST NOT modify phase artifacts (proposal.md, specs.md, design.md, tasks.md).
They may create auxiliary files in the change directory.

---

## Entry points

### /forge (default)

Perform session initialisation above (Steps 1–3).

### /forge new

1. Load `superpowers:using-git-worktrees` to create a new worktree/branch.
2. Phase is EXPLORE (no change exists yet).
3. Skip phase detection — go directly to EXPLORE dispatch.
