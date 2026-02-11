## Riel-5.18 - Do Not Confuse Optional Containment with Inheritance

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Do not confuse optional containment with the need for inheritance. Modeling optional containment with inheritance will lead to a proliferation of classes."*

### Riel-5.18:1 - Problem Frame

When an object may or may not have a component, designers sometimes model the with/without cases as separate subclasses.

### Riel-5.18:2 - Problem

Using inheritance to represent optional components creates a combinatorial explosion of subclasses: one for each combination of present/absent components.

### Riel-5.18:3 - Forces

| Force | Tension |
|-------|---------|
| **Combinatorial explosion** | N optional components yield 2^N subclasses vs. containment handles optionality naturally. |
| **Modeling accuracy** | Optional parts are containment, not specialization vs. inheritance seems like it captures the difference. |

### Riel-5.18:4 - Solution

Model optional components as nullable or Optional-typed contained objects. Do not create subclasses for the presence or absence of optional parts.

### Riel-5.18:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Car` may optionally have a `Sunroof`. Model this as an optional contained object, not as `CarWithSunroof` and `CarWithoutSunroof` subclasses. |
| **U.Episteme** | A `Study` may optionally have a `ControlGroup`. Use optional containment, not `ControlledStudy`/`UncontrolledStudy` subclasses. |

### Riel-5.18:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.18:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.18.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.18.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.18:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Optional-as-subclass** | Subclasses created for with/without optional components. | Combinatorial explosion; 2^N subclasses for N options. | Use optional containment. |

### Riel-5.18:9 - Consequences

| Benefits |
|----------|
| Optional components are modeled naturally without class proliferation. |

| Trade-off | Mitigation |
|-----------|-----------|
| Null checks | Optional containment requires null safety; mitigated by Optional types. |

### Riel-5.18:10 - Rationale

Optional parts are an orthogonal axis of variation. Inheritance is for specialization, not for presence/absence of components.

### Riel-5.18:11 - SoTA-Echoing

Optional types (Java Optional, Kotlin nullable, Rust Option) provide safe optional containment. The Decorator pattern (GoF, 1994) adds optional behavior without subclassing.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.18:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.18:End
