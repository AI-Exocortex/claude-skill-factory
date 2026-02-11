## Riel-4.11 - Centralize Volatile Constraint Information

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"The semantic information on which a constraint is based is best placed in a central, third-party object when that information is volatile."*

### Riel-4.11:1 - Problem Frame

Some constraints depend on information that changes frequently, like business rules or configuration.

### Riel-4.11:2 - Problem

If volatile constraint information is scattered among the constrained classes, updating it requires touching many classes, increasing the risk of inconsistency.

### Riel-4.11:3 - Forces

| Force | Tension |
|-------|---------|
| **Change frequency** | Volatile information needs easy update vs. scattering it makes updates error-prone. |
| **Centralization** | A central source ensures consistency vs. it creates a dependency point. |

### Riel-4.11:4 - Solution

When constraint information is volatile, place it in a central third-party object (a configuration object, rule engine, or context) that all constrained classes consult. This allows constraint changes without modifying the constrained classes.

### Riel-4.11:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Tax rates (volatile) are best stored in a central `TaxConfiguration` object rather than hard-coded in `Invoice` and `Receipt` classes. |
| **U.Episteme** | Significance thresholds (which may vary by journal or field) are best stored in a central `StatisticalConfig` rather than in individual `Test` classes. |

### Riel-4.11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.11.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.11.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.11:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Scattered constants** | Volatile values are duplicated across classes. | Inconsistent updates; forgotten locations. | Centralize in a configuration object. |

### Riel-4.11:9 - Consequences

| Benefits |
|----------|
| Constraint changes are centralized and consistent. |
| Constrained classes are simpler. |

| Trade-off | Mitigation |
|-----------|-----------|
| Central dependency | All constrained classes depend on the central object; mitigated by a stable interface. |

### Riel-4.11:10 - Rationale

Volatile information should live where it can be changed once and propagated everywhere. Centralization achieves this.

### Riel-4.11:11 - SoTA-Echoing

Configuration management patterns, Feature Flags, and the Externalized Configuration pattern (Twelve-Factor App, 2012) all centralize volatile parameters.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.11:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.11:End
