## SBPP-COL-06 - Hashing Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-06:1 - Problem frame

Whenever a class overrides `equals()`, Java's contract requires that `hashCode()` must
also be overridden consistently. Objects used as keys in `HashMap` or elements in `HashSet`
without a correct `hashCode()` will silently fail to be found or stored correctly.

### SBPP-COL-06:2 - Problem

How do you implement `hashCode()` correctly so that objects work reliably in hash-based
collections (`HashSet`, `HashMap`, `LinkedHashSet`, `LinkedHashMap`)?

### SBPP-COL-06:3 - Forces

| Force | Tension |
|-------|---------|
| **Contract** | Equal objects MUST have equal hash codes ↔ hash code computation can be expensive |
| **Distribution** | Good distribution reduces hash collisions ↔ overly complex hash function is costly |
| **Stability** | Hash code must be stable for the lifetime of the object in a collection ↔ mutable fields would change it |

### SBPP-COL-06:4 - Solution — Use `Objects.hash()` or record/data class auto-generation; hash only immutable fields

Use `Objects.hash(field1, field2, ...)` in Java or let records and Kotlin data classes
auto-generate `hashCode()`. Only include the same fields used in `equals()`.

**Java — manual hashCode using Objects.hash():**

```java
public final class PolicyId {
    private final String value;

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof PolicyId other)) return false;
        return Objects.equals(value, other.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);   // ✅ same fields as equals; null-safe
    }
}
```

**Java — record (auto-generated, preferred):**

```java
// hashCode() auto-generated from all components
public record Money(long cents, Currency currency) {}
// new Money(100, USD).hashCode() == new Money(100, USD).hashCode() ✓
```

**Kotlin — data class (auto-generated):**

```kotlin
data class Money(val cents: Long, val currency: Currency)
// hashCode auto-generated from primary constructor properties
```

**Multi-field hashCode guidelines:**

```java
// ✅ Correct: hash all fields used in equals
@Override
public int hashCode() {
    return Objects.hash(firstName, lastName, dateOfBirth);
}

// ❌ Avoid: hashing mutable fields
@Override
public int hashCode() {
    return Objects.hash(mutableStatus);  // status can change — breaks HashSet
}

// ❌ Avoid: constant hash code (legal but destroys performance)
@Override
public int hashCode() { return 42; }  // O(n) HashSet operations
```

### SBPP-COL-06:5 - Archetypal Grounding

**U.System:** `Objects.hash(cents, currency)` produces a hash consistent with `equals()`
on the same fields — required for `HashMap<Money, Discount>` to work.

**U.Episteme:** The contract "equal objects must have equal hashCode" is an invariant,
not a convention. Violating it produces unreproducible bugs.

### SBPP-COL-06:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **hashCode in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `hashCode`-only bug (no `equals` change) is hard to detect | Always implement both; use records/data classes to eliminate manual risk |
| **Arch** | Poor hash distribution degrades HashMap performance to O(n) | Use `Objects.hash()` which uses `Arrays.hashCode` internally — good distribution |
| **Onto/Epist** | Including all fields in hashCode produces a unique, well-distributed code | Only include the same fields as `equals`; don't add "extra" fields for distribution |
| **Prag** | Java records auto-generate both `equals` and `hashCode` consistently | Use records for value objects |
| **Did** | New developers may implement `hashCode` returning a constant | Explain the performance impact; show the O(n) degeneration |

### SBPP-COL-06:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL06-1** | Every class that overrides `equals` MUST also override `hashCode`. | Maintains contract |
| **CC-COL06-2** | `hashCode` MUST use the same fields as `equals`, no more, no less. | Ensures contract: equal objects → equal hash |
| **CC-COL06-3** | `hashCode` MUST NOT depend on mutable fields that can change while the object is in a collection. | Prevents lost-in-collection bugs |
| **CC-COL06-4** | Java value objects SHOULD use records; Kotlin value objects SHOULD use data classes (auto-generate both). | Eliminates manual error risk |

### SBPP-COL-06:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Mutable field in hashCode**
An order changes status; if `status` is in `hashCode`, it "disappears" from a `HashSet`.
Fix: only hash immutable/identity fields.

**Anti-pattern 2: Constant hashCode**
`return 1;` is technically legal but degrades all HashSet/HashMap operations to O(n).
Fix: use `Objects.hash()`.

### SBPP-COL-06:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Hash-based collections (`HashSet`, `HashMap`) work correctly | Requires discipline to keep equals/hashCode in sync |
| `Objects.hash()` provides good distribution | — |
| Records/data classes eliminate the synchronization risk | — |

### SBPP-COL-06:10 - Rationale

Beck's Hashing Method is the mandatory companion to Equality Method. In modern Java/Kotlin,
records and data classes make this a non-issue for value objects. The manual implementation
using `Objects.hash()` is the fallback for non-record classes. The contract "equal objects
must have equal hash codes" is inviolable.

### SBPP-COL-06:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 11 ("Always override hashCode when you override equals").
The definitive guidance. *Adopt.*

**Java 16+ records (JEP 395):** Auto-generate consistent `equals`/`hashCode`. *Adopt.*

**Kotlin data class (post-2016):** Same auto-generation. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. Item 11 (Bloch, 2018) | Mandatory companion to equals | **Adopt** |
| Java 16+ records | Auto-generation | **Adopt** |
| Kotlin data class (post-2016) | Auto-generation | **Adopt** |

### SBPP-COL-06:12 - Relations

* **Required by:** SBPP-COL-04 (Set), SBPP-COL-07 (Dictionary/Map keys)
* **Mandated alongside:** SBPP-COL-05 (Equality Method — must always be implemented together)
* **Consistency with:** SBPP-BEH-08 (Comparing Method — compareTo must be consistent with equals and thus hashCode)

### SBPP-COL-06:End
