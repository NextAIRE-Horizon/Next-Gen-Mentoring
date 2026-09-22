"""Plugin root: the exercise 3 folder next to this one."""
from pathlib import Path

_EX5 = Path(__file__).resolve().parent
PLUGIN_ROOT = (_EX5.parent / "ex3_next_air_assistant" / "next-air-assistant").resolve()


def require_plugin() -> Path:
    persona = PLUGIN_ROOT / "agents" / "next-air-assistant.md"
    if not persona.is_file():
        raise FileNotFoundError(
            f"Next-Air-Assistant plugin not found at {PLUGIN_ROOT}. "
            "Keep the zip folder layout. Exercise 3 must sit next to this one."
        )
    return PLUGIN_ROOT
