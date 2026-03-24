## SBPP-BEH-07 - Query Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-07:1 - Problem frame

In Java/Kotlin objects, some methods exist solely to answer questions about an object's
state without modifying it. The naming and return-type conventions for these "query"
methods directly affect how readable the surrounding code is, particularly in complex
boolean expressions and conditional logic.

### SBPP-BEH-07:2 - Problem

How do you represent testing a property of an object so that callers can write
readable boolean expressions and the method's behaviour is immediately understood?

### SBPP-BEH-07:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | Boolean queries read naturally in conditionals ↔ multiple return types are more flexible |
| **Naming** | `isX()` / `hasX()` names self-document return type ↔ they exclude non-boolean queries |
| **Command-Query Separation** | Queries must not modify state ↔ convenience tempts combining query with side-effect |

### SBPP-BEH-07:4 - Solution — Return boolean and name with `is` / `has` / `can` / `was`

For methods that test a boolean property: return `boolean`/`Boolean` and name with a verb
that reads naturally in an `if` expression. Never modify state inside a query method.

**Java example:**

```java
public final class InsurancePolicy {
    private final LocalDate expiryDate;
    private final PolicyStatus status;
    private final List<Claim> claims;

    // ✅ Query Methods — boolean, named to read naturally
    public boolean isExpired() {
        return expiryDate.isBefore(LocalDate.now());
    }

    public boolean isActive() {
        return status == PolicyStatus.ACTIVE && !isExpired();
    }

    public boolean hasClaims() {
        return !claims.isEmpty();
    }

    public boolean canBeRenewed() {
        return isExpired() && status != PolicyStatus.CANCELLED;
    }
}

// Usage reads like English
if (policy.isActive() && policy.hasClaims()) {
    riskEngine.evaluate(policy);
}
if (policy.canBeRenewed()) {
    notificationService.sendRenewalOffer(policy);
}
```

**Kotlin example:**

```kotlin
data class InsurancePolicy(
    val expiryDate: LocalDate,
    val status: PolicyStatus,
    val claims: List<Claim>
) {
    val isExpired: Boolean get() = expiryDate.isBefore(LocalDate.now())
    val isActive:  Boolean get() = status == PolicyStatus.ACTIVE && !isExpired
    val hasClaims: Boolean get() = claims.isNotEmpty()
    val canBeRenewed: Boolean get() = isExpired && status != PolicyStatus.CANCELLED
}

// Kotlin: computed properties for state tests read most naturally
if (policy.isActive && policy.hasClaims) riskEngine.evaluate(policy)
```

**Rule:** Query methods MUST be side-effect-free (Command-Query Separation). A method
that both tests and modifies state is a design error.

### SBPP-BEH-07:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Domain objects expose boolean properties named to read naturally as predicate expressions.
*Show:* `policy.isActive()` in a Java `if` condition reads as prose; `policy.getStatus() == ACTIVE` does not.

**U.Episteme (design reasoning):**
*Tell:* The Command-Query Separation principle requires that observation has no side effects.
*Show:* `account.isOverdrawn()` called in a log statement must not modify account balance
— its caller cannot know it will change state.

### SBPP-BEH-07:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin OO state-testing methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | CQS enforcement is cultural, not enforced by Java compiler | Enforce via code review; tools like ArchUnit can detect state mutation in methods named `is*` |
| **Arch** | Computed boolean properties in Kotlin may recompute on every access if expensive | Cache expensive computations or use `lazy` delegation |
| **Onto/Epist** | `isActive` can have temporal ambiguity — active now? as-of when? | Make time parameters explicit if "now" is not the universal context |
| **Prag** | JavaBeans convention requires `is` prefix for boolean getters, creating naming alignment | This aligns well with Java standard; no conflict |
| **Did** | Developers may add side effects to query methods for convenience | Enforce CQS as a non-negotiable rule in code review |

### SBPP-BEH-07:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH07-1** | Methods that test a boolean property SHALL be named `isX()`, `hasX()`, `canX()`, or `wasX()`. | Ensures readability in boolean expressions |
| **CC-BEH07-2** | Query methods MUST NOT modify any object state (Command-Query Separation). | Prevents hidden side effects |
| **CC-BEH07-3** | Kotlin boolean properties SHOULD use computed `val` with `get()` rather than `fun` for simple state tests. | Idiomatic Kotlin |
| **CC-BEH07-4** | Query methods with expensive computation SHOULD document or cache the cost. | Prevents performance surprises for callers |

### SBPP-BEH-07:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Query with Side Effect**
```java
public boolean isAuthenticated() {
    lastChecked = Instant.now(); // ❌ side effect in a query
    return token != null && !token.isExpired();
}
```
Fix: Separate the timestamp update into a distinct command method; keep the query pure.

**Anti-pattern 2: Non-Boolean Query Named with `is`**
```java
public String isValid() { return errors.isEmpty() ? "OK" : errors.toString(); }
```
Fix: Return `boolean` from `isValid()`; add a separate `validationErrors()` query for the string.

### SBPP-BEH-07:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Conditional code reads naturally in English | Boolean return type limits expressiveness — use overloaded method variants for richer queries |
| CQS compliance makes code predictable and testable | Discipline required to maintain side-effect freedom |
| Aligns with JavaBeans convention and Kotlin property idiom | — |

### SBPP-BEH-07:10 - Rationale

Beck's Query Method is the object-level expression of Bertrand Meyer's Command-Query
Separation principle (1988, formalized in "Object-Oriented Software Construction").
In Java/Kotlin, the `is`/`has`/`can` naming convention is standard across the JDK and
major frameworks (Spring's `isRunning()`, `hasNext()`, `canWrite()`). This pattern has
near-universal adoption in professional Java/Kotlin code.

### SBPP-BEH-07:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Consistent with JavaBeans naming conventions.
Boolean accessors named `is` are the standard. *Adopt.*

**Clean Code (Martin, 2008/ongoing):** "Functions should either do something or answer
something, but not both" (CQS). Query methods are the canonical application. *Adopt.*

**Kotlin language spec (JetBrains, post-2016):** Computed `val` properties with boolean
type named `isX` are the idiomatic Kotlin equivalent. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | JavaBeans boolean naming | **Adopt** |
| Clean Code (Martin, ongoing) | CQS at method level | **Adopt** |
| Kotlin language idioms (post-2016) | Computed property convention | **Adopt** |

### SBPP-BEH-07:12 - Relations

* **Implements:** Command-Query Separation (Meyer, 1988)
* **Constrains:** SBPP-BEH-01 (Composed Method — composed methods use query methods for conditions)
* **Relates to:** SBPP-BEH-08 (Comparing Method — comparison is a specialized query)
* **Constrained by:** CQS principle: queries MUST be side-effect-free

### SBPP-BEH-07:End
