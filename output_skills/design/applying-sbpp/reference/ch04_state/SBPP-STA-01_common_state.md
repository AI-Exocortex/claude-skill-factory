## SBPP-STA-01 - Common State

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-01:1 - Problem frame

Every Java/Kotlin object has fields. Choosing which state to encode as typed instance
variables — versus deferring to maps, property bags, or runtime-added fields — is a
foundational design decision. Common State addresses the simplest, best case: state that
all (or nearly all) instances share.

### SBPP-STA-01:2 - Problem

How do you represent state that is shared by all instances of a class, so that the
structure is explicit, type-safe, and accessible to tools (IDE, refactoring, serialisation)?

### SBPP-STA-01:3 - Forces

| Force | Tension |
|-------|---------|
| **Explicitness** | Typed fields are visible in IDE and refactoring ↔ dynamic maps are flexible |
| **Type Safety** | Compile-time field type checking ↔ map values are untyped |
| **Performance** | Field access is direct ↔ map lookup is O(1) but adds overhead |
| **Tooling** | IDEs navigate fields instantly ↔ dynamic keys are invisible to tooling |

### SBPP-STA-01:4 - Solution — Declare shared state as typed instance fields; use Java records or Kotlin data classes for value objects

When all (or nearly all) instances have the same set of state, declare it as typed
instance fields. For immutable value objects use Java records or Kotlin data classes.

**Java example:**

```java
// ✅ Common State as typed fields — explicit, IDE-navigable, type-safe
public final class InsurancePolicy {
    private final PolicyId id;
    private final CustomerId holderId;
    private PolicyStatus status;
    private Money premium;
    private LocalDate expiryDate;

    public InsurancePolicy(PolicyId id, CustomerId holderId, Money premium, LocalDate expiryDate) {
        this.id        = Objects.requireNonNull(id);
        this.holderId  = Objects.requireNonNull(holderId);
        this.premium   = Objects.requireNonNull(premium);
        this.expiryDate = Objects.requireNonNull(expiryDate);
        this.status    = PolicyStatus.DRAFT;
    }
}

// ✅ Java record for immutable value objects (Java 16+)
public record Money(long cents, Currency currency) {
    public Money {
        Objects.requireNonNull(currency);
        if (cents < 0) throw new IllegalArgumentException("Negative money: " + cents);
    }
}
```

**Kotlin example:**

```kotlin
// ✅ Common State as typed properties
class InsurancePolicy(
    val id: PolicyId,
    val holderId: CustomerId,
    var premium: Money,
    var expiryDate: LocalDate,
    var status: PolicyStatus = PolicyStatus.DRAFT
)

// ✅ Kotlin data class for value objects
data class Money(val cents: Long, val currency: Currency) {
    init {
        require(cents >= 0) { "Negative money: $cents" }
    }
}
```

**Rule:** If state is shared by all instances → typed field.
If state is present in some instances but not others → see SBPP-STA-02 (Variable State).

### SBPP-STA-01:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Domain objects declare their state as typed fields; no Map<String,Object> property bags.
*Show:* `policy.getPremium()` returns `Money`; the IDE knows the type and autocompletes all
`Money` methods. `policy.getProperties().get("premium")` returns `Object`.

**U.Episteme (design reasoning):**
*Tell:* Typed fields make the object's data model visible and verifiable at compile time.
*Show:* Renaming `premium` to `basePremium` is a safe compiler-guided refactoring;
renaming a Map key is a grep-and-pray operation.

### SBPP-STA-01:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin object state design**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Schema migrations become necessary when fields change | Use versioned DTOs at system boundaries; keep domain model free to evolve |
| **Arch** | Mutable fields create thread-safety concerns | Make fields `final`/`val` where possible; document mutability clearly |
| **Onto/Epist** | "All instances" may hide future variation | Revisit when a feature requires optional state; consider Variable State then |
| **Prag** | Java records and Kotlin data classes eliminate much boilerplate | Use them for value objects; full class for entities with complex lifecycle |
| **Did** | Over-designing fields (too many on one class) creates God Objects | Apply SRP; split when a class exceeds ~7-10 fields meaningfully |

### SBPP-STA-01:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA01-1** | State shared by all instances SHALL be declared as typed instance fields. | Explicitness and type safety |
| **CC-STA01-2** | Fields SHOULD be `private` (Java) or `private`/`internal` (Kotlin); expose via methods or properties. | Encapsulation |
| **CC-STA01-3** | Immutable value objects SHOULD use Java records or Kotlin data classes. | Eliminates boilerplate; enforces immutability |
| **CC-STA01-4** | Fields representing domain invariants MUST be validated at construction time. | Maintains valid state |

### SBPP-STA-01:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Property Bag**
```java
private Map<String, Object> properties = new HashMap<>();
```
Used where typed fields should be. Fix: Declare actual fields; use Variable State (STA-02)
only for genuinely dynamic state.

**Anti-pattern 2: God Object**
One class accumulates 25 fields because "all policies have these." Fix: Split into
cohesive sub-objects (e.g., `PolicyHolder`, `CoverageTerms`, `PremiumDetails`).

### SBPP-STA-01:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| IDE navigation, refactoring, and documentation work on typed fields | Schema evolution requires migration for persisted data |
| Compile-time type checking catches misuse | More upfront design — justified by long-term maintainability |
| Java records / Kotlin data classes generate equals, hashCode, toString | — |

### SBPP-STA-01:10 - Rationale

Common State is the baseline of object-oriented design — it is how objects differ from
hash maps. Java records (Java 16+) and Kotlin data classes eliminate the historical
boilerplate objection. Every domain object's state should be expressed as typed fields
unless there is a concrete reason for dynamic state (Variable State, BEH-02).

### SBPP-STA-01:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 17 (minimise mutability) and Item 15 (minimise
accessibility of classes and members). Both reinforce typed, encapsulated fields. *Adopt.*

**Java 16 Records (JEP 395, 2021):** Language-level support for immutable data carriers.
Direct embodiment of Common State for value objects. *Adopt.*

**Kotlin data classes (JetBrains, post-2016):** Idiomatic Common State for value objects.
*Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Items 15, 17 | **Adopt** |
| Java 16 Records (JEP 395, 2021) | Typed immutable Common State | **Adopt** |
| Kotlin data classes (post-2016) | Idiomatic value object state | **Adopt** |

### SBPP-STA-01:12 - Relations

* **Precedes:** SBPP-STA-02 (Variable State — for optional/dynamic state)
* **Constrains:** SBPP-STA-03 (Explicit Initialization), SBPP-STA-04 (Lazy Initialization)
* **Enables:** SBPP-STA-07 (Direct Variable Access), SBPP-STA-08 (Indirect Variable Access)
* **Named by:** SBPP-STA-14 (Role Suggesting Instance Variable Name)

### SBPP-STA-01:End
