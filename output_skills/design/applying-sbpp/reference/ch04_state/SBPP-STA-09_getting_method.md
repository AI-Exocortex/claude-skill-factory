## SBPP-STA-09 - Getting Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-09:1 - Problem frame

External callers — and internal callers using Indirect Variable Access — need a method
to retrieve a field's current value. The Getting Method (getter) provides this access
point. The key design questions are: what should it be named, how private should it be,
and should it return the field directly or a defensive copy?

### SBPP-STA-09:2 - Problem

How do you provide access to an instance variable in a way that encapsulates the storage
strategy and keeps the interface stable even if the implementation changes?

### SBPP-STA-09:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Getter hides field type and storage ↔ overly revealing getters break encapsulation |
| **Convention** | Java `getX()` / Kotlin `val x` are standard ↔ domain vocabulary may differ |
| **Mutability** | Return field directly (fast) ↔ return defensive copy (safe for mutable fields) |

### SBPP-STA-09:4 - Solution — Return immutable fields directly; return defensive copies for mutable; name by convention

**Java example:**

```java
public final class InsurancePolicy {
    private final PolicyId id;
    private final Money premium;             // immutable — return directly
    private final List<Claim> claims;        // mutable — return defensive copy
    private LocalDate expiryDate;            // mutable value — return directly (value type)

    // ✅ Immutable field — direct return
    public PolicyId getId()        { return id; }
    public Money getPremium()      { return premium; }

    // ✅ Mutable collection — defensive copy
    public List<Claim> getClaims() { return Collections.unmodifiableList(claims); }

    // ✅ Value type — safe to return directly
    public LocalDate getExpiryDate() { return expiryDate; }
}
```

**Kotlin — properties are the standard getting method:**

```kotlin
data class InsurancePolicy(
    val id: PolicyId,
    val premium: Money,
    private val _claims: MutableList<Claim> = mutableListOf()
) {
    // ✅ Property exposes immutable view of internal list
    val claims: List<Claim> get() = _claims.toList()

    // ✅ All other vals are auto-accessed as properties
}
```

**Naming conventions:**

| Context | Java name | Kotlin name |
|---------|-----------|-------------|
| Standard getter | `getStatus()` | `status` property |
| Boolean | `isActive()` | `isActive` / `active` property |
| Domain-meaningful | `currentPremium()` | `currentPremium` property |

### SBPP-STA-09:5 - Archetypal Grounding

**U.System:** `policy.getClaims()` returns an unmodifiable view — callers cannot mutate the internal list.
**U.Episteme:** The getter's signature is stable even if the internal storage changes from `ArrayList` to `LinkedList`.

### SBPP-STA-09:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Field accessor design in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | JavaBeans getter proliferation creates anemic domain models | Prefer domain-meaningful methods over raw getters where possible |
| **Arch** | Defensive copies (`toList()`) are O(n) — can be expensive for large collections | Document the copy cost; use `Collections.unmodifiableList()` for O(1) immutable view |
| **Onto/Epist** | `getX()` / `setX()` creates a data container, not a domain object | Provide domain-meaningful methods alongside getters |
| **Prag** | Kotlin's `val` makes most getter boilerplate unnecessary | Use `val` for immutable fields; add custom `get()` only when needed |
| **Did** | New developers generate all getters via IDE without thinking about mutability | Review: does the getter expose mutable state that shouldn't be? |

### SBPP-STA-09:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA09-1** | Getters for mutable collection fields SHALL return an unmodifiable view or defensive copy. | Prevents external mutation of internal state |
| **CC-STA09-2** | Boolean getters SHALL follow `is`/`has`/`can` naming per CC-BEH07-1. | Consistency |
| **CC-STA09-3** | Getters MUST be side-effect free (Command-Query Separation). | Predictability |
| **CC-STA09-4** | In Kotlin, `val` properties SHOULD be preferred over explicit `getX()` functions. | Idiomatic Kotlin |

### SBPP-STA-09:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Returning mutable internal collection**
```java
public List<Claim> getClaims() { return claims; }  // caller can mutate!
```
Fix: `return Collections.unmodifiableList(claims);`

**Anti-pattern 2: Getter with side effect**
```java
public Money getPremium() { accessLog.record("getPremium"); return premium; }
```
Fix: Violates CQS. Remove side effect; log elsewhere.

### SBPP-STA-09:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Internal storage strategy hidden from callers | Defensive copies have cost — use unmodifiable views |
| Kotlin `val` properties eliminate boilerplate | — |
| Boolean naming convention aids readability | — |

### SBPP-STA-09:10 - Rationale

Getting Method is the standard Java/Kotlin encapsulation mechanism. Kotlin properties
make it idiomatic — `val` IS a getting method. The defensive copy discipline for mutable
collections is a critical correctness requirement often overlooked.

### SBPP-STA-09:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 50 (make defensive copies when needed) and
Item 15 (minimise accessibility). *Adopt.*

**Kotlin `val` properties (JetBrains, post-2016):** Idiomatic getter. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Items 15, 50 | **Adopt** |
| Kotlin `val` properties (post-2016) | Getter as property | **Adopt** |

### SBPP-STA-09:12 - Relations

* **Implements:** SBPP-STA-08 (Indirect Variable Access)
* **Complement:** SBPP-STA-10 (Setting Method)
* **Constrained by:** CQS — no side effects

### SBPP-STA-09:End
