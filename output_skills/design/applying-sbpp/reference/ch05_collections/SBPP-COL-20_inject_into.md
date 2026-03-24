## SBPP-COL-20 - Inject:into (Reduce/Fold)

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-20:1 - Problem frame

Accumulating a running value across a collection — sum, product, maximum, concatenation,
building a complex result — is a universal pattern. Writing the manual accumulation
pattern (initialise, loop, update, return) obscures the intent. `reduce`/`fold` express
it declaratively.

### SBPP-COL-20:2 - Problem

How do you reduce a collection to a single value by applying a combining function
iteratively, in a way that communicates the accumulation intent?

### SBPP-COL-20:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | `reduce`/`fold` announce accumulation ↔ explicit loop is sometimes clearer for complex accumulators |
| **Initial value** | `fold` requires an initial value ↔ `reduce` may fail on empty collection |
| **Type change** | `fold` can accumulate into a different type ↔ `reduce` must stay in the same type |

### SBPP-COL-20:4 - Solution — Use `stream().reduce()` / `stream().collect()` (Java) or `fold`/`reduce` (Kotlin)

**Java:**

```java
// ✅ reduce: sum Money values
Optional<Money> totalOpt = premiums.stream().reduce(Money::add);
Money total = premiums.stream().reduce(Money.ZERO, Money::add);

// ✅ reduce to different type via collect/fold pattern
Map<PolicyStatus, Long> countByStatus = policies.stream()
    .collect(Collectors.groupingBy(Policy::getStatus, Collectors.counting()));

// ✅ reduce for max/min
Optional<Money> highest = premiums.stream().reduce((a, b) -> a.compareTo(b) >= 0 ? a : b);
// Better: use built-in
Optional<Policy> mostExpensive = policies.stream().max(Comparator.comparing(Policy::getPremium));

// ✅ Specialized reduce operations
IntSummaryStatistics stats = policies.stream()
    .mapToInt(p -> p.getClaimCount())
    .summaryStatistics();
```

**Kotlin:**

```kotlin
// ✅ fold: accumulate with initial value (works on empty collection)
val total: Money = premiums.fold(Money.ZERO) { acc, premium -> acc + premium }

// ✅ reduce: no initial value (returns first element if singleton; throws if empty)
val total: Money = premiums.reduce { acc, premium -> acc + premium }

// ✅ sumOf: specialized fold for numbers
val totalCents: Long = premiums.sumOf { it.cents }
val avgAge: Double = policies.map { it.applicantAge.toDouble() }.average()

// ✅ fold to different type
val idSet: Set<PolicyId> = policies.fold(emptySet()) { acc, policy -> acc + policy.id }

// ✅ groupingBy equivalent
val countByStatus: Map<PolicyStatus, Int> = policies
    .groupBy { it.status }
    .mapValues { (_, ps) -> ps.size }
```

### SBPP-COL-20:5 - Archetypal Grounding

**U.System:** `premiums.fold(Money.ZERO) { acc, p -> acc + p }` — accumulates all premiums into a total; intent is "running sum".
**U.Episteme:** `fold` requires an identity (initial) value — `Money.ZERO` is the identity for addition; the math mirrors the algebraic structure.

### SBPP-COL-20:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `reduce` on an empty collection returns empty `Optional` — easy to miss | Use `fold` with identity value; never call `.get()` on `reduce` result |
| **Arch** | For large collections, parallel `reduce` is available via parallel streams | Profile first; parallel adds complexity |
| **Onto/Epist** | `fold` is more general than `reduce` — prefer it | Use `fold`; only use `reduce` when there is no natural identity value |
| **Prag** | Kotlin has `sumOf`, `maxOf`, `minOf`, `average` for common numeric reductions | Use specialised functions; only write `fold` for custom accumulators |
| **Did** | `fold` is a functional concept new to many Java developers | Teach with sum example first, then generalise |

### SBPP-COL-20:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL20-1** | Running-value accumulation SHALL use `stream().reduce()` / `fold` / `reduce`, not explicit loop + accumulator variable. | Declarative intent |
| **CC-COL20-2** | Numeric reductions in Kotlin SHOULD use `sumOf`, `maxOf`, `minOf`, `average` when available. | Idiomatic |
| **CC-COL20-3** | `fold` SHOULD be preferred over `reduce` when an identity/initial value exists. | Safe on empty collections |

### SBPP-COL-20:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Manual accumulator: `var total = Money.ZERO; for (p in policies) total += p.premium` — Fix: `policies.fold(Money.ZERO) { acc, p -> acc + p.premium }`.
**Anti-pattern 2:** `stream().reduce().get()` without empty handling — Fix: `.reduce(identity, combiner)`.

### SBPP-COL-20:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Declarative accumulation; no mutable accumulator variable | `fold` concept requires understanding |
| Kotlin specialised functions (`sumOf`) eliminate even the fold | Empty collection handling with `reduce` |

### SBPP-COL-20:10 - Rationale

`inject:into:` (Smalltalk's fold/reduce) is one of Beck's most elegant patterns.
Java/Kotlin provide `reduce`/`fold` and rich specialised collectors. Kotlin's `sumOf`,
`maxOf`, `minOf` make the most common reductions one-liners.

### SBPP-COL-20:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `stream().reduce()` / `Collectors` (post-2014):** Full reduction toolkit. *Adopt.*
**Kotlin `fold`/`reduce`/`sumOf` (post-2016):** Idiomatic reductions. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream reduce/Collectors | Full reduction toolkit | **Adopt** |
| Kotlin `fold`/`sumOf` (post-2016) | Idiomatic | **Adopt** |

### SBPP-COL-20:12 - Relations

* **Part of:** Collection Protocol patterns
* **Generalises:** sum, max, min, count
* **Used by:** SBPP-BEH-31 (Collecting Parameter — alternative accumulation strategy)

### SBPP-COL-20:End
