	## Riel-5.19 - Build Reusable Frameworks, Not Just Components

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"When building an inheritance hierarchy, try to construct reusable frameworks rather than reusable components."*

### Riel-5.19:1 - Problem Frame

OO design can aim for reusable individual classes (components) or for reusable hierarchies and collaboration patterns (frameworks).

### Riel-5.19:2 - Problem

Reusable components have limited value without the context in which they collaborate. Reusable frameworks capture the collaboration structure itself, providing far greater reuse leverage.

### Riel-5.19:3 - Forces

| Force | Tension |
|-------|---------|
| **Reuse scope** | Framework reuse is more powerful than component reuse vs. frameworks are harder to design. |
| **Abstraction level** | Frameworks capture collaboration patterns vs. components capture individual behaviors. |

### Riel-5.19:4 - Solution

Design inheritance hierarchies with framework reuse in mind: define abstract classes that capture the collaboration protocol, leaving concrete implementations to be plugged in by users.

### Riel-5.19:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A GUI framework defines abstract `Widget`, `Layout`, and `EventHandler` with collaboration protocols. Users implement concrete versions. |
| **U.Episteme** | A research framework defines abstract `DataSource`, `Analyzer`, and `Reporter` with collaboration protocols. Researchers implement concrete versions. |

### Riel-5.19:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.19:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.19.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.19.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.19:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Isolated reuse** | Individual classes are reusable but the collaboration patterns are not. | Limited reuse leverage; users must rediscover collaboration patterns. | Design the collaboration itself for reuse. |

### Riel-5.19:9 - Consequences

| Benefits |
|----------|
| Users reuse entire patterns of collaboration, not just individual classes. |

| Trade-off | Mitigation |
|-----------|-----------|
| Framework design difficulty | Frameworks are harder to design correctly; mitigated by incremental refinement based on concrete uses. |

### Riel-5.19:10 - Rationale

The highest value in OO reuse lies not in individual classes but in the patterns of collaboration between them. Frameworks capture these patterns.

### Riel-5.19:11 - SoTA-Echoing

Application frameworks (Spring, Rails, React) exemplify this. Domain-Specific Languages (DSLs) extend the idea further. Hexagonal Architecture's ports-and-adapters provide a framework structure.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.19:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.19:End
