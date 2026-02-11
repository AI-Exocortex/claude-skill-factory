## Riel-5.5 - Practical Hierarchy Depth Limit

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"In practice, inheritance hierarchies should be no deeper than an average person can keep in his or her short-term memory. A popular value for this depth is six."*

### Riel-5.5:1 - Problem Frame

While deep hierarchies are theoretically optimal, human cognitive limits constrain practical depth.

### Riel-5.5:2 - Problem

Hierarchies deeper than about six levels exceed most developers' ability to mentally trace the chain, leading to confusion and errors.

### Riel-5.5:3 - Forces

| Force | Tension |
|-------|---------|
| **Cognitive limits** | Short-term memory limits practical depth vs. deep hierarchies offer more reuse. |
| **Comprehensibility** | Shallow hierarchies are easier to understand vs. they may duplicate code. |

### Riel-5.5:4 - Solution

Keep inheritance hierarchies no deeper than approximately six levels. If domain complexity demands more, consider refactoring to use composition at intermediate levels.

### Riel-5.5:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A hierarchy of physical parts should not exceed six specialization levels; use containment to manage additional complexity. |
| **U.Episteme** | A taxonomy of research methods should not exceed six inheritance levels; use composition for cross-cutting concerns. |

### Riel-5.5:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.5:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.5.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.5.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.5:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Ultra-deep hierarchy** | More than six levels of inheritance. | Developers cannot mentally trace the chain. | Refactor deep branches to use composition. |

### Riel-5.5:9 - Consequences

| Benefits |
|----------|
| Hierarchies remain comprehensible. |

| Trade-off | Mitigation |
|-----------|-----------|
| Reduced reuse depth | Some theoretical reuse is sacrificed for comprehensibility; often the right trade-off. |

### Riel-5.5:10 - Rationale

This is the practical counterweight to Heuristic 5.4. Good design balances reuse with human cognitive capacity.

### Riel-5.5:11 - SoTA-Echoing

Miller's Law (1956). Studies on code comprehension confirm that very deep hierarchies degrade understanding (Daly et al., 1996).

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.5:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.5:End
