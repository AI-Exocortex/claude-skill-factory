## Riel-3.1 - Distribute Intelligence Horizontally

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Distribute system intelligence horizontally as uniformly as possible, that is, the top-level classes in a design should share the work uniformly."*

### Riel-3.1:1 - Problem Frame

In action-oriented designs, intelligence concentrates in a few controlling routines. OO design should distribute it across collaborating objects, but designers often replicate the centralized pattern.

### Riel-3.1:2 - Problem

When system intelligence is concentrated in a few classes, those classes become god classes that are hard to understand, maintain, and test, while the remaining classes are anemic shells.

### Riel-3.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Uniformity** | Even distribution simplifies each class vs. some problems have natural coordinators. |
| **Comprehensibility** | Smaller, focused classes are easier to understand vs. coordination logic must live somewhere. |

### Riel-3.1:4 - Solution

Ensure that top-level classes share behavioral responsibility roughly evenly. If one class is significantly larger or more complex than its peers, redistribute its responsibilities. Use metrics like lines of code and method count as heuristic indicators.

### Riel-3.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In an ATM system, the `ATM` class should not contain all transaction logic. Instead, `Account`, `Transaction`, `CardReader`, and `Display` should each handle their own responsibilities. |
| **U.Episteme** | In a research pipeline, the orchestrator should not contain all analysis logic. Each stage (`DataLoader`, `Preprocessor`, `Analyzer`, `Reporter`) handles its own concern. |

### Riel-3.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Central controller** | One class orchestrates everything; others are data holders. | The controller becomes unmaintainable; others are not reusable. | Move behavior to the classes that own the relevant data. |

### Riel-3.1:9 - Consequences

| Benefits |
|----------|
| Each class is manageable in size. |
| Parallel development is feasible. |

| Trade-off | Mitigation |
|-----------|-----------|
| Coordination overhead | More inter-class messaging; mitigated by well-defined interfaces. |

### Riel-3.1:10 - Rationale

Uniform distribution is the OO antidote to procedural main-loop thinking. It ensures that each class earns its existence through meaningful behavior.

### Riel-3.1:11 - SoTA-Echoing

GRASP's Information Expert principle (Larman, 2004) assigns responsibility to the class with the data. Microservice architectures apply the same principle at the service level.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.1:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5, Riel-3.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.1:End
