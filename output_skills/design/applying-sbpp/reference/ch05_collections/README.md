# Chapter 5: Collections — Pattern Index

**Source:** Kent Beck, *Smalltalk Best Practice Patterns* (1997), Chapter 5  
**Adaptation:** Java 17+ / Kotlin 1.9+ microservice development  
**FPF Template:** E.8 Canonical Pattern Template  
**Patterns:** 28

## Adoption Verdicts at a Glance

| ID | Pattern | Verdict |
|----|---------|---------|
| SBPP-COL-01 | Collection | **ADOPT** |
| SBPP-COL-02 | OrderedCollection | **ADOPT** |
| SBPP-COL-03 | RunArray | **ADAPT** |
| SBPP-COL-04 | Set | **ADOPT** |
| SBPP-COL-05 | Equality Method | **ADOPT** |
| SBPP-COL-06 | Hashing Method | **ADOPT** |
| SBPP-COL-07 | Dictionary | **ADOPT** |
| SBPP-COL-08 | SortedCollection | **ADOPT** |
| SBPP-COL-09 | Array | **ADOPT/ADAPT** |
| SBPP-COL-10 | ByteArray | **ADOPT** |
| SBPP-COL-11 | Interval | **ADOPT** |
| SBPP-COL-12 | IsEmpty | **ADOPT** |
| SBPP-COL-13 | Includes | **ADOPT** |
| SBPP-COL-14 | Concatenation | **ADOPT** |
| SBPP-COL-15 | Enumeration | **ADOPT** |
| SBPP-COL-16 | Do | **ADOPT** |
| SBPP-COL-17 | Collect | **ADOPT** |
| SBPP-COL-18 | Select/Reject | **ADOPT** |
| SBPP-COL-19 | Detect | **ADOPT** |
| SBPP-COL-20 | Inject:into: | **ADOPT** |
| SBPP-COL-21 | Duplicate Removing Set | **ADOPT** |
| SBPP-COL-22 | Temporarily Sorted Collection | **ADOPT** |
| SBPP-COL-23 | Stack | **ADOPT** |
| SBPP-COL-24 | Queue | **ADOPT** |
| SBPP-COL-25 | Searching Literal | **ADOPT** |
| SBPP-COL-26 | Lookup Cache | **ADOPT** |
| SBPP-COL-27 | Parsing Stream | **ADOPT/ADAPT** |
| SBPP-COL-28 | Concatenating Stream | **ADOPT** |

## Key Modern Mappings

| Smalltalk Pattern | Java/Kotlin Equivalent |
|-------------------|----------------------|
| `OrderedCollection` | `ArrayList` / `buildList {}` |
| `Set` | `HashSet` / `Set.of()` / `setOf()` |
| `Dictionary` | `HashMap` / `Map.of()` / `mapOf()` |
| `SortedCollection` | `stream().sorted()` / `sortedWith()` |
| `do:` | for-each / `forEach` |
| `collect:` | `stream().map()` / `.map {}` |
| `select:` / `reject:` | `stream().filter()` / `.filter {}` / `.filterNot {}` |
| `detect:` | `stream().findFirst()` / `.find {}` |
| `inject:into:` | `stream().reduce()` / `fold` / `sumOf` |
| Literal set search | `Set.of().contains()` / `in setOf()` |
| Concatenating Stream | `StringBuilder` / `buildString {}` / `joinToString` |
| Parsing Stream | `BufferedReader.lines()` / `readLines()` |

## Critical Correctness Rules

1. **equals + hashCode always together** (COL-05, COL-06) — use records/data classes
2. **Set/Map keys must be immutable** (COL-07) — mutable keys cause "lost entry" bugs  
3. **Defensive copy for byte[]** (COL-10) — `Arrays.copyOf()` in constructor and accessor
4. **isEmpty() not size()==0** (COL-12) — correct semantics and potentially more efficient
5. **fold over reduce** (COL-20) — fold handles empty collections safely
