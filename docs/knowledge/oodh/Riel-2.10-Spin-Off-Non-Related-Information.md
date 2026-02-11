## Riel-2.10 - Spin Off Non-Related Information

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Spin off nonrelated information into another class (i.e., noncommunicating behavior)."*

### Riel-2.10:1 - Problem Frame

A class may accumulate methods that operate on disjoint subsets of its data members. These noncommunicating method groups indicate that multiple abstractions have been conflated.

### Riel-2.10:2 - Problem

Noncommunicating behavior within a class signals low cohesion. The class is doing too many unrelated things, making it harder to understand, test, and reuse.

### Riel-2.10:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion** | High cohesion requires related behavior only vs. convenience gathers unrelated things. |
| **Discoverability** | Focused classes are found easily vs. unfocused classes hide capabilities. |

### Riel-2.10:4 - Solution

Identify method groups that operate on disjoint data subsets. Extract each group, along with its data, into a separate class. The original class may then contain or reference the new classes.

### Riel-2.10:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Vehicle` class with separate method clusters for engine management and GPS navigation should be split: the engine logic moves to an `Engine` class, the navigation to a `Navigator`. |
| **U.Episteme** | A `ResearchPaper` class with separate clusters for bibliographic metadata and statistical analysis should split these into `BibliographicRecord` and `StatisticalSummary`. |

### Riel-2.10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.10.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.10.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.10:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Grab-bag class** | A class accumulates methods from unrelated domains over time. | Low cohesion; hard to name; hard to test in isolation. | Periodically audit method-data affinity and extract classes. |

### Riel-2.10:9 - Consequences

| Benefits |
|----------|
| Each resulting class has high cohesion and a clear purpose. |
| Testing becomes targeted and simpler. |

| Trade-off | Mitigation |
|-----------|-----------|
| Refactoring effort | Splitting requires updating references; mitigated by improved long-term maintainability. |

### Riel-2.10:10 - Rationale

Noncommunicating behavior is the telltale sign of a class with multiple responsibilities. Extracting these into separate classes is a direct application of the cohesion principle.

### Riel-2.10:11 - SoTA-Echoing

The Extract Class refactoring (Fowler, 1999/2018) operationalizes this heuristic. LCOM metrics (Chidamber & Kemerer, 1994) quantify noncommunicating behavior.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.10:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.10:End
