# Examples

Real examples from sessions demonstrating proper skill creation. This file grows over time as new sessions contribute examples.

---

## Example: Kaydet Work Report Generation Skill (Incorrect Structure)

**Context**: User requested creation of a skill to generate work reports from kaydet logs for client invoicing.

### Problem

Claude created a single markdown file at:
- `~/.claude/mirat/skills/kaydet-work-report-generation.md`
- `~/.claude/valocom/skills/kaydet-work-report-generation.md`

This violated the proper skill structure which requires:
1. A directory: `~/.claude/skills/kaydet-work-report-generation/`
2. Three files: `SKILL.md`, `examples.md`, `troubleshooting.md`
3. YAML frontmatter in SKILL.md

The created file was comprehensive (250+ lines) with good content, but:
- No frontmatter with `name` and `description` fields
- No "Failed Attempts" table documenting what didn't work
- No separate examples or troubleshooting files
- Not in the user-level skills directory (`~/.claude/skills/`)

### Solution

The correct structure should have been:

```bash
# Create directory
mkdir -p ~/.claude/skills/kaydet-work-report-generation/

# Create three files
touch ~/.claude/skills/kaydet-work-report-generation/SKILL.md
touch ~/.claude/skills/kaydet-work-report-generation/examples.md
touch ~/.claude/skills/kaydet-work-report-generation/troubleshooting.md
```

**SKILL.md** should start with:
```markdown
---
name: kaydet-work-report-generation
description: |
  Generate professional work reports for client invoicing from kaydet time-tracking logs and git metrics.
  Use when: creating monthly invoices, generating work reports, user mentions "fatura" or "work report".
  Example triggers: "generate work report from kaydet", "ocak ayı için fatura", "create invoice for January".
---

# Kaydet-Based Work Report Generation

```

**Failed Attempts table** should document:
- Initially searched `~/.local/share/kaydet/` when logs were actually in `~/Documents/Kaydet/`
- Assumed kaydet location instead of checking `kaydet config show`

**examples.md** should include:
- The January 2026 report generation as a concrete example
- Show the actual commands used and output generated

**troubleshooting.md** should include:
- "Error: No kaydet logs found" → Check actual kaydet config location
- How to handle missing days or sick days in billing

### Why This Matters

Proper structure enables:
1. **Discoverability**: Frontmatter `description` is used for skill matching
2. **Growth**: `examples.md` and `troubleshooting.md` can grow over time
3. **Versioning**: Version history tracks evolution
4. **Attribution**: Clear session sources for verification
5. **Failure learning**: Failed Attempts prevent repeating mistakes

---

## Example: Correct Multi-Instance Skill Creation

**Context**: User had two Claude instances (`mirat` and `valocom`) and wanted the skill available to both.

### Problem

User expected the skill to be created in project-specific locations:
- `~/.claude/mirat/skills/`
- `~/.claude/valocom/skills/`

However, this violates the principle that skills should be user-level, not project-level.

### Solution

Skills should be created in the user-level directory:
```bash
mkdir -p ~/.claude/skills/skill-name/
```

Not in project-specific directories:
```bash
# ❌ Wrong - project-specific
~/.claude/mirat/skills/skill-name.md
~/.claude/valocom/skills/skill-name.md

# ✅ Right - user-level
~/.claude/skills/skill-name/
```

If a skill truly is project-specific (uses project-specific file paths, configs, etc.), then it belongs in the project directory. But most skills should be generalizable and user-level.

### Why This Works

User-level skills in `~/.claude/skills/` are:
- Available to all Claude instances
- Easier to manage (one location)
- More reusable across projects
- Properly organized and discoverable

---
