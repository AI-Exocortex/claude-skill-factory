# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository is a skill creation system for Claude Code. It provides:
- **Knowledge base**: Official Anthropic documentation on creating skills (`docs/knowledge/anthropic-skill-docs/`)
- **Output directory**: Completed skills organized by name (`output_skills/`)

## Common Commands

**Update documentation** (fetch latest from Anthropic):
```bash
./update-docs
```

**Manually run fetch script**:
```bash
uv run scripts/fetch_anthropic_skill_docs.py
```

## Architecture

The repository follows a separation between **knowledge** (how to create skills) and **output** (created skills):

```
docs/knowledge/anthropic-skill-docs/  # Reference documentation
    ├── overview.md                   # Core concepts
    ├── skills.md                     # Implementation patterns
    ├── best-practices.md             # Guidelines and pitfalls
    └── quickstart.md                 # Getting started

output_skills/                        # Created skills
    └── [skill-name]/                 # Each skill in its own folder
```

**Documentation update workflow**:
1. URLs listed in `scripts/sources.txt`
2. `scripts/fetch_anthropic_skill_docs.py` fetches from those URLs
3. Markdown files saved to `docs/knowledge/anthropic-skill-docs/`

## Creating Skills

When creating new skills:
1. Read documentation in `docs/knowledge/anthropic-skill-docs/` for official patterns
2. Save completed skill to `output_skills/[skill-name]/`
3. Each skill should be self-contained in its own directory

Refer to `docs/map.md` for complete repository structure.
