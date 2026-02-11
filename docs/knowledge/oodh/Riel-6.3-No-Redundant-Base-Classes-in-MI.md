## Riel-6.3 - No Redundant Base Classes in MI

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 6 — Multiple Inheritance
> **Chapter Theme:** Multiple inheritance validation and simplification

**Original Statement:** *"Whenever you have found a multiple inheritance relationship in an object-oriented design, be sure that no base class is actually a derived class of another base class."*

### Riel-6.3:1 - Problem Frame

In MI hierarchies, it is possible for a class to inherit from two bases where one base is already a descendant of the other, creating redundancy.

### Riel-6.3:2 - Problem

Redundant inheritance creates diamond problems, duplicated state, and ambiguous method resolution—all without any design benefit.

### Riel-6.3:3 - Forces

| Force | Tension |
|-------|---------|
| **Hierarchy clarity** | Clean MI has orthogonal bases vs. redundant bases create diamonds. |
| **Resolution ambiguity** | Redundant paths cause ambiguous dispatch vs. clean paths are unambiguous. |

### Riel-6.3:4 - Solution

When using MI, verify that no base class is an ancestor of another base class in the same MI set. If it is, the inheritance is redundant and should be simplified.

### Riel-6.3:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `C` inherits from both `A` and `B`, and `B` already inherits from `A`, then C's inheritance from `A` is redundant. Simplify to inherit only from `B`. |
| **U.Episteme** | If a `ReviewArticle` inherits from both `Publication` and `PeerReviewedPublication`, and the latter already extends the former, the MI is redundant. |

### Riel-6.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-6.3:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-6.3.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-6.3.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-6.3:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Diamond duplication** | A class inherits from a base both directly and indirectly. | Duplicated state; ambiguous resolution. | Remove the direct redundant inheritance link. |

### Riel-6.3:9 - Consequences

| Benefits |
|----------|
| MI hierarchies are clean and unambiguous. |

| Trade-off | Mitigation |
|-----------|-----------|
| Review cost | Each MI case requires ancestry checking; a small cost for correctness. |

### Riel-6.3:10 - Rationale

Redundant MI paths add complexity without benefit. They are always simplifiable.

### Riel-6.3:11 - SoTA-Echoing

C++ virtual inheritance addresses diamond problems but adds complexity. Most modern languages avoid the issue by restricting MI to interfaces.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-6.3:12 - Relations

* **Source:** Riel (1996), Chapter 6 — Multiple Inheritance
* **Sibling heuristics:** Riel-6.1, Riel-6.2
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-6.3:End
