## SBPP-CLS-02 - Qualified Subclass Name

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-CLS-02:1 - Problem frame

When a superclass hierarchy is established with a Simple Superclass Name (CLS-01), new
subclasses need names that communicate two things simultaneously: what they share with
the parent (how they are the same) and what distinguishes them (how they are different).
A name that fails to communicate both pieces forces readers to open the class to understand
its relationship to its parent.

### SBPP-CLS-02:2 - Problem

What do you name a subclass in a hierarchy so that readers immediately understand
how it relates to its superclass and what distinguishes it, without reading the class body?

### SBPP-CLS-02:3 - Forces

| Force | Tension |
|-------|---------|
| **Similarity communication** | Must signal "this is a kind of X" ↔ not every subclass should use the parent name |
| **Distinction communication** | Must signal "this is X but with quality Y" ↔ qualifier must be precise, not generic |
| **Name length** | Including the parent name makes names longer ↔ conciseness aids readability |
| **Implementation vs role** | Sometimes inheritance is for implementation only, not role similarity ↔ the name should reflect role, not inheritance structure |

### SBPP-CLS-02:4 - Solution — Prepend an adjective to the superclass name; drop the parent name when the subclass has a unique well-known identity

Name a subclass by prepending a **distinctive adjective or noun** to the superclass name
when the "is-a-kind-of" relationship is part of the domain model. Skip the parent name
when the subclass has a unique name that is already well-understood on its own.

**Java examples — Qualified Subclass Names:**

```java
// ✅ Adjective + Superclass pattern — clear hierarchy membership
public abstract class Adjustment { }
public final class PercentageAdjustment extends Adjustment { }    // Percentage + Adjustment
public final class FlatRateAdjustment   extends Adjustment { }    // FlatRate + Adjustment
public final class CapAdjustment        extends Adjustment { }    // Cap + Adjustment

// ✅ Another hierarchy
public interface Repository<T, ID> { }
public interface PolicyRepository extends Repository<Policy, PolicyId> { }   // Policy + Repository
public interface ClaimRepository  extends Repository<Claim, ClaimId>   { }   // Claim + Repository

// ✅ Qualifier communicates the key difference
public abstract class RiskScorer { }
public class AgeBasedRiskScorer       extends RiskScorer { }   // AgeBase + RiskScorer
public class ClaimHistoryRiskScorer   extends RiskScorer { }   // ClaimHistory + RiskScorer
public class MLRiskScorer             extends RiskScorer { }   // ML (domain term) + RiskScorer
```

**Kotlin sealed class hierarchy (idiomatic qualified subclass names):**

```kotlin
// ✅ Sealed hierarchy — subclasses are Qualified Subclass Names
sealed class PremiumAdjustment {
    data class PercentageDiscount(val pct: Double)    : PremiumAdjustment()
    data class FlatSurcharge(val amount: Money)       : PremiumAdjustment()
    data class AgeBanding(val band: AgeRange, val factor: Double) : PremiumAdjustment()
    object NoAdjustment                               : PremiumAdjustment()
}

// ✅ Interface hierarchy
interface EventHandler<E>
class PolicyCreatedHandler  : EventHandler<PolicyCreatedEvent>
class ClaimFiledHandler     : EventHandler<ClaimFiledEvent>
class PaymentReceivedHandler: EventHandler<PaymentReceivedEvent>
```

**When to use unique name instead of qualified name:**

```java
// ✅ Well-known name beats qualified name
// Array IS a Collection, but "Array" is universally understood; "ArrayCollection" is not
// String IS a CharSequence but "String" is universally understood; "StringCharSequence" is not
// LinkedList IS a List but "LinkedList" is well-known; "LinkedArrayList" would be wrong

// In domain terms:
// "Invoice" may extend "Document" but "Invoice" is universally understood in billing
// "Mortgage" may extend "Loan" but "Mortgage" is a well-known domain concept

// Rule: if the subclass name is well-known in the domain WITHOUT the parent name,
// use the simple name. If it is not well-known, use Qualified Subclass Name.
```

