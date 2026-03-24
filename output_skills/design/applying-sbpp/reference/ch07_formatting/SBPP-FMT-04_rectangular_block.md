## SBPP-FMT-04 - Rectangular Block

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-FMT-04:1 - Problem frame

Beck's Rectangular Block addressed formatting Smalltalk block literals (`[...]`) so their
boundaries were visually clear. In Java/Kotlin, the equivalent is formatting lambda
expressions and code blocks (`{ }`) so that single-expression lambdas stay inline and
multi-statement lambdas are expanded into a recognisable rectangular shape.

### SBPP-FMT-04:2 - Problem

How do you format lambda bodies and anonymous blocks so that a reader can immediately
distinguish single-expression lambdas from multi-statement ones, and can easily
locate the block's boundaries?

### SBPP-FMT-04:3 - Forces

| Force | Tension |
|-------|---------|
| **Compactness** | Single-expression lambdas inline ↔ long inline lambdas are unreadable |
| **Visual boundaries** | Braces make start/end explicit ↔ arrow syntax omits braces for single expressions |
| **Consistency** | One style for all lambdas ↔ inline vs block style serves different cases |

### SBPP-FMT-04:4 - Solution — Inline single-expression lambdas; expand multi-statement lambdas into rectangular blocks

**Java lambdas:**

```java
// ✅ Single expression — inline, no braces needed
policies.stream().filter(p -> p.isActive());
policies.stream().map(Policy::getPremium);

// ✅ Single expression with method chain — still inline if fits in line
policies.stream().filter(p -> p.isActive() && p.getPremium().compareTo(MIN) > 0);

// ✅ Multi-statement — expand to rectangular block
policies.stream().forEach(policy -> {        // opening brace on same line as arrow
    validatePolicy(policy);
    enrichPolicy(policy);
    persistPolicy(policy);
});                                           // closing brace on its own line

// ✅ Lambda that returns — explicit return in block form
Function<Policy, Money> calculator = policy -> {
    RiskProfile risk = riskService.assess(policy);
    return premiumTable.lookup(risk);
};
```

**Kotlin lambdas (function literals):**

```kotlin
// ✅ Single expression — trailing lambda, no braces for body needed (idiomatic)
policies.filter { it.isActive }
policies.map { it.premium }

// ✅ Multi-statement trailing lambda — expand to rectangular block
policies.forEach {
    validatePolicy(it)       // body indented inside braces
    enrichPolicy(it)
    persistPolicy(it)
}                            // closing brace alone on its own line

// ✅ Named parameter in multi-statement lambda
policies.forEachIndexed { index, policy ->
    log.info("[$index] Processing ${policy.id}")
    process(policy)
}

// ✅ Lambda stored in variable
val calculator: (Policy) -> Money = { policy ->
    val risk = riskService.assess(policy)
    premiumTable.lookup(risk)
}
```

**The rectangle rule applied:**

```
Single expression: [ opening-brace ]  expression  [ closing-brace ]  — keep on one line
Multi-statement:   opening-brace
                       statement1
                       statement2
                   closing-brace                                      — rectangle shape
```

### SBPP-FMT-04:5 - Archetypal Grounding

**U.System:** `policies.forEach { validatePolicy(it); enrichPolicy(it) }` — the braces form
a clear rectangle; the reader can find the block boundary without parsing the content.

**U.Episteme:** In Kotlin, `{ it.isActive }` vs `{ policy -> validatePolicy(policy); enrichPolicy(policy) }` — the visual density signals single-expression vs multi-step immediately.

### SBPP-FMT-04:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Lambda and block formatting in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Multi-statement lambdas are often a code smell — extract to a method | If the lambda has > 3 statements, extract it as a named method and use a method reference |
| **Arch** | Auto-formatters handle this — manual rectangle formatting is unnecessary | Let the formatter decide; never override it |
| **Onto/Epist** | Kotlin trailing lambda syntax (`{ }` outside parens) is idiomatic only for the last parameter | Use trailing lambda for single-argument or last-argument lambdas only |
| **Prag** | IntelliJ/ktlint will expand a multi-statement inline lambda automatically | Rely on the tool |
| **Did** | Teach: "if the lambda body has a name, the lambda is too big — extract it" | |

### SBPP-FMT-04:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT04-1** | Single-expression lambdas SHOULD be written without braces (Kotlin) or with braces and no line break (Java). | Compactness |
| **CC-FMT04-2** | Multi-statement lambdas SHALL use the rectangular block form: opening brace at end of previous line, body indented, closing brace on its own line. | Visual block boundary |
| **CC-FMT04-3** | Lambdas with > 3 statements SHOULD be extracted to a named method; the lambda becomes a method reference. | Keeps blocks small and nameable |

### SBPP-FMT-04:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Multi-statement lambda inline**
`policies.forEach(p -> { validate(p); enrich(p); persist(p); });`
Fix: expand to rectangular block.

**Anti-pattern 2: Giant lambda that should be a method**
10-line lambda body. Fix: extract to a named method (`this::processPolicy`); use a method reference.

### SBPP-FMT-04:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Block boundaries visually clear | Multi-statement blocks are a smell — prefer extraction |
| Auto-formatter handles this | — |

### SBPP-FMT-04:10 - Rationale

Beck's visual "rectangle" principle applies directly to lambda formatting. Single-expression
lambdas stay dense; multi-statement lambdas expand into a clearly bounded rectangle.
Kotlin's trailing lambda syntax is the closest modern equivalent to Smalltalk's `[...]` blocks.

### SBPP-FMT-04:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Kotlin Coding Conventions (JetBrains, post-2016):** Single-expression functions without braces;
multi-statement functions with rectangular `{...}` body. Direct alignment. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** Functions (and by extension lambdas) should do one thing
— single-expression lambdas express one thing; multi-statement lambdas suggest extraction. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin Coding Conventions (post-2016) | Single-expr without braces | **Adopt** |
| Clean Code (Martin, ongoing) | Small focused blocks | **Adopt** |

### SBPP-FMT-04:12 - Relations

* **Applied within:** SBPP-FMT-03 (Indented Control Flow — blocks appear inside indented expressions)
* **Contrasts with:** SBPP-FMT-05 (Guard Clause — avoids deeply nested blocks)
* **Relates to:** SBPP-BEH-30 (Pluggable Block — these are the blocks being plugged)

### SBPP-FMT-04:End
