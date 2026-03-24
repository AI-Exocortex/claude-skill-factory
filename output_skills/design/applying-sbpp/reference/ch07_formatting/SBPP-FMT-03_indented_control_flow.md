## SBPP-FMT-03 - Indented Control Flow

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-FMT-03:1 - Problem frame

Complex expressions — chained method calls, multi-clause conditionals, nested stream
pipelines — can be formatted in a single long line or spread across multiple indented
lines. The formatting choice directly affects whether the structure of the computation
is visible at a glance or requires careful reading.

### SBPP-FMT-03:2 - Problem

How do you format multi-part expressions — method chains, conditionals, and nested
calls — so that the structure is visible immediately without reading every character?

### SBPP-FMT-03:3 - Forces

| Force | Tension |
|-------|---------|
| **Structure visibility** | One-part-per-line makes nesting explicit ↔ wastes vertical space |
| **Horizontal scanning** | Long single-line expressions require horizontal scrolling ↔ wrapping aids scanning |
| **Consistency** | Consistent indentation rules enable automatic formatting ↔ many ad hoc exceptions |

### SBPP-FMT-03:4 - Solution — Each chained method on its own line, indented; align closing brackets with opening

**Java — stream pipeline indentation:**

```java
// ✅ Each operation on its own line, indented 4 spaces from the base
List<PolicySummary> summaries = policies.stream()
    .filter(Policy::isActive)
    .filter(p -> p.getPremium().compareTo(MINIMUM_PREMIUM) > 0)
    .sorted(Comparator.comparing(Policy::getStartDate))
    .map(PolicySummary::from)
    .collect(toUnmodifiableList());

// ✅ Multi-clause builder/conditional
RatingResult result = RatingResult.builder()
    .policyId(policy.getId())
    .premium(calculatedPremium)
    .adjustments(adjustments)
    .effectiveDate(effectiveDate)
    .build();
```

**Java — multi-argument method call:**

```java
// ✅ Arguments aligned after opening paren or one-per-line
Money premium = calculator.calculate(
    policy.getBaseRate(),
    riskProfile.getLoadingFactor(),
    region.getRegulatoryMultiplier()
);
```

**Kotlin — chained calls:**

```kotlin
// ✅ Each step on its own line
val summaries = policies
    .filter { it.isActive }
    .filter { it.premium > MINIMUM_PREMIUM }
    .sortedBy { it.startDate }
    .map { PolicySummary.from(it) }

// ✅ Scope functions indented
val result = policy
    .also { validatePolicy(it) }
    .let { enrichPolicy(it) }
    .run { calculatePremium(this) }

// ✅ When expression — each branch aligned
val description = when (status) {
    PolicyStatus.ACTIVE   -> "Active policy"
    PolicyStatus.EXPIRED  -> "Expired — renewal available"
    PolicyStatus.CANCELLED -> "Cancelled — no renewal"
}
```

**Key rule: indent one level per "nesting step":**

```java
// ✅ Clear nesting levels
if (policy.isActive()) {
    if (policy.hasClaims()) {
        claims.stream()                // +1 indent per level
            .filter(Claim::isUrgent)  // pipeline indent
            .forEach(this::process);
    }
}
```

### SBPP-FMT-03:5 - Archetypal Grounding

**U.System:** A five-stage stream pipeline where each stage is on its own indented line — a
reader scans vertically to understand the transformation sequence in order.

**U.Episteme:** Consistent indentation is a visual grammar: the eye reads structure before
content. Indentation communicates nesting depth; aligning closing tokens confirms boundaries.

### SBPP-FMT-03:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin expression and control flow formatting**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Deep nesting is a code smell regardless of how well it is indented | Refactor deeply nested code rather than just formatting it better |
| **Arch** | Auto-formatters (ktlint, Spotless/google-java-format) format differently than hand-formatting | Commit to one auto-formatter; never override it manually |
| **Onto/Epist** | "One operation per line" for 3-step streams may add excessive vertical space | Apply judgment: trivial one-liners can stay inline; complex pipelines warrant splitting |
| **Prag** | IntelliJ IDEA auto-formats on code reformat (Ctrl+Alt+L / Cmd+Option+L) | Use it; stop manually formatting |
| **Did** | Teach indentation as visual grammar, not cosmetic preference | Show before/after of a complex pipeline formatted inline vs. split |

### SBPP-FMT-03:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT03-1** | Method chains with ≥ 3 operations SHALL have each operation on its own indented line. | Structure visibility |
| **CC-FMT03-2** | Indentation SHALL use spaces consistently per the project's configured indent size (2 for Kotlin, 4 for Java by convention). | Consistency |
| **CC-FMT03-3** | Closing tokens (`)`, `}`) SHALL align with the start of their opening expression or their first argument. | Visual bracket matching |
| **CC-FMT03-4** | Expression formatting SHALL be delegated to the configured auto-formatter (ktlint / google-java-format / Spotless). | Removes manual overhead |

### SBPP-FMT-03:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Long single-line chain**
`.filter(Policy::isActive).sorted(Comparator.comparing(Policy::getStartDate)).map(PolicySummary::from).collect(toList())`
Fix: one operation per line, each indented.

**Anti-pattern 2: Inconsistent indentation**
Different methods in the same class use 2, 4, or tab indentation.
Fix: configure the formatter once and enforce it in CI.

### SBPP-FMT-03:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Transformation/computation structure visible at a glance | More vertical lines — acceptable cost |
| Auto-formatter makes this zero-effort | Must configure and commit to one formatter |
| Diff readability — each line is one operation | — |

### SBPP-FMT-03:10 - Rationale

Beck's Indented Control Flow establishes that indentation is a semantic tool, not just
cosmetic. In Java/Kotlin, stream pipelines, builder chains, and scope functions benefit
most from this principle. Auto-formatters make the principle free.

### SBPP-FMT-03:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**google-java-format (Google, post-2015):** Opinionated Java formatter that enforces
consistent indentation including method chain wrapping. *Adopt.*

**ktlint (post-2016):** Kotlin formatter that enforces the Kotlin Coding Conventions
including chain indentation. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Indentation is the primary visual grammar of code
structure — consistent indentation is non-negotiable. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| google-java-format (post-2015) | Automated chain formatting | **Adopt** |
| ktlint (post-2016) | Kotlin chain formatting | **Adopt** |
| Clean Code (Martin, ongoing) | Indentation as grammar | **Adopt** |

### SBPP-FMT-03:12 - Relations

* **Applied to:** All multi-part expressions in SBPP-COL-15 through COL-20 (enumeration patterns)
* **Complements:** SBPP-FMT-04 (Rectangular Block — formatting the blocks within expressions)
* **Enables:** SBPP-FMT-05 (Guard Clause — uses indentation to flatten nesting)
* **Constrained by:** Team formatter configuration

### SBPP-FMT-03:End