**The qualification decision tree:**

```
Creating a subclass of SuperclassX?
  ├── Is "SubclassX" already a well-known domain concept? (like "SortedCollection")
  │     └── YES → Use Qualified Subclass Name (adjective + superclass)
  │                Example: SortedCollection is Sorted + Collection
  │
  ├── Is the subclass relationship purely for code sharing, not role similarity?
  │     └── YES → Use Simple Superclass Name for the subclass (its own concept)
  │                Example: String IS-A CharSequence but "String" is the concept
  │
  └── Default: prepend a distinctive adjective → AdjX
               Example: PercentageAdjustment, FlatRateAdjustment
```

### SBPP-CLS-02:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Every subclass name communicates both its parent concept and its distinguishing characteristic.
*Show:* `PercentageAdjustment` tells a reader: this is an `Adjustment` (shares the role)
that applies as a `Percentage` (the distinguishing feature). No need to open the class.

**U.Episteme (design reasoning):**
*Tell:* The qualified name encodes the "same + different" relationship that defines subclassing.
*Show:* A code reviewer reading `AgeBasedRiskScorer` and `ClaimHistoryRiskScorer` immediately
understands the shape of the `RiskScorer` hierarchy — without reading any class body.

### SBPP-CLS-02:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Subclass naming in Java/Kotlin hierarchies**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Long compound names (`ClaimHistoryBasedPremiumAdjustmentCalculatorService`) become unworkable | Apply the "adjective + superclass" pattern; refactor if the name exceeds ~4 words |
| **Arch** | Qualified names encode hierarchy in the name — if the hierarchy changes, names may need updating | Accept this as a property of named hierarchies; refactor names when hierarchy changes |
| **Onto/Epist** | The qualifier must be the *role* distinguisher, not the implementation detail | `CachedPolicyRepository` encodes an implementation concern; `InMemoryPolicyRepository` may be acceptable in tests |
| **Prag** | Kotlin sealed classes make the hierarchy explicit structurally — the name is reinforced by nesting | Use both: nest sealed subclasses AND qualify their names |
| **Did** | New developers may name subclasses purely by function: `PremiumCalculatorV2` instead of `MLPremiumCalculator` | Teach: the qualifier should express the conceptual difference, not a version or iteration |

### SBPP-CLS-02:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-CLS02-1** | Subclass names SHALL include the superclass concept name when the "is-a-kind-of" relationship is domain-meaningful and the subclass is not universally well-known on its own. | Self-documenting hierarchy membership |
| **CC-CLS02-2** | The qualifying adjective SHALL describe the role distinction, not the implementation mechanism. | Domain fidelity |
| **CC-CLS02-3** | Qualified names SHOULD be ≤ 4 words (e.g., `ClaimHistoryRiskScorer`). Names longer than 4 words indicate the class has too many responsibilities. | Controls cognitive load |
| **CC-CLS02-4** | Well-known domain terms (e.g., `Invoice`, `Mortgage`, `SavingsAccount`) MAY use Simple Superclass Names even when they are technically subclasses. | Respects established domain vocabulary |

### SBPP-CLS-02:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Version-qualified names**
`PolicyCalculatorV2`, `NewClaimProcessor`, `UpdatedRiskScorer`.
Version numbers in names encode iteration history, not domain concepts.
Fix: name after the distinguishing concept — `MLPolicyCalculator`, `StreamingClaimProcessor`,
`RegionAwareRiskScorer`.

**Anti-pattern 2: Over-qualification (including implementation details)**
`HashMapBackedPolicyIndex`, `JdbcPostgresClaimRepository`.
Fix: `PolicyIndex`, `ClaimRepository`. Infrastructure details belong in the package or
configuration, not the class name. Exception: in test code, `InMemoryPolicyRepository`
is acceptable since the implementation choice is the relevant distinguishing fact.

