## SBPP-COL-14 - Concatenation

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-14:1 - Problem frame

Combining two or more collections into one is a routine operation. Using `addAll()` in a loop
or `+` concatenation with many collections creates intermediate copies. Java streams and
Kotlin's `plus` / `flatMap` provide more expressive and efficient concatenation.

### SBPP-COL-14:2 - Problem

How do you combine multiple collections into one without unnecessary copies or verbose imperative code?

### SBPP-COL-14:3 - Forces

| Force | Tension |
|-------|---------|
| **Simplicity** | `list1 + list2` is readable ↔ creates a copy |
| **Performance** | Stream concatenation defers materialisation ↔ slightly more complex |
| **Immutability** | Concatenation should produce a new list, not modify existing | |

### SBPP-COL-14:4 - Solution — Use Stream/flatMap for concatenation; Kotlin `+` for simple cases

**Java:**

```java
// ✅ Two-collection concat via Stream
List<Policy> all = Stream.concat(activePolicies.stream(), expiredPolicies.stream())
    .collect(toList());

// ✅ Multiple collections via flatMap
List<Coverage> allCoverages = Stream.of(fireCoverages, theftCoverages, liabilityCoverages)
    .flatMap(Collection::stream)
    .collect(toList());

// ✅ Collect from nested structure
List<Coverage> policyCoverages = policies.stream()
    .flatMap(p -> p.getCoverages().stream())
    .collect(toList());
```

**Kotlin:**

```kotlin
// ✅ Simple concat with + (creates new list)
val all: List<Policy> = activePolicies + expiredPolicies

// ✅ Multiple via flatMap
val allCoverages: List<Coverage> = listOf(fireCoverages, theftCoverages).flatten()

// ✅ Nested flatMap
val policyCoverages: List<Coverage> = policies.flatMap { it.coverages }

// ✅ buildList for conditional concatenation
val combined = buildList {
    addAll(activePolicies)
    if (includeExpired) addAll(expiredPolicies)
}
```

### SBPP-COL-14:5 - Archetypal Grounding

**U.System:** `policies.flatMap { it.coverages }` — collects all coverages from all policies in one line.
**U.Episteme:** `Stream.concat()` defers copying until `collect()` — combining 10 streams does not create 9 intermediate lists.

### SBPP-COL-14:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `list1 + list2 + list3` in Kotlin creates two intermediate lists | Use `buildList { addAll ... }` for many collections |
| **Arch** | `Stream.concat` is lazy; result only materialised at `collect()` | Prefer for large data; use `+` for small |
| **Onto/Epist** | Order of concatenation matters — document it | Concatenation order is semantic; name the collections clearly |
| **Prag** | Kotlin `flatten()` is more readable than nested `flatMap { it }` | Use `flatten()` on `List<List<T>>` |
| **Did** | Java's `addAll()` loop is a common beginner pattern | Teach `Stream.concat` and `flatMap` as the modern idiom |

### SBPP-COL-14:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL14-1** | Collection concatenation SHALL use `Stream.concat()` / `flatMap()` (Java) or `+` / `flatten()` / `flatMap` (Kotlin). | Avoids imperative loops |
| **CC-COL14-2** | Concatenation of many (>3) collections SHOULD use `flatMap` to avoid intermediate copies. | Performance |

### SBPP-COL-14:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `List<T> result = new ArrayList<>(list1); result.addAll(list2);` — verbose; fix with `Stream.concat()`.
**Anti-pattern 2:** `list1 + list2 + list3 + ...` in Kotlin — creates O(n) intermediate lists; fix with `buildList { addAll ... }`.

### SBPP-COL-14:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Expressive one-line concatenation | `Stream.concat` is slightly more verbose than `+` |
| `flatMap` eliminates nested loops for collection extraction | — |

### SBPP-COL-14:10 - Rationale

Concatenation is a universal collection operation. Java streams and Kotlin's collection
API provide clean, lazy concatenation that avoids the intermediate copies of simple `+`.

### SBPP-COL-14:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `Stream.concat` / `flatMap` (post-2014):** Standard concatenation idioms. *Adopt.*
**Kotlin `flatten` / `flatMap` (post-2016):** Idiomatic flattening. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream API | `concat`, `flatMap` | **Adopt** |
| Kotlin stdlib (post-2016) | `flatten`, `flatMap`, `+` | **Adopt** |

### SBPP-COL-14:12 - Relations

* **Part of:** Collection Protocol patterns
* **Relates to:** SBPP-COL-28 (Concatenating Stream — stream-based approach)

### SBPP-COL-14:End
