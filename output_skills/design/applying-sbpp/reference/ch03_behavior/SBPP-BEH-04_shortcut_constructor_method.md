## SBPP-BEH-04 - Shortcut Constructor Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-04:1 - Problem frame

When a Constructor Method (BEH-02) is the primary way to create an object, calling it
repeatedly at many sites in a large Java/Kotlin codebase is verbose. For ubiquitous
value types used in hundreds of call sites — `Money`, `Coordinate`, `Range`, `Duration`
— every constructor invocation adds noise that obscures the business logic around it.

### SBPP-BEH-04:2 - Problem

How do you provide a concise creation syntax for objects that are created pervasively,
without sacrificing the encapsulation and intent-communication of the full Constructor
Method?

### SBPP-BEH-04:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness vs Brevity** | Named factory communicates intent ↔ repeated verbose calls obscure surrounding logic |
| **Discoverability vs Convenience** | Full name is self-documenting ↔ short alias requires knowing the convention |
| **API Stability** | Shortcut aliases are part of the public API and may be harder to remove | Versioned deprecation mitigates |

### SBPP-BEH-04:4 - Solution — Provide a terse static factory alias for the most common creation path

Identify the single most common creation scenario. Provide a very short static method
(commonly `of(…)`, `at(…)`, or the type's own abbreviation) as an alias for the
verbose Constructor Method.

**Java example:**

```java
public final class Coordinate {
    private final double lat;
    private final double lon;

    private Coordinate(double lat, double lon) {
        this.lat = lat;
        this.lon = lon;
    }

    // Full Constructor Method — verbose, self-documenting
    public static Coordinate atLatitudeLongitude(double lat, double lon) {
        validateRange(lat, lon);
        return new Coordinate(lat, lon);
    }

    // Shortcut Constructor Method — terse alias for pervasive use
    public static Coordinate at(double lat, double lon) {
        return atLatitudeLongitude(lat, lon);
    }

    private static void validateRange(double lat, double lon) {
        if (lat < -90 || lat > 90) throw new IllegalArgumentException("Invalid latitude: " + lat);
        if (lon < -180 || lon > 180) throw new IllegalArgumentException("Invalid longitude: " + lon);
    }
}

// At call sites: terse form reduces noise in business code
var depot  = Coordinate.at(51.5074, -0.1278);
var pickup = Coordinate.at(48.8566,  2.3522);
```

**Kotlin example:**

```kotlin
data class Coordinate private constructor(val lat: Double, val lon: Double) {
    companion object {
        fun atLatitudeLongitude(lat: Double, lon: Double): Coordinate {
            require(lat in -90.0..90.0) { "Invalid latitude: $lat" }
            require(lon in -180.0..180.0) { "Invalid longitude: $lon" }
            return Coordinate(lat, lon)
        }

        // Shortcut: idiomatic Kotlin uses 'of' or domain-specific short name
        fun at(lat: Double, lon: Double) = atLatitudeLongitude(lat, lon)
    }
}

val depot  = Coordinate.at(51.5074, -0.1278)
val pickup = Coordinate.at(48.8566,  2.3522)
```

**Rule:** Reserve shortcuts only for types used at ≥ 10 call sites. Shortcuts for
rarely created objects add API noise without payoff.

### SBPP-BEH-04:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* High-frequency value object construction uses a short alias that delegates to the full factory.
*Show:* `Coordinate.at(51.5, -0.1)` appears 200 times in route-planning code; the surrounding
logic stays readable because the construction call is brief.

**U.Episteme (design reasoning):**
*Tell:* A shortcut alias must never bypass validation — it is syntactic sugar, not a different contract.
*Show:* The shortcut delegates to the full factory; both paths enforce the same invariants.

### SBPP-BEH-04:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin value-object creation**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Two public creation paths can cause confusion about which to use in new code | Document in Javadoc that the shortcut is an alias; reference the full method |
| **Arch** | Shortcuts expand the public API surface, complicating future evolution | Mark full factory as primary in documentation; deprecate shortcuts before removing |
| **Onto/Epist** | Short names (`at`, `of`) convey less semantic information | Use only when the type name itself carries all the domain meaning |
| **Prag** | Kotlin named parameters often eliminate the need for shortcuts | Prefer named params for non-pervasive objects; use shortcuts only for truly ubiquitous types |
| **Did** | New developers may create shortcuts prematurely | Apply only after a type is confirmed to be pervasive (many call sites) |

### SBPP-BEH-04:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH04-1** | A Shortcut Constructor Method SHALL delegate to the full Constructor Method, not re-implement creation. | Ensures single source of truth for invariant enforcement |
| **CC-BEH04-2** | Shortcuts SHOULD only be introduced for types that appear at ≥ 10 distinct call sites. | Prevents premature API surface expansion |
| **CC-BEH04-3** | The full-name factory SHALL remain part of the public API alongside the shortcut. | Supports self-documenting code in new call sites |

### SBPP-BEH-04:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Shortcut with divergent validation**
Implementing the shortcut with different (weaker) validation than the full factory.
Fix: The shortcut MUST call the full factory — never duplicate creation logic.

**Anti-pattern 2: Shortcut creep**
Adding shortcuts for every object in the domain, not just pervasive ones.
Fix: Only add a shortcut when you can cite many real call sites that benefit.

### SBPP-BEH-04:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Business logic at call sites is less cluttered | Two API entry points — mitigated by clear documentation |
| Reduces visual noise in heavily used value-object code | Shortcuts can be over-used — enforce the pervasiveness criterion |
| Kotlin's `of` convention aligns with JDK (`List.of`, `Map.of`) | — |

### SBPP-BEH-04:10 - Rationale

Beck introduced this pattern to handle ubiquitous object creation in Smalltalk image code
without drowning business logic in construction noise. Java's `List.of()`, `Map.of()`,
`Optional.of()`, and `Duration.ofHours()` are mainstream incarnations of this pattern in
the JDK itself. Kotlin extends this via companion object conventions and operator overloading.

The critical constraint — that shortcuts must not bypass validation — ensures the pattern
does not introduce inconsistent object creation paths.

### SBPP-BEH-04:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** The JDK adopts this pattern wholesale: `List.of()`,
`Map.of()`, `Set.of()`, `Optional.of()`, `Path.of()` are all shortcut factory methods.
Bloch's Item 1 implicitly endorses them. *Adopt.*

**Kotlin companion object idioms (JetBrains, post-2016):** The `invoke` operator on companion
objects allows `Coordinate(51.5, -0.1)` syntax as the ultimate shortcut. *Adapt: use `invoke`
operator only for truly ubiquitous types.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. — JDK factory conventions | Direct alignment (`List.of`, etc.) | **Adopt** |
| Kotlin companion `invoke` operator (post-2016) | Even terser shortcut syntax | **Adapt** |
| Java 17+ record compact constructors | Simplifies value object creation | **Adopt** |

### SBPP-BEH-04:12 - Relations

* **Specialises:** SBPP-BEH-02 (Constructor Method — shortcut is an alias)
* **Motivated by:** pervasive use of a type across the codebase
* **Constrains:** Must not bypass validation in SBPP-BEH-02
* **Relates to:** SBPP-STA-03 (Explicit Initialization)

### SBPP-BEH-04:End
