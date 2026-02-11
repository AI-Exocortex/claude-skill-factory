## Riel-4.1 - Minimize Collaborating Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Minimize the number of classes with which another class collaborates."*

### Riel-4.1:1 - Problem Frame

Every class a given class collaborates with represents a dependency. More dependencies mean more coupling and more fragility.

### Riel-4.1:2 - Problem

A class with many collaborators is tightly coupled to the system. Changes in any collaborator may require changes in this class, and testing requires complex setups.

### Riel-4.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Coupling breadth** | Fewer collaborators reduce coupling vs. complex tasks may require many participants. |
| **Testability** | Fewer dependencies simplify test setup vs. real behavior may need many interactions. |

### Riel-4.1:4 - Solution

Keep the collaborator set of each class as small as possible. If a class needs data or behavior from many other classes, consider introducing a mediator or facade that consolidates the interactions.

### Riel-4.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `PayrollCalculator` that directly accesses `Employee`, `TaxTable`, `Benefits`, `TimeSheet`, and `BankAPI` should use a `PayrollContext` facade. |
| **U.Episteme** | A `MetaAnalysis` class that directly accesses dozens of `Study` classes should use a `StudyRepository` abstraction. |

### Riel-4.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Highly-connected class** | A class imports and uses many other classes directly. | Fragile; changes propagate widely. | Introduce facades or mediators to reduce direct dependencies. |

### Riel-4.1:9 - Consequences

| Benefits |
|----------|
| Reduced coupling makes the class more stable and testable. |

| Trade-off | Mitigation |
|-----------|-----------|
| Indirection | Facades add a layer; mitigated by simpler individual class contracts. |

### Riel-4.1:10 - Rationale

Coupling breadth is a direct measure of fragility. Minimizing it improves resilience.

### Riel-4.1:11 - SoTA-Echoing

CBO (Coupling Between Objects) metric (Chidamber & Kemerer, 1994). The Law of Demeter (Lieberherr, 1989) limits transitive coupling. Facade pattern (GoF, 1994) consolidates interactions.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.1:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5, Riel-4.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.1:End
