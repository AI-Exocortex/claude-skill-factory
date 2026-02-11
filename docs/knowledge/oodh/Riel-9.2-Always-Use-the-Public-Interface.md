## Riel-9.2 - Always Use the Public Interface

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 9 — Physical Object-Oriented Design
> **Chapter Theme:** Logical versus physical design integrity

**Original Statement:** *"Do not change the state of an object without going through its public interface."*

### Riel-9.2:1 - Problem Frame

Physical design sometimes tempts developers to bypass the public interface for performance or convenience, directly modifying object state.

### Riel-9.2:2 - Problem

Bypassing the public interface breaks encapsulation, invalidates invariants, and creates invisible dependencies that are nearly impossible to debug.

### Riel-9.2:3 - Forces

| Force | Tension |
|-------|---------|
| **Encapsulation** | The public interface guarantees invariants vs. direct access is faster. |
| **Correctness** | Invariant violations cause subtle, hard-to-find bugs vs. the performance cost of method calls is negligible. |

### Riel-9.2:4 - Solution

Always modify object state through the public interface, even in physical design. If performance requires bulk operations, add them to the public interface rather than bypassing it.

### Riel-9.2:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | Even in a performance-critical game engine, object state should be modified through methods that maintain invariants, not by direct field writes. |
| **U.Episteme** | Even when bulk-loading data into a model, use the model's interface to ensure validation and constraint checking. |

### Riel-9.2:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-9.2:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-9.2.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-9.2.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-9.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Backdoor mutation** | State is modified through reflection, friend functions, or raw memory access. | Invariants are silently broken; bugs are non-reproducible. | Route all mutations through the public interface. |

### Riel-9.2:9 - Consequences

| Benefits |
|----------|
| Invariants are always maintained. |
| All state changes are auditable through the interface. |

| Trade-off | Mitigation |
|-----------|-----------|
| Performance overhead | Method calls add minimal overhead; mitigated by adding efficient bulk operations to the interface. |

### Riel-9.2:10 - Rationale

The public interface is the guardian of correctness. Bypassing it trades correctness for speed—a trade that almost always costs more than it saves.

### Riel-9.2:11 - SoTA-Echoing

Immutability trends in modern languages (Kotlin, Rust, functional programming) enforce this by making all state changes explicit. Event sourcing makes state changes auditable by design.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-9.2:12 - Relations

* **Source:** Riel (1996), Chapter 9 — Physical Object-Oriented Design
* **Sibling heuristics:** Riel-9.1
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-9.2:End
