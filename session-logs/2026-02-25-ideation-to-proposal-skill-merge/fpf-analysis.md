# FPF Analysis of openspec-explore and brainstorming Skills

**Analysis Date**: 2026-02-25
**Analyst Role**: AI Agent bearing FPF-AnalystRole
**Evidence Sources**:
- SCR://openspec-explore/SKILL.md
- SCR://brainstorming/SKILL.md

## A.7 Strict Distinction Analysis

### openspec-explore
- **Holon Type**: U.Episteme (knowledge artifact)
- **Role**: ExplorationFacilitatorRole / ThinkingPartnerRole
- **MethodDescription**: The skill file itself (design-time guidance)
- **Method**: Capability to facilitate open-ended exploration
- **Work**: NOT described (this is design-time)
- **System**: AI agent bearing ExplorationFacilitatorRole

### brainstorming
- **Holon Type**: U.Episteme (knowledge artifact)
- **Role**: RequirementsElicitationRole / DesignValidationRole
- **MethodDescription**: The skill file (design-time process)
- **Method**: Capability to guide ideation to approved designs
- **Work**: NOT described (design-time)
- **System**: AI agent bearing RequirementsElicitationRole

## B.3 F-G-R Trust Calculus Analysis

### openspec-explore Assessment

**F (Formality)**: F1-F2 (Structured narrative)
- ✓ Clear stance and principles
- ✓ ASCII diagram guidance
- ✓ OpenSpec integration patterns
- ✗ No formal checklist
- ✗ No quality gates
- **Evidence**: "This is a stance, not a workflow. There are no fixed steps..."

**G (ClaimScope)**: Broad exploration domain
- **Applicability**: Vague ideas, specific problems, mid-implementation, option comparison
- **Context**: OpenSpec-aware (proposals, designs, specs, tasks)
- **Boundary**: Ideation/exploration phase
- **Evidence**: "Handling Different Entry Points" section covers 4 scenarios

**R (Reliability)**: R ~ 0.7 (moderate, due to lack of gates)
- ✓ Clear guardrails ("don't implement", "don't fake understanding")
- ✓ References OpenSpec commands
- ✗ No mandatory outputs
- ✗ Can end without closure ("Sometimes the thinking IS the value")
- ✗ Implementation boundary is soft (only "remind them")

### brainstorming Assessment

**F (Formality)**: F2-F3 (Formalizable with strict rules)
- ✓ Mandatory 6-item checklist
- ✓ HARD-GATE prevents premature implementation
- ✓ Process flow diagram
- ✓ Terminal state defined
- ✓ Task creation required
- **Evidence**: "Do NOT invoke any implementation skill... This applies to EVERY project"

**G (ClaimScope)**: Narrower, implementation-focused
- **Applicability**: Implementation tasks requiring design
- **Context**: Must produce design doc, git commit, transition to writing-plans
- **Boundary**: Ideation → approved design → implementation planning
- **Evidence**: "The ONLY skill you invoke after brainstorming is writing-plans"

**R (Reliability)**: R ~ 0.9 (high, strong gates)
- ✓ HARD-GATE enforcement
- ✓ Checklist ensures completeness
- ✓ User approval required
- ✓ Documentation required
- ✗ Rigidity may cause process circumvention
- ✗ "Simple" trap awareness suggests past failures

## B.1 Gamma Operator (Aggregation) Analysis

### Invariant Compliance Assessment

**IDEM (Idempotence)**: ✓ PASS
- Each skill alone maintains its character
- openspec-explore → exploration stance
- brainstorming → structured validation path

**COMM (Commutativity)**: ✗ FAIL
- These epistemes are NOT commutative
- openspec-explore endpoint: "thinking" / "captured decisions"
- brainstorming endpoint: "approved design" + "invoke writing-plans"
- **Implication**: Cannot simply union these; must define composition order

**LOC (Locality)**: ⚠ PARTIAL
- Both can be applied in isolation
- BUT: brainstorming explicitly constrains next step ("ONLY writing-plans")

**WLNK (Weakest-Link)**: ✓ APPLIES
- Combined F_eff = min(F1-F2, F2-F3) = F1-F2
- Combined R_eff must account for congruence penalty (see below)

**MONO (Monotonicity)**: ⚠ TENSION
- Adding structure to exploration may reduce flexibility (hurts exploration value)
- Adding flexibility to validation may reduce reliability (hurts quality gates)

### Congruence Level (CL) Analysis

