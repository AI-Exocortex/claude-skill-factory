# Chapter 3: Behavior — Pattern Index

**Source:** Kent Beck, *Smalltalk Best Practice Patterns* (1997), Chapter 3  
**Adaptation:** Java 17+ / Kotlin 1.9+ microservice development  
**FPF Template:** E.8 Canonical Pattern Template  
**Patterns:** 31

## Adoption Verdicts at a Glance

| ID | Pattern | Verdict |
|----|---------|---------|
| SBPP-BEH-01 | Composed Method | **ADOPT** |
| SBPP-BEH-02 | Constructor Method | **ADOPT** |
| SBPP-BEH-03 | Constructor Parameter Method | **ADOPT** |
| SBPP-BEH-04 | Shortcut Constructor Method | **ADOPT** |
| SBPP-BEH-05 | Converter Method | **ADOPT/ADAPT** |
| SBPP-BEH-06 | Converter Constructor Method | **ADOPT/ADAPT** |
| SBPP-BEH-07 | Query Method | **ADOPT** |
| SBPP-BEH-08 | Comparing Method | **ADOPT** |
| SBPP-BEH-09 | Reversing Method | **ADOPT/ADAPT** |
| SBPP-BEH-10 | Method Object | **ADOPT** |
| SBPP-BEH-11 | Execute Around Method | **ADOPT** |
| SBPP-BEH-12 | Debug Printing Method | **ADOPT** |
| SBPP-BEH-13 | Method Comment | **ADOPT** |
| SBPP-BEH-14 | Message | **ADOPT** |
| SBPP-BEH-15 | Choosing Message | **ADOPT** |
| SBPP-BEH-16 | Decomposing Message | **ADOPT** |
| SBPP-BEH-17 | Intention Revealing Message | **ADOPT** |
| SBPP-BEH-18 | Intention Revealing Selector | **ADOPT** |
| SBPP-BEH-19 | Dispatched Interpretation | **ADOPT** |
| SBPP-BEH-20 | Double Dispatch | **ADOPT/ADAPT** |
| SBPP-BEH-21 | Mediating Protocol | **ADOPT** |
| SBPP-BEH-22 | Super | **ADOPT/ADAPT** |
| SBPP-BEH-23 | Extending Super | **ADOPT** |
| SBPP-BEH-24 | Modifying Super | **ADAPT** |
| SBPP-BEH-25 | Delegation | **ADOPT** |
| SBPP-BEH-26 | Simple Delegation | **ADOPT** |
| SBPP-BEH-27 | Self Delegation | **ADOPT/ADAPT** |
| SBPP-BEH-28 | Pluggable Behavior | **ADOPT** |
| SBPP-BEH-29 | Pluggable Selector | **ADOPT** (adapted to method references) |
| SBPP-BEH-30 | Pluggable Block | **ADOPT** |
| SBPP-BEH-31 | Collecting Parameter | **ADOPT/ADAPT** |

## Pattern Sections (FPF E.8 Canonical Template)

Each file contains all 13 mandatory FPF sections:

1. Problem frame
2. Problem
3. Forces (table)
4. Solution — Java 17+ / Kotlin code examples
5. Archetypal Grounding (U.System + U.Episteme Tell–Show)
6. Bias-Annotation (Gov / Arch / Onto-Epist / Prag / Did)
7. Conformance Checklist (SHALL/SHOULD/MAY)
8. Common Anti-Patterns and How to Avoid Them
9. Consequences (benefits / trade-offs table)
10. Rationale
11. SoTA-Echoing (post-2015 sources; adopt/adapt/reject table)
12. Relations
13. Footer marker (:End)

## Key Themes in Chapter 3

- **Method design:** Composed Method, Method Object, Execute Around Method establish the
  method-level design vocabulary.
- **Naming:** Intention Revealing Selector is the single most impactful naming principle.
- **Polymorphism:** Message, Choosing Message, Dispatched Interpretation, Double Dispatch
  collectively replace procedural type-switching.
- **Reuse:** Delegation over inheritance; Pluggable Behavior replaces subclass proliferation.
- **Modern Java/Kotlin adaptations:** Sealed classes replace some Double Dispatch cases;
  Kotlin `by` delegation, `buildList`, and `fun interface` are first-class alternatives.
