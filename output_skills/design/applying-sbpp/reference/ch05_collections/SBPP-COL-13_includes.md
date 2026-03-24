## SBPP-COL-13 - Includes

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-13:1 - Problem frame

Testing whether a collection contains an element is a fundamental collection operation.
The temptation to use manual enumeration loops or `indexOf()` checks instead of
`contains()` leads to verbose, intent-obscuring code.

### SBPP-COL-13:2 - Problem

How do you test whether a specific element is present in a collection in a way that
communicates intent clearly and is as efficient as the collection type allows?

### SBPP-COL-13:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | `contains()` names the concept ↔ loop-based check reveals mechanics |
| **Performance** | `HashSet.contains()` is O(1) ↔ `List.contains()` is O(n) |
| **Type** | Right collection for frequent membership tests is `Set`, not `List` |

### SBPP-COL-13:4 - Solution — Use `contains()` for membership tests; use `Set` when contains is a hot path

**Java:**

```java
// ❌ Manual loop
boolean found = false;
for (RiskCode code : policy.getRiskCodes()) {
    if (code.equals(RiskCode.FLOOD)) { found = true; break; }
}

// ✅ Use contains()
boolean hasFloodRisk = policy.getRiskCodes().contains(RiskCode.FLOOD);

// ✅ Use Set when membership is a hot path
Set<PolicyId> activePolicyIds = new HashSet<>(activeIds);
if (activePolicyIds.contains(incomingId)) { ... }  // O(1)

// ✅ containsAll for subset check
boolean hasAllRequiredCoverages = policy.getCoverages().containsAll(requiredCoverages);

// ✅ Stream-based predicate for complex membership
boolean hasHighRisk = policy.getRiskFactors().stream()
    .anyMatch(f -> f.getScore() > HIGH_RISK_THRESHOLD);
```

**Kotlin:**

```kotlin
// ✅ contains via 'in' operator
val hasFloodRisk = RiskCode.FLOOD in policy.riskCodes

// ✅ any() for predicate-based membership
val hasHighRisk = policy.riskFactors.any { it.score > HIGH_RISK_THRESHOLD }

// ✅ all() and none()
val allCriticalCovered = requiredCoverages.all { it in policy.coverages }
val noExclusions = exclusionList.none { it in policy.coverages }
```

### SBPP-COL-13:5 - Archetypal Grounding

**U.System:** `RiskCode.FLOOD in policy.riskCodes` — reads as a business rule; a for-loop does not.
**U.Episteme:** Choosing `Set` over `List` when `contains()` is on a hot path is an O(n) → O(1) improvement that the type system signals.

### SBPP-COL-13:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Membership testing in Java/Kotlin collections**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `List.contains()` is O(n) — performance bug if called in a loop | Change to `Set` when `contains` is called frequently |
| **Arch** | `contains()` requires correct `equals()` on elements | Use records/data classes |
| **Onto/Epist** | `any { predicate }` vs `contains()` — use `contains()` for exact match, `any` for predicates | Pick the right API for the test type |
| **Prag** | Kotlin `in` operator is sugar for `contains()` — use it | `if (x in collection)` is idiomatic Kotlin |
| **Did** | New developers write loops instead of `contains()` | Teach: `contains()` is always clearer than a manual loop |

### SBPP-COL-13:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL13-1** | Membership tests SHALL use `contains()` / `in` operator, not manual loops. | Expressiveness |
| **CC-COL13-2** | When `contains()` is called in a loop or repeatedly, the collection SHOULD be a `Set`. | O(1) performance |
| **CC-COL13-3** | Predicate-based membership tests SHALL use `stream().anyMatch()` (Java) or `.any {}` (Kotlin). | Intention-revealing |

### SBPP-COL-13:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Manual loop for `contains`. Fix: `collection.contains(element)`.
**Anti-pattern 2:** `list.contains()` in O(n) loop → O(n²). Fix: convert to `Set` first.

### SBPP-COL-13:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Reads as business intent | O(n) for List — convert to Set when performance matters |
| `any {}` / `anyMatch()` for predicate membership | — |

### SBPP-COL-13:10 - Rationale

Beck's Includes: pattern is directly `contains()` in Java/Kotlin. The modern extension is
Kotlin's `in` operator and stream `anyMatch()` for predicate-based membership.

### SBPP-COL-13:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Kotlin `in` operator (post-2016):** Sugar for `contains()`; reads as a business rule. *Adopt.*
**Java Stream `anyMatch()` (Java 8+):** Predicate-based membership. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin `in` operator (post-2016) | Idiomatic membership test | **Adopt** |
| Java 8+ `anyMatch()` | Predicate membership | **Adopt** |

### SBPP-COL-13:12 - Relations

* **Part of:** Collection Protocol patterns
* **Performance depends on:** SBPP-COL-04 (Set) for O(1) contains

### SBPP-COL-13:End
