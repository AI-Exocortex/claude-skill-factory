## SBPP-BEH-09 - Reversing Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-09:1 - Problem frame

When writing fluent or pipelined code in Java/Kotlin, a sequence of operations may feel
"inside-out" because the natural subject of the sentence is not the receiver at the start
of the chain. Adding a method to the object that reverses the direction of the message
restores a natural reading order.

### SBPP-BEH-09:2 - Problem

How do you rewrite code that passes objects as arguments (breaking the "single receiver"
flow) so that all messages flow through a single object and the code reads in a natural order?

### SBPP-BEH-09:3 - Forces

| Force | Tension |
|-------|---------|
| **Fluency** | Code reading left-to-right matches thought flow ↔ argument-passing breaks the chain |
| **Coupling** | Reversing method couples the subject to the target | Justified when the relationship is fundamental |
| **Discoverability** | New method is findable via IDE completion ↔ adds to API surface |

### SBPP-BEH-09:4 - Solution — Add a method to the natural subject that accepts the other object

When a computation reads awkwardly because an object is passed as an argument rather
than being the receiver, add a method to the natural subject that accepts the other
object and delegates the work.

**Java example:**

```java
// ❌ Awkward: must read right-to-left; subject (order) is buried inside
double tax = TaxCalculator.calculate(order, TaxRegion.UK);

// ✅ Reversing Method on Order: order is the natural subject
public class Order {
    public Money taxFor(TaxRegion region) {
        return region.calculateTax(this);  // delegates back; region does the work
    }
}

// Now reads naturally left-to-right
Money tax = order.taxFor(TaxRegion.UK);

// Another example: serialization
// ❌ awkward
String json = JsonSerializer.serialize(event);

// ✅ reversing method
public class DomainEvent {
    public String toJson() {
        return JsonSerializer.serialize(this);
    }
}
String json = event.toJson();
```

**Kotlin example:**

```kotlin
// Extension function as Reversing Method
fun Order.taxFor(region: TaxRegion): Money = region.calculateTax(this)

// Or as member function
data class Order(val items: List<LineItem>) {
    fun taxFor(region: TaxRegion): Money = region.calculateTax(this)
}

// Call site reads as prose
val tax = order.taxFor(TaxRegion.UK)
```

**Rule:** Use Reversing Method when (a) the object is the natural subject of the sentence,
(b) the computation is fundamental to the object's role, and (c) it meaningfully improves
call-site readability. Do not add reversing methods for every utility function.

### SBPP-BEH-09:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Methods are added to domain objects so that computation flows through the domain subject.
*Show:* `order.taxFor(region)` reads as "the order's tax for this region"; `TaxCalc.calc(order, region)` does not.

**U.Episteme (design reasoning):**
*Tell:* Reversing methods restore the subject-verb-object sentence structure to code.
*Show:* A chain `order.validate().enrich().taxFor(region).toDto()` is readable as a pipeline because
every step is a method on the natural subject.

### SBPP-BEH-09:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin method fluency**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Reversing methods can gradually accumulate, bloating domain objects | Only add when the computation is genuinely fundamental to the object's role |
| **Arch** | May couple domain objects to infrastructure concerns (serialization, tax calculation) | Use Kotlin extension functions for reversing methods outside the domain's core concern |
| **Onto/Epist** | The "natural subject" is subjective; teams may disagree on which object owns the method | Design reviews; document reasoning in method Javadoc |
| **Prag** | Kotlin extension functions allow reversing without modifying the class | Prefer extensions for reversing methods in outer layers |
| **Did** | New developers may over-apply, adding reversing methods for every utility call | Teach with examples of appropriate vs. gratuitous use |

### SBPP-BEH-09:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH09-1** | A Reversing Method SHALL be added only when it meaningfully improves call-site readability. | Prevents gratuitous API expansion |
| **CC-BEH09-2** | Reversing Methods in outer layers (application, infrastructure) SHOULD be Kotlin extension functions. | Avoids coupling domain to outer-layer concerns |
| **CC-BEH09-3** | The reversing method MAY delegate to the original computation; it MUST NOT duplicate logic. | Single source of truth |

### SBPP-BEH-09:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Convenience Explosion**
Adding reversing methods for every utility call (`order.formatForEmail()`, `order.formatForSms()`, ...).
Fix: Only reverse when the method name reads as fundamental domain behaviour.

**Anti-pattern 2: Circular Delegation**
`order.taxFor(region)` calls `region.calculateTax(order)` which calls `order.taxFor(region)`.
Fix: Ensure the delegation terminates; the reversing method must delegate to a different method.

### SBPP-BEH-09:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Call-site code reads naturally as subject-verb-object | Adds to class API surface — use extensions for non-core reversals |
| Enables fluent method chains through a single object | Delegation adds one indirection — negligible on JVM |
| Improves discoverability via IDE completion on the domain object | — |

### SBPP-BEH-09:10 - Rationale

Beck's Reversing Method is the precursor to Kotlin's extension functions and Java's
method-reference patterns. It solves the readability problem by making the natural subject
the grammatical subject of the code sentence. In modern Java/Kotlin, extension functions
are the clean-architecture-safe mechanism for reversing methods that belong to outer layers.

### SBPP-BEH-09:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Kotlin extension functions (JetBrains, post-2016):** The primary modern mechanism for reversing
methods in Java/Kotlin. Allows adding subject-first methods without modifying the class. *Adopt.*

**Fluent API / Builder patterns (standard in Java post-2015):** Modern Java APIs (Stream, Optional)
are built on the reversing principle — computation flows through a single object chain. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin extension functions (post-2016) | Outer-layer reversing without coupling | **Adopt** |
| Java Stream/Optional API (Java 8+) | Fluent single-object chains | **Adopt** |
| Refactoring 2nd ed. — "Move Method" (Fowler, 2018) | Systematic method relocation | **Adopt** |

### SBPP-BEH-09:12 - Relations

* **Implements:** Fluent interface / subject-centric API design
* **Enables:** Method chaining (BEH-01 Composed Method at call site)
* **Extends:** SBPP-BEH-05 (Converter Method — often structured as a reversing method)
* **Relates to:** SBPP-BEH-21 (Mediating Protocol — reversal is one mediation technique)
* **Implemented by:** Kotlin extension functions for cross-layer reversals

### SBPP-BEH-09:End
