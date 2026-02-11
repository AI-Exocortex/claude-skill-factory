## Riel-4.2 - Minimize Messages Between Collaborators

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"Minimize the number of message sends between a class and its collaborator."*

### Riel-4.2:1 - Problem Frame

Even when two classes must collaborate, the volume of messages between them should be kept low.

### Riel-4.2:2 - Problem

Excessive messaging between two classes indicates tight coupling in depth, not just breadth. It suggests that responsibilities may be misallocated.

### Riel-4.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Coupling depth** | Fewer messages reduce dependency depth vs. complex interactions may require many calls. |
| **Responsibility allocation** | Excessive messaging may signal misplaced behavior vs. some collaboration is inherently chatty. |

### Riel-4.2:4 - Solution

When the message count between two classes is high, consider moving some behavior from the caller to the callee (or vice versa) to reduce the interaction surface.

### Riel-4.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `OrderProcessor` sends 15 different messages to `Inventory`, some of that logic likely belongs inside `Inventory`. |
| **U.Episteme** | If a `ReportGenerator` sends many queries to a `DataStore`, consider adding higher-level query methods to `DataStore`. |

### Riel-4.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Chatty interface** | Many fine-grained calls between two classes. | High coupling depth; performance issues in distributed systems. | Consolidate into coarser-grained operations. |

### Riel-4.2:9 - Consequences

| Benefits |
|----------|
| Cleaner, more intentional collaboration. |

| Trade-off | Mitigation |
|-----------|-----------|
| Coarser methods | Higher-level methods may reduce flexibility; balance with actual usage patterns. |

### Riel-4.2:10 - Rationale

The number of messages is a proxy for coupling depth. Reducing it simplifies the contract between collaborators.

### Riel-4.2:11 - SoTA-Echoing

Fowler's 'Feature Envy' smell (1999/2018) signals methods that send too many messages to another class.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.2:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.3, Riel-4.4, Riel-4.5, Riel-4.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.2:End
