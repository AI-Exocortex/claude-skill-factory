## Riel-3.7 - Eliminate Irrelevant Classes

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Eliminate irrelevant classes from your design."*

### Riel-3.7:1 - Problem Frame

During analysis, many candidate classes are identified. Some have no meaningful behavior within the system's domain and should not survive into design.

### Riel-3.7:2 - Problem

Irrelevant classes add complexity without value. They clutter the design, consume maintenance effort, and dilute the team's focus on essential abstractions.

### Riel-3.7:3 - Forces

| Force | Tension |
|-------|---------|
| **Completeness** | Capturing every domain noun feels thorough vs. not every noun is a meaningful abstraction. |
| **Simplicity** | Fewer classes reduce complexity vs. premature elimination may remove something needed later. |

### Riel-3.7:4 - Solution

Review candidate classes for meaningful behavior. A class with no behavior (only data) in the system domain is suspect. If it has no methods beyond accessors, either move its data into a related class or promote it by adding genuine behavior.

### Riel-3.7:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In a library system, `Book` has meaningful behavior; `Shelf` may be irrelevant if no behavior depends on shelf identity. |
| **U.Episteme** | In a research tracking system, `Citation` has meaningful behavior; `FontStyle` is irrelevant to the domain model. |

### Riel-3.7:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.7:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.7.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.7.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.7:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Noun-driven class proliferation** | Every noun from requirements becomes a class. | Many classes with no behavior. | Apply a behavior test: if a class has no meaningful methods, it should not exist. |

### Riel-3.7:9 - Consequences

| Benefits |
|----------|
| The design is leaner and more focused. |
| Maintenance cost is reduced. |

| Trade-off | Mitigation |
|-----------|-----------|
| Risk of under-modeling | May need to reintroduce classes later; cost is small compared to carrying unnecessary classes. |

### Riel-3.7:10 - Rationale

Every class in a design should earn its existence through meaningful behavior. A class without behavior is dead weight.

### Riel-3.7:11 - SoTA-Echoing

CRC cards (Beck & Cunningham, 1989) evaluate classes by their responsibilities. Responsibility-driven design explicitly filters for behavioral relevance.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.7:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.7:End
