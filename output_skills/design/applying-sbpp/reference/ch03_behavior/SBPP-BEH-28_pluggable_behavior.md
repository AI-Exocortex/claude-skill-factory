## SBPP-BEH-28 - Pluggable Behavior

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-28:1 - Problem frame

In Java/Kotlin microservices, some objects need to behave differently based on
configuration, context, or user preference — not on their type. Creating a subclass for
every behavioural variant bloats the class hierarchy. Pluggable Behavior solves this by
parameterising the varying logic.

### SBPP-BEH-28:2 - Problem

How do you allow an object's behaviour to vary at runtime without creating a subclass
for each variation?

### SBPP-BEH-28:3 - Forces

| Force | Tension |
|-------|---------|
| **Flexibility** | Behaviour configured at runtime ↔ static type hierarchy does not accommodate this |
| **Class Proliferation** | Each variation as a subclass creates many thin classes ↔ plugins avoid this |
| **Testability** | Pluggable behaviour can be injected as a test double ↔ subclasses cannot be easily substituted |

### SBPP-BEH-28:4 - Solution — Store the varying behaviour as a functional interface field

Extract the varying behaviour into a functional interface or `Function<>`. Store an
instance as a field. Configure at construction time.

**Java example:**

```java
// ❌ Subclass explosion
class PolicyFormatter { String format(Policy p) { return p.getId().toString(); } }
class VerbosePolicyFormatter extends PolicyFormatter { ... }
class JsonPolicyFormatter extends PolicyFormatter { ... }
class CsvPolicyFormatter extends PolicyFormatter { ... }

// ✅ Pluggable Behavior
public class PolicyProcessor {
    private final Function<Policy, String> formatter;    // pluggable behavior

    public PolicyProcessor(Function<Policy, String> formatter) {
        this.formatter = formatter;
    }

    public String process(Policy policy) {
        return formatter.apply(policy);
    }
}

// Different behaviors plugged in at construction
var verbose = new PolicyProcessor(p -> p.getId() + ": " + p.getStatus() + " " + p.getPremium());
var json    = new PolicyProcessor(p -> jsonMapper.writeValueAsString(p));
var csv     = new PolicyProcessor(p -> p.getId() + "," + p.getStatus());
```

**Kotlin:**

```kotlin
class PolicyProcessor(private val formatter: (Policy) -> String) {
    fun process(policy: Policy): String = formatter(policy)
}

val verbose = PolicyProcessor { "${it.id}: ${it.status} ${it.premium}" }
val json    = PolicyProcessor { jsonMapper.writeValueAsString(it) }
```

### SBPP-BEH-28:5 - Archetypal Grounding

**U.System:** `PolicyProcessor` accepts any `Policy → String` function; callers plug in their format.
**U.Episteme:** The Strategy pattern is the formal OO expression of Pluggable Behavior — the strategy interface is the plug point.

### SBPP-BEH-28:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Lambda behaviour is opaque in logs and stack traces | Use named classes or method references for important behaviors |
| **Arch** | Plugged functions capture external state (closures) — can be tricky to reason about | Prefer pure functions for pluggable behavior; avoid capturing mutable state |
| **Onto/Epist** | "Pluggable" suggests loose coupling — ensure the plug point's contract is clear | Define the functional interface or Function signature precisely |
| **Prag** | Kotlin's function types make plugging trivial | Use liberally; apply Pluggable Behavior wherever subclass proliferation would occur |
| **Did** | This IS the Strategy pattern — introduce via GoF Strategy | Teach together |

### SBPP-BEH-28:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH28-1** | Pluggable behavior fields SHALL use a functional interface or `Function<>` type. | Clear plugging contract |
| **CC-BEH28-2** | Pluggable behaviors SHOULD be pure functions (no side effects, no captured mutable state). | Predictability |
| **CC-BEH28-3** | The default behavior SHOULD be provided (via a constant or constructor default). | Usability |

### SBPP-BEH-28:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Pluggable Mutation**
Plugged function modifies shared state. Fix: Pluggable behaviors should return a value; side
effects should be explicit.

**Anti-pattern 2: Unconfigured Plug Point**
`formatter` field can be null. Fix: Provide a non-null default.

### SBPP-BEH-28:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| No subclass per variation | Lambda capture can hide complexity |
| Behavior injectable as test double | Contract of the function must be explicit |
| Compose multiple behaviors easily | — |

### SBPP-BEH-28:10 - Rationale

Pluggable Behavior is the first-class version of the Strategy pattern in functional-style
Java and Kotlin. Java 8+ lambdas and Kotlin function types make this idiomatic.

### SBPP-BEH-28:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**GoF Strategy (widely applied post-2015):** Pluggable Behavior is Strategy with functional types. *Adopt.*

**Java 8+ lambdas / Kotlin function types (post-2016):** Make plugging trivial. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| GoF Strategy (post-2015) | Strategy = Pluggable Behavior | **Adopt** |
| Java 8+ / Kotlin function types | Idiomatic implementation | **Adopt** |

### SBPP-BEH-28:12 - Relations

* **Implements:** GoF Strategy Pattern
* **Specialised by:** SBPP-BEH-29 (Pluggable Selector), SBPP-BEH-30 (Pluggable Block)
* **Enables:** SBPP-BEH-11 (Execute Around Method uses pluggable work block)

### SBPP-BEH-28:End
