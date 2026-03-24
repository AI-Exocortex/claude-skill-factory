## SBPP-STA-02 - Variable State

> **Type:** Architectural (A)
> **Status:** Reject (for primary use) / Adopt (for specific legitimate cases)
> **Normativity:** Normative

### SBPP-STA-02:1 - Problem frame

Beck himself flags this as a pattern to avoid in most circumstances. It represents state
whose presence varies from instance to instance — stored in a property map rather than
typed fields. In Java/Kotlin, this maps to `Map<String,Object>`, `@JsonAnyGetter`,
or EAV (Entity-Attribute-Value) database patterns.

### SBPP-STA-02:2 - Problem

How do you represent state that only some instances of a class have, without creating
dozens of nullable fields or a subclass explosion?

### SBPP-STA-02:3 - Forces

| Force | Tension |
|-------|---------|
| **Flexibility** | Any instance can have any property ↔ no compile-time structure |
| **Type Safety** | Dynamic map is untyped ↔ typed optional fields require null handling |
| **Extensibility** | New properties require no code change ↔ discoverability disappears |
| **Performance** | Map lookup is more expensive than field access | Negligible for most use cases |

### SBPP-STA-02:4 - Solution — Use only for legitimate dynamic-attribute scenarios; prefer typed alternatives

**AVOID** in most cases. Use typed alternatives:
- Optional fields: `Optional<T>` (Java) or nullable `T?` (Kotlin)
- Sealed subclasses: for structured variation
- Composition: sub-objects that may be null/absent

**Legitimate uses:** user-defined metadata, plugin/extension attributes, JSON pass-through.

**Java — typed alternatives (preferred):**

```java
// ❌ Variable State (avoid for domain logic)
class Policy {
    private Map<String, Object> attributes = new HashMap<>();
}

// ✅ Typed nullable for optional domain state
public final class Policy {
    private final PolicyId id;
    private @Nullable Discount appliedDiscount;     // absent for most policies
    private @Nullable ClaimRecord lastClaim;        // absent until first claim
}

// ✅ Sealed subclasses for structured variation
public sealed interface PolicyType permits StandardPolicy, CommercialPolicy, LifePolicy {}
```

**Kotlin — typed nullable:**

```kotlin
data class Policy(
    val id: PolicyId,
    val discount: Discount? = null,       // optional, typed
    val lastClaim: ClaimRecord? = null    // optional, typed
)
```

**When Variable State is justified:**

```java
// ✅ Legitimate: user-defined metadata on a policy (open-ended extension point)
public class Policy {
    private final Map<String, String> metadata;  // user-defined labels, tags

    public String getMetadata(String key) { return metadata.get(key); }
    public void setMetadata(String key, String value) { metadata.put(key, value); }
}
```

### SBPP-STA-02:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Optional domain state uses typed nullable fields; only open-ended extension attributes use maps.
*Show:* `policy.getDiscount()` returns `Optional<Discount>` — type-safe and discoverable.
`policy.getMetadata("risk-note")` returns `String` — acceptable for open-ended user data.

**U.Episteme (design reasoning):**
*Tell:* Variable State sacrifices type safety for flexibility; the cost rarely pays off in domain models.
*Show:* A bug where `attributes.get("premium")` returns a `String` instead of `Money` is found
only at runtime; a typed field is caught at compile time.

### SBPP-STA-02:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Optional/dynamic state in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Dynamic attributes require separate governance for what keys are allowed | Define an explicit key registry for semi-dynamic attributes |
| **Arch** | Map-based state leaks into serialization, persistence, and API contracts | Isolate to a clearly-named `metadata` field; never use for domain logic |
| **Onto/Epist** | Beck warns this is an anti-pattern in most cases | Apply only for open-ended user extension, not for known domain variation |
| **Prag** | EAV databases are a known anti-pattern in relational systems | Prefer typed columns; use JSONB for truly dynamic data |
| **Did** | New developers may use maps as a shortcut for "I don't know the schema yet" | Teach: design the schema; use typed fields; revisit if genuinely dynamic |

### SBPP-STA-02:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA02-1** | Variable State (Map-based) MUST NOT be used for state that has known domain semantics. | Forces explicit typing of domain concepts |
| **CC-STA02-2** | When state is present in only some instances, typed nullable fields or sealed subclasses SHOULD be used. | Type-safe optional state |
| **CC-STA02-3** | Map-based state SHALL be used only for open-ended extension attributes explicitly named as such (e.g., `metadata`, `tags`). | Scopes legitimate use |

### SBPP-STA-02:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Domain Logic on Attributes**
```java
if (policy.getAttributes().get("isHighRisk") != null) { ... }
```
Fix: Add `boolean isHighRisk()` as a typed boolean property.

**Anti-pattern 2: Type-Unsafe Retrieval**
```java
Money premium = (Money) policy.getAttributes().get("premium");
```
Fix: Add `Money getPremium()` as a typed field accessor.

### SBPP-STA-02:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Enables open-ended extension without code changes | Type safety lost; runtime ClassCastException risk |
| Useful for plugin/metadata scenarios | Domain logic on dynamic attributes is a design smell |

### SBPP-STA-02:10 - Rationale

Beck's own warning ("This is not a pattern you should use often, if ever") is upheld.
In Java/Kotlin, typed nullable fields, Optional, and sealed types cover virtually all
cases where Variable State might be tempting. Reserve Map-based attributes for genuine
open-ended user extension points.

### SBPP-STA-02:11 - SoTA-Echoing

**Adoption verdict: REJECT for domain use; ADOPT for metadata/extension points**

**Effective Java 3rd ed. (Bloch, 2018):** Item 64 (use interfaces to refer to objects) and
Item 57 (minimise scope of local variables). Both argue against untyped bags. *Reject for domain state.*

**Kotlin nullable types (post-2016):** `T?` is the idiomatic, type-safe way to express optional state. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Avoid untyped containers | **Reject** for domain |
| Kotlin nullable types (post-2016) | Type-safe optional | **Adopt** as alternative |
| JSON:API / OpenAPI extension patterns | Metadata maps are accepted for extension points | **Adopt** scoped |

### SBPP-STA-02:12 - Relations

* **Contrast with:** SBPP-STA-01 (Common State — use this instead)
* **Alternative:** Sealed subclasses (SBPP-BEH-15), typed nullables (SBPP-STA-07)
* **Constrained by:** Type safety requirements of Java/Kotlin

### SBPP-STA-02:End
