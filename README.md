# agent-skills

Personal Claude skills. Each folder under [skills/](skills/) is one skill.

## Skills

- `engineering-standards`
- `university-calendar`

## Adding a skill

Create `skills/<name>/SKILL.md` with `name` (matching the folder) and `description` frontmatter.
The `Validate skills` workflow checks this on every push to `main` that touches `skills/`.
Run it locally with `python scripts/validate_skills.py`.

## Using a skill

Zip the skill folder so `SKILL.md` sits inside a folder named after the skill
(`<name>.zip` containing `<name>/SKILL.md`), then upload it in Claude under
Settings > Capabilities > Skills.
