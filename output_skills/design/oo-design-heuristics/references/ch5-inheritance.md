# Chapter 5: Inheritance
Theme: Inheritance hierarchies, polymorphism, and specialization

## Riel-5.1 — Inheritance for Specialization Only
**Heuristic:** *"Inheritance should be used only to model a specialization hierarchy."*
**Problem:** Using inheritance for anything other than genuine specialization ('is-a') creates fragile hierarchies where derived classes inherit inappropriate behavior and violate substitutability.
**Resolution:** Before using inheritance, verify that the derived class is a genuine specialization of the base class — every instance of the derived class must be substitutable wherever the base class is expected. If the relationship is 'uses' or 'has-a', prefer containment.
**Watch for:**
- Convenience inheritance → Use containment or delegation instead.

## Riel-5.2 — Base Class Ignorance of Derived Classes
**Heuristic:** *"Derived classes must have knowledge of their base class by definition, but base classes should not know anything about their derived classes."*
**Problem:** If a base class references specific derived classes, adding a new derived class requires modifying the base, violating the Open/Closed Principle.
**Resolution:** Base classes must never import, reference, or conditionally branch on specific derived class types. Use virtual/abstract methods and polymorphic dispatch instead.
**Watch for:**
- Downward type check → Use polymorphic dispatch (virtual methods).

## Riel-5.3 — All Base Class Data Should Be Private
**Heuristic:** *"All data in a base class should be private; do not use protected data."*
**Problem:** Protected data allows derived classes to bypass the base class's methods and manipulate internal state directly, breaking encapsulation along the hierarchy dimension.
**Resolution:** Make all base class data private. Provide protected methods for access if needed, but never expose the data members themselves.
**Watch for:**
- Protected field → Use private data with protected accessor methods.

## Riel-5.4 — Deep Hierarchies in Theory
**Heuristic:** *"In theory, inheritance hierarchies should be deep — the deeper, the better."*
**Problem:** Shallow hierarchies miss opportunities for shared behavior at intermediate levels, leading to code duplication among sibling classes.
**Resolution:** Design hierarchies to be as deep as the domain's natural specialization structure allows. Each intermediate level should represent a genuine, meaningful abstraction.
**Watch for:**
- Flat hierarchy → Introduce meaningful intermediate abstractions.

## Riel-5.5 — Practical Hierarchy Depth Limit
**Heuristic:** *"In practice, inheritance hierarchies should be no deeper than an average person can keep in short-term memory. A popular value for this depth is six."*
**Problem:** Hierarchies deeper than about six levels exceed most developers' ability to mentally trace the chain.
**Resolution:** Keep inheritance hierarchies no deeper than approximately six levels. If domain complexity demands more, consider refactoring to use composition at intermediate levels.
**Watch for:**
- Ultra-deep hierarchy → Refactor deep branches to use composition.

## Riel-5.6 — Abstract Classes Must Be Base Classes
**Heuristic:** *"All abstract classes must be base classes."*
**Problem:** An abstract class that is not used as a base class is dead code — it defines a contract no one fulfills.
**Resolution:** Ensure every abstract class has at least one concrete derived class. If an abstract class has no descendants, either make it concrete or remove it.
**Watch for:**
- Orphaned abstraction → Add concrete descendants or remove the abstraction.

## Riel-5.7 — Base Classes Should Be Abstract
**Heuristic:** *"All base classes should be abstract classes."*
**Problem:** Concrete base classes tempt developers to instantiate them when they should be choosing a more specific subclass.
**Resolution:** Make base classes abstract. Only leaf classes in the hierarchy should be concrete. If a 'default' implementation is needed, create a concrete Default subclass.
**Watch for:**
- Concrete root → Make the root abstract; add an explicit default subclass if needed.

## Riel-5.8 — Factor Commonality High in the Hierarchy
**Heuristic:** *"Factor the commonality of data, behavior, and/or interface as high as possible in the inheritance hierarchy."*
**Problem:** Shared behavior duplicated across sibling classes is a maintenance burden. Changes must be replicated across all copies.
**Resolution:** Identify common data, behavior, and interface across sibling classes and migrate them to the nearest common ancestor. Create a new intermediate abstract class if no suitable ancestor exists.
**Watch for:**
- Sibling duplication → Extract common code to the nearest ancestor.

## Riel-5.9 — Common Data Without Behavior: Use Containment
**Heuristic:** *"If two or more classes share only common data (no common behavior), then that common data should be placed in a class that will be contained by each sharing class."*
**Problem:** Using inheritance to share only data violates the specialization principle and creates a misleading hierarchy.
**Resolution:** Extract the common data into a separate class. Each sharing class contains an instance of this data class. No inheritance hierarchy is created.
**Watch for:**
- Data inheritance → Use containment instead.

## Riel-5.10 — Common Data and Behavior: Use Inheritance
**Heuristic:** *"If two or more classes have common data and behavior, then those classes should each inherit from a common base class that captures those data and methods."*
**Problem:** Duplicated data and behavior across sibling classes is a clear signal that a common base class is missing.
**Resolution:** Create a common base class that captures the shared data and behavior. Each original class inherits from this base, adding only its unique specializations.
**Watch for:**
- Missed common base → Extract a common base class.

