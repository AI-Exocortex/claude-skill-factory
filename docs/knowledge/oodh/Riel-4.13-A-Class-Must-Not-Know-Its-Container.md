## Riel-4.13 - A Class Must Not Know Its Container

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"A class must know what it contains, but it should never know who contains it."*

### Riel-4.13:1 - Problem Frame

Containment creates an asymmetric knowledge relationship. The container knows its parts; the parts should not know their container.

### Riel-4.13:2 - Problem

If a contained class knows its container, it cannot be reused in a different container. The dependency direction is inverted, creating tight coupling.

### Riel-4.13:3 - Forces

| Force | Tension |
|-------|---------|
| **Reusability** | Container-unaware parts are reusable anywhere vs. container-aware parts are locked in. |
| **Communication needs** | Parts sometimes need to notify containers vs. this can be done without direct knowledge. |

### Riel-4.13:4 - Solution

Design contained classes without any reference to their container. If upward communication is needed, use observer patterns, callbacks, or event mechanisms that do not require knowledge of the specific container type.

### Riel-4.13:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Wheel` should not know it is inside a `Car`. It should work identically in a `Bicycle` or a `Cart`. |
| **U.Episteme** | A `DataPoint` should not know it is part of a `TimeSeries` or a `CrossSection`. Its behavior should be container-independent. |

### Riel-4.13:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.13:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.13.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.13.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.13:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Upward reference** | A part holds a typed reference to its container. | Cannot be reused in a different container. | Use an abstract observer or event interface instead. |

### Riel-4.13:9 - Consequences

| Benefits |
|----------|
| Parts are maximally reusable. |
| Containment hierarchies can be restructured freely. |

| Trade-off | Mitigation |
|-----------|-----------|
| Communication complexity | Observer patterns add indirection; mitigated by well-understood patterns. |

### Riel-4.13:10 - Rationale

Containment should be a one-way knowledge relationship. Parts that know their containers are coupled upward, destroying composability.

### Riel-4.13:11 - SoTA-Echoing

The Dependency Inversion Principle (Martin, 2003) forbids upward dependencies. Component architectures (React, SwiftUI) enforce this: child components never reference parent types.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.13:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.13:End
