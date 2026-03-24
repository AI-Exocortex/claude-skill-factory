## SBPP-CLS-01 - Simple Superclass Name

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-CLS-01:1 - Problem frame

Every class in a Java/Kotlin codebase needs a name. Classes that are meant to be
extended — root types in domain hierarchies, abstract base services, shared protocol
interfaces — need names that are simple, stable, and meaningful in isolation without
reference to any particular subclass. A poorly named root type forces all its subclasses
to carry the cognitive burden of explaining the hierarchy.

### SBPP-CLS-01:2 - Problem

What do you name a class that is the root of a hierarchy, where the name must
communicate the essential concept cleanly — standing on its own without requiring
the reader to know any of its subclasses?

### SBPP-CLS-01:3 - Forces

| Force | Tension |
|-------|---------|
| **Abstraction** | Root name must capture the essential concept ↔ too abstract and it becomes meaningless |
| **Stability** | Root names are used everywhere; changing them is costly ↔ a poor early name compounds |
| **Discoverability** | Short names are easy to remember ↔ may conflict with common vocabulary |
| **Domain fidelity** | Name must match the domain model's vocabulary ↔ technical names can pollute domain language |

### SBPP-CLS-01:4 - Solution — Use a single, simple noun that names the concept; avoid prefixes, suffixes, and implementation hints

Name the root or abstract class with the **simplest noun** that a domain expert would
recognise as the concept itself. The name should work without a qualifier — if you need
a qualifier to understand the type, it is a Qualified Subclass Name (CLS-02).

**Good Java examples — Simple Superclass Names:**

```java
// ✅ Single noun, domain-precise, no technical suffix
public abstract class Policy { }          // not: PolicyBase, AbstractPolicy, IPolicy
public abstract class Claim { }           // not: ClaimEntity, ClaimModel
public interface Calculator { }           // not: ICalculator, BaseCalculator
public abstract class RiskFactor { }      // not: AbstractRiskFactor
public abstract class Adjustment { }      // not: AdjustmentBase

// ✅ Interface as root — also a Simple Superclass Name
public interface Payment { }              // not: IPayment, PaymentInterface
public interface Repository<T, ID> { }   // not: BaseRepository, IRepository

// ✅ From the JDK — classic Simple Superclass Names
// Number, Collection, Map, List, Set, Comparable, Iterable, Runnable
```

**Kotlin examples:**

```kotlin
// ✅ Sealed class hierarchy root — single concept name
sealed class PremiumAdjustment            // not: AbstractPremiumAdjustment
data class DiscountAdjustment(val pct: Double) : PremiumAdjustment()
data class SurchargeAdjustment(val flat: Money) : PremiumAdjustment()

// ✅ Abstract root — no suffix
abstract class RiskScorer                 // not: RiskScorerBase
abstract class PolicyValidator            // acceptable: the compound noun is the concept

// ✅ Interface root
interface EventHandler<E>                 // not: IEventHandler
interface PremiumRepository               // not: PremiumRepositoryInterface
```

**Naming decision tree:**

```
Is this a root/abstract type?
  └─ YES → Is one noun sufficient to name the concept?
             └─ YES → Simple Superclass Name (this pattern)
             └─ NO  → Consider: is this really a variant of something? → Qualified Subclass Name
  └─ NO  → It is a concrete type → Simple Superclass Name still applies for unique names
                                   OR Qualified Subclass Name if it is "Adjective + Superclass"
```

**Anti-patterns to refuse:**

```java
// ❌ Hungarian-style prefixes/suffixes on abstractions
abstract class AbstractPolicy { }      // redundant — caller knows it's abstract
interface ICalculator { }              // "I" prefix is a .NET convention; not Java/Kotlin
class PolicyBase { }                   // "Base" suffix adds nothing

// ❌ Technical noise in names
class PolicyEntity { }                 // "Entity" is JPA noise; domain says "Policy"
class ClaimModel { }                   // "Model" is framework noise; domain says "Claim"
class PaymentDTO { }                   // "DTO" belongs in the package/layer, not the name
```

### SBPP-CLS-01:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Abstract root types are named with the single domain noun they represent.
*Show:* In an insurance platform, `Policy`, `Claim`, `Coverage`, `RiskFactor`, and `Adjustment`
are the root names. `AbstractPolicy` or `PolicyBase` would be rejected at code review — the
prefix adds no information because the abstract modifier already communicates abstractness.

**U.Episteme (design reasoning):**
*Tell:* A Simple Superclass Name is stable because it encodes only the concept, not the
implementation structure.
*Show:* When the hierarchy evolves from a class hierarchy to a sealed interface hierarchy,
`Policy` remains the right name; `AbstractPolicy` would need renaming.

### SBPP-CLS-01:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin class and interface naming**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Short names can clash with JDK types (`List`, `Map`, `String`) | Use domain package for disambiguation; avoid shadowing JDK types |
| **Arch** | `AbstractX` is a well-known Spring/JPA convention that many teams follow | Where framework convention uses `Abstract` prefix, apply consistently; never mix |
| **Onto/Epist** | "Simple" does not mean "vague" — `Policy` is precise in an insurance context | Validate with domain experts; domain vocabulary is the arbiter |
| **Prag** | Java's `Abstract` prefix is widespread in framework code (Spring, JPA) | Confine `Abstract` to framework/infrastructure layer; keep domain layer names clean |
| **Did** | New developers copy framework naming (`IService`, `AbstractBase`) into domain code | Code review: reject `Abstract`, `I`, `Base`, `Model`, `Entity` in domain class names |

