## SBPP-STA-16 - Collecting Temporary Variable

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-STA-16:1 - Problem frame

When a method needs to accumulate values — summing amounts, building a list of errors,
gathering results from a loop — it needs a local variable to collect them. In modern
Java/Kotlin, functional operations (`fold`, `reduce`, `buildList`, `stream().collect()`)
often eliminate the need for an explicit collecting variable.

### SBPP-STA-16:2 - Problem

How do you gradually accumulate intermediate results within a method, and when should
you use an explicit collecting variable versus a functional approach?

### SBPP-STA-16:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Named accumulator is explicit ↔ functional fold is more concise |
| **Mutability** | Collecting variable is mutable ↔ functional approach avoids mutation |
| **Complexity** | Simple accumulation suits functional ↔ complex multi-source accumulation suits explicit variable |

### SBPP-STA-16:4 - Solution — Use functional fold/reduce for simple accumulation; use explicit variable only for complex multi-source collection

**Java — prefer Stream:**

```java
// ✅ Functional — no explicit collecting variable needed
Money totalPremium = policies.stream()
    .map(Policy::getPremium)
    .reduce(Money.ZERO, Money::add);

List<ValidationError> errors = Stream.of(
    validateCustomer(request.customer()),
    validateCoverage(request.items()),
    validateRegulatory(request)
).flatMap(Collection::stream).collect(toList());
```

**Java — explicit collecting variable for complex cases:**

```java
// ✅ Explicit collecting variable when accumulation is complex
List<ValidationError> errors = new ArrayList<>();
if (request.getCustomer() == null)    errors.add(ValidationError.of("CUSTOMER_REQUIRED"));
if (request.getItems().isEmpty())     errors.add(ValidationError.of("COVERAGE_REQUIRED"));
if (request.getPremium().isZero())    errors.add(ValidationError.of("PREMIUM_ZERO"));
request.getItems().stream()
    .filter(i -> i.getSumInsured().isZero())
    .map(i -> ValidationError.of("ZERO_SUM_INSURED", i.getCode()))
    .forEach(errors::add);
return errors;
```

**Kotlin — `buildList` eliminates the mutable variable:**

```kotlin
// ✅ buildList — collecting without mutable variable
val errors = buildList {
    if (request.customer == null) add(ValidationError("CUSTOMER_REQUIRED"))
    if (request.items.isEmpty())  add(ValidationError("COVERAGE_REQUIRED"))
    request.items.filter { it.sumInsured.isZero() }
                 .forEach { add(ValidationError("ZERO_SUM_INSURED", it.code)) }
}

// ✅ fold for monetary accumulation
val total = policies.fold(Money.ZERO) { acc, p -> acc + p.premium }
```

### SBPP-STA-16:5 - Archetypal Grounding

**U.System:** Kotlin `buildList { }` collects validation errors without a visible mutable variable — the collector is implicit.
**U.Episteme:** The functional form makes the accumulation intent explicit through the operator name (`fold`, `reduce`).

### SBPP-STA-16:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Accumulation in Java/Kotlin methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Mutable collecting variable can be accidentally cleared or reassigned | Declare `final` in Java; use `buildList` in Kotlin |
| **Arch** | Functional `collect` is idiomatic Java/Kotlin; explicit variable is Java 7 style | Prefer functional; use explicit only when complex |
| **Onto/Epist** | `buildList` in Kotlin is less obvious to developers new to it | Teach as the idiomatic Kotlin pattern |
| **Prag** | `buildList` (Kotlin 1.6+), `stream().collect()` cover 90% of cases | Apply the 90% rule; fall back to explicit only when needed |
| **Did** | Start with explicit collecting variable for teaching; upgrade to functional | Show both, explain trade-offs |

### SBPP-STA-16:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA16-1** | Simple accumulation (sum, count, collect-all) SHALL use functional operations. | Idiomatic |
| **CC-STA16-2** | Kotlin collecting SHOULD use `buildList {}`, `buildMap {}`, or `fold`. | Avoids mutable variable |
| **CC-STA16-3** | When explicit collecting variable is used, it SHALL be `final` in Java. | Prevents reassignment |

### SBPP-STA-16:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Mutable collecting variable where functional works**
```java
List<String> names = new ArrayList<>();
policies.forEach(p -> names.add(p.getHolderName()));  // ← functional preferred
```
Fix: `policies.stream().map(Policy::getHolderName).collect(toList())`.

### SBPP-STA-16:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| `buildList` / functional forms avoid mutable state | Functional form requires familiarity |
| Named collecting variable makes multi-source accumulation readable | Mutable variable — declare final |

### SBPP-STA-16:10 - Rationale

The functional alternatives (`stream().collect()`, Kotlin `buildList`, `fold`) directly supersede
the mutable collecting variable for simple cases. The explicit variable remains valid for
complex multi-source accumulation.

### SBPP-STA-16:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Java 8 Stream `collect()` (post-2014):** Canonical functional replacement. *Adopt.*
**Kotlin `buildList` (1.6+, post-2021):** Idiomatic Kotlin collecting. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8 Stream `collect()` | Functional accumulation | **Adopt** |
| Kotlin `buildList` (post-2021) | Mutable-free collection | **Adopt** |

### SBPP-STA-16:12 - Relations

* **Specialises:** SBPP-STA-15 (Temporary Variable)
* **Modern replacements:** Java Stream `collect()`, Kotlin `buildList`/`fold`
* **Relates to:** SBPP-BEH-31 (Collecting Parameter — cross-method version)

### SBPP-STA-16:End
