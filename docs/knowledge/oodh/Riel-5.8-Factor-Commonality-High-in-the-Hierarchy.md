## Riel-5.8 - Factor Commonality High in the Hierarchy

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Factor the commonality of data, behavior, and/or interface as high as possible in the inheritance hierarchy."*

### Riel-5.8:1 - Problem Frame

When multiple classes share data, behavior, or interface, the shared elements should be placed in their common ancestor.

### Riel-5.8:2 - Problem

Shared behavior duplicated across sibling classes is a maintenance burden. Changes must be replicated across all copies, risking inconsistency.

### Riel-5.8:3 - Forces

| Force | Tension |
|-------|---------|
| **DRY** | Sharing via inheritance eliminates duplication vs. premature factoring can create artificial abstractions. |
| **Hierarchy depth** | Factoring high adds intermediate levels vs. keeps shared code in one place. |

### Riel-5.8:4 - Solution

Identify common data, behavior, and interface across sibling classes and migrate them to the nearest common ancestor. Create a new intermediate abstract class if no suitable ancestor exists.

### Riel-5.8:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `Car` and `Truck` both implement `startEngine()`, move it to their common ancestor `MotorVehicle`. |
| **U.Episteme** | If `TTest` and `ANOVA` both implement `checkAssumptions()`, move it to `StatisticalTest`. |

### Riel-5.8:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.8:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.8.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.8.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.8:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Sibling duplication** | Multiple subclasses duplicate identical code. | Maintenance nightmare; inconsistency risk. | Extract common code to the nearest ancestor. |

### Riel-5.8:9 - Consequences

| Benefits |
|----------|
| Code is shared rather than duplicated. |
| Changes propagate automatically through inheritance. |

| Trade-off | Mitigation |
|-----------|-----------|
| Artificial intermediates | New abstract classes may feel forced; justified by eliminated duplication. |

### Riel-5.8:10 - Rationale

DRY (Don't Repeat Yourself) is fundamental. Inheritance is the natural mechanism for sharing across a specialization hierarchy.

### Riel-5.8:11 - SoTA-Echoing

Extract Superclass refactoring (Fowler, 1999/2018). Template Method (GoF, 1994) formalizes shared algorithm structure.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.8:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.8:End
