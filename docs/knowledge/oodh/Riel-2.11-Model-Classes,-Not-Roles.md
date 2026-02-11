## Riel-2.11 - Model Classes, Not Roles

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Be sure the abstractions that you model are classes and not simply the roles objects play."*

### Riel-2.11:1 - Problem Frame

In domain modeling, it is tempting to create classes for every noun, including roles that objects temporarily assume. A `Mother` is not a separate kind of being from a `Person`; it is a role a `Person` plays.

### Riel-2.11:2 - Problem

Modeling roles as classes leads to type-switching at runtime (a `Person` cannot become a `Mother` without changing class) and an explosion of artificial inheritance hierarchies.

### Riel-2.11:3 - Forces

| Force | Tension |
|-------|---------|
| **Domain fidelity** | Roles feel like distinct types in natural language vs. they are dynamic and context-dependent. |
| **Runtime flexibility** | Role-based modeling allows dynamic assignment vs. class-based modeling is static. |

### Riel-2.11:4 - Solution

Distinguish between enduring identity (the class) and transient behavior (the role). Model the enduring identity as a class and the role as a property, contained role object, or strategy pattern that can be attached and detached dynamically.

### Riel-2.11:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | `Person` is a class; `Mother`, `Employee`, `Customer` are roles a `Person` object may hold at different times. Model them as role objects or flags, not as subclasses. |
| **U.Episteme** | `Researcher` is a role a `Person` plays within an `Institution`. The same person may also play `Reviewer` and `Author` roles. These are not separate classes but contextual assignments. |

### Riel-2.11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.11.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.11.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.11:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Role-as-subclass** | Every role becomes a subclass of the base entity. | Objects cannot change roles without changing class; combinatorial explosion of subclasses. | Use composition or the Role Object pattern. |

### Riel-2.11:9 - Consequences

| Benefits |
|----------|
| Objects can assume and relinquish roles dynamically. |
| The class hierarchy reflects genuine specialization, not transient behavior. |

| Trade-off | Mitigation |
|-----------|-----------|
| Design complexity | Role-object patterns are more complex than simple subclassing; mitigated by avoiding the far worse problems of static role hierarchies. |

### Riel-2.11:10 - Rationale

Classes model what something *is*; roles model what something *does* in a context. Confusing these categories leads to rigid designs that fight against the dynamic nature of domains.

### Riel-2.11:11 - SoTA-Echoing

The Role Object pattern (Bäumer et al., 1997) and the DCI architecture (Reenskaug & Coplien, 2009) provide formal solutions. Modern entity-component-system (ECS) architectures in game development take this further by fully decomposing identity from behavior.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.11:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.11:End
