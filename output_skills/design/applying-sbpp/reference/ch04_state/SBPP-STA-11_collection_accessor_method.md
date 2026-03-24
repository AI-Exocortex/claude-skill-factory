## SBPP-STA-11 - Collection Accessor Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-11:1 - Problem frame

When a domain object holds a collection (a policy's claims, an order's line items), naive
exposure via a getter hands the internal mutable collection to callers, who can then
mutate it without the owner knowing. The Collection Accessor Method pattern provides
safe, controlled access: add, remove, and query operations — but not direct collection mutation.

### SBPP-STA-11:2 - Problem

How do you provide access to a collection instance variable so that callers can work with
its elements without being able to directly mutate, replace, or iterate in ways the
owning object hasn't sanctioned?

### SBPP-STA-11:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Hide internal collection type and structure ↔ callers need to add/remove/query |
| **Invariant Safety** | Owner controls when items are added/removed ↔ callers expect free mutation |
| **Performance** | Defensive copy is safe ↔ unmodifiable view is O(1) but may surprise callers |

### SBPP-STA-11:4 - Solution — Expose add, remove, and query methods; return an unmodifiable view for iteration

```java
public class InsurancePolicy {
    private final List<Claim> claims = new ArrayList<>();
    private final List<CoverageItem> coverageItems = new ArrayList<>();

    // ✅ Read-only view for iteration
    public List<Claim> getClaims() {
        return Collections.unmodifiableList(claims);
    }

    // ✅ Controlled add with validation
    public void addClaim(Claim claim) {
        Objects.requireNonNull(claim, "Claim must not be null");
        if (claims.stream().anyMatch(c -> c.getId().equals(claim.getId())))
            throw new IllegalArgumentException("Duplicate claim: " + claim.getId());
        claims.add(claim);
    }

    // ✅ Controlled remove
    public boolean removeClaim(ClaimId claimId) {
        return claims.removeIf(c -> c.getId().equals(claimId));
    }

    // ✅ Query without exposing internals
    public boolean hasClaims()            { return !claims.isEmpty(); }
    public int claimCount()               { return claims.size(); }
    public Optional<Claim> findClaim(ClaimId id) {
        return claims.stream().filter(c -> c.getId().equals(id)).findFirst();
    }
}
```

**Kotlin:**

```kotlin
class InsurancePolicy {
    private val _claims = mutableListOf<Claim>()

    // ✅ Immutable view
    val claims: List<Claim> get() = _claims.toList()

    fun addClaim(claim: Claim) {
        require(_claims.none { it.id == claim.id }) { "Duplicate claim: ${claim.id}" }
        _claims.add(claim)
    }

    fun removeClaim(id: ClaimId): Boolean = _claims.removeIf { it.id == id }

    val hasClaims: Boolean get() = _claims.isNotEmpty()
    fun findClaim(id: ClaimId): Claim? = _claims.find { it.id == id }
}
```

### SBPP-STA-11:5 - Archetypal Grounding

**U.System:** `policy.addClaim(claim)` enforces duplicate checking; `policy.getClaims().add(claim)` bypasses it.
**U.Episteme:** The owning object is the only authority on its collection's invariants.

### SBPP-STA-11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Collection field access in Java/Kotlin domain objects**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `toList()` in Kotlin creates a copy every time — expensive for large collections | Use `Collections.unmodifiableList()` (Java) for O(1) view; `toList()` only when defensive copy is truly needed |
| **Arch** | `_claims` / `claims` naming convention in Kotlin is a common pattern | Document the convention in team style guide |
| **Onto/Epist** | Returning `List<Claim>` promises that the collection doesn't change behind the caller's back | Document that the view is a snapshot; or use `Collections.unmodifiableList()` for a live view |
| **Prag** | Spring Data repository pattern often replaces object-owned collections | For persistence, use repository; Collection Accessor for domain-owned collections |
| **Did** | New developers often expose the mutable list directly | Code review checklist: no direct mutable collection getter |

### SBPP-STA-11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA11-1** | Collection fields MUST NOT be exposed directly via getters. | Prevents external mutation |
| **CC-STA11-2** | Read access SHALL return `Collections.unmodifiableList()` (Java) or `List<T>` from `_list` (Kotlin). | Safe read access |
| **CC-STA11-3** | Add/remove operations SHALL validate invariants before modifying the collection. | Maintains invariants |
| **CC-STA11-4** | Query operations (count, contains, find) SHOULD be provided as named methods. | Reduces temptation to get the list for querying |

### SBPP-STA-11:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Direct collection getter**
```java
public List<Claim> getClaims() { return claims; }  // mutable internal list exposed
```
Fix: `return Collections.unmodifiableList(claims);`

**Anti-pattern 2: No add/remove methods**
Only a getter is provided; callers call `policy.getClaims().add(claim)`.
Fix: Provide `addClaim()`/`removeClaim()` with validation.

### SBPP-STA-11:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Collection invariants enforced by the owning object | More API surface (add/remove/find methods) |
| Internal collection type hidden | Defensive copy cost — mitigated by unmodifiable view |
| Domain vocabulary in collection operations | — |

### SBPP-STA-11:10 - Rationale

Collection Accessor Method is the standard encapsulation pattern for domain collections.
It prevents the "collection getter" anti-pattern and supports invariant enforcement.
DDD aggregates apply this pattern: only the aggregate root exposes collection mutation methods.

### SBPP-STA-11:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**DDD Aggregate pattern (Vernon, 2016):** Only the aggregate root controls its collection members. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 50 — make defensive copies for mutable fields. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| DDD Aggregate (Vernon, 2016) | Root-controlled collection | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 50 defensive copies | **Adopt** |

### SBPP-STA-11:12 - Relations

* **Specialises:** SBPP-STA-09 (Getting Method)
* **Implements:** DDD Aggregate collection management
* **Enables:** SBPP-STA-12 (Enumeration Method — iterating the collection)

### SBPP-STA-11:End
