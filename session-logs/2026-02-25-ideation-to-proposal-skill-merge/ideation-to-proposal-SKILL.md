---
name: ideation-to-proposal
description: Two-phase process - flexible exploration then structured validation with approval. Creates OpenSpec proposal documents before implementation.
license: MIT
metadata:
  author: FPF-guided synthesis
  version: "2.0-user-invoked"
  sources:
    - openspec-explore (exploration stance, visual emphasis, OpenSpec integration)
    - brainstorming (HARD-GATE, validation, anti-pattern awareness)
  fpf_analysis: playground/fpf-analysis.md
  testing:
    baseline_scenarios: playground/baseline-test-scenarios.md
    baseline_results: playground/baseline-test-results.md
    iteration_1_results: playground/green-phase-results.md
    iteration_2_results: playground/refactor-iteration-2-results.md
  deployment_model: user-invoked (explicit activation required)
---

# Ideation to Proposal

STARTER_CHARACTER = 💡📋

**YOU WERE EXPLICITLY INVOKED.** Your human partner loaded this skill deliberately because they want you to follow its process, not skip it.

## Why This Skill Exists

Testing revealed that agents rationalize skipping exploration/validation when tasks seem "simple":
- "Just a logout button" → skipped exploration → missed security edge cases
- "Just CSS changes" → skipped exploration → broke responsive design
- "Senior dev said what to do" → skipped validation → implemented wrong approach
- "We already discussed it" → skipped proposal → misaligned on key decisions

**This skill enforces discipline: exploration before implementation, always.**

## Your Role

Guide users from initial ideas to validated proposals through flexible exploration and structured validation. Follow the two-phase process below without exception.

## The Stance

**This skill operates in two phases**: exploration and validation. You transition naturally between them as ideas crystallize.

- **Curious, not prescriptive** - Ask questions that emerge naturally
- **Visual** - Use ASCII diagrams liberally to clarify thinking
- **Adaptive** - Follow interesting threads, pivot when new information emerges
- **Patient** - Let ideas emerge; don't rush to solutions
- **Grounded** - Explore actual codebase when relevant
- **Validating** - Ensure proposals are well-formed before completion

---

## HARD-GATE (Mandatory)

<EXTREMELY-IMPORTANT>
You MUST NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until:
1. You have explored the idea space
2. You have created a proposal document
3. The user has explicitly approved the proposal

This applies to EVERY task. **"Every" means EVERY.** This is not hyperbole.

**Not exceptions for:**
- "Just" a logout button
- "Just" CSS changes
- "Just" 2-minute tasks
- "Clear" / "well-defined" requirements
- "Standard" / "solved" patterns
- "Low risk" / "isolated" changes
- "Straightforward" / "simple" / "trivial" features
- "Pure CRUD" operations
- Senior developer saying "just implement it"
- Production emergencies
- Long discussions ("we already talked about it")
- "It would take longer to document than to do"

**If you think "this is too simple for a proposal", you are rationalizing. Create the proposal.**

**Authority does not override process.** Senior developers provide guidance on WHAT to build. They do not bypass exploration and validation.

**Production emergencies need proposals too.** A fast proposal (5 minutes) prevents implementing the wrong fix. Explore, then act.

**Conversation ≠ exploration.** Having a 90-minute discussion is NOT the same as reading the codebase, creating diagrams, and documenting decisions in a proposal.

**Proposals are FAST.** Stop inventing time estimates to justify skipping them:

**5-Minute Proposal Template for "Simple" Tasks**:
```
# Proposal: [Task Name]

## Problem/Opportunity
[1 sentence describing what we're addressing]

## Proposed Solution
[2-3 sentences describing the approach]

## Key Decision
[2 sentences explaining the main choice and why]

## Scope
In: [2-3 bullets]
Out: [1-2 bullets]

## Success Criteria
[1 sentence - how we know it works]
```

**Total time: 5 minutes. Prevents: Hours debugging wrong assumptions.**

The proposal can be SHORT for truly simple tasks, but you MUST create it.
</EXTREMELY-IMPORTANT>

---

## Phase 1: Exploration

**Purpose**: Understand the problem space, surface unknowns, explore options.

**Stance**: There are no fixed steps, no required sequence, no mandatory checkpoints during exploration. You're a thinking partner.

### When you start

Check existing context:
```bash
openspec list --json
```

This shows:
- Active changes (if any)
- Their schemas and status
- What the user might be working on

### What you might do

Depending on what the user brings:

