## Riel-2.4 - Implement a Minimal Universal Public Interface

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Implement a minimal public interface that all classes understand [e.g., operations such as copy (deep versus shallow), equality testing, pretty printing, parsing from an ASCII description, etc.]."*

### Riel-2.4:1 - Problem Frame

In any object-oriented system, there are common operations that nearly every object should support: copying, comparison, display, and serialization. Without a shared minimal interface, each class invents its own conventions.

### Riel-2.4:2 - Problem

Absence of a universal minimal interface forces users to learn ad-hoc conventions per class and prevents generic algorithms from operating uniformly across objects.

### Riel-2.4:3 - Forces

| Force | Tension |
|-------|---------|
| **Uniformity** | A common interface enables generic programming vs. forcing it on all classes adds boilerplate. |
| **Semantic correctness** | Default implementations may be wrong (e.g., shallow vs. deep copy) vs. no default leaves gaps. |
| **Framework integration** | Collections and frameworks rely on equality, hashing, and display vs. missing implementations cause subtle bugs. |

### Riel-2.4:4 - Solution

Define a minimal set of universal operations (equality, copy, string representation, hashing) that all classes in the system implement. Make conscious decisions about deep versus shallow semantics for each class. Language-level mechanisms (e.g., Java's `Object` methods, Python's dunder methods) provide the hook; the designer must ensure each class overrides them meaningfully.

### Riel-2.4:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Every domain entity in an enterprise system implements `equals()`, `hashCode()`, and `toString()`. This enables uniform use in collections, logging, and debugging. |
| **U.Episteme** | Every model artifact in a research pipeline implements serialization and equality testing, enabling reproducible comparison of experimental results. |

### Riel-2.4:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.4:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.4.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.4.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.4:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Inherited defaults** | Relying on language-default equality (identity) when value equality is needed. | Collections and tests behave incorrectly. | Override equality and hashing for every value-carrying class. |

### Riel-2.4:9 - Consequences

| Benefits |
|----------|
| Generic algorithms and collections work correctly across all classes. |
| Debugging and logging produce meaningful output. |
| Copy semantics are explicit and intentional. |

| Trade-off | Mitigation |
|-----------|-----------|
| Implementation overhead | Every class must implement these methods; mitigated by IDE generation and language features like `record` types. |

### Riel-2.4:10 - Rationale

A universal minimal interface creates a shared behavioral floor that enables polymorphic use of objects in generic contexts, from collections to serialization frameworks.

### Riel-2.4:11 - SoTA-Echoing

Java's `Object` class, Python's dunder protocol, Rust's `Debug`/`Clone`/`PartialEq` traits, and Kotlin's `data class` all formalize a minimal universal interface. Effective Java (Bloch, 2018) devotes multiple items to correct `equals`/`hashCode` implementation.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.4:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.3, Riel-2.5, Riel-2.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.4:End
