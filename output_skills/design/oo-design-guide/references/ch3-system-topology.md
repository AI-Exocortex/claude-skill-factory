# Chapter 3: System Topology
Theme: System intelligence distribution and god-class avoidance

## Riel-3.1 — Distribute Intelligence Horizontally
**Heuristic:** *"Distribute system intelligence horizontally as uniformly as possible, that is, the top-level classes in a design should share the work uniformly."*
**Problem:** When system intelligence is concentrated in a few classes, those classes become god classes that are hard to understand, maintain, and test, while the remaining classes are anemic shells.
**Resolution:** Ensure that top-level classes share behavioral responsibility roughly evenly. If one class is significantly larger or more complex than its peers, redistribute its responsibilities.
**Watch for:**
- Central controller → Move behavior to the classes that own the relevant data.

## Riel-3.2 — Avoid God Classes
**Heuristic:** *"Do not create god classes/objects in your system. Be very suspicious of a class whose name contains Driver, Manager, System, or Subsystem."*
**Problem:** God classes concentrate too much intelligence, becoming maintenance bottlenecks, testing nightmares, and single points of failure for understanding the system.
**Resolution:** When a class's name contains 'Driver', 'Manager', 'System', or 'Subsystem', scrutinize it for god-class symptoms: too many methods, too many data members, too many collaborators. Redistribute its responsibilities to domain-appropriate classes.
**Watch for:**
- God class → Apply Heuristic 3.1 to redistribute intelligence.

## Riel-3.3 — Watch for Excessive Accessor Methods
**Heuristic:** *"Beware of classes that have many accessor methods defined in their public interface. Having many implies that related data and behavior are not being kept in one place."*
**Problem:** Excessive accessors signal that other classes are pulling data out and operating on it externally, violating co-location of data and behavior.
**Resolution:** When a class has many accessors, ask where the behavior that uses that data lives. Move the behavior into the class and eliminate the now-unnecessary accessors.
**Watch for:**
- Getter parade → Replace getters with meaningful behavioral methods.

## Riel-3.4 — Watch for Noncommunicating Behavior
**Heuristic:** *"Beware of classes that have too much noncommunicating behavior, that is, methods that operate on a proper subset of the data members of a class."*
**Problem:** Noncommunicating behavior indicates the class should be split. Left unaddressed, it grows into a god class with increasingly tangled responsibilities.
**Resolution:** Analyze method-data affinity. When methods cluster around data subsets, extract each cluster with its data into a separate class.
**Watch for:**
- Creeping conflation → Regularly run LCOM analysis and extract when clusters emerge.

## Riel-3.5 — Model-Interface Separation
**Heuristic:** *"In applications that consist of an object-oriented model interacting with a user interface, the model should never be dependent on the interface."*
**Problem:** When the model depends on the interface, the model cannot be reused with a different interface, tested independently, or reasoned about without UI knowledge.
**Resolution:** Ensure the dependency arrow points from the interface to the model, never the reverse. Use observer patterns or event systems if the model needs to notify the UI of state changes.
**Watch for:**
- Model-to-UI callback → Use observer pattern or event bus.

## Riel-3.6 — Model the Real World When Possible
**Heuristic:** *"Model the real world whenever possible. (This heuristic is often violated for reasons of system intelligence distribution, avoidance of god classes, and the keeping of related data and behavior in one place.)"*
**Problem:** Modeling the real world naively may produce god classes, misplaced intelligence, or violations of data-behavior co-location. Real-world structure is not always optimal software structure.
**Resolution:** Start with real-world modeling for initial conceptualization, but be prepared to deviate when design heuristics demand it. Document where and why the software model departs from the domain model.
**Watch for:**
- Naive mapping → Validate each class against cohesion and coupling heuristics.

## Riel-3.7 — Eliminate Irrelevant Classes
**Heuristic:** *"Eliminate irrelevant classes from your design."*
**Problem:** Irrelevant classes add complexity without value. They clutter the design and dilute focus on essential abstractions.
**Resolution:** Review candidate classes for meaningful behavior. A class with no behavior (only data) is suspect. If it has no methods beyond accessors, either move its data into a related class or promote it by adding genuine behavior.
**Watch for:**
- Noun-driven class proliferation → Apply a behavior test: if a class has no meaningful methods, it should not exist.

## Riel-3.8 — Eliminate Outside-System Classes
**Heuristic:** *"Eliminate classes that are outside the system."*
**Problem:** Including classes that are outside the system boundary adds complexity without utility. They represent actors or external entities, not internal abstractions.
**Resolution:** Identify the system boundary clearly. Entities outside this boundary should be represented only at the boundary as interfaces or stubs, not as full internal classes.
**Watch for:**
- External entity internalization → Model external entities as boundary interfaces.

## Riel-3.9 — Do Not Turn Operations into Classes
**Heuristic:** *"Do not turn an operation into a class. Be suspicious of any class whose name is a verb or is derived from a verb, especially those that have only one piece of meaningful behavior."*
**Problem:** A verb-named class with a single behavior is likely a function masquerading as a class. It adds structural overhead without providing the benefits of a genuine abstraction.
**Resolution:** When a candidate class is named after a verb, ask: does this operation belong on an existing class? Only reify as a class if the operation needs polymorphic dispatch, queuing, or undo (Strategy or Command patterns).
**Watch for:**
- Verb class → Move the method to the class whose data it operates on.

## Riel-3.10 — Prune Agent Classes in Design
**Heuristic:** *"Agent classes are often placed in the analysis model of an application. During design time, many agents are found to be irrelevant and should be removed."*
**Problem:** Agent classes that merely pass messages between domain objects are middlemen that add complexity without intelligence.
**Resolution:** During the transition from analysis to design, scrutinize every agent class. If it merely delegates without adding intelligence, remove it and let the domain objects collaborate directly.
**Watch for:**
- Middleman → Eliminate the agent; let collaborators interact directly.
