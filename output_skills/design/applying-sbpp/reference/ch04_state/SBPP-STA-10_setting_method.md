## SBPP-STA-10 - Setting Method

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-STA-10:1 - Problem frame

While Getting Methods provide read access, Setting Methods (setters) provide write access
to instance variables. Beck strongly cautions against over-exposing setters — they allow
external code to change object state directly, potentially breaking invariants and creating
hidden coupling. Modern Java/Kotlin best practice is to prefer immutable objects and
domain-meaningful state-transition methods over raw setters.

### SBPP-STA-10:2 - Problem

How do you allow controlled modification of an instance variable while maintaining
invariants and preventing inappropriate external mutation?

### SBPP-STA-10:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Setter allows controlled change ↔ setter exposes that the field is mutable |
| **Immutability** | Immutable objects are thread-safe and predictable ↔ setters enable convenient mutation |
| **Framework compatibility** | JPA/Jackson need setters for deserialization ↔ domain model should not be framework-driven |

### SBPP-STA-10:4 - Solution — Prefer domain-meaningful state-transition methods; use setters only when necessary

**Preferred: domain state-transition methods (not raw setters):**

```java
// ❌ Raw setter — exposes representation, no domain meaning
public void setStatus(PolicyStatus status) { this.status = status; }

// ✅ Domain-meaningful state transition
public void activate() {
    if (status != PolicyStatus.DRAFT && status != PolicyStatus.PENDING)
        throw new IllegalStateException("Can only activate draft or pending policies");
    this.status = PolicyStatus.ACTIVE;
}

public void cancel(CancellationReason reason) {
    if (status == PolicyStatus.CANCELLED) throw new IllegalStateException("Already cancelled");
    this.status = PolicyStatus.CANCELLED;
    this.cancellationReason = reason;
    this.cancelledAt = Instant.now();
}
```

**When setters are necessary (framework integration):**

```java
// ✅ Package-private setter for JPA — not part of public API
@Entity
public class PolicyEntity {
    private PolicyStatus status;

    void setStatus(PolicyStatus status) { this.status = status; }  // package-private for JPA
}
```

**Kotlin — `copy()` for immutable state changes:**

```kotlin
data class PolicyDraft(
    val id: PolicyId,
    val premium: Money,
    val status: PolicyStatus = PolicyStatus.DRAFT
) {
    // ✅ Domain transition returns new instance (immutable)
    fun submit(): PolicyDraft = copy(status = PolicyStatus.PENDING)
    fun approve(finalPremium: Money): PolicyDraft = copy(premium = finalPremium, status = PolicyStatus.ACTIVE)
}
```

### SBPP-STA-10:5 - Archetypal Grounding

**U.System:** `policy.activate()` documents a business event; `policy.setStatus(ACTIVE)` does not.
**U.Episteme:** A state-transition method enforces invariants; a setter bypasses them.

### SBPP-STA-10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Mutable state control in Java/Kotlin domain objects**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Public setters on domain entities are a DDD anti-pattern | Make setters private or package-private; expose only domain transitions |
| **Arch** | JPA entities need setters for ORM framework | Separate JPA entity from domain model; map between them |
| **Onto/Epist** | Raw setters expose representation; domain transitions encode business events | Prefer domain vocabulary: `activate()`, `cancel()`, `renew()` |
| **Prag** | Kotlin `data class copy()` enables immutable-style mutation | Use `copy()` for immutable updates; state machines for complex transitions |
| **Did** | IDE "Generate setters" creates anemic domain models instantly | Teach: domain objects should have behaviour, not just getters/setters |

### SBPP-STA-10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA10-1** | Public setters SHOULD NOT exist on domain entities; use domain state-transition methods instead. | Prevents invariant violations |
| **CC-STA10-2** | When setters are required by frameworks (JPA, Jackson), they SHALL be package-private or annotated `@JsonProperty` with `access = WRITE_ONLY`. | Limits framework exposure |
| **CC-STA10-3** | State-transition methods MUST validate the current state before applying the transition. | Maintains invariants |
| **CC-STA10-4** | Kotlin domain objects SHOULD use `data class copy()` or return new instances for state changes. | Immutability |

### SBPP-STA-10:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Anemic Domain Model**
Entity with public getters and setters for every field, no business methods.
Fix: Replace `setStatus()` with `activate()`, `cancel()`, `suspend()`.

**Anti-pattern 2: Setter bypassing invariant**
```java
policy.setExpiryDate(LocalDate.of(2020, 1, 1));  // past date — invalid
```
Fix: `policy.extendExpiryTo(date)` validates that `date` is in the future.

### SBPP-STA-10:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Domain transitions encode business events and validate invariants | More methods than raw getters/setters |
| Immutable Kotlin objects eliminate setter concerns | Requires separating domain model from persistence layer |
| Anemic domain model prevented | — |

### SBPP-STA-10:10 - Rationale

Beck's caution about setters is validated by DDD's critique of anemic domain models.
Modern Java/Kotlin best practice is to either make objects immutable (Kotlin `data class`,
Java record) or expose only domain-meaningful transition methods. Public setters on domain
entities are a design smell.

### SBPP-STA-10:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**DDD Anemic Domain Model (Fowler, widely cited post-2015):** The anemic domain model is an
anti-pattern; domain objects should have behaviour. *Adapt: replace setters with transitions.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 17 — minimise mutability. *Adopt.*

**Kotlin `data class copy()` (JetBrains, post-2016):** Immutable state change idiom. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| DDD Anemic Domain Model critique (Fowler, post-2015) | No raw setters on entities | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | Item 17 — minimise mutability | **Adopt** |
| Kotlin `data class copy()` (post-2016) | Immutable mutation idiom | **Adopt** |

### SBPP-STA-10:12 - Relations

* **Complement:** SBPP-STA-09 (Getting Method)
* **Implemented by:** Domain state-transition methods; Kotlin `copy()`
* **Constrained by:** DDD — entities should not have public setters
* **Replaces:** Raw setters in domain model

### SBPP-STA-10:End
