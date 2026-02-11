## Riel-3.8 - Eliminate Outside-System Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Eliminate classes that are outside the system."*

### Riel-3.8:1 - Problem Frame

Domain analysis may identify entities that exist in the broader domain but lie outside the system boundary.

### Riel-3.8:2 - Problem

Including classes that are outside the system boundary adds complexity without utility. They represent actors or external entities, not internal abstractions.

### Riel-3.8:3 - Forces

| Force | Tension |
|-------|---------|
| **Scope clarity** | Including only in-scope classes keeps the system focused vs. external entities may seem important. |
| **Interface modeling** | External entities influence the system's interfaces vs. they should not be modeled as internal classes. |

### Riel-3.8:4 - Solution

Identify the system boundary clearly. Entities that exist outside this boundary (e.g., users, external systems) should be represented only at the boundary as interfaces or stubs, not as full internal classes.

### Riel-3.8:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In a banking application, `RegulatingAuthority` is outside the system. It should appear only as an interface at the boundary, not as an internal domain class. |
| **U.Episteme** | In a lab information management system, `JournalPublisher` is an external entity; it should be modeled as an external interface, not an internal class. |

### Riel-3.8:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.8:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.8.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.8.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.8:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **External entity internalization** | An external actor is modeled as a full internal class with behavior. | The design over-reaches; maintains fiction of control over external entities. | Model external entities as boundary interfaces. |

### Riel-3.8:9 - Consequences

| Benefits |
|----------|
| The system boundary is clear. |
| Internal classes represent genuine internal abstractions. |

| Trade-off | Mitigation |
|-----------|-----------|
| Boundary complexity | Interfaces to external entities need careful design; mitigated by established integration patterns. |

### Riel-3.8:10 - Rationale

A system's scope is defined by its boundary. Classes that live outside that boundary dilute the design and misrepresent the system's responsibilities.

### Riel-3.8:11 - SoTA-Echoing

Context Mapping in DDD (Evans, 2003) and the Hexagonal Architecture (Cockburn, 2005) formalize the boundary between internal domain and external actors.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.8:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.8:End
