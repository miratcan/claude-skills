# Troubleshooting

Error → solution mappings for quick reference when creating skills.

---

## Error: Skill not being discovered/loaded

**Symptom**: Created a skill file but Claude doesn't recognize or use it in future sessions.

**Cause**: Missing or malformed frontmatter. The `name` and `description` fields are required for skill indexing and discovery.

**Solution**:
1. Check that SKILL.md has YAML frontmatter at the very top:
```markdown
---
name: skill-name
description: |
  Clear description with specific triggers.
---
```

2. Verify the description is specific enough with:
   - What the skill does (first sentence)
   - "Use when:" scenarios
   - Example trigger phrases users might say
   - Exact error messages if applicable

3. Restart Claude Code or reload skills if necessary


---

## Error: Skill is a file, not a directory

**Symptom**: Created `skill-name.md` instead of `skill-name/` directory structure.

**Cause**: Misunderstanding of skill structure - skills must be directories with multiple files.

**Solution**:
1. Delete the single file:
```bash
rm ~/.claude/skills/skill-name.md
```

2. Create proper directory structure:
```bash
mkdir -p ~/.claude/skills/skill-name/
touch ~/.claude/skills/skill-name/SKILL.md
touch ~/.claude/skills/skill-name/examples.md
# Only if errors were encountered:
touch ~/.claude/skills/skill-name/troubleshooting.md
```

3. Move content from the single file into SKILL.md with proper frontmatter


---

## Error: No Failed Attempts section

**Symptom**: Skill SKILL.md is created but lacks the "Failed Attempts" table.

**Cause**: Forgetting to document what didn't work during the session.

**Solution**:
1. Review the session transcript for:
   - Approaches that were tried and failed
   - Errors encountered
   - User corrections ("no, don't do X, do Y instead")
   - Wrong assumptions that were corrected

2. Add Failed Attempts table:
```markdown
## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| [First wrong approach] | [Exact error or reason] | [What to do instead] |
| [Second wrong approach] | [Why it didn't work] | [Correct approach] |
```

3. Document even "obvious" failures - they prevent wasted time in future sessions

**Why this matters**: Failed attempts are often more valuable than success stories because they document anti-patterns and dead ends.


---

## Error: Vague or generic descriptions

**Symptom**: Skill description is too generic like "Helps with API errors" or "Solves database issues".

**Cause**: Not being specific enough about what the skill actually handles.

**Solution**:
Rewrite description to be highly specific:

❌ **Bad**:
```yaml
description: Helps with API errors
```

✅ **Good**:
```yaml
description: |
  Resolve OpenAI API rate limit and timeout errors in Python applications.
  Use when: encountering 429 rate limit errors, API timeout exceptions,
  or "RateLimitError" in error logs.
  Example triggers: "getting rate limited", "API keeps timing out",
  "RateLimitError: You exceeded your current quota".
```

Include:
- Specific technologies/tools (OpenAI API, Python, etc.)
- Exact error messages users will see
- Phrases users actually say when encountering the problem
- Clear "Use when:" scenarios


---
