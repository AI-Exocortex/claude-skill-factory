## SBPP-BEH-19 - Dispatched Interpretation

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-19:1 - Problem frame

In Java/Kotlin microservices, one object often needs to operate on data whose internal
representation it should not know. A calculator should not need to know whether it is
working with a percentage, a flat amount, or a combined adjustment. Passing the
representation as a parameter forces the receiver to decode it — coupling two objects
through a shared encoding scheme.

### SBPP-BEH-19:2 - Problem

How can two objects cooperate when one wishes to perform an operation on data whose
representation is managed by the other, without either object needing to know the
other's internal encoding?

### SBPP-BEH-19:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Each object hides its representation ↔ cooperation requires shared data access |
| **Coupling** | Encoding schemes couple caller and callee ↔ polymorphic dispatch breaks the coupling |
| **Extensibility** | New encodings must not require modifying existing code ↔ callers need to handle all variants |

### SBPP-BEH-19:4 - Solution — Let the encoded object dispatch the interpretation to the consumer

Instead of passing encoded data and letting the consumer decode it, reverse the direction:
the consumer sends a message that asks the encoded object to interpret itself for the consumer.

**Java example:**

```java
// ❌ Consumer decodes: coupled to encoding
public class PremiumCalculator {
    public Money apply(Object adjustment, Money base) {
        if (adjustment instanceof Double pct) return base.multiply(1 - pct);     // encoding leak
        if (adjustment instanceof Money flat) return base.add(flat);              // encoding leak
        throw new IllegalArgumentException("Unknown adjustment type");
    }
}

// ✅ Dispatched interpretation: encoded object interprets itself
public interface Adjustment {
    Money applyTo(Money base);  // dispatched interpretation
}

public record PercentDiscount(double pct) implements Adjustment {
    @Override public Money applyTo(Money base) { return base.multiply(1 - pct); }
}

public record FlatSurcharge(Money amount) implements Adjustment {
    @Override public Money applyTo(Money base) { return base.add(amount); }
}

// Calculator knows nothing about encoding
public class PremiumCalculator {
    public Money apply(Adjustment adjustment, Money base) {
        return adjustment.applyTo(base);  // dispatched to the adjustment's own logic
    }
}
```

**Kotlin:**

```kotlin
fun interface Adjustment { fun applyTo(base: Money): Money }

val percentDiscount = Adjustment { base -> base * 0.9 }
val flatSurcharge   = Adjustment { base -> base + Money.of(50, USD) }

fun applyAll(adjustments: List<Adjustment>, base: Money): Money =
    adjustments.fold(base) { acc, adj -> adj.applyTo(acc) }
```

### SBPP-BEH-19:5 - Archetypal Grounding

**U.System:** `adjustment.applyTo(premium)` — the adjustment knows how to apply itself; the calculator does not need to know what kind of adjustment it is.
**U.Episteme:** Adding a new adjustment type requires only a new class implementing `Adjustment`; no existing code changes.

### SBPP-BEH-19:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Polymorphic interpretation in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Interface per encoding type increases class count | Sealed hierarchies keep the type set bounded |
| **Arch** | Dispatched interpretation can be indirect and hard to trace | Use transparent naming (`PercentDiscount.applyTo`) to make dispatch path clear |
| **Onto/Epist** | Not all encoded data maps cleanly to an interface | Apply when the consumer's operation is uniform; use switch/when when operations diverge |
| **Prag** | Kotlin `fun interface` + lambdas make lightweight dispatching trivial | Prefer for simple cases |
| **Did** | `instanceof` checks feel more explicit to beginners | Show how the OCP is violated by encoding-leaks; explain the long-term cost |

### SBPP-BEH-19:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH19-1** | When a consumer operates on data with multiple encodings, the interpretation SHALL be dispatched to the encoded object via an interface method. | Eliminates encoding-coupling |
| **CC-BEH19-2** | The dispatch interface method SHALL be named from the consumer's perspective (what it needs done). | Maintains caller intent clarity |

### SBPP-BEH-19:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Encoding Check**
```java
if (adjustment.getType() == AdjustmentType.PERCENT) { ... }
```
Fix: Give `Adjustment` an `applyTo()` method; each type implements its own logic.

### SBPP-BEH-19:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| New encodings added without modifying consumers | Interface per encoding type — manageable with sealed hierarchies |
| Consumer is decoupled from encoding decisions | Indirect dispatch can be harder to debug — use transparent naming |

### SBPP-BEH-19:10 - Rationale

Dispatched Interpretation is the general form of the Visitor-adjacent pattern where
objects interpret themselves in response to messages. It is the foundation for
Double Dispatch (BEH-20) and Mediating Protocol (BEH-21).

### SBPP-BEH-19:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Design Patterns (GoF, 1994; strategy/visitor widely applied post-2015):** Strategy pattern
is the formal expression of this pattern. *Adopt.*

**Kotlin sealed class + `when` (post-2016):** When exhaustive handling is needed, sealed
classes with `when` expressions are a compile-safe alternative. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Strategy pattern (widely used post-2015) | Dispatched execution | **Adopt** |
| Kotlin sealed class + `when` (post-2016) | Exhaustive dispatch | **Adopt** |
| Java 21 pattern matching switch | Compile-safe dispatch | **Adopt** |

### SBPP-BEH-19:12 - Relations

* **Foundation for:** SBPP-BEH-20 (Double Dispatch), SBPP-BEH-21 (Mediating Protocol)
* **Implements:** Strategy Pattern, Visitor-like dispatch
* **Relates to:** SBPP-BEH-15 (Choosing Message — single-receiver version)

### SBPP-BEH-19:End
