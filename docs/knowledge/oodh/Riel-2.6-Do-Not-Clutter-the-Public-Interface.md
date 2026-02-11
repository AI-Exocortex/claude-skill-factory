## Riel-2.6 - Do Not Clutter the Public Interface

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Do not clutter the public interface of a class with things that users of that class are not able to use or are not interested in using."*

### Riel-2.6:1 - Problem Frame

A class's public interface is its contract with the outside world. Including methods that users cannot meaningfully invoke or do not need creates noise and confusion.

### Riel-2.6:2 - Problem

A cluttered interface obscures the essential capabilities of a class, leading users to misuse irrelevant methods or overlook the important ones.

### Riel-2.6:3 - Forces

| Force | Tension |
|-------|---------|
| **Signal-to-noise ratio** | A clean interface highlights capabilities vs. clutter drowns them. |
| **User cognitive load** | Fewer options are easier to navigate vs. more options seem 'complete.' |

### Riel-2.6:4 - Solution

Audit the public interface from the user's perspective. Remove or hide any method that is not relevant to the user's interaction with the abstraction. Methods that exist for framework or infrastructure purposes should be separated into distinct interfaces if possible.

### Riel-2.6:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Button` UI class should not expose internal rendering-pipeline methods that only the framework's layout engine calls. Those belong on a separate, framework-internal interface. |
| **U.Episteme** | A `JournalArticle` class should not expose internal indexing hooks in its public API; those are relevant only to the search infrastructure, not to researchers reading the article. |

### Riel-2.6:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.6:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.6.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.6.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.6:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Infrastructure leak** | Framework hooks appear alongside user-facing methods. | Users are confused about what to call. | Use interface segregation to separate user and framework contracts. |

### Riel-2.6:9 - Consequences

| Benefits |
|----------|
| Users can quickly understand and correctly use the class. |
| The interface communicates intent clearly. |

| Trade-off | Mitigation |
|-----------|-----------|
| Multiple interfaces | Segregation requires more interface types; mitigated by clearer contracts. |

### Riel-2.6:10 - Rationale

An interface is a communication device. Noise in that device degrades understanding. Keeping it clean is an act of respect for the user's cognitive budget.

### Riel-2.6:11 - SoTA-Echoing

Interface Segregation (Martin, 2003) and API Usability research (Bloch, 'How to Design a Good API', 2006) both stress minimal, role-focused interfaces.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.6:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.6:End
