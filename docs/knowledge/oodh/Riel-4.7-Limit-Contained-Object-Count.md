## Riel-4.7 - Limit Contained Object Count

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Classes should not contain more objects than a developer can fit in his or her short-term memory. A favorite value for this number is six."*

### Riel-4.7:1 - Problem Frame

Human short-term memory has a well-known capacity limitation. A class with too many contained objects exceeds a developer's ability to reason about it.

### Riel-4.7:2 - Problem

When a class contains more objects than a person can mentally track (roughly six), it becomes difficult to understand, debug, and maintain.

### Riel-4.7:3 - Forces

| Force | Tension |
|-------|---------|
| **Cognitive limits** | Human memory limits constrain effective class size vs. complex domains may have many parts. |
| **Decomposition** | Splitting reduces per-class count vs. adds containment levels. |

### Riel-4.7:4 - Solution

Limit the number of directly contained objects to approximately six. When a class naturally has more components, introduce intermediate containing classes to group related components.

### Riel-4.7:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Computer` class should not directly contain CPU, RAM, SSD, GPU, PSU, motherboard, fan, case, and six peripheral ports. Group them: `Motherboard` contains CPU and RAM, etc. |
| **U.Episteme** | A `ConferenceProceedings` should not directly contain hundreds of `Paper` objects; group them by session or topic. |

### Riel-4.7:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.7:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.7.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.7.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.7:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Flat containment explosion** | A class directly contains dozens of objects. | Exceeds cognitive limits; hard to reason about. | Introduce intermediate grouping classes. |

### Riel-4.7:9 - Consequences

| Benefits |
|----------|
| Each class is comprehensible at a glance. |
| Deep, narrow hierarchies guide attention. |

| Trade-off | Mitigation |
|-----------|-----------|
| Deeper hierarchies | More containment levels add indirection; mitigated by improved comprehensibility at each level. |

### Riel-4.7:10 - Rationale

Design should respect human cognitive limits. The magic number seven (plus or minus two) from Miller's (1956) research is a practical upper bound.

### Riel-4.7:11 - SoTA-Echoing

Miller's Law (1956) on short-term memory capacity. The Rule of Seven is applied across UX, architecture, and management. Modern complexity metrics enforce similar limits.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.7:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.7:End
