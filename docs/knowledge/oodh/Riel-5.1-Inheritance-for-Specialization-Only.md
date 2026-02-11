## Riel-5.1 - Inheritance for Specialization Only

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Inheritance should be used only to model a specialization hierarchy."*

### Riel-5.1:1 - Problem Frame

Inheritance is the strongest relationship in OO. It is often abused for code reuse when containment or delegation would be more appropriate.

### Riel-5.1:2 - Problem

Using inheritance for anything other than genuine specialization ('is-a') creates fragile hierarchies where derived classes inherit inappropriate behavior and violate substitutability.

### Riel-5.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Code reuse temptation** | Inheritance provides free code reuse vs. it also inherits semantic commitments. |
| **Substitutability** | Specialization preserves Liskov Substitutability vs. non-specialization breaks it. |

### Riel-5.1:4 - Solution

Before using inheritance, verify that the derived class is a genuine specialization of the base class—every instance of the derived class must be substitutable wherever the base class is expected. If the relationship is 'uses' or 'has-a', prefer containment.

### Riel-5.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `SavingsAccount` is a genuine specialization of `BankAccount`. But `Stack` should not inherit from `LinkedList` merely to reuse its storage—that is containment. |
| **U.Episteme** | A `PeerReviewedArticle` is a genuine specialization of `Publication`. But `Bibliography` should not inherit from `List` just to reuse list operations. |

### Riel-5.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Convenience inheritance** | Inheriting to get free methods, not to model specialization. | Breaks substitutability; inherited methods may be nonsensical. | Use containment or delegation instead. |

### Riel-5.1:9 - Consequences

| Benefits |
|----------|
| Hierarchies are meaningful and substitutable. |
| Derived classes honor base class contracts. |

| Trade-off | Mitigation |
|-----------|-----------|
| Less free code | Containment requires delegation boilerplate; mitigated by composition utilities and IDE support. |

### Riel-5.1:10 - Rationale

Inheritance is a semantic relationship (is-a), not a code-sharing mechanism. Misusing it corrupts the type system.

### Riel-5.1:11 - SoTA-Echoing

The Liskov Substitution Principle (Liskov & Wing, 1994) formalizes this. 'Favor composition over inheritance' (GoF, 1994; Effective Java, Bloch, 2018) is the practical corollary.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.1:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5, Riel-5.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.1:End
