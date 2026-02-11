## Riel-4.14 - No Peer-to-Peer Uses Within a Container

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Objects that share lexical scope—those contained in the same containing class—should not have uses relationships between them."*

### Riel-4.14:1 - Problem Frame

When a container holds multiple objects, those sibling objects may be tempted to communicate directly with each other rather than through the container.

### Riel-4.14:2 - Problem

Direct uses relationships between siblings create hidden coupling that the container does not mediate, making the containment hierarchy harder to understand and refactor.

### Riel-4.14:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | The container should mediate all inter-part communication vs. direct sibling access is convenient. |
| **Transparency** | All relationships should be visible at the container level vs. hidden sibling coupling is invisible. |

### Riel-4.14:4 - Solution

Sibling objects within a container should communicate only through the container. If sibling A needs sibling B's services, the container should mediate the interaction.

### Riel-4.14:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Inside a `Computer`, the `CPU` should not directly access the `NetworkCard`. The `Motherboard` (container) mediates all inter-component communication. |
| **U.Episteme** | Within a `StudyProtocol`, the `DataCollection` component should not directly access `Analysis`. The protocol mediates. |

### Riel-4.14:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.14:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.14.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.14.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.14:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Sibling coupling** | Contained objects reference and call each other directly. | Hidden dependencies; container loses control. | Route all inter-part communication through the container. |

### Riel-4.14:9 - Consequences

| Benefits |
|----------|
| All dependencies are visible at the container level. |
| Parts are independently replaceable. |

| Trade-off | Mitigation |
|-----------|-----------|
| Container bottleneck | All mediation goes through the container; mitigated by keeping the container's mediating interface small and focused. |

### Riel-4.14:10 - Rationale

The container is the coordination authority for its parts. Allowing unsanctioned sibling communication undermines that authority and creates hidden coupling.

### Riel-4.14:11 - SoTA-Echoing

The Mediator pattern (GoF, 1994) formalizes container-mediated communication. Component architectures enforce parent-mediated data flow (React's 'lifting state up').

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.14:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.14:End
