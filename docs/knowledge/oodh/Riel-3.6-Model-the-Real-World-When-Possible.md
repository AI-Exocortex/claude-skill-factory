## Riel-3.6 - Model the Real World When Possible

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Model the real world whenever possible. (This heuristic is often violated for reasons of system intelligence distribution, avoidance of god classes, and the keeping of related data and behavior in one place.)"*

### Riel-3.6:1 - Problem Frame

OO design often starts with domain modeling: mapping real-world entities to classes. However, blind fidelity to the real world can conflict with good design principles.

### Riel-3.6:2 - Problem

Modeling the real world naively may produce god classes (a 'company' class that does everything), misplaced intelligence, or violations of data-behavior co-location. Real-world structure is not always optimal software structure.

### Riel-3.6:3 - Forces

| Force | Tension |
|-------|---------|
| **Domain fidelity** | Real-world mapping aids understanding vs. real-world structures may have poor OO properties. |
| **Design quality** | Intelligence distribution overrides real-world mapping when they conflict. |

### Riel-3.6:4 - Solution

Start with real-world modeling for initial conceptualization, but be prepared to deviate when design heuristics (intelligence distribution, cohesion, coupling) demand it. Document where and why the software model departs from the domain model.

### Riel-3.6:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | In an ATM design, the real world has one 'ATM machine', but good design distributes its intelligence across `CardReader`, `Display`, `CashDispenser`, and `TransactionProcessor`. |
| **U.Episteme** | In modeling a university, the real-world hierarchy (University > College > Department) may need adjustment to avoid a god-class `University` that controls everything. |

### Riel-3.6:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.6:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.6.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.6.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.6:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Naive mapping** | Every real-world entity becomes a class regardless of cohesion. | God classes and anemic classes emerge. | Validate each class against cohesion and coupling heuristics. |

### Riel-3.6:9 - Consequences

| Benefits |
|----------|
| Initial design is intuitive and communicable. |
| Deviations are documented and justified. |

| Trade-off | Mitigation |
|-----------|-----------|
| Modeling divergence | Software model may not match domain mental model; mitigated by clear documentation. |

### Riel-3.6:10 - Rationale

The real world is a useful starting point, not a binding blueprint. Software design must satisfy engineering constraints that the real world does not face.

### Riel-3.6:11 - SoTA-Echoing

Domain-Driven Design (Evans, 2003) distinguishes between the 'domain model' and the 'implementation model', acknowledging necessary divergence. Bounded Contexts formalize this.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.6:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.6:End
