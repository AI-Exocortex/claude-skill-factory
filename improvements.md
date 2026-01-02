# Nullables Skill Improvements

## Structure Improvements

- [ ] **Separate "thinking" from "building"** — The skill mixes philosophy with implementation. Consider reorganizing into:
  1. Core Concepts (what, why) — keep in SKILL.md
  2. Building Patterns (how) — extract more to references

- [ ] **Make A-Frame more prominent** — It's the architectural foundation but appears after examples. Move up or make clearer that this is the prerequisite pattern.

- [ ] **Add a "Quick Start" workflow** — After reading, Claude should know the exact steps. Something like:
  1. Identify infrastructure code
  2. Create wrapper with create()/createNull()
  3. Add embedded stub
  4. Add output tracking
  5. Write tests using createNull()

## Anti-Patterns Section

- [ ] **Add "Stub Drift" anti-pattern** — Embedded stubs can diverge from real infrastructure behavior. Solution: Narrow Integration Tests.

- [ ] **Add "God Class" warning for Traffic Cop** — Event-driven architectures can become monolithic. Split into modules when handlers grow.

- [ ] **Add "Overbuild" warning** — Don't build generic stub features that aren't test-driven through your code's public interface.

## Reference Files

- [ ] **Add table of contents to longer reference files** — embedded-stubs.md is 317 lines, infrastructure-wrappers.md is 402 lines. Adding TOCs at top helps Claude navigate if it does partial reads.

- [ ] **Consolidate architecture references** — a-frame.md (78 lines), logic-sandwich.md (110 lines), and event-driven.md (112 lines) could potentially be merged into one file since they're conceptually connected.

## Examples

- [ ] **Show failure case in main example** — Current CommandLine example only shows success. Add one test showing error configuration.

- [ ] **Add Python example** — All examples are JavaScript. The pattern is language-agnostic; showing a second language would reinforce this.

## Output Tracking Reference

- [ ] **Simplify OutputListener in SKILL.md** — The inline OutputListener code (lines 117-145 in command_line example) is implementation detail. The concept is what matters; the implementation belongs in the reference.

## Test Patterns Reference

- [ ] **Add "expect.any()" portability warning more prominently** — The note about Jest-specific matchers is buried at the end. Move to where timestamp examples appear.

## Migration Reference

- [ ] **Add concrete "Find mocks" commands for more frameworks** — Currently only shows generic grep. Add specific patterns for Jest, Sinon, etc.
