# Chapter 2: Classes and Objects
Theme: Encapsulation, cohesion, and class interface design

## Riel-2.1 — Hide All Data Within Its Class
**Heuristic:** *"All data should be hidden within its class."*
**Problem:** If a class exposes its data members publicly, every consumer becomes coupled to the internal representation. Any change to that representation ripples across the entire system, making maintenance prohibitively expensive and error-prone.
**Resolution:** Declare all data members of a class as private. Provide access only through a well-defined public interface of methods. This ensures that the internal representation can evolve independently of the consumers, and that invariants on the data can be enforced consistently by the class itself.
**Watch for:**
- Public-field shortcut → Make all fields private from the start; use accessor methods where truly needed.
- Getter/setter flood → Expose behavior, not data; ask whether each accessor is genuinely needed.

## Riel-2.2 — Class Independence from Its Users
**Heuristic:** *"Users of a class must be dependent on its public interface, but a class should not be dependent on its users."*
**Problem:** When a class depends on its users, it cannot be reused in a new context without dragging those user-specific dependencies along. The dependency direction is inverted, breaking modularity.
**Resolution:** Ensure that the dependency arrow points from user to class, never the reverse. A class should define its public interface without any reference to who calls it. When notification is needed, use observer patterns or callback abstractions rather than hard-coding knowledge of specific consumers.
**Watch for:**
- Upward dependency → Invert the dependency; let the caller adapt to the utility's interface.
- Hard-coded callbacks → Use an abstract listener or observer interface.

## Riel-2.3 — Minimize Protocol Size
**Heuristic:** *"Minimize the number of messages in the protocol of a class."*
**Problem:** An overly large public interface makes a class difficult to learn, use correctly, and maintain. It also signals that the class may be capturing more than one key abstraction.
**Resolution:** Keep the public interface of each class as small as possible. Each public method should represent a distinct, necessary capability of the abstraction. Convenience methods that can be composed from existing public methods should be avoided or placed in utility classes.
**Watch for:**
- Kitchen-sink interface → Apply the Interface Segregation Principle; split into role-specific interfaces.

## Riel-2.4 — Implement a Minimal Universal Public Interface
**Heuristic:** *"Implement a minimal public interface that all classes understand [e.g., copy, equality testing, pretty printing, parsing from an ASCII description, etc.]."*
**Problem:** Absence of a universal minimal interface forces users to learn ad-hoc conventions per class and prevents generic algorithms from operating uniformly across objects.
**Resolution:** Define a minimal set of universal operations (equality, copy, string representation, hashing) that all classes in the system implement. Make conscious decisions about deep versus shallow semantics for each class.
**Watch for:**
- Inherited defaults → Override equality and hashing for every value-carrying class.

## Riel-2.5 — Exclude Implementation Details from Public Interface
**Heuristic:** *"Do not put implementation details such as common-code private functions into the public interface of a class."*
**Problem:** Exposing implementation helpers publicly inflates the protocol, confuses users about the class's purpose, and prevents the implementor from freely refactoring internal code.
**Resolution:** Keep all implementation-detail functions private. The public interface should contain only methods that represent the abstraction's essential behavior as seen by its users.
**Watch for:**
- Accidental publicity → Default to private; promote to public only when a genuine use case demands it.

## Riel-2.6 — Do Not Clutter the Public Interface
**Heuristic:** *"Do not clutter the public interface of a class with things that users of that class are not able to use or are not interested in using."*
**Problem:** A cluttered interface obscures the essential capabilities of a class, leading users to misuse irrelevant methods or overlook the important ones.
**Resolution:** Audit the public interface from the user's perspective. Remove or hide any method that is not relevant to the user's interaction with the abstraction.
**Watch for:**
- Infrastructure leak → Use interface segregation to separate user and framework contracts.

## Riel-2.7 — Nil or Export Coupling Only
**Heuristic:** *"Classes should only exhibit nil or export coupling with other classes, that is, a class should only use operations in the public interface of another class or have nothing to do with that class."*
**Problem:** When a class bypasses another class's public interface to access its internals, both classes become locked together. Any internal change in one forces changes in the other.
**Resolution:** Ensure that every inter-class interaction goes exclusively through the public interface. No class should use friend declarations, reflection hacks, or package-private access to manipulate another class's internals.
**Watch for:**
- Friend abuse → Redesign the interface to expose what is genuinely needed.
- Reflection hacking → Treat reflection as a diagnostic tool, not a design technique.

## Riel-2.8 — One Key Abstraction Per Class
**Heuristic:** *"A class should capture one and only one key abstraction."*
**Problem:** A class capturing multiple abstractions has low cohesion, a large interface, and is difficult to name, understand, reuse, or maintain.
**Resolution:** Ensure each class represents exactly one key domain abstraction. If a class is hard to name with a single noun, or if its methods cluster into groups that operate on separate subsets of its data, it should be split into multiple classes.
**Watch for:**
- Dual-purpose class → Split into one class per key abstraction.

## Riel-2.9 — Keep Related Data and Behavior Together
**Heuristic:** *"Keep related data and behavior in one place."*
**Problem:** When behavior that operates on a class's data is placed outside that class, developers must coordinate changes across multiple locations, leading to subtle bugs.
**Resolution:** Place every operation that primarily manipulates a class's data inside that class. If an operation requires data from multiple classes, consider which class is the natural owner.
**Watch for:**
- Anemic domain model → Move behavior to the class that owns the data.

## Riel-2.10 — Spin Off Non-Related Information
**Heuristic:** *"Spin off nonrelated information into another class (i.e., noncommunicating behavior)."*
**Problem:** Noncommunicating behavior within a class signals low cohesion. The class is doing too many unrelated things, making it harder to understand, test, and reuse.
**Resolution:** Identify method groups that operate on disjoint data subsets. Extract each group, along with its data, into a separate class.
**Watch for:**
- Grab-bag class → Periodically audit method-data affinity and extract classes.

## Riel-2.11 — Model Classes, Not Roles
**Heuristic:** *"Be sure the abstractions that you model are classes and not simply the roles objects play."*
**Problem:** Modeling roles as classes leads to type-switching at runtime (a Person cannot become a Mother without changing class) and an explosion of artificial inheritance hierarchies.
**Resolution:** Distinguish between enduring identity (the class) and transient behavior (the role). Model the enduring identity as a class and the role as a property, contained role object, or strategy pattern that can be attached and detached dynamically.
**Watch for:**
- Role-as-subclass → Use composition or the Role Object pattern.
