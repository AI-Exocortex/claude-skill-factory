## SBPP-STA-13 - Boolean Property Setting Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-13:1 - Problem frame

Boolean properties can be set via a single setter (`setEnabled(true/false)`) or via
two separate intention-revealing methods (`enable()` / `disable()`). Beck recommends
the two-method approach because it encodes the intent explicitly and prevents callers
from needing to know the representation.

### SBPP-STA-13:2 - Problem

How do you provide a way to set a boolean property so that callers express intent without
knowing the underlying representation?

### SBPP-STA-13:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | `activate()` reads as domain event ↔ `setActive(true)` exposes representation |
| **API symmetry** | Two methods vs one setter | Two methods are slightly more to learn |
| **Representation hiding** | `enable()`/`disable()` work even if representation changes from boolean to enum | Setter exposes boolean representation |

### SBPP-STA-13:4 - Solution — Provide two intention-revealing methods instead of a boolean setter

```java
public class PolicySwitch {
    private boolean enabled;

    // ❌ Boolean setter — exposes representation
    // public void setEnabled(boolean enabled) { this.enabled = enabled; }

    // ✅ Intention-revealing pair
    public void enable()  { this.enabled = true; }
    public void disable() { this.enabled = false; }
    public boolean isEnabled() { return enabled; }
}

// Usage reads like domain events
policySwitch.enable();
policySwitch.disable();
```

**Kotlin:**

```kotlin
class PolicySwitch(var isEnabled: Boolean = false) {
    fun enable()  { isEnabled = true }
    fun disable() { isEnabled = false }
    // Or use Kotlin property directly if no domain validation needed:
    // isEnabled = true / isEnabled = false
}
```

**For domain objects with invariants:**

```java
public class InsurancePolicy {
    private boolean underReview;

    public void placeUnderReview()     { this.underReview = true; }
    public void clearFromReview()      { this.underReview = false; }
    public boolean isUnderReview()     { return underReview; }
}
```

### SBPP-STA-13:5 - Archetypal Grounding

**U.System:** `policy.placeUnderReview()` — the action's domain meaning is in the name.
**U.Episteme:** If the representation changes from `boolean` to `ReviewStatus enum`, only the two methods change — callers are unaffected.

### SBPP-STA-13:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Boolean state management in Java/Kotlin domain objects**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Framework serialization expects `setX(boolean)` convention | Use `@JsonProperty`/Jackson annotation; keep domain API clean |
| **Arch** | Kotlin `var isEnabled` with direct assignment is idiomatic and clean | For simple flags with no domain logic, direct property assignment is acceptable |
| **Onto/Epist** | "Enable/disable" names may not fit all domains — use domain vocabulary | `activate()`/`deactivate()`, `approve()`/`reject()`, `lock()`/`unlock()` |
| **Prag** | Works well for domain-meaningful state changes; overkill for simple flags | Apply when the property change has domain meaning; skip for internal flags |
| **Did** | Teach as part of DDD state transition methods | Pair with domain transition examples |

### SBPP-STA-13:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA13-1** | Domain-meaningful boolean state changes SHOULD be expressed as paired intention-revealing methods. | Domain vocabulary |
| **CC-STA13-2** | The boolean getter SHALL follow `is`/`has`/`can` naming. | Consistency with Query Method |
| **CC-STA13-3** | Simple internal flags with no domain significance MAY use direct property assignment (Kotlin). | Pragmatism |

### SBPP-STA-13:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Boolean parameter flag**
```java
policy.setReviewStatus(true);  // true means what?
```
Fix: `policy.placeUnderReview()`.

### SBPP-STA-13:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Domain vocabulary in state changes | Two methods instead of one setter |
| Representation changes don't affect callers | — |

### SBPP-STA-13:10 - Rationale

Boolean Property Setting Method is one expression of Intention Revealing Message (BEH-17).
The two-method approach also future-proofs against representation changes — if `boolean`
becomes a three-state `ReviewStatus`, the calling code needs no changes.

### SBPP-STA-13:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008/ongoing):** Boolean parameters in methods are a code smell.
Two methods express intent explicitly. *Adopt.*

**DDD Ubiquitous Language (Vernon, 2016):** Domain events expressed as method calls. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, ongoing) | No boolean parameters | **Adopt** |
| DDD Ubiquitous Language (Vernon, 2016) | Domain vocab | **Adopt** |

### SBPP-STA-13:12 - Relations

* **Implements:** SBPP-BEH-17 (Intention Revealing Message)
* **Paired with:** SBPP-STA-10 (Setting Method — general case)
* **Read side:** SBPP-BEH-07 (Query Method — the boolean getter)

### SBPP-STA-13:End
