## SBPP-COL-18 - Select/Reject

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-18:1 - Problem frame

Filtering a collection to include only elements matching a criterion is one of the most
common collection operations. Writing explicit loops with conditional add is verbose and
obscures the filtering intent.

### SBPP-COL-18:2 - Problem

How do you produce a sub-collection of elements that meet a criterion, and a complement
that does not, without writing explicit iteration loops?

### SBPP-COL-18:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | `filter` announces "selection" ↔ a loop with `if` does not |
| **Reuse** | Named predicate can be reused across multiple filter calls | |
| **Partition** | Sometimes both matching and non-matching subsets are needed | |

### SBPP-COL-18:4 - Solution — Use `filter` / `filterNot` / `partition` for all collection selection

**Java:**

```java
// ✅ filter (select)
List<Policy> activePolicies = policies.stream()
    .filter(Policy::isActive)
    .collect(toList());

// ✅ filter with lambda predicate
List<Policy> highRisk = policies.stream()
    .filter(p -> p.getRiskScore() > HIGH_RISK_THRESHOLD)
    .collect(toList());

// ✅ filter with named predicate (reusable)
Predicate<Policy> isHighRisk = p -> p.getRiskScore() > HIGH_RISK_THRESHOLD;
List<Policy> highRiskPolicies = policies.stream().filter(isHighRisk).collect(toList());
List<Policy> highRiskExpired = policies.stream()
    .filter(isHighRisk.and(Policy::isExpired)).collect(toList());

// ✅ partition (select AND reject simultaneously)
Map<Boolean, List<Policy>> partitioned = policies.stream()
    .collect(Collectors.partitioningBy(Policy::isActive));
List<Policy> active  = partitioned.get(true);
List<Policy> expired = partitioned.get(false);
```

**Kotlin:**

```kotlin
// ✅ filter (select)
val activePolicies = policies.filter { it.isActive }

// ✅ filterNot (reject)
val inactivePolicies = policies.filterNot { it.isActive }

// ✅ partition (both at once)
val (active, expired) = policies.partition { it.isActive }

// ✅ filterIsInstance (filter by type)
val premiumPolicies: List<PremiumPolicy> = policies.filterIsInstance<PremiumPolicy>()
```

### SBPP-COL-18:5 - Archetypal Grounding

**U.System:** `val (active, expired) = policies.partition { it.isActive }` — select AND reject in one destructured expression.
**U.Episteme:** Named predicates (`isHighRisk`) can be composed with `and`/`or`/`negate()` — building a vocabulary of selection criteria.

### SBPP-COL-18:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Complex predicates inline are hard to review | Extract to named `Predicate<T>` constants or functions |
| **Arch** | `filter` + `map` chained is a common pattern — order matters for performance | Filter first, then map — reduces elements before transformation |
| **Onto/Epist** | `partition` is underused but eliminates two-pass filtering | Use `partition` when both halves are needed |
| **Prag** | Kotlin `filterNot` is `filter { !it.condition }` — clearer | Use `filterNot` for rejection |
| **Did** | Most developers know `filter` — teach `partition` and predicate composition | |

### SBPP-COL-18:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL18-1** | Collection filtering SHALL use `filter` / `stream().filter()`, not explicit loops. | Clarity |
| **CC-COL18-2** | When both matching and non-matching subsets are needed, `partition` SHOULD be used. | Avoids two-pass iteration |
| **CC-COL18-3** | Complex predicates SHALL be extracted to named constants. | Readability and reuse |

### SBPP-COL-18:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Two separate filter passes for active and inactive — Fix: `partition`.
**Anti-pattern 2:** `filter { !predicate }` instead of `filterNot { predicate }` — Fix: use `filterNot`.

### SBPP-COL-18:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Intent-revealing filtering | Complex predicates can become verbose inline |
| `partition` eliminates double iteration | — |

### SBPP-COL-18:10 - Rationale

Beck's Select/Reject maps directly to `filter`/`filterNot`. Kotlin adds `partition` as
a first-class two-way filter — elegant for the common "split a list" operation.

### SBPP-COL-18:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `stream().filter()` (post-2014):** Standard selection. *Adopt.*
**Kotlin `filter`/`filterNot`/`partition` (post-2016):** Idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream `filter` | Selection | **Adopt** |
| Kotlin `filter`/`partition` (post-2016) | Idiomatic select/reject | **Adopt** |

### SBPP-COL-18:12 - Relations

* **Part of:** Collection Protocol patterns
* **Contrast with:** COL-17 (Collect — transformation), COL-19 (Detect — find first)

### SBPP-COL-18:End
