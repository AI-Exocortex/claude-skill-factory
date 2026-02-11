# Chapter 6: Multiple Inheritance
Theme: Safe use of multiple inheritance

## Riel-6.1 — Multiple Inheritance Is Suspect by Default
**Heuristic:** *"If you have an example of multiple inheritance in your design, assume you have made a mistake and then prove otherwise."*
**Problem:** MI is often used when containment or interface implementation would be more appropriate. The complexity cost is high and the design benefits are rarely worth it.
**Resolution:** Treat every MI use as guilty until proven innocent. For each case, verify that (1) the entity genuinely 'is-a' each base class, and (2) neither containment nor interface implementation can express the relationship. Only keep MI that survives both tests.
**Watch for:**
- Lazy MI → Replace with containment or interface implementation.

## Riel-6.2 — Two Questions for Every Inheritance
**Heuristic:** *"Whenever there is inheritance in an object-oriented design, ask yourself two questions: (1) Am I a special type of the thing from which I'm inheriting? (2) Is the thing from which I'm inheriting part of me?"*
**Problem:** If the answer to question (2) is 'yes', then containment, not inheritance, is the correct relationship.
**Resolution:** For every inheritance link, ask both questions. If 'is-a' is true and 'has-a' is false, keep inheritance. If 'has-a' is true, use containment. If both are ambiguous, default to containment.
**Watch for:**
- Inheritance for has-a → Apply the two-question test; switch to containment.

## Riel-6.3 — No Redundant Base Classes in MI
**Heuristic:** *"Whenever you have found a multiple inheritance relationship, be sure that no base class is actually a derived class of another base class."*
**Problem:** Redundant inheritance creates diamond problems, duplicated state, and ambiguous method resolution.
**Resolution:** When using MI, verify that no base class is an ancestor of another base class in the same MI set. If it is, simplify the inheritance.
**Watch for:**
- Diamond duplication → Remove the direct redundant inheritance link.

# Chapter 7: Association
Theme: Association vs. containment relationships

## Riel-7.1 — Prefer Containment Over Association
**Heuristic:** *"When given a choice between a containment relationship and an association relationship, choose the containment relationship."*
**Problem:** Association is a weaker, less committed relationship. When the domain implies ownership or lifecycle dependency, using association misrepresents the relationship.
**Resolution:** When an object owns or has lifecycle control over another, use containment. Use association only when objects have independent lifecycles and the relationship is transient or navigational.
**Watch for:**
- Weak reference for owned objects → Use containment to express ownership.

# Chapter 8: Class-Specific Data
Theme: Class-level vs. instance-level data management

## Riel-8.1 — No Global Data for Class Bookkeeping
**Heuristic:** *"Do not use global data or functions to perform bookkeeping information on the objects of a class. Class variables or methods should be used instead."*
**Problem:** Global data couples the bookkeeping to the global namespace, breaking encapsulation and making the class non-self-contained.
**Resolution:** Use class variables (static members) and class methods (static methods) to manage class-level bookkeeping.
**Watch for:**
- Global counter → Move to a class variable with class methods for access.

# Chapter 9: Physical Design
Theme: Physical packaging and interface discipline

## Riel-9.1 — Logical Design Integrity over Physical Criteria
**Heuristic:** *"Object-oriented designers should not allow physical design criteria to corrupt their logical designs."*
**Problem:** When physical concerns (performance optimization, memory layout, network boundaries) drive the logical design, the result is a corrupted model that is hard to understand and evolve.
**Resolution:** Design the logical model first, driven by domain correctness. Then address physical concerns as a separate layer of decisions, clearly documented and separated from the logical design.
**Watch for:**
- Performance-driven distortion → Separate logical and physical design; optimize the physical layer.

## Riel-9.2 — Always Use the Public Interface
**Heuristic:** *"Do not change the state of an object without going through its public interface."*
**Problem:** Bypassing the public interface breaks encapsulation, invalidates invariants, and creates invisible dependencies that are nearly impossible to debug.
**Resolution:** Always modify object state through the public interface, even in physical design. If performance requires bulk operations, add them to the public interface rather than bypassing it.
**Watch for:**
- Backdoor mutation → Route all mutations through the public interface.
