## SBPP-FMT-10 - Interesting Return Value

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-FMT-10:1 - Problem frame

In Java/Kotlin, methods produce two distinct kinds of value: those whose primary purpose
is the **value they return** (queries, transformations, computations), and those whose
primary purpose is the **side effect they cause** (commands, mutations, saves). The return
type and explicit return statement are the signals by which a reader understands which
kind of method they are reading. Incorrect or missing return statements obscure this
distinction.

### SBPP-FMT-10:2 - Problem

When should a method explicitly return a value, and when should it return nothing
(void/Unit)? How do you signal clearly at the end of a method whether its result
is intended for use by the caller?

### SBPP-FMT-10:3 - Forces

| Force | Tension |
|-------|---------|
| **CQS** | Commands return void; queries return a value ↔ some operations are both |
| **Clarity** | Explicit return type is the contract ↔ `Unit` / `void` is also explicit |
| **Kotlin** | `Unit` is explicit; no-return-statement implies `Unit` ↔ can be ambiguous for short single-expression functions |

### SBPP-FMT-10:4 - Solution — Return a value only when the caller is expected to use it; declare void/Unit for commands; make the return type the documentation

**Java — explicit return type as contract:**

```java
// ✅ Query — return type communicates "caller should use this"
public Money calculatePremium(Policy policy) {
    return ratingEngine.rate(policy);
}

// ✅ Command — void communicates "this is a side effect, no meaningful return"
public void activate(PolicyId policyId) {
    Policy policy = repository.findById(policyId).orElseThrow();
    policy.activate();
    repository.save(policy);
    eventBus.publish(new PolicyActivated(policyId));
    // no return — the caller does not need a value
}

// ✅ Return self for fluent API (explicit in method design)
public PolicyBuilder withPremium(Money premium) {
    this.premium = premium;
    return this;   // explicitly return this — Interesting Return Value
}

// ✅ Boolean return for "did it work?" pattern
public boolean tryActivate(PolicyId policyId) {
    Optional<Policy> policy = repository.findById(policyId);
    if (policy.isEmpty()) return false;
    policy.get().activate();
    repository.save(policy.get());
    return true;
}
```

**Kotlin — expression body for queries; Unit for commands:**

```kotlin
// ✅ Expression body — no 'return' keyword; return type is the expression value
fun calculatePremium(policy: Policy): Money = ratingEngine.rate(policy)

// ✅ Block body query — explicit return
fun findActivePolicies(holderId: CustomerId): List<Policy> {
    return repository.findByHolder(holderId).filter { it.isActive }
}

// ✅ Command — explicit Unit (usually omitted, but communicates intent)
fun activate(policyId: PolicyId) {   // : Unit omitted — standard Kotlin
    val policy = repository.findById(policyId) ?: throw PolicyNotFoundException(policyId)
    policy.activate()
    repository.save(policy)
    eventBus.publish(PolicyActivated(policyId))
}

// ✅ Interesting return value — explicitly returning self in Kotlin builders
fun PolicyBuilder.withPremium(premium: Money): PolicyBuilder = apply { this.premium = premium }
```

**When to add a non-obvious return vs. when not to:**

```java
// ✅ Interesting: the caller will use the saved entity (with generated ID)
public Policy save(Policy policy) { return repository.save(policy); }

// ✅ Not interesting: audit log write — caller never uses the result
public void recordAuditEntry(AuditEntry entry) { auditRepository.save(entry); }

// ✅ Kotlin — Non-interesting void: don't return Unit explicitly in most cases
fun recordAuditEntry(entry: AuditEntry) {  // Unit implicit
    auditRepository.save(entry)
}
```

### SBPP-FMT-10:5 - Archetypal Grounding

**U.System:** `public Policy save(Policy policy)` returns the saved policy (with generated ID
and database timestamp) — the caller *should* use this; `void recordAuditEntry(entry)` — the
caller has no need for a return value, and the `void` communicates this.

**U.Episteme:** The return type is the first line of documentation about a method's contract.
`Money calculatePremium(...)` announces "I produce a Money value intended for your use."
`void activate(...)` announces "I perform an action; the result is the side effect."

