## Riel-5.11 - Common Interface Only: Inherit Only If Polymorphic

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"If two or more classes share only a common interface (i.e., messages, not methods), then they should inherit from a common base class only if they will be used polymorphically."*

### Riel-5.11:1 - Problem Frame

Sometimes classes share only an interface (same method signatures) but not implementation. Inheritance is justified only if polymorphic substitution is actually needed.

### Riel-5.11:2 - Problem

Creating a common base class for mere interface similarity, without polymorphic use, adds unnecessary coupling and hierarchy complexity.

### Riel-5.11:3 - Forces

| Force | Tension |
|-------|---------|
| **Polymorphic need** | If clients treat instances interchangeably, a common base is needed vs. if not, it adds coupling. |
| **Interface reuse** | A shared interface type documents commonality vs. an unused inheritance link is noise. |

### Riel-5.11:4 - Solution

Create a common interface or abstract base class only when clients will actually use the classes polymorphically—that is, through a reference to the common type. Without polymorphic use, the interface similarity is coincidental.

### Riel-5.11:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Printer` and a `Logger` may both have `write()`, but unless a client treats them interchangeably, no common base is needed. |
| **U.Episteme** | A `DataImporter` and a `DataExporter` may share `open()`/`close()`, but unless a client uses them polymorphically, no common interface is needed. |

### Riel-5.11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.11.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.11.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.11:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Speculative interface** | A common base is created 'just in case' polymorphism is needed later. | Unnecessary coupling and hierarchy clutter. | Add the common base only when polymorphic use is concrete. |

### Riel-5.11:9 - Consequences

| Benefits |
|----------|
| Inheritance hierarchies exist only for functional polymorphic needs. |

| Trade-off | Mitigation |
|-----------|-----------|
| Missed opportunity | If polymorphism is needed later, the base must be added retroactively; usually a small refactoring. |

### Riel-5.11:10 - Rationale

Inheritance carries semantic weight. Using it without polymorphic justification creates noise in the type system.

### Riel-5.11:11 - SoTA-Echoing

Go's implicit interface satisfaction and Rust's trait system allow polymorphism without inheritance hierarchies, sidestepping this dilemma.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.11:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.11:End
