## SBPP-BEH-16 - Decomposing Message

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-16:1 - Problem frame

When a method grows too large in a Java/Kotlin microservice, it needs to be broken into
smaller parts. Unlike Composed Method (BEH-01), which focuses on abstraction levels,
Decomposing Message focuses on the act of calling a sub-operation by name — the message
send itself — as the primary mechanism of decomposition and communication.

### SBPP-BEH-16:2 - Problem

How do you break a computation into named parts that can be understood independently,
reused across methods, and overridden by subclasses?

### SBPP-BEH-16:3 - Forces

| Force | Tension |
|-------|---------|
| **Comprehension** | Named sub-operations explain the structure ↔ too many hops to follow the code |
| **Reuse** | Extracted sub-operation is callable from other methods ↔ premature extraction fragments logic |
| **Overridability** | Extracted method can be overridden in subclasses (Template Method) ↔ unintended override points |

### SBPP-BEH-16:4 - Solution — Name and extract sub-computations as separate methods; call by name

Extract any logically distinct step of a computation into a private or protected method.
Name it with an intention-revealing verb phrase. Call it by name in the decomposed method.
This is the inverse of inlining — deliberately making the named call the unit of composition.

**Java example:**

```java
// ❌ Monolithic
public PolicyDecision underwrite(Application application) {
    // 50 lines of mixed concerns
}

// ✅ Decomposed — each step is named and delegated
public PolicyDecision underwrite(Application application) {
    RiskProfile profile = buildRiskProfile(application);
    List<RuleViolation> violations = checkUnderwritingRules(profile);
    if (!violations.isEmpty()) return PolicyDecision.decline(violations);
    Money premium = calculatePremium(profile);
    return PolicyDecision.accept(premium, buildConditions(profile));
}

private RiskProfile buildRiskProfile(Application app) { ... }
private List<RuleViolation> checkUnderwritingRules(RiskProfile profile) { ... }
private Money calculatePremium(RiskProfile profile) { ... }
private List<Condition> buildConditions(RiskProfile profile) { ... }
```

**Kotlin:**

```kotlin
fun underwrite(application: Application): PolicyDecision {
    val profile    = buildRiskProfile(application)
    val violations = checkUnderwritingRules(profile)
    if (violations.isNotEmpty()) return PolicyDecision.decline(violations)
    val premium    = calculatePremium(profile)
    return PolicyDecision.accept(premium, buildConditions(profile))
}
```

### SBPP-BEH-16:5 - Archetypal Grounding

**U.System:** `underwrite()` reads as five named steps; each step's name explains its purpose.
**U.Episteme:** Extracting `checkUnderwritingRules()` makes the business rule validation independently
testable and documentable without reading the underwriting algorithm.

### SBPP-BEH-16:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Method decomposition in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | No limit on decomposition depth; can create deep call chains | Keep decomposition to 2 levels of nesting; use Method Object for deeper algorithms |
| **Arch** | `protected` methods are unintentional override points | Use `private` by default; only use `protected` when override is intentional (Template Method) |
| **Onto/Epist** | Naming is the hard part; poor names harm more than help | Practice naming via pair review; reject vague names like `processStep1` |
| **Prag** | IDE "Extract Method" refactoring makes this a one-keystroke operation | Use it aggressively during cleanup; treat long methods as a smell |
| **Did** | New developers may not recognise when a sub-operation has been extracted enough | Teach: if the body of an extracted method needs another comment, extract further |

### SBPP-BEH-16:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH16-1** | Methods longer than ~20 lines SHOULD be decomposed into named sub-operations. | Controls complexity |
| **CC-BEH16-2** | Extracted methods SHALL be named with verb phrases that reveal the sub-operation's intent. | Self-documentation |
| **CC-BEH16-3** | Extracted methods SHOULD be `private` unless intentional override (Template Method) is designed. | Prevents accidental override |

### SBPP-BEH-16:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Meaningless Names**
`private void step1()`, `private void processHelper()` — names add no information.
Fix: Name after what the method *does* for the business: `checkFraudRules()`, `applyDiscounts()`.

**Anti-pattern 2: Over-Decomposition**
Every two-line block becomes a method: `private boolean isNull(Object x) { return x == null; }`.
Fix: Extract only when the name reveals intent beyond what the code itself shows.

### SBPP-BEH-16:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Sub-operations are independently testable | More private methods per class |
| Algorithm structure is visible in the top-level method | Call chain to follow — mitigated by IDE navigation |
| Common sub-operations can be reused across methods | — |

### SBPP-BEH-16:10 - Rationale

Decomposing Message is the mechanism behind every good decomposition. It is distinct from
Composed Method in emphasis: Composed Method focuses on abstraction level uniformity;
Decomposing Message focuses on the extraction and naming of sub-operations.
In practice they are applied together.

### SBPP-BEH-16:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Refactoring 2nd ed. — "Extract Function" (Fowler, 2018):** The primary refactoring
technique. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** "Functions should do one thing." Decomposing Message
is the mechanism. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Refactoring 2nd ed. (Fowler, 2018) | "Extract Function" | **Adopt** |
| Clean Code (Martin, ongoing) | One-thing functions | **Adopt** |
| IntelliJ IDEA "Extract Method" (JetBrains, post-2015) | Tooling support | **Adopt** |

### SBPP-BEH-16:12 - Relations

* **Specialises:** SBPP-BEH-01 (Composed Method — decomposition is the mechanism)
* **Enables:** SBPP-BEH-14 (Message — named methods are the messages)
* **Relates to:** SBPP-BEH-10 (Method Object — when decomposition still leaves shared state)

### SBPP-BEH-16:End
