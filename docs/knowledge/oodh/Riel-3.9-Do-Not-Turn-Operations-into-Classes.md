## Riel-3.9 - Do Not Turn Operations into Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Do not turn an operation into a class. Be suspicious of any class whose name is a verb or is derived from a verb, especially those that have only one piece of meaningful behavior (i.e., do not count sets, gets, and prints). Ask if that piece of meaningful behavior needs to be migrated to some existing or undiscovered class."*

### Riel-3.9:1 - Problem Frame

During class identification, operations (verbs) are sometimes mistakenly elevated to class status, creating classes like `Validator` or `Calculator` that have only one meaningful method.

### Riel-3.9:2 - Problem

A verb-named class with a single behavior is likely a function masquerading as a class. It adds structural overhead without providing the benefits of a genuine abstraction.

### Riel-3.9:3 - Forces

| Force | Tension |
|-------|---------|
| **Abstraction integrity** | Classes should model things, not actions vs. some actions deserve reification (Strategy, Command). |
| **Design overhead** | A single-method class may be overkill vs. it provides polymorphic dispatch. |

### Riel-3.9:4 - Solution

When a candidate class is named after a verb, ask: does this operation belong on an existing class? Only if the operation needs to be treated polymorphically, queued, or undone should it be reified as a class (following Strategy or Command patterns).

### Riel-3.9:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Validator` class with only `validate(data)` should probably be a method on the `Data` class—unless multiple validation strategies need to be swapped at runtime. |
| **U.Episteme** | A `Calculator` class with only `calculate(formula)` should be a method on `Formula`—unless calculation strategies vary polymorphically. |

### Riel-3.9:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.9:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.9.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.9.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.9:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Verb class** | A class named after an action with one meaningful method. | Structural overhead without abstraction benefit. | Move the method to the class whose data it operates on. |

### Riel-3.9:9 - Consequences

| Benefits |
|----------|
| The design contains fewer artificial classes. |
| Behavior resides on the classes that own the relevant data. |

| Trade-off | Mitigation |
|-----------|-----------|
| Lost polymorphism | If the operation does need multiple strategies, it should be reified; the heuristic warns against doing so by default. |

### Riel-3.9:10 - Rationale

In OO, classes model nouns (abstractions) and methods model verbs (operations). Elevating a verb to a class is a category error unless polymorphism justifies it.

### Riel-3.9:11 - SoTA-Echoing

The Command and Strategy patterns (GoF, 1994) are the legitimate cases for reifying operations. Fowler's refactoring catalog addresses 'Move Method' for the common case.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.9:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.9:End
