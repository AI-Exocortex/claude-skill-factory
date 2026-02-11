## Riel-9.1 - Logical Design Integrity over Physical Criteria

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 9 — Physical Object-Oriented Design
> **Chapter Theme:** Logical versus physical design integrity

**Original Statement:** *"Object-oriented designers should not allow physical design criteria to corrupt their logical designs. However, physical design criteria are often used in the decision-making process at logical design time."*

### Riel-9.1:1 - Problem Frame

Logical design models the domain correctly. Physical design addresses performance, memory, distribution, and other implementation concerns.

### Riel-9.1:2 - Problem

When physical concerns (performance optimization, memory layout, network boundaries) drive the logical design, the result is a corrupted model that is hard to understand, maintain, and evolve.

### Riel-9.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Logical purity** | A clean domain model vs. physical constraints are real. |
| **Performance** | Optimizations may require structural changes vs. premature optimization corrupts design. |
| **Pragmatism** | Physical constraints must eventually be addressed vs. they should not distort the model. |

### Riel-9.1:4 - Solution

Design the logical model first, driven by domain correctness. Then address physical concerns as a separate layer of decisions, clearly documented and separated from the logical design. If physical criteria influence logical decisions, document the trade-off explicitly.

### Riel-9.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `DistributedCache` may physically replicate data, but the logical model should still present a single coherent cache abstraction. |
| **U.Episteme** | A `LargeDataset` may be physically partitioned across files, but the logical model should present unified query access. |

### Riel-9.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-9.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-9.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-9.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-9.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Performance-driven distortion** | The logical model is warped to satisfy premature performance concerns. | Incomprehensible model; maintenance nightmare. | Separate logical and physical design; optimize the physical layer. |

### Riel-9.1:9 - Consequences

| Benefits |
|----------|
| The logical model remains clean and comprehensible. |
| Physical optimizations are localized and documented. |

| Trade-off | Mitigation |
|-----------|-----------|
| Two-layer thinking | Requires discipline to maintain separation; mitigated by clear architectural boundaries. |

### Riel-9.1:10 - Rationale

Logical integrity is the foundation. Physical optimization is a derived concern. Allowing the derivative to corrupt the foundation inverts the design priority.

### Riel-9.1:11 - SoTA-Echoing

Clean Architecture (Martin, 2017) and Hexagonal Architecture (Cockburn, 2005) enforce the separation of domain logic from infrastructure concerns.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-9.1:12 - Relations

* **Source:** Riel (1996), Chapter 9 — Physical Object-Oriented Design
* **Sibling heuristics:** Riel-9.2
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-9.1:End
