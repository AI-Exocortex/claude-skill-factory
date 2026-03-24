## SBPP-STA-15 - Temporary Variable

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-15:1 - Problem frame

Within a method body, some intermediate values need to be stored temporarily — to avoid
recomputing them, to name them for clarity, or to hold a result that changes as the
method executes. The decision of when to introduce a local variable and what to name it
directly affects method readability.

### SBPP-STA-15:2 - Problem

How do you use local variables (temporary variables) within a method body so that they
improve rather than obscure the method's readability?

### SBPP-STA-15:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Named variable explains an intermediate value ↔ introduces state to track |
| **Performance** | Cache expensive computation in a local ↔ premature optimisation |
| **Scope** | Local variable is scoped to the method ↔ needs documentation of its role |

### SBPP-STA-15:4 - Solution — Introduce locals only when they name something, cache something, or reuse something

A local variable is justified when it:
1. **Names** an intermediate value (Explaining Temporary Variable — STA-18)
2. **Caches** an expensive or side-effecting expression (Caching Temporary Variable — STA-17)
3. **Collects** accumulated results (Collecting Temporary Variable — STA-16)
4. **Reuses** a value that can only be computed once (Reusing Temporary Variable — STA-19)

**Java example:**

```java
public Money calculateNetPremium(Policy policy, List<Adjustment> adjustments) {
    // ✅ Naming intermediate: explains what basePremium is
    Money basePremium = policy.getBasePremium();

    // ✅ Collecting: accumulates adjustments
    Money totalAdjustment = adjustments.stream()
        .map(adj -> adj.applyTo(basePremium))
        .reduce(Money.ZERO, Money::add);

    // ✅ Naming final result for clarity
    Money netPremium = basePremium.add(totalAdjustment);

    return netPremium;
}
```

**Kotlin:**

```kotlin
fun calculateNetPremium(policy: Policy, adjustments: List<Adjustment>): Money {
    val basePremium = policy.basePremium
    val totalAdjustment = adjustments.fold(Money.ZERO) { acc, adj -> acc + adj.applyTo(basePremium) }
    return basePremium + totalAdjustment
}
```

**Rule:** Every local variable should earn its place by naming something, caching something,
or collecting something. A local that just copies a value unnecessarily is noise.

### SBPP-STA-15:5 - Archetypal Grounding

**U.System:** `val basePremium = policy.basePremium` — gives the intermediate value a name that explains its role.
**U.Episteme:** A method with well-named locals reads like a series of named steps; one with anonymous expressions does not.

### SBPP-STA-15:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Local variable use in Java/Kotlin methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | No compiler enforcement of naming quality | Code review is the gate |
| **Arch** | Kotlin `val` encourages immutable locals by default | Use `val` unless mutation is required; avoid `var` |
| **Onto/Epist** | "Unnecessary" local is subjective | Apply the four-criteria test: name, cache, collect, or reuse |
| **Prag** | Kotlin's expression-based syntax often eliminates the need for intermediate locals | Use expressions inline when they're readable without naming |
| **Did** | Teach the four roles of temporary variables | Pair each type with a named pattern (STA-16 through STA-19) |

### SBPP-STA-15:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA15-1** | Local variables SHALL be introduced only when they name, cache, collect, or reuse an intermediate value. | Prevents gratuitous locals |
| **CC-STA15-2** | Kotlin local variables SHOULD be `val` (immutable) unless mutation is required. | Immutability |
| **CC-STA15-3** | Java local variables SHOULD be declared with `var` (Java 10+) when type is obvious from context. | Conciseness |
| **CC-STA15-4** | Local variable names SHALL follow SBPP-STA-20 (role-suggesting names). | Readability |

### SBPP-STA-15:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Unnecessary copy**
```java
PolicyStatus s = policy.getStatus();  // only used once in next line
if (s == ACTIVE) { ... }
```
Fix: `if (policy.getStatus() == ACTIVE) { ... }` — no intermediate needed.

**Anti-pattern 2: Single-letter locals**
```java
Money x = calculateBase();
Money y = x.add(adjustment);
```
Fix: `basePremium`, `adjustedPremium`.

### SBPP-STA-15:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Named locals make method intent readable | Extra lines — justified by clarity |
| Kotlin `val` makes locals immutable by default | — |
| Reduces cognitive load in complex methods | — |

### SBPP-STA-15:10 - Rationale

Temporary Variables are a fundamental tool. The pattern's value is in the discipline it
encodes: only introduce a local when it earns its place by naming, caching, collecting,
or reusing. Kotlin's expression-oriented style often eliminates the need for intermediate
locals that Java would require.

### SBPP-STA-15:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008/ongoing):** "Explanatory variables" — extract complex expressions
into named locals for clarity. *Adopt.*

**Kotlin `val` (JetBrains, post-2016):** Default-immutable locals. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, ongoing) | Explanatory variables | **Adopt** |
| Kotlin `val` (post-2016) | Immutable locals by default | **Adopt** |
| Java 10 `var` (JEP 286) | Type inference for locals | **Adopt** |

### SBPP-STA-15:12 - Relations

* **Foundation for:** STA-16 through STA-19 (specific uses of temporary variables)
* **Named by:** SBPP-STA-20 (Role Suggesting Temporary Variable Name)
* **Provides context for:** Composed Methods (BEH-01) through their local state

### SBPP-STA-15:End
