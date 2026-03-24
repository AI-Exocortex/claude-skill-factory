## SBPP-COL-26 - Lookup Cache

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-26:1 - Problem frame

When a `detect` or `filter` operation on a collection is called frequently on the same
data with the same search key, repeating the O(n) scan wastes time. Adding a `Map`
cache converts repeated O(n) searches to O(1) lookups.

### SBPP-COL-26:2 - Problem

How do you optimise repeated searches against a collection by a specific attribute,
without changing the canonical representation of the data?

### SBPP-COL-26:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | O(1) cached lookup vs O(n) scan ↔ cache must be kept consistent with source |
| **Memory** | Cache uses additional memory ↔ lookup performance improves |
| **Consistency** | Cache must be invalidated when source data changes ↔ complexity |

### SBPP-COL-26:4 - Solution — Build a derived `Map` index lazily or eagerly; or use `computeIfAbsent`

**Java — eager index (build once):**

```java
public class PolicyPortfolio {
    private final List<Policy> policies;
    // Derived index — built once, used for fast lookup
    private final Map<PolicyId, Policy> byId;
    private final Map<String, List<Policy>> byHolder;

    public PolicyPortfolio(List<Policy> policies) {
        this.policies = List.copyOf(policies);
        this.byId = policies.stream()
            .collect(Collectors.toMap(Policy::getId, p -> p));
        this.byHolder = policies.stream()
            .collect(Collectors.groupingBy(Policy::getHolderId));
    }

    public Optional<Policy> findById(PolicyId id) {
        return Optional.ofNullable(byId.get(id));       // O(1)
    }

    public List<Policy> findByHolder(String holderId) {
        return byHolder.getOrDefault(holderId, List.of()); // O(1)
    }
}
```

**Java — lazy cache with `computeIfAbsent`:**

```java
public class RateCache {
    private final Map<CacheKey, Money> cache = new HashMap<>();

    public Money getRate(RiskCode risk, Region region) {
        CacheKey key = new CacheKey(risk, region);
        return cache.computeIfAbsent(key, k -> rateService.calculateRate(k.risk(), k.region()));
    }
}
```

**Kotlin:**

```kotlin
class PolicyPortfolio(policies: List<Policy>) {
    private val policies: List<Policy> = policies.toList()
    private val byId: Map<PolicyId, Policy> = policies.associateBy { it.id }
    private val byHolder: Map<String, List<Policy>> = policies.groupBy { it.holderId }

    fun findById(id: PolicyId): Policy? = byId[id]                    // O(1)
    fun findByHolder(holderId: String): List<Policy> = byHolder[holderId] ?: emptyList()
}

// Lazy cache with Kotlin delegates
class RateService {
    private val cache = mutableMapOf<CacheKey, Money>()
    fun getRate(risk: RiskCode, region: Region): Money =
        cache.getOrPut(CacheKey(risk, region)) { calculateRate(risk, region) }
}
```

### SBPP-COL-26:5 - Archetypal Grounding

**U.System:** `byId.get(id)` in `PolicyPortfolio` — O(1) policy lookup; the underlying list unchanged.
**U.Episteme:** The Map index is derived data — built from the canonical list, consistent because the list is immutable. When the list changes, the index is rebuilt.

### SBPP-COL-26:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Cache invalidation is hard — must be kept consistent with source | Build index once from immutable source; rebuild on source change |
| **Arch** | Cache doubles memory usage | Profile first; apply only when O(n) scan is measured as a bottleneck |
| **Onto/Epist** | `computeIfAbsent` is not thread-safe in `HashMap` | Use `ConcurrentHashMap.computeIfAbsent` for concurrent caches |
| **Prag** | Kotlin `getOrPut` is `computeIfAbsent` equivalent | Use `getOrPut` in Kotlin |
| **Did** | The index-as-derived-data pattern is powerful and broadly applicable | |

### SBPP-COL-26:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL26-1** | Lookup caches SHALL be derived from an immutable source collection (built once, never partially updated). | Consistency |
| **CC-COL26-2** | Concurrent lookup caches SHALL use `ConcurrentHashMap.computeIfAbsent()`. | Thread safety |
| **CC-COL26-3** | Cache usage SHOULD only be applied after profiling confirms the O(n) scan is a bottleneck. | Avoids premature optimisation |

### SBPP-COL-26:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Partially updating the cache instead of rebuilding. Fix: treat cache as derived from immutable source; rebuild completely.
**Anti-pattern 2:** `HashMap.computeIfAbsent` in concurrent code. Fix: `ConcurrentHashMap.computeIfAbsent`.

### SBPP-COL-26:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(1) lookup from O(n) scan | Extra memory; consistency complexity |
| `associateBy`/`groupBy` build the index in one line | Cache invalidation must be designed carefully |

### SBPP-COL-26:10 - Rationale

Beck's Lookup Cache converts a repeated scan into a derived index. Kotlin's `associateBy`
and `groupBy` make building the index one-line operations. The pattern is safe when applied
to immutable source data.

### SBPP-COL-26:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Guava `CacheBuilder` / Caffeine (post-2015):** Production-grade caches with TTL, max-size,
eviction. Use for external service caches. *Adopt for complex caches.*

**Kotlin `associateBy` / `groupBy` (post-2016):** Build index maps in one expression. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Caffeine cache (post-2015) | Production cache library | **Adopt** for complex caches |
| Kotlin `associateBy`/`groupBy` | Index building | **Adopt** |

### SBPP-COL-26:12 - Relations

* **Implements:** Index/Derived-data pattern
* **Specialises:** SBPP-COL-07 (Dictionary — the cache is a Map)
* **Applies when:** SBPP-COL-19 (Detect) is repeatedly called on the same collection

### SBPP-COL-26:End
