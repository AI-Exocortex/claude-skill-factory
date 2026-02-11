## Riel-5.9 - Common Data Without Behavior: Use Containment

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"If two or more classes share only common data (no common behavior), then that common data should be placed in a class that will be contained by each sharing class."*

### Riel-5.9:1 - Problem Frame

When classes share data but not behavior, inheritance is not the right mechanism—there is no behavioral contract to inherit.

### Riel-5.9:2 - Problem

Using inheritance to share only data violates the specialization principle and creates a misleading hierarchy.

### Riel-5.9:3 - Forces

| Force | Tension |
|-------|---------|
| **Relationship accuracy** | Containment correctly models 'has-a' data sharing vs. inheritance implies 'is-a' which is false here. |
| **Code reuse** | Both mechanisms provide reuse vs. only inheritance also implies substitutability. |

### Riel-5.9:4 - Solution

Extract the common data into a separate class. Each sharing class contains an instance of this data class. No inheritance hierarchy is created.

### Riel-5.9:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `Employee` and `Customer` share `Address` data but no address behavior, create an `Address` class contained by both. |
| **U.Episteme** | If `Article` and `Book` share `PublicationMetadata` but no common behavior, create a `PublicationMetadata` containment object. |

### Riel-5.9:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.9:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.9.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.9.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.9:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Data inheritance** | Classes inherit from a common base purely for shared fields. | Misleading hierarchy; false is-a relationship. | Use containment instead. |

### Riel-5.9:9 - Consequences

| Benefits |
|----------|
| The design accurately reflects relationships. |
| No false inheritance hierarchies. |

| Trade-off | Mitigation |
|-----------|-----------|
| Delegation boilerplate | Accessing contained data requires forwarding; mitigated by language features. |

### Riel-5.9:10 - Rationale

Inheritance is for shared behavior (specialization). Shared data without shared behavior is a containment relationship.

### Riel-5.9:11 - SoTA-Echoing

The 'composition over inheritance' principle (GoF, 1994). Mixins and traits provide an intermediate option in some languages.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.9:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.9:End
