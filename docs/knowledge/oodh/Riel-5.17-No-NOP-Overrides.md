## Riel-5.17 - No NOP Overrides

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"It should be illegal for a derived class to override a base class method with a NOP method, that is, a method that does nothing."*

### Riel-5.17:1 - Problem Frame

When a derived class inherits a method that is not applicable to it, the temptation is to override it with an empty (NOP) implementation.

### Riel-5.17:2 - Problem

A NOP override means the derived class does not truly satisfy the base class contract. It breaks the Liskov Substitution Principle: callers expect the method to have an effect, but it silently does nothing.

### Riel-5.17:3 - Forces

| Force | Tension |
|-------|---------|
| **Substitutability** | Derived classes must honor base class contracts vs. some inherited methods may not apply. |
| **Hierarchy correctness** | A NOP signals a flawed hierarchy vs. it seems like a pragmatic fix. |

### Riel-5.17:4 - Solution

If a derived class needs to NOP a method, the inheritance hierarchy is flawed. Either the method does not belong in the base class, or the derived class is not a genuine specialization. Restructure the hierarchy.

### Riel-5.17:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If a `Penguin` subclass of `Bird` overrides `fly()` with a NOP, the hierarchy is wrong. Not all birds fly; introduce a `FlyingBird` intermediate class. |
| **U.Episteme** | If a `TheoreticalStudy` NOPs `collectData()` inherited from `Study`, the hierarchy needs restructuring. |

### Riel-5.17:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.17:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.17.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.17.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.17:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **NOP override** | An overriding method has an empty body. | Breaks the base class contract; callers are silently deceived. | Restructure the hierarchy to avoid inheriting inapplicable methods. |

### Riel-5.17:9 - Consequences

| Benefits |
|----------|
| Every method in the hierarchy does real work. |
| Substitutability is preserved. |

| Trade-off | Mitigation |
|-----------|-----------|
| Hierarchy restructuring | May require adding intermediate classes; a necessary investment in correctness. |

### Riel-5.17:10 - Rationale

A NOP override is a code-level declaration that the hierarchy is wrong. The fix is structural, not behavioral.

### Riel-5.17:11 - SoTA-Echoing

Liskov Substitution Principle (1994). The 'Refused Bequest' smell (Fowler, 1999/2018) captures this. Interface segregation avoids the problem.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.17:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.17:End
