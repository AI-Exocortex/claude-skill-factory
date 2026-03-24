## SBPP-STA-18 - Explaining Temporary Variable

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-18:1 - Problem frame

Complex expressions — especially in conditional checks, calculations, or transformations
— are hard to read when written inline. Extracting the expression into a named local
variable explains what it represents, improving the readability of the surrounding code
without changing its behaviour.

### SBPP-STA-18:2 - Problem

How do you simplify a complex expression within a method so that a reader can understand
it without having to decode the full expression each time?

### SBPP-STA-18:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Named variable explains complex expression ↔ adds a line of code |
| **Extraction** | Could extract to a method instead ↔ local variable is sufficient for one-time use |
| **Inline** | Complex inline expression is compact ↔ opaque |

### SBPP-STA-18:4 - Solution — Extract complex sub-expressions into named local variables

```java
// ❌ Complex inline expression — hard to read
if (policy.getExpiryDate().isBefore(LocalDate.now()) &&
    policy.getStatus() == PolicyStatus.ACTIVE &&
    policy.getClaimCount() > 0 &&
    policy.getPremium().compareTo(PremiumLimits.MINIMUM) >= 0) {
    processRenewal(policy);
}

// ✅ Explaining temporary variables
boolean isExpiredActive   = policy.getExpiryDate().isBefore(LocalDate.now())
                            && policy.getStatus() == PolicyStatus.ACTIVE;
boolean hasEligibleClaims = policy.getClaimCount() > 0;
boolean meetsMinPremium   = policy.getPremium().compareTo(PremiumLimits.MINIMUM) >= 0;
boolean eligibleForRenewal = isExpiredActive && hasEligibleClaims && meetsMinPremium;

if (eligibleForRenewal) {
    processRenewal(policy);
}
```

**Kotlin:**

```kotlin
val isExpiredActive   = policy.expiryDate.isBefore(LocalDate.now()) && policy.status == ACTIVE
val hasEligibleClaims = policy.claimCount > 0
val meetsMinPremium   = policy.premium >= PremiumLimits.MINIMUM
val eligibleForRenewal = isExpiredActive && hasEligibleClaims && meetsMinPremium

if (eligibleForRenewal) processRenewal(policy)
```

**Note:** If the condition is reused or needs a clear name visible in call hierarchies,
extract it to a query method (BEH-07) instead of a local variable.

### SBPP-STA-18:5 - Archetypal Grounding

**U.System:** `val eligibleForRenewal = ...` — the complex predicate has a name that a reviewer can assess in one word.
**U.Episteme:** Refactoring "Introduce Explaining Variable" (Fowler) names this pattern exactly.

### SBPP-STA-18:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Complex expression readability in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Local variable is not discoverable via IDE call hierarchy — if reused, extract to method | Escalate to method when the expression is reused or has domain significance |
| **Arch** | IDE "Introduce Variable" refactoring makes this trivial | Use it liberally |
| **Onto/Epist** | Local name encodes understanding at the time of writing — may become stale | Rename as understanding improves |
| **Prag** | Kotlin's expression-oriented style often eliminates need for boolean locals | Use `when` or extract to property if Kotlin idiom is cleaner |
| **Did** | Teach: if you need a comment to explain what an expression does, name it instead | Show before/after |

### SBPP-STA-18:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA18-1** | Complex boolean conditions with > 2 terms SHOULD be extracted to named locals or query methods. | Readability |
| **CC-STA18-2** | Complex arithmetic expressions SHOULD be named if they represent a domain concept. | Communicates meaning |
| **CC-STA18-3** | When an explaining variable is used in multiple methods, it SHOULD be promoted to a query method. | Reusability |

### SBPP-STA-18:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Comment instead of name**
```java
// check if eligible for renewal
if (policy.getExpiry().isBefore(now) && policy.getStatus() == ACTIVE && ...) {
```
Fix: Replace comment + complex expression with `boolean eligibleForRenewal = ...`.

### SBPP-STA-18:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Complex conditions become readable at a glance | Extra lines |
| Names capture current understanding of domain logic | Stale names — rename as understanding evolves |

### SBPP-STA-18:10 - Rationale

Explaining Temporary Variable is the "Introduce Explaining Variable" refactoring from
Fowler's catalogue. It is one of the most impactful readability improvements available
in Java/Kotlin, requiring only naming discipline.

### SBPP-STA-18:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Refactoring 2nd ed. — "Introduce Explaining Variable" (Fowler, 2018):** Direct pattern match. *Adopt.*
**Clean Code (Martin, ongoing):** Explanatory variables as a core technique. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Refactoring 2nd ed. (Fowler, 2018) | "Introduce Explaining Variable" | **Adopt** |
| Clean Code (Martin, ongoing) | Explanatory names | **Adopt** |

### SBPP-STA-18:12 - Relations

* **Specialises:** SBPP-STA-15 (Temporary Variable — explaining use case)
* **Precursor to:** SBPP-BEH-07 (Query Method — when the expression is reused)
* **Triggered by:** IntelliJ IDEA "Introduce Variable" refactoring

### SBPP-STA-18:End
