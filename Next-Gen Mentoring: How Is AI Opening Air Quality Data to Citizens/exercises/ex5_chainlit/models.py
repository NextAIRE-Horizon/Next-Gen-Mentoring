"""Short OpenRouter list. Free slugs rotate; edit this file if one dies."""

DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning:free"

# Free first so a zip with no credit still runs. Paid needs OpenRouter credit.
SIDEBAR_MODELS = [
    DEFAULT_MODEL,
    "qwen/qwen3.8-27b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3.5-lightning",
    "openai/gpt-4o-mini",
    "google/gemini-2.5-flash",
    "anthropic/claude-sonnet-5",
]
