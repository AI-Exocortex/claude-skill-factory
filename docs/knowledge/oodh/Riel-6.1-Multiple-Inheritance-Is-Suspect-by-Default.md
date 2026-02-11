## Riel-6.1 - Multiple Inheritance Is Suspect by Default

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 6 — Multiple Inheritance
> **Chapter Theme:** Multiple inheritance validation and simplification

**Original Statement:** *"If you have an example of multiple inheritance in your design, assume you have made a mistake and then prove otherwise."*

### Riel-6.1:1 - Problem Frame

Multiple inheritance (MI) introduces significant complexity: diamond problems, ambiguous method resolution, and tight coupling to multiple base classes.

### Riel-6.1:2 - Problem

MI is often used when containment or interface implementation would be more appropriate. The complexity cost is high and the design benefits are rarely worth it.

### Riel-6.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Expressiveness** | MI can model genuine multi-typed entities vs. it introduces resolution ambiguity. |
| **Simplicity** | Single inheritance is simpler to reason about vs. MI handles rare cross-cutting cases. |

### Riel-6.1:4 - Solution

Treat every MI use as guilty until proven innocent. For each case, verify that (1) the entity genuinely 'is-a' each base class, and (2) neither containment nor interface implementation can express the relationship. Only keep MI that survives both tests.

### Riel-6.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `FlyingCar` that inherits from both `Car` and `Aircraft` should be scrutinized. Is it truly both? Or does it contain flight and driving capabilities? |
| **U.Episteme** | A `ReviewArticle` inheriting from both `SurveyPaper` and `OriginalResearch` should be questioned: is it genuinely both, or is one aspect contained? |

### Riel-6.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-6.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-6.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-6.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-6.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Lazy MI** | MI used for convenience rather than genuine multi-typing. | Diamond problems; ambiguous resolution; tight coupling. | Replace with containment or interface implementation. |

### Riel-6.1:9 - Consequences

| Benefits |
|----------|
| MI is used only where genuinely necessary. |
| Designs are simpler. |

| Trade-off | Mitigation |
|-----------|-----------|
| Expressiveness loss | Some rare genuine MI cases exist; the heuristic ensures they are justified. |

### Riel-6.1:10 - Rationale

MI has a very high complexity-to-benefit ratio. The burden of proof should be on its inclusion, not its exclusion.

### Riel-6.1:11 - SoTA-Echoing

Many modern languages (Java, C#, Swift, Kotlin) prohibit class-level MI, allowing only interface MI. This is a language-level enforcement of this heuristic.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-6.1:12 - Relations

* **Source:** Riel (1996), Chapter 6 — Multiple Inheritance
* **Sibling heuristics:** Riel-6.2, Riel-6.3
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-6.1:End
