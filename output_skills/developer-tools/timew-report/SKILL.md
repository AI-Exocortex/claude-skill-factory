---
name: timew-report
description: Queries Timewarrior for time statistics and updates pers-dev PROJ files with time summaries. Use when reviewing hours spent today, over the last 7 or 30 days, or logging tracked time into vault project files.
---

STARTER_CHARACTER = ⏱️

# Timew Report

Surfaces Timewarrior time-tracking data for three rolling windows and writes cumulative per-project totals into pers-dev vault PROJ files as a `time_tracked:` frontmatter field.

## Commands

```bash
timew summary :day                                                        # today
timew summary $(date -v-7d +%Y-%m-%d) to $(date +%Y-%m-%d)               # last 7 days
timew summary $(date -v-30d +%Y-%m-%d) to $(date +%Y-%m-%d)              # last 30 days
timew summary :all "<tag-name>"                                           # all-time total for one tag
timew export                                                              # raw JSON intervals
```

Note: date syntax uses macOS BSD `date`. Linux equivalent: `date -d '-7 days' +%Y-%m-%d`.

## Workflow: Display Stats

1. Run all three summaries.
2. Group tags by the vault PROJ they map to (use the tag-to-PROJ mapping from Step 1 of Update PROJ Files below). Tags with no PROJ mapping go under **Untracked**.
3. Present:
   - Per-period totals (today / 7 days / 30 days)
   - Most-active tracked project
   - Daily average trend: 7-day avg vs 30-day avg

## Workflow: Update PROJ Files

Writes cumulative all-time tracked hours into the frontmatter of pers-dev vault project files.

### Step 1 — Build tag-to-PROJ mapping

1. Run `task export` to get all Taskwarrior tasks.
2. For each task with a `vault:` annotation, note its `description` — this becomes the Timewarrior tag when `task start` is called — and the PROJ file path from the annotation.
3. Build a map: `timew-tag → PROJ-file-path`. Tasks without a `vault:` annotation cannot be mapped; list their tags as **unmatched** in the report.

### Step 2 — Sum time per PROJ file

For each mapped tag, get its all-time total:

```bash
timew summary :all "<tag-name>"
```

Read the `Total` value from the summary output. Sum totals across all tags that share the same PROJ file.

### Step 3 — Update frontmatter

Add or update `time_tracked:` in each PROJ file's YAML frontmatter. Place it after `status:`. Express as `Xh Ym` (e.g. `3h 12m`).

```yaml
time_tracked: "3h 12m"
```

Replace the existing value if present. Do not modify any other frontmatter field or body content.

Confirm with the user before writing if more than 3 PROJ files would be updated.

## Notes

- `time_tracked:` holds cumulative all-time totals, not window-scoped values.
- `:week` and `:month` hints use calendar boundaries; use explicit date ranges for rolling windows.
- If Timewarrior is not installed: `brew install timewarrior`
