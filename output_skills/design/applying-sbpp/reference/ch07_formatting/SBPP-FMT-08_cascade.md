## SBPP-FMT-08 - Cascade

> **Type:** Architectural (A)
> **Status:** Adapt
> **Normativity:** Normative

### SBPP-FMT-08:1 - Problem frame

In Smalltalk, the cascade (`;`) allowed sending multiple messages to the same receiver
without repeating the receiver expression. Java and Kotlin have no direct cascade syntax,
but they provide equivalent mechanisms: builder patterns, scope functions (`apply`, `also`,
`with`, `let`, `run`), and method chaining. This pattern establishes when to use these
equivalents and when to use a temporary variable instead.

### SBPP-FMT-08:2 - Problem

How do you express multiple operations on the same object without repeatedly writing
the receiver expression or creating unnecessary temporary variables?

### SBPP-FMT-08:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | Cascade/scope function communicates "all these ops go to the same object" ↔ may obscure sequential dependencies |
| **Return value** | Some operations don't return `this`, making chaining impossible | |
| **Mutability** | Cascades are for mutation ↔ builders prefer immutable construction | |

### SBPP-FMT-08:4 - Solution — Use builder patterns for construction; Kotlin scope functions for configuration; method chaining for fluent APIs

**Java — Builder pattern (construction cascade):**

```java
// ✅ Builder = cascade equivalent for construction
RatingResult result = RatingResult.builder()
    .policyId(policy.getId())
    .premium(premium)
    .riskScore(riskScore)
    .effectiveDate(effectiveDate)
    .adjustments(adjustments)
    .build();
```

**Java — temporary variable for configuration (explicit, readable):**

```java
// ✅ Temporary variable — clearest when receiver is complex to compute
PolicySummary summary = new PolicySummary();
summary.setPolicyId(policy.getId());
summary.setStatus(policy.getStatus());
summary.setPremium(policy.getPremium());
// Note: prefer a Builder or named factory over mutable object configuration
```

**Java — fluent method chaining (self-returning methods):**

```java
// ✅ Fluent builder / chaining when each method returns `this`
new PolicyValidator()
    .checkActive(policy)
    .checkSufficientCoverage(policy)
    .checkNoOutstandingClaims(policy)
    .validate();
```

**Kotlin — scope functions as cascade equivalents:**

```kotlin
// ✅ apply: configure an object, return the object
val summary = PolicySummary().apply {
    policyId = policy.id
    status = policy.status
    premium = policy.premium
}

// ✅ also: perform side effects, return the object
val policy = findPolicy(id)
    .also { log.info("Processing policy ${it.id}") }
    .also { auditService.record(it) }

// ✅ with: operate on an object, return result (non-extension form)
val description = with(policy) {
    "Policy $id: $status, premium=$premium"
}

// ✅ let: transform an object (like map for single values)
val premium = policy.basePremium
    .let { applyDiscounts(it) }
    .let { applySurcharges(it) }
    .let { roundToNearestCent(it) }
```

**When to use each Kotlin scope function:**

| Scope function | Returns | Use when |
|---------------|---------|---------|
| `apply { }` | receiver | Configuring/initialising an object |
| `also { }` | receiver | Side effects (logging, auditing) without changing the chain |
| `let { }` | lambda result | Transforming a value (like `map` for single value) |
| `run { }` | lambda result | Computing a result using the object's context |
| `with(obj) { }` | lambda result | Grouping operations on an object without extension |

### SBPP-FMT-08:5 - Archetypal Grounding

**U.System:** `PolicySummary().apply { policyId = policy.id; status = policy.status }` — the
`apply` block is a Kotlin cascade: all assignments go to the same newly created object.

**U.Episteme:** Kotlin's scope functions are Beck's cascade concept made explicit and typed —
each scope function communicates a distinct intent (`apply` = configure, `also` = side-effect,
`let` = transform).

### SBPP-FMT-08:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Multi-operation on same object in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Overuse of Kotlin scope functions can make code harder to read for Java developers | Use scope functions where they provide clear benefit; document their semantics in team guidelines |
| **Arch** | Mutable object configuration (setter-based) is a design smell — prefer builders or constructors | Use scope functions primarily for builder-style configuration; avoid `apply` on domain objects that should be immutable |
| **Onto/Epist** | Java has no scope functions; the closest equivalent is a Builder or temporary variable | In Java, prefer Builder; use temporary variable for simple multi-setter cases |
| **Prag** | Kotlin's `apply`/`also`/`let` are idiomatic and widely used | Use them; but choose the right one semantically |
| **Did** | New Kotlin developers overuse `let` where `if (x != null)` or `apply` is clearer | Teach each scope function's semantics with examples |

### SBPP-FMT-08:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT08-1** | Object construction with multiple fields SHALL use a Builder (Java) or data class `copy()` / primary constructor (Kotlin). | Immutable construction |
| **CC-FMT08-2** | Kotlin `apply {}` SHOULD be used for mutable object initialisation when a builder is not available. | Cascade equivalent |
| **CC-FMT08-3** | Kotlin `also {}` SHOULD be used for side effects (logging, auditing) that do not change the main chain. | Semantic clarity |
| **CC-FMT08-4** | The right scope function SHOULD be selected based on its return value and semantic intent (see table above). | Intentional use |

### SBPP-FMT-08:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Wrong scope function**
Using `let` when `apply` is needed (or vice versa) — `let` returns the lambda result; `apply`
returns the receiver. A chain that unexpectedly loses the original object is a `let`/`apply` confusion.
Fix: check return value of the scope function before choosing.

**Anti-pattern 2: Deeply nested scope functions**
`policy.let { p -> p.claims.let { cs -> cs.filter { ... } } }` — Fix: use intermediate variables
or extract to a named function.

### SBPP-FMT-08:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| "All these ops on the same object" intent is clear | Scope function semantics must be known by the team |
| Kotlin scope functions are typed — return value is predictable | Overuse creates hard-to-read nested chains |
| Builder pattern eliminates setter-based configuration | — |

### SBPP-FMT-08:10 - Rationale

Smalltalk's cascade (`;`) has no direct equivalent in Java/Kotlin syntax. The idioms that
serve the same purpose — Builder, fluent chaining, Kotlin scope functions — are in some ways
superior: they have explicit return-value semantics and communicate distinct intents (`apply`
vs `also` vs `let`). The adaptation is a genuine improvement over the original.

### SBPP-FMT-08:11 - SoTA-Echoing

**Adoption verdict: ADAPT**

**Kotlin scope functions documentation (JetBrains, post-2016):** Defines `apply`, `also`, `let`,
`run`, `with` with explicit semantics. *Adopt as the Kotlin cascade equivalent.*

**Builder pattern (GoF, widely applied post-2015):** The Java construction cascade. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 2 ("Consider a builder when faced with many
constructor parameters") — the Java cascade for construction. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin scope functions (JetBrains, post-2016) | Typed cascade equivalents | **Adopt** |
| Effective Java 3rd ed. Item 2 (Bloch, 2018) | Builder as construction cascade | **Adopt** |
| GoF Builder (widely applied post-2015) | Java multi-field construction | **Adopt** |

### SBPP-FMT-08:12 - Relations

* **Extends:** SBPP-FMT-03 (Indented Control Flow — cascades/scope functions are formatted with these rules)
* **Enables:** SBPP-FMT-09 (Yourself — the value problem that Yourself solves; in Kotlin, `apply` solves it structurally)
* **Relates to:** SBPP-BEH-11 (Execute Around Method — scope functions are Execute Around patterns)

### SBPP-FMT-08:End
