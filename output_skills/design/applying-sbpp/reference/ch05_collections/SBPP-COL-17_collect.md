## SBPP-COL-17 - Collect

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-17:1 - Problem frame

When you need to transform every element of a collection — apply a function and collect
the results — `collect:`/`map` is the right operation. Using `forEach` with mutation to
build a result list is a common anti-pattern that confuses transformation with side effects.

### SBPP-COL-17:2 - Problem

How do you produce a new collection by applying a function to each element of an existing
collection, communicating that this is a pure transformation?

### SBPP-COL-17:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | `map` announces "transformation" ↔ `forEach` with list.add() implies "side effect" |
| **Immutability** | `map` produces a new collection, never modifies the source | |
| **Type transformation** | `map` can change element types ↔ the type system tracks this |

### SBPP-COL-17:4 - Solution — Use `stream().map().collect()` (Java) or `.map {}` (Kotlin) for transformations

**Java:**

```java
// ✅ map: transform each element
List<Money> premiums = policies.stream()
    .map(Policy::getPremium)
    .collect(toList());

// ✅ map with transformation function
List<String> policyIds = policies.stream()
    .map(p -> p.getId().toString())
    .collect(toList());

// ✅ map to different type
List<PolicySummaryDto> summaries = policies.stream()
    .map(PolicySummaryDto::from)
    .collect(toList());

// ✅ Collectors.toUnmodifiableList() for immutable result (Java 10+)
List<Money> immutablePremiums = policies.stream()
    .map(Policy::getPremium)
    .collect(Collectors.toUnmodifiableList());
```

**Kotlin:**

```kotlin
// ✅ map: clean one-liner
val premiums: List<Money> = policies.map { it.premium }
val policyIds: List<String> = policies.map { it.id.toString() }
val summaries: List<PolicySummaryDto> = policies.map { PolicySummaryDto.from(it) }

// ✅ mapNotNull: transform and filter nulls in one step
val activeHolders: List<Customer> = policies.mapNotNull { it.activeHolder }

// ✅ mapIndexed: when position matters
val indexed: List<String> = policies.mapIndexed { i, p -> "$i: ${p.id}" }
```

### SBPP-COL-17:5 - Archetypal Grounding

**U.System:** `policies.map { it.premium }` — transforms a `List<Policy>` into a `List<Money>`; intent is transformation, not side effect.
**U.Episteme:** `map` communicates "apply function to each"; `forEach` communicates "execute for each". They have different intent; choose the right one.

### SBPP-COL-17:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Java `stream().map().collect()` is verbose compared to Kotlin `.map {}` | Accept the verbosity; it is standard Java idiom |
| **Arch** | Lazy stream evaluation: `map` is lazy; materialised at `collect()` | Understand that the list is not built until `collect()` |
| **Onto/Epist** | `map` should not have side effects — it is a pure transformation | Never put side-effecting code inside `map`; use `forEach` for that |
| **Prag** | Kotlin `mapNotNull` combines mapping and null filtering | Use it when the transform function can return null |
| **Did** | Teach `map` before `filter` — it is the most universal transformation | |

### SBPP-COL-17:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL17-1** | Transforming each element to produce a new collection SHALL use `map` / `stream().map()`. | Communicates transformation intent |
| **CC-COL17-2** | `map` functions SHOULD be pure (no side effects). | Functional correctness |
| **CC-COL17-3** | In Kotlin, `mapNotNull` SHOULD be used when the transform may return null. | Idiomatic null handling |

### SBPP-COL-17:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `forEach` building a result: `list.forEach { results.add(transform(it)) }` — Fix: `list.map { transform(it) }`.
**Anti-pattern 2:** Side effects in `map`: `list.map { it.also { process(it) } }` — Fix: separate transformation and side effects.

### SBPP-COL-17:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Pure transformation clearly separated from side effects | Java `stream().map().collect()` more verbose than Kotlin |
| Type-safe element type change | — |

### SBPP-COL-17:10 - Rationale

`collect:` in Smalltalk is `map` in Java/Kotlin. It is the most fundamental transformation
operation. The functional idiom — pure function applied to each element — is universally
supported and encouraged.

### SBPP-COL-17:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `stream().map()` (post-2014):** Standard transformation. *Adopt.*
**Kotlin `.map {}` (post-2016):** Idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ Stream `map` | Transformation | **Adopt** |
| Kotlin `.map {}` (post-2016) | Idiomatic | **Adopt** |

### SBPP-COL-17:12 - Relations

* **Part of:** Collection Protocol patterns
* **Contrast with:** COL-16 (Do — side effects), COL-18 (Select/Reject — filtering)

### SBPP-COL-17:End
