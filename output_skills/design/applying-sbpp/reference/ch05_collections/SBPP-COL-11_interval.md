## SBPP-COL-11 - Interval

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-11:1 - Problem frame

Sequential ranges of numbers or dates are common in insurance microservices: age bands,
coverage periods, premium bands, instalment schedules. Representing them as explicit
arrays wastes memory and obscures the range semantics. Java/Kotlin range idioms
communicate the sequential structure directly.

### SBPP-COL-11:2 - Problem

How do you represent a sequence of consecutive numbers or a range, without allocating
storage for every individual element?

### SBPP-COL-11:3 - Forces

| Force | Tension |
|-------|---------|
| **Memory** | Range is logically infinite (or large) ↔ storing all elements is impractical |
| **Expressiveness** | `IntStream.range()` communicates "sequence" ↔ a plain array does not |
| **Type Safety** | Java/Kotlin range types vary by domain (int range vs date range) | |

### SBPP-COL-11:4 - Solution — Use `IntStream.range()`, `IntStream.rangeClosed()`, Kotlin ranges, or domain range value objects

**Java numeric range:**

```java
// ✅ Iteration over a range
IntStream.range(1, 13).forEach(month -> processMonth(month));

// ✅ Collect to list when needed
List<Integer> months = IntStream.rangeClosed(1, 12).boxed().collect(toList());

// ✅ Range-based calculation without allocation
long sum = LongStream.rangeClosed(1, 100).sum();
```

**Kotlin ranges:**

```kotlin
// ✅ Kotlin range is a first-class language construct
for (month in 1..12) processMonth(month)

// ✅ Range check
val isValidAge = applicantAge in 18..80

// ✅ Step range
for (year in 2020..2030 step 2) processYear(year)

// ✅ Downward range
for (i in 10 downTo 1) countDown(i)

// ✅ Convert to list only when needed
val months: List<Int> = (1..12).toList()
```

**Domain range value object (for business ranges):**

```java
// ✅ Business range as a value object
public record AgeRange(int minAge, int maxAge) {
    public AgeRange {
        if (minAge > maxAge) throw new IllegalArgumentException("invalid range");
    }
    public boolean contains(int age) { return age >= minAge && age <= maxAge; }
    public IntStream stream() { return IntStream.rangeClosed(minAge, maxAge); }
}

AgeRange youngDriver = new AgeRange(18, 25);
boolean isYoung = youngDriver.contains(applicant.getAge());
```

### SBPP-COL-11:5 - Archetypal Grounding

**U.System:** `1..12` in Kotlin — a range literal communicates "all twelve months" without allocating 12 integers.
**U.Episteme:** `applicantAge in 18..80` reads as a business rule; `applicantAge >= 18 && applicantAge <= 80` does not.

### SBPP-COL-11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Range representation in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Range boundaries (inclusive/exclusive) are a frequent source of off-by-one errors | Use `rangeClosed` when upper bound is inclusive; document explicitly |
| **Arch** | `IntStream.range` is exclusive-end; `IntStream.rangeClosed` is inclusive | Establish team convention: prefer `rangeClosed` for business ranges |
| **Onto/Epist** | Date ranges need a domain value object (`DateRange`) — no built-in | Implement `DateRange` with `LocalDate` start/end and `contains(LocalDate)` |
| **Prag** | Kotlin range `..` is inclusive; `until` is exclusive | Use `..` for business ranges; `until` for loop indices |
| **Did** | Java has no range literal; developers may not know `IntStream.range` | Show the `IntStream` idioms; teach Kotlin `..` as the more expressive alternative |

### SBPP-COL-11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL11-1** | Numeric sequences SHALL use `IntStream.range()`/`rangeClosed()` (Java) or `..` ranges (Kotlin) instead of allocating arrays. | Memory efficiency |
| **CC-COL11-2** | Business ranges (age bands, date periods) SHOULD be domain value objects with `contains()` and `stream()` methods. | Domain expressiveness |
| **CC-COL11-3** | Range boundaries (inclusive vs exclusive) MUST be documented or made explicit in method names. | Prevents off-by-one errors |

### SBPP-COL-11:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Array of sequential integers**
`int[] months = {1,2,3,4,5,6,7,8,9,10,11,12}` — Fix: `IntStream.rangeClosed(1, 12)`.

**Anti-pattern 2: Off-by-one boundary confusion**
`IntStream.range(1, 12)` produces 1..11, not 1..12. Fix: use `IntStream.rangeClosed(1, 12)`.

### SBPP-COL-11:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| No memory allocation for the range itself | Inclusive/exclusive boundary must be explicit |
| Kotlin `..` ranges read as business rules | Java lacks range literal — use `IntStream` |

### SBPP-COL-11:10 - Rationale

Smalltalk's `Interval` maps to Java/Kotlin ranges. Kotlin's range literal `..` is the closest
equivalent — first-class language syntax that communicates sequential structure.
For domain ranges (age, date, premium), a value object wrapping the bounds is cleaner.

### SBPP-COL-11:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8+ `IntStream.range()` (post-2014):** The Java Interval equivalent. *Adopt.*

**Kotlin ranges (`..`, `until`, `downTo`) (post-2016):** First-class language ranges. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8+ `IntStream.range/rangeClosed` | Numeric range iteration | **Adopt** |
| Kotlin range literals (post-2016) | First-class range syntax | **Adopt** |

### SBPP-COL-11:12 - Relations

* **Specialises:** SBPP-COL-09 (Array — sequential numeric variant with no allocation)
* **Uses:** Java `IntStream`, Kotlin `IntRange`, `LongRange`

### SBPP-COL-11:End
