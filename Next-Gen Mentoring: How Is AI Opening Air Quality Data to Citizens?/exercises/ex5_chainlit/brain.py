"""Concatenate the exercise 3 plugin into one system prompt."""
import glob
from datetime import datetime, timezone
from pathlib import Path

from plugin_paths import require_plugin

RUNTIME = """
## This chat (this host only)

You are running in a local web chat the user started, not in Cursor or n8n.
Follow agents/next-air-assistant.md: OODA with the human pause in Decide.
Tools here are HTTP functions (Open-Meteo, optional Tavily, Chronos), exposed
through LangChain. They are not MCP. If a tool fails, say so. Do not invent
Open-Meteo, CAMS, news, or indoor values.
Do not name commercial indoor monitors or a private consultant.
"""


def load_brain() -> str:
    root = require_plugin()
    parts: list[str] = [
        f"# CURRENT DATE AND TIME\n\n{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC"
    ]
    persona = root / "agents" / "next-air-assistant.md"
    parts.append(f"# Persona (agents/next-air-assistant.md)\n\n{persona.read_text(encoding='utf-8')}")
    for skill_path in sorted(glob.glob(str(root / "skills" / "*" / "SKILL.md"))):
        name = Path(skill_path).parent.name
        parts.append(f"# Skill: {name}\n\n{Path(skill_path).read_text(encoding='utf-8')}")
    for kf in sorted(glob.glob(str(root / "knowledge" / "**" / "*.md"), recursive=True)):
        rel = Path(kf).relative_to(root)
        parts.append(f"# Knowledge: {rel}\n\n{Path(kf).read_text(encoding='utf-8')}")
    parts.append(RUNTIME)
    return "\n\n---\n\n".join(parts)


def skill_names() -> list[str]:
    root = require_plugin()
    return sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
