## SBPP-COL-05 - Equality Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-05:1 - Problem frame

Java's `Object.equals()` defaults to identity (reference equality). For value objects —
`Money`, `PolicyId`, `Address`, `Coordinate` — two instances with the same data should
be equal. Without overriding `equals()`, `Set`, `Map`, and any code that tests equality
will behave incorrectly for these types.

### SBPP-COL-05:2 - Problem

How do you define equality for a new class so that instances with the same meaningful
data are considered equal, enabling correct use in collections and conditionals?

### SBPP-COL-05:3 - Forces

| Force | Tension |
|-------|---------|
| **Contract** | `equals` must be reflexive, symmetric, transitive, consistent, and null-safe ↔ subtle to implement correctly |
| **Consistency** | `equals` and `hashCode` MUST be consistent ↔ implementing one without the other causes Set/Map failures |
| **Maintenance** | Manually written `equals` must be updated when fields change ↔ auto-generated methods handle this |

### SBPP-COL-05:4 - Solution — Use records (Java) or data classes (Kotlin); write manually only when needed

For value objects, use Java records or Kotlin data classes — they auto-generate correct
`equals()` and `hashCode()`. Write manually only for entities (where identity matters)
or when business equality differs from structural equality.

**Java — record (auto-generated equals):**

```java
// ✅ Record auto-generates correct equals() and hashCode()
public record Money(long cents, Currency currency) {}

// ✅ equals() works correctly
Money a = new Money(100, Currency.USD);
Money b = new Money(100, Currency.USD);
assert a.equals(b);  // true — same data
assert !a.equals(new Money(200, Currency.USD));  // false

// ✅ Works in Set and Map
Set<Money> prices = Set.of(new Money(100, USD), new Money(200, USD));
```

**Java — manual equals for non-record class:**

```java
public final class PolicyId {
    private final String value;

    public PolicyId(String value) { this.value = Objects.requireNonNull(value); }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof PolicyId other)) return false;
        return Objects.equals(value, other.value);
    }

    @Override
    public int hashCode() { return Objects.hash(value); }
}
```

**Kotlin — data class (auto-generated equals):**

```kotlin
// ✅ data class auto-generates equals(), hashCode(), toString(), copy()
data class Money(val cents: Long, val currency: Currency)
data class PolicyId(val value: String)

val a = Money(100, Currency.USD)
val b = Money(100, Currency.USD)
println(a == b)  // true
```

**Entity equality (identity, not structure):**

```java
// Entity: two Orders with the same ID are the same, regardless of other fields
public class Order {
    private final OrderId id;
    // ...
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Order other)) return false;
        return id.equals(other.id);  // identity via business key
    }
    @Override public int hashCode() { return id.hashCode(); }
}
```

### SBPP-COL-05:5 - Archetypal Grounding

**U.System:** `Money(100, USD).equals(Money(100, USD))` must be `true` for `Set<Money>` deduplication to work.
**U.Episteme:** The equals contract (reflexive, symmetric, transitive, consistent, null-safe) is a mathematical specification that the implementation must satisfy — not a preference.

### SBPP-COL-05:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Object equality in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Broken `equals` causes silent, hard-to-diagnose Set/Map bugs | Use records/data classes; test equality explicitly |
| **Arch** | Adding a field to a record/data class changes equality semantics automatically | Review field additions to value objects; ensure all fields should participate in equality |
| **Onto/Epist** | Value objects use structural equality; entities use identity equality | Establish team convention: records/data classes for values; hand-written equals for entities |
| **Prag** | Lombok `@EqualsAndHashCode` is an alternative for Java non-records | Acceptable; prefer records for new code |
| **Did** | The `equals`/`hashCode` contract is subtle — common errors include missing null check, missing type check | Use IntelliJ's "Generate" or records/data classes; never write equals from scratch without tests |

### SBPP-COL-05:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL05-1** | Value objects SHALL use Java records or Kotlin data classes, which auto-generate correct `equals`/`hashCode`. | Prevents contract violations |
| **CC-COL05-2** | Entity equality SHALL be based on a stable business key (ID), not all fields. | Correct entity identity semantics |
| **CC-COL05-3** | Any class that overrides `equals` MUST also override `hashCode`. | Maintains equals/hashCode contract |
| **CC-COL05-4** | `equals` MUST handle `null` safely and return `false` for `null` argument. | Null-safety contract |

### SBPP-COL-05:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: equals without hashCode**
`@Override public boolean equals(Object o) { ... }` — without `hashCode`, Set/Map breaks.
Fix: always implement both together; use records/data classes to avoid the issue.

**Anti-pattern 2: Mutable field in equals**
Equality based on a field that changes over time causes objects to "disappear" from HashSets.
Fix: only use immutable fields in `equals`/`hashCode`.

### SBPP-COL-05:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| `Set`/`Map` and equality checks work correctly | Must be consistent with `hashCode` |
| Structural equality enables value-object idioms | New fields auto-included in record equality — review on every field addition |

### SBPP-COL-05:10 - Rationale

Beck's Equality Method is one of the most critical patterns in Java/Kotlin. Java records
and Kotlin data classes resolve the implementation problem — but the design decision
(which fields define equality) remains a developer responsibility. Entity vs value object
is the key architectural distinction.

### SBPP-COL-05:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Items 10-11 are the definitive Java guidance on `equals`/`hashCode`.
*Adopt: implement per contract; use records for value objects.*

**Java 16+ records (JEP 395):** Auto-generate correct `equals`/`hashCode` for all record components. *Adopt.*

**Kotlin data class (JetBrains, post-2016):** Same auto-generation. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. Items 10-11 (Bloch, 2018) | Definitive `equals` contract | **Adopt** |
| Java 16+ records | Auto-generated equals | **Adopt** |
| Kotlin data class (post-2016) | Auto-generated equals | **Adopt** |

### SBPP-COL-05:12 - Relations

* **Required by:** SBPP-COL-04 (Set), SBPP-COL-06 (Hashing Method), SBPP-COL-07 (Dictionary keys)
* **Constrained by:** `equals`/`hashCode`/`compareTo` consistency triangle
* **Relates to:** SBPP-BEH-08 (Comparing Method — compareTo must be consistent with equals)

### SBPP-COL-05:End
