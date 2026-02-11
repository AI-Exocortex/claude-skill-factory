## Riel-5.16 - Do Not Create Classes at Runtime

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"If you think you need to create new classes at runtime, take a step back and realize that what you are trying to create are objects. Now generalize these objects into a class."*

### Riel-5.16:1 - Problem Frame

Some designs appear to require runtime class creation, where new types emerge during execution.

### Riel-5.16:2 - Problem

Runtime class creation confuses the class level with the object level. What seems like a new type is almost always a new instance with different configuration.

### Riel-5.16:3 - Forces

| Force | Tension |
|-------|---------|
| **Static vs. dynamic typing** | Classes are defined at compile time vs. dynamic needs are met by object configuration. |
| **Generalization** | A class that generates varied instances is more powerful than runtime class creation. |

### Riel-5.16:4 - Solution

Instead of creating new classes at runtime, generalize the varying behavior into a single class parameterized by configuration, strategies, or data. Create new objects of that class at runtime.

### Riel-5.16:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Instead of generating a new `RedWidget` class at runtime, create a `Widget` class with a `color` attribute and instantiate it with `color=RED`. |
| **U.Episteme** | Instead of generating a new `SpecificStudyDesign` class, create a configurable `StudyDesign` class parameterized by its characteristics. |

### Riel-5.16:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.16:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.16.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.16.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.16:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Runtime class generation** | Code generates new class definitions dynamically. | Confuses meta-levels; hard to reason about types. | Generalize into a configurable class with runtime object creation. |

### Riel-5.16:9 - Consequences

| Benefits |
|----------|
| The type system is static and comprehensible. |
| Runtime variation is handled through object configuration. |

| Trade-off | Mitigation |
|-----------|-----------|
| Configuration complexity | Configurable classes may be more complex; offset by comprehensibility. |

### Riel-5.16:10 - Rationale

The class/object distinction is a fundamental OO boundary. Crossing it dynamically creates confusion at both levels.

### Riel-5.16:11 - SoTA-Echoing

Prototype pattern (GoF, 1994) and Abstract Factory provide object-level variation without runtime class creation. Dynamic languages (Python, Ruby) blur this line but should still prefer instances.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.16:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.16:End
