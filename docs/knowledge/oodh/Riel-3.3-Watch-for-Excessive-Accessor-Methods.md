## Riel-3.3 - Watch for Excessive Accessor Methods

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
> **Chapter Theme:** System intelligence distribution and god-class avoidance

**Original Statement:** *"Beware of classes that have many accessor methods defined in their public interface. Having many implies that related data and behavior are not being kept in one place."*

### Riel-3.3:1 - Problem Frame

A class with many getters and setters suggests it is a data container whose behavior has leaked elsewhere.

### Riel-3.3:2 - Problem

Excessive accessors signal that other classes are pulling data out and operating on it externally, violating co-location of data and behavior.

### Riel-3.3:3 - Forces

| Force | Tension |
|-------|---------|
| **Data exposure** | Accessors provide controlled access vs. many accessors imply data-driven external logic. |
| **Anemic design** | Trivial accessors avoid logic in the class vs. they punt behavior to callers. |

### Riel-3.3:4 - Solution

When a class has many accessors, ask where the behavior that uses that data lives. Move the behavior into the class and eliminate the now-unnecessary accessors. The class should offer behavior, not data.

### Riel-3.3:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Sensor` class with getters for raw voltage, calibration offset, and unit type should instead provide `getReading()` that encapsulates the calculation. |
| **U.Episteme** | A `SurveyResult` class with getters for every raw field should instead provide analytical methods like `calculateScore()` and `isFlagged()`. |

### Riel-3.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-3.3:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-3.3.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-3.3.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-3.3:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Getter parade** | Every field has a public getter; behavior lives elsewhere. | Procedural code disguised as OO. | Replace getters with meaningful behavioral methods. |

### Riel-3.3:9 - Consequences

| Benefits |
|----------|
| Behavior moves to where the data lives. |
| The public interface becomes behavioral, not structural. |

| Trade-off | Mitigation |
|-----------|-----------|
| Framework requirements | Some frameworks require getters; mitigated by limiting them to framework-facing interfaces. |

### Riel-3.3:10 - Rationale

Accessors are a necessary evil, not a design goal. A class whose interface is dominated by them has failed to encapsulate its behavior.

### Riel-3.3:11 - SoTA-Echoing

The 'Feature Envy' and 'Data Class' code smells (Fowler, 1999/2018) capture this heuristic. The 'Tell, Don't Ask' principle (Hunt & Thomas, 1999) provides the corrective.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-3.3:12 - Relations

* **Source:** Riel (1996), Chapter 3 — Topologies of Action-Oriented Versus Object-Oriented Applications
* **Sibling heuristics:** Riel-3.1, Riel-3.2, Riel-3.4, Riel-3.5, Riel-3.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-3.3:End
