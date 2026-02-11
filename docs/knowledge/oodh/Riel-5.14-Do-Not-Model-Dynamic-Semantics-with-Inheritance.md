## Riel-5.14 - Do Not Model Dynamic Semantics with Inheritance

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Do not model the dynamic semantics of a class through the use of the inheritance relationship. An attempt to model dynamic semantics with a static semantic relationship will lead to a toggling of types at runtime."*

### Riel-5.14:1 - Problem Frame

Inheritance defines a static relationship: an object's class is fixed at creation. Using it to model state changes leads to objects needing to change class at runtime.

### Riel-5.14:2 - Problem

If a `Person` is modeled as a `Student` subclass, what happens when they graduate? They must be destroyed and recreated as a `Graduate`—a runtime type toggle that is awkward and error-prone.

### Riel-5.14:3 - Forces

| Force | Tension |
|-------|---------|
| **Static vs. dynamic** | Inheritance is compile-time vs. state changes are runtime phenomena. |
| **Identity continuity** | Objects should maintain identity through state changes vs. type changes require new objects. |

### Riel-5.14:4 - Solution

Use the State pattern, role objects, or attribute-based modeling for dynamic semantics. Reserve inheritance for permanent, structural specialization.

### Riel-5.14:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Person` who transitions from `Student` to `Employee` should use a state or role attribute, not a class change. |
| **U.Episteme** | A `Manuscript` that transitions from `Draft` to `InReview` to `Published` should use the State pattern, not subclasses. |

### Riel-5.14:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.14:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.14.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.14.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.14:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Type toggling** | An object's class must change at runtime to reflect a state change. | Requires object destruction and recreation; breaks identity. | Use State pattern or role objects. |

### Riel-5.14:9 - Consequences

| Benefits |
|----------|
| Objects maintain identity through state changes. |
| State transitions are clean and explicit. |

| Trade-off | Mitigation |
|-----------|-----------|
| Pattern complexity | State pattern adds classes; mitigated by clear state management. |

### Riel-5.14:10 - Rationale

Inheritance models what an object *is*, permanently. Dynamic behavior models what an object *does*, transiently. Mixing them creates incoherent designs.

### Riel-5.14:11 - SoTA-Echoing

State pattern (GoF, 1994). Role Object pattern (Bäumer et al., 1997). Modern state machines (XState, 2020s) formalize dynamic semantics.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.14:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.14:End
