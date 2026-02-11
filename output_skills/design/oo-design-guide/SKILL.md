---
name: oo-design-guide
description: Guides OO design decisions using Riel's heuristics on encapsulation, cohesion, coupling, and inheritance. Use when writing new classes, designing features, or structuring code in OO codebases.
---

STARTER_CHARACTER = 🧭

## Purpose

Use Riel's 61 object-oriented design heuristics as guidelines that shape design decisions while writing code. Heuristics are guidelines, not laws — departures are fine when justified, but the default path should follow them.

## Design Process

### 1. Understand the Task

Read the feature request, requirements, or problem description. Identify what new classes, responsibilities, and relationships are needed.

### 2. Load Relevant Guidelines

Not all heuristics apply to every task. Load only the chapters that match what you're designing:

- Defining class boundaries, interfaces, responsibilities → [Ch.2: Classes and Objects](references/ch2-classes-and-objects.md)
- Distributing intelligence, avoiding god classes → [Ch.3: System Topology](references/ch3-system-topology.md)
- Structuring collaborations, containment, constraints → [Ch.4: Class Relationships](references/ch4-class-relationships.md)
- Designing inheritance hierarchies, choosing polymorphism → [Ch.5: Inheritance](references/ch5-inheritance.md)
- Multiple inheritance, association, class data, physical design → [Ch.6–9: MI, Association, Class Data, Physical Design](references/ch6-9-supplementary.md)

### 3. Apply Heuristics While Designing

Let the heuristics guide choices as they come up:

- **Defining a class** → hide data (2.1), depend on public interface only (2.2), one abstraction per class (2.8), keep data and behavior together (2.9), spin off unrelated info (2.10)
- **Distributing responsibilities** → spread intelligence horizontally (3.1), avoid god classes (3.2), push intelligence down containment hierarchies (4.8)
- **Relating classes** → minimize collaborators (4.1), minimize message sends (4.2–4.3), prefer containment over association (7.1), contained class must not know its container (4.13)
- **Using inheritance** → model specialization only (5.1), base classes should be abstract (5.7), factor commonality high (5.8), prefer polymorphism over type switches (5.12)
- **Placing constraints** → prefer class-definition constraints (4.9), push constraints down (4.10), centralize volatile ones (4.11), decentralize stable ones (4.12)

You don't need to check every heuristic. Let the design decision at hand pull in the relevant ones.

### 4. Note Departures

When you intentionally depart from a heuristic, briefly note why. This keeps the design honest without slowing down the work.

## Quick Reference: 61 Heuristics by Chapter

### Ch.2 — Classes and Objects (encapsulation, cohesion, interfaces)
- **2.1** Hide all data within its class
- **2.2** Class users should depend on the public interface, not implementation
- **2.3** Minimize the number of messages in a class's protocol
- **2.4** Implement a minimal universal public interface (init, copy, compare, print, etc.)
- **2.5** Exclude implementation details from the public interface
- **2.6** Do not clutter the public interface with things users can't use or don't need
- **2.7** Classes should only exhibit nil or export coupling with other classes
- **2.8** A class should capture one and only one key abstraction
- **2.9** Keep related data and behavior in one place
- **2.10** Spin off non-related information into another class
- **2.11** Model classes, not roles people or things play

### Ch.3 — System Topology (intelligence distribution, god classes)
- **3.1** Distribute system intelligence horizontally — avoid central control
- **3.2** Do not create god classes (suspect names: Manager, Driver, System, Subsystem)
- **3.3** Beware of classes with many accessor methods — data may belong elsewhere
- **3.4** Beware of classes with noncommunicating behavior (disjoint method groups)
- **3.5** Separate model from interface in MVC-style designs
- **3.6** Model the real world whenever possible
- **3.7** Eliminate classes that only carry data with no behavior (unless they are records/DTOs)
- **3.8** Eliminate classes that model things outside the system boundary
- **3.9** Do not turn operations into classes
- **3.10** Agent classes from analysis are often eliminated during design

