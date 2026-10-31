# agent-skills

Personal Claude Code skills, distributed as a plugin marketplace.

## Skills

Everything under [skills/](skills/) is shipped as the `toolkit` plugin:

- `engineering-standards`
- `university-calendar`

## Setup (once per device)

In Claude Code:

```
/plugin marketplace add Joniba1/agent-skills
/plugin install toolkit@joniba-skills-toolkit
```

Then open `/plugin` > Marketplaces > `joniba-skills-toolkit` and enable auto-update.

## Getting updates

Pushing to `main` does not touch your machines; Claude Code fetches the repo itself.
With auto-update on, it picks up changes at startup. To pull immediately:

```
/plugin marketplace update joniba-skills-toolkit
/reload-plugins
```

## Adding a skill

Create `skills/<name>/SKILL.md` with `name` (matching the folder) and `description` frontmatter.
The `Validate skills` workflow checks this on every push to `main` that touches `skills/`.
Run it locally with `python scripts/validate_skills.py`.
