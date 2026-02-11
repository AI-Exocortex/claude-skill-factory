## Riel-8.1 - No Global Data for Class Bookkeeping

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 8 — Class-Specific Data and Behavior
> **Chapter Theme:** Class-level (static) versus instance-level responsibilities

**Original Statement:** *"Do not use global data or functions to perform bookkeeping information on the objects of a class. Class variables or methods should be used instead."*

### Riel-8.1:1 - Problem Frame

Tracking class-level information (e.g., instance count, shared configuration) is sometimes done via global variables or free functions.

### Riel-8.1:2 - Problem

Global data couples the bookkeeping to the global namespace, breaking encapsulation and making the class non-self-contained. It also prevents having multiple independent instance populations.

### Riel-8.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | Class-level data belongs in the class vs. global data is accessible and modifiable by anyone. |
| **Self-containment** | A class should manage its own bookkeeping vs. external globals fragment responsibility. |

### Riel-8.1:4 - Solution

Use class variables (static members) and class methods (static methods) to manage class-level bookkeeping. This keeps the information encapsulated within the class and accessible through a controlled interface.

### Riel-8.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Tracking the number of `Connection` instances should use a `Connection.count` class variable, not a global `connectionCount`. |
| **U.Episteme** | Tracking the number of `Experiment` instances should use `Experiment.instanceCount`, not a global variable. |

### Riel-8.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-8.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-8.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-8.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-8.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Global counter** | A global variable tracks instances of a class. | Any code can corrupt the count; breaks encapsulation. | Move to a class variable with class methods for access. |

### Riel-8.1:9 - Consequences

| Benefits |
|----------|
| Class-level data is encapsulated. |
| Multiple independent populations are possible. |

| Trade-off | Mitigation |
|-----------|-----------|
| Static state caution | Class variables introduce shared mutable state; mitigated by careful access control and thread safety. |

### Riel-8.1:10 - Rationale

The class is the natural home for class-level data. Placing it globally breaks the self-containment that makes OO modular.

### Riel-8.1:11 - SoTA-Echoing

Static members are standard in all major OO languages. The Singleton pattern (GoF, 1994) and class-level factory methods demonstrate proper use. Modern concerns about static state and testability suggest additional patterns like dependency injection.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-8.1:12 - Relations

* **Source:** Riel (1996), Chapter 8 — Class-Specific Data and Behavior
* **Sibling heuristics:** None in the same chapter
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-8.1:End
