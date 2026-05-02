---
name: skill-structure-creation
description: |
  Create new skills following the proper directory structure with SKILL.md, examples.md, and troubleshooting.md files.
  Use when: creating a new skill, extracting knowledge from a session, documenting a reusable pattern.
  Example triggers: "create a skill for this", "save this as a skill", "extract this pattern as a skill".
---

# Skill Structure Creation

## When to Use

- Creating a new skill to document a reusable pattern
- User asks to "create a skill" or "save this as a skill"
- Extracting knowledge from a completed session
- Documenting a solved problem for future reference

## Instructions

### 1. Create Directory Structure

Skills must be directories with three files, not single markdown files:

```bash
mkdir -p ~/.claude/skills/<skill-name>/
```

**Naming convention**:
- Use kebab-case (lowercase with hyphens)
- Be specific and searchable (e.g., `kaydet-work-report-generation` not `report-generation`)
- Focus on the problem, not the solution (e.g., `python-venv-macos-homebrew` not `fix-venv`)

### 2. Create SKILL.md with Frontmatter

The main skill file MUST have YAML frontmatter:

```markdown
---
name: skill-name
description: |
  What it does. When to use it.
  Use when: specific scenarios.
  Example triggers: "user phrase 1", "user phrase 2".
---

# Skill Display Name

## When to Use

[Specific scenarios and triggers]

## Instructions

[Step-by-step guidance with exact commands]

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| [Approach] | [Error/Problem] | [What to do instead] |

## Common Mistakes

- **Don't**: [What not to do]
  **Instead**: [What to do]
  **Why**: [Reason]

## See Also

- [Examples](examples.md) - Real examples demonstrating this skill
- [Troubleshooting](troubleshooting.md) - Error → solution mappings
```

**Description guidelines**:
- First sentence: What the skill does
- "Use when:" with specific scenarios
- Include exact error messages if applicable
- Add phrases users might say
- Maximum 1024 characters

### 3. Create examples.md

Document real examples from sessions:

```markdown
# Examples

Real examples from sessions demonstrating this skill. This file grows over time as new sessions contribute examples.

---

## Example: [Short Title]

**Context**: [What user was trying to do]

### Problem

[What went wrong or was needed]

### Solution

[Exact solution: code, commands, or configs]

### Why This Works

[Brief explanation]

---
```

### 4. Create troubleshooting.md

Document error cases and solutions:

```markdown
# Troubleshooting

Error → solution mappings for quick reference. This file grows over time as new error cases are discovered.

---

## Error: [Exact error message]

**Symptom**: [What you see]

**Cause**: [Why it happens]

**Solution**:
[How to fix it]

---
```

**Note**: Only create this file if there were actual errors encountered during the session.

### 5. Verify Structure

```bash
ls -la ~/.claude/skills/<skill-name>/
# Should show: SKILL.md, examples.md, troubleshooting.md (if errors occurred)
```

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| Creating a single `.md` file at `~/.claude/<project>/skills/skill-name.md` | Skills must be directories with multiple files (SKILL.md, examples.md, troubleshooting.md) following the template structure | Always create a directory with the three-file structure, not a single markdown file |
| Writing skill content without frontmatter | The `name` and `description` fields in frontmatter are required for skill discovery and indexing | Always include YAML frontmatter with `name` and `description` fields at the top of SKILL.md |
| Omitting the "Failed Attempts" table | This is the most valuable section - it documents what NOT to do, preventing wasted time in future sessions | Always include a "Failed Attempts" table, even if you have to reconstruct it from the session transcript |

## Common Mistakes

- **Don't**: Create a single markdown file like `skill-name.md`
  **Instead**: Create a directory `skill-name/` with `SKILL.md`, `examples.md`, and optionally `troubleshooting.md`
  **Why**: Skills need structured components that can grow over time

- **Don't**: Write generic descriptions like "Helps with API errors"
  **Instead**: Write specific descriptions with triggers: "Resolve OpenAI API rate limit (429) and timeout errors. Use when: encountering RateLimitError..."
  **Why**: Specific descriptions enable better skill discovery and matching

- **Don't**: Skip the Failed Attempts section
  **Instead**: Document what didn't work, even if it means reviewing the transcript
  **Why**: Failed attempts are often more valuable than successful approaches - they prevent wasted time

- **Don't**: Use vague instructions like "Configure the system properly"
  **Instead**: Provide exact commands with flags: `kaydet config show` to check current config
  **Why**: Future sessions need concrete, actionable guidance

## See Also

- [Examples](examples.md) - Real examples of skill creation
- [Troubleshooting](troubleshooting.md) - Common issues when creating skills

