## Riel-2.3 - Minimize Protocol Size

> **Type:** Heuristic (Object-Oriented Design)
> **Status:** Extracted
> **Source:** Arthur J. Riel, *Object-Oriented Design Heuristics* (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
> **Chapter Theme:** Encapsulation, cohesion, and class interface design

**Original Statement:** *"Minimize the number of messages in the protocol of a class."*

### Riel-2.3:1 - Problem Frame

The public interface (protocol) of a class is the contract that all users must learn and depend upon. A large protocol increases the cognitive burden on users and the maintenance surface for implementors.

### Riel-2.3:2 - Problem

An overly large public interface makes a class difficult to learn, use correctly, and maintain. It also signals that the class may be capturing more than one key abstraction.

### Riel-2.3:3 - Forces

| Force | Tension |
|-------|---------|
| **Learnability** | A small interface is easier to learn vs. a large interface may cover more use cases. |
| **Maintenance surface** | Fewer public methods reduce the cost of change vs. removing methods is a breaking change. |
| **Abstraction cohesion** | A focused interface suggests a cohesive abstraction vs. a sprawling one suggests over-generalization. |

### Riel-2.3:4 - Solution

Keep the public interface of each class as small as possible. Each public method should represent a distinct, necessary capability of the abstraction. Convenience methods that can be composed from existing public methods should be avoided or placed in utility classes. Regularly audit the protocol for unused or rarely-used methods.

### Riel-2.3:5 - Archetypal Grounding

| Substrate | Illustration |
|-----------|-------------|
| **U.System** | A `Stack` class exposes only `push()`, `pop()`, `peek()`, and `isEmpty()`. Methods like `sort()` or `filter()` are not part of the stack abstraction and belong elsewhere. |
| **U.Episteme** | A `HypothesisTest` class exposes `run()` and `getResult()`. Internal computations like distribution sampling are private implementation details, not public protocol. |

### Riel-2.3:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Prag** (pragmatic software design). This heuristic originates from a practitioner tradition focused on object-oriented implementation quality. It is language-community-biased (primarily C++/Java-era OO) and may require adaptation for functional, multi-paradigm, or actor-based systems.

### Riel-2.3:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-Riel-2.3.1** | A design review **SHALL** verify that this heuristic is either satisfied or a documented exception exists. | Ensures conscious engagement with the heuristic. |
| **CC-Riel-2.3.2** | Any violation **SHALL** include a rationale in the Design-Rationale Record explaining why the heuristic was overridden. | Maintains auditability of design decisions. |

### Riel-2.3:8 - Common Anti-Patterns and How to Avoid Them

| Anti-Pattern | Symptom | Why It Fails | How to Avoid |
|-------------|---------|--------------|--------------|
| **Kitchen-sink interface** | Every conceivable operation is made public. | Users cannot distinguish essential from incidental behavior. | Apply the Interface Segregation Principle; split into role-specific interfaces. |

### Riel-2.3:9 - Consequences

| Benefits |
|----------|
| Users face a smaller learning curve. |
| The class is easier to re-implement or wrap. |
| Cohesion violations become visible earlier. |

| Trade-off | Mitigation |
|-----------|-----------|
| Convenience gap | Users may need to compose multiple calls; mitigated by providing well-documented usage patterns. |

### Riel-2.3:10 - Rationale

A minimal protocol is a direct expression of the principle of least privilege applied to class design: expose only what is necessary and sufficient for the abstraction's purpose.

### Riel-2.3:11 - SoTA-Echoing

The Interface Segregation Principle (Martin, 2003) counsels against fat interfaces. Modern API design guides (Google, Microsoft) recommend small, composable interfaces. Rust's trait system and Go's small interfaces exemplify this heuristic in language design.

Riel's heuristic (1996) predates many of these formalizations but captures the same essential insight from practitioner experience. The enduring validity of this heuristic across three decades of practice and language evolution confirms its status as a genuine design principle rather than a period-specific guideline.

### Riel-2.3:12 - Relations

* **Source:** Riel (1996), Chapter 2 — Classes and Objects: The Building Blocks of the Object-Oriented Paradigm
* **Sibling heuristics:** Riel-2.1, Riel-2.2, Riel-2.4, Riel-2.5, Riel-2.6
* **FPF integration:** This heuristic informs FPF-aligned design decisions wherever OO structures are used as implementation substrates for `U.System` or `U.Episteme` architectures.

### Riel-2.3:End
