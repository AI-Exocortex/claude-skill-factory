## SBPP-COL-02 - OrderedCollection

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-02:1 - Problem frame

When a collection's size is not known at creation time, a dynamically resizing list is
needed. In Java/Kotlin this is the most common collection use case — adding elements to
a growing list during processing or accumulation.

### SBPP-COL-02:2 - Problem

How do you represent a collection whose size varies at runtime, without imposing arbitrary
size limits?

### SBPP-COL-02:3 - Forces

| Force | Tension |
|-------|---------|
| **Flexibility** | No arbitrary size limit ↔ memory grows unboundedly |
| **Performance** | `ArrayList` is O(1) amortised add ↔ `LinkedList` is O(1) add at head/tail |
| **Immutability** | Mutable during construction ↔ immutable after assembly |

### SBPP-COL-02:4 - Solution — Use `ArrayList` during construction; expose as immutable `List`

Build with `ArrayList` (Java) or `mutableListOf()` (Kotlin) when elements are added
incrementally. Expose the result as an immutable `List` when the collection is complete.

**Java example:**

```java
public List<RiskFactor> buildRiskFactors(PolicyRequest request) {
    List<RiskFactor> factors = new ArrayList<>();          // mutable builder
    factors.add(RiskFactor.ageRisk(request.applicantAge()));
    if (request.hasClaimHistory()) factors.add(RiskFactor.PRIOR_CLAIMS);
    if (request.isHighValueProperty()) factors.add(RiskFactor.HIGH_VALUE);
    return List.copyOf(factors);                           // immutable result
}
```

**Kotlin example:**

```kotlin
fun buildRiskFactors(request: PolicyRequest): List<RiskFactor> =
    buildList {
        add(RiskFactor.ageRisk(request.applicantAge))
        if (request.hasClaimHistory) add(RiskFactor.PRIOR_CLAIMS)
        if (request.isHighValueProperty) add(RiskFactor.HIGH_VALUE)
    }  // buildList {} returns read-only List
```

**When to choose ArrayList vs LinkedList:**

| Use case | Recommended |
|----------|-------------|
| Random access by index | `ArrayList` |
| Frequent add/remove at middle | `ArrayList` (usually still faster due to cache) |
| Queue/deque operations (head/tail) | `ArrayDeque` |
| General-purpose dynamic list | `ArrayList` |

### SBPP-COL-02:5 - Archetypal Grounding

**U.System:** `buildList {}` in Kotlin builds a dynamic list without imposing a size limit;
`List.copyOf()` in Java seals it after construction.

**U.Episteme:** "Dynamic size without arbitrary limits" is the semantic contract;
`ArrayList` is the canonical implementation fulfilling it.

### SBPP-COL-02:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Dynamic list use in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `ArrayList` is so common it is used uncritically | Ask: does order matter? Are duplicates allowed? If not, `Set` is better |
| **Arch** | Growing an `ArrayList` causes periodic array copying | Pre-size with `new ArrayList<>(expectedSize)` when size is roughly known |
| **Onto/Epist** | `ArrayList` vs `LinkedList` choice is often cargo-culted | Profile first; `ArrayList` wins for almost all access patterns |
| **Prag** | Kotlin `buildList {}` eliminates the mutable-then-immutable ceremony | Use `buildList` in Kotlin; prefer `List.copyOf()` in Java |
| **Did** | Developers may return the raw `ArrayList` from domain methods | Enforce: domain methods return `List`, never `ArrayList` |

### SBPP-COL-02:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL02-1** | Dynamic lists SHALL be built with `ArrayList` (Java) or `buildList {}` / `mutableListOf()` (Kotlin). | Standard dynamic list |
| **CC-COL02-2** | Lists returned from domain methods SHALL be declared as `List<E>`, not `ArrayList<E>`. | API abstraction |
| **CC-COL02-3** | Lists returned from domain methods SHOULD be immutable (`List.copyOf()` / Kotlin read-only). | Mutation safety |

### SBPP-COL-02:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Returning raw ArrayList**
`public ArrayList<Policy> getPolicies()` — Fix: return `List<Policy>`.

**Anti-pattern 2: Using LinkedList for random access**
`LinkedList` has O(n) random access. Fix: use `ArrayList` unless profiling shows otherwise.

### SBPP-COL-02:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| No arbitrary size limits | Memory grows with content — use stream processing for very large sets |
| O(1) amortised add | Resize copies — pre-size when expected capacity is known |

### SBPP-COL-02:10 - Rationale

`ArrayList` is the Java/Kotlin equivalent of Smalltalk's `OrderedCollection`. It is
the correct default for any dynamic list. Kotlin's `buildList {}` improves on Java
by producing a read-only list from the outset.

### SBPP-COL-02:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 29 ("Favour generic types") and Items 17-18
on immutability. `ArrayList` is the standard JDK dynamic list. *Adopt.*

**Kotlin stdlib `buildList` (post-2019):** The idiomatic Kotlin dynamic-list builder. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Standard JDK collection usage | **Adopt** |
| Kotlin `buildList` (post-2019) | Idiomatic immutable list builder | **Adopt** |

### SBPP-COL-02:12 - Relations

* **Specialises:** SBPP-COL-01 (Collection — ordered, variable-size variant)
* **Used by:** SBPP-COL-31 (Collecting Parameter — accumulator is an OrderedCollection)
* **Relates to:** SBPP-COL-23 (Stack), SBPP-COL-24 (Queue — built on OrderedCollection)

### SBPP-COL-02:End
