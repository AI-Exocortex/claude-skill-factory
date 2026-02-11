## Riel-3.2 - Avoid God Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Do not create god classes/objects in your system. Be very suspicious of a class whose name contains Driver, Manager, System, or Subsystem."*

### Riel-3.2:1 - Problem Frame

Large, central classes that control the entire system (god classes) are a common result of mapping procedural designs directly into OO structures.

### Riel-3.2:2 - Problem

God classes concentrate too much intelligence, becoming maintenance bottlenecks, testing nightmares, and single points of failure for understanding the system.

### Riel-3.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Centralization instinct** | A single controlling class feels organized vs. it becomes a monolith. |
| **Naming signals** | Names like 'Manager' or 'System' suggest excessive scope vs. sometimes coordination is needed. |

### Riel-3.2:4 - Solution

When a class's name contains 'Driver', 'Manager', 'System', or 'Subsystem', scrutinize it for god-class symptoms: too many methods, too many data members, too many collaborators. Redistribute its responsibilities to domain-appropriate classes.

### Riel-3.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `SystemManager` class controlling all aspects of a building's HVAC, lighting, and security should be decomposed into `HVACController`, `LightingController`, and `SecurityController`. |
| **U.Episteme** | A `ResearchManager` class that handles data collection, analysis, and publication should be split into focused classes for each concern. |

### Riel-3.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **God class** | One class has hundreds of methods and knows about every other class. | Unmaintainable monolith. | Apply Heuristic 3.1 to redistribute intelligence. |

### Riel-3.2:9 - Consequences

| Benefits |
|----------|
| No single class dominates the design. |
| Changes are localized. |

| Trade-off | Mitigation |
|-----------|-----------|
| More classes to manage | Offset by each class being simpler and more focused. |

### Riel-3.2:10 - Rationale

God classes negate the benefits of OO. They are procedural programs wearing a class costume. Eliminating them restores genuine object collaboration.

### Riel-3.2:11 - SoTA-Echoing

The God Class code smell (Fowler, 1999) is widely recognized. Static analysis tools (SonarQube, NDepend) flag classes exceeding cohesion and size thresholds.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.2:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.3, Riel-3.4, Riel-3.5, Riel-3.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.2:End
