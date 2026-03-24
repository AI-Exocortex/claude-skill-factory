## SBPP-COL-21 - Duplicate Removing Set

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-21:1 - Problem frame

When a collection accumulates elements from multiple sources and duplicates must be
removed, the manual "check-then-add" loop is verbose and O(n²). Converting to a `Set`
and back is the canonical deduplication idiom in Java/Kotlin.

### SBPP-COL-21:2 - Problem

How do you remove duplicate elements from a collection efficiently and without manual loop logic?

### SBPP-COL-21:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | Set conversion is O(n) ↔ manual `contains` check is O(n²) for List |
| **Order** | `HashSet` loses order ↔ `LinkedHashSet` preserves insertion order |
| **Equality** | Deduplication uses `equals()`/`hashCode()` — must be correct |

### SBPP-COL-21:4 - Solution — Convert to Set; or use stream `distinct()` / Kotlin `distinct()`

**Java:**

```java
// ✅ Fastest deduplication — O(n), loses order
Set<PolicyId> uniqueIds = new HashSet<>(policyIds);

// ✅ Deduplication preserving insertion order
Set<PolicyId> orderedUnique = new LinkedHashSet<>(policyIds);

// ✅ Stream distinct() — preserves encounter order
List<Policy> noDuplicates = policies.stream()
    .distinct()
    .collect(toList());

// ✅ Deduplicate by attribute using groupingBy
List<Policy> uniqueByHolder = new ArrayList<>(
    policies.stream()
        .collect(Collectors.toMap(
            Policy::getHolderId,
            p -> p,
            (existing, replacement) -> existing  // keep first
        ))
        .values()
);
```

**Kotlin:**

```kotlin
// ✅ toSet() — removes duplicates
val uniqueIds: Set<PolicyId> = policyIds.toSet()

// ✅ distinct() — preserves order, returns List
val noDuplicates: List<Policy> = policies.distinct()

// ✅ distinctBy — deduplicate by attribute
val uniqueByHolder: List<Policy> = policies.distinctBy { it.holderId }
```

### SBPP-COL-21:5 - Archetypal Grounding

**U.System:** `policies.distinctBy { it.holderId }` — keeps one policy per holder ID; one expression.
**U.Episteme:** `Set` is the mathematical model for collections without duplicates; converting to `Set` is the direct application of the model.

### SBPP-COL-21:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Which duplicate to keep? `distinct()` keeps first in encounter order | Document "first wins" vs "last wins" semantics |
| **Arch** | Deduplication requires correct `equals`/`hashCode` | Use records/data classes |
| **Onto/Epist** | `distinctBy` attribute may not match `equals` — explicit | Use `distinctBy` over `distinct` when deduplication key differs from equality |
| **Prag** | Kotlin `distinctBy` is very expressive for attribute-based deduplication | Use it |
| **Did** | Teach Set conversion as the primary idiom; `distinct()` as the functional alternative | |

### SBPP-COL-21:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL21-1** | Deduplication SHALL use `Set` conversion or `distinct()` / `distinctBy()`, not manual `contains` loop. | O(n) vs O(n²) |
| **CC-COL21-2** | When insertion order must be preserved, `LinkedHashSet` (Java) or `distinct()` (Kotlin) SHALL be used. | Correct order |

### SBPP-COL-21:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `if (!list.contains(item)) list.add(item)` in a loop — O(n²). Fix: `new LinkedHashSet<>(list)`.
**Anti-pattern 2:** Using `distinct()` when `distinctBy` is needed — silently keeps wrong duplicate. Fix: use `distinctBy { attribute }`.

### SBPP-COL-21:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(n) deduplication | Requires correct `equals`/`hashCode` |
| One-liner: `list.toSet()` / `list.distinct()` | — |

### SBPP-COL-21:10 - Rationale

Beck's Duplicate Removing Set idiom maps directly to `Set` conversion in Java/Kotlin.
Kotlin adds `distinctBy` for attribute-based deduplication — more powerful than the original.

### SBPP-COL-21:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `stream().distinct()` (post-2014):** Stream-based deduplication. *Adopt.*
**Kotlin `distinct()` / `distinctBy()` (post-2016):** Idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ `distinct()` | Deduplication | **Adopt** |
| Kotlin `distinctBy` (post-2016) | Attribute deduplication | **Adopt** |

### SBPP-COL-21:12 - Relations

* **Specialises:** SBPP-COL-04 (Set — the semantic foundation)
* **Uses:** SBPP-COL-05 (Equality Method)

### SBPP-COL-21:End
