## SBPP-STA-20 - Role Suggesting Temporary Variable Name

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-20:1 - Problem frame

Local variable names have a short scope (one method body), but poor names — `temp`, `x`,
`result`, `val` — still obscure intent within that scope. Good local variable names
communicate the role the value plays in the computation, making the method readable
without requiring readers to trace the value to its source.

### SBPP-STA-20:2 - Problem

What do you name a local variable so that a reader immediately understands its role in
the method without examining the expression that assigned it?

### SBPP-STA-20:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Role-based name explains purpose ↔ longer names take more time to type |
| **Scope** | Short scope means shorter names may suffice ↔ names still need to be meaningful |
| **Type** | Type is already inferred/declared ↔ don't repeat type in the name |

### SBPP-STA-20:4 - Solution — Name locals after their role in the computation; use domain vocabulary

```java
// ❌ Generic, type-redundant, or meaningless names
List<Policy> list       = repository.findAll();
Money        amount     = policy.getPremium();
LocalDate    date       = policy.getExpiryDate();
boolean      flag       = policy.isActive();
int          counter    = 0;
Object       temp       = getRiskMatrix();

// ✅ Role-based names — domain vocabulary
List<Policy>    activePolicies  = repository.findAllActive();
Money           basePremium     = policy.getPremium();
LocalDate       expiryDate      = policy.getExpiryDate();
boolean         isEligible      = policy.isActive() && policy.hasValidCoverage();
int             claimCount      = 0;
RiskMatrix      riskMatrix      = getRiskMatrix();
```

**Kotlin:**

```kotlin
// ✅ Role-based Kotlin locals
val activePolicies = repository.findAllActive()
val basePremium    = policy.premium
val expiryDate     = policy.expiryDate
val isEligible     = policy.isActive && policy.hasValidCoverage
val riskMatrix     = loadRiskMatrix()
```

**Naming vocabulary for locals:**

| Purpose | Pattern | Example |
|---------|---------|---------|
| Domain object | domain-noun | `policy`, `claim`, `customer` |
| Amount/money | role + no type suffix | `basePremium`, `netDiscount`, `taxAmount` |
| Boolean condition | `is`/`has`/`can` prefix | `isEligible`, `hasOpenClaims` |
| Accumulator | what is being accumulated | `totalPremium`, `errors`, `results` |
| Cached value | same as the expression | `riskMatrix`, `expiryDate`, `today` |
| Loop variable | domain-meaningful | `policy`, `claim` (not `p`, `c`, `i`) |

### SBPP-STA-20:5 - Archetypal Grounding

**U.System:** `val basePremium = policy.premium` — the local name `basePremium` tells the reader what role this money value plays.
**U.Episteme:** `val x = policy.premium` forces the reader to remember what `x` represents throughout the method.

### SBPP-STA-20:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Local variable naming in Java/Kotlin methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | No static enforcement of naming quality | Code review is the primary gate |
| **Arch** | Kotlin `var`/`val` type inference means type is often invisible — name is the only guide | Even more reason to use role-based names in Kotlin |
| **Onto/Epist** | Loop variable convention (`i`, `j`) conflicts with role-based naming | Use domain-meaningful names even in loops: `for (policy in policies)` |
| **Prag** | IDEs auto-suggest names from types: `localDate` for `LocalDate` — type-based | Override IDE suggestion with role-based name |
| **Did** | Demonstrate the readability difference with a real before/after | Show a method with `temp`, `x`, `result` vs one with role names |

### SBPP-STA-20:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA20-1** | Local variable names SHALL communicate role, not implementation type. | Readability |
| **CC-STA20-2** | Generic names (`temp`, `x`, `result`, `data`, `value`) MUST NOT be used. | Prevents meaningless names |
| **CC-STA20-3** | Loop variables over domain collections SHOULD use the domain singular: `for (Policy policy : policies)`. | Domain vocabulary |
| **CC-STA20-4** | Boolean locals SHOULD use `is`/`has`/`can` prefix. | Consistency |

### SBPP-STA-20:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Single-letter variable**
`for (Policy p : policies)` — Fix: `for (Policy policy : policies)`.

**Anti-pattern 2: Type-based name**
`LocalDate localDate = policy.getExpiryDate();` — Fix: `LocalDate expiryDate = ...`.

**Anti-pattern 3: Generic accumulator**
`List<String> result = ...` — Fix: `List<String> errorMessages = ...`.

### SBPP-STA-20:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Method body reads like a sequence of named steps | Longer names — justified always |
| Readers don't need to trace variables to understand them | — |

### SBPP-STA-20:10 - Rationale

Role Suggesting Temporary Variable Name is the local-variable application of
Intention Revealing Selector (BEH-18). The same principle applies: name after the role,
not after the type or the mechanism. Kotlin's type inference makes this even more
important — the name is often the only documentation of a value's purpose.

### SBPP-STA-20:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code ch.2 (Martin, 2008/ongoing):** Intention-revealing names at all scopes. *Adopt.*
**Google Java Style (Google, post-2015):** No single-letter names (except loop indices in mathematical code). *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code ch.2 (Martin, ongoing) | Intention-revealing names | **Adopt** |
| Google Java Style (post-2015) | No single-letter names | **Adopt** |
| Kotlin type inference (post-2016) | Name is primary documentation | **Adopt** |

### SBPP-STA-20:12 - Relations

* **Specialises:** SBPP-BEH-18 (Intention Revealing Selector — applied to locals)
* **Parallel:** SBPP-STA-14 (Role Suggesting Instance Variable Name — for fields)
* **Applies to:** All uses of SBPP-STA-15 through STA-19

### SBPP-STA-20:End
