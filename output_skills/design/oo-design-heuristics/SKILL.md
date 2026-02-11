---
name: oo-design-heuristics
description: Reviews designs against Riel's object-oriented design heuristics covering encapsulation, cohesion, coupling, inheritance, and class relationships. Use when reviewing class designs, evaluating object models, or designing features in OO codebases.
---

STARTER_CHARACTER = 🏛️

## Purpose

Apply Riel's 61 object-oriented design heuristics as a systematic review lens for class designs and feature architectures. Heuristics are guidelines, not laws — violations require documented rationale, not blind compliance.

## Review Process

### 1. Understand the Design

Read or receive the design under review: class diagrams, code, feature descriptions, or object models. Identify the classes, their responsibilities, relationships (containment, inheritance, association), and collaborations.

### 2. Select Relevant Chapters

Not all heuristics apply to every design. Load only the chapters that match the design concerns:

- Encapsulation issues, bloated interfaces → [Ch.2: Classes and Objects](references/ch2-classes-and-objects.md)
- Centralized control, god classes, procedural feel → [Ch.3: System Topology](references/ch3-system-topology.md)
- Coupling, containment, constraint placement → [Ch.4: Class Relationships](references/ch4-class-relationships.md)
- Inheritance hierarchies, polymorphism, hierarchy depth → [Ch.5: Inheritance](references/ch5-inheritance.md)
- Multiple inheritance, association, class data, physical design → [Ch.6–9: MI, Association, Class Data, Physical Design](references/ch6-9-supplementary.md)

### 3. Check Against Heuristics

For each relevant heuristic, assess:
- Does the design satisfy it?
- If not, is there a justified reason?

### 4. Report Findings

For each violation found:
- State the heuristic ID and name
- Describe the specific violation in the design
- Suggest a concrete improvement
- Note if the violation is justified (with rationale)

Group findings by severity: structural issues first (wrong abstractions, god classes, broken encapsulation), then refinements (interface cleanliness, constraint placement).

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

## Anti-patterns to Flag

These are the highest-signal violations to catch early:
- **God class** (3.2): A class that controls everything. Look for Manager/Driver/System names, excessive method count, or every other class depending on it.
- **Public data** (2.1): Data members exposed without encapsulation.
- **Getter/setter flood** (2.1, 3.3): Every field has a trivial getter and setter — encapsulation is nominal only.
- **Convenience inheritance** (5.1): Inheriting to reuse code rather than to model specialization.
- **Type switch** (5.12): Branching on instanceof/typeid instead of using polymorphism.
- **NOP override** (5.17): Overriding a method to do nothing — signals the hierarchy is wrong.
- **Container awareness** (4.13): A contained object knows about its container.
- **Low cohesion** (4.6): Methods partition into groups using disjoint data subsets — the class should be split.
