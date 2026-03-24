## SBPP-BEH-22 - Super

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-BEH-22:1 - Problem frame

In Java/Kotlin class hierarchies, a subclass often needs to call a superclass method —
to initialise inherited state, extend superclass behaviour, or participate in a Template
Method. The `super` keyword invokes superclass logic, but over-use of `super` creates
tight coupling between superclass implementation and subclass code.

### SBPP-BEH-22:2 - Problem

How do you invoke superclass behaviour when a subclass needs to build on or extend what
the superclass provides, without coupling the subclass to the superclass's implementation details?

### SBPP-BEH-22:3 - Forces

| Force | Tension |
|-------|---------|
| **Code Reuse** | `super` avoids duplicating superclass logic ↔ creates coupling to superclass implementation |
| **Liskov Substitution** | Subclasses should be substitutable ↔ `super` calls can break LSP if used incorrectly |
| **Inheritance Depth** | Deep hierarchies rely heavily on `super` chains ↔ composition avoids this |

### SBPP-BEH-22:4 - Solution — Use `super` sparingly; prefer composition for code reuse

Use `super` only in two justified scenarios:
1. **Extending Super** (BEH-23): calling super to run the superclass logic, then adding your own.
2. **Constructors**: `super()` in constructors is idiomatic and unavoidable.

Avoid `super` for arbitrary superclass method calls in non-constructor, non-extending contexts.
When in doubt, prefer composition over inheritance.

**Java example — justified super use:**

```java
public class AuditedRepository extends BaseRepository {
    @Override
    public void save(Entity entity) {
        super.save(entity);  // ✅ Extending Super: super runs first, then audit
        auditLog.record(entity.getId(), "SAVED");
    }

    // ✅ Constructor super is always appropriate
    public AuditedRepository(DataSource ds, AuditLog log) {
        super(ds);
        this.auditLog = log;
    }
}
```

**Java example — prefer composition over super:**

```java
// ❌ Deep super chain
class A { void init() { /* set up A */ } }
class B extends A { @Override void init() { super.init(); /* B setup */ } }
class C extends B { @Override void init() { super.init(); /* C setup */ } }

// ✅ Composition — no super dependency chain
class Repository {
    private final ConnectionManager connections;
    private final AuditLog audit;
    private final Cache cache;
    // all assembled via constructor injection — no super chain
}
```

**Kotlin:**

```kotlin
open class BaseRepository(protected val ds: DataSource) {
    open fun save(entity: Entity) { /* persist */ }
}

class AuditedRepository(ds: DataSource, private val auditLog: AuditLog)
    : BaseRepository(ds) {
    override fun save(entity: Entity) {
        super.save(entity)           // call superclass logic
        auditLog.record(entity.id)  // then extend
    }
}
```

### SBPP-BEH-22:5 - Archetypal Grounding

**U.System:** `super.save(entity)` in `AuditedRepository` calls the persistence logic already in `BaseRepository`.
**U.Episteme:** Every `super` call is a dependency on the superclass's current implementation — document this coupling explicitly.

### SBPP-BEH-22:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Java/Kotlin inheritance and super calls**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Deep `super` chains are opaque in code review | Limit inheritance depth to 2-3 levels; prefer composition |
| **Arch** | `super` creates a white-box dependency on superclass implementation | Document `super` calls in method Javadoc; consider `final` superclass methods |
| **Onto/Epist** | Superclass behaviour is assumed to be stable; any change breaks subclasses | Design superclasses for extension (hooks); avoid changing methods with `super` callers |
| **Prag** | Kotlin `open` is opt-in; classes are `final` by default — encourages composition | Use Kotlin's default-final as a guide: inheritance requires conscious design |
| **Did** | New developers over-use inheritance; prefer composition training | "Favour composition over inheritance" — GoF, Bloch |

### SBPP-BEH-22:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH22-1** | `super` method calls (outside constructors) SHALL only appear in override methods that extend or modify superclass behaviour. | Prevents arbitrary coupling to superclass internals |
| **CC-BEH22-2** | Inheritance hierarchies SHOULD be limited to 2 levels of concrete classes. | Controls coupling depth |
| **CC-BEH22-3** | Kotlin classes SHOULD be `final` by default; mark `open` only when extension is explicitly designed. | Enforces deliberate inheritance design |

### SBPP-BEH-22:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Deep super chains**
`C.init()` calls `B.init()` which calls `A.init()`. Change in A breaks C.
Fix: Use composition; assemble behaviour via constructor injection.

**Anti-pattern 2: Calling super outside override**
`super.helperMethod()` called in a non-override method to access superclass utility.
Fix: Extract the utility to a shared helper or use composition.

### SBPP-BEH-22:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Reuses superclass logic without duplication | Creates coupling — mitigated by shallow hierarchies |
| Enables Template Method pattern | Fragile base class problem — design superclasses carefully |
| Constructor `super` is unavoidable and idiomatic | — |

### SBPP-BEH-22:10 - Rationale

Beck treats `super` as a sharp tool requiring discipline. Java/Kotlin reinforce this:
Kotlin's default `final` classes and `open` opt-in directly encode the advice "design for
extension or prohibit it" (Effective Java Item 19). Reserve `super` for deliberate
Extending Super (BEH-23) and constructor delegation.

### SBPP-BEH-22:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 19 ("Design and document for inheritance or
else prohibit it"). Java `super` requires the superclass to be explicitly designed for extension. *Adopt.*

**Kotlin language design (JetBrains, post-2016):** Default `final` classes; `open` required
for inheritance. Forces deliberate design. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Item 19 — design for extension | **Adopt** |
| Kotlin default-final (post-2016) | Deliberate inheritance | **Adopt** |
| GoF "Favour composition over inheritance" (widely applied post-2015) | Prefer composition | **Adopt** |

### SBPP-BEH-22:12 - Relations

* **Enables:** SBPP-BEH-23 (Extending Super), SBPP-BEH-24 (Modifying Super)
* **Alternatives:** SBPP-BEH-25 (Delegation — prefer when composition suffices)
* **Constrained by:** Effective Java Item 19 — must be designed for

### SBPP-BEH-22:End
