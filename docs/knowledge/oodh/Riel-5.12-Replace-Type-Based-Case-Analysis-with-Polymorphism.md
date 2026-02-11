## Riel-5.12 - Replace Type-Based Case Analysis with Polymorphism

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 5 — The Inheritance Relationship
> **Chapter Theme:** Inheritance hierarchies, polymorphism, and specialization

**Original Statement:** *"Explicit case analysis on the type of an object is usually an error. The designer should use polymorphism in most of these cases."*

### Riel-5.12:1 - Problem Frame

Code that branches on an object's type (using instanceof, typeid, or similar) is a procedural pattern in an OO system.

### Riel-5.12:2 - Problem

Type-based case analysis defeats polymorphism, creates maintenance hotspots, and forces modifications every time a new type is added.

### Riel-5.12:3 - Forces

| Force | Tension |
|-------|---------|
| **Open/Closed** | Polymorphism allows extension without modification vs. case analysis requires modification for each new type. |
| **Encapsulation** | Polymorphism keeps type-specific logic in the type vs. case analysis externalizes it. |

### Riel-5.12:4 - Solution

Replace type-based conditionals with polymorphic method dispatch. Each type handles its own case through an overridden method.

### Riel-5.12:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Instead of `if (shape instanceof Circle) ... else if (shape instanceof Rectangle) ...`, define `shape.draw()` where each subclass implements its own drawing. |
| **U.Episteme** | Instead of `if (test instanceof TTest) ... else if (test instanceof ANOVA) ...`, define `test.compute()` polymorphically. |

### Riel-5.12:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-5.12:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-5.12.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-5.12.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-5.12:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Type switch** | A method uses instanceof/typeid to branch on subtypes. | Every new subtype requires modification; violates Open/Closed. | Use polymorphic dispatch. |

### Riel-5.12:9 - Consequences

| Benefits |
|----------|
| New types can be added without modifying existing code. |
| Type-specific logic is encapsulated in each type. |

| Trade-off | Mitigation |
|-----------|-----------|
| Visitor pattern need | Sometimes type-based dispatch is needed for operations across types; use the Visitor pattern. |

### Riel-5.12:10 - Rationale

Polymorphism is the core mechanism of OO. Type-based case analysis bypasses it and regresses to procedural control flow.

### Riel-5.12:11 - SoTA-Echoing

Replace Conditional with Polymorphism (Fowler, 1999/2018). Pattern matching in modern languages (Kotlin, Scala, Rust) provides a safer alternative when polymorphism is impractical.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-5.12:12 - Relations

* **Source:** Riel (1996), Chapter 5 — The Inheritance Relationship
* **Sibling heuristics:** Riel-5.1, Riel-5.2, Riel-5.3, Riel-5.4, Riel-5.5
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-5.12:End
