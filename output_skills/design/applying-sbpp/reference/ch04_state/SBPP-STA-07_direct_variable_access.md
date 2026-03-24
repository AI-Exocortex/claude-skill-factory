## SBPP-STA-07 - Direct Variable Access

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-07:1 - Problem frame

Within a class, fields can be accessed either directly (by name) or indirectly (via
getter/setter methods). Beck presents both approaches and recommends each in specific
circumstances. Direct Variable Access is the simpler, more readable option — field
access reads as the field itself, not through an indirection layer.

### SBPP-STA-07:2 - Problem

How do you access instance variables within a class when readability is the priority and
the variable is always valid as accessed?

### SBPP-STA-07:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | Direct `premium` is simpler than `getPremium()` ↔ getter allows future interception |
| **Flexibility** | Direct access couples code to field name and type ↔ getter allows lazy init, validation |
| **Kotlin convention** | Kotlin properties unify direct and indirect access ↔ Java requires explicit choice |

### SBPP-STA-07:4 - Solution — Access fields directly within the class; use Kotlin properties for unified access

In Java, access instance fields directly within the class that owns them. Use getters only
for external access. In Kotlin, properties already unify direct and indirect access.

**Java example:**

```java
public class InsurancePolicy {
    private PolicyStatus status;
    private Money premium;
    private List<Claim> claims;

    // ✅ Within the class: direct field access
    public boolean isActive() {
        return status == PolicyStatus.ACTIVE;  // direct, readable
    }

    public boolean hasHighPremium() {
        return premium.compareTo(HIGH_PREMIUM_THRESHOLD) > 0;  // direct
    }

    private Money applyDiscount(BigDecimal rate) {
        return premium.multiply(BigDecimal.ONE.subtract(rate));  // direct
    }

    // ✅ Getter for external access only
    public PolicyStatus getStatus() { return status; }
    public Money getPremium() { return premium; }
}
```

**Kotlin — properties unify the concern:**

```kotlin
class InsurancePolicy(
    var status: PolicyStatus = PolicyStatus.DRAFT,
    var premium: Money,
    val claims: MutableList<Claim> = mutableListOf()
) {
    // Kotlin: property access IS direct access; backing field accessed automatically
    val isActive: Boolean get() = status == PolicyStatus.ACTIVE
    val hasHighPremium: Boolean get() = premium > HIGH_PREMIUM_THRESHOLD

    private fun applyDiscount(rate: BigDecimal): Money = premium * (BigDecimal.ONE - rate)
}
```

**Rule:** In Java, use direct field access within the class; use getters for external callers.
In Kotlin, properties make this distinction automatic.

### SBPP-STA-07:5 - Archetypal Grounding

**U.System:** `status == PolicyStatus.ACTIVE` inside the policy class — direct, readable, unambiguous.
**U.Episteme:** Direct access documents that the field value is used as-is — no lazy init, no transformation needed.

### SBPP-STA-07:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Intra-class field access in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Direct access cannot be intercepted by subclasses or proxies | If interception is ever needed, switch to Indirect Variable Access |
| **Arch** | Java serialization frameworks (Jackson) access fields directly via reflection by default | Annotate correctly; don't rely on direct access semantics for serialization |
| **Onto/Epist** | Kotlin properties make the distinction invisible — which is correct | Embrace Kotlin's unified property access |
| **Prag** | Spring/Hibernate may instrument getters via proxies; direct field access bypasses this | Use getters in JPA entities; direct access is for pure domain classes |
| **Did** | New Java developers often put `this.` prefix everywhere unnecessarily | `this.` is needed only for shadowing; otherwise omit |

### SBPP-STA-07:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA07-1** | Within a class, fields SHOULD be accessed directly (no `this.getX()` for internal use). | Readability |
| **CC-STA07-2** | External callers MUST use public getter methods or Kotlin properties. | Encapsulation |
| **CC-STA07-3** | JPA entity field access SHOULD be via getter methods (unless using `@Access(FIELD)`). | Framework proxy compatibility |

### SBPP-STA-07:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Internal getter call**
```java
public boolean isActive() { return this.getStatus() == ACTIVE; }  // unnecessary indirection
```
Fix: `return status == ACTIVE;`

**Anti-pattern 2: Bypassing lazy init**
```java
return riskScore;  // bypasses lazy initialization logic in getRiskScore()
```
Fix: When a field uses Lazy Initialization, always access via the getter — switch to Indirect Variable Access.

### SBPP-STA-07:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Simple, readable intra-class code | Cannot intercept without switching to Indirect Variable Access |
| Kotlin properties unify the pattern automatically | — |

### SBPP-STA-07:10 - Rationale

Direct Variable Access is the default for intra-class access. The choice between direct
and indirect access is made once per field: if the field ever needs lazy init, validation,
or override, switch to Indirect Variable Access for that field.

### SBPP-STA-07:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Fields should be private; within the class, direct
access is standard. *Adopt.*

**Kotlin property access (JetBrains, post-2016):** Properties unify the direct/indirect
distinction. Backing field accessed directly; custom getter adds indirection transparently. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Private fields, direct internal access | **Adopt** |
| Kotlin properties (post-2016) | Unified direct/indirect access | **Adopt** |

### SBPP-STA-07:12 - Relations

* **Contrast with:** SBPP-STA-08 (Indirect Variable Access — via getter/setter)
* **Complement:** SBPP-STA-09 (Getting Method — for external access)
* **Choose between:** Use direct when no interception needed; use indirect when lazy init, validation, or override is required

### SBPP-STA-07:End