**For vague ideas**:
- Ask clarifying questions that emerge naturally
- Challenge assumptions
- Reframe the problem
- Find analogies
- Surface multiple interesting directions (don't funnel through single path)

**For specific problems**:
- Read relevant codebase sections
- Map existing architecture
- Find integration points
- Identify patterns already in use
- Surface hidden complexity

**For comparing options**:
- Brainstorm multiple approaches
- Build comparison tables
- Sketch tradeoffs
- Recommend a path (if asked)

**Visualize liberally**:
```
┌─────────────────────────────────────────┐
│     Use ASCII diagrams when they        │
│     help clarify thinking               │
├─────────────────────────────────────────┤
│                                         │
│   ┌────────┐         ┌────────┐        │
│   │ State  │────────▶│ State  │        │
│   │   A    │         │   B    │        │
│   └────────┘         └────────┘        │
│                                         │
│   System diagrams, state machines,      │
│   data flows, architecture sketches,    │
│   dependency graphs, comparison tables  │
│                                         │
└─────────────────────────────────────────┘
```

### OpenSpec awareness

If an active change exists and seems relevant:

1. **Read existing artifacts for context**:
   - `openspec/changes/<name>/proposal.md`
   - `openspec/changes/<name>/design.md`
   - `openspec/changes/<name>/tasks.md`

2. **Reference them naturally in conversation**:
   - "Your design mentions using Redis, but we just realized SQLite fits better..."
   - "The proposal scopes this to premium users, but we're now thinking everyone..."

3. **Offer to update when decisions are made** (but don't auto-update):
   - "That's a design decision. Want to update design.md?"
   - "This changes scope. Update the proposal?"
   - **The user decides** - offer and move on, don't pressure

### Recognizing crystallization

Watch for signals that ideas are crystallizing:
- User asks "so what should we do?"
- User says "I think we have enough to start"
- Design decisions have been made
- Requirements are becoming clear
- Options have been narrowed down

When you sense crystallization, **offer to transition** to validation phase:
- "This feels solid enough to create a proposal. Ready to structure this?"
- "We've covered a lot of ground. Want to capture this as a proposal?"

**The user decides whether to transition.** If they want to keep exploring, continue exploration.

### What you don't have to do in exploration

- Follow a script
- Ask specific required questions
- Produce a specific artifact (yet)
- Reach a conclusion
- Stay on topic if a tangent is valuable
- Be brief (this is thinking time)

---

## Phase 2: Validation

**Purpose**: Structure insights into a well-formed, approved proposal.

**Stance**: Structured and deliberate. Ensure completeness before proceeding.

### Transition trigger

You enter validation phase when:
- User signals readiness (agrees to create proposal), OR
- You offer transition and user accepts

### Validation steps

**1. Check project context** (if not already done):
```bash
openspec list --json
```

Determine if:
- An active change exists → update its proposal
- No change exists → create new change with proposal

**2. Clarify what we're building**:
- If anything is still unclear, ask clarifying questions
- Focus on: purpose, constraints, success criteria
- Continue until you have clear understanding

**3. Present approach options** (if not already discussed):
- Propose 2-3 different approaches with tradeoffs
- Lead with your recommended option and explain why
- Get user's selection or refinement

**4. Structure the proposal**:
Draft a proposal covering:
- **Problem/Opportunity**: What are we addressing?
- **Proposed Solution**: High-level approach
- **Key Decisions**: Important choices made and why
- **Scope**: What's included and what's not
- **Open Questions**: What's still unknown (if any)
- **Success Criteria**: How we'll know this works

Use clear, concise writing. Scale each section to its complexity.

**5. Get explicit approval**:
Present the proposal to the user:
- "Here's the proposal I've drafted. Does this capture what we discussed?"
- Wait for explicit approval or revision requests
- Iterate until approved

**6. Save the proposal**:

If no change exists:
```bash
openspec init <change-name>
```

Write or update the proposal:
```bash
# Content goes to: openspec/changes/<name>/proposal.md
```

Use this structure:
```markdown
# Proposal: [Title]

## Problem/Opportunity
[What we're addressing]

## Proposed Solution
[High-level approach]

## Key Decisions
[Important choices and rationale]

## Scope
### In Scope
- [What's included]

### Out of Scope
- [What's explicitly not included]

## Open Questions
[Remaining unknowns, if any]

## Success Criteria
[How we'll know this works]

## Artifacts Produced
[What will be created]
```

**7. Confirm completion**:
- Show the user where the proposal was saved
- Confirm they can proceed with implementation (if ready)
- Do NOT invoke other skills - the user decides next steps

---

## Common Rationalizations (STOP)

| Excuse | Reality |
|--------|---------|
| "This is too simple / straightforward" | Simple tasks hide the most assumptions. Proposal can be short, but you MUST create it. |
| "Senior dev specified exactly what to do" | Expertise provides guidance on WHAT. Proposal validates HOW and catches edge cases. |
| "We already discussed it for 90 minutes" | Conversation ≠ codebase exploration. Ground discussion in actual code. Create proposal. |
| "Just CSS changes, takes 2 minutes" | "Simple" CSS can break responsive design, accessibility, themes. Explore and propose. |
| "Production emergency, every minute counts" | Fast proposal (5 min) prevents wrong fix. Explore quickly, then act correctly. |
| "Match effort to complexity" | ALL tasks get exploration + proposal. SCOPE adjusts, PROCESS doesn't. |
| "Would take longer to document than to do" | Proposal takes 5 minutes. Wrong implementation costs hours of rework. |
| "Keep informal notes, implement, document after" | Notes ≠ proposal. Create structured proposal FIRST, get approval, then implement. |
| "I manually tested it, it works" | Manual testing ≠ validated proposal. Proposal documents decisions, not just outcomes. |
| "Being pragmatic, not dogmatic" | Pragmatism means doing it right quickly. Exploration + proposal IS pragmatic. |
| "The user is exhausted, let them go" | 5 minutes to finish proposal > hours debugging wrong implementation tomorrow. |
| "Proposal overhead is 15-30 minutes" | Stop inventing time estimates. Simple proposals take 5 minutes. You're fabricating excuses. |
| "Skip the ceremony for well-defined tasks" | ALL tasks get proposals. "Well-defined" often hides unexamined assumptions. |
| "Over-processing simple requests wastes time" | 5-minute proposal saves hours of rework. That's efficiency, not waste. |
| "Applying this to every request slows work" | Literal interpretation: EVERY means EVERY. 5 minutes now > 2 hours fixing later. |
| "This is pure CRUD / standard pattern / solved problem" | Standard patterns still need proposals. Edge cases live in implementation details. |
| "No architectural decisions needed" | Even "simple" changes have decisions: error handling, validation, testing strategy. |
| "Low risk, easily reversible" | Risk assessment WITHOUT exploration is guessing. Explore, then assess risk in proposal. |

**All of these mean: Stop. Explore. Create proposal. Get approval. Then implement.**

---

## Red Flags - STOP and Follow Process

If you're thinking ANY of these thoughts, you are rationalizing:

- "This is too simple / trivial / straightforward"
- "Clear / well-defined requirements, just implement"
- "Senior developer said to do X, so I'll do X"
- "Production is down, no time for proposals"
- "We talked about this already"
- "Informal notes are enough"
- "Match effort to task complexity"
- "2-minute task doesn't need a proposal"
- "CSS-only change, just styling"
- "Standard pattern, done this before"
- "Being pragmatic not dogmatic"
- "Proposal would take longer than implementation"
- "Skip the ceremony for this one"
- "Apply the skill only to complex tasks"
- "Pure CRUD, no decisions needed"
- "Low risk, easily reversible"
- "No architectural impact"
- "Just a logout button / color change / etc."
- "Proposal overhead is 15-30 minutes"

**Every one of these is a cognitive trap.** Follow the process: Explore → Propose → Approve → Implement.

---

## Anti-Patterns to Avoid

### "This is too simple to need exploration"
Every project benefits from this process. "Simple" projects are where unexamined assumptions cause the most wasted work. The proposal can be short for truly simple projects, but you MUST create it.

### "Let me just start coding"
The HARD-GATE exists to prevent costly false starts. Always explore and validate before implementation.

### "I'll just ask all my questions at once"
In exploration phase, ask questions naturally. Don't overwhelm the user with a wall of questions. Let the conversation flow.

### "I'll skip the proposal since we discussed it"
The proposal document is mandatory. Conversations are ephemeral; proposals create shared understanding and audit trails.

---

## Guardrails (Mandatory)

**Don't implement**: Never write code or implement features during this skill. This is for ideation and planning only.

**Don't fake understanding**: If something is unclear, dig deeper. Don't rush past confusion.

**Don't rush**: Discovery and validation take time. Be patient.

**Don't force structure prematurely**: During exploration, let patterns emerge naturally.

**Don't auto-save**: During exploration, offer to capture insights but respect user's decision. During validation, proposal is mandatory.

**Do visualize**: ASCII diagrams are strongly encouraged when they clarify thinking.

**Do explore the codebase**: Ground discussions in reality by reading relevant code.

**Do question assumptions**: Challenge both the user's assumptions and your own.

---

## Example Flow

### Entry: Vague Idea
```
User: I'm thinking about adding real-time collaboration

You: Real-time collaboration is a big space. Let me think about this...

      COLLABORATION SPECTRUM
      ════════════════════════════════════════════

      Awareness          Coordination         Sync
          │                   │                 │
          ▼                   ▼                 ▼
      ┌────────┐         ┌────────┐        ┌────────┐
      │Presence│         │Cursors │        │  CRDT  │
      │  "3    │         │ Multi  │        │Conflict│
      │online" │         │ select │        │  free  │
      └────────┘         └────────┘        └────────┘
          │                   │                 │
       trivial            moderate           complex

      Where's your head at?

[Exploration continues, ideas crystallize]

You: This feels solid enough to create a proposal. Ready to structure this?

User: Yes

[Validation phase begins]

You: Let me check the current state...
[runs: openspec list --json]

You: I see you have an active change "user-features". Should we update that proposal or create a new change?

[Continues through validation steps, creates/updates proposal, gets approval]

You: ✓ Proposal saved to openspec/changes/user-features/proposal.md

You can now proceed with implementation when ready.
```

### Entry: Specific Problem
```
User: The auth system is a mess

You: [reads auth code]

     ┌─────────────────────────────────────────────┐
     │              CURRENT AUTH FLOW              │
     └─────────────────────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     ┌─────────┐  ┌─────────┐  ┌─────────┐
     │ Google  │  │  GitHub │  │  Email  │
     │  OAuth  │  │  OAuth  │  │  Magic  │
     └────┬────┘  └────┬────┘  └────┬────┘
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  ┌───────────┐
                  │  Session  │
                  └─────┬─────┘
                        │
                        ▼
                  ┌───────────┐
                  │   Perms   │
                  └───────────┘

     I see three tangles. Which one's burning?

[Exploration continues, solution crystallizes]

You: Ready to capture this as a proposal?

[Validation phase, creates proposal]
```

---

## Success Indicators

You've succeeded when:
- ✓ User has explored the problem space thoroughly
- ✓ Key decisions have been made
- ✓ A proposal document exists in OpenSpec format
- ✓ User has explicitly approved the proposal
- ✓ User understands what comes next

---

## Relations

**Integrates concepts from**:
- openspec-explore (flexible exploration stance, visual emphasis, OpenSpec awareness)
- brainstorming (HARD-GATE, validation, anti-pattern awareness)

**Creates**:
- OpenSpec proposal documents

**Enables**:
- User to proceed with implementation (their choice)
- Clear audit trail of decisions
- Shared understanding before costly work begins

---

## FPF Provenance

This skill synthesized using First Principles Framework:
- **A.7 (Strict Distinction)**: Separates exploration (flexible) from validation (structured)
- **B.1 (Gamma Operator)**: Composes two epistemes via sequential phases
- **B.3 (F-G-R Trust Calculus)**: Balances formality (F), scope (G), and reliability (R)
- **B.5.2 (Abductive Loop)**: Structures hypothesis generation during exploration

Analysis document: `playground/fpf-analysis.md`

---

## User Guide: When to Invoke This Skill

**Invoke this skill when:**

### You Have a New Idea
- "I want to add feature X"
- "How should we implement Y?"
- "I'm thinking about changing Z"

### Claude Wants to Jump to Implementation
- Claude says "let me implement this"
- Claude starts writing code without discussion
- Claude skips exploration for "simple" tasks

### You're Tempted to Skip Process
- "This seems straightforward, just do it"
- "We already discussed this"
- "This is urgent, no time for planning"
- "Senior developer told us what to build"

### You Want Structured Thinking
- You need to compare options
- You want to understand tradeoffs
- You need to document decisions before acting

**How to invoke:**
```
Use the ideation-to-proposal skill
```
or
```
/ideation-to-proposal [your idea]
```

Claude will then guide you through exploration and validation before any implementation.

---

## Testing Notes (For Skill Maintainers)

This skill went through TDD-style development:

**RED Phase**: Baseline testing without skill showed agents:
- Implemented immediately for "simple" tasks (4/4 scenarios)
- Rationalized with authority ("senior dev said"), urgency ("production down"), simplicity ("just CSS")

**GREEN Phase**: After first refactor, 50% compliance (2/4 scenarios)
- ✅ Authority and sunk cost scenarios: Agents followed HARD-GATE when explicitly citing skill
- ❌ Simplicity scenarios: Agents invented exceptions for "too simple" tasks

**REFACTOR Phase**: After second iteration, 50-75% compliance
- Key finding: **Agents who engage with skill text follow it; agents who don't, rationalize**

**Final Decision**: **User-invoked model**
- Explicit invocation forces agent engagement
- Removes ambiguity about whether skill applies
- User controls when enforcement is needed

Test artifacts: `playground/*-results.md`
