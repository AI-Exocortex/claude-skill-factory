## Riel-2.7 - Nil or Export Coupling Only

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Classes should only exhibit nil or export coupling with other classes, that is, a class should only use operations in the public interface of another class or have nothing to do with that class."*

### Riel-2.7:1 - Problem Frame

Coupling between classes can range from no coupling (nil) through public interface usage (export) to direct access to internals (content coupling). Stronger coupling forms make systems brittle.

### Riel-2.7:2 - Problem

When a class bypasses another class's public interface to access its internals, both classes become locked together. Any internal change in one forces changes in the other.

### Riel-2.7:3 - Forces

| Force | Tension |
|-------|---------|
| **Coupling strength** | Weaker coupling improves maintainability vs. stronger coupling may seem expedient. |
| **Performance** | Direct field access avoids method overhead vs. the cost is negligible compared to maintenance risk. |
| **Encapsulation** | Respecting interfaces preserves encapsulation vs. bypassing them destroys it. |

### Riel-2.7:4 - Solution

Ensure that every inter-class interaction goes exclusively through the public interface. No class should use friend declarations, reflection hacks, or package-private access to manipulate another class's internals. If the public interface is insufficient, extend it properly rather than circumventing it.

### Riel-2.7:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `PaymentProcessor` interacts with a `BankAccount` only through `debit()` and `credit()`, never by directly modifying the account's balance field. |
| **U.Episteme** | An `ExperimentRunner` interacts with a `Model` only through `train()` and `evaluate()`, never by directly tweaking internal weight matrices. |

### Riel-2.7:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.7:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.7.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.7.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.7:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Friend abuse** | Using language-level friend/internal access to bypass interfaces. | Couples classes at the implementation level. | Redesign the interface to expose what is genuinely needed. |
| **Reflection hacking** | Using reflection to access private fields from outside. | Defeats encapsulation entirely. | Treat reflection as a diagnostic tool, not a design technique. |

### Riel-2.7:9 - Consequences

| Benefits |
|----------|
| Classes can evolve their internals independently. |
| The dependency graph reflects true architectural relationships. |

| Trade-off | Mitigation |
|-----------|-----------|
| Interface enrichment | May require adding methods to public interfaces; mitigated by thoughtful API design. |

### Riel-2.7:10 - Rationale

Export coupling is the maximum acceptable coupling in a well-designed OO system. Anything stronger breaks the encapsulation contract and negates the benefits of object orientation.

### Riel-2.7:11 - SoTA-Echoing

Coupling metrics (Chidamber & Kemerer, 1994) formalize coupling strength. Modern linters and architecture fitness functions flag violations. The 'Connascence' framework (Page-Jones, 1996; Parsons, 2020s revival) provides a finer-grained coupling taxonomy.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.7:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.7:End
