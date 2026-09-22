"""Local Next-Air-Assistant chat. chainlit run app.py -h"""
from __future__ import annotations

import os
from pathlib import Path

import chainlit as cl
from chainlit.input_widget import Select, Slider
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from brain import load_brain, skill_names
from llm import run_turn
from models import DEFAULT_MODEL, SIDEBAR_MODELS
from plugin_paths import require_plugin

DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 4096

STARTERS = [
    (
        "I teach twenty-five children in a primary classroom in Seville, Spain.",
        "I teach about twenty-five children in a primary classroom in Seville, Spain. "
        "We have no indoor air sensor and no mechanical cooling, but we can open the windows. "
        "One child is sensitive to heat. I need to plan next week’s afternoons: please look up "
        "outdoor air and heat, then pause before you tell me whether to open, close, filter, or stay indoors.",
    ),
    (
        "There is wildfire smoke outside my flat in Porto, Portugal.",
        "I am at home in a flat in Porto, Portugal. There is wildfire smoke outside. "
        "I can close the windows and I have a portable particle filter in the living room. "
        "I have asthma, which I have not copied into the Active table of this plugin. "
        "Should I close the windows and run the filter, or do you still need outdoor CAMS before you recommend?",
    ),
    (
        "Someone just read 1400 ppm of CO2 in our office in Lyon, France.",
        "This is a small open-plan office in Lyon, France. At about 11:00 local time someone read "
        "1400 ppm of CO2 on a handheld meter. About twelve people are in the room, the windows can open, "
        "and nobody is listed in the Active table. We do not have an outdoor sensor. "
        "After you look at outdoor air, what should we do with the windows?",
    ),
    (
        "Forecast indoor CO2 from the labelled 24-hour classroom series in Valencia.",
        "Please forecast indoor CO2 using the labelled classroom example series that ships with this plugin "
        "(synthetic, not a real sensor). The room is in Valencia, Spain. We can open the windows. "
        "The file is a 24-hour school day. Forecast the next two hours from the last point, name that clock, "
        "and say whether those two hours are a lesson. If they are not, still tell me what the same series "
        "did during class hours.",
    ),
]

COMMAND_HINTS = {
    "help": "What this helper can do, and how to give it context",
    "assess": "Outdoor snapshot for a named place",
    "open-close-filter-stay": "One room decision after a pause",
    "forecast-co2": "Indoor CO2 horizon from a 10-minute series",
}


@cl.set_starters
async def set_starters():
    return [cl.Starter(label=label, message=msg) for label, msg in STARTERS]


@cl.on_chat_start
async def on_chat_start():
    try:
        require_plugin()
        system = load_brain()
    except FileNotFoundError as exc:
        await cl.Message(content=str(exc)).send()
        return
    cl.user_session.set("system", system)
    cl.user_session.set("history", [])
    chosen = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    cl.user_session.set("model", chosen)
    cl.user_session.set("temperature", DEFAULT_TEMPERATURE)
    cl.user_session.set("max_tokens", DEFAULT_MAX_TOKENS)
    try:
        initial_index = SIDEBAR_MODELS.index(chosen)
    except ValueError:
        initial_index = 0

    await cl.ChatSettings(
        [
            Select(
                id="model",
                label="OpenRouter model",
                values=SIDEBAR_MODELS,
                initial_index=initial_index,
            ),
            Slider(
                id="temperature",
                label="Temperature (0 = steadier, 1 = more varied)",
                initial=DEFAULT_TEMPERATURE,
                min=0.0,
                max=1.0,
                step=0.05,
            ),
            Slider(
                id="max_tokens",
                label="Max output tokens (cuts the reply if the model runs long)",
                initial=DEFAULT_MAX_TOKENS,
                min=256,
                max=8192,
                step=256,
            ),
        ]
    ).send()

    commands = [
        {
            "id": name,
            "icon": "leaf",
            "description": COMMAND_HINTS.get(name, name),
            "button": True,
        }
        for name in skill_names()
    ]
    await cl.context.emitter.set_commands(commands)

    if not os.getenv("OPENROUTER_API_KEY", "").strip():
        await cl.Message(
            content="OPENROUTER_API_KEY is missing. Copy `.env.example` to `.env` and paste the key from exercise 2."
        ).send()


@cl.on_settings_update
async def on_settings_update(settings: dict):
    if settings.get("model"):
        cl.user_session.set("model", settings["model"])
    if settings.get("temperature") is not None:
        try:
            cl.user_session.set("temperature", float(settings["temperature"]))
        except (TypeError, ValueError):
            cl.user_session.set("temperature", DEFAULT_TEMPERATURE)
    if settings.get("max_tokens") is not None:
        try:
            cl.user_session.set("max_tokens", int(float(settings["max_tokens"])))
        except (TypeError, ValueError):
            cl.user_session.set("max_tokens", DEFAULT_MAX_TOKENS)


@cl.on_message
async def on_message(message: cl.Message):
    system = cl.user_session.get("system")
    if not system:
        await cl.Message(content="Plugin did not load. Check the folder layout and restart.").send()
        return
    prefix = ""
    if getattr(message, "command", None):
        prefix = (
            f"The user invoked the `{message.command}` skill. "
            f"Follow skills/{message.command}/SKILL.md.\n\n"
        )
    history = cl.user_session.get("history") or []
    model = cl.user_session.get("model")
    temperature = cl.user_session.get("temperature")
    max_tokens = cl.user_session.get("max_tokens")
    reply = cl.Message(content="")
    await reply.send()
    steps: dict[str, cl.Step] = {}

    async def on_tool_start(call_id: str, name: str, args: dict) -> None:
        step = cl.Step(name=name, type="tool")
        step.input = args
        await step.send()
        steps[call_id] = step

    async def on_tool_end(call_id: str, name: str, output: str, ok: bool, dur_ms: float) -> None:
        step = steps.pop(call_id, None)
        if step is None:
            return
        step.output = (output or "")[:2000]
        await step.update()

    async def on_token(piece: str) -> None:
        await reply.stream_token(piece)

    try:
        text = await run_turn(
            system=system,
            history=history,
            user_text=prefix + message.content,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            on_token=on_token,
            on_tool_start=on_tool_start,
            on_tool_end=on_tool_end,
        )
    except Exception as exc:
        text = f"This turn failed: {exc}"
        await reply.stream_token(("\n\n" if reply.content else "") + text)
    if not (reply.content or "").strip():
        text = text or "(empty reply)"
        await reply.stream_token(text)
    await reply.update()
    history.append({"role": "user", "content": prefix + message.content})
    history.append({"role": "assistant", "content": text})
    cl.user_session.set("history", history[-24:])
