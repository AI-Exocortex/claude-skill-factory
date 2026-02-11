## Riel-5.2 - Base Class Ignorance of Derived Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Derived classes must have knowledge of their base class by definition, but base classes should not know anything about their derived classes."*

### Riel-5.2:1 - Problem Frame

Inheritance creates an asymmetric knowledge relationship. The derived class knows its base; the base should be oblivious to its descendants.

### Riel-5.2:2 - Problem

If a base class references specific derived classes, adding a new derived class requires modifying the base, violating the Open/Closed Principle.

### Riel-5.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Extensibility** | An ignorant base class allows unlimited extension vs. base-class knowledge of derivatives limits it. |
| **Coupling direction** | Downward knowledge creates cycles vs. ignorance preserves acyclicity. |

### Riel-5.2:4 - Solution

Base classes must never import, reference, or conditionally branch on specific derived class types. Use virtual/abstract methods and polymorphic dispatch instead.

### Riel-5.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Shape` base class should not have `if (this instanceof Circle)` logic. It defines abstract `draw()` and lets each subclass implement it. |
| **U.Episteme** | A `StatisticalTest` base class should not check `if (this instanceof TTest)`. Each test subclass implements its own `compute()` method. |

### Riel-5.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Downward type check** | Base class uses instanceof to handle specific subclasses. | Every new subclass requires base-class modification. | Use polymorphic dispatch (virtual methods). |

### Riel-5.2:9 - Consequences

| Benefits |
|----------|
| New subclasses can be added without modifying the base. |
| The hierarchy is open for extension. |

| Trade-off | Mitigation |
|-----------|-----------|
| Abstract method discipline | Requires careful abstract interface design; mitigated by clear contracts. |

### Riel-5.2:10 - Rationale

This is the inheritance analog of Heuristic 2.2: the provider (base) should not know its consumers (derived classes).

### Riel-5.2:11 - SoTA-Echoing

The Open/Closed Principle (Meyer, 1988; Martin, 2003) formalizes this. Template Method (GoF, 1994) provides the pattern.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.2:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.3, Riel-5.4, Riel-5.5, Riel-5.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.2:End
