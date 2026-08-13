---
name: elegant-objects
description: Apply Elegant Objects patterns to design, refactor, or review Java object-oriented code. Use when defining classes and interfaces, shaping construction and dependencies, improving immutability and encapsulation, removing null/static/type-switch hazards, designing tests, or managing exceptions and resource lifetimes.
---

# Elegant Objects

Use this skill to make Java object-oriented design decisions with the 23 source-derived patterns from Yegor Bugayenko's *Elegant Objects*. The patterns are deliberately opinionated. Treat them as lenses for exposing a design trade-off, not as blanket rules that override an existing project's constraints, framework requirements, or public API compatibility.

## Workflow

1. Identify the concrete design concern in the Java code or proposed change.
2. Load only the matching file from `reference/`; every reference contains the pattern rationale, consequences, anti-patterns, and bad-versus-good Java examples.
3. Compare the current code against the pattern's problem and conformance checklist.
4. Recommend the smallest change that improves the stated concern. State any deliberate departure from the pattern and why.
5. Preserve observable behavior unless the request explicitly changes it. Add or update behavior-focused tests when the change affects a contract.

## Pattern routing

### Construction and object identity

- Use [1.1 Never use -er names](reference/1.1%20Never%20use%20-er%20names.md) when a class is named `Manager`, `Handler`, `Formatter`, or another procedural role; name the represented object instead.
- Use [1.2 Make one constructor primary](reference/1.2%20Make%20one%20constructor%20primary.md) when several constructors establish the same state; delegate normalization to one state-writing constructor.
- Use [1.3 Keep constructors code-free](reference/1.3%20Keep%20constructors%20code-free.md) when construction performs parsing, I/O, or other work; compose a collaborator and defer execution to a requested method.

### Class boundaries, contracts, and collaboration

- Use [2.1 Encapsulate as little as possible](reference/2.1%20Encapsulate%20as%20little%20as%20possible.md) when a class has a large collaborator set or unclear responsibility; split coherent roles before hiding dependencies.
- Use [2.2 Encapsulate something](reference/2.2%20Encapsulate%20something.md) when a class is a stateless wrapper around globals or static calls; make its context an explicit collaborator.
- Use [2.3 Always use interfaces](reference/2.3%20Always%20use%20interfaces.md) when a client depends on a concrete implementation and a stable capability boundary is needed.
- Use [2.4 Choose method names carefully](reference/2.4%20Choose%20method%20names%20carefully.md) when method names or return types conceal whether they query a result or change the represented world.
- Use [2.5 Don't use public constants](reference/2.5%20Don't%20use%20public%20constants.md) when raw public constants carry domain semantics across classes; replace behavior-bearing values with a focused object.
- Use [2.6 Be immutable](reference/2.6%20Be%20immutable.md) when mutable state causes temporal coupling, partial failure, test fragility, or unsafe sharing; return a new value instead of changing an existing one.
- Use [2.7 Write tests instead of documentation](reference/2.7%20Write%20tests%20instead%20of%20documentation.md) when behavior is explained only by comments; add readable executable examples while retaining prose needed for rationale or operations.
- Use [2.8 Don't mock; use fakes](reference/2.8%20Don't%20mock;%20use%20fakes.md) when interaction mocks make tests brittle; use a small fake through the production interface when it can model the required behavior.
- Use [2.9 Keep interfaces short; use smarts](reference/2.9%20Keep%20interfaces%20short;%20use%20smarts.md) when an interface combines unrelated client needs; split it by role and add behavior through implementations or decorators.

### Behavior, dependencies, and polymorphism

- Use [3.1 Expose fewer than five public methods](reference/3.1%20Expose%20fewer%20than%20five%20public%20methods.md) when a class exposes a broad public API; use the count as a cohesion diagnostic, not a target to game.
- Use [3.2 Don't use static methods](reference/3.2%20Don't%20use%20static%20methods.md) when domain behavior is expressed as global or utility procedures; prefer an explicit object when composition or substitution matters.
- Use [3.3 Never accept NULL arguments](reference/3.3%20Never%20accept%20NULL%20arguments.md) when `null` gives a parameter a second, hidden meaning; make absence a separate operation, empty collection, or role-valid object.
- Use [3.4 Be loyal and immutable, or constant](reference/3.4%20Be%20loyal%20and%20immutable,%20or%20constant.md) when changing external observations are confused with changing object state; distinguish immutable state from time-dependent results.
- Use [3.5 Never use getters and setters](reference/3.5%20Never%20use%20getters%20and%20setters.md) when a domain object exposes storage rather than behavior; move state transitions and domain operations into the owning object.
- Use [3.6 Don't use new outside of secondary ctors](reference/3.6%20Don't%20use%20new%20outside%20of%20secondary%20ctors.md) when methods or primary constructors instantiate production dependencies; inject the needed role instead.
- Use [3.7 Avoid type introspection and casting](reference/3.7%20Avoid%20type%20introspection%20and%20casting.md) when code branches on `instanceof`, casts, or reflection; publish the needed role through a signature or use polymorphism.

### Failures, inheritance, and resources

- Use [4.1 Never return NULL](reference/4.1%20Never%20return%20NULL.md) when a method may return `null`; choose an explicit exception, empty plural result, or meaningful null object based on the contract.
- Use [4.2 Throw only checked exceptions](reference/4.2%20Throw%20only%20checked%20exceptions.md) when failure paths are hidden, discarded, or used as ordinary branching; retain the cause, add context, and recover only at an owning boundary. Adapt the pattern to the project's language and error model.
- Use [4.3 Be either final or abstract](reference/4.3%20Be%20either%20final%20or%20abstract.md) when inheritance leaves extension rights ambiguous; make a complete implementation final or make intended refinement explicit in an abstract base.
- Use [4.4 Use RAII](reference/4.4%20Use%20RAII.md) when files, streams, connections, or locks lack an obvious owner; bind Java resource release to `try`-with-resources or another explicit lifetime protocol.

## Guardrails

- Do not apply a pattern mechanically to framework adapters, generated code, serialization DTOs, or public APIs without checking their boundary constraints.
- Do not convert code solely to satisfy a heuristic count or naming convention.
- Distinguish source-derived advice from verified project requirements. Use tests, compilation, and relevant repository conventions as the evidence for a proposed change.
