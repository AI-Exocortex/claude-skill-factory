## SBPP-BEH-26 - Simple Delegation

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-26:1 - Problem frame

When an object delegates to a collaborator, the simplest case is where the collaborator
does not need to know about the delegating object — it is self-contained. This is Simple
Delegation: the delegating object forwards a message, gets a result, and the collaborator
has no back-reference.

### SBPP-BEH-26:2 - Problem

How do you invoke a disinterested delegate — one that needs no reference back to the
delegating object — cleanly and without coupling?

### SBPP-BEH-26:3 - Forces

| Force | Tension |
|-------|---------|
| **Simplicity** | Simple forward is easy ↔ may need to pass self later (Self Delegation) |
| **Coupling** | Delegate has no reference back ↔ limits what delegate can do |
| **Testability** | Self-contained delegate is independently testable | No bidirectional dependency |

### SBPP-BEH-26:4 - Solution — Forward the message; pass only required data, not `this`

Call the delegate's method with only the data it needs. Never pass `this` (the delegating
object) unless the delegate genuinely requires it (that's Self Delegation, BEH-27).

**Java example:**

```java
public class OrderService {
    private final PriceCalculator calculator;    // simple delegate — no knowledge of OrderService
    private final OrderRepository repository;

    public Order placeOrder(Cart cart, Customer customer) {
        Money total = calculator.calculate(cart.items());   // simple delegation — no 'this'
        Order order = Order.create(customer, cart, total);
        return repository.save(order);                       // simple delegation — no 'this'
    }
}

// PriceCalculator is self-contained; knows nothing about OrderService
public class PriceCalculator {
    public Money calculate(List<LineItem> items) {
        return items.stream().map(LineItem::total).reduce(Money.ZERO, Money::add);
    }
}
```

**Kotlin:**

```kotlin
class OrderService(
    private val calculator: PriceCalculator,
    private val repository: OrderRepository
) {
    fun placeOrder(cart: Cart, customer: Customer): Order {
        val total = calculator.calculate(cart.items)   // simple delegation
        val order = Order.create(customer, cart, total)
        return repository.save(order)                  // simple delegation
    }
}
```

### SBPP-BEH-26:5 - Archetypal Grounding

**U.System:** `calculator.calculate(items)` — pure forward, no back-reference, no coupling.
**U.Episteme:** `PriceCalculator` can be tested with any list of items; it doesn't need an `OrderService` to exist.

### SBPP-BEH-26:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | No issues — simplest delegation form | — |
| **Arch** | Simple delegation is the default; don't over-engineer | Keep it simple; escalate to Self Delegation only when needed |
| **Onto/Epist** | "Self-contained" delegate must not acquire hidden dependencies | Inject all dependencies via delegate's constructor |
| **Prag** | Spring DI makes simple delegation trivially injectable | Use constructor injection |
| **Did** | Teach this before Self Delegation | Use as the baseline example of delegation |

### SBPP-BEH-26:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH26-1** | When delegating to a self-contained collaborator, SHALL NOT pass `this` to the delegate. | Prevents unnecessary coupling |
| **CC-BEH26-2** | The delegate SHOULD be injectable via the delegating object's constructor. | Enables testing |

### SBPP-BEH-26:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Passing self unnecessarily**
`calculator.calculate(this)` when only `this.items` is needed.
Fix: Pass `this.items` — the delegate needs data, not the object.

### SBPP-BEH-26:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Delegate is independently testable | Delegate cannot call back — may need Self Delegation later |
| No circular reference | — |

### SBPP-BEH-26:10 - Rationale

Simple Delegation is the cleanest form of delegation and should be the default choice.
Escalate to Self Delegation only when the delegate genuinely needs to call back.

### SBPP-BEH-26:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Architecture (Martin, 2017):** Use-case classes delegate to repository and service
interfaces — all simple delegation. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Architecture (Martin, 2017) | Use-case delegation | **Adopt** |
| Spring DI (2015+) | Constructor-injected delegates | **Adopt** |

### SBPP-BEH-26:12 - Relations

* **Specialises:** SBPP-BEH-25 (Delegation)
* **Contrast with:** SBPP-BEH-27 (Self Delegation — back-reference needed)
* **Default choice:** Use before considering Self Delegation

### SBPP-BEH-26:End
