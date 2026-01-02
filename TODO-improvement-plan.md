# Approval-Tests Skill Improvement Plan (Python Focus)

## Analysis Summary

### Current Structure
```
approval-tests/
├── SKILL.md (89 lines) - Main entry, philosophy, workflow
├── python.md (81 lines) - Language router with quick start
├── nodejs.md, java.md - Other language routers
├── links.md - Source references (not linked, for authoring only)
├── references/
│   ├── patterns/
│   │   ├── combinations.md (161 lines) - Cross-language combinations
│   │   └── testing-patterns.md (179 lines) - Cross-language patterns
│   └── python/
│       ├── api.md (152 lines) - Full API reference
│       ├── setup.md (222 lines) - Installation, config, reporters
│       ├── scrubbers.md (196 lines) - Scrubber reference
│       ├── inline.md (134 lines) - Inline approvals
│       ├── logging.md (130 lines) - Logging verification
│       ├── combinations.md (99 lines) - Python combinations
│       └── patterns.md (252 lines) - Testing patterns
```

### What's Working Well
1. Progressive disclosure structure (SKILL.md → python.md → references)
2. 2-level depth for language router (intentional per important.md)
3. TOC in most reference files
4. Good emoji (📸)
5. Anti-patterns section
6. links.md not linked from anywhere (correct)

## Identified Improvements

### 1. Remove Cross-Language Pattern Files
**Problem:** SKILL.md links to `references/patterns/combinations.md` and `testing-patterns.md`, which contain mixed Python/JS/Java examples. But Python-specific equivalents exist in `references/python/`. This:
- Creates confusion about which file to load
- Loads irrelevant language examples into context
- Violates knowledge composition (focused, composable files)

**Solution:** Remove cross-language patterns section from SKILL.md. Python users get patterns via python.md routing.

### 2. Add Missing Table of Contents
**Problem:** Best practices say long reference files (>100 lines) should have TOC so Claude sees full scope even with partial reads.

**Missing TOC:**
- api.md (152 lines) - Needs TOC
- combinations.md (99 lines) - Close to threshold, would benefit

### 3. Reduce Bold Header Overuse
**Problem:** important.md says avoid heavy bold formatting. Some files use bold for every list item header.

**Files to check:**
- api.md uses "**verify()** - Basic..." pattern (acceptable for API signatures)
- Review other files for excessive bolding

### 4. Content Overlap Between patterns.md and Specialized Files
**Problem:** patterns.md duplicates content from inline.md, logging.md, combinations.md. This could:
- Create confusion about which to reference
- Bloat context when patterns.md is loaded

**Solution:** patterns.md should reference specialized files more, keep only summary. Current approach seems reasonable but worth reviewing.

### 5. Python Combinations File Enhancement
**Problem:** Python combinations.md (99 lines) could benefit from parity with the more detailed cross-language version while removing non-Python content.

### 6. Verify pytest Integration Documentation
**Problem:** The setup.md mentions pytest-approvaltests plugin but could be clearer about when it's needed vs optional.

## Implementation Order

1. **Add TOC to api.md and combinations.md** - Low risk, clear improvement
2. **Update SKILL.md to remove cross-language patterns links** - Clarifies structure
3. **Review bold formatting across all Python files** - Consistency
4. **Consider merging useful content from cross-language patterns into Python-specific files** - Then remove cross-language files

## Commits

Each improvement should be a separate commit as per TASK.md instructions.
