## SBPP-STA-19 - Reusing Temporary Variable

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-19:1 - Problem frame

Some expressions produce a value that changes between calls (due to external state, time,
or IO) but must be used consistently within a method. Calling the expression multiple
times would give different results on each call, introducing subtle bugs. A local variable
captures the value at one point in time and reuses it safely.

### SBPP-STA-19:2 - Problem

How do you use an expression several times within a method when its value may change
between evaluations, requiring consistency across all uses?

### SBPP-STA-19:3 - Forces

| Force | Tension |
|-------|---------|
| **Correctness** | Must use the same value consistently ↔ expression changes between calls |
| **Clarity** | Named variable makes the intent explicit ↔ adds a line |
| **Concurrency** | Time-sensitive expressions must be captured at the right moment | — |

### SBPP-STA-19:4 - Solution — Capture the value once; reuse the captured value

```java
public PolicyRenewal computeRenewal(Policy policy) {
    // ✅ Capture "now" once — consistent throughout the method
    LocalDate today = LocalDate.now();

    boolean isExpiredByToday = policy.getExpiryDate().isBefore(today);
    LocalDate newExpiryDate  = today.plusYears(1);
    boolean isRenewalPremature = today.isBefore(policy.getExpiryDate().minusDays(30));

    return new PolicyRenewal(isExpiredByToday, newExpiryDate, isRenewalPremature);
}
// Without caching LocalDate.now(), each call could return a different date
// if the method runs near midnight!
```

**Kotlin:**

```kotlin
fun computeRenewal(policy: Policy): PolicyRenewal {
    val today = LocalDate.now()  // captured once

    val isExpiredByToday     = policy.expiryDate.isBefore(today)
    val newExpiryDate        = today.plusYears(1)
    val isRenewalPremature   = today.isBefore(policy.expiryDate.minusDays(30))

    return PolicyRenewal(isExpiredByToday, newExpiryDate, isRenewalPremature)
}
```

**Other reuse cases:**

```java
// ✅ Iterator-style: reading from a stream must only advance once
String line = reader.readLine();  // reuse 'line' — re-reading would advance the reader
if (line != null && !line.isBlank()) {
    process(line);
    log(line);
}
```

### SBPP-STA-19:5 - Archetypal Grounding

**U.System:** `val today = LocalDate.now()` — captured once, used three times — all three references are guaranteed the same date.
**U.Episteme:** The correctness argument: if `LocalDate.now()` were called three times at midnight, the first could return one day and the second another.

### SBPP-STA-19:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Time and state capture in Java/Kotlin methods**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Time-dependent methods are hard to test without injectable clock | Use `Clock` injection; capture `clock.instant()` or `clock.date()` |
| **Arch** | Captured value may be stale if the method runs long | Acceptable for most domain methods; document if long-running |
| **Onto/Epist** | "Now" is the most obvious case; also applies to UUID generation, random numbers | Apply to any expression that may produce different results on repeated calls |
| **Prag** | Kotlin `val` makes reuse variables immutable — correct by default | Use `val` always for reuse variables |
| **Did** | Midnight bug is a classic interview example | Use it to teach the importance of this pattern |

### SBPP-STA-19:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA19-1** | Time-sensitive values (current date/time) used multiple times SHALL be captured in a local. | Consistency |
| **CC-STA19-2** | IO-advancing expressions (stream reads) used multiple times MUST be captured. | Correctness |
| **CC-STA19-3** | Reuse variables SHALL be `final`/`val`. | Prevents reassignment |

### SBPP-STA-19:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Midnight bug**
```java
if (policy.getExpiry().isBefore(LocalDate.now())) {
    renew(policy, LocalDate.now().plusYears(1));  // could be a different day!
}
```
Fix: `LocalDate today = LocalDate.now();` and reuse `today`.

### SBPP-STA-19:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Prevents time-related correctness bugs | One extra line per captured value |
| Tests can inject a controlled clock | — |

### SBPP-STA-19:10 - Rationale

Reusing Temporary Variable is a correctness pattern, not just a readability one. The
classic midnight bug (calling `LocalDate.now()` twice near a day boundary) is a real
production defect that this pattern prevents.

### SBPP-STA-19:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Avoid repeated calls to methods that change over time. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Consistency of repeated calls | **Adopt** |
| Java Clock API (Java 8+) | Injectable time source for testability | **Adopt** |

### SBPP-STA-19:12 - Relations

* **Specialises:** SBPP-STA-15 (Temporary Variable — reuse use case)
* **Motivated by:** Correctness (not just readability)
* **Contrast with:** SBPP-STA-17 (Caching Temporary Variable — motivated by performance)

### SBPP-STA-19:End
