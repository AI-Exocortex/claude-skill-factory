## Riel-3.4 - Watch for Noncommunicating Behavior

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Beware of classes that have too much noncommunicating behavior, that is, methods that operate on a proper subset of the data members of a class. God classes often exhibit a great deal of noncommunicating behavior."*

### Riel-3.4:1 - Problem Frame

A class whose methods split into clusters, each using only a subset of the data, has low internal cohesion and likely conflates multiple abstractions.

### Riel-3.4:2 - Problem

Noncommunicating behavior indicates the class should be split. Left unaddressed, it grows into a god class with increasingly tangled responsibilities.

### Riel-3.4:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion** | High cohesion means all methods use most data vs. clusters reveal hidden abstractions. |
| **Detection difficulty** | Noncommunicating behavior is invisible in code reviews without explicit analysis vs. metrics can detect it. |

### Riel-3.4:4 - Solution

Analyze method-data affinity. When methods cluster around data subsets, extract each cluster with its data into a separate class. Cohesion metrics (LCOM) help detect this programmatically.

### Riel-3.4:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Vehicle` class where engine methods never touch navigation data, and vice versa, should be split into `Engine` and `Navigator`. |
| **U.Episteme** | A `StudyReport` class where statistical methods and bibliography methods never share data members should be split into `StatisticalAnalysis` and `Bibliography`. |

### Riel-3.4:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.4:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.4.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.4.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.4:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Creeping conflation** | Over time, unrelated features are added to an existing class. | Low cohesion, high complexity. | Regularly run LCOM analysis and extract when clusters emerge. |

### Riel-3.4:9 - Consequences

| Benefits |
|----------|
| Each resulting class has high cohesion. |
| The god-class risk is eliminated early. |

| Trade-off | Mitigation |
|-----------|-----------|
| Refactoring cost | Splitting an established class requires effort; the cost grows if deferred. |

### Riel-3.4:10 - Rationale

Noncommunicating behavior is a quantifiable cohesion failure. It is the internal signal that a class has violated the one-key-abstraction principle.

### Riel-3.4:11 - SoTA-Echoing

LCOM (Lack of Cohesion of Methods) metrics (Chidamber & Kemerer, 1994; Henderson-Sellers, 1996) formalize this. Modern IDEs and static analyzers report cohesion metrics.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.4:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.5, Riel-3.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.4:End
