## SBPP-BEH-10 - Method Object

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-10:1 - Problem frame

Some algorithms in Java/Kotlin microservices are inherently complex: they share many local
variables across steps, cannot be simplified by straightforward extraction (because every
extracted method would need all the same parameters), and represent a coherent computation
that does not belong entirely to any existing class. The calculation engine in an insurance
rating system is a typical example.

### SBPP-BEH-10:2 - Problem

How do you organise a method whose complexity cannot be reduced by Composed Method because
all its parts share many arguments and temporary variables, making extraction impractical?

### SBPP-BEH-10:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion** | All parts of the algorithm are tightly coupled ↔ putting everything in one class is a God Object |
| **Testability** | Large methods are hard to test in isolation ↔ splitting requires passing many parameters |
| **Reusability** | Algorithm may need to be reused with different configurations ↔ tight coupling prevents easy reuse |

### SBPP-BEH-10:4 - Solution — Extract the method into its own class; make arguments become fields

Create a new class whose sole purpose is to represent the computation. Constructor parameters
become instance fields. The original method's body becomes a method (conventionally `compute()`,
`execute()`, or `calculate()`). Steps become private methods that share the fields.

**Java example:**

```java
// Before: unextractable because all steps share riskScore, adjustments, factors
public Money calculatePremium(Policy policy, RiskContext context) {
    double riskScore = computeBaseRisk(policy, context);       // needs policy & context
    List<Adjustment> adjustments = gatherAdjustments(policy, context, riskScore);
    double loadingFactor = computeLoading(adjustments, riskScore, context);
    // ... 50 more lines sharing all these variables
}

// After: Method Object
public final class PremiumCalculation {
    private final Policy policy;
    private final RiskContext context;
    // derived state shared across steps
    private double riskScore;
    private List<Adjustment> adjustments;
    private double loadingFactor;

    public PremiumCalculation(Policy policy, RiskContext context) {
        this.policy = policy;
        this.context = context;
    }

    public Money calculate() {
        computeBaseRisk();
        gatherAdjustments();
        computeLoading();
        return assemblePremium();
    }

    private void computeBaseRisk() {
        this.riskScore = RiskScorer.score(policy, context);
    }

    private void gatherAdjustments() {
        this.adjustments = AdjustmentProvider.for(policy, context, riskScore);
    }

    private void computeLoading() {
        this.loadingFactor = LoadingTable.lookup(adjustments, riskScore);
    }

    private Money assemblePremium() {
        return policy.getBasePremium()
                     .multiply(loadingFactor)
                     .add(adjustments.stream().map(Adjustment::amount)
                                     .reduce(Money.ZERO, Money::add));
    }
}

// Calling code
Money premium = new PremiumCalculation(policy, riskContext).calculate();
```

**Kotlin example:**

```kotlin
class PremiumCalculation(
    private val policy: Policy,
    private val context: RiskContext
) {
    private var riskScore: Double = 0.0
    private var adjustments: List<Adjustment> = emptyList()
    private var loadingFactor: Double = 1.0

    fun calculate(): Money {
        computeBaseRisk()
        gatherAdjustments()
        computeLoading()
        return assemblePremium()
    }

    private fun computeBaseRisk() { riskScore = RiskScorer.score(policy, context) }
    private fun gatherAdjustments() { adjustments = AdjustmentProvider.forContext(policy, context, riskScore) }
    private fun computeLoading() { loadingFactor = LoadingTable.lookup(adjustments, riskScore) }
    private fun assemblePremium() = policy.basePremium * loadingFactor + adjustments.sumOf { it.amount }
}
```

### SBPP-BEH-10:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Complex algorithms that share many intermediate values are encapsulated in single-purpose calculation classes.
*Show:* `PremiumCalculation` encapsulates five interdependent steps; each step is a one-liner
because all share the same instance fields.

