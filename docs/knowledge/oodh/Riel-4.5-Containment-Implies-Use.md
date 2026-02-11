## Riel-4.5 - Containment Implies Use

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"If a class contains objects of another class, then the containing class should be sending messages to the contained objects, that is, the containment relationship should always imply a uses relationship."*

### Riel-4.5:1 - Problem Frame

Containment (has-a) is one of the most common relationships in OO design. If a class contains another but never sends it messages, the containment is pointless.

### Riel-4.5:2 - Problem

A class that contains objects it never uses is carrying dead weight. The containment relationship consumes resources and adds complexity without providing behavior.

### Riel-4.5:3 - Forces

| Force | Tension |
|-------|---------|
| **Structural integrity** | Every containment should serve a purpose vs. speculative containment 'for later.' |
| **Data co-location** | Containing related objects is natural vs. unused containment wastes resources. |

### Riel-4.5:4 - Solution

For every containment relationship, verify that the containing class sends messages to the contained object. If not, either the containment is unnecessary, or behavior that should use the contained object has been misplaced elsewhere.

### Riel-4.5:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If a `Car` contains a `SpareTire` object but no method ever references it, either remove it or add the behavior that needs it. |
| **U.Episteme** | If a `Paper` object contains a `RawDataset` but never calls any of its methods, the containment is suspect. |

### Riel-4.5:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.5:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.5.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.5.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.5:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Dead containment** | A contained object is never sent any messages. | Dead weight; wasted resources; misleading design. | Remove the containment or add the missing behavior. |

### Riel-4.5:9 - Consequences

| Benefits |
|----------|
| Every containment relationship is justified by actual usage. |
| The design is lean. |

| Trade-off | Mitigation |
|-----------|-----------|
| Premature removal | Sometimes containment is needed in an upcoming feature; use design reviews to distinguish. |

### Riel-4.5:10 - Rationale

Containment without use is a structural lie. It implies a relationship that does not functionally exist.

### Riel-4.5:11 - SoTA-Echoing

Dead code elimination principles apply structurally: unused relationships are dead structure. Static analysis can flag contained objects with zero message sends.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.5:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.5:End
