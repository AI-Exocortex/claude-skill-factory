## SBPP-STA-03 - Explicit Initialization

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-03:1 - Problem frame

When an instance variable has a known, fixed default value, the question is where to
express that default: inline in the field declaration, in the constructor, or deferred
to first use (Lazy Initialization). Explicit Initialization declares the default at the
field declaration site or in the constructor — it is always set before use.

### SBPP-STA-03:2 - Problem

How do you initialize an instance variable to its default value so that the initial
state is always clear, deterministic, and impossible to miss?

### SBPP-STA-03:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | Inline defaults are obvious at the declaration ↔ they scatter across the class |
| **Flexibility** | Constructor initialization supports logic ↔ inline is simpler |
| **Fail-Fast** | Fields always valid after construction ↔ Lazy Initialization defers validity |

### SBPP-STA-03:4 - Solution — Initialize all fields at declaration or in the constructor; never leave nulls unexpectedly

Set every field to its default value either at the declaration site (Java/Kotlin inline
initialization) or in the constructor. Never rely on Java's implicit `null`/`0`/`false`
defaults for domain fields.

**Java example:**

```java
public final class PolicyDraft {
    // ✅ Explicit inline initialization — default clear at declaration
    private PolicyStatus status = PolicyStatus.DRAFT;
    private List<CoverageItem> items = new ArrayList<>();
    private int version = 1;
    private LocalDate createdAt = LocalDate.now();

    // Constructor initializes domain-required fields
    private final PolicyId id;
    private final CustomerId holderId;

    public PolicyDraft(PolicyId id, CustomerId holderId) {
        this.id       = Objects.requireNonNull(id);
        this.holderId = Objects.requireNonNull(holderId);
        // status, items, version, createdAt already defaulted above
    }
}
```

**Kotlin example:**

```kotlin
class PolicyDraft(
    val id: PolicyId,
    val holderId: CustomerId
) {
    // ✅ Explicit inline defaults in Kotlin
    var status: PolicyStatus = PolicyStatus.DRAFT
    val items: MutableList<CoverageItem> = mutableListOf()
    var version: Int = 1
    val createdAt: LocalDate = LocalDate.now()
}

// ✅ Or via primary constructor defaults
data class PolicyConfig(
    val maxItems: Int = 10,
    val allowPartialCoverage: Boolean = false,
    val currency: Currency = Currency.USD
)
```

**Rule:** Fields that must be non-null at construction time → constructor parameter.
Fields with known defaults → inline initialization. Use `Objects.requireNonNull` / Kotlin
`requireNotNull` for all non-optional parameters.

### SBPP-STA-03:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Every field has a deterministic initial value set at construction — no NullPointerException surprises.
*Show:* `new PolicyDraft(id, holder)` — `status`, `items`, `version`, `createdAt` are all
set without reading the constructor body.

**U.Episteme (design reasoning):**
*Tell:* Explicit initialization makes the object's initial state a documented contract, not an implicit assumption.
*Show:* A reviewer can confirm "draft policies start at version 1" by reading the declaration — no runtime trace needed.

### SBPP-STA-03:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Instance variable initialization in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Inline defaults in Java are not enforced — developers can still leave fields uninitialised | Use `@NonNull` annotations + NullAway/Error Prone for enforcement |
| **Arch** | `LocalDate.now()` inline creates hidden test-time dependency on system clock | Use an injected clock for time-dependent defaults in production code |
| **Onto/Epist** | "Default value" may hide domain assumptions | Name the constant explicitly: `INITIAL_VERSION = 1` not magic `1` |
| **Prag** | Kotlin primary constructor default parameters eliminate most initialization boilerplate | Use them; they make defaults visible at the constructor call site |
| **Did** | New developers may rely on Java's `null` default for reference fields | Enforce non-null by default policy; use NullAway or Kotlin's type system |

### SBPP-STA-03:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA03-1** | All instance fields SHALL be initialized to a meaningful value at declaration or in the constructor. | Prevents uninitialised-field NullPointerExceptions |
| **CC-STA03-2** | Time-dependent defaults (e.g., `LocalDate.now()`) SHOULD use an injectable clock. | Testability |
| **CC-STA03-3** | Magic literal defaults SHOULD be named constants. | Communicates intent |
| **CC-STA03-4** | Constructor parameters MUST be validated with `requireNonNull`/`require` before assignment. | Fail-fast on invalid input |

### SBPP-STA-03:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Relying on Java's null default**
```java
private List<CoverageItem> items;  // implicitly null — NPE waiting
```
Fix: `private List<CoverageItem> items = new ArrayList<>();`

**Anti-pattern 2: Half-Initialized Object**
Constructor sets some fields; others are set via setters before use — object is in an
invalid intermediate state. Fix: All mandatory state set in the constructor; optional
state defaulted inline.

### SBPP-STA-03:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Object is always in a valid state after construction | Slightly more constructor code |
| NPEs from uninitialised fields are structurally prevented | Inline defaults can hide clock/context dependencies |
| Kotlin primary constructor defaults are part of the API | — |

### SBPP-STA-03:10 - Rationale

Explicit Initialization is the fail-safe approach: all state is set before any method can
use it. Java records and Kotlin data classes enforce this by construction. For mutable
classes, the discipline must be applied manually, aided by NullAway or Kotlin's
non-nullable type system.

### SBPP-STA-03:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 50 (make defensive copies when needed) and
Item 72 (favour the use of standard exceptions) both assume well-initialised objects. *Adopt.*

**NullAway (Uber, 2017+):** Static analysis tool that enforces non-null field initialisation
in Java. *Adopt.*

**Kotlin type system (post-2016):** Non-nullable types (`T` not `T?`) enforce initialisation
at compile time. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Validated, initialised objects | **Adopt** |
| NullAway (Uber, 2017+) | Compile-time null enforcement | **Adopt** |
| Kotlin non-nullable types (post-2016) | Language-enforced init | **Adopt** |

### SBPP-STA-03:12 - Relations

* **Applied to:** SBPP-STA-01 (Common State fields)
* **Contrast with:** SBPP-STA-04 (Lazy Initialization — defer until needed)
* **Supports:** SBPP-STA-05 (Default Value Method — for complex defaults)
* **Enforced by:** Constructor design, NullAway, Kotlin type system

### SBPP-STA-03:End
