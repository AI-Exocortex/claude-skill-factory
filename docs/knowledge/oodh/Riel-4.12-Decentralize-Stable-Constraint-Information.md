## Riel-4.12 - Decentralize Stable Constraint Information

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 4 — The Relationships Between Classes and Objects
> **Chapter Theme:** Coupling, containment, collaboration, and semantic constraints

**Original Statement:** *"The semantic information on which a constraint is based is best decentralized among the classes involved in the constraint when that information is stable."*

### Riel-4.12:1 - Problem Frame

Not all constraint information is volatile. Some constraints are stable domain truths that rarely change.

### Riel-4.12:2 - Problem

Centralizing stable constraint information adds unnecessary indirection and a single point of failure without the benefit of easy changeability.

### Riel-4.12:3 - Forces

| Force | Tension |
|-------|---------|
| **Stability** | Stable information can safely live locally vs. over-centralization adds indirection. |
| **Self-containment** | Local information makes classes self-sufficient vs. external dependencies reduce autonomy. |

### Riel-4.12:4 - Solution

When constraint information is stable, embed it directly in the constrained classes. This makes each class self-sufficient and avoids unnecessary coupling to a central object.

### Riel-4.12:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | The constraint that a triangle has three sides is stable and belongs directly in the `Triangle` class, not in an external configuration. |
| **U.Episteme** | The constraint that a peer-reviewed paper requires at least two reviews is stable domain knowledge and belongs in the `ReviewProcess` class. |

### Riel-4.12:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-4.12:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-4.12.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-4.12.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-4.12:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Over-centralization** | Stable domain truths are placed in a central config. | Unnecessary indirection; fragile dependency on external object. | Embed stable constraints locally. |

### Riel-4.12:9 - Consequences

| Benefits |
|----------|
| Classes are self-contained. |
| No unnecessary coupling. |

| Trade-off | Mitigation |
|-----------|-----------|
| Change risk | If a 'stable' constraint changes, multiple classes need updating; mitigated by the rarity of such changes. |

### Riel-4.12:10 - Rationale

The volatile/stable distinction determines the optimal placement. Stable constraints belong with the classes they govern; volatile ones belong centrally. This is a complementary pair with Heuristic 4.11.

### Riel-4.12:11 - SoTA-Echoing

The distinction between volatile and stable dependencies is central to the Stable Dependencies Principle (Martin, 2003).

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-4.12:12 - Relations

* **Source:** Riel (1996), Chapter 4 — The Relationships Between Classes and Objects
* **Sibling heuristics:** Riel-4.1, Riel-4.2, Riel-4.3, Riel-4.4, Riel-4.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-4.12:End
