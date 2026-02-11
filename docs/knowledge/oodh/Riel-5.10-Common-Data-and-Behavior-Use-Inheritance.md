## Riel-5.10 - Common Data and Behavior: Use Inheritance

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"If two or more classes have common data and behavior (i.e., methods), then those classes should each inherit from a common base class that captures those data and methods."*

### Riel-5.10:1 - Problem Frame

When classes share both data and behavior, inheritance is the appropriate mechanism to eliminate duplication.

### Riel-5.10:2 - Problem

Duplicated data and behavior across sibling classes is a clear signal that a common base class is missing.

### Riel-5.10:3 - Forces

| Force | Tension |
|-------|---------|
| **DRY** | Inheritance eliminates duplication of both data and behavior vs. adds a hierarchy level. |
| **Specialization** | Shared data+behavior constitutes a genuine common abstraction. |

### Riel-5.10:4 - Solution

Create a common base class that captures the shared data and behavior. Each original class inherits from this base, adding only its unique specializations.

### Riel-5.10:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | If `SavingsAccount` and `CheckingAccount` share balance data and `deposit()`/`withdraw()` behavior, create `BankAccount` as a common base. |
| **U.Episteme** | If `TTest` and `ZTest` share test-statistic data and `computePValue()` behavior, create `ParametricTest` as a common base. |

### Riel-5.10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.10.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.10.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.10:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Missed common base** | Sibling classes duplicate both data and behavior. | Maintenance burden; inconsistency risk. | Extract a common base class. |

### Riel-5.10:9 - Consequences

| Benefits |
|----------|
| Duplication eliminated. |
| The shared abstraction is named and documented. |

| Trade-off | Mitigation |
|-----------|-----------|
| Hierarchy depth | Adds one level; justified by eliminated duplication. |

### Riel-5.10:10 - Rationale

When both data and behavior are shared, the sharing classes genuinely specialize a common abstraction. Inheritance is the correct relationship.

### Riel-5.10:11 - SoTA-Echoing

Extract Superclass refactoring (Fowler, 1999/2018). This is the classic and uncontroversial use of inheritance.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.10:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.10:End
