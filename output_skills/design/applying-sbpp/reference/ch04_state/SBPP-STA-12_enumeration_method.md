## SBPP-STA-12 - Enumeration Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-12:1 - Problem frame

When a collection is private, callers may need to iterate over its elements. Rather than
exposing the collection or providing dozens of query methods, an enumeration method
gives callers a way to process each element via a lambda — without exposing the
internal structure at all.

### SBPP-STA-12:2 - Problem

How do you provide safe, general-purpose iteration over a private collection's elements
without exposing the collection type or structure?

### SBPP-STA-12:3 - Forces

| Force | Tension |
|-------|---------|
| **Generality** | Lambda-based enumeration is general ↔ specific query methods are more explicit |
| **Encapsulation** | Collection type hidden ↔ callers need to iterate |
| **Stream vs Consumer** | Java Stream is richer ↔ Consumer is simpler |

### SBPP-STA-12:4 - Solution — Provide a method that accepts a Consumer/lambda to iterate elements

```java
public class InsurancePolicy {
    private final List<Claim> claims = new ArrayList<>();

    // ✅ Enumeration Method — provides iteration without exposing the collection
    public void forEachClaim(Consumer<Claim> action) {
        claims.forEach(action);
    }

    // ✅ Stream-based enumeration for richer operations
    public Stream<Claim> claimsStream() {
        return claims.stream();
    }
}

// Usage — caller provides the logic
policy.forEachClaim(claim -> auditLog.record(claim.getId()));
long openClaims = policy.claimsStream().filter(c -> c.isOpen()).count();
```

**Kotlin:**

```kotlin
class InsurancePolicy {
    private val _claims = mutableListOf<Claim>()

    // ✅ Extension-style enumeration via sequence
    fun forEachClaim(action: (Claim) -> Unit) = _claims.forEach(action)
    fun claims(): Sequence<Claim> = _claims.asSequence()
}

policy.forEachClaim { claim -> auditLog.record(claim.id) }
val openCount = policy.claims().count { it.isOpen }
```

### SBPP-STA-12:5 - Archetypal Grounding

**U.System:** `policy.forEachClaim { ... }` — caller provides the operation; policy controls the collection.
**U.Episteme:** A `Stream` or `Sequence` gives callers the full power of functional operations without exposing mutable internals.

### SBPP-STA-12:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Collection iteration in Java/Kotlin domain objects**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Both `forEachX` and `xStream()` may be needed — doubles the API | Provide Stream/Sequence only; deprecate `forEach` variant |
| **Arch** | Java Stream is lazy and must be consumed once | Document stream lifecycle |
| **Onto/Epist** | `Stream<Claim>` exposes that claims are stored as a collection | Acceptable — the element type is part of the domain API |
| **Prag** | Kotlin `Sequence` is lazy like Java Stream; `List` view may be simpler | Use whichever matches the use case |
| **Did** | New developers may iterate without terminal operations on Java Stream | Teach: streams must be consumed; add `collect()`, `count()`, `findFirst()` |

### SBPP-STA-12:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA12-1** | Enumeration methods SHALL NOT expose the mutable backing collection. | Encapsulation |
| **CC-STA12-2** | Java Stream-based enumeration methods SHOULD name them `xStream()` or return via `Stream`. | Naming clarity |
| **CC-STA12-3** | Kotlin enumeration SHOULD return `Sequence<T>` for lazy evaluation or `List<T>` for eager. | Idiomatic Kotlin |

### SBPP-STA-12:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Iterator exposure**
```java
public Iterator<Claim> claimsIterator() { return claims.iterator(); }
// Returns internal iterator — caller can call remove()
```
Fix: Return a `Stream` or use `forEachClaim(Consumer)`.

### SBPP-STA-12:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Full functional operations (filter, map, count) without exposing internals | Stream consumed once in Java — document |
| Collection type hidden | — |

### SBPP-STA-12:10 - Rationale

Java Streams and Kotlin Sequences are the modern Enumeration Method. They provide
the full power of functional collection processing while keeping the backing collection
private. This is a significant improvement over Beck's original `do:` block approach.

### SBPP-STA-12:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java 8 Stream API (post-2014):** The canonical Java Enumeration Method. *Adopt.*
**Kotlin Sequence (post-2016):** Lazy Enumeration Method. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java 8 Stream (post-2014) | Functional iteration | **Adopt** |
| Kotlin Sequence (post-2016) | Lazy functional iteration | **Adopt** |

### SBPP-STA-12:12 - Relations

* **Extends:** SBPP-STA-11 (Collection Accessor Method — read-only iteration)
* **Implemented by:** Java Stream, Kotlin Sequence
* **Enables:** Functional collection operations (filter, map, reduce)

### SBPP-STA-12:End
