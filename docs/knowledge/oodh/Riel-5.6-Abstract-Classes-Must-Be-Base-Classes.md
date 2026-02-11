## Riel-5.6 - Abstract Classes Must Be Base Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"All abstract classes must be base classes."*

### Riel-5.6:1 - Problem Frame

An abstract class cannot instantiate itself. It exists to be inherited and to define a contract for its descendants.

### Riel-5.6:2 - Problem

An abstract class that is not used as a base class (has no derived classes) is dead code—it defines a contract no one fulfills.

### Riel-5.6:3 - Forces

| Force | Tension |
|-------|---------|
| **Purposefulness** | Every abstract class should have at least one concrete descendant vs. premature abstraction may precede concrete needs. |

### Riel-5.6:4 - Solution

Ensure every abstract class has at least one concrete derived class that fulfills its contract. If an abstract class has no descendants, either make it concrete or remove it.

### Riel-5.6:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | An abstract `Shape` class must have concrete descendants like `Circle`, `Rectangle`. An abstract class with no subclasses serves no purpose. |
| **U.Episteme** | An abstract `ExperimentalDesign` must have concrete implementations like `RandomizedControlTrial`, `CohortStudy`. |

### Riel-5.6:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.6:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.6.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.6.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.6:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Orphaned abstraction** | An abstract class with zero derived classes. | Dead code that confuses the design. | Add concrete descendants or remove the abstraction. |

### Riel-5.6:9 - Consequences

| Benefits |
|----------|
| Every abstraction is grounded in at least one concrete implementation. |

| Trade-off | Mitigation |
|-----------|-----------|
| Premature judgment | An abstract class may await future subclasses; use sparingly and document intent. |

### Riel-5.6:10 - Rationale

An abstract class is a promise. A promise with no fulfillment is a lie in the codebase.

### Riel-5.6:11 - SoTA-Echoing

Static analysis tools flag abstract classes with no subclasses. Modern languages provide interface types for pure contracts and abstract classes for partial implementations.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.6:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.6:End
