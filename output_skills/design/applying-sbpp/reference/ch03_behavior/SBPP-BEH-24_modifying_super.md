## SBPP-BEH-24 - Modifying Super

> **Type:** Architectural (A)
> **Status:** Adapt
> **Normativity:** Normative

### SBPP-BEH-24:1 - Problem frame

Sometimes a subclass needs to change part of a superclass method's behaviour without
calling `super` — it fully overrides the method with a different implementation. This
Modifying Super pattern is the most tightly coupled use of inheritance and should be
used with great caution.

### SBPP-BEH-24:2 - Problem

How do you change part of a superclass method's behaviour in a subclass when the change
is too fine-grained for simple extension but the superclass method cannot be refactored?

### SBPP-BEH-24:3 - Forces

| Force | Tension |
|-------|---------|
| **Coupling** | Complete override tightly couples subclass to expected superclass behaviour | Must understand superclass fully |
| **LSP** | Complete override risks violating the Liskov Substitution Principle | Subclass may not honour the superclass contract |
| **Encapsulation** | Superclass should not need to be known in detail | Override forces understanding of the superclass |

### SBPP-BEH-24:4 - Solution — Prefer refactoring the superclass with hooks over complete override

Before using Modifying Super, refactor the superclass using Composed Method (BEH-01) to
extract the part that varies into an overridable hook method. Then override only the hook.

**Java example — refactor to hooks first:**

```java
// ❌ Before: full override needed to change just one step
public class StandardCalculator {
    public Money calculate(Policy policy) {
        double base = policy.basePremium().cents();
        double risk = riskMatrix.lookup(policy.category());   // ← want to change only this
        return Money.of((long)(base * risk), policy.currency());
    }
}

// ✅ After: extract the variable part as a hook
public class StandardCalculator {
    public final Money calculate(Policy policy) {
        double base = policy.basePremium().cents();
        double risk = lookupRisk(policy);   // ← overridable hook
        return Money.of((long)(base * risk), policy.currency());
    }

    protected double lookupRisk(Policy policy) {
        return riskMatrix.lookup(policy.category());
    }
}

// Subclass modifies only the hook
public class ExperimentalCalculator extends StandardCalculator {
    @Override
    protected double lookupRisk(Policy policy) {
        return mlRiskModel.predict(policy);  // different risk calculation
    }
}
```

**Kotlin:**

```kotlin
open class StandardCalculator {
    fun calculate(policy: Policy): Money {
        val base = policy.basePremium.cents
        val risk = lookupRisk(policy)
        return Money.of((base * risk).toLong(), policy.currency)
    }

    protected open fun lookupRisk(policy: Policy): Double =
        riskMatrix.lookup(policy.category)
}

class ExperimentalCalculator : StandardCalculator() {
    override fun lookupRisk(policy: Policy) = mlRiskModel.predict(policy)
}
```

### SBPP-BEH-24:5 - Archetypal Grounding

**U.System:** Instead of overriding the whole `calculate()` method, `ExperimentalCalculator` overrides only `lookupRisk()` — the hook for the changing part.
**U.Episteme:** Hooks document the designed extension points; complete overrides do not.

### SBPP-BEH-24:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Superclass modification via subclass in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Full override without `super` is invisible in code review as a "modification" | Flag `@Override` without `super` calls in code review; prefer hook methods |
| **Arch** | Full overrides violate LSP if the subclass changes the semantic contract | Design hook methods; make non-hookable methods `final` |
| **Onto/Epist** | Distinction between "extend" and "modify" is subtle | Document in method Javadoc: "Override this hook to modify X" |
| **Prag** | Composition is almost always a better alternative to Modifying Super | Apply composition test: can I achieve this with a strategy/delegate instead? |
| **Did** | Developers may use full overrides when hooks would be cleaner | Teach Template Method as the design solution |

### SBPP-BEH-24:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH24-1** | Before implementing a full override (Modifying Super), the superclass SHOULD be refactored to extract an overridable hook. | Avoids brittle full overrides |
| **CC-BEH24-2** | Overridable hook methods SHALL be named to communicate what aspect they control. | Documents extension points |
| **CC-BEH24-3** | Non-variable parts of a Template Method SHOULD be `final`. | Prevents accidental modification |

### SBPP-BEH-24:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Silent full override**
Overriding `save()` without calling `super` or documenting the change — readers assume `super` was just forgotten.
Fix: If intentional, document explicitly: `// Does not call super — intentional: replaces persistence strategy`.

**Anti-pattern 2: Override-and-ignore**
Override the method, call super, and then ignore its return value.
Fix: Either extend (use the return value) or fully replace (don't call super).

### SBPP-BEH-24:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Fine-grained subclass customisation without duplicating entire method | LSP risk — must honour superclass contract |
| Hook methods document the designed variation points | Requires superclass refactoring first |

### SBPP-BEH-24:10 - Rationale

Beck warns that Modifying Super creates tighter coupling than Extending Super. The modern
Java/Kotlin solution is to design superclasses with explicit hook methods (Template Method
pattern). Full overrides without super should be treated as design debt requiring refactoring.

### SBPP-BEH-24:11 - SoTA-Echoing

**Adoption verdict: ADAPT**

**GoF Template Method (widely applied post-2015):** Formalises the "extract hook" approach.
*Adopt the pattern; use it to avoid Modifying Super.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 19 requires documenting which methods are designed
for override. *Adopt: mark non-hookable methods `final`.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Template Method (post-2015) | Hook-based design avoids full override | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 19 — document override design | **Adopt** |

### SBPP-BEH-24:12 - Relations

* **Contrasts with:** SBPP-BEH-23 (Extending Super — add, not replace)
* **Preferred solution:** Refactor superclass with SBPP-BEH-01 (Composed Method) to extract hooks
* **Implements (when used):** GoF Template Method hook override
* **Alternative:** SBPP-BEH-25 (Delegation — composition avoids this entirely)

### SBPP-BEH-24:End
