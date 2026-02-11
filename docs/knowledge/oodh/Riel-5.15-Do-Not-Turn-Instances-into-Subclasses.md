## Riel-5.15 - Do Not Turn Instances into Subclasses

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Do not turn objects of a class into derived classes of the class. Be very suspicious of any derived class for which there is only one instance."*

### Riel-5.15:1 - Problem Frame

Sometimes designers create a subclass for what is really just a particular instance of the base class.

### Riel-5.15:2 - Problem

If a derived class has only one instance (e.g., `Mars` as a subclass of `Planet`), the designer has confused classification with instantiation. `Mars` is an instance of `Planet`, not a type of planet.

### Riel-5.15:3 - Forces

| Force | Tension |
|-------|---------|
| **Instance vs. type** | Instances are objects of a class vs. types are classes in a hierarchy. |
| **Singleton confusion** | A unique entity feels like it deserves its own class vs. it is just a unique instance. |

### Riel-5.15:4 - Solution

If a would-be subclass would have only one instance, model it as an instance (object) of the existing class with unique attribute values, not as a separate class.

### Riel-5.15:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | `Mars`, `Earth`, and `Jupiter` are instances of `Planet`, not subclasses. |
| **U.Episteme** | A specific historical experiment is an instance of `Experiment`, not a subclass. |

### Riel-5.15:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.15:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.15.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.15.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.15:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Instance-as-class** | A single-instance subclass. | Confuses the type system; class proliferation without purpose. | Make it an instance with unique attribute values. |

### Riel-5.15:9 - Consequences

| Benefits |
|----------|
| The type hierarchy reflects genuine classification. |
| No single-instance class clutter. |

| Trade-off | Mitigation |
|-----------|-----------|
| Reduced specificity | Instance-specific behavior may require configuration; mitigated by Strategy or configuration patterns. |

### Riel-5.15:10 - Rationale

The class-instance distinction is fundamental. A class represents a category; an instance represents a particular. Confusing them is a category error.

### Riel-5.15:11 - SoTA-Echoing

UML distinguishes between classifiers and instances explicitly. Domain-Driven Design's Entity vs Value Object distinction reinforces this.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.15:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.15:End
