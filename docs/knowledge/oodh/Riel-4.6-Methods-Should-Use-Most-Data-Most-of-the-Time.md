## Riel-4.6 - Methods Should Use Most Data Most of the Time

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Most of the methods defined on a class should be using most of the data members most of the time."*

### Riel-4.6:1 - Problem Frame

Cohesion is measurable by examining how many data members each method accesses. If most methods access most data, cohesion is high.

### Riel-4.6:2 - Problem

When methods access only small subsets of the data, it indicates that the class may be capturing multiple abstractions and should be split.

### Riel-4.6:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion measurement** | Uniform data access implies cohesion vs. clustered access implies hidden abstractions. |
| **Class splitting** | Extracting classes from clusters increases class count vs. improves cohesion. |

### Riel-4.6:4 - Solution

Analyze method-to-data-member usage patterns. If methods partition into groups that access disjoint data subsets, extract each group with its data into a separate class.

### Riel-4.6:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In a `Vehicle` class, if engine methods and navigation methods access disjoint fields, split into `Engine` and `Navigator`. |
| **U.Episteme** | In a `Publication` class, if citation-tracking methods and review-tracking methods access disjoint fields, split accordingly. |

### Riel-4.6:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.6:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.6.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.6.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.6:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Hidden partitioning** | Methods naturally cluster around data subsets but the class is never split. | Low LCOM; hard to understand; testing is complex. | Run LCOM analysis and extract classes. |

### Riel-4.6:9 - Consequences

| Benefits |
|----------|
| Each class has verifiably high cohesion. |

| Trade-off | Mitigation |
|-----------|-----------|
| Overhead of measurement | Requires analysis tooling; mitigated by IDE and static analysis support. |

### Riel-4.6:10 - Rationale

This heuristic provides a quantifiable criterion for cohesion: the degree to which methods share data members.

### Riel-4.6:11 - SoTA-Echoing

LCOM metrics (Chidamber & Kemerer, 1994) directly measure this. Tools like SonarQube compute LCOM automatically.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.6:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.6:End
