## SBPP-COL-09 - Array

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-COL-09:1 - Problem frame

When the number of elements is known at creation time and will not change, a fixed-size
array is more explicit than a dynamically sized list. In Java/Kotlin, arrays have both
legitimate uses (performance-critical code, interoperability) and overuse pitfalls.

### SBPP-COL-09:2 - Problem

How do you represent a collection with a fixed number of elements, communicating that
the size is known and will not change?

### SBPP-COL-09:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | `List.of()` communicates fixed size ↔ raw arrays lack type safety with generics |
| **Performance** | Arrays have zero-overhead direct access ↔ `List` has minor boxing/wrapping overhead |
| **Type Safety** | Generic arrays are problematic in Java ↔ `List<E>` is fully generic |

### SBPP-COL-09:4 - Solution — Prefer `List.of()` for fixed collections in business code; use arrays only for primitives and interop

In Java/Kotlin business logic, `List.of()` (Java) or `listOf()` (Kotlin) communicate
fixed size more safely than raw arrays. Use arrays for primitive performance, JNI
interop, or when an array is explicitly required by an API.

**Java example:**

```java
// ✅ Fixed-size immutable list — preferred for business code
List<RiskCode> STANDARD_RISKS = List.of(
    RiskCode.FIRE, RiskCode.THEFT, RiskCode.LIABILITY
);

// ✅ Primitive array — legitimate for performance-critical numeric work
double[] rateFactors = new double[riskCodes.size()];
for (int i = 0; i < rateFactors.length; i++) {
    rateFactors[i] = rateTable.get(riskCodes.get(i));
}

// ✅ Array for API interop
String[] headerNames = new String[]{"Id", "Premium", "Status"};
csvWriter.writeHeader(headerNames);

// ❌ Object array for business logic — use List
Policy[] policies = new Policy[10];  // lose type safety and collection API
```

**Kotlin example:**

```kotlin
// ✅ Fixed immutable list (preferred)
val standardRisks: List<RiskCode> = listOf(RiskCode.FIRE, RiskCode.THEFT, RiskCode.LIABILITY)

// ✅ Primitive array for performance
val rateFactors = DoubleArray(riskCodes.size) { i -> rateTable[riskCodes[i]] ?: 0.0 }

// ✅ Array for interop
val headers: Array<String> = arrayOf("Id", "Premium", "Status")
```

### SBPP-COL-09:5 - Archetypal Grounding

**U.System:** `double[] rateFactors` — a fixed-size primitive array for a tight calculation loop where boxing overhead matters.
**U.Episteme:** `List.of(RiskCode.FIRE, RiskCode.THEFT)` communicates "these two codes are fixed by contract"; `new RiskCode[2]` does not.

### SBPP-COL-09:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Array vs List choice in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Object arrays (`Object[]`) lose generic type safety; Java creates `Object[]` for generic arrays | Avoid generic arrays; use `List<E>` for object collections |
| **Arch** | Arrays are mutable by default — no immutable array in Java | Use `List.of()` for immutable fixed collections; use `List.copyOf()` for snapshots |
| **Onto/Epist** | Array covariance in Java is unsound (`String[]` is a `Object[]`) | Avoid array subtyping; use `List<E>` |
| **Prag** | Kotlin has both `Array<T>` and primitive arrays (`IntArray`, `DoubleArray`) | Use primitive arrays for numeric work; `List<T>` for domain objects |
| **Did** | New developers from C/C++ may default to arrays for everything | Teach: default to `List`; use arrays only for primitives and interop |

### SBPP-COL-09:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL09-1** | Business domain collections SHALL use `List<E>` / `Set<E>` / `Map<K,V>`, not raw arrays. | Type safety and API richness |
| **CC-COL09-2** | Primitive arrays (`int[]`, `double[]`) MAY be used for performance-critical numeric computation. | Justified performance optimization |
| **CC-COL09-3** | Arrays SHOULD only be used when an API explicitly requires them (interop). | Minimizes unsafe array usage |

### SBPP-COL-09:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Object array for domain collections**
`Policy[] policies = new Policy[100]` — loses collection API. Fix: `List<Policy> policies`.

**Anti-pattern 2: Generic array creation**
`T[] arr = (T[]) new Object[n]` — unchecked cast. Fix: use `List<T>`.

### SBPP-COL-09:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Primitive arrays have zero boxing overhead | No generic type safety for object arrays |
| `List.of()` communicates fixed-size semantics more safely | — |

### SBPP-COL-09:10 - Rationale

Beck's Array pattern emphasises using arrays when fixed size is known. In modern Java/Kotlin,
`List.of()` / `listOf()` serve this purpose better for object collections. Arrays remain
relevant for primitive performance and API interop.

### SBPP-COL-09:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 28 ("Prefer lists to arrays") — arrays are covariant and lack generic type safety. *Adopt: use List for objects, arrays for primitives/interop.*

**Kotlin primitive arrays (post-2016):** `IntArray`, `DoubleArray` provide unboxed primitive performance. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. Item 28 (Bloch, 2018) | Prefer Lists | **Adopt** |
| Kotlin primitive arrays (post-2016) | Primitive performance | **Adopt** |

### SBPP-COL-09:12 - Relations

* **Specialises:** SBPP-COL-01 (Collection — fixed-size variant)
* **Contrast with:** SBPP-COL-02 (OrderedCollection — dynamic-size)
* **Superseded by:** `List.of()` / `listOf()` for most object collection use cases

### SBPP-COL-09:End
