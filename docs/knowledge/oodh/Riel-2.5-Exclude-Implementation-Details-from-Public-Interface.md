## Riel-2.5 - Exclude Implementation Details from Public Interface

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Do not put implementation details such as common-code private functions into the public interface of a class."*

### Riel-2.5:1 - Problem Frame

During implementation, helper functions often emerge that factor out common code. If these are placed in the public interface, users become coupled to implementation artifacts.

### Riel-2.5:2 - Problem

Exposing implementation helpers publicly inflates the protocol, confuses users about the class's purpose, and prevents the implementor from freely refactoring internal code.

### Riel-2.5:3 - Forces

| Force | Tension |
|-------|---------|
| **Interface clarity** | Public interface should reflect the abstraction vs. convenience of making helpers accessible. |
| **Refactoring freedom** | Private helpers can be changed freely vs. public helpers become frozen contracts. |

### Riel-2.5:4 - Solution

Keep all implementation-detail functions private. The public interface should contain only methods that represent the abstraction's essential behavior as seen by its users.

### Riel-2.5:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Printer` class has a private `formatHeader()` helper used by several public print methods. This helper is an implementation detail and must not appear in the public interface. |
| **U.Episteme** | A `DataCleaner` class uses an internal `normalizeWhitespace()` utility. Exposing it publicly would bind users to a particular cleaning strategy that may change. |

### Riel-2.5:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.5:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.5.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.5.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.5:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Accidental publicity** | A helper method is made public 'just in case someone needs it.' | It becomes a permanent contract. | Default to private; promote to public only when a genuine use case demands it. |

### Riel-2.5:9 - Consequences

| Benefits |
|----------|
| The public interface remains focused and stable. |
| Internal refactoring is unconstrained. |

| Trade-off | Mitigation |
|-----------|-----------|
| Reduced flexibility for power users | Some users may want access to helpers; mitigated by providing a well-designed public API that covers real needs. |

### Riel-2.5:10 - Rationale

The public interface is a contract. Implementation details placed in a contract become liabilities, not assets. Keeping them private preserves the class's ability to evolve.

### Riel-2.5:11 - SoTA-Echoing

Effective Java (Bloch, 2018) advises minimizing accessibility. Modern languages provide module-private (Rust `pub(crate)`, Kotlin `internal`, Swift `internal`) to give nuanced control.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.5:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.5:End
