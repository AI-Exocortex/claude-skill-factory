## Riel-4.10 - Push Constraints Down Containment Hierarchies

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"When implementing semantic constraints in the constructor of a class, place the constraint test in the constructor as far down a containment hierarchy as the domain allows."*

### Riel-4.10:1 - Problem Frame

When constraints must be checked at runtime, the question is where in the containment hierarchy to place the check.

### Riel-4.10:2 - Problem

Placing constraint checks too high in the hierarchy means the containing class knows too much about its parts' invariants, violating encapsulation and making reuse difficult.

### Riel-4.10:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Each class should enforce its own constraints vs. some constraints span multiple objects. |
| **Localization** | Lower placement keeps knowledge local vs. domain rules may transcend individual parts. |

### Riel-4.10:4 - Solution

Place each constraint check in the constructor of the most deeply nested class that has sufficient information to evaluate it. Only elevate to a higher level when the constraint genuinely spans multiple contained objects.

### Riel-4.10:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A constraint that 'a cylinder must have a positive radius' belongs in `Cylinder`'s constructor, not in `Engine`'s, even though `Engine` contains `Cylinder`. |
| **U.Episteme** | A constraint that 'a measurement must have a positive uncertainty' belongs in `Measurement`'s constructor, not in `Experiment`'s. |

### Riel-4.10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.10.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.10.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.10:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Over-elevated constraint** | A containing class validates its parts' internal invariants. | Breaks encapsulation; contained classes cannot be reused independently. | Move the check into the contained class's constructor. |

### Riel-4.10:9 - Consequences

| Benefits |
|----------|
| Each class is self-validating. |
| Reuse is not hindered by external constraint checks. |

| Trade-off | Mitigation |
|-----------|-----------|
| Cross-object constraints | Some constraints genuinely require a higher-level coordinator; this is the exception, not the rule. |

### Riel-4.10:10 - Rationale

Pushing constraints down is an application of encapsulation: each class should be the guardian of its own invariants.

### Riel-4.10:11 - SoTA-Echoing

Domain-Driven Design's Aggregate pattern (Evans, 2003) localizes invariant enforcement within aggregate boundaries.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.10:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.10:End
