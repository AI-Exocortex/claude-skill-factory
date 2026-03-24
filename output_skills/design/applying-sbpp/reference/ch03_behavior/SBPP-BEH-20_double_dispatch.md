## SBPP-BEH-20 - Double Dispatch

> **Type:** Architectural (A)
> **Status:** Adopted/Adapt
> **Normativity:** Normative

### SBPP-BEH-20:1 - Problem frame

In Java, method dispatch considers only the runtime type of the receiver, not the
arguments. When a computation depends on the types of two objects — both the receiver
and an argument — a single dispatch is insufficient. In insurance microservices this
arises when combining two amounts of possibly different types: `Money + Money`,
`Money + Percentage`, `Percentage + Percentage`.

### SBPP-BEH-20:2 - Problem

How do you implement a computation whose logic depends on the runtime types of two
participating objects, without resorting to `instanceof` chains?

### SBPP-BEH-20:3 - Forces

| Force | Tension |
|-------|---------|
| **Type Safety** | Compile-time checking ↔ dynamic dispatch needed for both types |
| **OCP Compliance** | New types should not require modifying existing ones ↔ n×m combinations grow rapidly |
| **Readability** | Type-specific logic is explicit ↔ double dispatch indirection obscures flow |

### SBPP-BEH-20:4 - Solution — Two-level dispatch: receiver dispatches to argument, argument dispatches back

First dispatch selects the method on the receiver based on its type. That method then
sends a type-specific message back to the argument, achieving the second dispatch.

**Java example (Visitor-style double dispatch):**

```java
// First family
public interface Amount {
    Money combineWith(Amount other);
    Money combineWithMoney(Money money);
    Money combineWithPercentage(Percentage pct);
}

public record Money(long cents, Currency currency) implements Amount {
    @Override
    public Money combineWith(Amount other) {
        return other.combineWithMoney(this);  // second dispatch
    }
    @Override
    public Money combineWithMoney(Money money) {
        return new Money(this.cents + money.cents, this.currency);
    }
    @Override
    public Money combineWithPercentage(Percentage pct) {
        return new Money((long)(this.cents * (1 + pct.value())), this.currency);
    }
}

public record Percentage(double value) implements Amount {
    @Override
    public Money combineWith(Amount other) {
        return other.combineWithPercentage(this);  // second dispatch
    }
    @Override
    public Money combineWithMoney(Money money) {
        return money.combineWithPercentage(this);
    }
    @Override
    public Money combineWithPercentage(Percentage other) {
        // combining two percentages is a domain decision
        throw new UnsupportedOperationException("Cannot combine two percentages directly");
    }
}
```

**Kotlin — sealed class + when (often cleaner than true double dispatch):**

```kotlin
sealed class Amount
data class MoneyAmount(val cents: Long, val currency: Currency) : Amount()
data class PercentageAmount(val value: Double) : Amount()

fun MoneyAmount.combineWith(other: Amount): MoneyAmount = when (other) {
    is MoneyAmount       -> MoneyAmount(cents + other.cents, currency)
    is PercentageAmount  -> MoneyAmount((cents * (1 + other.value)).toLong(), currency)
}
```

**Note:** For sealed types in Kotlin/Java 17+, `when`/`switch` expressions with pattern
matching are often clearer than true double dispatch, since the type set is finite and
exhaustive. Reserve double dispatch for open type hierarchies.

### SBPP-BEH-20:5 - Archetypal Grounding

**U.System:** `amount.combineWith(otherAmount)` works correctly regardless of whether the
amounts are `Money` or `Percentage`, dispatching to the right combination logic.
**U.Episteme:** The pattern makes the n×m type interaction grid explicit and manageable —
each combination has one named method.

### SBPP-BEH-20:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Cross-type dispatch in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Double dispatch creates tight coupling between two type hierarchies | Only apply when the cross-product logic is genuinely necessary |
| **Arch** | Code path is non-obvious; debugging requires two dispatch steps | Add documentation; use sealed types for compile-safe exhaustiveness |
| **Onto/Epist** | Java 21 pattern matching `switch` provides a readable alternative | Prefer `switch`/`when` for sealed/known type sets; use double dispatch for open hierarchies |
| **Prag** | Most double-dispatch use cases in Java are better served by Visitor pattern or sealed `when` | Evaluate before implementing full double dispatch |
| **Did** | One of the hardest patterns to understand initially | Provide worked examples and trace through the two dispatch steps |

### SBPP-BEH-20:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH20-1** | Double Dispatch SHALL only be used when single dispatch is genuinely insufficient (both types matter). | Avoids unnecessary complexity |
| **CC-BEH20-2** | For sealed/known type sets, `when`/`switch` pattern matching SHOULD be preferred over double dispatch. | Modern, more readable alternative |
| **CC-BEH20-3** | Double dispatch methods SHALL be named from the perspective of the operation being requested. | Maintains intent clarity |

### SBPP-BEH-20:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: instanceof Chain**
```java
if (other instanceof Money m) { ... } else if (other instanceof Percentage p) { ... }
```
Fix: Implement true double dispatch or use sealed `when` for exhaustiveness.

**Anti-pattern 2: Over-Engineering**
Implementing double dispatch for a case where only one type matters.
Fix: Check if single dispatch (Choosing Message) suffices first.

### SBPP-BEH-20:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Eliminates `instanceof` in cross-type operations | Complex dispatch path — mitigated by clear naming and sealed hierarchies |
| New type pairs handled without modifying callers | Requires changes to both interfaces when adding a new type |
| Type combinations are explicit and testable | — |

### SBPP-BEH-20:10 - Rationale

Double Dispatch is a foundational pattern for cross-type computation. In modern Java/Kotlin,
sealed classes and pattern-matching `when`/`switch` provide a more readable alternative for
closed type sets, while Visitor pattern formalises double dispatch for open hierarchies.

### SBPP-BEH-20:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**GoF Visitor pattern (widely applied post-2015):** Formalises double dispatch. *Adopt for
open hierarchies.*

**Java 21 pattern matching switch (JEP 441, 2023):** Exhaustive switch on sealed types
replaces double dispatch for closed type sets. *Adapt — prefer switch for sealed types.*

**Kotlin sealed class `when` (post-2016):** Exhaustive, compile-checked alternative.
*Adopt for Kotlin.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Visitor (widely used post-2015) | Open hierarchy double dispatch | **Adopt** |
| Java 21 pattern matching switch | Sealed hierarchy alternative | **Adapt** |
| Kotlin sealed `when` (post-2016) | Idiomatic exhaustive dispatch | **Adopt** |

### SBPP-BEH-20:12 - Relations

* **Extends:** SBPP-BEH-19 (Dispatched Interpretation — one level)
* **Formalised by:** GoF Visitor pattern
* **Superseded by:** `when`/`switch` pattern matching for sealed type sets
* **Relates to:** SBPP-COL-05 (Equality Method — equality between two families uses this)

### SBPP-BEH-20:End
