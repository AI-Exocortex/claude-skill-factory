## SBPP-BEH-18 - Intention Revealing Selector

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-18:1 - Problem frame

Every method, parameter, and variable in a Java/Kotlin codebase has a name. These names
collectively form the cognitive interface through which developers understand the system.
Poor names — `process()`, `data`, `temp`, `doIt()` — force readers to examine implementations
to understand intent. Good names communicate intent without reading bodies.

### SBPP-BEH-18:2 - Problem

What do you name a method so that its purpose is immediately clear from the name alone,
without requiring callers to read its implementation?

### SBPP-BEH-18:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | Name communicates full intent ↔ names should be concise |
| **Stability** | Names should survive implementation changes ↔ over-specific names couple name to implementation |
| **Discoverability** | Intent-based names aid search ↔ technical names align with implementation vocabulary |

### SBPP-BEH-18:4 - Solution — Name methods after what they accomplish (intent), not how they work

Name every method after the result it produces or the action it performs in domain terms.
Never name after the algorithm or data structure used. A reader should be able to guess
what a method does from its name without reading its body.

**Java naming guidelines:**

```java
// ❌ Implementation-revealing names
public List<Policy> linearSearchPolicies(String holderId) { ... }
public void setBooleanFlagToTrueForActivation() { ... }
public BigDecimal computeWithLookupTable(Policy p, RiskMatrix m) { ... }

// ✅ Intention-revealing names
public List<Policy> findPoliciesFor(CustomerId holderId) { ... }
public void activate() { ... }
public BigDecimal calculatePremium(Policy policy) { ... }

// ✅ More examples
public boolean isEligibleForDiscount() { ... }    // not: checkDiscountBooleanValue()
public Money applyTo(Money base) { ... }           // not: runAdjustmentCalculation()
public Order placeWith(Cart cart) { ... }          // not: executeOrderCreation()
```

**Kotlin naming guidelines:**

```kotlin
// Kotlin val/var properties as intention-revealing selectors
val isExpired: Boolean get() = expiryDate.isBefore(LocalDate.now())   // not: checkExpiry()
val netPremium: Money get() = grossPremium - discounts.total()         // not: getPremiumAfterDiscounts()

// Extension functions — intention in the extension name
fun Policy.renewFor(years: Int): Policy = copy(expiryDate = expiryDate.plusYears(years.toLong()))
```

**Naming vocabulary by method type:**

| Method Type | Preferred Prefix | Example |
|-------------|-----------------|---------|
| Boolean query | `is`, `has`, `can`, `was` | `isExpired()`, `hasOpenClaims()` |
| Action (command) | Verb | `activate()`, `cancel()`, `submit()` |
| Factory | `of`, `from`, `create`, `build` | `Money.of(100, USD)` |
| Conversion | `to` | `toDecimal()`, `toDto()` |
| Search/retrieval | `find`, `get` | `findById()`, `getPolicies()` |
| Calculation | `calculate`, `compute` | `calculatePremium()` |

### SBPP-BEH-18:5 - Archetypal Grounding

**U.System:** `findPoliciesFor(holderId)` — a reader knows this searches for policies; implementation irrelevant.
**U.Episteme:** When the underlying search changes from linear to hash-based, the name `findPoliciesFor` survives unchanged; `linearSearchPolicies` would need renaming.

### SBPP-BEH-18:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin method naming**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Names are subjective; teams disagree on "good" names | Establish team naming guidelines; use code review for naming quality |
| **Arch** | Intent-based names can be vague (`process()`, `handle()`) | Apply domain vocabulary; vague verbs are as bad as technical ones |
| **Onto/Epist** | Names encode current understanding of intent, which evolves | Rename aggressively as understanding improves; IDE refactoring makes this cheap |
| **Prag** | Java's verbosity limits name length; Kotlin's terseness can go too far | Balance: enough words to be clear, few enough to scan |
| **Did** | New developers default to technical names because they know the implementation | Review names; ask "would a domain expert understand this name?" |

### SBPP-BEH-18:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH18-1** | Method names SHALL communicate intent (what), not implementation (how). | Decouples name from implementation |
| **CC-BEH18-2** | Names SHOULD use domain vocabulary recognisable to non-developers. | Enforces Ubiquitous Language |
| **CC-BEH18-3** | Names MUST NOT encode the data structure or algorithm used (`hashSearch`, `arraySort`). | Prevents coupling name to implementation |
| **CC-BEH18-4** | Boolean query methods SHALL use `is`/`has`/`can`/`was` prefix per CC-BEH07-1. | Consistency with Query Method pattern |

### SBPP-BEH-18:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Algorithm-Encoding Name**
`binarySearchForPolicy()` — fix: `findPolicy()`.

**Anti-pattern 2: Hungarian Notation**
`strPolicyId`, `boolIsActive`, `lstPolicies` — fix: `policyId`, `isActive`, `policies`.

**Anti-pattern 3: Vague Manager/Helper/Util Names**
`PolicyHelper.doStuff()` — fix: name after the specific operation: `PolicyRenewalEligibilityChecker.isEligible()`.

### SBPP-BEH-18:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Code reads as prose; cognitive load drops | Investment in naming upfront — paid back immediately |
| Refactoring implementations does not require renaming | — |
| Code review focuses on intent, not mechanics | — |

### SBPP-BEH-18:10 - Rationale

Intention Revealing Selector is the single most impactful naming principle in Beck's
work. It subsumes most of "Clean Code" Chapter 2 and is the practical application of
Ubiquitous Language in DDD. In Java/Kotlin, the principle applies to methods, fields,
variables, classes, and packages.

### SBPP-BEH-18:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code ch.2 (Martin, 2008/ongoing):** "Use intention-revealing names" is chapter 2's
central principle. *Adopt.*

**DDD Ubiquitous Language (Evans/Vernon, 2016):** Domain vocabulary in code names.
*Adopt.*

**Google Java Style Guide (Google, continuously updated):** Prescribes intent-based naming
conventions aligned with this pattern. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code ch.2 (Martin, ongoing) | Intention-revealing names | **Adopt** |
| DDD Ubiquitous Language (Vernon, 2016) | Domain vocab in names | **Adopt** |
| Google Java Style Guide (2015+) | Naming conventions | **Adopt** |

### SBPP-BEH-18:12 - Relations

* **Foundation for:** All other patterns (all depend on good naming)
* **Implements:** DDD Ubiquitous Language, Clean Code naming
* **Paired with:** SBPP-BEH-17 (Intention Revealing Message — applying the name)
* **Constrains:** All methods in the codebase

### SBPP-BEH-18:End
