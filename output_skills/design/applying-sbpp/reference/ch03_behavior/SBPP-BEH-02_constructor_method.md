## SBPP-BEH-02 - Constructor Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-02:1 - Problem frame

In Java and Kotlin, objects must be created before they can be used. Raw constructors
(`new Foo(a, b, c)` or `Foo(a, b, c)`) leak implementation detail about the number and
type of parameters, making it hard to evolve the object's internal representation.
Teams building microservices often encounter this problem when domain objects are
instantiated in many places, and a future structural change forces widespread edits.

### SBPP-BEH-02:2 - Problem

How do you provide object creation in a way that hides internal representation,
communicates the intent of each creation scenario, and allows the representation to
change without affecting callers?

### SBPP-BEH-02:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation vs Convenience** | Hiding constructor params ↔ direct `new` is simple |
| **Expressiveness vs Simplicity** | Named factory methods reveal intent ↔ add API surface |
| **Flexibility vs Stability** | Factory can return subtypes ↔ callers can't subclass factory easily |

### SBPP-BEH-02:4 - Solution — Provide named static factory methods as primary creation API

Provide one or more static factory methods (or companion object functions in Kotlin) that
communicate the reason for creation. Name them after the scenario they represent, not the
implementation they invoke.

**Java example:**

```java
public final class Money {
    private final long cents;
    private final Currency currency;

    // Private constructor — hides representation
    private Money(long cents, Currency currency) {
        this.cents = cents;
        this.currency = currency;
    }

    // Named factory methods — communicate intent
    public static Money of(long cents, Currency currency) {
        return new Money(cents, currency);
    }

    public static Money zero(Currency currency) {
        return new Money(0, currency);
    }

    public static Money fromDollars(double dollars, Currency currency) {
        return new Money(Math.round(dollars * 100), currency);
    }
}

// Usage — intent is clear at the call site
var price = Money.of(1999, Currency.USD);
var free  = Money.zero(Currency.EUR);
```

**Kotlin example:**

```kotlin
class Money private constructor(
    val cents: Long,
    val currency: Currency
) {
    companion object {
        fun of(cents: Long, currency: Currency) = Money(cents, currency)
        fun zero(currency: Currency) = Money(0, currency)
        fun fromDollars(dollars: Double, currency: Currency) =
            Money((dollars * 100).roundToLong(), currency)
    }
}

// Usage
val price = Money.of(1999, Currency.USD)
val free  = Money.zero(Currency.EUR)
```

For simple value objects in Kotlin, also consider using a data class with
a private constructor + companion factory.

### SBPP-BEH-02:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Domain value objects expose only named factory methods; raw constructors are private.
*Show:* `Money.fromDollars(9.99, USD)` is unambiguous; `new Money(999, USD)` is not.

**U.Episteme (design reasoning):**
*Tell:* Named creation methods document the usage contract; anonymous parameter lists do not.
*Show:* A future refactoring that changes `cents` to `BigDecimal` only touches the factory bodies,
not every call site in the codebase.

### SBPP-BEH-02:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin domain object creation**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Multiple factory methods increase API surface; governance of which factories are "official" is needed | Document intended creation paths in Javadoc/KDoc; deprecate obsolete ones |
| **Arch** | Factories cannot be easily subclassed for testing without interfaces | Define a CreationStrategy or use abstract factory; prefer interfaces for injection |
| **Onto/Epist** | Factory method names encode assumptions about usage scenarios that may not be stable | Keep factory names general enough to survive domain evolution |
| **Prag** | Kotlin data classes + `copy()` already solve many factory use cases | Use data classes where appropriate; use factory pattern when invariant validation is required |
| **Did** | New developers often overlook factory methods and use constructors directly | Enforce via constructor visibility (private/internal) |

### SBPP-BEH-02:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH02-1** | Primary creation paths SHALL be static factory methods with intention-revealing names. | Communicates creation intent |
| **CC-BEH02-2** | Raw constructors SHOULD be private or package-private when factory methods exist. | Enforces encapsulation |
| **CC-BEH02-3** | Factory methods SHALL validate invariants before constructing the object. | Ensures object validity |
| **CC-BEH02-4** | Multiple factory methods for the same class SHALL have distinct, non-overloaded names. | Avoids ambiguous overload resolution |

### SBPP-BEH-02:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Telescoping Constructors**
```java
new Order(customer, items, discount, shipping, null, null)
```
Fix: Use Builder pattern (Java) or named parameters (Kotlin) for objects with many optional fields.

**Anti-pattern 2: Anemic Factory**
A factory method named `create()` or `newInstance()` that adds no semantic information.
Fix: Name the factory after the scenario: `forNewCustomer()`, `fromImport()`, `draft()`.

### SBPP-BEH-02:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Internal representation can change without affecting call sites | Slightly more code than plain `new` — justified by encapsulation |
| Factory method names appear in stack traces, aiding debugging | Multiple factories increase API surface — mitigated by clear naming and deprecation strategy |
| Factory can return a subtype or cached instance | Cannot use `new` syntax — acceptable in OO code |

### SBPP-BEH-02:10 - Rationale

Beck's Constructor Method pattern addresses the fundamental tension between object creation
convenience and representation encapsulation. In Java/Kotlin, this maps directly to Bloch's
advice in Effective Java (Item 1: "Consider static factory methods instead of constructors").

Kotlin's named parameters and default values reduce the pressure for many factory methods
in simple cases, but factory methods remain essential when: (1) invariant validation is required
at creation, (2) the returned type may be a subtype, or (3) multiple distinct creation
scenarios exist with the same parameter types.

### SBPP-BEH-02:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 1 ("Consider static factory methods instead of
constructors") is the canonical Java articulation of this pattern. Bloch lists five advantages
including descriptive names and ability to return subtypes. *Adopt directly.*

**Kotlin Idioms (kotlinlang.org, continuously updated post-2015):** Kotlin companion object
functions are the idiomatic equivalent. Named and default parameters further reduce the need
for overloaded constructors. *Adopt: companion factories are idiomatic Kotlin.*

**Domain-Driven Design (Evans, reissued; Vernon 2016):** Value objects MUST enforce invariants
at creation; factory methods are the standard mechanism. *Adopt: DDD mandates this pattern.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 1 — static factory methods | **Adopt** |
| Kotlin companion object idioms (post-2015) | Companion factories | **Adopt** |
| DDD / Vernon "Implementing DDD" (2016) | Value object creation | **Adopt** |

### SBPP-BEH-02:12 - Relations

* **Implements:** Encapsulation, Information Hiding
* **Extends:** SBPP-BEH-03 (Constructor Parameter Method)
* **Relates to:** SBPP-BEH-04 (Shortcut Constructor Method)
* **Constrained by:** Object invariant requirements
* **Constrains:** SBPP-STA-03 (Explicit Initialization — initialized via factory)

### SBPP-BEH-02:End