### SBPP-FMT-10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Return value design in Java/Kotlin methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Ignoring return values of methods that have interesting returns is a common bug | Enable `@CheckReturnValue` annotation or static analysis to flag ignored return values |
| **Arch** | CQS recommends never returning values from commands — strict CQS is sometimes too rigid (e.g., `save` returning the persisted entity) | Apply CQS as a principle, not a law; document exceptions |
| **Onto/Epist** | Kotlin expression bodies (`= expression`) communicate "I am a pure computation" very clearly | Use expression bodies for all pure query functions in Kotlin |
| **Prag** | `@SuppressWarnings("ResultOfMethodCallIgnored")` in Java — if you need this, the return value may not be truly "interesting" | Reconsider the API design |
| **Did** | Teach CQS: "commands return void; queries return a value" — and the Interesting Return Value refinement: "only return a value when the caller needs it" | |

### SBPP-FMT-10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT10-1** | Methods that produce a result intended for the caller SHALL have a non-void return type, and SHALL have an explicit `return` statement (Java) or expression body (Kotlin). | Documents return intent |
| **CC-FMT10-2** | Methods whose purpose is a side effect (commands) SHALL declare `void` (Java) or implicit `Unit` (Kotlin). | CQS compliance |
| **CC-FMT10-3** | Kotlin pure query functions SHOULD use expression body (`= expression`) to communicate "I produce a single value". | Idiomatic query form |
| **CC-FMT10-4** | Methods that return `this` for fluent chaining SHALL document `@return this` in Javadoc. | Communicates return value intent |

### SBPP-FMT-10:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: void method that should return the modified object**
`public void save(Policy policy)` when the saved entity has a generated ID.
Fix: `public Policy save(Policy policy)` — return the persisted entity.

**Anti-pattern 2: Returning the parameter unnecessarily**
`public Policy activate(Policy policy) { policy.activate(); return policy; }` — if callers
already have the reference, returning it adds no value. Fix: `void activate(Policy policy)`.

**Anti-pattern 3: Kotlin non-expression body for trivial query**
```kotlin
fun isActive(): Boolean {
    return status == PolicyStatus.ACTIVE
}
```
Fix: `val isActive: Boolean get() = status == PolicyStatus.ACTIVE` or
`fun isActive() = status == PolicyStatus.ACTIVE`.

### SBPP-FMT-10:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Return type is the first line of documentation | Requires deliberate design discipline |
| CQS compliance reduces surprises | Some operations are genuinely both command and query — document the exception |
| Kotlin expression bodies make pure queries visually distinct | — |

### SBPP-FMT-10:10 - Rationale

Beck's Interesting Return Value establishes the distinction between "methods that produce
a value for their caller" and "methods that exist for their side effects." In Java/Kotlin
this maps precisely to the CQS principle and to Kotlin's expression-body syntax for queries.

The modern addition is the `@CheckReturnValue` annotation and static analysis enforcement —
if a method has an interesting return value, ignoring it should be flagged by tooling.

### SBPP-FMT-10:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**CQS — Command-Query Separation (Meyer, 1988; widely applied post-2015):** Commands return
void; queries return a value and have no side effects. *Adopt as the guiding principle.*

**Kotlin expression bodies (JetBrains, post-2016):** `fun query() = expression` vs
`fun command() { sideEffect() }` — the syntax makes the distinction visible. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 17 ("Minimize mutability") and the overall
style where query methods return values and mutating methods return `this` for chaining. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| CQS (Meyer, widely applied post-2015) | Return value = query indicator | **Adopt** |
| Kotlin expression bodies (post-2016) | Query/command syntax distinction | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Query/command discipline | **Adopt** |

### SBPP-FMT-10:12 - Relations

* **Implements:** Command-Query Separation (CQS)
* **Aligns with:** SBPP-BEH-07 (Query Method — the "interesting return value" pattern IS a query method)
* **Constrains:** All method signatures in the codebase — every method declares its intent via its return type
* **Relates to:** SBPP-FMT-09 (Yourself — Yourself was about returning the receiver from a cascade; this pattern is about when any return value is interesting)

### SBPP-FMT-10:End
