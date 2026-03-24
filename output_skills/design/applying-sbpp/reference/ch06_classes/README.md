# Chapter 6: Classes — Pattern Index

**Source:** Kent Beck, *Smalltalk Best Practice Patterns* (1997), Chapter 6  
**Adaptation:** Java 17+ / Kotlin 1.9+ microservice development  
**FPF Template:** E.8 Canonical Pattern Template  
**Patterns:** 2

## Adoption Verdicts

| ID | Pattern | Verdict |
|----|---------|---------|
| SBPP-CLS-01 | Simple Superclass Name | **ADOPT** |
| SBPP-CLS-02 | Qualified Subclass Name | **ADOPT** |

## The Two Rules Together

These two patterns form a complete naming system for class hierarchies:

| Situation | Rule | Example |
|-----------|------|---------|
| Root / abstract type, or well-known concept | Simple Superclass Name | `Policy`, `Claim`, `Adjustment`, `RiskScorer` |
| Subtype that is a recognisable variant of its parent | Qualified Subclass Name | `PercentageAdjustment`, `MLRiskScorer`, `PolicyRepository` |
| Subtype with a universally well-known standalone name | Simple Superclass Name | `Invoice` (not `BillingDocument`), `SavingsAccount` (not `DepositAccount`) |

## Core Principle

> A class name must communicate two things: **what it is** (the concept) and,
> for subclasses, **how it differs** from its parent. No more, no less.

## What to Reject in Code Review

| Anti-pattern | Fix |
|-------------|-----|
| `AbstractPolicy`, `PolicyBase` | `Policy` |
| `ICalculator`, `CalculatorInterface` | `Calculator` |
| `PolicyEntity`, `ClaimModel` | `Policy`, `Claim` |
| `PolicyCalculatorV2` | `MLPolicyCalculator` (name the concept) |
| `HashMapPolicyIndex` | `PolicyIndex` (drop implementation detail) |
| `ClaimHandlerProcessor` | `ClaimProcessor` (pick one concept noun) |

## FPF Sections in Each File (all 13 mandatory)

1. Problem frame · 2. Problem · 3. Forces · 4. Solution (with Java/Kotlin examples)  
5. Archetypal Grounding · 6. Bias-Annotation · 7. Conformance Checklist  
8. Anti-Patterns · 9. Consequences · 10. Rationale · 11. SoTA-Echoing  
12. Relations · 13. `:End` marker