### SBPP-CLS-01:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-CLS01-1** | Root and abstract domain classes SHALL be named with a single domain noun, without `Abstract`, `Base`, `I`, or `Model` prefixes/suffixes. | Domain clarity and Ubiquitous Language |
| **CC-CLS01-2** | Interface names SHALL NOT use the `I` prefix (Java convention is no prefix; Kotlin follows the same). | Language convention |
| **CC-CLS01-3** | Names SHOULD be validated against the domain expert's vocabulary — if a domain expert would not use the name, it needs revision. | Ubiquitous Language enforcement |
| **CC-CLS01-4** | Names MUST NOT shadow JDK type names without strong justification. | Prevents confusion |

### SBPP-CLS-01:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Abstract/Base/I prefix pollution**
`AbstractPolicyCalculator`, `BasePremiumService`, `IClaimRepository`.
These names encode implementation structure, not concepts. Fix: `PolicyCalculator`,
`PremiumService`, `ClaimRepository`. The modifier (`abstract`, `interface`) lives in the
language keyword, not the name.

**Anti-pattern 2: Layer suffix leakage into domain names**
`PolicyEntity`, `ClaimDTO`, `RiskModel`, `PaymentServiceBean`. These embed infrastructure
concerns into domain names. Fix: use layer packages to provide context:
`com.insurance.domain.Policy`, `com.insurance.api.PolicyDto`.
The name `PolicyDto` is acceptable *only* in the API layer; the domain layer uses `Policy`.

**Anti-pattern 3: Overly general names**
`Manager`, `Handler`, `Processor`, `Helper`, `Util` as class names. These communicate
nothing about the concept. Fix: name after the specific responsibility:
`PremiumCalculationService` (not `PremiumManager`), `ClaimFileUploadHandler` (not `Handler`).

### SBPP-CLS-01:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Names match Ubiquitous Language — domain experts can read the code | Short names may clash with foreign packages — use fully qualified names or import aliases |
| Root names are stable across structural refactors (class → sealed → interface) | Initial investment in naming discussions with domain experts |
| Subclass names become self-describing with Qualified Subclass Name (CLS-02) | — |
| Code reviews and onboarding focus on concepts, not structural suffixes | — |

### SBPP-CLS-01:10 - Rationale

Beck's Simple Superclass Name is the foundation of the Domain-Driven Design principle
of Ubiquitous Language applied to class naming. A name like `AbstractPolicyCalculatorBase`
communicates technical structure but not domain meaning. A name like `PolicyCalculator`
communicates the domain role directly.

Java/Kotlin have no need for the `I` prefix (unlike early COM/Windows conventions).
The `Abstract` prefix became common in Spring and JPA infrastructure but should be
confined to framework layer code. Domain model classes carry their entire meaning
in their noun — no qualifier needed.

The longevity argument is compelling: `Policy` as a root name survives the evolution from
`abstract class Policy` to `sealed interface Policy` to `interface Policy` — the domain
concept is stable even when the implementation structure changes. `AbstractPolicy`
would require renaming with each structural evolution.

### SBPP-CLS-01:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Domain-Driven Design — Ubiquitous Language (Evans 2003; Vernon 2016):** Class names must
come from and reinforce the domain's shared vocabulary. A domain expert who hears
`AbstractPolicyBase` has learned nothing about the domain. The Ubiquitous Language
principle requires that code vocabulary matches domain vocabulary. *Adopt directly.*

**Effective Java 3rd ed. (Bloch, 2018):** Item 68 ("Adhere to generally accepted naming
conventions") notes that type parameter names are single letters for generics, but class
names should be descriptive nouns or noun phrases. Bloch's own JDK designs (Collections
API: `List`, `Set`, `Map`, `Collection`) are textbook Simple Superclass Names. *Adopt.*

**Google Java Style Guide (Google, continuously updated post-2015):** Class names use
`UpperCamelCase`; no I-prefix for interfaces; no "Abstract" requirement. *Adopt.*

**Kotlin Coding Conventions (JetBrains, post-2016):** Same: no I-prefix, no Abstract-prefix.
Sealed class roots are named as domain nouns. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| DDD Ubiquitous Language (Vernon, 2016) | Domain vocabulary mandate | **Adopt** |
| Effective Java 3rd ed. (Bloch, 2018) | JDK naming conventions | **Adopt** |
| Google Java Style Guide (post-2015) | No I-prefix or Abstract mandate | **Adopt** |
| Kotlin Coding Conventions (JetBrains, post-2016) | Same conventions as Java | **Adopt** |

### SBPP-CLS-01:12 - Relations

* **Enables:** SBPP-CLS-02 (Qualified Subclass Name — subclasses build on the root name)
* **Implements:** DDD Ubiquitous Language principle
* **Constrains:** All class and interface naming in the domain layer
* **Constrained by:** Domain vocabulary — names must be validated with domain experts

### SBPP-CLS-01:End
