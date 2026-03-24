## SBPP-STA-06 - Constant Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-06:1 - Problem frame

Domain constants — tax rates, maximum limits, regulatory thresholds — need to be
expressed somewhere in a codebase. Magic literals scattered across methods make the
constants invisible. Symbolic constants (Java `static final`, Kotlin `const val`) make
them named and findable, but choosing where to declare them matters.

### SBPP-STA-06:2 - Problem

How do you represent a constant value — one that does not change between instances —
so that it is named, discoverable, overridable when needed, and associated with the
right domain object?

### SBPP-STA-06:3 - Forces

| Force | Tension |
|-------|---------|
| **Naming** | Constants need intention-revealing names ↔ magic numbers are tempting |
| **Location** | Constants belong near what they constrain ↔ separate constants classes centralise them |
| **Overridability** | Method-based constants can be overridden by subclasses ↔ `static final` cannot |

### SBPP-STA-06:4 - Solution — Declare constants as named `static final` fields or companion `const val`; use methods when override is needed

**Java — static constant (primary approach):**

```java
public final class PremiumLimits {
    // ✅ Named constants near where they're used
    public static final Money MINIMUM_PREMIUM = Money.of(50_00, Currency.USD);
    public static final Money MAXIMUM_PREMIUM = Money.of(500_000_00, Currency.USD);
    public static final int   MAX_ADJUSTMENTS = 10;
    public static final BigDecimal BASE_RATE  = new BigDecimal("0.05");

    private PremiumLimits() {}
}

// In domain class — reference the constant
public class PremiumCalculator {
    public Money validate(Money premium) {
        if (premium.compareTo(PremiumLimits.MINIMUM_PREMIUM) < 0)
            throw new IllegalArgumentException("Premium below minimum");
        return premium;
    }
}
```

**Java — method-based constant (when subclass override is designed):**

```java
public class StandardRatingEngine {
    // Override-able constant via method
    protected BigDecimal baseRate() { return new BigDecimal("0.05"); }

    public Money calculate(Policy policy) {
        return policy.getSumInsured().multiply(baseRate());
    }
}

public class HighRiskRatingEngine extends StandardRatingEngine {
    @Override protected BigDecimal baseRate() { return new BigDecimal("0.12"); }
}
```

**Kotlin:**

```kotlin
object PremiumLimits {
    val MINIMUM_PREMIUM = Money.of(5000, Currency.USD)
    val MAXIMUM_PREMIUM = Money.of(50_000_000, Currency.USD)
    const val MAX_ADJUSTMENTS = 10
}

// Companion object constant
class PremiumCalculator {
    companion object {
        val BASE_RATE = BigDecimal("0.05")
    }
}
```

### SBPP-STA-06:5 - Archetypal Grounding

**U.System:** `PremiumLimits.MINIMUM_PREMIUM` — findable, named, with a clear home near the domain it constrains.
**U.Episteme:** Naming `0.05` as `BASE_RATE` makes a regulatory parameter visible and changeable in one place.

### SBPP-STA-06:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Constant declaration in Java/Kotlin domain code**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Constants class becomes a dumping ground (`ConstantsHelper.java`) | Group constants by domain concern, not alphabetically |
| **Arch** | `static final` constants cannot be overridden; configuration-driven values need a different approach | Use Spring `@Value` or configuration beans for environment-varying constants |
| **Onto/Epist** | "Constant" hides that regulatory values change over time | Use versioned constant sets or external config for annually-updated values |
| **Prag** | Kotlin `object` declarations are natural constant namespaces | Use objects, not companion objects, for standalone constant groups |
| **Did** | New developers scatter constants as magic literals | Lint rule: no numeric/string literals in domain logic without a named constant |

### SBPP-STA-06:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA06-1** | Domain constants SHALL be named and declared as `static final` (Java) or `const val`/`val` in `object` (Kotlin). | Eliminates magic literals |
| **CC-STA06-2** | Constants SHOULD be grouped by domain concern, not in a single global constants file. | Cohesion |
| **CC-STA06-3** | Regulatory or configuration-driven values SHALL be loaded from external config, not hardcoded. | Supports environment-specific values |

### SBPP-STA-06:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Magic literal**
```java
if (premium.compareTo(BigDecimal.valueOf(50)) < 0) { ... }
```
Fix: `PremiumLimits.MINIMUM_PREMIUM`.

**Anti-pattern 2: God Constants File**
`public class Constants { ... 200 unrelated constants ... }`.
Fix: Group constants in their owning domain class or a focused constants object.

### SBPP-STA-06:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Magic literals eliminated — one change location | Must keep constants grouped logically |
| Override via method pattern enables polymorphic configuration | — |
| Kotlin `const val` inlined by compiler — zero overhead | — |

### SBPP-STA-06:10 - Rationale

Constant Method corresponds to Java `static final` and Kotlin `const val`. The method
variant (non-static) is still valuable when configuration must vary by subclass.
For environment-varying values, external config (Spring `@Value`) is the modern replacement.

### SBPP-STA-06:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 34 (use enums instead of int constants) and
general guidance on `static final` constants. *Adopt.*

**Spring `@Value` / `@ConfigurationProperties` (post-2015):** Externalise environment-dependent
constants. *Adopt for config-driven values.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Named constants | **Adopt** |
| Spring `@ConfigurationProperties` (post-2015) | Externalised config | **Adopt** |
| Kotlin `const val` / `object` (post-2016) | Idiomatic constants | **Adopt** |

### SBPP-STA-06:12 - Relations

* **Provides values for:** SBPP-STA-05 (Default Value Method)
* **Named by:** SBPP-BEH-18 (Intention Revealing Selector)
* **Alternative for config values:** Spring `@ConfigurationProperties`

### SBPP-STA-06:End