### Ch.4 — Class Relationships (coupling, containment, constraints)
- **4.1** Minimize the number of classes a class collaborates with
- **4.2** Minimize the number of message sends between collaborators
- **4.3** Minimize the breadth of collaboration (number of distinct message types)
- **4.4** Minimize fanout (messages sent from a single method)
- **4.5** If a class contains another class, it should use it
- **4.6** Most methods should use most data members most of the time
- **4.7** Keep the number of contained objects low (around six)
- **4.8** Distribute system intelligence vertically — deep containers shouldn't be mere shells
- **4.9** Prefer constraining via class definition over constructor validation
- **4.10** Push constraints down containment hierarchies
- **4.11** Centralize volatile constraints; if they change, one place changes
- **4.12** Decentralize stable constraints; spread them across the classes that own them
- **4.13** A contained class must not know about its container
- **4.14** Objects inside a container should not use each other directly

### Ch.5 — Inheritance (specialization, polymorphism, hierarchy)
- **5.1** Inheritance should model specialization only
- **5.2** Base classes should not know about derived classes
- **5.3** All base class data should be private (not protected)
- **5.4** In theory, deep hierarchies are desirable for reuse
- **5.5** In practice, keep hierarchy depth manageable (avoid very deep trees)
- **5.6** All abstract classes should be base classes
- **5.7** All base classes should be abstract
- **5.8** Factor commonality as high as possible in the hierarchy
- **5.9** Two classes with common data but no common behavior → use containment, not inheritance
- **5.10** Two classes with common data and behavior → use inheritance
- **5.11** Two classes with only a common interface → inherit only if polymorphism is needed
- **5.12** Replace explicit type-based case analysis with polymorphism
- **5.13** Replace explicit value-based case analysis with inheritance hierarchies
- **5.14** Do not model dynamic semantics (state changes) with inheritance
- **5.15** Do not turn object instances into subclasses
- **5.16** Do not create new classes at runtime to model dynamic behavior
- **5.17** Overriding a method with a NOP is a design error
- **5.18** Do not confuse optional containment with inheritance
- **5.19** Build reusable frameworks, not just reusable components

### Ch.6–9 — MI, Association, Class Data, Physical Design
- **6.1** Multiple inheritance is suspect by default
- **6.2** For every inheritance, ask: "Is the derived a special kind of the base?" and "Is the base ever not specialized?"
- **6.3** In MI, ensure no redundant base classes in the lattice
- **7.1** Prefer containment over association
- **8.1** Do not use global data for class bookkeeping — use class variables
- **9.1** Logical design integrity trumps physical packaging criteria
- **9.2** Always use the public interface, even within the implementation package

## Traps to Steer Clear Of

These are the highest-impact design traps — catch them as you shape the code, not after:

- **God class** (3.1, 3.2): A class that orchestrates everything. Suspect names: Manager, Driver, System, Subsystem. Spread responsibilities across domain classes instead.
- **Public data** (2.1): Exposing fields directly. Start with all data private; add accessors only when genuinely needed.
- **Getter/setter flood** (2.1, 3.3): Wrapping every field in trivial get/set gives only nominal encapsulation. Expose behavior, not data.
- **Convenience inheritance** (5.1): Inheriting to reuse code rather than to model specialization. Use containment or delegation.
- **Type switch** (5.12): Branching on instanceof/typeid instead of using polymorphism. Add a method to the hierarchy.
- **NOP override** (5.17): Overriding a method to do nothing signals the hierarchy is wrong. Restructure so the method isn't inherited where it doesn't apply.
- **Container awareness** (4.13): A contained object referencing its container. Use callbacks or observer interfaces for upward communication.
- **Low cohesion** (4.6): Methods partition into groups using disjoint data subsets. Split the class before it grows further.
