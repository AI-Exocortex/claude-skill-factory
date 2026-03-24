## SBPP-FMT-09 - Yourself

> **Type:** Architectural (A)
> **Status:** Reject (as original) / Superseded
> **Normativity:** Normative

### SBPP-FMT-09:1 - Problem frame

In Smalltalk, `yourself` was needed because a cascade's value was the result of the
**last message** in the cascade, not the receiver. If the last message returned something
other than the receiver (e.g., `add:` returns the added element, not the collection),
appending `; yourself` made the cascade return the receiver. In Java/Kotlin, this problem
does not arise because builders return `this` explicitly, and Kotlin scope functions have
typed, documented return values.

### SBPP-FMT-09:2 - Problem

How do you ensure that a multi-message sequence returns the original receiver object,
rather than the result of the last message, when you need the receiver for further use?

### SBPP-FMT-09:3 - Forces

| Force | Tension |
|-------|---------|
| **Return value control** | Want the receiver ↔ last operation may return something else |
| **API design** | Fluent APIs should return `this` consistently ↔ some operations have their own meaningful return value |
| **Clarity** | Explicit return value communicates intent ↔ implicit return can surprise |

### SBPP-FMT-09:4 - Solution — Design fluent APIs to return `this` explicitly; use Kotlin `apply` / `also` to ensure receiver return

**The problem in context:**

```java
// Smalltalk problem: add: returns the added element, not the collection
// all := OrderedCollection new add: 5; add: 7   --> all = 7, not the collection!
// Smalltalk fix: append ; yourself

// Java equivalent: this problem doesn't arise with proper builders
List<Integer> all = new ArrayList<>();
all.add(5);   // add() returns boolean in Java, not the element
all.add(7);
// all is the list — no Yourself pattern needed
```

**Java — builder returns `this` explicitly (solves the return value problem):**

```java
// ✅ Builder design: every setter returns `this`
public final class PolicyBuilder {
    private PolicyId id;
    private Money premium;

    public PolicyBuilder withId(PolicyId id) {
        this.id = id;
        return this;        // explicit return this — no Yourself needed
    }

    public PolicyBuilder withPremium(Money premium) {
        this.premium = premium;
        return this;
    }

    public Policy build() { return new Policy(id, premium); }
}

PolicyBuilder builder = new PolicyBuilder()
    .withId(policyId)
    .withPremium(premium);  // returns the builder — use it or build()
```

**Kotlin — `apply` is `yourself` made structural:**

```kotlin
// ✅ apply {} always returns the receiver — Yourself is built in
val list = mutableListOf<Int>()
    .apply {
        add(5)      // add() returns Boolean in Kotlin too
        add(7)      // but apply always returns the list
    }
// list is the MutableList<Int>, not 7

// ✅ also {} — side effects, returns receiver
val policy = createPolicy()
    .also { log.info("Created: ${it.id}") }  // log returns Unit; also returns policy
    .also { auditService.record(it) }
// policy is still the Policy object
```

**When Yourself thinking still applies in Kotlin — `fold` with yourself:**

```kotlin
// Smalltalk: inject:into: with yourself
// Kotlin equivalent: fold where accumulator needs to return itself after modification
val result = items.fold(mutableListOf<ProcessedItem>()) { acc, item ->
    acc.also { it.add(process(item)) }   // also returns acc (the list), not the add() result
}
```

### SBPP-FMT-09:5 - Archetypal Grounding

**U.System:** `mutableListOf<Int>().apply { add(5); add(7) }` — `apply` guarantees the list is
returned, not the boolean from `add()`. This is `yourself` made structural in the language.

**U.Episteme:** The underlying problem Beck solved — "return the receiver, not the last message
result" — is solved in Java by designing builders to return `this`, and in Kotlin by `apply`/`also`
which have this guarantee built into their type signatures.

### SBPP-FMT-09:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Return value management in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Java's `add()`/`put()` return values (boolean/previous value) are often ignored — this can be a mistake | Use return values where they matter; annotate ignored returns with `@SuppressWarnings("unused")` or `_` (Kotlin) |
| **Arch** | Methods that return `this` for chaining must document this contract | Javadoc: `@return this` in builder methods |
| **Onto/Epist** | `yourself` is a Smalltalk-specific workaround for a cascade semantics limitation; Java/Kotlin solve this at the language/pattern level | There is no direct equivalent because the problem does not arise in the same form |
| **Prag** | Kotlin's `apply`/`also` fully replace `yourself`; no adaptation needed | Use `apply`/`also` idiomatically |
| **Did** | Teach `apply` as "do stuff, get back the object you started with" — the Yourself intuition | |

### SBPP-FMT-09:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-FMT09-1** | Fluent builder methods in Java SHALL return `this` explicitly. | Enables chaining without Yourself workaround |
| **CC-FMT09-2** | When a Kotlin `fold`/`reduce` accumulator needs to perform a mutation and return itself, SHOULD use `also { }`. | Kotlin's `yourself` equivalent |
| **CC-FMT09-3** | Kotlin `apply {}` SHOULD be the default for "configure and return receiver" use cases. | Supersedes Yourself |

### SBPP-FMT-09:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Java builder method that doesn't return `this`**
`public void withId(PolicyId id) { this.id = id; }` — loses chaining. Fix: `return this;`.

**Anti-pattern 2: Kotlin `fold` losing the accumulator**
`items.fold(mutableListOf<T>()) { acc, item -> acc.add(process(item)); acc }` — verbose.
Fix: `items.fold(mutableListOf<T>()) { acc, item -> acc.also { it.add(process(item)) } }`.

### SBPP-FMT-09:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Yourself problem doesn't arise when builders return `this` | Builder design discipline required |
| Kotlin `apply`/`also` fully solve the return-value problem | Scope function semantics must be known |

### SBPP-FMT-09:10 - Rationale

Yourself is one of the few Beck patterns that is **superseded** rather than adopted or adapted.
The problem it solves — cascade return value — does not exist in Java's method-chaining model or
in Kotlin's scope functions. The mental model ("I want the receiver back after this sequence") is
directly expressed by `apply`/`also` in Kotlin and by builder `return this` in Java.

### SBPP-FMT-09:11 - SoTA-Echoing

**Adoption verdict: REJECT (pattern) / SUPERSEDED by `apply`/`also`/builder-return-this**

The Yourself pattern addresses a Smalltalk language limitation that does not exist in Java/Kotlin.
No post-2015 source recommends a `yourself` equivalent in Java/Kotlin because the problem
is structurally avoided.

**Kotlin scope functions (JetBrains, post-2016):** `apply` and `also` provide typed "return the
receiver" guarantees by design. *Adopt as the superseding mechanism.*

**Effective Java 3rd ed. Item 2 (Bloch, 2018):** Builder pattern with return-this methods. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin `apply`/`also` (post-2016) | Supersedes `yourself` | **Adopt** (superseding mechanism) |
| Effective Java 3rd ed. Item 2 (Bloch, 2018) | Builder return-this | **Adopt** |

### SBPP-FMT-09:12 - Relations

* **Superseded by:** Kotlin `apply`/`also`, Java builder `return this`
* **Paired with:** SBPP-FMT-08 (Cascade — Yourself solved the cascade return-value problem)
* **Context:** Only arises when using mutable accumulation in `fold`/`reduce`-style code

### SBPP-FMT-09:End
