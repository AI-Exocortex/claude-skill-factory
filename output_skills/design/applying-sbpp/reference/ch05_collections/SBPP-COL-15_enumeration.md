## SBPP-COL-15 - Enumeration

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-15:1 - Problem frame

Executing code across every element of a collection is the most fundamental collection
operation. Java's for-each loop and the Stream API, and Kotlin's collection functions,
provide multiple idioms. Choosing the right one for the operation determines both
readability and correctness.

### SBPP-COL-15:2 - Problem

How do you express code that applies an operation to every element of a collection,
choosing between imperative and functional styles appropriately?

### SBPP-COL-15:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | `forEach` names the intent ↔ a for-each loop is sometimes clearer for complex bodies |
| **Functional purity** | Stream pipeline is declarative ↔ `forEach` with side effects is imperative in a functional wrapper |
| **Modification** | Cannot remove elements during `forEach` ↔ `Iterator.remove()` allows safe removal |

### SBPP-COL-15:4 - Solution — Use enhanced for-each for simple iteration; streams for transformation; avoid `forEach` with side effects

**Java:**

```java
// ✅ Enhanced for-each — clearest for simple operations
for (Policy policy : policies) {
    auditLog.record(policy.getId());
}

// ✅ Stream forEach only for terminal side effects after a pipeline
policies.stream()
    .filter(Policy::isExpired)
    .forEach(this::sendRenewalNotification);

// ✅ Stream pipeline (transformation, not side-effect)
List<Money> premiums = policies.stream()
    .map(Policy::getPremium)
    .collect(toList());

// ❌ forEach with complex mutation — use regular for-each instead
policies.forEach(p -> { p.recalculate(); results.add(p.getPremium()); });
```

**Kotlin:**

```kotlin
// ✅ forEach for side effects
policies.forEach { auditLog.record(it.id) }

// ✅ Transformation — map/filter
val premiums: List<Money> = policies.map { it.premium }
val expired: List<Policy> = policies.filter { it.isExpired }

// ✅ forEachIndexed when index matters
policies.forEachIndexed { index, policy -> log.info("[$index] ${policy.id}") }

// ✅ onEach for side effects in a chain (returns the original collection)
val processed = policies
    .filter { it.isActive }
    .onEach { auditLog.record(it.id) }   // side effect mid-chain
    .map { it.premium }
```

### SBPP-COL-15:5 - Archetypal Grounding

**U.System:** `policies.filter { it.isExpired }.forEach { sendRenewalNotification(it) }` — filter then act, two clear stages.
**U.Episteme:** `stream().forEach()` with complex mutation is anti-pattern — it mixes the functional form with imperative semantics; use a plain for-each.

### SBPP-COL-15:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `ConcurrentModificationException` when modifying during iteration | Use iterator with `remove()` or collect to new list |
| **Arch** | Stream `forEach` does not allow `break`/`continue` | Use enhanced for-each when early exit is needed |
| **Onto/Epist** | Functional `map`/`filter` communicate transformation intent; `forEach` communicates side effects | Use the right one for the right intent |
| **Prag** | Kotlin `forEach`, `map`, `filter` are extension functions on `Iterable` | Use them everywhere; they work on all collections |
| **Did** | New developers write index-based loops for everything | Teach: for-each first; streams/collection functions second; index loop only when index matters |

### SBPP-COL-15:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL15-1** | Collection traversal for transformation SHOULD use `map`/`filter`/`flatMap` (stream or Kotlin). | Functional clarity |
| **CC-COL15-2** | `forEach` SHOULD only be used for terminal side effects, not for building results. | Separation of side effects |
| **CC-COL15-3** | Enhanced for-each SHOULD be used when the loop body is complex and early exit is needed. | Appropriate loop form |

### SBPP-COL-15:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `forEach` building a result list — use `map` / `collect` instead.
**Anti-pattern 2:** Index-based loop when only elements are needed — use for-each.

### SBPP-COL-15:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Functional pipelines communicate transformation intent | Stream `forEach` cannot `break` — use for-each when early exit needed |
| for-each works with any `Iterable` | — |

### SBPP-COL-15:10 - Rationale

Beck's Enumeration pattern establishes that collection iteration should be expressed at
the collection level, not at the element level. Java/Kotlin provide rich enumeration idioms
that make intent explicit.

### SBPP-COL-15:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ Stream API (post-2014):** `map`, `filter`, `forEach` as higher-level enumeration. *Adopt.*
**Kotlin collection functions (post-2016):** `forEach`, `map`, `filter`, `onEach`. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream API | Higher-order enumeration | **Adopt** |
| Kotlin stdlib (post-2016) | Extension-based enumeration | **Adopt** |

### SBPP-COL-15:12 - Relations

* **Foundation for:** COL-16 (Do), COL-17 (Collect), COL-18 (Select/Reject), COL-19 (Detect), COL-20 (Inject:into:)
* **Enables:** All higher-level collection protocols

### SBPP-COL-15:End
