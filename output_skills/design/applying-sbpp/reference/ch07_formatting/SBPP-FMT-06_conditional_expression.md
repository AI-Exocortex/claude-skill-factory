## SBPP-FMT-06 - Conditional Expression

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-FMT-06:1 - Problem frame

When both branches of a conditional assign to the same variable or return a value, the
conditional is not "a path of control" but "a choice of value". Expressing it as an
expression — rather than two assignment statements — makes the intent clearer and
often eliminates the variable entirely.

### SBPP-FMT-06:2 - Problem

How do you format conditionals where both branches produce the same kind of result
(assignment or return) so that the "selecting a value" intent is directly expressed?

### SBPP-FMT-06:3 - Forces

| Force | Tension |
|-------|---------|
| **Intent clarity** | Expression form communicates "choosing a value" ↔ statement form communicates "two execution paths" |
| **Immutability** | Expression form enables `final`/`val` assignment ↔ statement form requires mutable variable |
| **Readability** | Ternary `? :` is compact ↔ can be cryptic for complex conditions |

### SBPP-FMT-06:4 - Solution — Use ternary, `when`, or expression-form `if` to communicate value selection; factor assignment outside the conditional

**Java — ternary for simple two-way selection:**

```java
// ❌ Statement form — two assignment paths obscure the "select a value" intent
Money premium;
if (policy.isActive()) {
    premium = ratingEngine.calculate(policy);
} else {
    premium = Money.ZERO;
}

// ✅ Expression form — communicates "select one of two values"
Money premium = policy.isActive()
    ? ratingEngine.calculate(policy)
    : Money.ZERO;

// ✅ Even cleaner — assign to final
final Money premium = policy.isActive()
    ? ratingEngine.calculate(policy)
    : Money.ZERO;
```

**Java — inline ternary for simple one-liners:**

```java
// ✅ Simple condition + simple values → one line
String label = policy.isActive() ? "Active" : "Inactive";
Money effective = override != null ? override : defaultPremium;
```

**Java 21+ — pattern-matching switch expression (multi-way selection):**

```java
// ✅ switch expression selects a value
String description = switch (policy.getStatus()) {
    case ACTIVE    -> "Active policy";
    case EXPIRED   -> "Renewal available";
    case CANCELLED -> "No further action";
};
```

**Kotlin — `if` is an expression:**

```kotlin
// ✅ Kotlin if-expression: assigns the chosen value to premium
val premium = if (policy.isActive) ratingEngine.calculate(policy) else Money.ZERO

// ✅ Multi-line when needed
val premium = if (policy.isActive) {
    ratingEngine.calculate(policy)
} else {
    Money.ZERO
}

// ✅ when expression (multi-way)
val description = when (policy.status) {
    PolicyStatus.ACTIVE    -> "Active policy"
    PolicyStatus.EXPIRED   -> "Renewal available"
    PolicyStatus.CANCELLED -> "No further action"
}

// ✅ Eliminating the conditional entirely (Boolean case)
val isEmpty = collection.isEmpty     // NOT: val isEmpty = if (collection.isEmpty) true else false
```

**Factor out duplication from both branches:**

```java
// ❌ Duplicated assignment in both branches
if (policy.isActive()) {
    result = new PolicySummary(policy.getId(), calculatePremium(policy));
} else {
    result = new PolicySummary(policy.getId(), Money.ZERO);
}

// ✅ Factor out the shared structure
Money premium = policy.isActive() ? calculatePremium(policy) : Money.ZERO;
PolicySummary result = new PolicySummary(policy.getId(), premium);
```

### SBPP-FMT-06:5 - Archetypal Grounding

**U.System:** `val premium = if (policy.isActive) calculate(policy) else Money.ZERO` — the
`val` keyword makes immutability explicit; the expression form makes "selecting a value" intent clear.

**U.Episteme:** When you see both branches of a conditional assigning to the same variable,
that is the signal to refactor into an expression. The code is not "choosing a path"; it is
"choosing a value." The expression form encodes this distinction.

### SBPP-FMT-06:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Conditional value selection formatting in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Complex conditions inside a ternary reduce readability | Extract condition to a named boolean variable or method: `val isEligible = ...; val premium = if (isEligible) ...` |
| **Arch** | Expression form enables `final`/`val` (immutable) — a structural benefit beyond formatting | Always prefer `final`/`val`; expression form makes this natural |
| **Onto/Epist** | Kotlin `if` is already an expression; Java added switch expressions in Java 14 — the language supports this directly | Use language-native expression forms; avoid ternary chains |
| **Prag** | Nested ternary `a ? b : c ? d : e` is never acceptable | Use `when`/switch expression for multi-way; never chain ternary |
| **Did** | Show the elimination step: `val isEmpty = collection.isEmpty()` not `val isEmpty = if (...) true else false` | Teach: if both branches return Boolean, eliminate the conditional entirely |

### SBPP-FMT-06:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT06-1** | When both branches of a conditional produce the same kind of result, the expression form SHALL be used. | Communicates "value selection" intent |
| **CC-FMT06-2** | Assignment SHALL be factored outside the conditional when both branches assign to the same variable. | Enables `final`/`val` |
| **CC-FMT06-3** | Boolean conditionals of the form `if (x) true else false` SHALL be simplified to `x`. | Eliminates redundant conditional |
| **CC-FMT06-4** | Multi-way conditional expressions SHALL use `when` (Kotlin) or switch expression (Java 14+). | Avoids ternary chains |

### SBPP-FMT-06:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Boolean conditional**
`val active = if (status == ACTIVE) true else false` — Fix: `val active = status == ACTIVE`.

**Anti-pattern 2: Nested ternary**
`a ? b : c ? d : e` — unreadable. Fix: `when`/switch expression.

**Anti-pattern 3: Shared structure not factored out**
Both branches build `new PolicySummary(policy.getId(), ...)` with only the premium differing.
Fix: extract the varying part, build once.

### SBPP-FMT-06:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| `final`/`val` becomes natural — immutability as default | Complex conditions must be extracted to remain readable |
| Intent ("selecting a value") made explicit | — |
| Kotlin `when` eliminates all ternary chains | — |

### SBPP-FMT-06:10 - Rationale

Beck's Conditional Expression is one of the cleanest patterns in the book. In Java/Kotlin it
maps perfectly: `if` is an expression in Kotlin (always), and in Java via ternary or switch
expressions (Java 14+). The principle — "when both branches assign to the same variable,
factor the assignment out" — enables immutable `val`/`final` declarations and directly
communicates "value selection" intent.

### SBPP-FMT-06:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Kotlin language spec — `if` as expression (JetBrains, post-2016):** `if` always returns a
value in Kotlin. This makes Conditional Expression the language default. *Adopt.*

**Java 14+ switch expressions (JEP 361, 2020):** Java gains expression-form switch.
Multi-way Conditional Expressions are now first-class in Java. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 9 ("Prefer try-with-resources to try-finally")
exemplifies the expression-over-statement preference pervasive in modern Java. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin `if`-as-expression (post-2016) | Language-native | **Adopt** |
| Java 14+ switch expression (JEP 361, 2020) | Multi-way expression | **Adopt** |
| Kotlin `when` expression (post-2016) | Multi-way | **Adopt** |

### SBPP-FMT-06:12 - Relations

* **Enables:** Immutable `final`/`val` declarations
* **Eliminates:** Mutable variable + two-branch assignment pattern
* **Relates to:** SBPP-BEH-07 (Query Method — the condition uses query methods)
* **Relates to:** SBPP-FMT-05 (Guard Clause — complementary: guard for exclusion, expression for selection)

### SBPP-FMT-06:End
