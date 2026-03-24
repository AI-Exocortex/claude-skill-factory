## SBPP-STA-17 - Caching Temporary Variable

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-17:1 - Problem frame

When a method computes an expensive or side-effecting expression that is needed
multiple times, calling it repeatedly is wasteful or incorrect. A caching local variable
stores the result after the first call, eliminating redundant computation or unintended
repeated side effects.

### SBPP-STA-17:2 - Problem

How do you avoid recomputing an expensive or side-effecting expression when its value
is needed multiple times within a method?

### SBPP-STA-17:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | Single computation is faster ↔ local variable adds a line |
| **Correctness** | Expression with side effects must only run once ↔ inline call runs it each time |
| **Premature Optimisation** | Only cache when measured ↔ obvious cases should always be cached |

### SBPP-STA-17:4 - Solution — Cache the result of expensive or side-effecting expressions in a named local

```java
public RatingResult rate(Policy policy) {
    // ✅ Caching: getRiskMatrix() is an expensive DB call — cache it
    RiskMatrix matrix = riskMatrix();  // called once

    double baseRisk    = matrix.baseRiskFor(policy.getCategory());
    double adjustment  = matrix.adjustmentFor(policy.getRegion());
    double loadFactor  = matrix.loadFactorFor(policy.getClaimHistory());

    return RatingResult.of(baseRisk * adjustment * loadFactor);
}

// ❌ Without caching: riskMatrix() called three times (expensive!)
public RatingResult rateWithoutCache(Policy policy) {
    double baseRisk   = riskMatrix().baseRiskFor(policy.getCategory());
    double adjustment = riskMatrix().adjustmentFor(policy.getRegion());
    double loadFactor = riskMatrix().loadFactorFor(policy.getClaimHistory());
    return RatingResult.of(baseRisk * adjustment * loadFactor);
}
```

**Kotlin:**

```kotlin
fun rate(policy: Policy): RatingResult {
    val matrix = riskMatrix()  // cached once
    val baseRisk   = matrix.baseRiskFor(policy.category)
    val adjustment = matrix.adjustmentFor(policy.region)
    val loadFactor = matrix.loadFactorFor(policy.claimHistory)
    return RatingResult.of(baseRisk * adjustment * loadFactor)
}
```

**Side-effect caching:**

```java
// ✅ Event from stream — must only be consumed once (side effect: advances the stream)
Optional<DomainEvent> nextEvent = eventStream.nextEvent();  // cached — only read once
nextEvent.ifPresent(handler::handle);
nextEvent.ifPresent(auditLog::record);
```

### SBPP-STA-17:5 - Archetypal Grounding

**U.System:** `val matrix = riskMatrix()` — one DB call, used three times.
**U.Episteme:** A method where the same expensive call appears three times is a reader signal to cache; the pattern formalises this.

### SBPP-STA-17:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Intra-method performance and correctness in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Cache correctness depends on the expression being pure (same result each call) | Only cache when the method is deterministic in its context |
| **Arch** | JIT may eliminate duplicate pure expression calls anyway | Cache for side-effecting calls regardless; cache for pure calls only if profiling shows cost |
| **Onto/Epist** | "Expensive" is relative — requires profiling | Cache obvious cases (IO, DB); profile before caching CPU-cheap expressions |
| **Prag** | Kotlin `val` with expression body caches naturally | `val result = expensiveCall()` is idiomatic |
| **Did** | Teach: if you see the same call twice, ask "should this be cached?" | Pair with profiling and measurement discipline |

### SBPP-STA-17:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA17-1** | Expressions with IO, DB, or network calls used multiple times MUST be cached in a local. | Correctness and performance |
| **CC-STA17-2** | Side-effecting expressions MUST be cached to prevent repeated side effects. | Correctness |
| **CC-STA17-3** | Cache variables SHALL be `final`/`val`. | Prevents accidental reassignment |

### SBPP-STA-17:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Repeated expensive call**
```java
if (riskMatrix().isHighRisk(policy)) return riskMatrix().highRiskPremium(policy);
return riskMatrix().standardPremium(policy);
```
Fix: `RiskMatrix matrix = riskMatrix();` and use `matrix` throughout.

### SBPP-STA-17:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| IO/DB operations performed once per method call | Local variable to declare |
| Side effects triggered exactly once | Cache validity depends on method execution context |

### SBPP-STA-17:10 - Rationale

Caching Temporary Variable is justified on correctness grounds alone when side effects are
involved. For pure expensive computations, profile first; the JIT may already cache them.
In Kotlin, `val` makes caching the idiomatic default.

### SBPP-STA-17:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008/ongoing):** "Explanatory variables" — caching expensive calls in named locals. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, ongoing) | Named explanatory locals | **Adopt** |
| Kotlin `val` (post-2016) | Immutable caching by default | **Adopt** |

### SBPP-STA-17:12 - Relations

* **Specialises:** SBPP-STA-15 (Temporary Variable — caching use case)
* **Applied when:** Expression is expensive or has side effects and appears multiple times
* **Contrast with:** SBPP-STA-04 (Lazy Initialization — caches across method calls, not within one)

### SBPP-STA-17:End
