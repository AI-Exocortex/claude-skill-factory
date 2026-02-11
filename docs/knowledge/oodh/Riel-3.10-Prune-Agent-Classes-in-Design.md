## Riel-3.10 - Prune Agent Classes in Design

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Agent classes are often placed in the analysis model of an application. During design time, many agents are found to be irrelevant and should be removed."*

### Riel-3.10:1 - Problem Frame

Analysis models often include 'agent' classes that orchestrate behavior between domain objects. During design, many of these agents are found to add no value.

### Riel-3.10:2 - Problem

Agent classes that merely pass messages between domain objects are middlemen that add complexity without intelligence. Their responsibilities typically belong on the domain objects themselves.

### Riel-3.10:3 - Forces

| Force | Tension |
|-------|---------|
| **Analysis fidelity** | Agents model real-world coordinators vs. they may not translate to useful software abstractions. |
| **Indirection cost** | Agents add layers of indirection vs. direct collaboration is simpler. |

### Riel-3.10:4 - Solution

During the transition from analysis to design, scrutinize every agent class. If it merely delegates to domain objects without adding intelligence, remove it and let the domain objects collaborate directly.

### Riel-3.10:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | An `OrderProcessor` agent that simply calls methods on `Order`, `Inventory`, and `Payment` in sequence can often be eliminated by letting these objects collaborate directly. |
| **U.Episteme** | A `PipelineManager` agent that merely invokes stages in order can be replaced by direct stage-to-stage collaboration or a simple composition mechanism. |

### Riel-3.10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.10.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.10.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.10:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Middleman** | An agent class that only delegates. | Adds indirection without intelligence. | Eliminate the agent; let collaborators interact directly. |

### Riel-3.10:9 - Consequences

| Benefits |
|----------|
| Fewer unnecessary classes. |
| Simpler interaction paths. |

| Trade-off | Mitigation |
|-----------|-----------|
| Lost coordination point | Sometimes a coordinator is genuinely needed; the heuristic says to scrutinize, not blindly remove. |

### Riel-3.10:10 - Rationale

Agents that survive from analysis to design should justify their existence by adding genuine coordination intelligence, not mere delegation.

### Riel-3.10:11 - SoTA-Echoing

Fowler's 'Middle Man' code smell (1999/2018) captures this. The Mediator pattern (GoF, 1994) is the legitimate form of a coordination class.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.10:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.10:End
