## SBPP-BEH-12 - Debug Printing Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-12:1 - Problem frame

Every Java/Kotlin object eventually appears in a log message, an exception message, or a
debug statement. The default `toString()` inherited from `Object` (`ClassName@hexHashCode`)
is useless for debugging. Teams need consistent, informative `toString()` implementations
that serve both developers and log monitoring systems.

### SBPP-BEH-12:2 - Problem

How do you implement `toString()` so that it provides maximum debugging utility for
developers without exposing sensitive information or becoming a maintenance burden?

### SBPP-BEH-12:3 - Forces

| Force | Tension |
|-------|---------|
| **Debugging Utility** | All internal state visible ↔ security risk from PII/secrets in logs |
| **Maintenance** | Auto-generated methods never drift ↔ hand-written methods are precise |
| **Format Stability** | Stable format supports log parsing ↔ format should not be part of the contract |

### SBPP-BEH-12:4 - Solution — Override `toString()` with key identity/state fields; never include secrets

Override `toString()` to show the object's identity and key state fields in a readable
format. Use `@Override` explicitly. In Kotlin, `data class` auto-generates a compliant
`toString()`. Exclude passwords, tokens, and PII.

**Java example:**

```java
public final class InsurancePolicy {
    private final PolicyId id;
    private final PolicyStatus status;
    private final Money premium;
    private final String holderName;   // PII — excluded from toString

    @Override
    public String toString() {
        return "InsurancePolicy{id=%s, status=%s, premium=%s}"
                .formatted(id, status, premium);
        // holderName intentionally omitted — PII
    }
}
// Log output: InsurancePolicy{id=POL-1234, status=ACTIVE, premium=USD 125.00}
```

**Java — Lombok / IDE-generated (acceptable shortcut):**

```java
@ToString(exclude = {"holderName", "passwordHash"})
public class Account { ... }
```

**Kotlin — data class:**

```kotlin
// data class auto-generates toString() with all constructor properties
data class InsurancePolicy(
    val id: PolicyId,
    val status: PolicyStatus,
    val premium: Money
    // Do NOT put PII fields in the primary constructor if using data class toString
)
```

**Kotlin — manual override for PII control:**

```kotlin
class Account(
    val id: AccountId,
    val status: AccountStatus,
    private val passwordHash: String  // must be excluded
) {
    override fun toString() = "Account{id=$id, status=$status}"
}
```

### SBPP-BEH-12:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Every domain class overrides `toString()` to show identity and key non-sensitive state.
*Show:* Log line: `Processing InsurancePolicy{id=POL-1234, status=ACTIVE, premium=USD 125.00}`
is immediately debuggable; `Processing InsurancePolicy@7a81197d` is not.

**U.Episteme (design reasoning):**
*Tell:* The Debug Printing Method documents what fields constitute observable identity.
*Show:* Fields included in `toString()` are implicitly declared as the "debug-visible state" of the object.

### SBPP-BEH-12:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin `toString()` implementation**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `toString()` in logs can leak PII/secrets if all fields are included | Always audit fields included; add security review of new `toString()` implementations |
| **Arch** | `toString()` format leaks to callers who parse log output | Document that `toString()` output is not a stable API contract |
| **Onto/Epist** | Auto-generated `toString()` includes all fields; new sensitive fields may be added silently | Review every new field addition for PII sensitivity |
| **Prag** | Lombok `@ToString` reduces boilerplate; Kotlin `data class` eliminates it entirely | Use language/library features; write manual overrides only when exclusions are needed |
| **Did** | Developers may rely on `toString()` for serialization — a misuse | Enforce: `toString()` is for debugging only, never for data transfer |

### SBPP-BEH-12:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH12-1** | Every domain class SHALL override `toString()` or use a mechanism that produces meaningful output. | Ensures debuggability |
| **CC-BEH12-2** | `toString()` MUST NOT include passwords, tokens, private keys, or PII fields (name, SSN, address). | Security/privacy |
| **CC-BEH12-3** | `toString()` MUST NOT be used for serialization or data transfer; it is a diagnostic aid only. | Prevents coupling format to contract |
| **CC-BEH12-4** | Kotlin data classes SHOULD NOT include sensitive fields in the primary constructor. | Prevents accidental PII exposure via auto-generated toString |

### SBPP-BEH-12:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: PII in toString**
```java
return "Customer{name=" + name + ", ssn=" + ssn + "}";
```
Fix: Exclude PII fields; if identity is needed, use an anonymized ID.

**Anti-pattern 2: toString Used for Serialization**
```java
String json = myObject.toString(); // relying on toString format
```
Fix: Use a proper serializer; annotate `toString()` with `@DebugOnly` comment.

### SBPP-BEH-12:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Log messages are immediately debuggable | PII risk if all fields included — mitigated by explicit exclusion |
| Exception messages containing domain objects are informative | Format is not stable API — document this constraint |
| Reduces time spent in debugger inspecting objects | — |

### SBPP-BEH-12:10 - Rationale

This is among the most universally adopted patterns in Java/Kotlin. Every major Java style
guide recommends overriding `toString()`. Lombok, Kotlin data classes, and IDE generation
automate the boilerplate. The critical modern concern — PII/secret exclusion — is an
operational security requirement in GDPR-regulated environments.

### SBPP-BEH-12:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 12 ("Always override toString"). Bloch's
guidance is definitive and directly applicable. *Adopt.*

**GDPR / Data Privacy (EU, 2018+):** PII in log files is a compliance violation. `toString()`
exclusion of personal data is a GDPR requirement in regulated environments. *Adopt.*

**Kotlin data class spec (JetBrains, post-2016):** `data class` generates `toString()` 
automatically from primary constructor properties. *Adopt — exclude PII from primary constructor.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 12 | **Adopt** |
| GDPR compliance requirements (2018+) | PII exclusion mandate | **Adopt** |
| Kotlin data class (post-2016) | Auto-generated toString | **Adopt** |

### SBPP-BEH-12:12 - Relations

* **Implements:** Debuggability, Observability
* **Constrains:** SBPP-BEH-07 (Query Method — toString is a query; must be side-effect-free)
* **Relates to:** SBPP-COL-05 (Equality Method — toString fields should reflect equality fields)
* **Constrained by:** GDPR/privacy rules, security policies

### SBPP-BEH-12:End
