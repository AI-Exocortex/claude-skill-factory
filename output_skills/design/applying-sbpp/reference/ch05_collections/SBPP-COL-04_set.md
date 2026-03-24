## SBPP-COL-04 - Set

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-04:1 - Problem frame

When a collection must contain no duplicates — unique customer IDs, active feature flags,
distinct risk codes — using a `List` silently allows duplicates and requires manual
deduplication logic. The `Set` type encodes the uniqueness constraint in the type itself.

### SBPP-COL-04:2 - Problem

How do you represent a collection whose elements must be unique, without writing manual
deduplication logic at every insertion site?

### SBPP-COL-04:3 - Forces

| Force | Tension |
|-------|---------|
| **Uniqueness** | Set enforces uniqueness automatically ↔ requires `equals`/`hashCode` to be correct |
| **Order** | `HashSet` has no guaranteed order ↔ `LinkedHashSet` preserves insertion order ↔ `TreeSet` sorts |
| **Performance** | `HashSet` O(1) contains/add ↔ `TreeSet` O(log n) but sorted |

### SBPP-COL-04:4 - Solution — Use `Set` when uniqueness is a business constraint; choose the right Set implementation

Declare fields as `Set<E>`. Construct with the implementation that matches the ordering need.
Objects used as Set elements MUST implement `equals()` and `hashCode()` correctly (SBPP-COL-05, COL-06).

**Java example:**

```java
public final class PolicyPortfolio {
    // ✅ Set encodes the business rule: no duplicate policies
    private final Set<PolicyId> activePolicyIds;

    public PolicyPortfolio(Collection<PolicyId> ids) {
        this.activePolicyIds = Set.copyOf(ids);   // immutable set; throws on duplicates in Java 10+
    }

    public boolean contains(PolicyId id) { return activePolicyIds.contains(id); }

    // Choosing the right Set:
    // HashSet      — fastest, no order (use for most cases)
    // LinkedHashSet — insertion-order iteration
    // TreeSet      — sorted natural order
    // Set.of()     — immutable, no duplicates, no null (Java 9+)
}

// Deduplication idiom
List<String> withDuplicates = List.of("A", "B", "A", "C");
Set<String> unique = new LinkedHashSet<>(withDuplicates);   // preserves order, removes duplicates
```

**Kotlin example:**

```kotlin
data class PolicyPortfolio(
    val activePolicyIds: Set<PolicyId>  // read-only Set in Kotlin
)

// Kotlin set builders
val ids = setOf(PolicyId("P1"), PolicyId("P2"))            // immutable
val mutableIds = mutableSetOf(PolicyId("P1"))               // mutable during construction

// Deduplication
val withDups = listOf("A", "B", "A", "C")
val unique: Set<String> = withDups.toSet()                  // LinkedHashSet internally
val ordered: Set<String> = withDups.toSortedSet()           // TreeSet
```

**Set implementation selector:**

| Need | Java | Kotlin |
|------|------|--------|
| Fast, order unimportant | `HashSet` / `Set.of()` | `hashSetOf()` / `setOf()` |
| Preserve insertion order | `LinkedHashSet` | `linkedSetOf()` |
| Sorted natural order | `TreeSet` | `sortedSetOf()` |
| Immutable | `Set.of()` / `Set.copyOf()` | `setOf()` |

### SBPP-COL-04:5 - Archetypal Grounding

**U.System:** `Set<PolicyId> activePolicyIds` — the type itself documents "no duplicate active policies";
no comment or guard clause needed.

**U.Episteme:** `Set<String> processedEventIds` in an idempotency guard — duplicate events are
silently ignored because the Set absorbs them.

### SBPP-COL-04:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Set usage in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Set silently discards duplicates — business may need to know about them | Log or throw when a duplicate insertion represents a business error |
| **Arch** | `HashSet` equality depends on `hashCode`; broken hashCode causes silent failures | Always implement `equals`+`hashCode` together; use records or data classes |
| **Onto/Epist** | `Set.of()` in Java throws `NullPointerException` for null elements | Document null handling; use `EnumSet` for enum-typed sets |
| **Prag** | Kotlin `setOf()` returns a read-only `LinkedHashSet` — insertion order is preserved by default | Leverage this; only use `sortedSetOf()` when sorted iteration is needed |
| **Did** | New developers forget to implement `hashCode` when using `HashSet` | Use records (Java) or data classes (Kotlin) which auto-generate both |

### SBPP-COL-04:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL04-1** | Objects used as `Set` elements SHALL correctly implement `equals()` and `hashCode()`. | Correct set semantics |
| **CC-COL04-2** | `Set` SHALL be used wherever the uniqueness of elements is a business constraint. | Encodes constraint in type |
| **CC-COL04-3** | Set fields exposed from domain objects SHOULD be immutable (`Set.copyOf()` / Kotlin read-only). | Mutation safety |

### SBPP-COL-04:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Manual deduplication with List**
```java
if (!list.contains(item)) list.add(item);
```
Fix: Use a `Set` — the type enforces uniqueness automatically and is O(1) vs O(n).

**Anti-pattern 2: Set without hashCode**
Custom class in `HashSet` without `hashCode()`. Fix: use Java records or Kotlin data classes.

### SBPP-COL-04:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Uniqueness enforced structurally, not procedurally | Requires correct `equals`/`hashCode` — use records/data classes |
| O(1) `contains()` vs O(n) for `List` | `HashSet` has no guaranteed iteration order — use `LinkedHashSet` if needed |
| `Set.of()` provides an immutable set with zero overhead | `Set.of()` throws on null and on duplicates |

### SBPP-COL-04:10 - Rationale

Beck's Set pattern is directly applicable: use `Set` when elements must be unique, not `List`
with manual deduplication. Java/Kotlin provide multiple Set implementations covering every
order/performance trade-off. The critical prerequisite — correct `equals`/`hashCode` — is
auto-provided by Java records and Kotlin data classes.

### SBPP-COL-04:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Items 10-11 on `equals`/`hashCode` contracts are
the prerequisite for correct Set usage. Item 64: use interface types. *Adopt.*

**Java 16+ records (JEP 395):** Auto-generate `equals`/`hashCode` — making set-element creation
safer. *Adopt.*

**Kotlin data class (post-2016):** Auto-generates `equals`/`hashCode` from constructor properties. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | equals/hashCode contract | **Adopt** |
| Java 16+ records | Auto-generated equals/hashCode | **Adopt** |
| Kotlin data class (post-2016) | Auto-generated equals/hashCode | **Adopt** |

### SBPP-COL-04:12 - Relations

* **Specialises:** SBPP-COL-01 (Collection — unique-element variant)
* **Requires:** SBPP-COL-05 (Equality Method), SBPP-COL-06 (Hashing Method)
* **Used by:** SBPP-COL-21 (Duplicate Removing Set)
* **Relates to:** SBPP-COL-07 (Dictionary — Map keys have Set semantics)

### SBPP-COL-04:End
