## SBPP-COL-16 - Do

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-16:1 - Problem frame

`do:` in Smalltalk is the fundamental "execute for each element" operation. In Java/Kotlin
this maps to the enhanced for-each loop and `forEach()`. The pattern establishes when
to use simple iteration vs higher-order alternatives.

### SBPP-COL-16:2 - Problem

How do you execute a block of code for each element in a collection, in the simplest
possible way that communicates the intent?

### SBPP-COL-16:3 - Forces

| Force | Tension |
|-------|---------|
| **Simplicity** | for-each is universally understood ↔ `forEach()` is more composable |
| **Side effects** | `forEach` names that side effects are happening ↔ a for-loop is sometimes clearer for complex bodies |
| **Modification** | Cannot safely modify the collection during iteration with `forEach` | |

### SBPP-COL-16:4 - Solution — Use enhanced for-each for imperative work; `forEach()` for terminal stage of a pipeline

**Java:**

```java
// ✅ Enhanced for-each — standard imperative iteration
for (Claim claim : claims) {
    claimService.process(claim);
}

// ✅ forEach after a filter (pipeline terminal)
claims.stream()
    .filter(Claim::isUrgent)
    .forEach(claimService::process);

// ✅ forEach with method reference
claims.forEach(claimService::process);

// ✅ When index matters, use traditional for loop
for (int i = 0; i < claims.size(); i++) {
    log.info("Processing claim {} of {}", i + 1, claims.size());
    claimService.process(claims.get(i));
}
```

**Kotlin:**

```kotlin
// ✅ forEach with lambda
claims.forEach { claimService.process(it) }

// ✅ forEach with method reference style
claims.forEach(claimService::process)

// ✅ forEachIndexed when index needed
claims.forEachIndexed { i, claim ->
    log.info("Processing claim ${i+1} of ${claims.size}")
    claimService.process(claim)
}
```

### SBPP-COL-16:5 - Archetypal Grounding

**U.System:** `claims.forEach(claimService::process)` — one line, reads as "for each claim, process it".
**U.Episteme:** Enhanced for-each works on any `Iterable`; `forEach()` is an extension that adds composability.

### SBPP-COL-16:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `forEach` with complex side effects is hard to read | Use for-each when the body is complex |
| **Arch** | Cannot `break` out of `forEach()` | Use for-each or iterator when early exit is needed |
| **Onto/Epist** | `forEach` implies "side effect for each"; if you're building a result, use `map`/`collect` | Pick the right operation for the intent |
| **Prag** | Kotlin for-each is very clean | Use it everywhere for side-effect iteration |
| **Did** | Simplest iteration pattern — start here when teaching collections | |

### SBPP-COL-16:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL16-1** | Simple side-effect iteration SHALL use enhanced for-each (Java) or `forEach` (Kotlin). | Clarity |
| **CC-COL16-2** | `forEach` MUST NOT be used to build result values — use `map`/`collect` instead. | Correct operation choice |

### SBPP-COL-16:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Using `forEach` to build a result: `list.forEach { result.add(transform(it)) }` — Fix: `list.map { transform(it) }`.
**Anti-pattern 2:** Index-based for loop when index is not used — Fix: for-each.

### SBPP-COL-16:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Clear, universal iteration idiom | Cannot break mid-iteration in `forEach` |
| Method references make it concise | — |

### SBPP-COL-16:10 - Rationale

`do:` is Beck's most fundamental enumeration message. Java's for-each and Kotlin's `forEach`
are direct translations. The principle "prefer collection protocol over explicit loops" applies directly.

### SBPP-COL-16:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java enhanced for-each (Java 5+):** Universal iteration. *Adopt.*
**Kotlin `forEach` (post-2016):** Extension-based iteration. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java enhanced for-each | Universal iteration | **Adopt** |
| Kotlin `forEach` (post-2016) | Extension iteration | **Adopt** |

### SBPP-COL-16:12 - Relations

* **Specialises:** SBPP-COL-15 (Enumeration — simplest form)
* **Contrast with:** COL-17 (Collect), COL-18 (Select/Reject) — when result needed

### SBPP-COL-16:End
