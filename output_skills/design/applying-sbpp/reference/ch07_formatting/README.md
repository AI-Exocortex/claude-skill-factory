# Chapter 7: Formatting — Pattern Index

**Source:** Kent Beck, *Smalltalk Best Practice Patterns* (1997), Chapter 7  
**Adaptation:** Java 17+ / Kotlin 1.9+ microservice development  
**FPF Template:** E.8 Canonical Pattern Template  
**Patterns:** 10

## Adoption Verdicts

| ID | Pattern | Verdict | Modern Equivalent |
|----|---------|---------|-------------------|
| SBPP-FMT-01 | Inline Message Pattern | **ADOPT** | Formatter-enforced line-length wrapping |
| SBPP-FMT-02 | Type Suggesting Parameter Name | **ADOPT/ADAPT** | Role names, not type names (types are declared) |
| SBPP-FMT-03 | Indented Control Flow | **ADOPT** | Auto-formatter (ktlint / google-java-format) |
| SBPP-FMT-04 | Rectangular Block | **ADOPT/ADAPT** | Java/Kotlin lambda block formatting |
| SBPP-FMT-05 | Guard Clause | **ADOPT** | Early return / `require`/`check`/Elvis `?:` |
| SBPP-FMT-06 | Conditional Expression | **ADOPT** | Kotlin `if`-expression / Java switch expression |
| SBPP-FMT-07 | Simple Enumeration Parameter | **ADOPT/ADAPT** | Kotlin `it` / named lambda parameter |
| SBPP-FMT-08 | Cascade | **ADAPT** | Kotlin scope functions (`apply`/`also`/`let`) / Java Builder |
| SBPP-FMT-09 | Yourself | **REJECT/SUPERSEDED** | Kotlin `apply`/`also`; Java builder `return this` |
| SBPP-FMT-10 | Interesting Return Value | **ADOPT** | CQS principle; Kotlin expression bodies |

## Key Smalltalk → Java/Kotlin Mappings

| Smalltalk idiom | Java/Kotlin equivalent |
|-----------------|----------------------|
| Inline keyword pattern | Single-line signature; wrap one-per-line at limit |
| `aCollection` parameter | `collection` (role name; type is declared) |
| Multi-keyword indented message | Chained method call, each on own indented line |
| `[...]` block literal | Lambda `{ }` / trailing lambda |
| Guard `ifTrue: [^self]` | `if (!condition) return;` / `require(condition)` |
| Conditional expression `ifTrue: [...] ifFalse: [...]` | Kotlin `if`-expr / ternary / switch-expr |
| `:each` block parameter | Kotlin `it` / named lambda param |
| `;` cascade | Kotlin `apply`/`also`; Java Builder |
| `; yourself` | Kotlin `apply {}` / builder `return this` |
| Explicit `^self` return | `return this` (Java builder) / expression body (Kotlin) |

## The One Pattern to Teach First

**FMT-05 (Guard Clause)** delivers the highest value-to-effort ratio: it flattens deeply
nested code, reduces indentation levels, and makes the happy path immediately visible.
It is universally applicable and directly supported by Kotlin's `require`/`check`/`?: throw`.

## Tooling Automation

Three of these ten patterns are **fully automated** by standard tooling:

| Pattern | Tool |
|---------|------|
| FMT-01 (Inline Message Pattern) | ktlint / google-java-format / Checkstyle |
| FMT-03 (Indented Control Flow) | ktlint / IntelliJ auto-format |
| FMT-04 (Rectangular Block) | ktlint / IntelliJ auto-format |

Configure the formatter once; these patterns cost nothing thereafter.

## FPF Sections in Each File (all 13 mandatory)

1. Problem frame · 2. Problem · 3. Forces · 4. Solution (with Java/Kotlin examples)  
5. Archetypal Grounding · 6. Bias-Annotation · 7. Conformance Checklist  
8. Anti-Patterns · 9. Consequences · 10. Rationale · 11. SoTA-Echoing  
12. Relations · 13. `:End` marker
