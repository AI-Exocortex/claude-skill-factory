## SBPP-BEH-15 - Choosing Message

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-15:1 - Problem frame

In Java/Kotlin microservices, conditional logic that selects among multiple algorithm
variants based on type or state is a recurring smell. A series of `if-instanceof` or
`switch-on-type` statements that grows as new variants are added violates the Open/Closed
Principle and becomes a maintenance burden.

### SBPP-BEH-15:2 - Problem

How do you execute one of several alternative behaviours based on the runtime type of an
object, without hard-coding conditional logic in the caller?

### SBPP-BEH-15:3 - Forces

| Force | Tension |
|-------|---------|
| **Open/Closed** | Adding new variants should not require modifying callers ↔ callers need to invoke different behaviour |
| **Clarity** | Type-switch logic is readable in simple cases ↔ grows unmaintainable as variants multiply |
| **Type Safety** | Java `sealed` classes make exhaustive switches compile-safe ↔ open hierarchies do not |

### SBPP-BEH-15:4 - Solution — Declare a polymorphic method on the common interface; let dispatch choose

Instead of `if (x instanceof A) doA() else if (x instanceof B) doB()`,
define a method on the common interface and let Java/Kotlin's virtual dispatch select the
implementation.

**Java example (sealed classes + pattern matching, Java 17+):**

```java
// ✅ Polymorphic dispatch replaces if-instanceof chain
public sealed interface PremiumAdjustment
    permits DiscountAdjustment, SurchargeAdjustment, NullAdjustment {
    Money applyTo(Money premium);
}

public record DiscountAdjustment(double pct) implements PremiumAdjustment {
    @Override public Money applyTo(Money premium) { return premium.multiply(1 - pct); }
}

public record SurchargeAdjustment(Money flat) implements PremiumAdjustment {
    @Override public Money applyTo(Money premium) { return premium.add(flat); }
}

public record NullAdjustment() implements PremiumAdjustment {
    @Override public Money applyTo(Money premium) { return premium; }
}

// Caller sends the same message regardless of type:
Money adjusted = adjustments.stream()
    .reduce(base, (acc, adj) -> adj.applyTo(acc), (a, b) -> b);
```

**Kotlin example (sealed class):**

```kotlin
sealed class PremiumAdjustment {
    abstract fun applyTo(premium: Money): Money
}
data class DiscountAdjustment(val pct: Double) : PremiumAdjustment() {
    override fun applyTo(premium: Money) = premium * (1 - pct)
}
data class SurchargeAdjustment(val flat: Money) : PremiumAdjustment() {
    override fun applyTo(premium: Money) = premium + flat
}
object NullAdjustment : PremiumAdjustment() {
    override fun applyTo(premium: Money) = premium
}

// Single choosing message replaces all conditionals
val adjusted = adjustments.fold(base) { acc, adj -> adj.applyTo(acc) }
```

### SBPP-BEH-15:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Variants of an algorithm implement the same interface method; callers send one message.
*Show:* `adj.applyTo(premium)` works for discounts, surcharges, and no-ops without a single `instanceof` check.

**U.Episteme (design reasoning):**
*Tell:* Choosing Message converts a conditional expression into a type hierarchy, moving variation to where it belongs.
*Show:* Adding a new adjustment type requires only a new class — zero changes to the calling code.

### SBPP-BEH-15:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Polymorphic dispatch for variant selection in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Too many small classes can be hard to navigate | Group variants in a sealed hierarchy; use IDE navigation |
| **Arch** | Polymorphic dispatch is slightly slower than a direct switch for ≤ 3 variants (JIT usually inlines) | Profile; the architectural benefit outweighs negligible overhead |
| **Onto/Epist** | Java 21 pattern-matching `switch` provides a readable procedural alternative | For sealed types with data extraction, switch expressions can be more readable; apply judiciously |
| **Prag** | Sealed classes require exhaustive handling in `when`/`switch` — compile-time safety | Use sealed hierarchies when all variants are known; use open interfaces when variants are extensible |
| **Did** | New developers may add `instanceof` checks instead of extending the hierarchy | Code review; use sealed types to make exhaustive dispatch visible |

### SBPP-BEH-15:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH15-1** | Type-based conditional logic with > 2 branches SHALL be replaced with a polymorphic method. | Eliminates OCP violation |
| **CC-BEH15-2** | Known-finite variant sets SHOULD use Java `sealed` or Kotlin `sealed class` for compile-time exhaustiveness. | Prevents missing cases |
| **CC-BEH15-3** | The polymorphic method name SHALL express what is requested, not how variants differ. | Maintains caller ignorance of variant internals |

### SBPP-BEH-15:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: instanceof Chain**
```java
if (adj instanceof DiscountAdjustment d) { ... }
else if (adj instanceof SurchargeAdjustment s) { ... }
```
Fix: Add `applyTo(Money)` to the shared interface; delete the conditional.

**Anti-pattern 2: Enum with Behaviour Switch**
Large `switch` on an enum that grows with every new case. Fix: Give the enum an abstract
method; each enum constant provides its own implementation.

### SBPP-BEH-15:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Adding a new variant requires no change to calling code | Initial setup requires creating interface + implementations |
| Exhaustive sealed hierarchies are compile-safe | Open hierarchies can have missing implementations — mitigated by abstract method enforcement |
| Variant logic is co-located with the variant type | — |

### SBPP-BEH-15:10 - Rationale

Choosing Message is the pattern-level expression of polymorphism — the mechanism that
replaces `switch-on-type` with virtual dispatch. Java 17+ sealed classes and Kotlin sealed
classes strengthen this by making the variant set exhaustive and compile-checked.
Java 21 pattern-matching `switch` offers a hybrid when data extraction from variants is needed.

### SBPP-BEH-15:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 17 sealed classes (JEP 409, 2021):** Sealed hierarchies make Choosing Message exhaustive and
compile-safe. *Adopt.*

**Kotlin sealed classes (JetBrains, post-2016):** `when` expression on a sealed class is exhaustive
and type-safe. The idiomatic Kotlin Choosing Message mechanism. *Adopt.*

**Refactoring 2nd ed. — "Replace Conditional with Polymorphism" (Fowler, 2018):** Direct
articulation of this pattern. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 17 sealed classes (JEP 409, 2021) | Exhaustive polymorphic dispatch | **Adopt** |
| Kotlin sealed classes (post-2016) | `when` exhaustive dispatch | **Adopt** |
| Refactoring 2nd ed. (Fowler, 2018) | "Replace Conditional with Polymorphism" | **Adopt** |

### SBPP-BEH-15:12 - Relations

* **Implements:** Open/Closed Principle, Polymorphism
* **Foundation:** SBPP-BEH-14 (Message — polymorphic dispatch is the mechanism)
* **Relates to:** SBPP-BEH-19 (Dispatched Interpretation — two-level dispatch)
* **Constrains:** SBPP-BEH-20 (Double Dispatch — Choosing Message is the single-dispatch version)

### SBPP-BEH-15:End
