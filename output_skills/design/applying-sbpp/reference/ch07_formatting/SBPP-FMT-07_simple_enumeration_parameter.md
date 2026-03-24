## SBPP-FMT-07 - Simple Enumeration Parameter

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-FMT-07:1 - Problem frame

Beck's original pattern suggested calling the parameter of an enumeration block `each`
in Smalltalk. In Java/Kotlin, lambda parameters in iteration contexts are named, and
the convention differs slightly: Java uses descriptive single-word names; Kotlin uses
`it` implicitly for single-parameter lambdas, and named parameters for clarity.

### SBPP-FMT-07:2 - Problem

What do you name the iteration variable — the "current element" — inside a lambda
passed to a collection operation, so that the name adds clarity without adding noise?

### SBPP-FMT-07:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Descriptive name reveals what the element is ↔ generic `it` reduces noise |
| **Consistency** | One convention for all iteration ↔ context-specific names are sometimes clearer |
| **Nesting** | Nested iterations require distinguishing names ↔ `it` becomes ambiguous |

### SBPP-FMT-07:4 - Solution — Use `it` for obvious single-parameter lambdas in Kotlin; use a descriptive word for Java and for nested/complex lambdas

**Kotlin — `it` for obvious single-element lambdas:**

```kotlin
// ✅ it: unambiguous — "each policy" is obvious from the receiver
policies.filter { it.isActive }
policies.map { it.premium }
policies.forEach { process(it) }

// ✅ Named parameter — use when `it` is ambiguous or the body is complex
policies.filter { policy -> policy.isActive && policy.premium > MIN }
policies.forEach { policy ->
    val risk = riskService.assess(policy)
    ratingEngine.rate(policy, risk)
}

// ✅ Nested iteration — MUST use named parameters
portfolios.forEach { portfolio ->
    portfolio.policies.forEach { policy ->   // 'it' would be ambiguous here
        process(policy)
    }
}
```

**Java — descriptive single-word name derived from the type:**

```java
// ✅ Java: name matches the element's domain role
policies.stream().filter(policy -> policy.isActive());
policies.stream().map(policy -> policy.getPremium());
policies.stream().forEach(policy -> process(policy));

// ✅ Short conventional names acceptable when type is obvious from context
policies.stream().map(p -> p.getPremium());   // acceptable for simple one-liners

// ✅ Nested — longer names prevent confusion
portfolios.forEach(portfolio ->
    portfolio.getPolicies().forEach(policy ->
        process(policy)
    )
);
```

**Naming guidelines for iteration variables:**

| Context | Kotlin | Java |
|---------|--------|------|
| Simple one-arg lambda | `it` | `policy`, `claim` (lowercase type name) |
| Complex body lambda | `policy ->` | `policy ->` |
| Nested outer | `portfolio ->` | `portfolio ->` |
| Nested inner | `policy ->` | `policy ->` |
| Index also needed | `(index, policy) ->` | `(index, policy) ->` |

### SBPP-FMT-07:5 - Archetypal Grounding

**U.System:** `policies.filter { it.isActive }` — `it` is unambiguous; the receiver (`policies`)
makes the element type (`Policy`) obvious.

**U.Episteme:** In a nested loop `portfolios.forEach { portfolio -> portfolio.policies.forEach { policy -> ... } }`,
`it` in the inner loop would be ambiguous — named parameters are required.

### SBPP-FMT-07:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Iteration variable naming in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `it` in complex lambdas is harder to read and trace in stack traces | Use named parameters when the lambda body is > 2 lines |
| **Arch** | Kotlin `it` is always fine for single-line single-parameter lambdas | Switch to named parameter when the body grows |
| **Onto/Epist** | Beck's `each` in Smalltalk communicated "the current element of a collection" without specifying type | Kotlin's `it` serves the same role; named parameters serve Beck's intent more explicitly |
| **Prag** | IntelliJ shows the inferred type of `it` on hover — tooling compensates for the implicit name | Still prefer named parameter in code reviews |
| **Did** | Teach: `it` is acceptable when the element type is obvious; name it when it is not | Provide examples of ambiguous `it` usage |

### SBPP-FMT-07:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT07-1** | Kotlin single-parameter lambdas SHOULD use `it` when the element type is obvious from context. | Reduces noise |
| **CC-FMT07-2** | Named parameters MUST be used in nested lambdas to distinguish outer and inner elements. | Prevents ambiguity |
| **CC-FMT07-3** | Java iteration parameters SHOULD use a lowercase version of the element's type/role name (`policy`, `claim`). | Communicates element type |
| **CC-FMT07-4** | Named parameters SHALL be used when the lambda body exceeds 2 lines. | Readability |

### SBPP-FMT-07:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: `it` in nested lambdas (Kotlin)**
`portfolios.forEach { it.policies.forEach { process(it) } }` — the inner `it` is ambiguous.
Fix: `portfolios.forEach { portfolio -> portfolio.policies.forEach { policy -> process(policy) } }`.

**Anti-pattern 2: Completely anonymous Java lambda parameter**
`policies.stream().map(p -> p.getPremium())` — for a simple one-liner, `p` is acceptable;
but `policies.stream().map(x -> x.getPremium())` where `x` conveys nothing — Fix: `policy`.

### SBPP-FMT-07:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| `it` keeps simple lambdas terse | Can be ambiguous in nested context — use named parameter |
| Named parameters document element role | Slightly more verbose — justified for complex bodies |

### SBPP-FMT-07:10 - Rationale

Beck's `each` convention mapped to "the current element" in iteration. In Kotlin, `it`
serves this role for simple lambdas; named parameters serve it for complex ones. The
adaptation respects both the "concise for simple" and "explicit for complex" principles.

### SBPP-FMT-07:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Kotlin Coding Conventions (JetBrains, post-2016):** Use `it` for simple lambdas;
name the parameter when it is used multiple times or the lambda is long. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Variable names should be proportional to their scope —
short scope (single lambda) can have short names. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin Coding Conventions (post-2016) | `it` for simple; named for complex | **Adopt** |
| Clean Code (Martin, ongoing) | Proportional naming | **Adopt** |

### SBPP-FMT-07:12 - Relations

* **Appears in:** SBPP-COL-15 through COL-20 (enumeration patterns — `it` / named param is the iteration variable)
* **Named version follows:** SBPP-FMT-02 (Type Suggesting Parameter Name — applies to named lambda params too)
* **Contrasts with:** SBPP-STA-15 (Temporary Variable — lambda parameter has narrower scope than a temp var)

### SBPP-FMT-07:End
