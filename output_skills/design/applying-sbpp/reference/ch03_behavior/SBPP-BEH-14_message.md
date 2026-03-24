## SBPP-BEH-14 - Message

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-14:1 - Problem frame

This is a foundational pattern capturing the core OO principle: computation should be
invoked by sending a message to an object, not by procedural calls. In Java/Kotlin, the
"message" is a method call on an object reference. The pattern establishes the mental model
for all subsequent message-related patterns.

### SBPP-BEH-14:2 - Problem

How do you invoke computation in an object-oriented system so that the receiver has the
flexibility to respond in whatever way is appropriate for its type, enabling polymorphism
and encapsulation?

### SBPP-BEH-14:3 - Forces

| Force | Tension |
|-------|---------|
| **Polymorphism** | Same message name, different implementations per receiver | Requires type hierarchy or interface |
| **Encapsulation** | Caller does not know how receiver implements the response ↔ debugging requires knowledge of the hierarchy |
| **Coupling** | Message names must be stable ↔ implementations can change freely |

### SBPP-BEH-14:4 - Solution — Express computation as method calls on objects; program to interfaces

All computation is expressed as method calls. The caller knows only the interface (message
name and signature), not the receiver's type. Code to interfaces or abstract types, not
concrete classes.

**Java example:**

```java
// ✅ Message-centric: caller sends message to interface; receiver decides how
public interface PremiumCalculator {
    Money calculate(Policy policy);
}

public class RiskBasedCalculator implements PremiumCalculator {
    @Override
    public Money calculate(Policy policy) {
        return riskTable.lookup(policy.category()).multiply(policy.sumInsured());
    }
}

public class FlatRateCalculator implements PremiumCalculator {
    @Override
    public Money calculate(Policy policy) {
        return flatRate;
    }
}

// Caller is unaware which calculator it talks to
class UnderwritingService {
    private final PremiumCalculator calculator;  // message sent to interface

    public Money quote(Policy policy) {
        return calculator.calculate(policy);  // the "message"
    }
}
```

**Kotlin example:**

```kotlin
fun interface PremiumCalculator {
    fun calculate(policy: Policy): Money
}

class UnderwritingService(private val calculator: PremiumCalculator) {
    fun quote(policy: Policy): Money = calculator.calculate(policy)
}

// Kotlin SAM conversion — concise message receiver
val service = UnderwritingService { policy ->
    riskTable.lookup(policy.category) * policy.sumInsured
}
```

### SBPP-BEH-14:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* All inter-object computation is expressed as method calls on interface references.
*Show:* `calculator.calculate(policy)` — the caller doesn't know or care if the calculator
is risk-based, flat-rate, or a test stub.

**U.Episteme (design reasoning):**
*Tell:* Programming to interfaces separates the what (message name) from the how (implementation).
*Show:* Swapping `RiskBasedCalculator` for `FlatRateCalculator` requires zero changes to `UnderwritingService`.

### SBPP-BEH-14:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Core OO invocation model in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Interface proliferation when every pair of classes communicates through an interface | Use interfaces where substitutability is real; skip for final/internal collaborations |
| **Arch** | Virtual dispatch overhead compared to direct calls | JIT inlines monomorphic call sites; overhead is negligible in practice |
| **Onto/Epist** | "Sending a message" is a mental model; Java method call is not identical to Smalltalk message | The polymorphism semantics are equivalent; accept the conceptual mapping |
| **Prag** | Kotlin functional types and SAM conversions make lightweight message passing idiomatic | Use functional types for single-method interfaces |
| **Did** | New developers may skip interfaces for "simple" cases and couple directly to concrete types | Teach: program to the interface you need, not the implementation you have |

### SBPP-BEH-14:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH14-1** | Dependencies between collaborating objects SHALL be expressed as interface or abstract type references, not concrete types. | Enables polymorphism and testability |
| **CC-BEH14-2** | Method calls SHOULD be treated as messages: the caller specifies what it needs, not how the receiver should do it. | Preserves encapsulation |
| **CC-BEH14-3** | Kotlin single-method interfaces SHOULD use `fun interface` for SAM conversion support. | Idiomatic Kotlin |

### SBPP-BEH-14:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Concrete Dependency**
```java
private RiskBasedCalculator calculator;  // ❌ coupled to implementation
```
Fix: `private PremiumCalculator calculator;` — depend on the interface.

**Anti-pattern 2: Type Checking Before Messaging**
```java
if (calculator instanceof RiskBasedCalculator) { ... }
```
Fix: Add a method to the interface that provides the information needed without casting.

### SBPP-BEH-14:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Polymorphic dispatch enables Open/Closed extension | Interface per collaborator can create many small files |
| Callers are isolated from implementation changes | Indirection adds a level to navigate in IDE |
| Enables mock/stub testing without framework magic | — |

### SBPP-BEH-14:10 - Rationale

This is the foundational OO principle. Every subsequent pattern in the Behavior chapter
is built on it. Java interfaces and Kotlin fun interfaces are the mechanical expression of
Beck's "message" concept. Programming to interfaces is a non-negotiable principle in
enterprise Java/Kotlin.

### SBPP-BEH-14:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 64 ("Refer to objects by their interfaces").
This is the Java articulation of "Message". *Adopt.*

**Clean Code (Martin, 2008/ongoing):** "Depend on abstractions, not concretions" (DIP).
The Dependency Inversion Principle is Message at the architectural level. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 64 — interface references | **Adopt** |
| SOLID DIP (Martin, ongoing) | Depend on abstractions | **Adopt** |
| Kotlin `fun interface` (post-2016) | SAM-conversion message receivers | **Adopt** |

### SBPP-BEH-14:12 - Relations

* **Foundation for:** All subsequent message patterns (BEH-15 through BEH-31)
* **Implements:** Polymorphism, Encapsulation, Open/Closed Principle
* **Constrains:** All collaborating objects should communicate via interfaces

### SBPP-BEH-14:End
