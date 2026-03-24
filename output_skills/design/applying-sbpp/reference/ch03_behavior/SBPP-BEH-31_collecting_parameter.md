## SBPP-BEH-31 - Collecting Parameter

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-31:1 - Problem frame

When a Composed Method (BEH-01) is broken into smaller methods, a common need arises:
accumulating results across the steps. Returning a result from each step and combining
them at the top level can be awkward. Passing a collection as a parameter that each step
fills solves this — the collecting parameter threads through the decomposed steps.

### SBPP-BEH-31:2 - Problem

How do you accumulate results from several methods that collaborate on building a collection,
without making the top-level method responsible for merging all intermediate results?

### SBPP-BEH-31:3 - Forces

| Force | Tension |
|-------|---------|
| **Decomposition** | Want to split building logic across methods ↔ each method needs access to the accumulator |
| **Purity** | Pure functions return their result ↔ passing a mutable collection introduces shared state |
| **Readability** | Accumulator threading is explicit ↔ functional fold/reduce is often cleaner |

### SBPP-BEH-31:4 - Solution — Pass a mutable collection to methods that fill it; OR use functional fold

In Java/Kotlin, prefer the functional approach (streams, fold) when possible. Use the
mutable collecting parameter when the accumulation logic is complex enough to warrant
decomposed methods.

**Java example — collecting parameter:**

```java
public List<ValidationError> validate(PolicyRequest request) {
    List<ValidationError> errors = new ArrayList<>();  // collecting parameter
    validateCustomerDetails(request.getCustomer(), errors);
    validateCoverageItems(request.getItems(), errors);
    validateRegulatoryRequirements(request, errors);
    return errors;
}

private void validateCustomerDetails(CustomerDetails customer, List<ValidationError> errors) {
    if (customer.getDateOfBirth() == null) errors.add(ValidationError.of("DOB_REQUIRED"));
    if (customer.getName().isBlank())      errors.add(ValidationError.of("NAME_REQUIRED"));
}

private void validateCoverageItems(List<CoverageItem> items, List<ValidationError> errors) {
    if (items.isEmpty()) errors.add(ValidationError.of("COVERAGE_REQUIRED"));
    items.stream().filter(i -> i.getSumInsured().isZero())
         .map(i -> ValidationError.of("ZERO_SUM_INSURED", i.getCode()))
         .forEach(errors::add);
}
```

**Java — functional alternative (preferred for simple accumulations):**

```java
public List<ValidationError> validate(PolicyRequest request) {
    return Stream.of(
        validateCustomerDetails(request.getCustomer()),    // returns Stream<ValidationError>
        validateCoverageItems(request.getItems()),
        validateRegulatoryRequirements(request)
    ).flatMap(Function.identity()).collect(toList());
}

private Stream<ValidationError> validateCustomerDetails(CustomerDetails c) { ... }
```

**Kotlin:**

```kotlin
fun validate(request: PolicyRequest): List<ValidationError> =
    buildList {
        addAll(validateCustomerDetails(request.customer))
        addAll(validateCoverageItems(request.items))
        addAll(validateRegulatoryRequirements(request))
    }

// Each validator returns a list; no shared mutable state
private fun validateCustomerDetails(c: CustomerDetails): List<ValidationError> = buildList {
    if (c.dateOfBirth == null) add(ValidationError("DOB_REQUIRED"))
    if (c.name.isBlank())      add(ValidationError("NAME_REQUIRED"))
}
```

**Rule:** Prefer Kotlin's `buildList {}` and Java's `Stream.flatMap` over a mutable
collecting parameter. Use the mutable form only when the logic is too complex for
a functional approach.

### SBPP-BEH-31:5 - Archetypal Grounding

**U.System:** `validate()` delegates to three validation methods, all contributing to one `errors` list.
**U.Episteme:** The collecting parameter makes the accumulation contract explicit — each method knows it should add to, not replace, the errors list.

### SBPP-BEH-31:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Mutable shared parameter is an implicit contract | Document in Javadoc: "adds to the provided list, does not clear it" |
| **Arch** | Mutable collecting parameter creates action-at-a-distance | Prefer functional fold/flatMap; use mutable only when necessary |
| **Onto/Epist** | Kotlin `buildList {}` eliminates the mutable parameter while preserving the decomposition | Prefer `buildList {}` in Kotlin |
| **Prag** | Java Stream `flatMap` makes the functional version clean for simple cases | Use functional default; fall back to collecting parameter for complex multi-step logic |
| **Did** | The mutable form is easier to understand for beginners; functional form is more idiomatic | Teach both; note the functional form as the preferred target |

### SBPP-BEH-31:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH31-1** | In Kotlin, `buildList {}` SHOULD be preferred over a mutable collecting parameter. | Idiomatic and side-effect free |
| **CC-BEH31-2** | In Java, `Stream.flatMap` SHOULD be preferred for simple accumulations. | Functional clarity |
| **CC-BEH31-3** | When a mutable collecting parameter is used, each called method SHALL only add to the collection, never clear or replace it. | Prevents accidental data loss |

### SBPP-BEH-31:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Clearing the collecting parameter**
A helper method calls `errors.clear()` before adding its errors — erasing earlier steps.
Fix: Methods only add; they never clear.

**Anti-pattern 2: Returning the collecting parameter**
`return errors;` from a helper when `void` is correct.
Fix: The top-level method owns the list; helpers only contribute to it.

### SBPP-BEH-31:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Decomposed accumulation without complex return types | Mutable shared state — prefer functional alternative |
| Each validator/builder step is independently testable | Kotlin `buildList` eliminates the mutable concern |
| Clean composition of partial results | — |

### SBPP-BEH-31:10 - Rationale

Collecting Parameter is Beck's solution for accumulating results across a decomposed method.
In modern Java/Kotlin, the functional alternatives (`buildList`, `flatMap`, `fold`) are
usually cleaner. The mutable collecting parameter remains valid for complex multi-step
logic where the functional approach would be harder to read.

### SBPP-BEH-31:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Kotlin `buildList {}` (post-2019):** Standard library function that replaces the mutable
collecting parameter pattern with a clean DSL. *Adopt for Kotlin.*

**Java Stream flatMap (Java 8+):** Functional accumulation without mutable collections. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 46 — prefer functional-style operations when
working with streams. *Adopt: prefer functional over mutable collecting parameter.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin `buildList {}` (post-2019) | Replaces mutable collecting parameter | **Adopt** |
| Java 8+ Stream `flatMap` | Functional accumulation | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Prefer functional operations | **Adopt** |

### SBPP-BEH-31:12 - Relations

* **Enables:** SBPP-BEH-01 (Composed Method — collecting parameter solves accumulation across decomposed steps)
* **Alternative to:** Return-value composition in each step
* **Relates to:** SBPP-BEH-10 (Method Object — intermediate state alternative)
* **Superseded by:** Kotlin `buildList {}` and Java Stream `flatMap` in most cases

### SBPP-BEH-31:End
