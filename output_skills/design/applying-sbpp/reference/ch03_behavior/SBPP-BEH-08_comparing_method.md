## SBPP-BEH-08 - Comparing Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-08:1 - Problem frame

When domain objects in Java/Kotlin need to be sorted, compared for ordering, or used in
priority queues, the comparison logic must live somewhere. The choice between implementing
`Comparable`, providing a `Comparator`, or neither has long-term implications for how
the type is used across the codebase.

### SBPP-BEH-08:2 - Problem

How do you provide natural ordering for an object when there is one clear, dominant way
to compare instances, so that callers can sort and compare without boilerplate?

### SBPP-BEH-08:3 - Forces

| Force | Tension |
|-------|---------|
| **Natural Ordering** | One dominant comparison simplifies use ↔ multiple valid orderings exist for many types |
| **Contract Consistency** | `compareTo` must be consistent with `equals` ↔ some types have ordering but no meaningful equality |
| **Flexibility** | `Comparable` is built-in ↔ `Comparator` supports multiple orderings without coupling |

### SBPP-BEH-08:4 - Solution — Implement `Comparable` for single natural ordering; use `Comparator` for alternatives

Implement `Comparable<T>` on a class only when one ordering is overwhelmingly natural and
consistent with `equals`. Provide static `Comparator` constants for alternative orderings.

**Java example:**

```java
// Policy has one natural ordering: by premium amount
public final class InsurancePolicy implements Comparable<InsurancePolicy> {
    private final PolicyId id;
    private final Money premium;
    private final LocalDate startDate;

    @Override
    public int compareTo(InsurancePolicy other) {
        return this.premium.compareTo(other.premium);
    }

    // Alternative orderings as named Comparators
    public static final Comparator<InsurancePolicy> BY_START_DATE =
        Comparator.comparing(p -> p.startDate);

    public static final Comparator<InsurancePolicy> BY_ID =
        Comparator.comparing(p -> p.id.value());
}

// Usage
policies.sort(Comparator.naturalOrder());          // by premium
policies.sort(InsurancePolicy.BY_START_DATE);      // by date
policies.stream().min(InsurancePolicy.BY_ID);      // by id
```

**Kotlin example:**

```kotlin
data class InsurancePolicy(
    val id: PolicyId,
    val premium: Money,
    val startDate: LocalDate
) : Comparable<InsurancePolicy> {

    override fun compareTo(other: InsurancePolicy): Int =
        premium.compareTo(other.premium)

    companion object {
        val BY_START_DATE: Comparator<InsurancePolicy> =
            compareBy { it.startDate }
        val BY_ID: Comparator<InsurancePolicy> =
            compareBy { it.id.value }
    }
}

// Usage
policies.sorted()                          // natural order (by premium)
policies.sortedWith(InsurancePolicy.BY_START_DATE)
```

**Rule:** Implement `Comparable` only when the ordering is unambiguous and stable.
If multiple orderings are equally valid, use only `Comparator`s.

### SBPP-BEH-08:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Domain objects with a clear natural ordering implement `Comparable`; all other orderings are `Comparator`s.
*Show:* `policies.sorted()` works out of the box because `InsurancePolicy` implements `Comparable` by premium.

**U.Episteme (design reasoning):**
*Tell:* `compareTo` must be consistent with `equals`; violating this breaks sorted collections.
*Show:* If `a.compareTo(b) == 0` but `!a.equals(b)`, the object cannot be safely used in `TreeSet` or `TreeMap`.

### SBPP-BEH-08:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin object ordering**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `Comparable` forces a single natural order into the class definition permanently | Only implement when the ordering is truly canonical; use Comparators for flexibility |
| **Arch** | Comparing may depend on external context (e.g., currency exchange rates for Money) | Keep `compareTo` context-free; use external `Comparator`s for context-dependent ordering |
| **Onto/Epist** | "Natural order" is often a design assumption that proves wrong | Prefer Comparators for new types; promote to `Comparable` only after domain confirms the ordering |
| **Prag** | Java 8+ `Comparator.comparing()` chains are expressive and don't require `Comparable` | Favour `Comparator` composition for most types; `Comparable` only for primitives/value types |
| **Did** | Developers forget the `compareTo`/`equals` consistency contract | Document and enforce via unit tests |

### SBPP-BEH-08:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH08-1** | Classes implementing `Comparable<T>` SHALL ensure `compareTo` is consistent with `equals`. | Prevents broken sorted-collection behaviour |
| **CC-BEH08-2** | Alternative orderings SHALL be provided as named `static final Comparator<T>` constants. | Enables multiple sort criteria without coupling |
| **CC-BEH08-3** | `compareTo` MUST NOT throw unchecked exceptions for valid instances of the same type. | Ensures robustness in sort operations |

### SBPP-BEH-08:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: compareTo inconsistent with equals**
`a.compareTo(b) == 0` but `a.equals(b) == false`. Fix: implement both together; for Kotlin
`data class`, `equals` is auto-generated — ensure `compareTo` uses the same fields.

**Anti-pattern 2: Mutable comparison field**
The field used in `compareTo` is mutable, causing ordered collections to break.
Fix: use only immutable fields for comparison; document this constraint.

### SBPP-BEH-08:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| `sorted()`, `min()`, `max()` work without explicit comparator | Permanent API commitment — choose natural ordering carefully |
| Named `Comparator` constants serve as vocabulary for sort intents | Multiple orderings require multiple constants |
| Consistent with JDK collections contract | Must maintain `compareTo`/`equals` consistency |

### SBPP-BEH-08:10 - Rationale

Beck's Comparing Method applies directly: implement `compareTo` when there is "one overwhelming
way to order a new object." Java/Kotlin provide `Comparable` as the standard mechanism.
The additional guidance on `Comparator` for alternative orderings extends Beck's original
pattern to the richer Java 8+ comparison API.

### SBPP-BEH-08:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 14 ("Consider implementing Comparable").
Bloch's detailed guidance on `compareTo`/`equals` consistency is directly applicable. *Adopt.*

**Java 8+ Comparator API (Oracle, 2014+):** `Comparator.comparing()` chains eliminate the
need to write anonymous comparators; named static constants document orderings clearly. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 14 — `Comparable` guidance | **Adopt** |
| Java 8+ Comparator API | Functional comparator composition | **Adopt** |
| Kotlin `compareBy` / `sortedWith` (post-2016) | Idiomatic Kotlin comparison | **Adopt** |

### SBPP-BEH-08:12 - Relations

* **Specialises:** SBPP-BEH-07 (Query Method — comparison is a specialised query)
* **Constrains:** SBPP-COL-05 (Equality Method — must be consistent)
* **Relates to:** SBPP-COL-08 (SortedCollection — uses this pattern)
* **Constrained by:** `compareTo` / `equals` / `hashCode` contract triangle

### SBPP-BEH-08:End
