## SBPP-BEH-30 - Pluggable Block

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-30:1 - Problem frame

When the pluggable behavior is more complex than a single method call — it captures
context from the call site, combines multiple operations, or is only known at call time —
a lambda (closure) is the right mechanism. Pluggable Block maps to Java/Kotlin lambdas
and function literals.

### SBPP-BEH-30:2 - Problem

How do you plug in complex behaviour that is not implemented as a method on an existing
object and that may capture context from the call site?

### SBPP-BEH-30:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | Lambdas express complex behavior concisely ↔ can hide logic |
| **Context Capture** | Lambdas can capture local variables ↔ captured mutable state is dangerous |
| **Reusability** | Named lambdas (stored in constants) are reusable ↔ inline lambdas are one-off |

### SBPP-BEH-30:4 - Solution — Use lambdas for complex pluggable behavior; name reusable ones

Use a lambda (Java) or function literal (Kotlin) when the behavior is too complex for
a method reference. Store reusable blocks as named constants or fields.

**Java example:**

```java
public class RuleEngine {
    public <T> List<T> filter(List<T> items, Predicate<T> rule) {
        return items.stream().filter(rule).collect(toList());
    }
}

// Complex rules as named constants (named Pluggable Blocks)
public class PolicyRules {
    public static final Predicate<Policy> IS_HIGH_RISK =
        policy -> policy.getRiskScore() > 0.8 && policy.getClaims().size() > 2;

    public static final Predicate<Policy> NEEDS_MANUAL_REVIEW =
        policy -> IS_HIGH_RISK.test(policy) || policy.getPremium().compareTo(THRESHOLD) > 0;
}

// Usage
List<Policy> highRisk = engine.filter(policies, PolicyRules.IS_HIGH_RISK);
List<Policy> manual   = engine.filter(policies, PolicyRules.NEEDS_MANUAL_REVIEW);
// Inline block for one-off use
List<Policy> overdue  = engine.filter(policies, p -> p.getExpiryDate().isBefore(LocalDate.now()));
```

**Kotlin:**

```kotlin
class RuleEngine {
    fun <T> filter(items: List<T>, rule: (T) -> Boolean): List<T> = items.filter(rule)
}

object PolicyRules {
    val isHighRisk: (Policy) -> Boolean = { it.riskScore > 0.8 && it.claims.size > 2 }
    val needsManualReview: (Policy) -> Boolean = { isHighRisk(it) || it.premium > THRESHOLD }
}

val highRisk = engine.filter(policies, PolicyRules.isHighRisk)
val overdue  = engine.filter(policies) { it.expiryDate.isBefore(LocalDate.now()) }
```

### SBPP-BEH-30:5 - Archetypal Grounding

**U.System:** `PolicyRules.IS_HIGH_RISK` is a named Pluggable Block — complex logic stored as a reusable named predicate.
**U.Episteme:** Named blocks are discoverable, testable, and composable; inline anonymous lambdas are not.

### SBPP-BEH-30:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Inline lambdas are invisible in call hierarchies | Name important blocks as constants |
| **Arch** | Captured mutable state in lambdas causes subtle bugs | Lambdas should capture only effectively final variables |
| **Onto/Epist** | Complex lambda logic is hard to name and test | Extract to a named method and reference it; lambda then becomes a method reference |
| **Prag** | Kotlin trailing lambda syntax is very concise | Use trailing lambda for single-method calls; name for complex multi-step logic |
| **Did** | Lambda syntax requires explanation for developers new to functional style | Teach with simple examples; build to complex ones |

### SBPP-BEH-30:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH30-1** | Pluggable blocks used more than once SHALL be named as constants or fields. | Enables reuse and testability |
| **CC-BEH30-2** | Pluggable blocks MUST NOT capture mutable external state. | Prevents race conditions |
| **CC-BEH30-3** | Complex inline lambdas (> 3 lines) SHOULD be extracted to a named method. | Readability |

### SBPP-BEH-30:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Mutable State Capture**
```java
List<Policy> collected = new ArrayList<>();
policies.forEach(p -> { if (rule.test(p)) collected.add(p); });  // mutates captured list
```
Fix: Use `stream().filter().collect()` — pure transformation.

**Anti-pattern 2: Monster Lambda**
20-line inline lambda. Fix: Extract to a named method; reference it.

### SBPP-BEH-30:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Complex behavior expressible without a new class | Captured state risk — enforce immutability |
| Named blocks are testable in isolation | Inline blocks are opaque — name important ones |

### SBPP-BEH-30:10 - Rationale

Pluggable Block is the direct predecessor of Java 8 lambdas and Kotlin function literals.
The mapping is exact: Smalltalk blocks ≡ Java/Kotlin lambdas/closures.

### SBPP-BEH-30:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8 lambdas (post-2014):** Exact realization of Pluggable Block in Java. *Adopt.*

**Kotlin function literals (post-2016):** `{ ... }` function literals are idiomatic Pluggable Blocks. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8 lambdas | Direct implementation | **Adopt** |
| Kotlin function literals (post-2016) | Idiomatic Kotlin | **Adopt** |

### SBPP-BEH-30:12 - Relations

* **Specialises:** SBPP-BEH-28 (Pluggable Behavior — complex form)
* **Contrast with:** SBPP-BEH-29 (Pluggable Selector — simple single-method form)
* **Used by:** SBPP-BEH-11 (Execute Around Method uses a Pluggable Block for work)

### SBPP-BEH-30:End
