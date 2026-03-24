## SBPP-FMT-05 - Guard Clause

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-FMT-05:1 - Problem frame

Methods that begin with a complex nested conditional — "if valid, if authorised, if
not already processed, then do the work" — force readers to track multiple indentation
levels before reaching the actual logic. Guard clauses invert the structure: handle the
exceptional/invalid cases first with early returns, leaving the happy path at the top
level of indentation.

### SBPP-FMT-05:2 - Problem

How do you format methods that must handle invalid or exceptional cases so that the
main logic is clearly separated from the boundary conditions and reads at a single
indentation level?

### SBPP-FMT-05:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | Guard clauses flatten nesting ↔ "single exit" dogma from structured programming |
| **Intent** | Guard says "this case is excluded from further processing" ↔ else-branch says "this is a path of equal importance" |
| **Cognitive load** | Fewer nesting levels reduce mental stack ↔ multiple return points require reading all of them |

### SBPP-FMT-05:4 - Solution — Return early for precondition failures; keep the happy path at the top indentation level

Identify the preconditions that, when failed, should immediately terminate the method.
Express each as a one-line check followed by `return`, `throw`, or a short early-exit
action. The remaining body executes only when all preconditions pass.

**Java — before (nested) vs after (guard clauses):**

```java
// ❌ Before: nested — happy path is at the deepest indent
public Money calculatePremium(Policy policy, RiskContext context) {
    if (policy != null) {
        if (policy.isActive()) {
            if (context != null) {
                return ratingEngine.rate(policy, context);
            } else {
                throw new IllegalArgumentException("Context required");
            }
        } else {
            return Money.ZERO;
        }
    } else {
        throw new IllegalArgumentException("Policy required");
    }
}

// ✅ After: guard clauses — happy path at top level, immediately readable
public Money calculatePremium(Policy policy, RiskContext context) {
    Objects.requireNonNull(policy, "Policy required");
    Objects.requireNonNull(context, "Context required");
    if (!policy.isActive()) return Money.ZERO;         // guard: inactive policy

    return ratingEngine.rate(policy, context);          // happy path — clear
}
```

**Java — service method with multiple guards:**

```java
public void processClaim(ClaimId claimId, UserId userId) {
    Claim claim = claimRepository.findById(claimId)
        .orElseThrow(() -> new ClaimNotFoundException(claimId));

    if (!claim.isOpen())        throw new ClaimAlreadyProcessedException(claimId);
    if (!claim.isAssignedTo(userId)) throw new UnauthorisedException(userId, claimId);

    // Happy path — all guards passed
    claim.process();
    claimRepository.save(claim);
    eventBus.publish(new ClaimProcessed(claimId));
}
```

**Kotlin — guard clauses using `require`, `check`, `?:` (Elvis operator):**

```kotlin
fun calculatePremium(policy: Policy?, context: RiskContext?): Money {
    requireNotNull(policy) { "Policy required" }
    requireNotNull(context) { "Context required" }
    if (!policy.isActive) return Money.ZERO

    return ratingEngine.rate(policy, context)
}

// ✅ Elvis-based guard (idiomatic Kotlin)
fun processClaim(claimId: ClaimId, userId: UserId) {
    val claim = claimRepository.findById(claimId)
        ?: throw ClaimNotFoundException(claimId)

    check(claim.isOpen) { "Claim $claimId already processed" }
    check(claim.isAssignedTo(userId)) { "User $userId not authorised for $claimId" }

    // Happy path
    claim.process()
    claimRepository.save(claim)
    eventBus.publish(ClaimProcessed(claimId))
}
```

**Also — also — Kotlin `apply`/`also` for guard chains:**

```kotlin
// ✅ Guard + validation in Kotlin using require/check
fun Policy.validate(): Policy = apply {
    require(premium > Money.ZERO) { "Premium must be positive" }
    require(coverages.isNotEmpty()) { "Policy must have at least one coverage" }
    check(status != PolicyStatus.CANCELLED) { "Cannot validate a cancelled policy" }
}
```

### SBPP-FMT-05:5 - Archetypal Grounding

**U.System:** `processClaim` — three guard lines handle all exceptional cases; the happy-path
logic starts at column 4, not column 16.

