## Riel-2.9 - Keep Related Data and Behavior Together

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Keep related data and behavior in one place."*

### Riel-2.9:1 - Problem Frame

Object orientation's central promise is co-locating the data of an abstraction with the behavior that operates on it. Violating this scatters logic across the system.

### Riel-2.9:2 - Problem

When behavior that operates on a class's data is placed outside that class, developers must coordinate changes across multiple locations, leading to programming by convention and subtle bugs.

### Riel-2.9:3 - Forces

| Force | Tension |
|-------|---------|
| **Locality** | Co-location simplifies understanding and change vs. external placement may seem necessary for cross-cutting concerns. |
| **Convention risk** | Scattered behavior requires developers to remember non-obvious coordination rules vs. co-location makes dependencies explicit. |

### Riel-2.9:4 - Solution

Place every operation that primarily manipulates a class's data inside that class. If an operation requires data from multiple classes, consider which class is the natural owner and place the operation there, or introduce a mediator.

### Riel-2.9:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Temperature conversion logic belongs inside the `Temperature` class, not in a distant `ConversionUtility`. The data (degrees, scale) and the behavior (convert) are inseparable. |
| **U.Episteme** | Validation rules for a `Measurement` belong inside the `Measurement` class, not in an external validator. The class knows its own invariants. |

### Riel-2.9:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.9:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.9.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.9.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.9:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Anemic domain model** | Classes hold data only; all behavior lives in 'service' classes. | Scatters related logic; breaks encapsulation. | Move behavior to the class that owns the data. |

### Riel-2.9:9 - Consequences

| Benefits |
|----------|
| Changes to an abstraction are localized. |
| The class is self-documenting about its capabilities. |

| Trade-off | Mitigation |
|-----------|-----------|
| Class size growth | Some classes may grow larger; mitigated by splitting when multiple abstractions emerge. |

### Riel-2.9:10 - Rationale

Co-location of data and behavior is the defining characteristic of object orientation. Violating it reduces the design to a procedural system with data structures and separate functions.

### Riel-2.9:11 - SoTA-Echoing

Fowler's 'Anemic Domain Model' anti-pattern (2003) describes the consequences of violating this heuristic. Domain-Driven Design's Aggregate pattern (Evans, 2003) reinforces behavioral encapsulation.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.9:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.9:End
