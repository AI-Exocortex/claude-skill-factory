## Riel-4.9 - Prefer Class-Definition Constraints

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"When implementing semantic constraints, it is best to implement them in terms of the class definition. Often this will lead to a proliferation of classes, in which case the constraint must be implemented in the behavior of the class—usually, but not necessarily, in the constructor."*

### Riel-4.9:1 - Problem Frame

Semantic constraints (e.g., 'a meal must have an entree') can be enforced either structurally (through class definitions) or behaviorally (through runtime checks).

### Riel-4.9:2 - Problem

If semantic constraints are enforced only through runtime checks, they can be bypassed or forgotten. Structural enforcement through the type system is stronger but may require more classes.

### Riel-4.9:3 - Forces

| Force | Tension |
|-------|---------|
| **Compile-time safety** | Structural constraints are checked at compile time vs. they may proliferate classes. |
| **Runtime flexibility** | Behavioral constraints are flexible vs. they can be bypassed. |

### Riel-4.9:4 - Solution

Prefer encoding constraints in the class definition (type system). When this causes excessive class proliferation, fall back to constructor-enforced runtime checks as a pragmatic compromise.

### Riel-4.9:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A 'meal must have an entree' constraint is best modeled by requiring an `Entree` parameter in the `Meal` constructor, rather than a runtime check. |
| **U.Episteme** | A 'study must have a methodology' constraint is best enforced by requiring a `Methodology` object at `Study` construction time. |

### Riel-4.9:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.9:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.9.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.9.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.9:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Deferred validation** | Constraints are checked only at use time, not at construction. | Invalid objects circulate through the system. | Validate in the constructor or, better, in the type structure. |

### Riel-4.9:9 - Consequences

| Benefits |
|----------|
| Constraints are enforced early, ideally at compile time. |
| Invalid objects cannot be created. |

| Trade-off | Mitigation |
|-----------|-----------|
| Class proliferation | More types needed; mitigated by clearer, self-documenting code. |

### Riel-4.9:10 - Rationale

The type system is the most reliable constraint enforcer. When it falls short, the constructor is the next best checkpoint.

### Riel-4.9:11 - SoTA-Echoing

'Make illegal states unrepresentable' (Yaron Minsky, 2011) echoes this heuristic. Algebraic data types (Haskell, Rust, Kotlin sealed classes) provide powerful structural constraint tools.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.9:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.9:End
