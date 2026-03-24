## SBPP-FMT-01 - Inline Message Pattern

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-FMT-01:1 - Problem frame

In Java/Kotlin, method signatures can grow long — especially with modern descriptive
naming. The question of whether to break a method signature across multiple lines,
and when, directly affects how quickly a reader can scan a file. Vertical space is
precious: a method signature that takes four lines leaves less room for the body.

### SBPP-FMT-01:2 - Problem

How do you format a method signature (name + parameters) so that it is readable
without consuming vertical space that should belong to the method body?

### SBPP-FMT-01:3 - Forces

| Force | Tension |
|-------|---------|
| **Scannability** | Single-line signatures are easy to scan ↔ very long signatures require horizontal scrolling |
| **Vertical economy** | Compact signatures leave room for the body ↔ wrapping can aid readability for long signatures |
| **Tooling** | IDEs show the signature separately; team formatters (Checkstyle, ktlint) enforce line length | |

### SBPP-FMT-01:4 - Solution — Keep method signatures on one line up to the team line-length limit; wrap parameters one-per-line when the limit is exceeded

**Java — short signature, inline (always preferred):**

```java
// ✅ One line — fits within 120 chars
public Money calculatePremium(Policy policy, RiskContext context) { ... }

// ✅ Still one line
public Optional<Policy> findActivePolicy(CustomerId customerId, ProductCode product) { ... }
```

**Java — long signature, wrap parameters one-per-line:**

```java
// ✅ Wrap when exceeding line length limit (120 chars common)
public RatingResult calculateRating(
        Policy policy,
        RiskProfile riskProfile,
        RegulatoryZone zone,
        EffectiveDate effectiveDate) {
    // body
}
```

**Kotlin — short signature, inline:**

```kotlin
fun calculatePremium(policy: Policy, context: RiskContext): Money { ... }

fun findActivePolicy(customerId: CustomerId, product: ProductCode): Policy? { ... }
```

**Kotlin — long signature, one-per-line with trailing comma:**

```kotlin
fun calculateRating(
    policy: Policy,
    riskProfile: RiskProfile,
    zone: RegulatoryZone,
    effectiveDate: EffectiveDate,   // trailing comma enables easier future additions
): RatingResult {
    // body
}
```

**Annotation-heavy signatures — always wrap:**

```java
// ✅ Each annotation + parameter on its own line
public ResponseEntity<PolicyDto> createPolicy(
        @RequestBody @Valid PolicyRequest request,
        @PathVariable String tenantId,
        @AuthenticationPrincipal UserDetails user) {
    // body
}
```

**Kotlin:**

```kotlin
fun createPolicy(
    @RequestBody @Valid request: PolicyRequest,
    @PathVariable tenantId: String,
): ResponseEntity<PolicyDto> { ... }
```

### SBPP-FMT-01:5 - Archetypal Grounding

**U.System:** A Kotlin function with four parameters fits inline at 100 chars; adding a fifth
makes it 130 chars, triggering the one-per-line wrap — a clear mechanical rule that ktlint
enforces automatically.

**U.Episteme:** The signature is a contract declaration. Keeping it dense and scannable
lets a reader find and parse method contracts quickly when navigating a class.

### SBPP-FMT-01:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin method signature formatting**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Line-length limit varies by team (80, 100, 120, 140 chars) — choose one and enforce consistently | Configure Checkstyle / ktlint with the team limit; never leave it unenforced |
| **Arch** | A signature with > 4 parameters is a design smell regardless of how it is formatted | Apply this pattern; also review whether the parameter count indicates a design problem |
| **Onto/Epist** | "Inline" does not mean "squeeze everything together" — adequate spacing around commas is required | `calculatePremium(policy,context)` — no. `calculatePremium(policy, context)` — yes |
| **Prag** | ktlint and Spotless auto-format Kotlin and Java respectively — this is tooling-solved | Enable auto-format on save; this pattern becomes a zero-effort default |
| **Did** | New developers may manually format signatures inconsistently | Require formatter configuration in the project setup; CI gate on format compliance |

### SBPP-FMT-01:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT01-1** | Method signatures SHOULD fit on one line when within the team's configured line-length limit. | Vertical economy |
| **CC-FMT01-2** | When the signature exceeds the line-length limit, each parameter SHALL appear on its own line, indented consistently. | Readability when wrapping |
| **CC-FMT01-3** | Kotlin wrapped signatures SHOULD use trailing commas on the last parameter. | Enables cleaner diff history |
| **CC-FMT01-4** | Signature formatting SHALL be enforced by a configured formatter (Checkstyle/ktlint/Spotless). | Automated compliance |

### SBPP-FMT-01:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Arbitrary mid-line wrapping**
```java
public Money calculatePremium(Policy policy,
    RiskContext context) { }   // inconsistent indent
```
Fix: wrap at the first parameter and align all subsequent parameters at the same indent level.

**Anti-pattern 2: Wrapping short signatures unnecessarily**
```java
public void activate(
        PolicyId id) { }   // 25 chars — no reason to wrap
```
Fix: `public void activate(PolicyId id) { }`.

### SBPP-FMT-01:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Vertical space preserved for the body | Line-length limit must be agreed and enforced |
| Consistent wrap style aids scanning | Auto-formatter removes the manual burden |
| Trailing commas (Kotlin) improve diff readability | — |

### SBPP-FMT-01:10 - Rationale

Beck's Inline Message Pattern addresses the trade-off between horizontal and vertical
space in method headers. In Java/Kotlin this maps to the line-length limit enforced by
formatters. The core principle — "keep the signature compact to leave room for the body"
— applies directly.

### SBPP-FMT-01:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Google Java Style Guide (continuously updated post-2015):** 100-character line limit;
parameter wrapping one-per-line when exceeded. *Adopt.*

**ktlint (JetBrains / community, post-2016):** Enforces Kotlin coding conventions including
signature wrapping at configured line length. *Adopt — automate via ktlint.*

**Spotless / Checkstyle (post-2015):** Java formatter enforcement. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Google Java Style Guide (post-2015) | Line limit + wrap rules | **Adopt** |
| ktlint (post-2016) | Automated enforcement | **Adopt** |
| Kotlin Coding Conventions (JetBrains, post-2016) | Trailing commas; one-per-line wrap | **Adopt** |

### SBPP-FMT-01:12 - Relations

* **Enables:** SBPP-FMT-02 (Type Suggesting Parameter Name — the names in the signature)
* **Relates to:** SBPP-FMT-03 (Indented Control Flow — body indentation uses the same principles)
* **Constrained by:** Team-configured line-length limit (Checkstyle / ktlint)

### SBPP-FMT-01:End
