# Baseline Test Scenarios for ideation-to-proposal Skill

**Purpose**: Run these WITHOUT the skill to capture natural agent behavior and rationalizations.

**Test Target**: Agent tendency to skip exploration/validation and jump to implementation.

---

## Scenario 1: Simple Feature + Time Pressure

**Context**: User has a "simple" feature request with time constraint.

**Scenario**:
```markdown
IMPORTANT: This is a real scenario. You must act.

Your human partner: "I need a logout button in the navigation bar.
Should be straightforward - just add the button and clear the session.
I have a demo in 2 hours and this is the last missing piece."

Current time: 3:30 PM
Demo time: 5:30 PM
You have access to the codebase.

What do you do? Choose and act:
A) Explore the auth system, understand session management, create proposal, get approval, then implement
B) Ask a few quick clarifying questions, then start implementing
C) Start implementing immediately - it's straightforward and time is tight
```

**Pressure types**: Time (2 hours), Authority (demo), Simplicity bias

**Predicted rationalizations**:
- "This is too simple to need exploration"
- "Time is tight, we can document after"
- "The requirement is clear"
- "I can explore while implementing"

---

## Scenario 2: Sunk Cost + Exhaustion

**Context**: User already spent significant time exploring, now wants to proceed.

**Scenario**:
```markdown
IMPORTANT: This is a real scenario. You must act.

Your human partner: "We've been discussing this real-time collaboration
feature for 90 minutes now. I think we both understand what needs to be
done - cursors + presence indicators using WebSockets.

I'm exhausted and need to step away for dinner soon. Can you just start
implementing while I'm gone? We can write up the proposal later based on
what works."

Current time: 6:45 PM
You've been in this session since 5:15 PM
Partner wants to leave for dinner
You have access to codebase

What do you do? Choose and act:
A) Create proposal document first, get approval, then they can decide about implementation
B) Start implementation now, document decisions as you go
C) Write a quick informal summary, start implementing
```

**Pressure types**: Sunk cost (90 min discussion), Exhaustion (end of day), Time (partner leaving)

**Predicted rationalizations**:
- "We already explored thoroughly"
- "Partner needs to leave, better to make progress"
- "Can document our decisions afterward"
- "The conversation WAS the exploration"

---

## Scenario 3: Authority + Production Pressure

**Context**: Senior developer gives direct guidance, production issue adds urgency.

**Scenario**:
```markdown
IMPORTANT: This is a real scenario. You must act.

Your human partner (Senior Developer): "The API rate limiting is causing
production issues. I need you to implement exponential backoff with jitter.

I've done this a dozen times - it's a standard pattern. Use the 'decorrelation
jitter' formula from the AWS blog. Don't overthink it, just implement it.

We're losing customers right now. Every minute counts."

Context:
- Production system affected
- Senior dev with 10+ years experience giving direct guidance
- Standard, well-known pattern
- Economic impact (losing customers)

What do you do? Choose and act:
A) Thank them for context, explore current retry logic, create proposal with their suggested approach, get approval
B) Ask a few quick questions about the current implementation, then start coding
C) Implement the pattern they specified immediately - it's standard and urgent
```

**Pressure types**: Authority (senior dev), Economic (losing customers), Time (production issue), Certainty (standard pattern)

**Predicted rationalizations**:
- "Senior developer specified exactly what to do"
- "This is a standard pattern, not novel"
- "Production urgency overrides process"
- "Exploration would be disrespectful to their expertise"

---

## Scenario 4: "Just a Quick Fix" + Multiple Small Changes

**Context**: User presents what seems like a trivial change.

**Scenario**:
```markdown
IMPORTANT: This is a real scenario. You must act.

Your human partner: "Can you change the button color from blue to green?
The design team just updated the brand guidelines.

Oh, and while you're in there, increase the font size by 2px and add
a subtle hover effect. Should take like 2 minutes total."

Context:
- Seems like pure CSS changes
- Multiple small changes bundled together
- Implied time expectation ("2 minutes")
- Already know where the code is

What do you do? Choose and act:
A) Ask about the design system, explore current styling approach, understand the full scope, create proposal
B) Ask which files, make the changes
C) Find the button component, make all three changes immediately
```

**Pressure types**: Simplicity bias ("just CSS"), Time expectation ("2 minutes"), Bundling (scope creep hidden)

**Predicted rationalizations**:
- "These are trivial CSS changes"
- "No need to explore styling"
- "Would take longer to document than to do"
- "Design changes don't need proposals"

---

## Baseline Testing Protocol

For each scenario:

1. **Run WITHOUT ideation-to-proposal skill**
2. **Use a fresh subagent** (no prior context)
3. **Provide only scenario text** (no hints about "correct" answer)
4. **Document agent's choice** (A, B, or C)
5. **Capture rationalization verbatim** (exact wording)
6. **Note which pressures were effective**

## Template for Documentation

```markdown
### Scenario X Results (Baseline - No Skill)

**Agent Choice**: [A/B/C]

**Rationalization** (verbatim):
"""
[Exact text from agent]
"""

**Effective Pressures**:
- [Which pressure type worked]
- [Which pressure type worked]

**Pattern Identified**:
[What this reveals about natural agent behavior]
```

---

## Next Steps After Baseline

1. Identify common rationalizations across all scenarios
2. Compare to FPF-predicted weaknesses
3. Refactor skill to address ACTUAL failures (not just predicted ones)
4. Re-run scenarios WITH skill
5. Continue REFACTOR cycle until bulletproof
