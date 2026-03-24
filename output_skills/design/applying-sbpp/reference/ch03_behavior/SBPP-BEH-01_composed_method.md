## SBPP-BEH-01 - Composed Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-01:1 - Problem frame

In Java and Kotlin microservices, methods grow over time as developers add logic
incrementally. A method that starts small accumulates conditionals, loops, and
local variables until it performs many conceptually distinct operations at different
levels of abstraction, making it hard to read, test, or extend.

### SBPP-BEH-01:2 - Problem

How do you divide a class's logic into methods so that each method communicates
clearly what it does, remains at a single level of abstraction, and can be
independently understood or replaced?

### SBPP-BEH-01:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability vs Brevity** | Short methods aid comprehension ↔ many small methods scatter context |
| **Single Abstraction Level** | Uniform abstraction within a method ↔ convenience of inline detail |
| **Testability vs Cohesion** | Fine-grained methods are individually testable ↔ fragmented logic is hard to follow |
| **Performance vs Clarity** | Inlining avoids call overhead ↔ JIT compilers eliminate most overhead anyway |

### SBPP-BEH-01:4 - Solution — Compose methods from single-abstraction-level calls

Divide every method so that it does exactly one thing at one level of abstraction.
Extract any sub-operation that can be named meaningfully into its own private method.
Name each extracted method with an intention-revealing verb phrase.

**Java example:**

```java
// ❌ Mixed abstraction levels
public void processOrder(Order order) {
    // validation
    if (order.getItems().isEmpty()) throw new IllegalArgumentException("empty");
    if (order.getCustomer() == null) throw new IllegalArgumentException("no customer");
    // calculate total
    double total = 0;
    for (var item : order.getItems()) total += item.price() * item.quantity();
    order.setTotal(total);
    // persist
    repository.save(order);
    eventBus.publish(new OrderPlaced(order.getId()));
}

// ✅ Composed method — each call at the same abstraction level
public void processOrder(Order order) {
    validateOrder(order);
    calculateTotal(order);
    persistOrder(order);
}

private void validateOrder(Order order) {
    if (order.getItems().isEmpty()) throw new IllegalArgumentException("Order has no items");
    if (order.getCustomer() == null) throw new IllegalArgumentException("Order has no customer");
}

private void calculateTotal(Order order) {
    double total = order.getItems().stream()
        .mapToDouble(item -> item.price() * item.quantity())
        .sum();
    order.setTotal(total);
}

private void persistOrder(Order order) {
    repository.save(order);
    eventBus.publish(new OrderPlaced(order.getId()));
}
```

**Kotlin example:**

```kotlin
// ✅ Composed method in Kotlin
fun processOrder(order: Order) {
    validateOrder(order)
    order.calculateTotal()
    persistOrder(order)
}

private fun validateOrder(order: Order) {
    require(order.items.isNotEmpty()) { "Order has no items" }
    requireNotNull(order.customer) { "Order has no customer" }
}

private fun Order.calculateTotal() {
    total = items.sumOf { it.price * it.quantity }
}

private fun persistOrder(order: Order) {
    repository.save(order)
    eventBus.publish(OrderPlaced(order.id))
}
```

**Rule:** A composed method body should read like a table of contents — each line names
a step, none of the lines implements one.

### SBPP-BEH-01:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Every public service method delegates to private helpers, each at one abstraction level.
*Show:* `processOrder()` calls `validateOrder()`, `calculateTotal()`, `persistOrder()` — three words,
three concepts, zero implementation detail visible at the top level.

**U.Episteme (design reasoning):**
*Tell:* Methods that mix abstraction levels force readers to context-switch mentally between
"what is being done" and "how it is done."
*Show:* When `processOrder` is one screen of mixed code, a reviewer cannot quickly confirm the
business rule; when it is three lines, the review is instant.

### SBPP-BEH-01:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin OO development**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Enforcement requires code-review culture; no static rule catches mixed abstraction levels | Use architecture fitness functions or linting (e.g., PMD method length rules) as proxies |
| **Arch** | Fine-grained decomposition can create class files with many private methods, inflating apparent complexity | Group private helpers with clear naming prefixes or nested static classes |
| **Onto/Epist** | "Single abstraction level" is a subjective judgment that varies by team experience | Provide examples in team guidelines; calibrate during pair/mob programming |
| **Prag** | IDE navigation is needed to follow the call chain; plain reading is interrupted | Modern IDEs (IntelliJ, VS Code) make jump-to-definition instant; cost is low |
| **Did** | New developers may create gratuitous one-liner extractions that fragment logic without clarity gain | Apply only when the extracted method has a non-trivial name that reveals intent |

