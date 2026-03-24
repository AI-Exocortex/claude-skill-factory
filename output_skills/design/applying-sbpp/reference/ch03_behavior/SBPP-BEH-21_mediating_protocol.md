## SBPP-BEH-21 - Mediating Protocol

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-21:1 - Problem frame

In complex Java/Kotlin microservices, two objects may evolve an ad hoc interaction over
time, accumulating many different messages flowing in both directions. Without a defined
contract between them, adding a new type of interaction requires understanding and modifying
multiple methods on both sides. The interaction becomes a ball of mud.

### SBPP-BEH-21:2 - Problem

How do you formalise the interaction protocol between two independent objects so that their
communication is explicit, bounded, and independently changeable?

### SBPP-BEH-21:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Explicit protocol documents the interaction ↔ overhead of formalising every interaction |
| **Independence** | Both objects should be independently changeable ↔ they must agree on the protocol |
| **Cohesion** | Related messages should be grouped ↔ protocol definition adds a new abstraction |

### SBPP-BEH-21:4 - Solution — Define a named interface for the messages flowing between two objects

When two objects have a rich, bidirectional interaction, extract the messages from one
to the other into a named interface. This interface becomes the Mediating Protocol —
the contract that decouples them.

**Java example:**

```java
// Before: ad hoc interaction — Calculator talks directly to Policy in many ways
class RatingEngine {
    public Money rate(Policy policy) {
        double risk      = policy.getRiskScore();          // message 1
        String category  = policy.getCategory().code();   // message 2
        boolean hasHistory = policy.hasClaimHistory();    // message 3
        int yearsNoClam  = policy.getYearsNoClaim();      // message 4
        // ... engine uses all four; Policy knows RatingEngine exists
    }
}

// After: Mediating Protocol
public interface RateablePolicy {    // the protocol between engine and policy
    double riskScore();
    String categoryCode();
    boolean hasClaimHistory();
    int yearsNoClaim();
}

public class InsurancePolicy implements RateablePolicy { ... }

// RatingEngine now depends only on the protocol, not on InsurancePolicy
class RatingEngine {
    public Money rate(RateablePolicy policy) {
        // ... uses only the protocol methods
    }
}
```

**Kotlin:**

```kotlin
interface RateablePolicy {
    val riskScore: Double
    val categoryCode: String
    val hasClaimHistory: Boolean
    val yearsNoClaim: Int
}

class InsurancePolicy : RateablePolicy { ... }

class RatingEngine {
    fun rate(policy: RateablePolicy): Money { ... }
}
```

### SBPP-BEH-21:5 - Archetypal Grounding

**U.System:** `RatingEngine` depends on `RateablePolicy` interface, not `InsurancePolicy`. Both can evolve independently.
**U.Episteme:** The `RateablePolicy` interface documents exactly what the rating engine needs from a policy — no more, no less.

### SBPP-BEH-21:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Object collaboration protocol in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Many small interfaces (Interface Segregation) can be hard to navigate | Group into meaningful role interfaces; use package structure |
| **Arch** | Protocol interfaces add a layer of indirection | Accepted cost; benefits independence and testability |
| **Onto/Epist** | "What does the consuming object really need?" requires analysis | Derive the protocol from actual usage, not from the full domain object API |
| **Prag** | Java/Kotlin structural typing (interfaces) requires explicit implementation | Kotlin extension functions can simulate protocol adherence for non-modifiable types |
| **Did** | ISP (Interface Segregation Principle) formalises this; introduce via ISP | Teach ISP alongside Mediating Protocol |

### SBPP-BEH-21:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH21-1** | When two objects have > 3 messages flowing between them, the messages SHALL be captured in a named interface. | Documents and bounds the protocol |
| **CC-BEH21-2** | Mediating Protocol interfaces SHALL be named from the consumer's perspective (role the producer plays for the consumer). | Communicates the relationship |
| **CC-BEH21-3** | Protocol interfaces SHOULD include only what the consumer actually needs (Interface Segregation). | Minimises coupling |

### SBPP-BEH-21:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: God Interface**
The protocol interface exposes the full domain object API rather than just what the consumer needs.
Fix: Derive the interface from actual usage; add only the methods the consumer calls.

**Anti-pattern 2: Leaky Protocol**
The interface exposes infrastructure concerns (e.g., `getEntityId()` for DB purposes).
Fix: Keep domain protocols pure; infrastructure needs go in separate interfaces.

### SBPP-BEH-21:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Both objects can evolve independently, constrained only by the protocol | Additional interface per significant collaboration |
| Protocol is testable independently with mocks/stubs | — |
| Documents the exact communication contract | — |

### SBPP-BEH-21:10 - Rationale

Mediating Protocol is the practical expression of the Interface Segregation Principle and
the Dependency Inversion Principle at the pair-collaboration level. It is the standard
mechanism for decoupling objects in hexagonal/clean architecture.

### SBPP-BEH-21:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**SOLID ISP (Martin, ongoing):** Clients should not be forced to depend on methods they do not use.
Mediating Protocol is ISP applied to object collaboration. *Adopt.*

**Hexagonal Architecture (Ports & Adapters, post-2015):** Ports are Mediating Protocols between
the domain and the outside world. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| SOLID ISP (Martin, ongoing) | Interface segregation | **Adopt** |
| Hexagonal Architecture Ports (post-2015) | Port = Mediating Protocol | **Adopt** |
| DDD Anti-Corruption Layer (Vernon, 2016) | Protocol isolation at context boundary | **Adopt** |

### SBPP-BEH-21:12 - Relations

* **Implements:** Interface Segregation Principle, Ports & Adapters
* **Extends:** SBPP-BEH-14 (Message — protocols define the messages)
* **Relates to:** SBPP-BEH-25 (Delegation — protocols mediate delegation)
* **Constrains:** Both collaborating objects to the agreed protocol only

### SBPP-BEH-21:End
