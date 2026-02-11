## Riel-2.8 - One Key Abstraction Per Class

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"A class should capture one and only one key abstraction."*

### Riel-2.8:1 - Problem Frame

Key abstractions are the essential entities of a domain. When a single class tries to represent multiple distinct abstractions, it becomes a grab-bag of unrelated responsibilities.

### Riel-2.8:2 - Problem

A class capturing multiple abstractions has low cohesion, a large interface, and is difficult to name, understand, reuse, or maintain.

### Riel-2.8:3 - Forces

| Force | Tension |
|-------|---------|
| **Cohesion** | One abstraction per class maximizes cohesion vs. combining saves class count. |
| **Naming** | A single-purpose class has a clear name vs. a multi-purpose class resists naming. |
| **Reuse** | Focused classes are reusable vs. composite classes carry unwanted baggage. |

### Riel-2.8:4 - Solution

Ensure each class represents exactly one key domain abstraction. If a class is hard to name with a single noun, or if its methods cluster into groups that operate on separate subsets of its data, it should be split into multiple classes, one per abstraction.

### Riel-2.8:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A class that combines `Customer` and `Order` functionality should be split into separate `Customer` and `Order` classes, each with focused responsibilities. |
| **U.Episteme** | A class that combines `Experiment` metadata and `Dataset` storage should be separated, allowing each concept to be versioned and reused independently. |

### Riel-2.8:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.8:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.8.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.8.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.8:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Dual-purpose class** | A class models both 'account' and 'transaction' concepts. | Low cohesion, hard to name, hard to reuse. | Split into one class per key abstraction. |

### Riel-2.8:9 - Consequences

| Benefits |
|----------|
| Classes are easy to name, understand, and reuse. |
| Cohesion is maximized. |
| Changes to one abstraction do not affect unrelated ones. |

| Trade-off | Mitigation |
|-----------|-----------|
| More classes | Class count increases; mitigated by better comprehensibility and smaller per-class complexity. |

### Riel-2.8:10 - Rationale

A class is a named abstraction. If it conflates multiple abstractions, the name becomes a lie, and the implementation becomes a maintenance trap. One abstraction, one class, one clear name.

### Riel-2.8:11 - SoTA-Echoing

The Single Responsibility Principle (Martin, 2003) is the modern formalization. Domain-Driven Design (Evans, 2003) emphasizes modeling each domain concept as a distinct entity. Clean Architecture (Martin, 2017) reinforces focused, single-purpose components.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.8:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.8:End
