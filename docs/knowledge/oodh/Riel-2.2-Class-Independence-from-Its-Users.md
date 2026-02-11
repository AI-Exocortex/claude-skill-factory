## Riel-2.2 - Class Independence from Its Users

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Users of a class must be dependent on its public interface, but a class should not be dependent on its users."*

### Riel-2.2:1 - Problem Frame

A class exists to serve multiple consumers across potentially different contexts. If the class acquires knowledge of its users, it becomes entangled with their specific needs.

### Riel-2.2:2 - Problem

When a class depends on its users, it cannot be reused in a new context without dragging those user-specific dependencies along. The dependency direction is inverted, breaking modularity.

### Riel-2.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Reusability** | A class independent of its users can be reused freely vs. user-aware classes are locked to their context. |
| **Dependency direction** | Dependencies should flow from consumer to provider vs. bidirectional dependencies create cycles. |
| **Notification needs** | Sometimes a class must inform users of state changes vs. direct user knowledge violates independence. |

### Riel-2.2:4 - Solution

Ensure that the dependency arrow points from user to class, never the reverse. A class should define its public interface without any reference to who calls it. When notification is needed, use observer patterns or callback abstractions rather than hard-coding knowledge of specific consumers.

### Riel-2.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | An `AlarmClock` class provides `setAlarm()` and `getTime()` without knowing whether it is used by a `Person`, a `SchedulingSystem`, or a test harness. Notification is handled via a generic listener interface, not by referencing specific user classes. |
| **U.Episteme** | A `StatisticalModel` class exposes `fit()` and `predict()` without knowledge of whether it is called from a notebook, a pipeline, or a web service. Decoupling from consumers allows the model to be validated and reused across research and production contexts. |

### Riel-2.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Upward dependency** | A utility class imports and references its caller's types. | Prevents reuse; creates circular dependencies. | Invert the dependency; let the caller adapt to the utility's interface. |
| **Hard-coded callbacks** | A class calls specific user methods by name. | Ties the class to a single consumer. | Use an abstract listener or observer interface. |

### Riel-2.2:9 - Consequences

| Benefits |
|----------|
| Classes become reusable across contexts without modification. |
| Dependency graphs remain acyclic and comprehensible. |
| Testing is simplified because classes have no hidden external dependencies. |

| Trade-off | Mitigation |
|-----------|-----------|
| Observer complexity | Introducing observer patterns adds indirection; mitigated by well-known design patterns and framework support. |

### Riel-2.2:10 - Rationale

Unidirectional dependency is a prerequisite for reusability. A class that knows its users is, in effect, a private implementation detail of those users, not a reusable abstraction.

### Riel-2.2:11 - SoTA-Echoing

The Dependency Inversion Principle (Martin, 2003) formalizes this as: 'High-level modules should not depend on low-level modules; both should depend on abstractions.' Modern frameworks (Spring, Angular, SwiftUI) enforce this through dependency injection and protocol-oriented programming.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.2:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.3, Riel-2.4, Riel-2.5, Riel-2.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.2:End
