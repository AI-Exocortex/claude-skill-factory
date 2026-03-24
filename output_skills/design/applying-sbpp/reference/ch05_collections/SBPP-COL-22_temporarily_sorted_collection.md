## SBPP-COL-22 - Temporarily Sorted Collection

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-22:1 - Problem frame

A collection is normally unsorted (a `HashSet` or `ArrayList`), but needs to be
presented in sorted order for one specific operation — a report, an API response,
a display. Permanently storing it as a `TreeSet` incurs ongoing O(log n) insert cost
for a benefit needed only occasionally.

### SBPP-COL-22:2 - Problem

How do you sort a collection for one specific use case without paying the cost of
permanently maintaining a sorted structure?

### SBPP-COL-22:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | Sort only when needed ↔ `TreeSet` always incurs O(log n) insert |
| **Expressiveness** | Sort-on-use is explicit ↔ a permanently sorted collection hides the sort cost |
| **Immutability** | Original collection should not be modified | |

### SBPP-COL-22:4 - Solution — Sort at the point of use with `stream().sorted()` or `.sortedWith()`; never modify the original

**Java:**

```java
// ✅ Sort for display/reporting only
public List<Policy> getPoliciesForReport() {
    return policies.stream()
        .sorted(Comparator.comparing(Policy::getPremium).reversed())
        .collect(toList());
    // policies field remains unsorted
}

// ✅ Sort with custom comparator
List<Claim> sortedClaims = claims.stream()
    .sorted(Comparator.comparing(Claim::getFiledDate).thenComparing(Claim::getUrgency))
    .collect(toList());
```

**Kotlin:**

```kotlin
// ✅ Sort for display — returns new sorted list
fun getPoliciesForReport(): List<Policy> =
    policies.sortedByDescending { it.premium }

// ✅ Multiple sort criteria
val sortedClaims = claims.sortedWith(compareBy(Claim::filedDate, Claim::urgency))
```

**Rule:** Never call `Collections.sort(list)` on a field — this modifies the stored collection.
Always create a sorted view.

### SBPP-COL-22:5 - Archetypal Grounding

**U.System:** `policies.sortedByDescending { it.premium }` in a report method — the field stays unsorted; only the report sees sorted data.
**U.Episteme:** The sort is declared at the point of use, making it clear to the reader that the order is for this specific context.

### SBPP-COL-22:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `Collections.sort()` modifies in place — wrong for shared collections | Always use stream `sorted()` or Kotlin `sortedWith()` |
| **Arch** | Sorting on every request is O(n log n) — expensive for large collections | Cache the sorted result if it is needed repeatedly |
| **Onto/Epist** | "Temporarily" implies the sort is for one context — document it | Javadoc: "Returns policies sorted by premium for display purposes" |
| **Prag** | Kotlin `sortedWith`/`sortedBy` always return a new list | Safe by default in Kotlin |
| **Did** | Teach: sort-on-use vs maintain-sorted-structure — the choice matters for performance | |

### SBPP-COL-22:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL22-1** | Temporary sorting SHALL use `stream().sorted()` (Java) or `sortedWith()` (Kotlin), producing a new collection. | Does not modify original |
| **CC-COL22-2** | `Collections.sort()` SHALL NOT be called on shared mutable collection fields. | Prevents unintended mutation |

### SBPP-COL-22:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `Collections.sort(this.policies)` in a getter — mutates the stored collection. Fix: `this.policies.stream().sorted(...)`.
**Anti-pattern 2:** Permanently converting to `TreeSet` when only one use needs order. Fix: sort at the point of use.

### SBPP-COL-22:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Original collection unmodified | O(n log n) per sort — cache if needed repeatedly |
| Sort criteria explicit at point of use | — |

### SBPP-COL-22:10 - Rationale

Beck's Temporarily Sorted Collection directly maps to sort-on-demand in Java/Kotlin.
The key principle — "sort when needed, not permanently" — applies directly.

### SBPP-COL-22:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `stream().sorted()` (post-2014):** Non-mutating sort. *Adopt.*
**Kotlin `sortedWith`/`sortedBy` (post-2016):** Always returns new list. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ `stream().sorted()` | Non-mutating sort | **Adopt** |
| Kotlin `sortedWith` (post-2016) | New-list sort | **Adopt** |

### SBPP-COL-22:12 - Relations

* **Specialises:** SBPP-COL-08 (SortedCollection — temporary variant)
* **Requires:** SBPP-BEH-08 (Comparing Method — sort key)

### SBPP-COL-22:End
