## SBPP-COL-28 - Concatenating Stream

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-28:1 - Problem frame

Building a string or output from many small pieces by repeated concatenation with `+` is
O(n²) in total characters. Using `StringBuilder` (Java) or `buildString` (Kotlin) avoids
the copies. The pattern is about choosing the right string-building mechanism.

### SBPP-COL-28:2 - Problem

How do you concatenate many string pieces or collections efficiently, without creating
many intermediate copies?

### SBPP-COL-28:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | `StringBuilder` O(n) vs `+` O(n²) ↔ for few pieces, `+` is fine |
| **Readability** | String templates (`${}` in Kotlin) are most readable ↔ not always sufficient |
| **Flexibility** | `StringBuilder` handles conditional/loop-based building | |

### SBPP-COL-28:4 - Solution — Use `StringBuilder` (Java) or `buildString` / string templates (Kotlin) for multi-piece assembly

**Java:**

```java
// ✅ For 3+ pieces in a loop — StringBuilder
public String buildReport(List<Policy> policies) {
    StringBuilder sb = new StringBuilder();
    sb.append("Policy Report
");
    sb.append("=============
");
    for (Policy policy : policies) {
        sb.append(policy.getId()).append(": ")
          .append(policy.getPremium().toDisplayString()).append('
');
    }
    return sb.toString();
}

// ✅ Stream joining — Collectors.joining()
String ids = policies.stream()
    .map(p -> p.getId().toString())
    .collect(Collectors.joining(", ", "[", "]"));
// Result: [P001, P002, P003]

// ✅ String.format / formatted() for structured output
String header = "Policy %s: %s premium".formatted(policy.getId(), policy.getPremium());
```

**Kotlin:**

```kotlin
// ✅ buildString — idiomatic Kotlin
fun buildReport(policies: List<Policy>): String = buildString {
    appendLine("Policy Report")
    appendLine("=============")
    policies.forEach { policy ->
        appendLine("${policy.id}: ${policy.premium.toDisplayString()}")
    }
}

// ✅ joinToString — Kotlin equivalent of Collectors.joining
val ids = policies.joinToString(separator = ", ", prefix = "[", postfix = "]") { it.id.toString() }

// ✅ String template for simple cases
val header = "Policy ${policy.id}: ${policy.premium} premium"
```

### SBPP-COL-28:5 - Archetypal Grounding

**U.System:** `policies.joinToString(", ")` — collects all policy ID strings with commas in one expression.
**U.Episteme:** Kotlin's `buildString {}` eliminates the builder construction and `.toString()` call — the DSL is the string builder.

### SBPP-COL-28:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Modern Java compiler optimises adjacent `+` operations — `"a" + "b" + "c"` is already efficient | Only use StringBuilder explicitly for loops; compiler handles fixed-count concatenation |
| **Arch** | `StringBuilder` is not thread-safe; `StringBuffer` is thread-safe but rarely needed | Use `StringBuilder` for single-thread; avoid `StringBuffer` |
| **Onto/Epist** | `Collectors.joining()` is the functional equivalent of `StringBuilder` for streams | Use `Collectors.joining()` when already in a stream pipeline |
| **Prag** | Kotlin `buildString`, `joinToString`, string templates cover 99% of string building | Rarely need explicit `StringBuilder` in Kotlin |
| **Did** | Teach the O(n²) `+` in loop problem; demonstrate with StringBuilder | |

### SBPP-COL-28:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL28-1** | String concatenation in loops SHALL use `StringBuilder` (Java) or `buildString {}` (Kotlin). | O(n) vs O(n²) |
| **CC-COL28-2** | Stream-based string joining SHALL use `Collectors.joining()` (Java) or `joinToString()` (Kotlin). | Functional idiom |
| **CC-COL28-3** | Simple few-piece concatenation MAY use `+` or string templates. | Readability for small cases |

### SBPP-COL-28:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `String result = ""; for (Policy p : policies) result += p.toString();` — O(n²). Fix: `StringBuilder`.
**Anti-pattern 2:** Creating a new `StringBuilder` for a 2-piece concatenation. Fix: just use `+`.

### SBPP-COL-28:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(n) string building vs O(n²) | StringBuilder is slightly more verbose |
| `joinToString` / `Collectors.joining` for collection-to-string | — |

### SBPP-COL-28:10 - Rationale

Beck's Concatenating Stream pattern addresses O(n²) string concatenation. In Java/Kotlin,
`StringBuilder`, `Collectors.joining()`, and Kotlin's `buildString`/`joinToString` are the
idiomatic solutions.

### SBPP-COL-28:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `Collectors.joining()` (post-2014):** Stream-based string joining. *Adopt.*
**Kotlin `buildString`/`joinToString` (post-2016):** Idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ `Collectors.joining()` | Stream joining | **Adopt** |
| Kotlin `buildString`/`joinToString` (post-2016) | Idiomatic | **Adopt** |

### SBPP-COL-28:12 - Relations

* **Pairs with:** SBPP-COL-27 (Parsing Stream — parsing is the inverse of building)
* **Solves:** O(n²) concatenation in loops

### SBPP-COL-28:End
