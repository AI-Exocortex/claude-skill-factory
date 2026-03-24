## SBPP-STA-08 - Indirect Variable Access

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-08:1 - Problem frame

When an instance variable needs lazy initialization, validation on access, computed
transformation, or subclass-level customisation, accessing it directly by name prevents
these requirements from being satisfied. Indirect Variable Access routes all access
through a getter method, providing an interception point.

### SBPP-STA-08:2 - Problem

How do you access instance variables within a class when flexibility — lazy init,
validation, or override — is needed rather than simple direct field access?

### SBPP-STA-08:3 - Forces

| Force | Tension |
|-------|---------|
| **Flexibility** | Getter enables lazy init, validation, subclass override ↔ adds indirection |
| **Readability** | Direct access is clearer ↔ getter routing centralises behaviour |
| **Subclassing** | Protected getter is overridable ↔ direct field access is not |

### SBPP-STA-08:4 - Solution — Route all access through a getter; access the field only in the getter itself

Access the backing field only within the getter method. All other intra-class references
use the getter, not the field directly.

**Java example:**

```java
public class PolicyRatingEngine {
    private RiskMatrix riskMatrix;  // lazily initialized

    // ✅ All access through getter — enables lazy init
    private RiskMatrix getRiskMatrix() {
        if (riskMatrix == null) {
            riskMatrix = RiskMatrix.loadForRegion(region);
        }
        return riskMatrix;
    }

    public Money calculateBase(Policy policy) {
        // ✅ Uses getter, not field directly
        return getRiskMatrix().apply(policy);
    }

    public Money calculateAdjusted(Policy policy, List<Adjustment> adjustments) {
        // ✅ Uses getter consistently
        double factor = getRiskMatrix().factor(policy.getCategory());
        return policy.getBasePremium().multiply(BigDecimal.valueOf(factor));
    }
}
```

**Kotlin — property with custom getter:**

```kotlin
class PolicyRatingEngine(private val region: String) {
    private var _riskMatrix: RiskMatrix? = null

    // ✅ All intra-class access via this property
    private val riskMatrix: RiskMatrix
        get() = _riskMatrix ?: RiskMatrix.loadForRegion(region).also { _riskMatrix = it }

    fun calculateBase(policy: Policy): Money = riskMatrix.apply(policy)
    fun calculateAdjusted(policy: Policy): Money = policy.basePremium * riskMatrix.factor(policy.category)
}

// ✅ Simpler with by lazy
class PolicyRatingEngine(private val region: String) {
    private val riskMatrix: RiskMatrix by lazy { RiskMatrix.loadForRegion(region) }

    fun calculateBase(policy: Policy): Money = riskMatrix.apply(policy)
}
```

### SBPP-STA-08:5 - Archetypal Grounding

**U.System:** All internal code uses `getRiskMatrix()` — if tomorrow the loading logic changes, one method changes.
**U.Episteme:** Routing through a getter makes the access point an extension point — a protected getter can be overridden by a subclass in tests.

### SBPP-STA-08:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Intra-class flexible field access in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Consistent routing requires discipline — developers may forget and access field directly | Code review + NullAway enforce correct access |
| **Arch** | Kotlin `by lazy` makes the indirect getter unnecessary for lazy init | Use `by lazy` in Kotlin; use this pattern only in Java or for non-lazy interception |
| **Onto/Epist** | Adds a layer that may be unnecessary if the field is always valid | Apply only when the interception has a clear value |
| **Prag** | Kotlin property getter IS indirect access — no extra method needed | Kotlin's property system subsumes this pattern |
| **Did** | Explain the trade-off clearly — when to use direct vs indirect | Teach with a concrete before/after example of lazy init bug |

### SBPP-STA-08:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA08-1** | When a field requires lazy init, validation, or override, ALL intra-class access SHALL use the getter. | Ensures consistent behaviour |
| **CC-STA08-2** | The backing field MUST only be accessed directly within the getter itself. | Single access point |
| **CC-STA08-3** | In Kotlin, `by lazy` SHOULD be used instead of hand-written indirect access for lazy initialization. | Idiomatic and thread-safe |

### SBPP-STA-08:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Mixed access**
```java
// Some methods use field; some use getter — inconsistent
void m1() { riskMatrix.apply(...); }       // direct — bypasses lazy
void m2() { getRiskMatrix().apply(...); }  // indirect — correct
```
Fix: Choose one approach per field; use Indirect consistently when lazy init is involved.

### SBPP-STA-08:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Single point for lazy init, validation, or transformation | Discipline required to use getter consistently |
| Protected getter enables test overrides | In Kotlin, `by lazy` is simpler for the lazy use case |

### SBPP-STA-08:10 - Rationale

Indirect Variable Access is the right choice when a field needs more than simple storage.
In Kotlin, `by lazy` and custom property getters make this idiomatic. In Java, it requires
discipline but is well-established.

### SBPP-STA-08:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Kotlin property access (JetBrains, post-2016):** Custom property getters are the Kotlin form. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 83 — lazy init via accessor method. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin property getters (post-2016) | Custom getter IS indirect access | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 83 | **Adopt** |

### SBPP-STA-08:12 - Relations

* **Contrast with:** SBPP-STA-07 (Direct Variable Access — simpler alternative)
* **Enables:** SBPP-STA-04 (Lazy Initialization via getter)
* **Implemented by:** SBPP-STA-09 (Getting Method)
* **Kotlin alternative:** `by lazy`, custom `get()` property

### SBPP-STA-08:End
