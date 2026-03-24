# Chapter 4: State — Pattern Index

**Source:** Kent Beck, *Smalltalk Best Practice Patterns* (1997), Chapter 4  
**Adaptation:** Java 17+ / Kotlin 1.9+ microservice development  
**FPF Template:** E.8 Canonical Pattern Template  
**Patterns:** 20

## Adoption Verdicts at a Glance

| ID | Pattern | Verdict |
|----|---------|---------|
| SBPP-STA-01 | Common State | **ADOPT** |
| SBPP-STA-02 | Variable State | **REJECT** (domain) / **ADOPT** (metadata) |
| SBPP-STA-03 | Explicit Initialization | **ADOPT** |
| SBPP-STA-04 | Lazy Initialization | **ADOPT/ADAPT** |
| SBPP-STA-05 | Default Value Method | **ADOPT** |
| SBPP-STA-06 | Constant Method | **ADOPT** |
| SBPP-STA-07 | Direct Variable Access | **ADOPT** |
| SBPP-STA-08 | Indirect Variable Access | **ADOPT** |
| SBPP-STA-09 | Getting Method | **ADOPT** |
| SBPP-STA-10 | Setting Method | **ADOPT/ADAPT** |
| SBPP-STA-11 | Collection Accessor Method | **ADOPT** |
| SBPP-STA-12 | Enumeration Method | **ADOPT** |
| SBPP-STA-13 | Boolean Property Setting Method | **ADOPT** |
| SBPP-STA-14 | Role Suggesting Instance Variable Name | **ADOPT** |
| SBPP-STA-15 | Temporary Variable | **ADOPT** |
| SBPP-STA-16 | Collecting Temporary Variable | **ADOPT/ADAPT** |
| SBPP-STA-17 | Caching Temporary Variable | **ADOPT** |
| SBPP-STA-18 | Explaining Temporary Variable | **ADOPT** |
| SBPP-STA-19 | Reusing Temporary Variable | **ADOPT** |
| SBPP-STA-20 | Role Suggesting Temporary Variable Name | **ADOPT** |

## Key Themes

- **Instance variables:** Common State (typed fields) vs Variable State (maps — avoid for domain).
  Java records and Kotlin data classes are the modern expression of Common State.
- **Initialization:** Explicit (always-set) vs Lazy (on-demand). Kotlin `by lazy` is the idiomatic
  lazy init. Direct/Indirect access are two strategies for intra-class field use.
- **Accessors:** Getting Methods (defensive copies for collections), Setting Methods (replaced by
  domain state-transition methods in DDD), Collection Accessor (controlled add/remove).
- **Naming:** Role-based names for both fields (STA-14) and locals (STA-20) — no Hungarian
  notation, no type suffixes, no generic names.
- **Temporary variables:** Four specialised uses — Collecting, Caching, Explaining, Reusing —
  each with a distinct justification.

## Modern Java/Kotlin Adaptations

| Beck's pattern | Modern Java/Kotlin equivalent |
|----------------|-------------------------------|
| Property list (Variable State) | Kotlin nullable `T?`, sealed subclasses |
| Explicit Initialization | Java record compact constructor, Kotlin `init` block |
| Lazy Initialization | Kotlin `by lazy`, Java DCL with `volatile` |
| Setting Method | Kotlin `data class copy()`, domain state-transition methods |
| Collecting Temporary | Kotlin `buildList {}`, Java `stream().collect()` |
| Enumeration Method | Java `Stream<T>`, Kotlin `Sequence<T>` |
