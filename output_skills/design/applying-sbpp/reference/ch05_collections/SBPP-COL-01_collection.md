## SBPP-COL-01 - Collection

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-01:1 - Problem frame

Every Java/Kotlin service manages one-to-many relationships: an order has line items,
a policy has coverages, a portfolio has positions. The choice of which collection type
to use is a recurring decision that affects performance, correctness, and readability.

### SBPP-COL-01:2 - Problem

How do you represent a one-to-many relationship between objects, choosing the right
collection abstraction so that the usage intent is clear and the implementation can change?

### SBPP-COL-01:3 - Forces

| Force | Tension |
|-------|---------|
| **Abstraction** | Program to the collection interface ↔ concrete type needed for construction |
| **Intent** | `List` implies order; `Set` implies uniqueness; `Map` implies keying ↔ wrong choice misleads readers |
| **Immutability** | Immutable collections prevent accidental mutation ↔ construction requires mutability |

### SBPP-COL-01:4 - Solution — Declare fields and parameters as the most abstract collection interface; construct with specific types

Use the most abstract interface that expresses the semantic requirement at field and
parameter declaration sites. Construct with the appropriate concrete type. Prefer immutable
views where possible.

**Java — interface-typed fields, concrete construction:**

```java
public final class InsurancePolicy {
    private final List<Coverage> coverages;      // List: order matters, duplicates allowed
    private final Set<Tag> tags;                 // Set: unique tags
    private final Map<RiskCode, RiskFactor> risks; // Map: keyed by risk code

    public InsurancePolicy(List<Coverage> coverages, Set<Tag> tags) {
        this.coverages = List.copyOf(coverages);   // immutable defensive copy
        this.tags = Set.copyOf(tags);
        this.risks = Map.of();
    }

    public List<Coverage> coverages() { return coverages; } // returns immutable view
}
```

**Kotlin — preferred immutable collections:**

```kotlin
data class InsurancePolicy(
    val coverages: List<Coverage>,          // read-only List
    val tags: Set<Tag>,                     // read-only Set
    val risks: Map<RiskCode, RiskFactor>    // read-only Map
)

// Construction — Kotlin provides read-only builders
val policy = InsurancePolicy(
    coverages = listOf(coverage1, coverage2),
    tags = setOf(Tag.HOME, Tag.STANDARD),
    risks = mapOf(RiskCode.FIRE to fireFactor)
)
```

**Choosing the right interface:**

| Semantic need | Java interface | Kotlin type | Use when |
|--------------|----------------|-------------|----------|
| Ordered, allows duplicates | `List<E>` | `List<E>` | Order matters or duplicates valid |
| Unique elements | `Set<E>` | `Set<E>` | Membership without duplicates |
| Key→value mapping | `Map<K,V>` | `Map<K,V>` | Lookup by key |
| Ordered unique | `SortedSet<E>` | `SortedSet<E>` | Sorted unique set |
| Fixed-size | `E[]` or `List.of()` | `Array<E>` / `listOf()` | Size known at creation |

### SBPP-COL-01:5 - Archetypal Grounding

**U.System:** `List<Coverage> coverages` — the interface declares "order matters; duplicates allowed";
switching `ArrayList` to `LinkedList` requires no API change.

**U.Episteme:** Choosing `Set<Tag>` instead of `List<Tag>` communicates "tags are unique" to every
reader without a comment; the type itself is the documentation.

### SBPP-COL-01:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin collection type selection**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Collection type choice is rarely reviewed; wrong types silently cause bugs | Add collection type to code-review checklist for new fields |
| **Arch** | Java's mutable-by-default collections require defensive copying at boundaries | Use `List.copyOf()`, `Set.copyOf()`; use Kotlin read-only types |
| **Onto/Epist** | `List` allows duplicates but business may not; semantics not enforced by type | Use `Set` when uniqueness is a business rule; document the constraint |
| **Prag** | Kotlin separates read-only and mutable collection types; Java does not | In Java, always copy at boundaries; in Kotlin, prefer read-only types |
| **Did** | New developers default to `ArrayList` for everything | Teach semantic collection choice: List=order, Set=uniqueness, Map=keying |

### SBPP-COL-01:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL01-1** | Fields and method parameters SHALL be declared as the most abstract collection interface (`List`, `Set`, `Map`). | Decouples from concrete implementation |
| **CC-COL01-2** | Collection fields exposed from domain objects SHALL be immutable or return immutable views. | Prevents external mutation |
| **CC-COL01-3** | Collection type selection SHOULD reflect business semantics: `Set` for uniqueness, `List` for order. | Self-documenting field declarations |

### SBPP-COL-01:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Concrete collection type in API**
`public ArrayList<Policy> getPolicies()` — callers become coupled to `ArrayList`.
Fix: `public List<Policy> getPolicies()`.

**Anti-pattern 2: Mutable collection leaked from domain object**
`return this.coverages;` where `coverages` is `ArrayList`. Fix: `return List.copyOf(coverages)` (Java) or declare as `val coverages: List<Coverage>` (Kotlin).

### SBPP-COL-01:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Implementation can change without API change | Defensive copies add allocation overhead — accepted for domain boundaries |
| Type communicates semantic intent | — |
| Immutable collections prevent mutation bugs | — |

### SBPP-COL-01:10 - Rationale

Beck's Collection pattern establishes the "right collection for the job" principle. In Java/Kotlin
this maps directly to interface-typed declarations and immutable-by-preference construction.
Kotlin's distinction between read-only (`List`) and mutable (`MutableList`) makes immutability
the ergonomic default — a major improvement over Java.

### SBPP-COL-01:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 64 ("Refer to objects by their interfaces") applied to collections.
Items 17–18 (minimize mutability, favour composition). *Adopt.*

**Kotlin Collection hierarchy (JetBrains, post-2016):** Kotlin separates `Collection`/`List`/`Set`/`Map` (read-only)
from `MutableCollection`/`MutableList` etc. (mutable). *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Items 64, 17-18 | **Adopt** |
| Kotlin read-only collection types (post-2016) | Immutable-first design | **Adopt** |
| Java 9+ `List.of`, `Set.of`, `Map.of` (JEP 269) | Immutable factory methods | **Adopt** |

### SBPP-COL-01:12 - Relations

* **Specialised by:** SBPP-COL-02 through SBPP-COL-11 (specific collection types)
* **Constrains:** All collection field declarations in domain objects
* **Relates to:** SBPP-COL-05 (Equality Method — required for Set/Map keys)
* **Relates to:** SBPP-COL-06 (Hashing Method — required for hash-based collections)

### SBPP-COL-01:End
