## Riel-4.3 - Minimize Collaboration Breadth

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Minimize the amount of collaboration between a class and its collaborator, that is, the number of different messages sent."*

### Riel-4.3:1 - Problem Frame

The number of distinct message types between two classes is a measure of the interface surface each depends on.

### Riel-4.3:2 - Problem

A wide message vocabulary between classes means each is deeply dependent on the other's interface, making changes in either class expensive.

### Riel-4.3:3 - Forces

| Force | Tension |
|-------|---------|
| **Interface dependency** | Fewer distinct messages reduce interface coupling vs. rich collaboration may require varied interactions. |

### Riel-4.3:4 - Solution

When two classes exchange many different message types, consider whether some of those interactions should be consolidated, or whether a different responsibility allocation would reduce the interface width.

### Riel-4.3:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `UIController` sends 12 different message types to `DataModel`, consider grouping related operations behind fewer, higher-level methods. |
| **U.Episteme** | If `AnalysisEngine` calls 10 different methods on `DataSource`, introduce a `DataView` abstraction that presents a simpler interface. |

### Riel-4.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.3:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.3.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.3.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.3:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Wide interface dependency** | Class A uses many distinct methods of class B. | Change in B's interface cascades to A. | Narrow the interface with facade or adapter patterns. |

### Riel-4.3:9 - Consequences

| Benefits |
|----------|
| Each class depends on a smaller slice of its collaborator's interface. |

| Trade-off | Mitigation |
|-----------|-----------|
| Abstraction overhead | May require intermediary types; justified by reduced coupling. |

### Riel-4.3:10 - Rationale

Interface width is a coupling dimension. Reducing it limits the blast radius of interface changes.

### Riel-4.3:11 - SoTA-Echoing

The Interface Segregation Principle (Martin, 2003) advocates narrow, role-specific interfaces.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.3:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.4, Riel-4.5, Riel-4.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.3:End
