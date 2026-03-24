## SBPP-COL-19 - Detect

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-19:1 - Problem frame

Finding the first element in a collection that satisfies a condition is a common
operation — finding the most urgent claim, the first expired policy, the cheapest
option. Manual loops that set a flag variable for "found" are verbose and error-prone.

### SBPP-COL-19:2 - Problem

How do you find the first element in a collection that meets a criterion, handling
the case where no such element exists safely?

### SBPP-COL-19:3 - Forces

| Force | Tension |
|-------|---------|
| **Safety** | What happens if no element is found? ↔ must handle absent result |
| **Clarity** | `findFirst()` / `find {}` communicates "search for first" ↔ loop + break does not |
| **Short-circuit** | Stream/Kotlin stops at first match ↔ full iteration wastes time |

### SBPP-COL-19:4 - Solution — Use `stream().filter().findFirst()` (Java) or `.find {}` (Kotlin); return `Optional`/nullable

**Java:**

```java
// ✅ findFirst returning Optional
Optional<Claim> urgentClaim = claims.stream()
    .filter(Claim::isUrgent)
    .findFirst();

// ✅ Safe handling of absent result
urgentClaim.ifPresent(claimService::processUrgent);

// ✅ Default when not found
Claim nextClaim = claims.stream()
    .filter(Claim::isPending)
    .findFirst()
    .orElseThrow(() -> new NoClaimsException("No pending claims"));

// ✅ findFirst with predicate (no separate filter needed in some cases)
Optional<Policy> target = policies.stream()
    .filter(p -> p.getId().equals(targetId))
    .findFirst();
```

**Kotlin:**

```kotlin
// ✅ find returns nullable
val urgentClaim: Claim? = claims.find { it.isUrgent }

// ✅ Safe null handling
urgentClaim?.let { claimService.processUrgent(it) }

// ✅ first/last with exception on not found
val nextClaim = claims.first { it.isPending }    // throws NoSuchElementException if none

// ✅ firstOrNull / lastOrNull
val candidate: Policy? = policies.firstOrNull { it.id == targetId }

// ✅ minByOrNull / maxByOrNull
val cheapest: Policy? = policies.minByOrNull { it.premium }
val mostExpensive: Policy? = policies.maxByOrNull { it.premium }
```

### SBPP-COL-19:5 - Archetypal Grounding

**U.System:** `claims.find { it.isUrgent }` — returns the first urgent claim or null; the caller handles both cases.
**U.Episteme:** `findFirst()` short-circuits — stops searching at the first match, making it O(k) where k is the position of the match.

### SBPP-COL-19:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `findFirst()` without null handling crashes on absent — use `Optional`/nullable | Always chain `.orElse()`/`?.` |
| **Arch** | `findFirst()` vs `findAny()` — `findAny()` may be faster in parallel streams | Use `findFirst()` for deterministic results |
| **Onto/Epist** | Kotlin `first { }` throws; `firstOrNull { }` returns null — easy to confuse | Use `firstOrNull` by default; use `first` only when absent is an error |
| **Prag** | Kotlin `minByOrNull`/`maxByOrNull` for extreme-value searches | Use instead of sort + first |
| **Did** | Teach `Optional`/nullable return as the correct absent-result pattern | |

### SBPP-COL-19:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL19-1** | Element search SHALL use `stream().filter().findFirst()` (Java) or `.find {}` / `.firstOrNull {}` (Kotlin). | Clarity and short-circuit |
| **CC-COL19-2** | The absent result case MUST be handled (`.orElse()`, `.orElseThrow()`, null check). | Prevents NPE/NoSuchElementException |
| **CC-COL19-3** | Kotlin `first {}` (throwing) SHALL only be used when absence is a programming error. | Correct error semantics |

### SBPP-COL-19:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Manual loop with boolean flag for "found" — Fix: `find`/`findFirst`.
**Anti-pattern 2:** `findFirst().get()` without `isPresent()` check — Fix: `.orElseThrow()` or `.orElse(null)`.

### SBPP-COL-19:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Short-circuits at first match | Must handle absent case |
| `Optional`/nullable communicates "may not exist" | — |

### SBPP-COL-19:10 - Rationale

Beck's Detect pattern maps directly to `findFirst()`/`find{}`. The key modern addition is
the mandatory absent-result handling via `Optional` (Java) or nullable (Kotlin).

### SBPP-COL-19:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `Optional` (post-2014):** Safe absent-result pattern. *Adopt.*
**Kotlin nullable + `firstOrNull` (post-2016):** Idiomatic null-safe search. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Optional/findFirst | Safe search | **Adopt** |
| Kotlin nullable/firstOrNull (post-2016) | Idiomatic | **Adopt** |

### SBPP-COL-19:12 - Relations

* **Part of:** Collection Protocol patterns
* **Contrast with:** COL-18 (Select/Reject — all matching elements)
* **Relates to:** COL-26 (Lookup Cache — cache-based detect optimisation)

### SBPP-COL-19:End
