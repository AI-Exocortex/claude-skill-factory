## SBPP-BEH-29 - Pluggable Selector

> **Type:** Architectural (A)
> **Status:** Adapt
> **Normativity:** Normative

### SBPP-BEH-29:1 - Problem frame

Beck's original Pluggable Selector stored a Smalltalk selector (method name as a symbol)
and used `perform:` to invoke it dynamically. In Java/Kotlin, method references and
functional interfaces serve the same role more cleanly. This pattern maps to the use of
method references as pluggable behavior.

### SBPP-BEH-29:2 - Problem

How do you implement simple pluggable behaviour where the varying part is a method call
on the plugged object, expressed as a method reference?

### SBPP-BEH-29:3 - Forces

| Force | Tension |
|-------|---------|
| **Simplicity** | Method reference is one token ↔ full lambda is more explicit |
| **Type Safety** | Method reference is compile-checked ↔ string-based reflection is not |
| **Discoverability** | Method references appear in call hierarchies | — |

### SBPP-BEH-29:4 - Solution — Use method references as pluggable selectors

Store a method reference (Java `::`) or function reference (Kotlin `::`) rather than
a full lambda when the behavior is a single method call on an existing object.

**Java example:**

```java
public class ReportGenerator {
    private final Function<Policy, String> labelExtractor;

    public ReportGenerator(Function<Policy, String> labelExtractor) {
        this.labelExtractor = labelExtractor;
    }

    public List<String> generateLabels(List<Policy> policies) {
        return policies.stream().map(labelExtractor).collect(toList());
    }
}

// Pluggable Selector: method reference instead of lambda
var idReport       = new ReportGenerator(Policy::policyNumber);
var statusReport   = new ReportGenerator(Policy::statusCode);
var premiumReport  = new ReportGenerator(p -> p.getPremium().toDisplayString());
```

**Kotlin:**

```kotlin
class ReportGenerator(private val labelExtractor: (Policy) -> String) {
    fun generateLabels(policies: List<Policy>): List<String> = policies.map(labelExtractor)
}

val idReport      = ReportGenerator(Policy::policyNumber)
val statusReport  = ReportGenerator(Policy::statusCode)
```

### SBPP-BEH-29:5 - Archetypal Grounding

**U.System:** `Policy::policyNumber` is a pluggable selector — one method reference selects the behavior.
**U.Episteme:** Method references are compile-safe and appear in IDE call hierarchies; runtime reflection is not.

### SBPP-BEH-29:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Reflection-based selectors (original Smalltalk approach) are unsafe | Never use reflection; use method references instead |
| **Arch** | Method reference type inference can be confusing for complex overloads | Use explicit functional interface type to resolve ambiguity |
| **Onto/Epist** | Kotlin function references (`::`) have a slightly different syntax from Java | Accept both; document conventions |
| **Prag** | Identical to simple lambda in most cases; method reference is a style choice | Use method reference when it is more readable; lambda when it is not |
| **Did** | Explain the Java `::` syntax carefully to newcomers | Provide examples of instance method references vs. static vs. constructor |

### SBPP-BEH-29:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH29-1** | Pluggable selectors SHOULD use method references (`::`) rather than reflection. | Type safety and compile-time checking |
| **CC-BEH29-2** | Method reference type SHOULD be declared as a named functional interface when the intent is non-obvious. | Communicates the role of the selector |

### SBPP-BEH-29:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: String-based selector (Smalltalk-style in Java)**
`Method m = clazz.getMethod(selectorName); m.invoke(obj);`
Fix: Use method references; reflection is fragile and unsafe.

### SBPP-BEH-29:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Compile-safe plugging via method reference | None significant |
| Appears in IDE call hierarchies | — |

### SBPP-BEH-29:10 - Rationale

The Smalltalk `perform:` mechanism is unsafe in Java/Kotlin. Method references provide
an equivalent facility that is compile-safe and refactoring-friendly. This is an adaptation
of the original pattern that is strictly superior in Java/Kotlin.

### SBPP-BEH-29:11 - SoTA-Echoing

**Adoption verdict: ADOPT (adapted from Smalltalk reflection to Java/Kotlin method references)**

**Java 8 method references (JEP 126, 2014 onward):** The canonical Java Pluggable Selector. *Adopt.*

**Kotlin function references (post-2016):** `::` references are idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8 method references | Compile-safe selector | **Adopt** |
| Kotlin function references (post-2016) | Idiomatic `::` | **Adopt** |

### SBPP-BEH-29:12 - Relations

* **Specialises:** SBPP-BEH-28 (Pluggable Behavior — simplest form)
* **Contrast with:** SBPP-BEH-30 (Pluggable Block — more complex behavior)

### SBPP-BEH-29:End
