"""Validate every skills/*/SKILL.md and the plugin manifests."""

import json
import re
import sys
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent
FRONTMATTER: re.Pattern[str] = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def validate_skills() -> list[str]:
    errors: list[str] = []
    skill_files: list[Path] = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found under skills/*/SKILL.md")
    for path in skill_files:
        folder: str = path.parent.name
        fields: dict[str, str] = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fields:
            errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
            continue
        if fields.get("name") != folder:
            errors.append(f"{path.relative_to(ROOT)}: name '{fields.get('name')}' != folder '{folder}'")
        if not fields.get("description"):
            errors.append(f"{path.relative_to(ROOT)}: missing description")
    return errors


def validate_manifests() -> list[str]:
    errors: list[str] = []
    for name in ("plugin.json", "marketplace.json"):
        path: Path = ROOT / ".claude-plugin" / name
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f".claude-plugin/{name}: {exc}")
    return errors


def main() -> int:
    errors: list[str] = validate_skills() + validate_manifests()
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("All skills and manifests are valid.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
