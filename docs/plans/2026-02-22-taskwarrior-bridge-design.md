# Taskwarrior Bridge Skill — Design

**Date**: 2026-02-22
**Target**: `/Users/eugene/Dev/pers-dev/.claude/skills/taskwarrior-bridge/SKILL.md`
**Type**: Workflow-driven skill (Approach 1)

## Problem

The pers-dev vault tracks projects, problems, hypotheses, and observations as markdown files with frontmatter. Task execution is informal — markdown checklists inside PROJ-*.md files. There's no execution engine with urgency scoring, filtering, dependencies, or reporting.

Taskwarrior provides all of that but has no awareness of the vault's semantic structure (contexts, problem severities, lifecycle phases).

## Solution

A Claude Code skill that bridges the vault's knowledge base with Taskwarrior's execution engine. Claude reads both sources, reasons over them, and executes Taskwarrior commands while keeping vault files in sync.

## Project Mapping

```
Vault Context (CTX-*.md)  →  Taskwarrior top-level project
Vault Project (PROJ-*.md) →  Taskwarrior sub-project under its context

CTX-LLM-Engineering-Automation  →  LLM-Engineering
PROJ-Build-FPF-MCP-Linter       →  LLM-Engineering.MCP-Linter
```

Rules:
- Strip prefixes (CTX-, PROJ-) and .md extension
- Use PROJ frontmatter `context` field to determine parent
- Simplify names (drop redundant words)
- Tag tasks with FPF lifecycle phase (+execution, +reasoning, etc.)
- Annotate tasks with vault file path for sync traceability

## Priority Derivation

- PROB severity 4-5 → priority:H
- PROB severity 2-3 → priority:M
- PROB severity 1 or unlinked → priority:L
- Active PROJ status boosts; archived deprioritizes

## Six Workflows

### 1. Create Task
Read PROJ file → extract/create checklist items → `task add` with derived project, tags, priority → annotate with vault path

### 2. Create Project + Task
Identify best CTX context → create PROJ-*.md from template → add checklist → create Taskwarrior project + first task

### 3. Next Task (Combined Intelligence)
`task next` urgency list + active PROJ files + PROB severities + recent OBS → top 3 recommendations with rationale

### 4. Manage Priorities
`task summary` + vault PROB severities → identify mismatches → suggest adjustments → apply after confirmation

### 5. Report
`task stats` + `task summary` + `task burndown.weekly` + vault artifact counts → combined dashboard

### 6. Sync (Two-Way)
Export Taskwarrior tasks with vault annotations → diff against PROJ checklist items → reconcile both directions → apply after showing diff

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project hierarchy | Dot notation (CTX.PROJ) | Matches Taskwarrior's native hierarchy; allows filtering by context |
| Priority source | Derived from vault | Keeps vault as source of truth for importance |
| Next-task logic | Combined intelligence | Neither source alone has full picture |
| Sync direction | Two-way | Vault and Taskwarrior both get used directly |
| Invocation scope | From within pers-dev only | Skill reads .md files relative to CWD |
| Skill structure | Single SKILL.md | Vault itself is the reference; no need for separate docs |

## Out of Scope (for v1)

- Recurring task management (can add later)
- Taskwarrior hooks/automation scripts
- UDA definitions (keep it vanilla Taskwarrior)
- Time tracking
