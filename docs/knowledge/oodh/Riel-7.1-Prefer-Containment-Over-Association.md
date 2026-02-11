## Riel-7.1 - Prefer Containment Over Association

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 7 — The Association Relationship
> **Chapter Theme:** Association versus containment trade-offs

**Original Statement:** *"When given a choice in an object-oriented design between a containment relationship and an association relationship, choose the containment relationship."*

### Riel-7.1:1 - Problem Frame

Containment (has-a) and association (uses-a) both model relationships between classes, but they differ in ownership semantics and lifecycle coupling.

### Riel-7.1:2 - Problem

Association is a weaker, less committed relationship. When the domain implies ownership or lifecycle dependency, using association instead of containment misrepresents the relationship and complicates memory/lifecycle management.

### Riel-7.1:3 - Forces

| Force | Tension |
|-------|---------|
| **Ownership clarity** | Containment makes ownership explicit vs. association leaves ownership ambiguous. |
| **Lifecycle management** | Containment ties lifecycles together vs. association requires separate management. |
| **Flexibility** | Association allows independent existence vs. containment couples lifecycles. |

### Riel-7.1:4 - Solution

When an object owns or has lifecycle control over another, use containment. Use association only when objects have independent lifecycles and the relationship is transient or navigational.

### Riel-7.1:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Car` owns its `Engine`—use containment. A `Car` uses a `GasStation`—use association. |
| **U.Episteme** | A `Paper` owns its `Abstract`—use containment. A `Paper` cites another `Paper`—use association. |

### Riel-7.1:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-7.1:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-7.1.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-7.1.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-7.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Weak reference for owned objects** | Using association for objects that are conceptually owned. | Lifecycle ambiguity; dangling references. | Use containment to express ownership. |

### Riel-7.1:9 - Consequences

| Benefits |
|----------|
| Ownership and lifecycle are explicit. |
| Memory management is simpler. |

| Trade-off | Mitigation |
|-----------|-----------|
| Reduced flexibility | Containment ties lifecycles; not appropriate for independent entities. |

### Riel-7.1:10 - Rationale

Containment is the stronger, clearer relationship. Defaulting to it ensures ownership semantics are explicit.

### Riel-7.1:11 - SoTA-Echoing

UML distinguishes composition (strong containment with lifecycle) from aggregation and association. Modern languages provide ownership semantics (Rust's ownership system) that formalize this.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-7.1:12 - Relations

* **Source:** Riel (1996), Chapter 7 — The Association Relationship
* **Sibling heuristics:** None in the same chapter
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-7.1:End