**Semantic Alignment**: CL1 (plausible mapping)
- ✓ Both address ideation/exploration phase
- ✗ Fundamental tension on structure vs. flexibility
- ✗ Contradictory guidance:
  - openspec-explore: "no fixed steps, no required sequence, no mandatory outputs"
  - brainstorming: "MUST create a task for each... complete them in order"

**CL Penalty**: Φ(CL1) ≈ 0.2 (significant penalty)
- Low congruence on methodology dimension
- Direct contradiction on "mandatory" concept
- **R_eff calculation**: R_eff = max(0, min(0.7, 0.9) - 0.2) = 0.5

## B.5.2 Abductive Loop Analysis

### 1. Frame the Anomaly

**Anomaly Statement**:
Users need BOTH open-ended thinking space AND structured quality gates during ideation. Existing skills optimize for one dimension at the expense of the other, creating a forced choice between:
- Flexible exploration that may drift or end without actionable output (openspec-explore)
- Structured validation that may constrain creative thinking (brainstorming)

### 2. Generate Candidate Hypotheses

**H1: Phased Composition** (exploration → validation)
- Merge by creating explicit phases
- Phase 1: Open exploration (openspec-explore stance)
- Phase 2: Structured validation (brainstorming checklist)
- Transition trigger: User signals readiness or natural crystallization

**H2: Weakening HARD-GATE**
- Make brainstorming's gates optional or graduated
- Risk: Loses reliability benefit

**H3: Strengthening Guardrails**
- Add optional structured checkpoints to openspec-explore
- Keep flexibility but offer structure on-demand
- Risk: Adds complexity without clear benefit

**H4: Adaptive Workflow**
- Unified skill that reads user intent signals
- Adapts between loose/structured based on context
- Risk: Complex to implement, unclear triggers

### 3. Apply Plausibility Filters

