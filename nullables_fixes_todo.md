# Nullables Skill: Issues and Improvements

Organized by progressive disclosure: SKILL.md stays lean, references hold depth.

---

## 1. SKILL.md Changes (Keep Lean)

### Description Field
- [ ] Reword to be clearer: "Helps write tests without mocks using James Shore's Nullables pattern. Use when testing infrastructure, avoiding mock libraries, or designing testable wrappers."
- [ ] Add natural triggers: "infrastructure isolation", "testable design", "dependency injection alternative", "fakes"

### Add One-Liner Pointers (with links to new/existing references)
- [ ] Add pointer to architecture patterns: "For structuring apps around Nullables, see [architecture.md](references/architecture.md)"
- [ ] Add pointer to migration: "For converting mock-based code, see [migration.md](references/migration.md)"
- [ ] Add "Sociable Tests" as one sentence in intro: "Tests run real code; only infrastructure is nulled."

### Fix Inconsistencies
- [ ] Replace inline `EventEmitter` example (lines 74-95) with `OutputListener` pattern from source repos - or just reference output-tracking.md
- [ ] Update Clock example date from `2024-01-15` to something neutral like `2020-01-01`

### Add Missing Anti-Patterns (brief, one line each)
- [ ] "Don't import mock libraries (sinon, jest.mock) - Nullables replace them"
- [ ] "Don't write broad end-to-end tests - sociable unit tests provide coverage"

### Remove/Trim
- [ ] Review if any explanations are things Claude already knows (e.g., "Unlike mocks (test-only constructs)..." - is this needed?)

---

## 2. New Reference Files to Create

### references/architecture.md (NEW)
Content to include:
- [ ] A-Frame Architecture - Logic and Infrastructure as peers under Application
- [ ] Logic Sandwich pattern - read → process → write
- [ ] Traffic Cop pattern - Observer variant for event-driven apps
- [ ] Diagram showing the structure
- [ ] When each pattern applies

### references/migration.md (NEW)
Content to include:
- [ ] Descend the Ladder - convert incrementally from top down
- [ ] Climb the Ladder - convert entire tree for simple cases
- [ ] Replace Mocks with Nullables - substitution strategy
- [ ] Throwaway Stub - temporary stubs during migration

---

## 3. Existing Reference File Improvements

### All reference files
- [ ] Add TOC to files over 100 lines (infrastructure-wrappers, embedded-stubs, test-patterns)

### references/output-tracking.md
- [ ] Align with source: show `OutputListener` as THE reusable utility (matches source repos)
- [ ] Fix `clear()` to return cleared data (matches source)

### references/configurable-responses.md
- [ ] Strengthen `mapObject()` example for HTTP endpoints
- [ ] Use factory `ConfigurableResponses.create()` consistently (not `new`)

### references/test-patterns.md
- [ ] Rename "Helper Functions" section to include term "Signature Shielding"
- [ ] Add explicit "Sociable Tests" subsection explaining the philosophy
- [ ] Add "Overlapping Tests" concept - tests naturally overlap, catching breaks in dependency chains
- [ ] Make "Narrow Integration Tests" more prominent (currently buried)
- [ ] Note that `expect.any(Number)` is Jest-specific, show portable alternative

### references/infrastructure-wrappers.md
- [ ] Add guidance: when NOT to create a wrapper (simple systems usable directly)
- [ ] Add: how to identify infrastructure boundaries

### references/embedded-stubs.md
- [ ] Add warning: don't over-complicate stubs, test-drive through wrapper's public interface

---

## 4. Terminology Consistency

- [ ] Pick "Nullables" (plural) as the pattern name, use consistently
- [ ] Capitalize pattern names consistently: "Embedded Stub", "Configurable Responses", "Output Tracking"

---

## 5. Evaluation & Testing

- [ ] Create 3 concrete evaluation scenarios per best-practices.md
- [ ] Test with Haiku, Sonnet, Opus to verify guidance level is appropriate
- [ ] Document what was tested

---

## Summary: Priority Order

**High (affects correctness/triggering):**
1. [ ] Fix description for better triggering
2. [ ] Fix OutputListener inconsistency (teaching wrong pattern)
3. [ ] Add Sociable Tests one-liner (core mental model)
4. [ ] Add missing anti-patterns (mock libraries, broad tests)

**Medium (completeness via progressive disclosure):**
5. [ ] Create references/architecture.md with A-Frame, Logic Sandwich, Traffic Cop
6. [ ] Create references/migration.md for legacy code conversion
7. [ ] Add TOC to long reference files
8. [ ] Add pointers in SKILL.md to new references

**Low (polish):**
9. [ ] Terminology consistency
10. [ ] Update date in example
11. [ ] Create evaluation scenarios

---

## Sources Referenced

| Resource | Used For |
|----------|----------|
| James Shore article | Missing concepts, patterns, anti-patterns |
| Simple example repo | OutputListener utility pattern |
| Complex example repo | ConfigurableResponses.mapObject, higher-level Nullables |
| best-practices.md | Progressive disclosure, conciseness, TOC guidance |
| skills.md | Description format, triggering |
| create_new_skill-process.md | Review checklist |
