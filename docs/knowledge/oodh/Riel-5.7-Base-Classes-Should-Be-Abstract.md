## Riel-5.7 - Base Classes Should Be Abstract

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"All base classes should be abstract classes."*

### Riel-5.7:1 - Problem Frame

If a base class is concrete, instances of the base class coexist with instances of its subclasses, raising questions about the base class's role.

### Riel-5.7:2 - Problem

Concrete base classes tempt developers to instantiate them when they should be choosing a more specific subclass. This weakens the type hierarchy's expressiveness.

### Riel-5.7:3 - Forces

| Force | Tension |
|-------|---------|
| **Hierarchy clarity** | Abstract bases force explicit specialization vs. concrete bases allow vague usage. |
| **Instantiation discipline** | Only leaves should be instantiable vs. sometimes a 'default' instance is useful. |

### Riel-5.7:4 - Solution

Make base classes abstract. Only leaf classes in the hierarchy should be concrete. If a 'default' implementation is needed, create a concrete `Default` subclass.

### Riel-5.7:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Shape` hierarchy should have abstract `Shape` as the root; `DefaultShape` can be a concrete leaf if a generic default is needed. |
| **U.Episteme** | A `Publication` base should be abstract; `GenericPublication` can serve as a concrete default if needed. |

### Riel-5.7:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.7:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.7.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.7.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.7:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Concrete root** | The root of an inheritance tree is concrete. | Ambiguous: is an instance of the root a valid entity or a design shortcut? | Make the root abstract; add an explicit default subclass if needed. |

### Riel-5.7:9 - Consequences

| Benefits |
|----------|
| The hierarchy is unambiguous: every concrete instance knows exactly what it is. |

| Trade-off | Mitigation |
|-----------|-----------|
| More classes | An explicit default subclass may be needed; a small cost for clarity. |

### Riel-5.7:10 - Rationale

Abstract bases enforce the discipline that every object must declare its specific type. This prevents the lazy pattern of using the base class as a catch-all.

### Riel-5.7:11 - SoTA-Echoing

Effective Java (Bloch, 2018) recommends designing for inheritance or prohibiting it. Sealed classes (Kotlin, Java 17+) provide a middle ground.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.7:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.7:End
