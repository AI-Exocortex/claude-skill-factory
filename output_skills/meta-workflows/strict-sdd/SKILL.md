---
name: strict-sdd
description: Orchestrates OpenSpec and Superpowers for complete spec-driven development lifecycle.
---

# Disciplined Specification-Driven Development

STARTER_CHARACTER = 📐

## Workflow Integration

This skill orchestrates interoperability between skill providers:
- **opsx**: Structure, format, artifact locations
- **Superpowers**: Process discipline and workflows
- **Technical Skills**: Implementation techniques (TDD, Approvals, BDD)

Each phase respects opsx format requirements while following superpowers processes.

## Steps

### 1. Exploration/Brainstorming (Optional)

Only if user explicitly mentions brainstorming.

Invoke `opsx:explore` + `superpowers:brainstorming`:
- Maximum 10 questions to crystallize the idea
- Stop earlier if additional questions won't add value
- Continue until idea has sufficient shape for specification

### 2. Specs Creation

Invoke `opsx:continue` (first invocation) + `collaborative-design`:
- Creates specs artifact (scenarios)
- Format and location dictated by opsx

### 3. Design Creation

Invoke `opsx:continue` (second invocation):
- Creates technical/architectural design document
- Use gathered context from brainstorming and specs phases
- Format and location dictated by opsx

### 4. Tasks Creation

Invoke `opsx:continue` (third invocation) + `superpowers:writing-plans`:
- Write to opsx's specified location (tasks.md)
- **CRITICAL**: Do NOT output code snippets
- Each task specifies skill invocations + context:
  ```
  Task 1: Implement user authentication
  - Invoke: superpowers:test-driven-development
  - Invoke: approval-tests
  - Context: Email/password login with JWT tokens
  ```

### 5. Implementation

Invoke `opsx:apply`:
- Delegates to superpowers implementation skill
- Implementation skill chooses execution strategy:
  - `superpowers:subagent-driven-development` (parallel)
  - `superpowers:executing-plans` (sequential with checkpoints)
- Tasks invoke technical skills as specified (tdd, approval-tests, bdd-with-approvals, etc.)
- **Mark each task done in tasks.md after completion**
- Keep plan synchronized in real-time

### 6. Pre-Finalization Review & Finalization

Before finalization:
1. Verify all tasks in tasks.md are marked completed
2. Document deviations from original plan
3. Document amendments made during implementation
4. Document non-trivial decisions or architectural choices
5. Wait for user confirmation

Then invoke `superpowers:finishing-a-development-branch`.

Tasks.md and plan artifacts MUST be updated before finalization.

### 7. Archive

Automatically after finalization completes.

Invoke `opsx:archive` to formally close the specification.