## Riel-5.11 — Common Interface Only: Inherit Only If Polymorphic
**Heuristic:** *"If two or more classes share only a common interface (messages, not methods), then they should inherit from a common base class only if they will be used polymorphically."*
**Problem:** Creating a common base class for mere interface similarity, without polymorphic use, adds unnecessary coupling and hierarchy complexity.
**Resolution:** Create a common interface or abstract base class only when clients will actually use the classes polymorphically. Without polymorphic use, the interface similarity is coincidental.
**Watch for:**
- Speculative interface → Add the common base only when polymorphic use is concrete.

## Riel-5.12 — Replace Type-Based Case Analysis with Polymorphism
**Heuristic:** *"Explicit case analysis on the type of an object is usually an error. The designer should use polymorphism in most of these cases."*
**Problem:** Type-based case analysis defeats polymorphism, creates maintenance hotspots, and forces modifications every time a new type is added.
**Resolution:** Replace type-based conditionals with polymorphic method dispatch. Each type handles its own case through an overridden method.
**Watch for:**
- Type switch → Use polymorphic dispatch.

## Riel-5.13 — Replace Value-Based Case Analysis with Inheritance
**Heuristic:** *"Explicit case analysis on the value of an attribute is often an error. The class should be decomposed into an inheritance hierarchy, where each value of the attribute is transformed into a derived class."*
**Problem:** Value-based case analysis scatters state-specific behavior across methods. Adding a new value requires touching every method.
**Resolution:** When methods repeatedly branch on the same attribute value, consider transforming each value into a derived class. Each subclass encapsulates the behavior for its state.
**Watch for:**
- Type-code multiplexing → Replace with inheritance or State pattern.

## Riel-5.14 — Do Not Model Dynamic Semantics with Inheritance
**Heuristic:** *"Do not model the dynamic semantics of a class through the use of the inheritance relationship."*
**Problem:** If a Person is modeled as a Student subclass, what happens when they graduate? They must be destroyed and recreated — a runtime type toggle that is awkward and error-prone.
**Resolution:** Use the State pattern, role objects, or attribute-based modeling for dynamic semantics. Reserve inheritance for permanent, structural specialization.
**Watch for:**
- Type toggling → Use State pattern or role objects.

## Riel-5.15 — Do Not Turn Instances into Subclasses
**Heuristic:** *"Do not turn objects of a class into derived classes of the class. Be very suspicious of any derived class for which there is only one instance."*
**Problem:** If a derived class has only one instance (e.g., Mars as a subclass of Planet), the designer has confused classification with instantiation.
**Resolution:** If a would-be subclass would have only one instance, model it as an instance of the existing class with unique attribute values, not as a separate class.
**Watch for:**
- Instance-as-class → Make it an instance with unique attribute values.

## Riel-5.16 — Do Not Create Classes at Runtime
**Heuristic:** *"If you think you need to create new classes at runtime, take a step back and realize that what you are trying to create are objects."*
**Problem:** Runtime class creation confuses the class level with the object level. What seems like a new type is almost always a new instance with different configuration.
**Resolution:** Generalize the varying behavior into a single class parameterized by configuration, strategies, or data. Create new objects of that class at runtime.
**Watch for:**
- Runtime class generation → Generalize into a configurable class with runtime object creation.

## Riel-5.17 — No NOP Overrides
**Heuristic:** *"It should be illegal for a derived class to override a base class method with a NOP method, that is, a method that does nothing."*
**Problem:** A NOP override means the derived class does not truly satisfy the base class contract. It breaks the Liskov Substitution Principle.
**Resolution:** If a derived class needs to NOP a method, the inheritance hierarchy is flawed. Either the method does not belong in the base class, or the derived class is not a genuine specialization. Restructure the hierarchy.
**Watch for:**
- NOP override → Restructure the hierarchy to avoid inheriting inapplicable methods.

## Riel-5.18 — Do Not Confuse Optional Containment with Inheritance
**Heuristic:** *"Do not confuse optional containment with the need for inheritance."*
**Problem:** Using inheritance to represent optional components creates a combinatorial explosion of subclasses: one for each combination of present/absent components.
**Resolution:** Model optional components as nullable or Optional-typed contained objects. Do not create subclasses for the presence or absence of optional parts.
**Watch for:**
- Optional-as-subclass → Use optional containment.

## Riel-5.19 — Build Reusable Frameworks, Not Just Components
**Heuristic:** *"When building an inheritance hierarchy, try to construct reusable frameworks rather than reusable components."*
**Problem:** Reusable components have limited value without the context in which they collaborate. Reusable frameworks capture the collaboration structure itself.
**Resolution:** Design inheritance hierarchies with framework reuse in mind: define abstract classes that capture the collaboration protocol, leaving concrete implementations to be plugged in.
**Watch for:**
- Isolated reuse → Design the collaboration itself for reuse.
