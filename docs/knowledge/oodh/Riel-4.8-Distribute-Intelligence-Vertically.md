## Riel-4.8 - Distribute Intelligence Vertically

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Distribute system intelligence vertically down narrow and deep containment hierarchies."*

### Riel-4.8:1 - Problem Frame

Complementing horizontal distribution (Heuristic 3.1), intelligence should also flow vertically down containment hierarchies.

### Riel-4.8:2 - Problem

When all intelligence sits at the top of a containment hierarchy, the top-level class becomes a god class while contained objects are passive data holders.

### Riel-4.8:3 - Forces

| Force | Tension |
|-------|---------|
| **Intelligence placement** | Push intelligence down to where the data lives vs. top-level coordination may seem natural. |
| **Depth vs. breadth** | Deep hierarchies with smart components vs. flat hierarchies with one smart controller. |

### Riel-4.8:4 - Solution

Push behavior down to the most specific contained object that has the relevant data. The containing class should delegate to its parts rather than reaching into their data to perform operations itself.

### Riel-4.8:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In a `Robot` containing an `Arm` containing a `Gripper`, force-feedback logic belongs in `Gripper`, not in `Robot`. |
| **U.Episteme** | In a `MetaAnalysis` containing `Studies` containing `Experiments`, statistical validation belongs in `Experiment`, not in `MetaAnalysis`. |

### Riel-4.8:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.8:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.8.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.8.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.8:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Top-heavy hierarchy** | The top-level class contains all logic; contained objects are data bags. | God class at the top; anemic objects below. | Delegate behavior to the contained objects that own the data. |

### Riel-4.8:9 - Consequences

| Benefits |
|----------|
| Intelligence is localized to where data lives. |
| Each level of the hierarchy is cohesive. |

| Trade-off | Mitigation |
|-----------|-----------|
| Navigation complexity | Deep delegation chains require careful design; mitigated by clear contracts at each level. |

### Riel-4.8:10 - Rationale

Vertical intelligence distribution is the containment-hierarchy analog of horizontal distribution. Together, they ensure no single class accumulates disproportionate responsibility.

### Riel-4.8:11 - SoTA-Echoing

The 'Information Expert' GRASP pattern (Larman, 2004) assigns responsibility to the class with the data. This heuristic extends it vertically through containment.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.8:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.8:End
