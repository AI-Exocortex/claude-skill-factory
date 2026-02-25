# Process File Comparison: ideation-to-proposal

**Compared Against**: `output_skills/ai/creating-process-files/SKILL.md`

**Date**: 2026-02-25

---

## Template Conformance

| Element | creating-process-files | ideation-to-proposal | Status |
|---------|----------------------|---------------------|--------|
| **Frontmatter (name, description)** | ✅ Yes | ✅ Yes | ✅ Pass |
| **Header (# Title)** | ✅ Yes | ✅ Yes | ✅ Pass |
| **STARTER_CHARACTER declaration** | ✅ `⚙️` | ✅ `💡📋` (added) | ✅ Pass |
| **Description/Why section** | ✅ "## Description" | ✅ "## Why This Skill Exists" | ✅ Pass (variant) |
| **Structured Phases** | ✅ 4 phases | ✅ 2 phases | ✅ Pass |
| **Clear Steps** | ✅ Numbered steps | ✅ Numbered steps | ✅ Pass |
| **Examples** | ✅ "examine this file" | ✅ Multiple flow examples | ✅ Pass |

---

## Structural Differences (Justified)

### 1. "Why This Skill Exists" vs "Description"

**creating-process-files**:
```markdown
## Description

This skill helps make new process files or fine tune existing ones.
A process file describes a structured sequence of steps for AI to follow
to create a predictable output.
```

**ideation-to-proposal**:
```markdown
## Why This Skill Exists

Testing revealed that agents rationalize skipping exploration/validation
when tasks seem "simple":
- "Just a logout button" → skipped exploration → missed security edge cases
[...]

**This skill enforces discipline: exploration before implementation, always.**
```

**Justification**: TDD testing showed agents need to understand WHY enforcement exists, not just WHAT the skill does. The empirical evidence (4 baseline failures) establishes credibility.

**Verdict**: ✅ Acceptable variant - serves the same purpose with stronger motivation

---

### 2. Defensive Elements (Not in Template)

**Elements Present in ideation-to-proposal**:
- HARD-GATE section (51 lines)
- Common Rationalizations table (21 entries)
- Red Flags list (19 items)
- 5-minute proposal template

**Not Present in creating-process-files**:
- creating-process-files is naturally compliant (meta-skill for creating processes)
- No risk of agents bypassing it

**Justification**:
- Baseline testing: 0% compliance without defensive elements
- Iteration 1: 50% compliance with basic HARD-GATE
- Iteration 2: 50-75% compliance with expanded defenses
- These elements are empirically validated as necessary

**Evidence**:
- `baseline-test-results.md`: Agents violated 4/4 scenarios without skill
- `green-phase-results.md`: Agents who engaged with rationalizations table followed the process
- `refactor-iteration-2-results.md`: Agents who didn't engage still violated

**Verdict**: ✅ Justified deviation - TDD-validated necessity

---

### 3. Rationalization Tables

**Example from ideation-to-proposal**:
```markdown
| Excuse | Reality |
|--------|---------|
| "This is too simple / straightforward" | Simple tasks hide the most assumptions. |
| "Senior dev specified exactly what to do" | Expertise provides guidance on WHAT. Proposal validates HOW. |
| "We already discussed it for 90 minutes" | Conversation ≠ codebase exploration. |
[...21 entries total]
```

**Not in creating-process-files template**.

**Justification**:
- Each entry captured verbatim from baseline testing
- Agents used these EXACT rationalizations to bypass the process
- Table format allows quick lookup when agent is tempted

**Test Evidence**:
```
Scenario 1: "straightforward", "no architectural decisions", "time is tight"
Scenario 2: "90 minutes = sufficient exploration", "informal notes = documentation"
Scenario 3: [No rationalization - pure authority compliance]
Scenario 4: "match effort to complexity", "simple tasks don't need ceremony"
```

**Verdict**: ✅ Justified addition - addresses empirical failure modes

---

### 4. Phase Structure Differences

**creating-process-files** (interview-driven):
1. Interview Phase - Gather requirements
2. Draft Phase - Create initial version
3. Clarification Phase - Ask questions
4. Simplification Phase - Remove unnecessary content

**ideation-to-proposal** (exploration-driven):
1. Exploration Phase - Flexible thinking, no fixed steps
2. Validation Phase - Structured proposal creation with approval

**Justification**:
- Different process types: interview vs exploration
- creating-process-files is about capturing structured input
- ideation-to-proposal is about open-ended discovery then convergence
- Both are valid phase structures for different contexts

**Verdict**: ✅ Appropriate difference - different process models

---

## Quality Assessment

### Strengths of ideation-to-proposal

1. **Empirically Validated**
   - Every defensive element tested through RED-GREEN-REFACTOR
   - Rationalization table entries are actual agent failures, not hypothetical

2. **User-Invoked Model**
   - Solves the engagement problem (agents who read it follow it)
   - Description optimized through 7-lens checking

3. **Complete Documentation**
   - FPF analysis provides theoretical foundation
   - TDD artifacts provide empirical validation
   - Lens checking provides discovery optimization

4. **Appropriate Verbosity**
   - Yes, longer than creating-process-files (520 lines vs 70 lines)
   - But: Each section addresses a validated failure mode
   - Trade-off: Completeness vs brevity (chose completeness based on evidence)

### Potential Improvements

1. **Consider Simplification**
   - Could move rationalization tables to a reference file
   - SKILL.md could link to `references/rationalizations.md`
   - Would match creating-process-files pattern better

2. **Example Placement**
   - Examples are near the end (lines 408-487)
   - Could move earlier for progressive disclosure
   - But: Current placement after all defenses might be intentional

3. **Section Ordering**
   - Current: Why → Your Role → Stance → HARD-GATE → Exploration → Validation
   - Alternative: Why → HARD-GATE → Exploration → Validation → Examples
   - Move "Stance" and "Your Role" into phase descriptions

---

## Recommendations

### Keep Current Structure

**Rationale**:
- Defensive elements are TDD-validated as necessary
- 0% → 50% → 75% compliance progression proves their value
- User-invoked model requires explicit understanding of WHY

### Optional Refactoring (Post-Deployment)

**After real-world usage data collected**:

1. **If compliance remains high (>80%)**:
   - Move rationalization tables to `references/rationalizations.md`
   - Simplify SKILL.md to match creating-process-files brevity

2. **If compliance drops**:
   - Keep current defensive structure
   - Proves empirical validation was correct

3. **If new rationalizations emerge**:
   - Add to tables
   - Run iteration 3 of REFACTOR cycle

---

## Conformance Verdict

**Overall**: ✅ **PASSES** process file pattern with justified deviations

**Template Compliance**: 7/7 required elements present

**Deviations**: 4 major deviations, all empirically justified through TDD testing

**Production Readiness**: ✅ Yes - skill is well-formed and evidence-based

---

## Files Referenced

- **Template**: `output_skills/ai/creating-process-files/SKILL.md`
- **Skill**: `playground/ideation-to-proposal-SKILL.md`
- **Evidence**:
  - `playground/fpf-analysis.md`
  - `playground/baseline-test-results.md`
  - `playground/green-phase-results.md`
  - `playground/refactor-iteration-2-results.md`
  - `playground/TDD-JOURNEY.md`
  - `playground/LENS-CHECKING-RESULTS.md`
