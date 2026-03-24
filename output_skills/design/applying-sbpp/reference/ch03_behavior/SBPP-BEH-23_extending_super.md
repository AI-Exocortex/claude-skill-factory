## SBPP-BEH-23 - Extending Super

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-23:1 - Problem frame

When a subclass needs to add behaviour to a superclass method — not replace it — `super`
is the correct tool. The subclass calls `super.method()` and then adds its own logic.
This "add to" pattern (Extending Super) is the most legitimate use of `super` outside
constructors and is the foundation of the Template Method pattern.

### SBPP-BEH-23:2 - Problem

How do you add behaviour to a superclass method in a subclass without duplicating the
superclass logic and while maintaining the contract of the overridden method?

### SBPP-BEH-23:3 - Forces

| Force | Tension |
|-------|---------|
| **DRY** | Don't duplicate superclass logic ↔ super creates coupling |
| **LSP** | Subclass should honour superclass contract ↔ addition might change observable behaviour |
| **Call Order** | Super first then addition ↔ addition first then super — order matters for correctness |

### SBPP-BEH-23:4 - Solution — Call super, then add; or add, then call super (as semantics demand)

Call `super.method()` at the position required by the semantics of the extension.
Document whether super must come first or last.

**Java example:**

```java
public class ValidatedPolicyRepository extends BasePolicyRepository {

    // ✅ Extending Super: super runs first (persistence), then we add audit
    @Override
    public void save(Policy policy) {
        super.save(policy);                                  // superclass: persist
        auditLog.record("POLICY_SAVED", policy.getId());     // subclass: add audit
    }

    // ✅ Extending Super: we add validation first, then let super persist
    @Override
    public Policy create(PolicyRequest request) {
        validator.validate(request);                         // subclass: add validation
        return super.create(request);                        // superclass: create and return
    }
}
```

**Kotlin:**

```kotlin
open class BasePolicyRepository {
    open fun save(policy: Policy) { /* persist */ }
}

class ValidatedPolicyRepository(
    private val auditLog: AuditLog,
    private val validator: PolicyValidator
) : BasePolicyRepository() {

    override fun save(policy: Policy) {
        super.save(policy)
        auditLog.record("POLICY_SAVED", policy.id)
    }
}
```

### SBPP-BEH-23:5 - Archetypal Grounding

**U.System:** `super.save()` runs base persistence, then subclass adds audit — auditing extends, not replaces, the save operation.
**U.Episteme:** Call order is a semantic contract: `super` first means "all superclass behaviour occurs, then I add mine."

### SBPP-BEH-23:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Subclass extension in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Forgetting `super.init()` in Android/framework code causes silent failures | Make `super` calls explicit and verify with tests |
| **Arch** | `super` creates fragile base class coupling | Prefer Template Method hooks over open `override` |
| **Onto/Epist** | "Extension" vs "modification" boundary is not always clear | Clear rule: if you call super, you're extending; if you don't, you're replacing |
| **Prag** | Spring AOP / Aspect-oriented extension is often better than inheritance extension | Use AOP for cross-cutting concerns; use Extending Super for OO behaviour addition |
| **Did** | New developers may both call super AND re-implement logic from the superclass | Teach: call super OR implement; never both |

### SBPP-BEH-23:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH23-1** | Overriding methods that extend superclass behaviour SHALL call `super.method()` at exactly one point. | Ensures super logic runs exactly once |
| **CC-BEH23-2** | The position of `super.method()` (first/last/middle) SHALL reflect the semantic order required by the domain. | Correct sequencing |
| **CC-BEH23-3** | Methods that extend super SHOULD document whether super must be called first or last. | Documents the extension contract |

### SBPP-BEH-23:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Double-calling super**
`super.save()` called twice — once explicitly, once via another method.
Fix: Trace call paths; call `super` exactly once.

**Anti-pattern 2: Not calling super when required**
Framework lifecycle methods (`onCreate`, `onStart`) require `super` calls.
Fix: If the superclass method is a lifecycle hook, `super` is mandatory — add a test.

### SBPP-BEH-23:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Superclass logic reused without duplication | Fragile base class — mitigated by template method hooks |
| Clear extension point for framework overrides | Super call position must be correct |
| Enables cross-cutting enrichment via inheritance | — |

### SBPP-BEH-23:10 - Rationale

Extending Super is the core legitimate use of `super`. It is the mechanism behind
Template Method (GoF) and Android/Spring lifecycle overrides. Used with discipline
(shallow hierarchies, documented call order), it is safe and expressive.

### SBPP-BEH-23:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**GoF Template Method (widely applied post-2015):** Template Method uses Extending Super as its
mechanism: subclass hooks extend the template. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 19 — document `super` call requirements for
overridable methods. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Template Method (post-2015) | Super as extension hook | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 19 | **Adopt** |

### SBPP-BEH-23:12 - Relations

* **Specialises:** SBPP-BEH-22 (Super — the legitimate extension use case)
* **Contrasts with:** SBPP-BEH-24 (Modifying Super — replacing rather than extending)
* **Implements:** GoF Template Method pattern

### SBPP-BEH-23:End
