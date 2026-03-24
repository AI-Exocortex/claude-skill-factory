## SBPP-STA-04 - Lazy Initialization

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-STA-04:1 - Problem frame

Some fields are expensive to compute or depend on state that may not be available at
construction time. Lazy Initialization defers computing the field value until it is first
accessed. In Kotlin this is a first-class language feature (`by lazy`). In Java it
requires careful implementation, especially in multi-threaded contexts.

### SBPP-STA-04:2 - Problem

How do you initialize an instance variable only when it is first needed, rather than
eagerly at construction time, so that unused values are never computed?

### SBPP-STA-04:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | Avoid computing expensive values that may never be used ↔ adds complexity to accessors |
| **Thread Safety** | Lazy init needs synchronization in multi-threaded code ↔ synchronization is a performance cost |
| **Simplicity** | Explicit initialization is simpler ↔ lazy is needed for circular or expensive dependencies |

### SBPP-STA-04:4 - Solution — Use `by lazy` in Kotlin; use double-checked locking or `Supplier` in Java

**Kotlin — idiomatic `by lazy`:**

```kotlin
class PolicyRiskProfile(private val policy: Policy) {
    // ✅ Computed once on first access; thread-safe by default
    val riskScore: Double by lazy {
        RiskScorer.computeScore(policy)  // expensive computation
    }

    val adjustments: List<Adjustment> by lazy {
        AdjustmentProvider.forPolicy(policy)
    }
}

// Usage — computation deferred until first access
val profile = PolicyRiskProfile(policy)
// ... riskScore not yet computed
val score = profile.riskScore  // computed here, cached thereafter
```

**Java — thread-safe lazy initialization patterns:**

```java
// ✅ Double-checked locking (Java 5+ with volatile)
public class PolicyRiskProfile {
    private volatile Double riskScore;

    public double getRiskScore() {
        if (riskScore == null) {
            synchronized (this) {
                if (riskScore == null) {
                    riskScore = RiskScorer.computeScore(policy);
                }
            }
        }
        return riskScore;
    }
}

// ✅ Initialization-on-demand holder (for static fields)
public class RegulatoryTableHolder {
    private static class Holder {
        static final RegulatoryTable TABLE = RegulatoryTable.load();
    }
    public static RegulatoryTable get() { return Holder.TABLE; }
}

// ✅ Java 8+ — Supplier-based lazy
private Supplier<Double> riskScoreSupplier =
    Suppliers.memoize(() -> RiskScorer.computeScore(policy));  // Guava
```

**Rule:** For simple single-threaded lazy init in Kotlin: `by lazy`.
For Java multi-threaded: use `volatile` + double-checked locking or Initialization-on-Demand holder.
Never use naive null-check without `volatile` in multi-threaded code.

### SBPP-STA-04:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Expensive computed fields use `by lazy`; they are computed at most once per instance.
*Show:* `profile.riskScore` — first call triggers the computation; subsequent calls return the cached value.

**U.Episteme (design reasoning):**
*Tell:* Lazy initialization is a performance optimization; apply it only after measuring that the eager cost matters.
*Show:* Without `by lazy`, every `PolicyRiskProfile` construction triggers an actuarial table lookup; with it, lookup happens only if `riskScore` is actually accessed.

### SBPP-STA-04:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Deferred initialization in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Thread-safety of lazy init is subtle; errors are difficult to reproduce | Use `by lazy` (Kotlin) or established Java patterns; avoid hand-rolled lazy |
| **Arch** | Lazy fields introduce mutable state even in otherwise-immutable objects | Kotlin `by lazy` is thread-safe; Java `volatile` pattern is well-tested |
| **Onto/Epist** | Lazy init hides when computation actually happens | Document in Javadoc/KDoc: "computed on first access; cached thereafter" |
| **Prag** | Most lazy init needs in microservices are better served by Spring `@Bean` singleton or `@Lazy` | Use `by lazy` for object-level; use Spring for application-level lazy init |
| **Did** | New developers may use naive `if (field == null)` without `volatile` in Java | Enforce thread-safe patterns; reject unsafe implementations in code review |

### SBPP-STA-04:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA04-1** | Lazy initialization in Kotlin SHOULD use `by lazy`. | Thread-safe, idiomatic |
| **CC-STA04-2** | Lazy initialization in Java for shared instances MUST use `volatile` + double-checked locking or Initialization-on-Demand. | Thread safety |
| **CC-STA04-3** | Lazy fields SHOULD be documented as "computed on first access; cached thereafter." | Communicates the contract |
| **CC-STA04-4** | Lazy initialization SHOULD only be applied when profiling shows the eager cost is significant. | Avoids premature optimisation |

### SBPP-STA-04:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Non-volatile Java lazy init**
```java
private RiskScore score;  // not volatile
public RiskScore getScore() {
    if (score == null) score = compute();  // data race in multi-threaded context
    return score;
}
```
Fix: Add `volatile` or use Kotlin `by lazy`.

**Anti-pattern 2: Lazy init for simple values**
Using `by lazy` for a field that is just `LocalDate.now()`. Fix: Use Explicit Initialization (STA-03).

### SBPP-STA-04:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Unused expensive computations are never performed | Added complexity in Java — mitigated by Kotlin `by lazy` |
| Objects construct faster when not all state is needed | Thread-safety requires care in Java |
| Breaks circular initialization dependencies | — |

### SBPP-STA-04:10 - Rationale

Kotlin's `by lazy` makes this pattern idiomatic and thread-safe with zero boilerplate.
In Java, the pattern requires discipline (volatile + DCL). In modern microservices, most
application-level lazy initialization is handled by Spring's IoC container, reducing the
need for object-level lazy initialization.

### SBPP-STA-04:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Kotlin `by lazy` (JetBrains, post-2016):** Thread-safe, idiomatic Lazy Initialization. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 83 ("Use lazy initialization judiciously").
Bloch's double-checked locking guidance is definitive for Java. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin `by lazy` (post-2016) | Idiomatic lazy init | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 83 — lazy init guidance | **Adopt** |
| Spring `@Lazy` (2015+) | Application-level lazy init | **Adopt** |

### SBPP-STA-04:12 - Relations

* **Contrast with:** SBPP-STA-03 (Explicit Initialization — eager alternative)
* **Requires:** SBPP-STA-05 (Default Value Method — for the lazy computation)
* **Requires:** SBPP-STA-09 (Getting Method — wraps the lazy logic)
* **Thread-safe implementations:** Kotlin `by lazy`, Java DCL, Initialization-on-Demand

### SBPP-STA-04:End
