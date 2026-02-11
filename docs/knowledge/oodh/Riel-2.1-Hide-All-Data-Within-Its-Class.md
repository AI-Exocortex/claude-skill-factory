## Riel-2.1 - Hide All Data Within Its Class

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"All data should be hidden within its class."*

### Riel-2.1:1 - Problem Frame

Object-oriented systems are built from classes that encapsulate both data and behavior. When data members are exposed directly, any external code can read or mutate the internal state of an object, creating invisible dependencies throughout the codebase.

### Riel-2.1:2 - Problem

If a class exposes its data members publicly, every consumer becomes coupled to the internal representation. Any change to that representation ripples across the entire system, making maintenance prohibitively expensive and error-prone.

### Riel-2.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation integrity** | Hiding data preserves freedom to change internals vs. exposing data offers short-term convenience. |
| **Maintenance cost** | Stable interfaces reduce long-term cost vs. direct access reduces short-term coding effort. |
| **Coupling control** | Information hiding minimizes coupling vs. public data maximizes coupling. |

### Riel-2.1:4 - Solution

Declare all data members of a class as private. Provide access only through a well-defined public interface of methods. This ensures that the internal representation can evolve independently of the consumers, and that invariants on the data can be enforced consistently by the class itself.

### Riel-2.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `TemperatureSensor` class hides its raw voltage reading behind a `getTemperature()` method. When the hardware changes from analog to digital, only the class internals change; all client code continues to call `getTemperature()` unmodified. |
| **U.Episteme** | A research dataset object hides its internal storage format (CSV, Parquet, database rows) behind a query interface. When the storage backend migrates, no analysis scripts need updating. |

### Riel-2.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Public-field shortcut** | Data members declared public for quick prototyping. | Breaks encapsulation; any representation change cascades system-wide. | Make all fields private from the start; use accessor methods where truly needed. |
| **Getter/setter flood** | Every private field gets a trivial getter and setter. | Encapsulation is nominal, not effective; clients still depend on representation. | Expose behavior, not data; ask whether each accessor is genuinely needed. |

### Riel-2.1:9 - Consequences

| Benefits |
|----------|
| Representation changes are localized to the class. |
| Class invariants can be enforced in a single place. |
| Coupling between classes is reduced to behavioral contracts. |

| Trade-off | Mitigation |
|-----------|-----------|
| Accessor overhead | May require additional method calls; mitigated by compiler inlining and the far greater cost of broken encapsulation. |

### Riel-2.1:10 - Rationale

Information hiding is the foundational principle of modular design. By making data private, the class becomes the sole guardian of its invariants, and all external interactions are mediated by a contract that can be versioned and verified independently.

### Riel-2.1:11 - SoTA-Echoing

Information hiding was formalized by Parnas (1972) and remains a cornerstone of modern software engineering. Contemporary languages enforce it through access modifiers (Java, C#, Kotlin) or module-level encapsulation (Rust, Go). The principle aligns with the SOLID Interface Segregation Principle and is echoed in Domain-Driven Design's emphasis on encapsulated Aggregates.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.1:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.2, Riel-2.3, Riel-2.4, Riel-2.5, Riel-2.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.1:End
