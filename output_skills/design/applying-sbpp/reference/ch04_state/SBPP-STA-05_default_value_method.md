## SBPP-STA-05 - Default Value Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-05:1 - Problem frame

When a field has a non-trivial default value — computed from other state, loaded from
configuration, or derived from a business rule — expressing that default inline in the
field declaration or constructor creates a maintenance problem. Extracting it into a
named method both documents the default and enables overriding in subclasses.

### SBPP-STA-05:2 - Problem

How do you represent a default value for a variable when the default is complex enough
to warrant a name and possibly to be overridden by subclasses?

### SBPP-STA-05:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Named method documents what the default represents ↔ adds a method to the class |
| **Overridability** | Protected method can be overridden ↔ breaks encapsulation if misused |
| **Reusability** | Default value method usable from multiple constructors ↔ overkill for simple defaults |

### SBPP-STA-05:4 - Solution — Extract non-trivial defaults into named private/protected methods

When a default value is more than a literal constant, extract it into a method named
after what it represents.

**Java example:**

```java
public class RatingPolicy {
    private final BigDecimal baseRate;
    private final int maxAdjustments;
    private final RiskTier defaultTier;

    public RatingPolicy(String region) {
        this.baseRate       = defaultBaseRate(region);
        this.maxAdjustments = defaultMaxAdjustments();
        this.defaultTier    = defaultRiskTier(region);
    }

    private BigDecimal defaultBaseRate(String region) {
        return RegionRateTable.getBaseRate(region)
                              .orElse(new BigDecimal("0.05"));
    }

    private int defaultMaxAdjustments() {
        return Integer.parseInt(
            System.getProperty("rating.max-adjustments", "5")
        );
    }

    protected RiskTier defaultRiskTier(String region) {
        // Protected so regional subclasses can override
        return RegionRiskMap.getDefaultTier(region);
    }
}
```

**Kotlin example:**

```kotlin
open class RatingPolicy(region: String) {
    val baseRate: BigDecimal = defaultBaseRate(region)
    val maxAdjustments: Int  = defaultMaxAdjustments()
    val defaultTier: RiskTier = defaultRiskTier(region)

    private fun defaultBaseRate(region: String) =
        RegionRateTable.getBaseRate(region) ?: BigDecimal("0.05")

    private fun defaultMaxAdjustments() =
        System.getProperty("rating.max-adjustments", "5").toInt()

    protected open fun defaultRiskTier(region: String) =
        RegionRiskMap.getDefaultTier(region)
}
```

### SBPP-STA-05:5 - Archetypal Grounding

**U.System:** `defaultBaseRate(region)` communicates that the value is a regional base rate default — not just a number.
**U.Episteme:** A `protected` default method is an explicit override point — a subclass knows exactly what it can customise.

### SBPP-STA-05:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Default value expression in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `protected` default methods are unintended override points if not designed for it | Use `private` unless override is explicitly intended |
| **Arch** | Calling overridable methods from constructors is dangerous in Java (subclass not yet initialised) | Use `private` in constructors; only use `protected` for post-construction overrides |
| **Onto/Epist** | Default method name should describe the default's domain meaning | Name after role, not mechanism: `defaultRiskTier` not `computeTierFromRegion` |
| **Prag** | Spring `@Value` and `@ConfigurationProperties` handle configuration defaults better | Use Spring for config-driven defaults; use this pattern for domain-rule defaults |
| **Did** | Calling overridable methods from constructors is a well-known Java pitfall | Teach and enforce: constructor calls must be to `private` or `final` methods |

### SBPP-STA-05:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA05-1** | Default Value Methods called from constructors MUST be `private` or `final`. | Prevents unsafe override in subclass constructor |
| **CC-STA05-2** | Default Value Methods SHOULD be named after the role the default value plays. | Communicates intent |
| **CC-STA05-3** | `protected` Default Value Methods SHALL only be used when override is an explicitly designed extension point. | Prevents accidental API |

### SBPP-STA-05:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Overridable constructor call**
```java
public MyClass() { this.tier = defaultTier(); }  // protected defaultTier() — unsafe
```
Fix: Make `defaultTier()` `private` or `final`.

**Anti-pattern 2: Default with side-effects**
```java
private LocalDate defaultExpiryDate() { auditLog.record("INIT"); return LocalDate.now().plusYears(1); }
```
Fix: Default value methods must be pure — no side effects.

### SBPP-STA-05:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Named default communicates domain meaning | Extra method per complex default |
| Subclass override point is explicit | Protected methods must be designed carefully |
| Reusable across multiple constructors | — |

### SBPP-STA-05:10 - Rationale

Default Value Method is a specialised application of Intention Revealing Message (BEH-17)
to field initialization. The name documents what the default represents, not just how to
compute it. The `private`/`protected` distinction determines whether the default is an
implementation detail or a designed extension point.

### SBPP-STA-05:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 19 — never call overridable methods from
constructors. This pattern enforces that guideline. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Intention-revealing names apply to default methods
as to all methods. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 19 — constructor safety | **Adopt** |
| Clean Code (Martin, ongoing) | Intention-revealing naming | **Adopt** |

### SBPP-STA-05:12 - Relations

* **Applied by:** SBPP-STA-03 (Explicit Initialization), SBPP-STA-04 (Lazy Initialization)
* **Named by:** SBPP-BEH-18 (Intention Revealing Selector)
* **Enables:** Template Method override of defaults in subclasses
* **Constrained by:** Must be `private` when called from constructors

### SBPP-STA-05:End
