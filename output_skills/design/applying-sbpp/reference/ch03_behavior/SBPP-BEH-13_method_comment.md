## SBPP-BEH-13 - Method Comment

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-13:1 - Problem frame

Developers in Java/Kotlin teams face a recurring choice: when, and how much, to comment
a method. Over-commenting drowns code in noise that quickly becomes outdated; under-commenting
leaves intent invisible. The pattern establishes when a comment adds genuine value versus
when the code should be rewritten to be self-documenting.

### SBPP-BEH-13:2 - Problem

How do you comment methods so that comments add genuine value by explaining things the
code cannot express, without creating noise that must be maintained alongside the code?

### SBPP-BEH-13:3 - Forces

| Force | Tension |
|-------|---------|
| **Intent Communication** | Comments explain why ↔ code shows what/how |
| **Maintenance Burden** | Comments must stay accurate ↔ code changes but comments lag |
| **Readability** | Well-named methods need no comment ↔ complex algorithms benefit from explanation |

### SBPP-BEH-13:4 - Solution — Comment the why, not the what; communicate intent the code cannot

Write a comment only when:
1. The method does something non-obvious and the *reason* cannot be encoded in the name.
2. There is a known performance trade-off, algorithm choice, or business rule that a reader would question.
3. A public API method needs Javadoc/KDoc for IDE documentation.

Do **not** comment when: the method name and body are self-explanatory, or when a better
method name would make the comment redundant.

**Java example — good comment use:**

```java
/**
 * Calculates the loading factor for the policy.
 * Uses a lookup table rather than formula because the actuarial table
 * is regulatory-mandated and cannot be expressed as a closed-form equation.
 * See: Actuarial Guidelines AG-47 (2023).
 */
private double computeLoadingFactor(Policy policy, RiskScore score) {
    return regulatoryTable.lookup(policy.getCategory(), score);
}

// Comment explaining non-obvious defensive code
// String interning here prevents memory leaks in the rate-cache under
// heavy load (see ADR-0042); do not remove without profiling.
String rateKey = rateCode.intern();
```

**Java example — comments that should be removed (code speaks for itself):**

```java
// BAD: comment just restates what the code says
// Check if policy is expired
if (policy.isExpired()) {
    // throw exception
    throw new PolicyExpiredException(policy.getId());
}
```

**Kotlin example — KDoc for public API:**

```kotlin
/**
 * Calculates the net premium after all applicable adjustments.
 *
 * @param adjustments list of adjustments to apply; order matters
 *   (discounts are applied before surcharges per underwriting rule UR-12)
 * @return the adjusted premium; never negative
 * @throws IllegalStateException if base premium has not been set
 */
fun calculateNetPremium(adjustments: List<Adjustment>): Money {
    check(basePremium != null) { "Base premium must be set before calling calculateNetPremium" }
    return adjustments.fold(basePremium) { acc, adj -> adj.applyTo(acc) }
}
```

### SBPP-BEH-13:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Comments explain regulatory constraints, non-obvious trade-offs, and business rules that cannot be encoded in names.
*Show:* `// Uses actuarial table AG-47; formula not available` explains a constraint invisible in the code.

**U.Episteme (design reasoning):**
*Tell:* A comment that says what the code does is noise; a comment that says why is signal.
*Show:* Deleting a comment that says "// check if expired" changes nothing; a reader sees `isExpired()` and knows.

### SBPP-BEH-13:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin method commenting**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | No static analysis enforces "why, not what" commenting quality | Code review is the only gate; provide examples of good/bad comments in team guidelines |
| **Arch** | Javadoc/KDoc on internal methods is often unnecessary overhead | Restrict mandatory documentation to public API; discourage for private methods |
| **Onto/Epist** | Comments encode assumptions that may become false | Date sensitive comments; link to issues/ADRs instead of embedding long explanations |
| **Prag** | Well-named, composed methods make comments redundant in most cases | Invest in naming before adding a comment |
| **Did** | New developers may feel obligated to comment everything | Teach: if you need a comment to explain what the code does, rename or refactor first |

### SBPP-BEH-13:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH13-1** | Public API methods SHALL have Javadoc/KDoc documenting purpose, parameters, returns, and throws. | IDE and tooling documentation |
| **CC-BEH13-2** | Inline comments SHOULD explain "why", not "what" — the code itself documents what. | Prevents redundant noise |
| **CC-BEH13-3** | Comments MUST NOT contradict the code; outdated comments SHALL be removed or updated. | Prevents misleading documentation |
| **CC-BEH13-4** | Non-obvious algorithms or business rules SHOULD reference their source (ticket, ADR, standard). | Preserves rationale |

### SBPP-BEH-13:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Commented-Out Code**
```java
// order.calculateOldTax();  // removed 2023-05-01
```
Fix: Delete; version control tracks history.

**Anti-pattern 2: Stale Comment**
```java
// Returns true if status is ACTIVE
public boolean isEligible() {
    return status == ACTIVE || status == PENDING;  // ← comment is wrong
}
```
Fix: Update comment or rewrite method; reject in code review.

### SBPP-BEH-13:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Comments carry only real information, making them trusted | Fewer comments mean more pressure on naming quality — which is healthy |
| Maintenance burden reduced (less to keep accurate) | Non-obvious code without comments is still hard to read — invest in self-documentation first |
| Public API documentation serves IDE and auto-doc tooling | — |

### SBPP-BEH-13:10 - Rationale

Beck's comment philosophy — "communicate intent the code cannot" — is universally adopted
in modern Java/Kotlin teams. Clean Code's rule ("don't comment what you can express in code")
is the most widely cited version. The modern addition is the requirement to document public APIs
with Javadoc/KDoc for tooling consumption.

### SBPP-BEH-13:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008/ongoing):** Chapter 4 ("Comments") argues that the best comment is
one you can avoid by writing expressive code. Retain only comments that explain *why*. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 56 ("Write doc comments for all exposed API elements").
Public Javadoc is mandatory; private methods do not require it. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code ch.4 (Martin, 2008/ongoing) | Why-not-what commenting | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 56 — public Javadoc | **Adopt** |
| KDoc (JetBrains, post-2016) | Kotlin API documentation | **Adopt** |

### SBPP-BEH-13:12 - Relations

* **Paired with:** SBPP-BEH-01 (Composed Method — good decomposition eliminates most comments)
* **Paired with:** SBPP-BEH-18 (Intention Revealing Selector — good naming eliminates most comments)
* **Constrains:** Comments MUST be kept accurate as code evolves

### SBPP-BEH-13:End
