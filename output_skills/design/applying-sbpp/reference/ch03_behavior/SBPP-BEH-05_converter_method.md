## SBPP-BEH-05 - Converter Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-05:1 - Problem frame

Domain objects in Java/Kotlin microservices often need to be represented in different forms:
a `Money` object becomes a `BigDecimal` for accounting, a `String` for display, a DTO for
the API layer. The question is where this conversion logic should live, and how it should
be named so that callers understand what they're getting.

### SBPP-BEH-05:2 - Problem

How do you represent the conversion of an object into another object with compatible
protocol but different format or representation, in a way that is discoverable and
keeps the source object's class from being cluttered with unrelated conversion logic?

### SBPP-BEH-05:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion** | Conversion belongs near the source ↔ too many conversions bloat the source class |
| **Discoverability** | `asX()` naming is easy to find ↔ not all targets deserve an instance method |
| **Coupling** | Converter method on source couples source to target type | Move to target when coupling is undesirable |

### SBPP-BEH-05:4 - Solution — Provide `toX()` instance methods for closely related representations

When a conversion is logically "part of" the source object's role and the target type is
closely related, implement the conversion as an instance method named `toX()` (Java) or
`toX()` / `asX()` (Kotlin).

**Java example:**

```java
public final class Money {
    private final long cents;
    private final Currency currency;

    public Money(long cents, Currency currency) {
        this.cents = cents;
        this.currency = currency;
    }

    // Converter Method — same data, different representation
    public BigDecimal toDecimal() {
        return BigDecimal.valueOf(cents, 2);
    }

    public String toDisplayString() {
        return String.format("%s %.2f", currency.getSymbol(), toDecimal());
    }

    public MoneyDto toDto() {
        return new MoneyDto(cents, currency.getCode());
    }
}
```

**Kotlin example:**

```kotlin
data class Money(val cents: Long, val currency: Currency) {
    fun toDecimal(): BigDecimal = BigDecimal.valueOf(cents, 2)
    fun toDisplayString(): String = "${currency.symbol} ${toDecimal()}"
    fun toDto(): MoneyDto = MoneyDto(cents, currency.code)
}

// Extension function for conversions that don't belong on the domain class:
fun Money.toAccountingEntry(): AccountingEntry =
    AccountingEntry(amount = toDecimal(), currencyCode = currency.code)
```

**Rule:** Use instance `toX()` methods when the conversion is fundamental to the type's
purpose. Use extension functions (Kotlin) or separate converter classes when the
conversion belongs to a different bounded context.

### SBPP-BEH-05:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* A domain value object provides `toDto()`, `toDecimal()` for its natural output forms.
*Show:* `order.getTotal().toDecimal()` is readable; a static `MoneyConverter.toDecimal(money)` is not.

**U.Episteme (design reasoning):**
*Tell:* Naming a conversion after its target makes the output type explicit without reading the implementation.
*Show:* `price.toDisplayString()` announces its return type in its name; `price.format()` does not.

### SBPP-BEH-05:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Domain object conversion in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Many `toX()` methods can make domain classes depend on infrastructure/DTO types | Use Kotlin extension functions or MapStruct for cross-layer conversion |
| **Arch** | Converter methods couple the domain model to presentation/persistence layers | Keep `toDto()` in application layer; domain class should not know DTO shapes |
| **Onto/Epist** | `asX()` vs `toX()` convention is inconsistent across JDK (e.g., `toString()` vs `toArray()`) | Establish team convention: `to` = different type, `as` = same data different view |
| **Prag** | MapStruct and ModelMapper automate DTO conversion; hand-written converters may be redundant | Use this pattern for domain-layer conversion; delegate DTO mapping to frameworks |
| **Did** | New developers may add converters to domain classes for every downstream format | Constrain: domain classes provide core conversions only; all others via extension/mapper |

### SBPP-BEH-05:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH05-1** | Converter methods SHALL be named `toX()` where X is the target type name. | Ensures discoverability and naming consistency |
| **CC-BEH05-2** | Domain classes SHOULD NOT implement converter methods to types in outer application layers (DTOs, API models). | Prevents domain-infrastructure coupling |
| **CC-BEH05-3** | Cross-layer conversions SHALL be implemented as Kotlin extension functions or dedicated mapper classes. | Maintains clean architecture layer boundaries |

### SBPP-BEH-05:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Conversion Method Proliferation**
A domain class accumulates 20+ `toX()` methods for every format any consumer might need.
Fix: Domain classes provide only core conversions (`toDecimal()`, `toString()`);
all others live in dedicated mappers or extension functions.

**Anti-pattern 2: Lossy Conversion without Warning**
`money.toDecimal()` silently drops currency information.
Fix: Either include all meaningful data in the conversion or name the loss explicitly:
`money.toUnsafeCentsDecimal()`.

### SBPP-BEH-05:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Conversion is discoverable via IDE completion on the source object | Domain class grows — mitigated by extension functions for non-core conversions |
| Fluent call chains: `order.total().toDecimal().setScale(2, HALF_UP)` | Coupling risk — mitigated by layer discipline |
| Self-documenting output type in method name | — |

### SBPP-BEH-05:10 - Rationale

Beck's concern about conversion proliferation ("twenty or thirty `as…` methods") is directly
relevant to Java microservices, where domain objects are converted to DTOs, JSON, database
records, and event payloads. The solution in modern Java/Kotlin is a layer-conscious
application of the pattern: core conversions on the domain object, cross-layer conversions
in extension functions or mapper classes.

### SBPP-BEH-05:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Clean Architecture (Martin, 2017):** Domain entities must not depend on outer layers.
Converter methods to DTOs violate this. *Adapt: use extension functions for cross-layer conversion.*

**Kotlin extension functions (JetBrains, post-2016):** Allow adding `toX()` conversions in
the consumer's package without modifying the source class. Directly resolves Beck's
proliferation concern. *Adopt: extensions for cross-layer; instance methods for domain-native.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Architecture (Martin, 2017) | Layer separation constrains `toDto()` placement | **Adapt** |
| Kotlin extension functions (post-2016) | Extension-based conversion avoids proliferation | **Adopt** |
| MapStruct / ModelMapper (2015+) | Framework-based DTO mapping | **Adapt** — use for DTO layers |

### SBPP-BEH-05:12 - Relations

* **Paired with:** SBPP-BEH-06 (Converter Constructor Method — complementary directions)
* **Constrained by:** Clean Architecture layer rules (no domain → infrastructure dependency)
* **Relates to:** SBPP-BEH-07 (Query Method — converter is a specialised query)
* **Constrains:** SBPP-COL-05 (Equality Method — two `Money` objects converted the same way must be equal)

### SBPP-BEH-05:End
