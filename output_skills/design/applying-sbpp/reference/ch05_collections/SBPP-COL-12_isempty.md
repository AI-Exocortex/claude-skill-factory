## SBPP-COL-12 - IsEmpty

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-12:1 - Problem frame

Testing whether a collection is empty is a ubiquitous operation. Developers frequently
write `size() == 0` or `size() > 0` instead of the semantically precise `isEmpty()` /
`isNotEmpty()`. The size comparison exposes implementation detail and reads less naturally.

### SBPP-COL-12:2 - Problem

How do you test whether a collection is empty in a way that communicates intent clearly
and works correctly for all collection types?

### SBPP-COL-12:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | `isEmpty()` names the concept ↔ `size() == 0` reveals the implementation |
| **Performance** | `isEmpty()` may be O(1) where `size()` is O(n) for some types | LinkedList prior to Java 6 |
| **Null safety** | Must handle null collections safely | |

### SBPP-COL-12:4 - Solution — Always use `isEmpty()` / `isNotEmpty()`; never `size() == 0`

**Java:**

```java
// ❌ Anti-pattern
if (policies.size() == 0) { ... }
if (policies.size() > 0) { ... }

// ✅ Always use isEmpty()
if (policies.isEmpty()) { throw new IllegalArgumentException("No policies provided"); }
if (!policies.isEmpty()) { processPolicies(policies); }

// ✅ Null-safe check
if (policies == null || policies.isEmpty()) { return Collections.emptyList(); }

// ✅ Stream isEmpty check
boolean hasResults = stream.findFirst().isPresent();
```

**Kotlin:**

```kotlin
// ✅ Kotlin provides isNotEmpty() directly
if (policies.isEmpty()) throw IllegalArgumentException("No policies provided")
if (policies.isNotEmpty()) processPolicies(policies)

// ✅ Even more idiomatic
policies.ifEmpty { return emptyList() }

// ✅ Null-safe
if (policies.isNullOrEmpty()) return emptyList()
```

### SBPP-COL-12:5 - Archetypal Grounding

**U.System:** `if (claims.isEmpty()) return Optional.empty()` — the intent is "no claims", not "size equals zero".
**U.Episteme:** For `LinkedList` and lazy streams, `isEmpty()` can be O(1) while `size()` is O(n). Using `isEmpty()` is correct regardless of implementation.

### SBPP-COL-12:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Collection emptiness testing**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Static analysis (PMD, SonarQube) flags `size() == 0` — enable these rules | Enable collection-usage linting |
| **Arch** | `isEmpty()` is O(1) for all standard JDK collections since Java 6 | No architecture concern |
| **Onto/Epist** | `size() == 0` is technically correct but semantically imprecise | Use `isEmpty()` as the canonical test |
| **Prag** | Kotlin adds `isNullOrEmpty()` for null-safe emptiness check | Use this in Kotlin when null is possible |
| **Did** | Simplest pattern in the collection — use it to introduce the broader principle "use the right API" | |

### SBPP-COL-12:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL12-1** | Collection emptiness SHALL be tested with `isEmpty()` / `isNotEmpty()`, never `size() == 0`. | Expressive and potentially more efficient |
| **CC-COL12-2** | Null-and-empty checks in Kotlin SHOULD use `isNullOrEmpty()`. | Null-safe idiom |

### SBPP-COL-12:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `list.size() == 0` — Fix: `list.isEmpty()`.
**Anti-pattern 2:** `list.size() != 0` — Fix: `!list.isEmpty()` (Java) / `list.isNotEmpty()` (Kotlin).

### SBPP-COL-12:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Reads as prose; reveals intent | None — strictly better |
| Potentially O(1) vs O(n) for some types | — |

### SBPP-COL-12:10 - Rationale

Beck's simplest collection protocol pattern. The principle "use the highest-level API that
expresses the concept" applies universally. `isEmpty()` is the canonical emptiness test in Java/Kotlin.

### SBPP-COL-12:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**SonarQube rule S1155 (post-2015):** Flags `size() == 0` usage; recommends `isEmpty()`. *Adopt.*
**Clean Code (Martin, ongoing):** Use intention-revealing names in all contexts, including API calls. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| SonarQube S1155 (post-2015) | Automated enforcement | **Adopt** |
| Kotlin `isNullOrEmpty()` (post-2016) | Null-safe idiom | **Adopt** |

### SBPP-COL-12:12 - Relations

* **Part of:** Collection Protocol patterns (COL-12 through COL-20)
* **Paired with:** SBPP-COL-13 (Includes: — membership test)

### SBPP-COL-12:End
