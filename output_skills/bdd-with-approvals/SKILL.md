---
name: bdd-with-approvals
description: Living specifications using approval tests instead of Gherkin. Use when writing BDD acceptance tests, system tests, e2e tests, or integration tests where you want scannable domain-level specs without Gherkin's step definition overhead.
---

# BDD with Approval Tests

Alternative to Gherkin for BDD-level tests. The fixture file is the living specification.

## Why Not Gherkin

Gherkin couples to implementation through step definitions. When things change, those wrappers break. Given/When/Then often ends up at implementation level—feels like unit tests, hard to scan.

Approval fixtures express behavior at domain level. A human looks at it and immediately sees: correct or not. No step definitions to maintain.

## When to Use

System-level tests:
- End-to-end with real infrastructure
- Integration tests with nulled infrastructure (see `/nullables`)
- Acceptance tests proving a feature works as specified

For the approval testing technique itself (verify, scrubbers, combinations), see `/approval-tests`.

## Core Pattern

Approval files combine input and expected output in a format designed for human validation:

```
## Input
context, parameters, initial state

## Output
expected results, side effects, final state
```

One test runner reads all fixtures, executes code, compares output. Adding test cases = adding files, not code.

See [references/approved-fixtures.md](references/approved-fixtures.md) for examples.

## Format Design

**Core question:** Can someone validate correctness in <5 seconds?

Design for human eyes, not machine parsing. Match how you'd explain it on a whiteboard.

**What makes formats scannable:**
- Columnar layouts with visual alignment
- Consistent structure across all cases
- Whitespace that groups related elements
- Symbolic notation matching the domain

**Formats by domain:**
- Grid/spatial: ASCII art
- Transformations: before/after
- Workflows: step sequences with results
- API calls: request/response pairs

**Avoid:**
- Dense JSON
- Single-line formats
- Formats requiring mental parsing

## Implementation

**One-time setup per domain:**
1. Parser: extracts input from fixture format
2. Formatter (printer): converts actual output to fixture format
3. Test runner: discovers fixtures, executes, compares

Keep parser/formatter simple. Format should mirror natural representation.

## Approved Logs

Alternative: turn structured logs into tests by copying and fixing incorrect lines. Useful for quick bug reproduction.

**Caveat:** Creates coupling—log format changes break tests. Use sparingly when logs happen to capture behavior well.

See [references/approved-logs.md](references/approved-logs.md).
