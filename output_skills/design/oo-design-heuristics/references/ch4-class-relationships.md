# Chapter 4: Class Relationships
Theme: Coupling, containment, collaboration, and semantic constraints

## Riel-4.1 — Minimize Collaborating Classes
**Heuristic:** *"Minimize the number of classes with which another class collaborates."*
**Problem:** A class with many collaborators is tightly coupled to the system. Changes in any collaborator may require changes in this class, and testing requires complex setups.
**Resolution:** Keep the collaborator set of each class as small as possible. If a class needs data or behavior from many other classes, consider introducing a mediator or facade.
**Watch for:**
- Highly-connected class → Introduce facades or mediators to reduce direct dependencies.

## Riel-4.2 — Minimize Messages Between Collaborators
**Heuristic:** *"Minimize the number of message sends between a class and its collaborator."*
**Problem:** Excessive messaging between two classes indicates tight coupling in depth, not just breadth. It suggests that responsibilities may be misallocated.
**Resolution:** When the message count between two classes is high, consider moving some behavior from the caller to the callee (or vice versa) to reduce the interaction surface.
**Watch for:**
- Chatty interface → Consolidate into coarser-grained operations.

## Riel-4.3 — Minimize Collaboration Breadth
**Heuristic:** *"Minimize the amount of collaboration between a class and its collaborator, that is, the number of different messages sent."*
**Problem:** A wide message vocabulary between classes means each is deeply dependent on the other's interface, making changes expensive.
**Resolution:** When two classes exchange many different message types, consider whether some interactions should be consolidated or whether a different responsibility allocation would reduce interface width.
**Watch for:**
- Wide interface dependency → Narrow the interface with facade or adapter patterns.

## Riel-4.4 — Minimize Fanout
**Heuristic:** *"Minimize fanout in a class, that is, the product of the number of messages defined by the class and the messages they send."*
**Problem:** High fanout indicates that a class is orchestrating too much behavior. It is a quantitative god-class signal.
**Resolution:** Monitor fanout as a complexity metric. When it exceeds a threshold, decompose the class by extracting sub-coordinators or moving behavior to the classes that own the relevant data.
**Watch for:**
- Fanout explosion → Decompose into focused classes with lower individual fanout.

## Riel-4.5 — Containment Implies Use
**Heuristic:** *"If a class contains objects of another class, then the containing class should be sending messages to the contained objects."*
**Problem:** A class that contains objects it never uses is carrying dead weight. The containment relationship consumes resources without providing behavior.
**Resolution:** For every containment relationship, verify that the containing class sends messages to the contained object. If not, either the containment is unnecessary, or behavior has been misplaced elsewhere.
**Watch for:**
- Dead containment → Remove the containment or add the missing behavior.

## Riel-4.6 — Methods Should Use Most Data Most of the Time
**Heuristic:** *"Most of the methods defined on a class should be using most of the data members most of the time."*
**Problem:** When methods access only small subsets of the data, it indicates that the class may be capturing multiple abstractions and should be split.
**Resolution:** Analyze method-to-data-member usage patterns. If methods partition into groups that access disjoint data subsets, extract each group with its data into a separate class.
**Watch for:**
- Hidden partitioning → Run LCOM analysis and extract classes.

## Riel-4.7 — Limit Contained Object Count
**Heuristic:** *"Classes should not contain more objects than a developer can fit in short-term memory. A favorite value for this number is six."*
**Problem:** When a class contains more objects than a person can mentally track, it becomes difficult to understand, debug, and maintain.
**Resolution:** Limit the number of directly contained objects to approximately six. When a class naturally has more components, introduce intermediate containing classes to group related components.
**Watch for:**
- Flat containment explosion → Introduce intermediate grouping classes.

## Riel-4.8 — Distribute Intelligence Vertically
**Heuristic:** *"Distribute system intelligence vertically down narrow and deep containment hierarchies."*
**Problem:** When all intelligence sits at the top of a containment hierarchy, the top-level class becomes a god class while contained objects are passive data holders.
**Resolution:** Push behavior down to the most specific contained object that has the relevant data. The containing class should delegate to its parts rather than reaching into their data.
**Watch for:**
- Top-heavy hierarchy → Delegate behavior to the contained objects that own the data.

## Riel-4.9 — Prefer Class-Definition Constraints
**Heuristic:** *"When implementing semantic constraints, it is best to implement them in terms of the class definition."*
**Problem:** If semantic constraints are enforced only through runtime checks, they can be bypassed or forgotten. Structural enforcement through the type system is stronger.
**Resolution:** Prefer encoding constraints in the class definition (type system). When this causes excessive class proliferation, fall back to constructor-enforced runtime checks.
**Watch for:**
- Deferred validation → Validate in the constructor or, better, in the type structure.

## Riel-4.10 — Push Constraints Down Containment Hierarchies
**Heuristic:** *"When implementing semantic constraints in the constructor of a class, place the constraint test as far down a containment hierarchy as the domain allows."*
**Problem:** Placing constraint checks too high means the containing class knows too much about its parts' invariants, violating encapsulation.
**Resolution:** Place each constraint check in the constructor of the most deeply nested class that has sufficient information to evaluate it.
**Watch for:**
- Over-elevated constraint → Move the check into the contained class's constructor.

## Riel-4.11 — Centralize Volatile Constraint Information
**Heuristic:** *"The semantic information on which a constraint is based is best placed in a central, third-party object when that information is volatile."*
**Problem:** If volatile constraint information is scattered, updating it requires touching many classes, increasing inconsistency risk.
**Resolution:** When constraint information is volatile, place it in a central third-party object that all constrained classes consult.
**Watch for:**
- Scattered constants → Centralize in a configuration object.

## Riel-4.12 — Decentralize Stable Constraint Information
**Heuristic:** *"The semantic information on which a constraint is based is best decentralized among the classes involved when that information is stable."*
**Problem:** Centralizing stable constraint information adds unnecessary indirection without the benefit of easy changeability.
**Resolution:** When constraint information is stable, embed it directly in the constrained classes.
**Watch for:**
- Over-centralization → Embed stable constraints locally.

## Riel-4.13 — A Class Must Not Know Its Container
**Heuristic:** *"A class must know what it contains, but it should never know who contains it."*
**Problem:** If a contained class knows its container, it cannot be reused in a different container. The dependency direction is inverted, creating tight coupling.
**Resolution:** Design contained classes without any reference to their container. If upward communication is needed, use observer patterns, callbacks, or event mechanisms.
**Watch for:**
- Upward reference → Use an abstract observer or event interface instead.

## Riel-4.14 — No Peer-to-Peer Uses Within a Container
**Heuristic:** *"Objects that share lexical scope — those contained in the same containing class — should not have uses relationships between them."*
**Problem:** Direct uses relationships between siblings create hidden coupling that the container does not mediate.
**Resolution:** Sibling objects within a container should communicate only through the container. If sibling A needs sibling B's services, the container should mediate.
**Watch for:**
- Sibling coupling → Route all inter-part communication through the container.
