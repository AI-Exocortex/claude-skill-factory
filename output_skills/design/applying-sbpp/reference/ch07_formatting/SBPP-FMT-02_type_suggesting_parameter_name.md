## SBPP-FMT-02 - Type Suggesting Parameter Name

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-FMT-02:1 - Problem frame

Beck's original pattern suggested naming Smalltalk parameters after their expected class
(`anInteger`, `aCollection`) because Smalltalk had no static types. Java and Kotlin have
strong static type systems — the type is declared explicitly. The naming challenge shifts:
parameters need names that communicate their **role**, not their type (which the type
declaration already communicates).

### SBPP-FMT-02:2 - Problem

What do you name method parameters so that their purpose at the call site is clear
without redundantly restating the type information already visible in the signature?

### SBPP-FMT-02:3 - Forces

| Force | Tension |
|-------|---------|
| **Role communication** | Parameter name should say *why* this value is needed ↔ type already says *what* it is |
| **Conciseness** | Short names reduce noise ↔ too short and the role is lost |
| **Type redundancy** | `Money premium` already communicates type; `Money premiumMoney` is redundant | |

### SBPP-FMT-02:4 - Solution — Name parameters after their role, not their type; use single words where role is self-evident from context

**Java — role-based parameter names:**

```java
// ✅ Role names: each parameter name answers "what role does this value play?"
public Money calculatePremium(Policy policy, RiskContext context) { }
//                             ^^^^^^ role   ^^^^^^^^^^^^^^ role

public RatingResult rate(Policy policy, EffectiveDate asOf) { }
//                                      ^^^^^^^^^^^^^^^^ role

// ✅ Multiple parameters of the same type — roles distinguish them
public DateRange between(LocalDate start, LocalDate end) { }
//                       ^^^^^^^^^^^^role ^^^^^^^^^^^role

// ✅ Single-letter conventional names — acceptable only for generic/mathematical contexts
public <T> List<T> merge(List<T> left, List<T> right) { }
//                       ^^^^^^^^^    ^^^^^^^^^^^ clear by convention

// ❌ Type-restating names (anti-pattern in typed languages)
public Money calculatePremium(Policy policyObject, RiskContext riskContextObj) { }
//                             ^^^^^^^^^^^^                   ^^^^^^ noise
public Money add(Money moneyToAdd) { }
//               ^^^^^^^^^^^^ "money" already in the type
```

**Kotlin — concise role names:**

```kotlin
// ✅ Role-based
fun calculatePremium(policy: Policy, context: RiskContext): Money

fun applyAdjustment(base: Money, adjustment: Adjustment): Money

// ✅ When the method name + type makes the role obvious, single-word suffices
fun Policy.renewFor(years: Int): Policy   // "years" is unambiguous

// ✅ Disambiguating same-type parameters
fun transferBetween(source: Account, target: Account, amount: Money)
//                  ^^^^^^ role     ^^^^^^ role
```

**Naming vocabulary for common roles:**

| Role concept | Recommended name |
|-------------|-----------------|
| The "subject" when only one of a type | Type name in camelCase: `policy`, `claim` |
| Start of a range | `start`, `from`, `begin` |
| End of a range | `end`, `to`, `until` |
| An amount/quantity | `amount`, `count`, `quantity` |
| A point in time | `asOf`, `at`, `when`, `timestamp` |
| A lookup key | `key`, `id`, `code` |
| A callback / handler | `handler`, `onSuccess`, `onError` |
| A predicate / filter | `predicate`, `filter`, `condition` |

### SBPP-FMT-02:5 - Archetypal Grounding

**U.System:** `fun transferBetween(source: Account, target: Account, amount: Money)` — `source`
and `target` distinguish two `Account` parameters by role; the type `Account` is already explicit.

**U.Episteme:** `calculatePremium(Policy policy, RiskContext context)` — a reader sees
"policy being rated" and "rating context" without opening the method body.

### SBPP-FMT-02:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin parameter naming**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Static analysis tools flag some naming conventions (`p` is too short) but not all role issues | Code review is the primary gate; checkstyle can flag single-char names |
| **Arch** | Generic method parameters (`<T>`) often have conventional single-char names (`t`, `e`) — accepted | Apply the convention; document in team guidelines |
| **Onto/Epist** | Beck's original `aCollection` naming is inappropriate in Java/Kotlin — the type declaration covers this | Adapt: name for role, not type |
| **Prag** | Kotlin's named arguments at call sites (`policy = myPolicy`) reduce the importance of positional parameter names | Still name well; named arguments are caller's choice, not a substitution for good names |
| **Did** | New developers copy type into parameter name (`Money moneyAmount`) | Teach: the type declaration is the type; the name is the role |

### SBPP-FMT-02:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT02-1** | Parameter names SHALL express the parameter's role, not restate its type. | Eliminates redundancy |
| **CC-FMT02-2** | When two parameters have the same type, their names MUST distinguish their roles. | Prevents ambiguity |
| **CC-FMT02-3** | Single-character parameter names SHOULD only be used for generic type parameters (`T`, `K`, `V`) or universally understood mathematical conventions. | Readability |

### SBPP-FMT-02:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Type-restating names**
`(Policy policyParam, Money moneyValue)` — Fix: `(Policy policy, Money amount)`.

**Anti-pattern 2: Undifferentiated same-type names**
`(Account a1, Account a2)` — Fix: `(Account source, Account target)`.

**Anti-pattern 3: Over-abbreviation**
`(Policy p, RiskContext rc)` — Fix: `(Policy policy, RiskContext context)`.

### SBPP-FMT-02:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Call sites become self-documenting | Requires discipline — no mechanical rule |
| Method body reads as prose | — |
| Kotlin named arguments reinforce role naming | — |

### SBPP-FMT-02:10 - Rationale

Beck's pattern was solving a Smalltalk-specific problem (no type declarations). In Java/Kotlin
the problem is inverted: the type is explicit, so the name's only job is to communicate
role. The adaptation — role names not type names — is a direct improvement over the original.

### SBPP-FMT-02:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Clean Code ch.2 (Martin, 2008/ongoing):** "Use intention-revealing names" for all variables
including parameters. Restating the type is not intention-revealing. *Adopt.*

**Google Java Style Guide (post-2015):** Parameters should be meaningful, non-abbreviated names. *Adopt.*

**Kotlin Coding Conventions (JetBrains, post-2016):** Parameters use camelCase; role-based naming
is the expected convention. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, ongoing) | Intention-revealing names | **Adopt** |
| Google Java Style Guide (post-2015) | Meaningful parameter names | **Adopt** |
| Kotlin Coding Conventions (post-2016) | camelCase role names | **Adopt** |

### SBPP-FMT-02:12 - Relations

* **Displayed in:** SBPP-FMT-01 (Inline Message Pattern — these names appear in the signature)
* **Aligned with:** SBPP-BEH-18 (Intention Revealing Selector — same naming principle for methods)
* **Extends:** SBPP-STA-14 (Role Suggesting Instance Variable Name — same principle for fields)

### SBPP-FMT-02:End
