## Riel-5.3 - All Base Class Data Should Be Private

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"All data in a base class should be private; do not use protected data."*

### Riel-5.3:1 - Problem Frame

Protected data in a base class is accessible to all derived classes, creating a coupling surface across the hierarchy.

### Riel-5.3:2 - Problem

Protected data allows derived classes to bypass the base class's methods and manipulate internal state directly, breaking encapsulation along the hierarchy dimension.

### Riel-5.3:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Private data preserves encapsulation vs. protected data seems convenient for subclasses. |
| **Coupling** | Protected data couples all derived classes to the representation vs. private data forces use of methods. |

### Riel-5.3:4 - Solution

Make all base class data private. Provide protected methods for access if needed, but never expose the data members themselves.

### Riel-5.3:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Vehicle` base class should not expose `protected int speed`. Instead, provide `protected void accelerate(int delta)` with invariant checks. |
| **U.Episteme** | A `Model` base class should not expose `protected double[] weights`. Provide `protected void updateWeights(...)` with validation. |

### Riel-5.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.3:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.3.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.3.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.3:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Protected field** | Base class data is declared protected for subclass convenience. | All subclasses are coupled to the representation; invariant checks can be bypassed. | Use private data with protected accessor methods. |

### Riel-5.3:9 - Consequences

| Benefits |
|----------|
| Base class representation can change without affecting subclasses. |
| Invariants are enforced consistently. |

| Trade-off | Mitigation |
|-----------|-----------|
| More methods | Protected accessor methods add code; mitigated by the encapsulation benefit. |

### Riel-5.3:10 - Rationale

Protected data is a half-measure that provides the illusion of encapsulation while actually exposing internals to an unbounded set of subclasses.

### Riel-5.3:11 - SoTA-Echoing

Effective Java (Bloch, 2018) and Effective C++ (Meyers, 2005) both advise against protected fields. Kotlin makes this easy by defaulting to `private` and providing `protected` accessors.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.3:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.4, Riel-5.5, Riel-5.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.3:End