**Anti-pattern 3: Dropping the parent name when the subclass is ambiguous**
A hierarchy of `Adjuster`, `ValueAdjuster`, `RateAdjuster` where only `Adjuster` is clear.
Fix: if readers cannot infer the parent concept from the subclass name alone, apply
Qualified Subclass Name: `ValueAdjustment`, `RateAdjustment`.

**Anti-pattern 4: Inconsistent qualification depth**
Some subclasses use `AdjX` (two-word names) while others use `ConceptAdjX` (three-word).
Fix: apply the "adjective + superclass" pattern consistently across the whole hierarchy.

### SBPP-CLS-02:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Hierarchy membership visible in the name — no class body needed | Longer names — mitigated by the 4-word guideline |
| Adding new variants is self-explanatory: new adjective + superclass | Names encode hierarchy; if hierarchy restructures, names need review |
| Sealed class hierarchies in Kotlin make the structure double-visible (nesting + name) | — |
| Code reviews can verify correct classification by reading names | — |

### SBPP-CLS-02:10 - Rationale

Beck observes that the two pieces of information a subclass name must convey are
"how it is the same" and "how it is different." The qualified name pattern (`Adjective + Superclass`)
encodes both in one compound. `SortedCollection` says: "a Collection (same) that is Sorted
(different)." `PercentageAdjustment` says: "an Adjustment (same) applied as a Percentage (different)."

The exception — unique well-known names like `Array`, `String`, `Invoice` — honours the
principle that established domain vocabulary takes precedence over structural naming conventions.

In Java/Kotlin's sealed class system, Qualified Subclass Names are amplified by the
structural nesting: `PremiumAdjustment.PercentageDiscount` is both textually and
syntactically a qualified subclass — the dot notation reinforces the "is-a-kind-of" relationship.

### SBPP-CLS-02:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Domain-Driven Design — Ubiquitous Language (Evans 2003; Vernon 2016):** DDD reinforces
that subtype names must be validated against the domain's own vocabulary. A hierarchy of
`PremiumAdjustment` subtypes must match what actuaries and underwriters call these
adjustments — `PercentageDiscount` and `FlatSurcharge` come from the domain glossary,
not from a naming convention. The qualified pattern provides the structure; the domain
provides the vocabulary. *Adopt.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 68 observes that class names should be noun
phrases. For hierarchies, qualified nouns communicate role and type simultaneously — a
principle consistent with Bloch's own JDK designs (`LinkedList`, `TreeMap`, `HashSet`,
`LinkedHashMap`). *Adopt.*

**Refactoring 2nd ed. — "Rename Class" (Fowler, 2018):** Fowler's motivation for renaming
includes exactly this pattern: when a class name does not communicate its place in a hierarchy,
rename it to include the superclass context. *Adopt.*

**Kotlin Sealed Classes guidance (JetBrains, post-2016):** The Kotlin documentation examples
for sealed classes consistently use qualified subclass names (`Success`, `Failure`, `Loading`
as subtypes of `Result` — these are qualified by context even when the parent name is dropped
in short hierarchies). *Adopt with adaptation: use full qualified names for domain hierarchies;
short names are acceptable for technical sealed types like `Result`.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| DDD Ubiquitous Language (Vernon, 2016) | Domain-validated qualified names | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | JDK naming patterns (LinkedList, TreeMap) | **Adopt** |
| Refactoring 2nd ed. "Rename Class" (Fowler, 2018) | Hierarchy-communicating names | **Adopt** |
| Kotlin sealed class guidance (JetBrains, post-2016) | Structural + textual qualification | **Adopt** |

### SBPP-CLS-02:12 - Relations

* **Requires:** SBPP-CLS-01 (Simple Superclass Name — the root name being qualified)
* **Implements:** DDD Ubiquitous Language at the subtype level
* **Constrained by:** 4-word guideline — long names signal too many responsibilities
* **Relates to:** SBPP-BEH-15 (Choosing Message — the hierarchy that gets Choosing Message also needs Qualified Subclass Names)
* **Relates to:** SBPP-BEH-19 (Dispatched Interpretation — hierarchies with dispatched interpretation need clear qualified names)

### SBPP-CLS-02:End
