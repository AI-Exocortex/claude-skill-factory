## Riel-5.13 - Replace Value-Based Case Analysis with Inheritance

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Explicit case analysis on the value of an attribute is often an error. The class should be decomposed into an inheritance hierarchy, where each value of the attribute is transformed into a derived class."*

### Riel-5.13:1 - Problem Frame

Code that branches on the value of a type-code attribute (e.g., `if (status == ACTIVE)`) often signals that the class should be split into subclasses.

### Riel-5.13:2 - Problem

Value-based case analysis scatters state-specific behavior across methods, making each method a multiplexer. Adding a new value requires touching every method.

### Riel-5.13:3 - Forces

| Force | Tension |
|-------|---------|
| **State encapsulation** | Subclasses encapsulate state-specific behavior vs. type codes keep everything in one class. |
| **Class proliferation** | Subclasses increase count vs. cleaner behavior distribution. |

### Riel-5.13:4 - Solution

When methods repeatedly branch on the same attribute value, consider transforming each value into a derived class. Each subclass encapsulates the behavior for its state, eliminating the case analysis.

### Riel-5.13:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | An `Order` with a `status` field branching on PENDING/SHIPPED/DELIVERED should become `PendingOrder`, `ShippedOrder`, `DeliveredOrder` subclasses (or use the State pattern). |
| **U.Episteme** | A `ReviewDecision` branching on ACCEPT/REVISE/REJECT should become subclasses or a State pattern. |

### Riel-5.13:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.13:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.13.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.13.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.13:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Type-code multiplexing** | Methods branch on an attribute value throughout the class. | Every new value requires changes in every method. | Replace with inheritance or State pattern. |

### Riel-5.13:9 - Consequences

| Benefits |
|----------|
| State-specific behavior is encapsulated. |
| Adding new states requires only a new class. |

| Trade-off | Mitigation |
|-----------|-----------|
| More classes | One class per value; mitigated by clear, focused classes. State pattern is an alternative. |

### Riel-5.13:10 - Rationale

Value-based case analysis is a procedural pattern. Converting it to inheritance or the State pattern leverages polymorphism.

### Riel-5.13:11 - SoTA-Echoing

Replace Type Code with Subclasses/State (Fowler, 1999/2018). The State pattern (GoF, 1994) provides a dynamic alternative.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.13:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.13:End
