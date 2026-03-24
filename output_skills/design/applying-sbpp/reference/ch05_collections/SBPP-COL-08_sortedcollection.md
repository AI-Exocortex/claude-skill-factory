## SBPP-COL-08 - SortedCollection

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-08:1 - Problem frame

When the order of elements in a collection matters for business logic — ranking policies
by premium, processing claims in date order, displaying entries sorted by name — the
collection must be sorted. Java/Kotlin provide multiple mechanisms for sorting that serve
different needs.

### SBPP-COL-08:2 - Problem

How do you maintain a collection in sorted order so that elements are always accessible
in the correct business sequence?

### SBPP-COL-08:3 - Forces

| Force | Tension |
|-------|---------|
| **Always-sorted vs sort-on-demand** | `TreeSet`/`PriorityQueue` maintain order on insert ↔ sorting on retrieval avoids overhead during mutation |
| **Natural vs custom order** | `Comparable` for natural order ↔ `Comparator` for context-dependent order |
| **Streaming vs persistent** | `stream().sorted()` is one-pass ↔ `TreeSet` maintains order persistently |

### SBPP-COL-08:4 - Solution — Sort at the point of use with `stream().sorted()` / `.sortedWith()`; use `TreeSet` only for always-sorted sets

**Java example — preferred: sort on use:**

```java
// ✅ Sort at retrieval time — no maintained sorted structure needed
List<Policy> rankedByPremium = policies.stream()
    .sorted(Comparator.comparing(Policy::premium).reversed())
    .collect(toList());

// Sort with multiple criteria
List<Claim> orderedClaims = claims.stream()
    .sorted(Comparator.comparing(Claim::filedDate)
                      .thenComparing(Claim::severity))
    .collect(toList());
```

**Java — TreeSet for always-sorted (use sparingly):**

```java
// ✅ TreeSet: always-sorted, unique elements
TreeSet<Policy> sortedPolicies = new TreeSet<>(
    Comparator.comparing(Policy::premium)
);
sortedPolicies.addAll(policies);
Policy mostExpensive = sortedPolicies.last();
Policy cheapest = sortedPolicies.first();
```

**Java — PriorityQueue for processing in priority order:**

```java
// ✅ PriorityQueue: next element is always the smallest
PriorityQueue<Claim> byUrgency = new PriorityQueue<>(
    Comparator.comparing(Claim::urgencyScore).reversed()
);
claimQueue.addAll(pendingClaims);
Claim next = claimQueue.poll();  // always highest urgency
```

**Kotlin example:**

```kotlin
// Sort on retrieval (preferred)
val rankedPolicies = policies.sortedByDescending { it.premium }
val orderedClaims  = claims.sortedWith(compareBy(Claim::filedDate, Claim::severity))

// Always-sorted set
val sortedSet = sortedSetOf(compareBy<Policy> { it.premium }, *policies.toTypedArray())
```

### SBPP-COL-08:5 - Archetypal Grounding

**U.System:** `policies.sortedByDescending { it.premium }` — sort declared at the use site,
close to where the order matters.

**U.Episteme:** "Sort on retrieval" is almost always correct; "always-sorted structure" is
only needed when the minimum/maximum element must be accessed repeatedly during mutation.

### SBPP-COL-08:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Sorted collection patterns in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Sorting is often forgotten — results presented in random order | Document sort order in API contracts; add tests for order |
| **Arch** | `TreeSet` adds O(log n) insert overhead vs `HashSet` O(1) | Use `TreeSet` only when sorted iteration is the primary operation |
| **Onto/Epist** | "Natural order" may not be the right order for a given use case | Always use explicit `Comparator` for clarity; don't rely on natural order unless it's universally correct |
| **Prag** | Kotlin `.sortedWith()` and `.sortedBy()` are clean and one-line | Prefer Kotlin sort idioms; avoid maintaining sorted data structures when not needed |
| **Did** | `Collections.sort()` sorts in place; `stream().sorted()` returns new — easy to confuse | In Kotlin: `sorted()` always returns a new list; `sortedWith()` uses a comparator |

### SBPP-COL-08:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL08-1** | Sorting SHOULD be declared at the point of use with `stream().sorted()` / `.sortedWith()`. | Avoids maintaining sorted structures unnecessarily |
| **CC-COL08-2** | `TreeSet` SHOULD only be used when the minimum/maximum element is frequently accessed during mutation. | Justifies the O(log n) insert cost |
| **CC-COL08-3** | Sort order SHOULD use an explicit `Comparator`, not reliance on natural order alone. | Clarity and intent |

### SBPP-COL-08:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Sorting inside a loop**
`sort(list)` called on every iteration — O(n log n) per iteration.
Fix: Sort once before the loop or use a `PriorityQueue`.

**Anti-pattern 2: TreeSet without `Comparator`**
`new TreeSet<Policy>()` without a comparator — fails at runtime if `Policy` doesn't implement `Comparable`.
Fix: always provide an explicit comparator.

### SBPP-COL-08:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Sort-on-use avoids maintaining sorted structures | `TreeSet` adds O(log n) per insert |
| `Comparator` chains are expressive and composable | — |

### SBPP-COL-08:10 - Rationale

Beck notes that experienced Smalltalk programmers "use the sort block more and implement
`<=` less." The equivalent Java/Kotlin wisdom is: sort with `Comparator` at use time;
reach for `TreeSet`/`PriorityQueue` only when the always-sorted guarantee is needed.

### SBPP-COL-08:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ Stream `sorted()` (post-2014):** The standard sort-on-demand mechanism. *Adopt.*

**Kotlin `sortedWith` / `sortedBy` (post-2016):** Idiomatic single-expression sorting. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 14 (Comparable); Items on Comparator composition. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream `sorted()` | Sort-on-demand | **Adopt** |
| Kotlin `sortedWith/sortedBy` (post-2016) | Idiomatic sort | **Adopt** |
| Effective Java 3rd ed. Item 14 (Bloch, 2018) | Comparator guidance | **Adopt** |

### SBPP-COL-08:12 - Relations

* **Specialises:** SBPP-COL-01 (Collection — sorted variant)
* **Requires:** SBPP-BEH-08 (Comparing Method — comparator definition)
* **Used by:** SBPP-COL-22 (Temporarily Sorted Collection)

### SBPP-COL-08:End