### SBPP-BEH-01:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH01-1** | A method SHALL contain statements at only one level of abstraction. | Enforces single-level decomposition |
| **CC-BEH01-2** | Each extracted helper method SHALL be named with a verb phrase that reveals its intent without reading its body. | Ensures self-documenting structure |
| **CC-BEH01-3** | Methods SHOULD be short enough to read without scrolling (≤ 20 lines as a guideline). | Supports cognitive chunking |
| **CC-BEH01-4** | Composed methods MUST NOT expose implementation details of their sub-operations at the call site. | Maintains abstraction boundary |

### SBPP-BEH-01:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: The Stepdown Fallacy**
Extracting methods but immediately inlining their detail via comments:
```java
public void processOrder(Order order) {
    // --- Step 1: validate ---
    if (order.getItems().isEmpty()) ...
    // --- Step 2: calculate ---
    double total = 0; ...
}
```
Fix: Actually extract methods; comments that repeat what the code does are a smell that extraction is needed.

**Anti-pattern 2: Micro-fragmentation**
Extracting every expression into a one-liner method with a name no clearer than the expression itself:
```java
private boolean isListEmpty(List<?> list) { return list.isEmpty(); }
```
Fix: Only extract when the extracted name communicates *intent*, not just *mechanics*.

**Anti-pattern 3: Utility Dump**
Collecting all "helper" methods in one class, losing cohesion. Fix: Keep helpers private to the class
that composes them; promote to shared utility only when reused.

### SBPP-BEH-01:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Methods become skimmable; intent is visible at top level | More methods per class — mitigated by IDE navigation |
| Extracted methods are individually unit-testable (via package-private or reflection in tests) | Slightly more verbose code — justified by maintenance savings |
| Easier to override individual steps in subclasses (Template Method) | Subclasses can override unexpectedly — mitigated by `final` on helpers |
| Reduces duplicate code by making steps discoverable for reuse | — |

### SBPP-BEH-01:10 - Rationale

Composed Method is the foundation of readable OO code. Beck identified it as the most
important pattern in Smalltalk, and the principle translates directly to Java/Kotlin. The
Single Responsibility Principle at the method level is exactly what this pattern operationalises.

Java's verbosity historically discouraged small methods due to boilerplate, but Java 17+
records, sealed classes, and expression switches reduce this friction. Kotlin's extension
functions and function literals make composition even more idiomatic.

The JVM's JIT compiler (HotSpot, GraalVM) aggressively inlines small methods, so the
performance concern Beck addressed in Smalltalk is effectively irrelevant in modern JVM
deployments. Profile before pessimising with longer methods.

### SBPP-BEH-01:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008 / widely cited post-2015):** Functions should do one thing, do it well,
and do it only. This is identical to Composed Method. The pattern is foundational to every
contemporary Java/Kotlin style guide. *Adopt directly.*

**Refactoring (Fowler et al., 2018 — 2nd edition):** "Extract Function" is the primary refactoring
technique in the catalogue. Fowler's criterion — "if a piece of code needs a comment to explain
what it does, extract it into a function named after what it does" — is a precise operational
definition of Composed Method. *Adopt directly.*

**Effective Java (Bloch, 2018 — 3rd edition):** Item 67 ("Optimize judiciously") explicitly notes
that the JVM inlines small methods, removing the last historical objection. *Adopt: removes
performance concern.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, 2008/2015+) | Identical "one thing" rule | **Adopt** |
| Refactoring 2nd ed. (Fowler, 2018) | "Extract Function" as primary refactoring | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | JIT inlining confirms no performance cost | **Adopt** |

### SBPP-BEH-01:12 - Relations

* **Implements:** Single Responsibility Principle (method level)
* **Enables:** SBPP-BEH-14 (Message), SBPP-BEH-18 (Intention Revealing Selector)
* **Relates to:** SBPP-BEH-10 (Method Object — when extraction needs its own state)
* **Constrained by:** SBPP-BEH-13 (Method Comment — composed methods rarely need inline comments)
* **Constrains:** SBPP-BEH-07 (Query Method — each query should be composed if complex)

### SBPP-BEH-01:End
