## Riel-6.2 - Two Questions for Every Inheritance

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 6 — Multiple Inheritance
> **Chapter Theme:** Multiple inheritance validation and simplification

**Original Statement:** *"Whenever there is inheritance in an object-oriented design, ask yourself two questions: (1) Am I a special type of the thing from which I'm inheriting? (2) Is the thing from which I'm inheriting part of me?"*

### Riel-6.2:1 - Problem Frame

Inheritance (is-a) and containment (has-a) are frequently confused, especially when a class reuses another's code.

### Riel-6.2:2 - Problem

If the answer to question (2) is 'yes', then containment, not inheritance, is the correct relationship. Using inheritance when the relationship is really 'has-a' creates fragile, incorrect hierarchies.

### Riel-6.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Relationship accuracy** | The correct relationship prevents design errors vs. the wrong one creates cascading problems. |
| **Simple test** | Two questions provide a quick litmus test vs. nuanced domain analysis may complicate the answer. |

### Riel-6.2:4 - Solution

For every inheritance link, ask both questions. If 'is-a' is true and 'has-a' is false, keep inheritance. If 'has-a' is true, use containment. If both are ambiguous, default to containment.

### Riel-6.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Is a `Stack` a special type of `LinkedList`? No—it has a `LinkedList` as its implementation. Use containment. |
| **U.Episteme** | Is a `Thesis` a special type of `Bibliography`? No—it has a bibliography. Use containment. |

### Riel-6.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-6.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-6.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-6.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-6.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Inheritance for has-a** | Inheriting to reuse code when the relationship is containment. | Fragile hierarchy; inappropriate inherited methods. | Apply the two-question test; switch to containment. |

### Riel-6.2:9 - Consequences

| Benefits |
|----------|
| Every inheritance relationship is semantically correct. |
| Has-a relationships use containment. |

| Trade-off | Mitigation |
|-----------|-----------|
| Delegation overhead | Containment requires method forwarding; mitigated by language features and IDE support. |

### Riel-6.2:10 - Rationale

This two-question test is the simplest and most effective tool for preventing inheritance abuse.

### Riel-6.2:11 - SoTA-Echoing

Liskov Substitution Principle (1994). 'Composition over inheritance' (GoF, 1994; Effective Java, Bloch, 2018).

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-6.2:12 - Relations

* **Source:** Riel (1996), Chapter 6 — Multiple Inheritance
* **Sibling heuristics:** Riel-6.1, Riel-6.3
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-6.2:End
