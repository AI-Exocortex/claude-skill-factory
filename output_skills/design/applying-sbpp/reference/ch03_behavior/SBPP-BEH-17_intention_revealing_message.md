## SBPP-BEH-17 - Intention Revealing Message

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-17:1 - Problem frame

In Java/Kotlin microservices, some operations are trivially simple in implementation but
important in intent. Writing `this.status = Status.ACTIVE` everywhere is clear mechanically
but communicates nothing about business intent. Naming the operation reveals what is happening
in domain terms, even when the implementation is a single line.

### SBPP-BEH-17:2 - Problem

How do you communicate the intent of a simple operation when the implementation alone
would not tell a reader what business event is occurring?

### SBPP-BEH-17:3 - Forces

| Force | Tension |
|-------|---------|
| **Intent Communication** | Named method reveals domain meaning ↔ trivial one-liners seem wasteful |
| **Reusability** | Named method can be overridden or extended ↔ inlined call cannot |
| **Discoverability** | Method name appears in IDE completion and call hierarchy ↔ inlined code does not |

### SBPP-BEH-17:4 - Solution — Extract one-line operations when the method name communicates domain intent

When a low-level operation has a domain-meaningful name that the implementation cannot
convey, extract it into a method even if the body is a single expression.

**Java example:**

```java
public class InsurancePolicy {
    private PolicyStatus status;

    // ❌ Without Intention Revealing Message
    void processRenewal() {
        this.status = PolicyStatus.ACTIVE;    // What does this mean in business terms?
        this.expiryDate = LocalDate.now().plusYears(1);
    }

    // ✅ With Intention Revealing Messages
    void processRenewal() {
        activate();
        extendCoverageForOneYear();
    }

    private void activate() {
        this.status = PolicyStatus.ACTIVE;
    }

    private void extendCoverageForOneYear() {
        this.expiryDate = LocalDate.now().plusYears(1);
    }
}
```

**Kotlin example:**

```kotlin
class InsurancePolicy {
    var status: PolicyStatus = PolicyStatus.DRAFT
    var expiryDate: LocalDate = LocalDate.now()

    fun processRenewal() {
        activate()
        extendCoverageForOneYear()
    }

    private fun activate() { status = PolicyStatus.ACTIVE }
    private fun extendCoverageForOneYear() { expiryDate = LocalDate.now().plusYears(1) }
}
```

### SBPP-BEH-17:5 - Archetypal Grounding

**U.System:** `activate()` in a policy class documents a state transition in domain vocabulary; direct field assignment does not.
**U.Episteme:** A method named `activate()` can be found in call hierarchies, grepped for, and appears in stack traces — the inline assignment does none of these.

### SBPP-BEH-17:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Intent communication in Java/Kotlin OO code**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Trivial one-line methods increase class size | Accept the cost — domain vocabulary methods are worth it |
| **Arch** | JIT inlines one-line methods; zero runtime cost | No mitigation needed |
| **Onto/Epist** | Method name may drift from its implementation over time | Keep implementations as one-liners; if they grow, the name may be wrong |
| **Prag** | Kotlin extension properties can express domain state changes concisely | Use either; prefer whatever reads most naturally in domain terms |
| **Did** | New developers dismiss single-line extractions as pointless | Demonstrate the business vocabulary benefit during code review |

### SBPP-BEH-17:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH17-1** | Domain state transitions SHOULD be named methods even when implementation is a single statement. | Communicates business intent |
| **CC-BEH17-2** | Intention Revealing Messages SHOULD use domain vocabulary, not technical vocabulary. | `activate()` not `setStatusActive()` |

### SBPP-BEH-17:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Technical Name**
`setStatusToActive()` — names the implementation, not the intent. Fix: `activate()`.

**Anti-pattern 2: Growing Body**
The "intention revealing" method body grows to 20 lines. Fix: Rename to reflect the expanded
scope or decompose further.

### SBPP-BEH-17:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Code reads in domain vocabulary | More methods per class |
| Business intent appears in call hierarchies and stack traces | — |
| State transitions can be overridden in subclasses | — |

### SBPP-BEH-17:10 - Rationale

Intention Revealing Message bridges code and domain model. In DDD terms, these methods
are the vocabulary of the Ubiquitous Language expressed in code. Every domain event or
state transition should have a name that a domain expert would recognise.

### SBPP-BEH-17:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**DDD Ubiquitous Language (Evans/Vernon, 2016):** Domain operations must be named in the
language of the domain experts. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Method names should communicate intent at all granularities. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| DDD Ubiquitous Language (Vernon, 2016) | Domain vocabulary in code | **Adopt** |
| Clean Code (Martin, ongoing) | Intent-revealing names at all levels | **Adopt** |

### SBPP-BEH-17:12 - Relations

* **Extends:** SBPP-BEH-18 (Intention Revealing Selector — the naming rule)
* **Implements:** DDD Ubiquitous Language principle
* **Foundation for:** SBPP-BEH-16 (Decomposing Message — each sub-operation is intention-revealing)

### SBPP-BEH-17:End
