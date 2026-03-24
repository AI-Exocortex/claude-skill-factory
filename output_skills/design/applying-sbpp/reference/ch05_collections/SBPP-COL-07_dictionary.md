## SBPP-COL-07 - Dictionary

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-07:1 - Problem frame

When data needs to be looked up by a meaningful key rather than by sequential index,
a key-value map is required. In Java/Kotlin, `Map<K,V>` serves this role. Choosing the
right Map implementation and using it idiomatically determines performance, thread
safety, and readability of lookup-heavy code.

### SBPP-COL-07:2 - Problem

How do you map one kind of object to another so that values can be efficiently retrieved
by key, without depending on sequential position?

### SBPP-COL-07:3 - Forces

| Force | Tension |
|-------|---------|
| **Lookup performance** | `HashMap` O(1) vs `TreeMap` O(log n) ↔ `TreeMap` provides sorted key iteration |
| **Key requirements** | Keys must implement `equals`/`hashCode` (HashMap) or be `Comparable` (TreeMap) |
| **Mutability** | Mutable map during construction ↔ immutable map for sharing |

### SBPP-COL-07:4 - Solution — Use `Map.of()` for small immutable maps; `HashMap` for dynamic maps; declare as `Map<K,V>`

Declare fields and parameters as `Map<K,V>`. Choose the implementation based on ordering
and mutability needs.

**Java example:**

```java
// Immutable small map — prefer Map.of()
Map<RiskCode, BigDecimal> rateTable = Map.of(
    RiskCode.FIRE,   BigDecimal.valueOf(0.15),
    RiskCode.THEFT,  BigDecimal.valueOf(0.08),
    RiskCode.FLOOD,  BigDecimal.valueOf(0.12)
);

// Dynamic accumulation — HashMap, then seal
Map<PolicyId, RatingResult> results = new HashMap<>();
policies.forEach(p -> results.put(p.getId(), ratingEngine.rate(p)));
Map<PolicyId, RatingResult> sealed = Map.copyOf(results);   // immutable

// Sorted key iteration — TreeMap
Map<LocalDate, List<Policy>> byStartDate = new TreeMap<>();

// Null-safe lookup idiom
BigDecimal rate = rateTable.getOrDefault(riskCode, BigDecimal.ZERO);

// Compute if absent
Map<String, List<Policy>> byHolder = new HashMap<>();
byHolder.computeIfAbsent(holderId, k -> new ArrayList<>()).add(policy);
```

**Kotlin example:**

```kotlin
// Immutable map
val rateTable: Map<RiskCode, BigDecimal> = mapOf(
    RiskCode.FIRE  to BigDecimal("0.15"),
    RiskCode.THEFT to BigDecimal("0.08")
)

// Dynamic accumulation
val results = mutableMapOf<PolicyId, RatingResult>()
policies.forEach { results[it.id] = ratingEngine.rate(it) }

// Kotlin grouped maps
val byHolder: Map<String, List<Policy>> = policies.groupBy { it.holderId }
val premiumByCategory: Map<String, Money> = policies
    .groupBy { it.category }
    .mapValues { (_, ps) -> ps.map { it.premium }.reduce(Money::add) }
```

**Map implementation selector:**

| Need | Java | Kotlin |
|------|------|--------|
| Fast lookup, order unimportant | `HashMap` / `Map.of()` | `hashMapOf()` / `mapOf()` |
| Preserve insertion order | `LinkedHashMap` | `linkedMapOf()` |
| Sorted by key | `TreeMap` | `sortedMapOf()` |
| Immutable | `Map.of()` / `Map.copyOf()` | `mapOf()` |
| Concurrent access | `ConcurrentHashMap` | `ConcurrentHashMap` |

### SBPP-COL-07:5 - Archetypal Grounding

**U.System:** `Map<RiskCode, BigDecimal>` rate table — O(1) lookup by risk code during premium calculation.
**U.Episteme:** `policies.groupBy { it.holderId }` in Kotlin produces a `Map<String, List<Policy>>`
in one expression — the groupBy higher-order function eliminates the manual accumulation loop.

### SBPP-COL-07:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Map usage in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Maps are mutable by default in Java — easy to accidentally modify shared state | Use `Map.copyOf()` when sharing; prefer `Map.of()` for constants |
| **Arch** | `HashMap` with a poor `hashCode` on keys degrades to O(n) | Use records/data classes for keys; test with realistic data volumes |
| **Onto/Epist** | Map keys must be immutable; mutable keys cause "lost entry" bugs | Keys MUST be value objects (immutable) |
| **Prag** | Kotlin's `groupBy`, `associateBy`, `mapValues` eliminate most manual map-building loops | Prefer higher-order functions over imperative `for` loops |
| **Did** | `computeIfAbsent` vs `getOrDefault` vs `putIfAbsent` — semantics are easy to confuse | Establish team idioms; use Kotlin's cleaner API when possible |

### SBPP-COL-07:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL07-1** | Map keys MUST be immutable objects with correct `equals`/`hashCode`. | Prevents lost-entry bugs |
| **CC-COL07-2** | Map fields and parameters SHALL be declared as `Map<K,V>`, not `HashMap<K,V>`. | API abstraction |
| **CC-COL07-3** | Maps returned from domain methods SHOULD be immutable (`Map.copyOf()` / Kotlin read-only). | Mutation safety |
| **CC-COL07-4** | In Kotlin, `groupBy`, `associateBy`, `mapValues` SHOULD be preferred over imperative accumulation. | Idiomatic Kotlin |

### SBPP-COL-07:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Mutable key in HashMap**
Using a mutable class as a Map key — after mutation, the entry cannot be found.
Fix: map keys must be value objects (immutable); use records/data classes.

**Anti-pattern 2: Null handling via `get()` without null check**
`map.get(key).doSomething()` — NPE if key absent. Fix: `map.getOrDefault(key, defaultVal)` or `map.get(key)?.doSomething()` (Kotlin).

### SBPP-COL-07:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(1) key-based lookup for HashMap | Key must implement equals/hashCode |
| `mapOf()` in Kotlin is concise and immutable | `Map.of()` in Java throws on null keys/values |
| `groupBy`, `associateBy` eliminate boilerplate | — |

### SBPP-COL-07:10 - Rationale

Beck's Dictionary pattern maps directly to Java/Kotlin `Map`. The modern addition is
Kotlin's rich collection transformation API (`groupBy`, `associateBy`) which eliminates
the imperative loop-and-accumulate pattern that was standard in Smalltalk and early Java.

### SBPP-COL-07:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 64 (use interface types for maps).
Items 10-11 (keys need correct equals/hashCode). *Adopt.*

**Kotlin collection operations (JetBrains, post-2016):** `groupBy`, `associateBy`, `mapValues`
replace imperative map-building. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Items 64, 10-11 | **Adopt** |
| Kotlin collection API (post-2016) | Higher-order map builders | **Adopt** |
| Java 9+ `Map.of()` (JEP 269) | Immutable small maps | **Adopt** |

### SBPP-COL-07:12 - Relations

* **Specialises:** SBPP-COL-01 (Collection — key-value mapping variant)
* **Requires:** SBPP-COL-05 (Equality Method), SBPP-COL-06 (Hashing Method) for keys
* **Used by:** SBPP-COL-26 (Lookup Cache — implemented as a Map)
* **Relates to:** SBPP-COL-04 (Set — Map keys form a Set)

### SBPP-COL-07:End