**U.Episteme:** Reading a method with guard clauses, a reviewer first understands what is
*excluded*, then immediately sees what happens in the *normal* case. The structure mirrors
the programmer's intent: "if any of these are wrong, bail out; otherwise, do the work."

### SBPP-FMT-05:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Early-exit and precondition formatting in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Some teams prohibit multiple return points (legacy "single exit" rule) | Provide Beck's rationale: short methods with guard clauses are safer than deeply nested ones; update the rule |
| **Arch** | Guard clauses mixed with complex happy path can still be hard to read | Keep guard clauses thin (one condition, one action); never put logic in the guard block |
| **Onto/Epist** | Kotlin `require`/`check` throw `IllegalArgumentException` / `IllegalStateException` — semantically correct | Use `require` for argument validation, `check` for state validation |
| **Prag** | Kotlin's `?: throw` idiom combines null-guard and exception in one line | Use it; it is idiomatic and expressive |
| **Did** | New developers equate "multiple returns" with "hard to trace" — show them the nesting alternative | Demonstrate that deeply nested code is harder to trace than guard clauses |

### SBPP-FMT-05:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT05-1** | Methods with preconditions SHALL use guard clauses (early return/throw) rather than nesting the happy path inside conditionals. | Flattens indentation |
| **CC-FMT05-2** | Each guard clause SHALL be a single condition + single action on one or two lines. | Keeps guards readable |
| **CC-FMT05-3** | Kotlin argument validation SHOULD use `require { }` ; state validation SHOULD use `check { }`. | Semantically correct exception types |
| **CC-FMT05-4** | Null guards in Kotlin SHOULD use the `?: throw` Elvis expression. | Idiomatic Kotlin |

### SBPP-FMT-05:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Logic inside a guard block**
```java
if (!policy.isActive()) {
    sendExpiryNotification(policy);
    policy.setStatus(ARCHIVED);
    return Money.ZERO;
}
```
Fix: a guard clause should do one thing. If the guard needs multiple steps, extract a method:
`if (!policy.isActive()) return handleInactivePolicy(policy);`

**Anti-pattern 2: Deep nesting instead of guards**
Three levels of `if (valid) { if (authorised) { if (available) { ... } } }`
Fix: three guard clauses at the top; happy path at indentation level 1.

### SBPP-FMT-05:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Happy path visible at a glance; minimal indentation | Multiple return points — but method is short, so all returns are visible |
| Preconditions are documented explicitly | Guard clauses must stay thin |
| Kotlin `require`/`check` self-document precondition type | — |

### SBPP-FMT-05:10 - Rationale

Beck's Guard Clause is one of the most universally applicable refactoring patterns. It
directly addresses the "arrow anti-pattern" (code that marches rightward with increasing
nesting). Fowler's "Replace Nested Conditional with Guard Clauses" (Refactoring) formalises
the same transformation. Kotlin's `require`/`check`/`?:` make guards syntactically elegant.

### SBPP-FMT-05:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Refactoring 2nd ed. — "Replace Nested Conditional with Guard Clauses" (Fowler, 2018):**
This is Beck's Guard Clause formalised as a named refactoring. *Adopt.*

**Kotlin stdlib `require`/`check` (JetBrains, post-2016):** Standard library functions
for guard clause precondition checks. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** "Avoid deep nesting" — guard clauses are the primary
mechanism. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Refactoring 2nd ed. (Fowler, 2018) | "Replace Nested Conditional with Guard Clauses" | **Adopt** |
| Kotlin stdlib `require`/`check` (post-2016) | Guard precondition functions | **Adopt** |
| Clean Code (Martin, ongoing) | Avoid deep nesting | **Adopt** |

### SBPP-FMT-05:12 - Relations

* **Enables:** SBPP-FMT-03 (Indented Control Flow — guard clauses keep the happy path at level 1)
* **Eliminates:** Deep nesting that SBPP-FMT-03 would otherwise need to handle
* **Relates to:** SBPP-BEH-07 (Query Method — guard conditions use query methods)
* **Relates to:** SBPP-BEH-01 (Composed Method — guards help keep methods short)

### SBPP-FMT-05:End