**U.Episteme (design reasoning):**
*Tell:* Making a method into an object turns shared local state into named instance fields,
restoring the possibility of meaningful decomposition.
*Show:* `computeBaseRisk()` can be tested in isolation by constructing a `PremiumCalculation`
and inspecting the `riskScore` field after the call — not possible with an inlined local variable.

### SBPP-BEH-10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Complex algorithm encapsulation in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Creates a class that is used once and discarded; can seem wasteful | The organisational benefit justifies the extra class |
| **Arch** | Mutable instance fields (`riskScore`, `adjustments`) make the object non-reusable across threads | Method objects are typically one-shot; never share across threads |
| **Onto/Epist** | The "method object" is a computation, not a domain entity; this can confuse domain model | Put in a dedicated `calculation` or `service` package; name clearly as a computation |
| **Prag** | For pure functions with no intermediate state, a simple static method or Kotlin function is clearer | Apply only when intermediate state genuinely needs sharing; not as a default |
| **Did** | Developers may turn every complex method into a Method Object prematurely | Try Composed Method first; use Method Object only when extraction fails due to shared state |

### SBPP-BEH-10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH10-1** | Method Object classes SHALL be named as a noun phrase describing the computation (e.g., `PremiumCalculation`, not `PremiumCalculator`). | Names the result, not the tool |
| **CC-BEH10-2** | Method Object instances MUST NOT be shared across threads (they hold mutable computation state). | Prevents race conditions |
| **CC-BEH10-3** | The public entry point SHOULD be a single method named `calculate()`, `compute()`, or `execute()`. | Makes intent unambiguous |
| **CC-BEH10-4** | Method Object SHOULD be applied only after Composed Method (BEH-01) fails due to shared intermediate state. | Prevents premature complexity |

### SBPP-BEH-10:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: God Method Object**
Putting the entire service class logic into one Method Object.
Fix: Apply Method Object only to the one algorithm that resists extraction; keep the service class lean.

**Anti-pattern 2: Shared Method Object Instance**
Caching a Method Object as a field or Spring bean (making it shared/stateful).
Fix: Create a new instance per invocation; Method Objects are cheap to construct.

### SBPP-BEH-10:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Complex algorithm becomes decomposable into meaningful private steps | One extra class per algorithm — justified by maintainability gain |
| Steps can be individually tested via package-private access | Mutable fields make thread-safety manual — create new instance per call |
| Intermediate state is named, not anonymous local variables | — |

### SBPP-BEH-10:10 - Rationale

Method Object is Beck's solution for the class of algorithms that resist Composed Method
because all parts share the same complex state. In Java/Kotlin microservices, premium
calculators, risk scorers, and workflow executors are typical examples.

The pattern is a direct precedent of modern "use-case" or "interactor" classes in Clean
Architecture, where each use case is a single class with a single public `execute()` method.

### SBPP-BEH-10:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Architecture (Martin, 2017):** Use-case / interactor classes are Method Objects —
single public `execute()` method, encapsulated input/output state. *Adopt.*

**Refactoring 2nd ed. — "Replace Function with Command" (Fowler, 2018):** Fowler's "Command"
refactoring is identical to Method Object. *Adopt.*

**Domain-Driven Design (Vernon, 2016):** Domain Services for complex operations that don't
belong to a single entity are Method Objects at the service level. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Architecture use-case (Martin, 2017) | Single-method interactor | **Adopt** |
| Refactoring 2nd ed. "Replace Function with Command" (Fowler, 2018) | Direct equivalence | **Adopt** |
| DDD Domain Services (Vernon, 2016) | Complex cross-entity operations | **Adopt** |

### SBPP-BEH-10:12 - Relations

* **Applied when:** SBPP-BEH-01 (Composed Method) fails due to shared intermediate state
* **Implements:** Clean Architecture use-case / interactor pattern
* **Relates to:** SBPP-BEH-31 (Collecting Parameter — alternative for result accumulation)
* **Constrains:** Must be created fresh per call (not shared as singleton)

### SBPP-BEH-10:End
