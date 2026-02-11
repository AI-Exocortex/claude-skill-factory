## Riel-3.5 - Model-Interface Separation

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"In applications that consist of an object-oriented model interacting with a user interface, the model should never be dependent on the interface. The interface should be dependent on the model."*

### Riel-3.5:1 - Problem Frame

Applications typically have a domain model and a user interface. The dependency direction between them determines the model's reusability and testability.

### Riel-3.5:2 - Problem

When the model depends on the interface, the model cannot be reused with a different interface, tested independently, or reasoned about without UI knowledge.

### Riel-3.5:3 - Forces

| Force | Tension |
|-------|---------|
| **Reusability** | An interface-independent model is reusable vs. UI-aware models are locked to one presentation. |
| **Testability** | An independent model is testable in isolation vs. UI-dependent models require UI simulation. |
| **Dependency direction** | Models should be stable; UIs change frequently vs. convenience of direct model-to-UI calls. |

### Riel-3.5:4 - Solution

Ensure the dependency arrow points from the interface to the model, never the reverse. The model should have no imports, references, or knowledge of UI classes. Use observer patterns or event systems if the model needs to notify the UI of state changes.

### Riel-3.5:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | An ATM's domain model (`Account`, `Transaction`) should be fully functional without any reference to `Screen` or `CardReader` UI classes. |
| **U.Episteme** | A statistical analysis model should produce results without knowledge of whether they will be displayed in a notebook, a PDF, or a dashboard. |

### Riel-3.5:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.5:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.5.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.5.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.5:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Model-to-UI callback** | The model directly calls UI update methods. | Model cannot be tested without UI; cannot be reused. | Use observer pattern or event bus. |

### Riel-3.5:9 - Consequences

| Benefits |
|----------|
| The model is reusable across multiple UIs. |
| Testing the model requires no UI infrastructure. |

| Trade-off | Mitigation |
|-----------|-----------|
| Indirection cost | Observer/event mechanisms add complexity; mitigated by frameworks (MVC, MVVM, React). |

### Riel-3.5:10 - Rationale

The model embodies the stable domain logic; the interface embodies the volatile presentation logic. Dependency should flow from volatile to stable.

### Riel-3.5:11 - SoTA-Echoing

MVC (Reenskaug, 1979), MVP, MVVM, and Clean Architecture all enforce this separation. Modern frameworks (React, SwiftUI, Jetpack Compose) build it into their architecture.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.5:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.3, Riel-3.4, Riel-3.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.5:End
