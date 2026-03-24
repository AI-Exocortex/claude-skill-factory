## SBPP-BEH-06 - Converter Constructor Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-06:1 - Problem frame

When one type needs to be created from another with a different structure, the conversion
can be expressed either as an `asX()` method on the source, or as a constructor/factory on
the target that accepts the source. In a Java/Kotlin microservice, receiving an external
representation (a DTO, a JSON-parsed object, a database record) and converting it into a
domain object is a pervasive operation that needs a clear, consistent home.

### SBPP-BEH-06:2 - Problem

How do you convert an object of one type into an object of a substantially different type,
when the target type has a different protocol, not just a different format?

### SBPP-BEH-06:3 - Forces

| Force | Tension |
|-------|---------|
| **Coupling direction** | Factory on target knows source type ↔ method on source knows target type |
| **Discoverability** | Conversion on source is found by IDE completion ↔ conversion on target is found where target is used |
| **Layer ownership** | Domain object should not know DTO format ↔ DTO factory that knows domain format couples infrastructure to domain |

### SBPP-BEH-06:4 - Solution — Put the conversion factory on the target type or in an assembler

When the target type is the natural "owner" of the conversion (it knows what it needs),
implement the factory on the target. When neither type should know the other, use an
assembler/mapper in the application layer.

**Java example — target owns the conversion:**

```java
// Domain value object
public record Money(long cents, Currency currency) { }

// DTO (lives in API/infrastructure layer)
public record MoneyDto(long cents, String currencyCode) {

    // Converter Constructor Method: DTO knows how to build itself from domain
    public static MoneyDto from(Money money) {
        return new MoneyDto(money.cents(), money.currency().getCode());
    }
}

// Domain factory: domain object builds from DTO (incoming direction)
public record Money(long cents, Currency currency) {

    public static Money from(MoneyDto dto) {
        return new Money(dto.cents(), Currency.of(dto.currencyCode()));
    }
}
```

**Kotlin example:**

```kotlin
// Domain
data class Money(val cents: Long, val currency: Currency)

// DTO with converter constructor
data class MoneyDto(val cents: Long, val currencyCode: String) {
    companion object {
        fun from(money: Money) = MoneyDto(money.cents, money.currency.code)
    }
}

// Domain factory accepting DTO (incoming conversion)
fun Money.Companion.from(dto: MoneyDto) =
    Money(dto.cents, Currency.of(dto.currencyCode))
```

**Rule:** The type that needs the other type's data pays the coupling cost.
For clean architecture, use an assembler class in the application layer when
neither domain nor infrastructure should know the other.

### SBPP-BEH-06:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* The API layer creates domain objects using `DomainType.from(dto)` at the boundary.
*Show:* `Money.from(moneyDto)` converts an incoming API DTO to a domain value object at
the service layer entry point, before any domain logic runs.

**U.Episteme (design reasoning):**
*Tell:* Placing the conversion factory on the type being constructed makes the dependency direction explicit.
*Show:* `MoneyDto.from(money)` means MoneyDto depends on Money — correct for outbound DTO creation
in the API layer.

### SBPP-BEH-06:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Cross-type conversion in layered architecture**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `Domain.from(Dto)` couples domain to DTO, violating Clean Architecture | Use assembler/mapper in application layer; keep domain free of DTO knowledge |
| **Arch** | Two `from()` methods (one on domain, one on DTO) can confuse which is canonical | Document the canonical conversion direction; use one authoritative mapper |
| **Onto/Epist** | "Converter Constructor" conflates construction with conversion | Keep the distinction clear: construction sets initial state, conversion translates representation |
| **Prag** | MapStruct generates conversion code from annotations; manual factories are redundant for simple types | Use this pattern for domain-critical conversions; use MapStruct for DTO mass-conversion |
| **Did** | Developers may place `from(Dto)` on domain entity without considering coupling | Make coupling explicit via code review guidelines and architecture tests (ArchUnit) |

### SBPP-BEH-06:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH06-1** | Converter Constructor Methods SHALL be named `from(SourceType source)` to signal the conversion direction. | Consistent, discoverable naming |
| **CC-BEH06-2** | Domain objects SHOULD NOT contain `from(InfrastructureDto)` methods; these SHALL live in the application layer. | Preserves domain isolation |
| **CC-BEH06-3** | Conversion MUST validate the source data and throw domain exceptions for invalid inputs. | Maintains invariants at the boundary |

### SBPP-BEH-06:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Bidirectional Cross-Layer Coupling**
Both `Money.from(MoneyDto)` and `MoneyDto.from(Money)` exist, creating a circular dependency.
Fix: Use a dedicated `MoneyAssembler` in the application layer that knows both types.

**Anti-pattern 2: No Validation in Converter Constructor**
`Money.from(dto)` trusts that `dto.currencyCode` is always valid.
Fix: Always validate external data at the boundary: `Currency.of(dto.currencyCode)` must throw
a meaningful exception if the code is unknown.

### SBPP-BEH-06:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Clear single location for cross-type conversion | Coupling between types — mitigated by layer discipline |
| Conversion path is visible in the target type's API | Two `from()` methods for bidirectional conversion — use assembler instead |
| Validates external data at system boundary | — |

### SBPP-BEH-06:10 - Rationale

Beck's pattern addresses the tension between conversion-on-source and construction-on-target.
In a layered Java/Kotlin microservice, the right answer depends on the direction of dependency.
The pattern is adopted with the modern constraint that domain objects should not depend on
infrastructure representations — a principle enforced via architecture tests.

### SBPP-BEH-06:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Domain-Driven Design (Vernon, 2016):** Assemblers translate between domain objects and DTOs
in the application layer. Converter constructors on domain objects violate this. *Adapt:
use assembler for cross-layer; `from()` factory for intra-layer conversion.*

**Kotlin extension functions (JetBrains, post-2016):** `fun Money.Companion.from(dto: MoneyDto)`
allows adding the factory without modifying the domain class, resolving the coupling concern. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Implementing DDD (Vernon, 2016) | Assembler pattern for cross-layer | **Adapt** |
| Kotlin companion extension (post-2016) | Decoupled factory addition | **Adopt** |
| ArchUnit (2019+) | Architecture tests enforce no domain→DTO dependency | **Adopt** |

### SBPP-BEH-06:12 - Relations

* **Paired with:** SBPP-BEH-05 (Converter Method — complementary direction)
* **Constrains:** Dependency direction between architectural layers
* **Relates to:** SBPP-BEH-02 (Constructor Method — specialized factory for conversion)
* **Implemented by:** Application-layer assembler classes

### SBPP-BEH-06:End
