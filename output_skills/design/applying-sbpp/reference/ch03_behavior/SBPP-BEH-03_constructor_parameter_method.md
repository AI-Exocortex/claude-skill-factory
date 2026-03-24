## SBPP-BEH-03 - Constructor Parameter Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-03:1 - Problem frame

When constructing a complex object in Java or Kotlin, several parameters must be set
on the new instance. Setting them inline in the constructor body can make the constructor
long and hard to follow, especially when some parameters require transformation or
validation before being stored.

### SBPP-BEH-03:2 - Problem

How do you initialize instance variables from constructor parameters in a way that
keeps the constructor body readable and makes the initialization logic reusable?

### SBPP-BEH-03:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | Each parameter initialisation in one line ↔ validation/transformation bloats constructors |
| **Reusability** | Initialization logic may be needed in multiple constructors | Duplicating it violates DRY |
| **Testability** | Individual initialization steps should be independently verifiable | Inline code is hard to unit-test |

### SBPP-BEH-03:4 - Solution — Delegate parameter initialization to private setter-like methods

Extract each parameter initialization step into a private method named after the role of the
parameter. Call these methods from the constructor.

**Java example:**

```java
public class PolicyCalculator {
    private final RiskMatrix riskMatrix;
    private final List<RiskFactor> factors;
    private final BigDecimal baseRate;

    public PolicyCalculator(RiskConfig config, List<RiskFactor> factors) {
        this.riskMatrix = buildRiskMatrix(config);
        this.factors = validateFactors(factors);
        this.baseRate = resolveBaseRate(config);
    }

    private RiskMatrix buildRiskMatrix(RiskConfig config) {
        return RiskMatrix.from(config.getRegion(), config.getCategory());
    }

    private List<RiskFactor> validateFactors(List<RiskFactor> factors) {
        if (factors == null || factors.isEmpty()) {
            throw new IllegalArgumentException("At least one risk factor required");
        }
        return List.copyOf(factors);
    }

    private BigDecimal resolveBaseRate(RiskConfig config) {
        return config.getBaseRate().orElse(BigDecimal.valueOf(0.05));
    }
}
```

**Kotlin example:**

```kotlin
class PolicyCalculator(config: RiskConfig, factors: List<RiskFactor>) {
    private val riskMatrix: RiskMatrix = buildRiskMatrix(config)
    private val factors: List<RiskFactor> = validateFactors(factors)
    private val baseRate: BigDecimal = resolveBaseRate(config)

    private fun buildRiskMatrix(config: RiskConfig) =
        RiskMatrix.from(config.region, config.category)

    private fun validateFactors(factors: List<RiskFactor>): List<RiskFactor> {
        require(factors.isNotEmpty()) { "At least one risk factor required" }
        return factors.toList()
    }

    private fun resolveBaseRate(config: RiskConfig) =
        config.baseRate ?: BigDecimal("0.05")
}
```

**Note for Kotlin:** prefer `init` blocks with property initializers over explicit
constructor-parameter methods when transformation is simple.

### SBPP-BEH-03:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Constructor bodies call named private methods for each complex parameter.
*Show:* `this.factors = validateFactors(factors)` — the constructor reads like a checklist
of what initialization must happen; the detail is hidden one level down.

**U.Episteme (design reasoning):**
*Tell:* Separating validation logic from assignment makes each concern independently reviewable.
*Show:* A bug in factor validation is findable in `validateFactors()`, not buried inside a
100-line constructor.

### SBPP-BEH-03:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin constructor design**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Private methods can't be directly tested in production code | Use package-private visibility for test access, or test via the constructor |
| **Arch** | Kotlin init blocks and property initializers often make explicit methods unnecessary | Use this pattern only when logic is non-trivial |
| **Onto/Epist** | Method names may encode validation assumptions that change over time | Keep names describing the role, not the current rule |
| **Prag** | Adds methods to the class; lightweight for complex constructors, overkill for simple ones | Only extract when the initialization step has a meaningful name |
| **Did** | Developers may confuse this with setter injection | Emphasize these are constructor-time-only methods, not mutable setters |

### SBPP-BEH-03:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH03-1** | Each constructor parameter transformation SHALL be delegated to a named private method when the transformation is non-trivial (> 1 expression). | Keeps constructors readable |
| **CC-BEH03-2** | Constructor parameter methods SHALL be named after the role they serve, not the technical operation. | Communicates intent |
| **CC-BEH03-3** | Constructor parameter methods MUST NOT have side effects beyond constructing their return value. | Maintains constructor purity |

### SBPP-BEH-03:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Fat Constructor**
All logic inline in the constructor, making it 30+ lines. Fix: Extract each logical block to
a named method using this pattern.

**Anti-pattern 2: Setter Confusion**
Methods named `setX()` called from constructor — implies mutability. Fix: Name as `buildX()`,
`validateX()`, `resolveX()` to make the constructor-only intent clear.

### SBPP-BEH-03:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Constructor body becomes a readable checklist of initialization concerns | More methods — acceptable overhead |
| Each initialization step is individually testable via package-private access | Does not help if the class has too many constructor parameters (use Builder instead) |
| Shared validation logic can be reused across multiple constructors | — |

### SBPP-BEH-03:10 - Rationale

This pattern is a direct application of Composed Method (BEH-01) to constructors. In Java,
constructors cannot be composed from other constructors using normal method calls (the
`this()`/`super()` must be first), so extracting initialization logic into named helpers
is the primary way to keep constructors readable.

In Kotlin, property initializers in the class body serve a similar function, and `init`
blocks allow sequenced initialization. This pattern is most valuable when each step has
non-trivial logic warranting its own name.

### SBPP-BEH-03:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Refactoring 2nd ed. (Fowler, 2018):** "Extract Function" applied to constructor steps is
explicitly addressed. Long constructors are a code smell that Extract Function resolves. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Functions should do one thing — applies equally to
constructors. Extracting initialization steps is recommended practice. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Refactoring 2nd ed. (Fowler, 2018) | Extract Function for constructors | **Adopt** |
| Clean Code (Martin, 2008/2015+) | Single-thing constructor discipline | **Adopt** |
| Kotlin idiomatic style (JetBrains, post-2016) | Property initializers as lighter alternative | **Adapt** |

### SBPP-BEH-03:12 - Relations

* **Specialises:** SBPP-BEH-01 (Composed Method — applied to constructors)
* **Precedes:** SBPP-BEH-02 (Constructor Method — the factory calls this internally)
* **Relates to:** SBPP-STA-03 (Explicit Initialization)
* **Constrains:** Object invariant establishment at construction time

### SBPP-BEH-03:End
