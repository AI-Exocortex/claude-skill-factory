## SBPP-BEH-27 - Self Delegation

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-BEH-27:1 - Problem frame

Sometimes the delegate needs to call back on the delegating object — either to access its
state or to invoke its methods. Simple Delegation fails because the delegate has no reference
to the original object. Self Delegation passes `this` (or a callback interface) to the
delegate, allowing bidirectional communication.

### SBPP-BEH-27:2 - Problem

How do you implement delegation to a collaborator that needs a reference to the delegating
object to complete its work?

### SBPP-BEH-27:3 - Forces

| Force | Tension |
|-------|---------|
| **Access** | Delegate needs the delegating object's state or methods ↔ coupling increases |
| **Circular Reference** | Passing `this` creates a bidirectional reference ↔ can prevent GC in some environments |
| **Interface Segregation** | Pass only what the delegate needs ↔ passing `this` exposes the entire delegating object |

### SBPP-BEH-27:4 - Solution — Pass a callback interface rather than `this`; limit what the delegate sees

Instead of passing `this` directly, define a callback interface with only the methods the
delegate needs. Pass the delegating object as that interface, not as its full type.

**Java example:**

```java
// Delegate needs to call back on the order to check discounts
public interface DiscountEligibility {
    boolean isEligibleForDiscount(DiscountType type);
    String customerId();
}

public class DiscountCalculator {
    // Accepts callback interface, not the full Order object
    public Money calculateDiscount(List<LineItem> items, DiscountEligibility eligibility) {
        if (eligibility.isEligibleForDiscount(DiscountType.LOYALTY)) {
            return loyaltyDiscount(items, eligibility.customerId());
        }
        return Money.ZERO;
    }
}

// Order implements the callback interface and passes itself
public class Order implements DiscountEligibility {
    private final DiscountCalculator discountCalculator;
    private final Customer customer;
    private final List<LineItem> items;

    @Override
    public boolean isEligibleForDiscount(DiscountType type) {
        return customer.hasLoyaltyStatus() && type == DiscountType.LOYALTY;
    }

    @Override
    public String customerId() { return customer.getId(); }

    public Money calculateDiscount() {
        return discountCalculator.calculateDiscount(items, this);  // self delegation
    }
}
```

**Kotlin:**

```kotlin
fun interface DiscountEligibility {
    fun isEligibleForDiscount(type: DiscountType): Boolean
}

class DiscountCalculator {
    fun calculateDiscount(items: List<LineItem>, eligibility: DiscountEligibility): Money =
        if (eligibility.isEligibleForDiscount(DiscountType.LOYALTY)) loyaltyDiscount(items)
        else Money.ZERO
}

class Order(
    private val customer: Customer,
    private val items: List<LineItem>,
    private val calculator: DiscountCalculator
) : DiscountEligibility {
    override fun isEligibleForDiscount(type: DiscountType) =
        customer.hasLoyaltyStatus && type == DiscountType.LOYALTY

    fun calculateDiscount() = calculator.calculateDiscount(items, this)
}
```

### SBPP-BEH-27:5 - Archetypal Grounding

**U.System:** `DiscountCalculator` receives a `DiscountEligibility` callback — it calls back on the order without knowing the order's full type.
**U.Episteme:** The callback interface limits the delegate's view; it can test only `isEligibleForDiscount()`, not all of `Order`.

### SBPP-BEH-27:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Bidirectional references increase mental overhead | Use callback interface to limit the delegate's view |
| **Arch** | Circular structure can be confusing | Use ISP — callback interface has only the methods the delegate needs |
| **Onto/Epist** | "Self" in the name implies this; the interface technique is cleaner | Always use callback interface in Java/Kotlin, not raw `this` |
| **Prag** | Many apparent Self Delegation needs can be solved by restructuring | Try Simple Delegation first; use Self Delegation only when necessary |
| **Did** | Advanced pattern; teach after Simple Delegation is mastered | Introduce with the "callback interface" framing |

### SBPP-BEH-27:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH27-1** | Self Delegation SHOULD pass a callback interface, not the full delegating object type. | Limits delegate's coupling surface |
| **CC-BEH27-2** | The callback interface SHALL contain only the methods the delegate actually calls. | Interface Segregation |

### SBPP-BEH-27:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Passing `this` as full type**
`delegate.process(this)` where `this` is a 40-method class. Fix: Define a callback
interface with only the methods the delegate needs.

### SBPP-BEH-27:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Delegate can call back on the delegating object | Bidirectional reference — mitigated by callback interface |
| Callback interface documents exactly what the delegate needs | Extra interface per callback scenario |

### SBPP-BEH-27:10 - Rationale

Self Delegation is the foundation of the Observer and Callback patterns. Using a callback
interface rather than passing `this` directly is the ISP-compliant approach recommended
in modern Java/Kotlin.

### SBPP-BEH-27:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**GoF Observer (widely used post-2015):** Observer pattern is Self Delegation — the observed
passes `this` (as an event source) to observers. *Adopt.*

**Java Functional Interfaces / Kotlin lambdas (post-2016):** Callbacks as lambdas are the
modern Self Delegation mechanism — simpler than full callback interface for single methods. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Observer (post-2015) | Self delegation via listener | **Adopt** |
| Java functional interfaces / Kotlin lambdas (post-2016) | Callback as lambda | **Adopt** |

### SBPP-BEH-27:12 - Relations

* **Specialises:** SBPP-BEH-25 (Delegation), SBPP-BEH-26 (Simple Delegation — upgrade path)
* **Implements:** Observer/Callback patterns
* **Constrained by:** Callback interface must use ISP

### SBPP-BEH-27:End
