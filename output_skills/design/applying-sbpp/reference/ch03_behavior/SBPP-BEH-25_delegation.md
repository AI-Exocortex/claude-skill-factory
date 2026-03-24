## SBPP-BEH-25 - Delegation

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-25:1 - Problem frame

Inheritance is Java/Kotlin's built-in mechanism for code sharing, but it is often misused
for sharing implementation when no "is-a" relationship exists. Delegation — holding a
reference to a collaborator and forwarding messages to it — provides code reuse without the
coupling costs of inheritance.

### SBPP-BEH-25:2 - Problem

How does an object share implementation with another object when there is no meaningful
"is-a" relationship justifying inheritance?

### SBPP-BEH-25:3 - Forces

| Force | Tension |
|-------|---------|
| **Code Reuse** | Want to reuse logic without copying ↔ inheritance requires "is-a" |
| **Coupling** | Delegation couples caller to collaborator interface ↔ inheritance couples to full superclass |
| **Flexibility** | Delegate can be swapped at runtime ↔ superclass is fixed at compile time |

### SBPP-BEH-25:4 - Solution — Hold a reference; forward messages; prefer composition

Hold an instance of the collaborator as a field. Forward method calls to it. This is
"delegation" in the composition-over-inheritance sense. The delegating class controls
what it exposes from the delegate.

**Java example:**

```java
// ❌ Inheritance misuse: RatingEngine is not a "kind of" Repository
public class RatingEngine extends PolicyRepository {
    // uses Repository methods for convenience, but is NOT a repository
}

// ✅ Delegation: RatingEngine uses a Repository, does not extend it
public class RatingEngine {
    private final PolicyRepository policyRepository;   // delegate

    public RatingEngine(PolicyRepository policyRepository) {
        this.policyRepository = policyRepository;
    }

    public RatingResult ratePolicy(PolicyId id) {
        Policy policy = policyRepository.findById(id);  // forward to delegate
        return calculateRating(policy);
    }
}
```

**Kotlin — delegation by interface:**

```kotlin
interface Logger {
    fun log(message: String)
}

class ConsoleLogger : Logger {
    override fun log(message: String) = println(message)
}

// Kotlin's 'by' keyword implements delegation automatically
class AuditedService(
    private val delegate: Logger
) : Logger by delegate {  // all Logger methods forwarded to delegate
    // only override what needs to change
}

// Or explicit delegation
class RatingEngine(private val repo: PolicyRepository) {
    fun ratePolicy(id: PolicyId): RatingResult {
        val policy = repo.findById(id)    // delegated
        return calculateRating(policy)
    }
}
```

### SBPP-BEH-25:5 - Archetypal Grounding

**U.System:** `RatingEngine` holds a `PolicyRepository` field and calls `findById()` — delegating persistence to the repository.
**U.Episteme:** The `PolicyRepository` delegate can be swapped with a test double without any change to `RatingEngine`.

### SBPP-BEH-25:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Composition over inheritance in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Delegation requires more boilerplate than inheritance in Java | Kotlin `by` delegation reduces this; Lombok `@Delegate` for Java |
| **Arch** | Deep delegation chains obscure where logic lives | Keep delegation chains short (≤ 2 levels); name delegates clearly |
| **Onto/Epist** | "Has-a" vs "is-a" judgment requires domain understanding | Default to delegation; use inheritance only when "is-a" is unambiguous |
| **Prag** | Spring DI makes delegation the natural pattern via constructor injection | Leverage Spring; delegates are injected via constructor |
| **Did** | New developers gravitate to inheritance for its apparent simplicity | Teach delegation first; introduce inheritance when "is-a" is proven |

### SBPP-BEH-25:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH25-1** | Objects SHOULD hold collaborator references and forward method calls rather than extend collaborator classes. | Composition over inheritance |
| **CC-BEH25-2** | Delegates SHOULD be injected via constructor, not created internally. | Enables substitution and testing |
| **CC-BEH25-3** | Kotlin `by` delegation SHOULD be used for interface-forwarding patterns. | Reduces boilerplate |

### SBPP-BEH-25:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Convenience Inheritance**
Extending `ArrayList` to get list operations in a domain class.
Fix: Hold an `ArrayList` field and expose only the operations the domain class needs.

**Anti-pattern 2: Self-Created Delegate**
`this.cache = new LocalCache()` inside the constructor — delegate is not injectable.
Fix: Accept delegate via constructor; never create infrastructure inside domain classes.

### SBPP-BEH-25:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Delegate can be swapped at runtime (strategy/mock) | More boilerplate than inheritance in Java |
| No superclass coupling; delegate interface is the only contract | — |
| Multiple delegates can be composed freely | — |

### SBPP-BEH-25:10 - Rationale

"Favour composition over inheritance" (GoF, 1994) is one of the most important design
principles. Java's constructor injection idiom and Kotlin's `by` delegation make composition
the ergonomic default. Delegation is the mechanism.

### SBPP-BEH-25:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 18 ("Favour composition over inheritance").
*Adopt.*

**GoF "Favour composition over inheritance" (widely cited post-2015):** The foundational principle. *Adopt.*

**Kotlin `by` delegation (JetBrains, post-2016):** First-class language support for
delegation with `by` keyword. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 18 | **Adopt** |
| GoF composition principle (post-2015) | Composition over inheritance | **Adopt** |
| Kotlin `by` delegation (post-2016) | Language-level delegation | **Adopt** |

### SBPP-BEH-25:12 - Relations

* **Implements:** Composition over Inheritance principle
* **Contrast with:** SBPP-BEH-22 (Super — inheritance approach)
* **Specialised by:** SBPP-BEH-26 (Simple Delegation), SBPP-BEH-27 (Self Delegation)
* **Enables:** SBPP-BEH-28 (Pluggable Behavior — behavior is a delegate)

### SBPP-BEH-25:End
