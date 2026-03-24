## SBPP-COL-25 - Searching Literal

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-25:1 - Problem frame

When code needs to test membership against a small fixed set of literal values known at
compile time — vowel characters, valid currency codes, supported operations — the Smalltalk
approach was `#($a $e $i $o $u) includes: aChar`. In Java/Kotlin the pattern maps to
`Set.of()` / `setOf()` with `contains()`, or Kotlin's `when`.

### SBPP-COL-25:2 - Problem

How do you test whether a value is one of a small fixed set of known literals, without
writing a chain of `||` conditions or a manual case statement?

### SBPP-COL-25:3 - Forces

| Force | Tension |
|-------|---------|
| **Readability** | `Set.of(a,e,i,o,u).contains(c)` is a one-liner ↔ `c=='a'||c=='e'...` grows with set size |
| **Maintainability** | Adding a new literal to a Set is one change ↔ `||` chain requires adding in the right place |
| **Performance** | `HashSet.contains()` is O(1) ↔ `||` chain is O(n) in the worst case but usually faster for very small sets |

### SBPP-COL-25:4 - Solution — Use `Set.of()` / `setOf()` for literal set membership; `EnumSet` for enums

**Java:**

```java
// ✅ Literal set membership
private static final Set<Character> VOWELS = Set.of('a', 'e', 'i', 'o', 'u');

public boolean isVowel(char c) {
    return VOWELS.contains(Character.toLowerCase(c));
}

// ✅ Valid value set
private static final Set<String> SUPPORTED_CURRENCIES = Set.of("USD", "EUR", "GBP", "JPY");

public void validateCurrency(String code) {
    if (!SUPPORTED_CURRENCIES.contains(code)) {
        throw new IllegalArgumentException("Unsupported currency: " + code);
    }
}

// ✅ EnumSet for enum literals (most efficient)
private static final Set<PolicyStatus> TERMINAL_STATUSES =
    EnumSet.of(PolicyStatus.CANCELLED, PolicyStatus.EXPIRED, PolicyStatus.VOID);

public boolean isTerminal(PolicyStatus status) {
    return TERMINAL_STATUSES.contains(status);
}
```

**Kotlin:**

```kotlin
// ✅ Literal set — setOf is read-only and preserves insertion order
private val VOWELS = setOf('a', 'e', 'i', 'o', 'u')
fun isVowel(c: Char) = c.lowercaseChar() in VOWELS

// ✅ Enum set via when (idiomatic Kotlin)
fun PolicyStatus.isTerminal(): Boolean = this in setOf(CANCELLED, EXPIRED, VOID)

// ✅ when expression for literal dispatch (when many literal branches)
fun describeRisk(code: RiskCode): String = when (code) {
    RiskCode.FIRE    -> "Fire damage"
    RiskCode.THEFT   -> "Theft"
    RiskCode.FLOOD   -> "Flood damage"
    else             -> "Other risk"
}
```

### SBPP-COL-25:5 - Archetypal Grounding

**U.System:** `TERMINAL_STATUSES.contains(status)` with `EnumSet` — O(1) via bit vector; the set of terminal statuses is declared once, used everywhere.
**U.Episteme:** Literal sets are business rules encoded as data — `Set.of(CANCELLED, EXPIRED, VOID)` makes the terminal status rule visible and maintainable.

### SBPP-COL-25:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Literal sets scattered in code are hard to maintain — extract to named constants | Declare as `private static final Set<T>` or `companion object` constant |
| **Arch** | `Set.of()` throws on null elements | Document: no nulls in literal sets |
| **Onto/Epist** | For enum types, `EnumSet` is more performant (bitset implementation) | Use `EnumSet.of()` for enum literal sets |
| **Prag** | Kotlin `when` is often more expressive than `in setOf(...)` for branching logic | Use `when` for multiple branches; `in setOf` for membership-only tests |
| **Did** | Teach `Set.of()` as the canonical literal set idiom | |

### SBPP-COL-25:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL25-1** | Membership tests against a fixed set of literals SHALL use `Set.of()` / `setOf()`, not `||` chains. | Maintainability |
| **CC-COL25-2** | Enum literal sets SHALL use `EnumSet.of()` for performance. | Optimal bit-vector implementation |
| **CC-COL25-3** | Literal sets SHALL be declared as named constants, not inline. | Reuse and discoverability |

### SBPP-COL-25:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u')` — Fix: `VOWELS.contains(c)`.
**Anti-pattern 2:** Inline `Set.of()` in the method body — Fix: extract to a named constant.

### SBPP-COL-25:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Business rules encoded as data, not code | Named constant required for reuse |
| O(1) membership test with `HashSet`/`EnumSet` | `Set.of()` throws on null |

### SBPP-COL-25:10 - Rationale

Beck's Searching Literal is directly `Set.of().contains()` in Java/Kotlin. The pattern
transforms a type-switch anti-pattern into a data-driven lookup.

### SBPP-COL-25:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 9+ `Set.of()` (JEP 269, 2017):** Immutable literal set factory. *Adopt.*
**Kotlin `setOf()` + `in` operator (post-2016):** Idiomatic. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 9+ `Set.of()` | Literal set | **Adopt** |
| Kotlin `in setOf()` (post-2016) | Idiomatic | **Adopt** |

### SBPP-COL-25:12 - Relations

* **Specialises:** SBPP-COL-04 (Set — used for literal set)
* **Alternative to:** SBPP-BEH-15 (Choosing Message — polymorphic dispatch for many branches)

### SBPP-COL-25:End