**Parsimony (Occam's Razor)**:
- H1: Moderate complexity (phase management)
- H2: Low complexity but loses key strength
- H3: Low complexity, incremental
- H4: High complexity
- **Winner**: H2 or H3

**Explanatory Power**:
- H1: Explains both needs (exploration + validation) ✓✓
- H2: Explains flexibility need, sacrifices reliability ✗
- H3: Explains both partially ✓
- H4: Explains both fully ✓✓
- **Winner**: H1 or H4

**Consistency with FPF Principles**:
- H1: Aligns with A.7 (Strict Distinction - design vs. validation are separate phases)
- H1: Aligns with natural workflow (explore → crystallize → validate)
- H1: Aligns with OpenSpec semantics (proposal is the output)
- **Winner**: H1

**Falsifiability**:
- H1: Testable - can observe if users benefit from phased approach
- H1: Clear success criterion: users complete both exploration and validation
- **Winner**: H1

### 4. Select Prime Hypothesis

**Selected**: H1 (Phased Composition)

**Rationale**:
- Highest explanatory power while maintaining parsimony
- Consistent with FPF principles (A.7 Strict Distinction)
- Consistent with OpenSpec workflow (exploration → proposal)
- Falsifiable and testable
- Preserves strengths of both skills

## Strengths to Preserve (Evidence-Based)

### From openspec-explore (F1-F2, G=broad, R=0.7)

**Strength 1: Flexible Stance**
- Evidence: "This is a stance, not a workflow. There are no fixed steps"
- Rationale: Enables genuine exploration without premature closure
- **PRESERVE**: Keep "stance over workflow" framing in exploration phase

**Strength 2: Visual Emphasis**
- Evidence: "Use ASCII diagrams liberally when they'd help clarify thinking"
- Rationale: Diagrams enable shared understanding in ambiguous domains
- **PRESERVE**: Mandate ASCII diagram use in merged skill

**Strength 3: Open Threads**
- Evidence: "Surface multiple interesting directions and let the user follow what resonates"
- Rationale: Prevents premature convergence, enables discovery
- **PRESERVE**: Keep multi-thread pattern in exploration phase

**Strength 4: Offer-Based Capture**
- Evidence: "Offer to capture when decisions are made... The user decides"
- Rationale: Respects user agency, prevents forced documentation
- **PRESERVE**: Keep "offer, don't force" pattern

**Strength 5: OpenSpec Integration**
- Evidence: "Check for context... openspec list --json"
- Rationale: Grounds exploration in existing work
- **PRESERVE**: Integrate OpenSpec awareness throughout

### From brainstorming (F2-F3, G=narrow, R=0.9)

**Strength 1: HARD-GATE**
- Evidence: "Do NOT invoke any implementation skill... This applies to EVERY project"
- Rationale: Prevents costly premature implementation
- **PRESERVE**: Maintain HARD-GATE at phase boundary

**Strength 2: Design Approval**
- Evidence: "Present design, get user approval before moving on"
- Rationale: Ensures alignment before costly implementation
- **PRESERVE**: Require explicit approval before exiting skill

**Strength 3: Documentation**
- Evidence: "Write design doc... commit to git"
- Rationale: Creates audit trail and shared understanding
- **PRESERVE**: Output proposal document (OpenSpec semantics)

**Strength 4: Anti-Pattern Awareness**
- Evidence: "Every project goes through this process... 'Simple' projects are where unexamined assumptions cause the most wasted work"
- Rationale: Counters cognitive bias toward skipping process
- **PRESERVE**: Include anti-pattern callouts in merged skill

## Weaknesses to Mitigate (Evidence-Based)

### From openspec-explore

**Weakness 1: No Quality Gates**
- Evidence: "There's no required ending. Discovery might just provide clarity"
- Problem: Can end without actionable output
- **MITIGATION**: Add validation phase that creates proposal document

**Weakness 2: Soft Implementation Boundary**
- Evidence: "If the user asks you to implement something, remind them to exit explore mode"
- Problem: "Remind" is weak; users can override
- **MITIGATION**: Use HARD-GATE from brainstorming

**Weakness 3: No Forcing Function**
- Evidence: "Offer to save insights, don't just do it"
- Problem: Insights may be lost if not captured
- **MITIGATION**: Make proposal document mandatory at skill exit

### From brainstorming

**Weakness 1: Rigid Structure**
- Evidence: "MUST create a task for each... complete them in order"
- Problem: Constrains exploratory thinking
- **MITIGATION**: Make task creation optional during exploration phase

**Weakness 2: Single Question Pattern**
- Evidence: "Only one question per message"
- Problem: May slow down natural conversation flow
- **MITIGATION**: Remove this constraint; allow natural dialogue pace

**Weakness 3: Forced Terminal State**
- Evidence: "The ONLY skill you invoke after brainstorming is writing-plans"
- Problem: Doesn't align with "save exploration as proposal" requirement
- **MITIGATION**: Remove writing-plans invocation; end with proposal document

## Γ_epist Composition Strategy

**Aggregation Approach**: Sequential Phase Composition (Γ_method style)

**Phase 1: Exploration** (openspec-explore characteristics)
- Formality: F1-F2 (flexible stance)
- Scope: G = broad (any ideation entry point)
- Reliability: R ~ 0.7 (guardrails present)
- Endpoint: Natural crystallization or user readiness signal

**Phase 2: Validation** (brainstorming characteristics)
- Formality: F2 (structured validation)
- Scope: G = design validation
- Reliability: R ~ 0.9 (HARD-GATE enforced)
- Endpoint: Approved proposal document in OpenSpec format

**Composition**:
- F_eff = min(F1-F2, F2) = F1-F2 (acceptable for ideation domain)
- G_eff = union(exploration, validation) constrained by support
- R_eff after phases: R ~ 0.85 (exploration 0.7 + validation gate 0.9 raises aggregate)
- CL improved: Phases are naturally sequential, reducing contradiction penalty

**Evidence**:
- A.7 supports phase distinction (exploration ≠ validation)
- B.1.5 (Γ_method) defines order-sensitive composition
- OpenSpec semantics: exploration → proposal is natural workflow

## Assurance Level

**Current State**: L0 (Unsubstantiated)
- This analysis is a new synthesis
- Requires empirical validation with users

**Path to L1**:
- Test merged skill with users
- Collect evidence on completion rates
- Measure satisfaction with both exploration and validation

## Relations

- **Builds on**: A.7 (Strict Distinction), B.1 (Gamma), B.3 (F-G-R), B.5.2 (Abduction)
- **Produces**: Design for merged ideation skill
- **Enables**: Next step: Write merged skill following this analysis

## Evidence Graph References

- A.7 pattern: SCR://fpf/A.7_strict_distinction_clarity_lattice.md
- B.1 pattern: SCR://fpf/B.1_universal_algebra_of_aggregation_γ.md
- B.3 pattern: SCR://fpf/B.3_trust_assurance_calculus_fgr_with_congruence.md
- B.5.2 pattern: SCR://fpf/B.5.2_abductive_loop.md
- openspec-explore: SCR://openspec-explore/SKILL.md
- brainstorming: SCR://brainstorming/SKILL.md
