# Important Notes for This Repo

## No Markdown Tables in Skill Files

Don't use markdown tables in SKILL.md or reference files. Use lists or prose instead.

Tables require rendering to read easily. In terminal, raw markdown tables are hard to scan.

## Light Formatting

Avoid heavy use of bold (`**text**`). Use sparingly for actual emphasis, not for every list item header.

- Do: Plain list items with periods between parts
- Not: **Bold header** - explanation for every item

Bold everywhere creates visual noise and loses its emphasis effect.

## approval-tests: 2-Level Reference Depth is Intentional

The approval-tests skill has this structure:
```
SKILL.md → python.md → references/python/*.md
           nodejs.md → references/nodejs/*.md
           java.md   → references/java/*.md
```

This is 2 levels deep from SKILL.md, not 1. This is **intentional, not a bug**.

**Why:** The three languages have very different implementations. The middle layer (python.md, nodejs.md, java.md) acts as a language router, keeping SKILL.md clean of language-specific details. Without this, SKILL.md would be polluted with implementation differences that only matter to users of specific languages.

## Write for Claude, Not Humans

Skills are consumed by Claude, not end users. Avoid:

- Question-based formatting ("Need X? Do Y")
- Leading language ("When you want to...", "If you need...")
- Hand-holding phrasing that assumes the reader needs guidance

Claude is smart. Just state what things are and what they do:

- Not: "Verifying an object? Use verify_as_json()"
- Do: "Objects → verify_as_json()"

- Not: "When to go deeper: [api.md] - Need verify_xml..."
- Do: "[api.md] - verify_xml, verify_html, Storyboard..."

Be succinct. State facts. Trust Claude to figure out when to apply them.

## links.md shouldn't be linked from anywhere - they are for you for when you're writing the skill