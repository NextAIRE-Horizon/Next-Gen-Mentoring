"""LangChain create_agent over OpenRouter. Stream visible tokens; hide think tags."""
from __future__ import annotations

import os
import time
import uuid
from typing import Any, Awaitable, Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

from models import DEFAULT_MODEL
from tools import TOOLS

MAX_ITERATIONS = 8
_OPEN_TAGS = ("<think>", "<thinking>", "<reasoning>")
_CLOSE_TAGS = ("</think>", "</thinking>", "</reasoning>")
_HOLD = 12  # longest open tag, so a split "<reason" cannot leak
TOOL_STEP_LIMIT = (
    "I hit the tool-call limit for this turn. Ask me to continue from the findings I already have."
)


def _openrouter_model(model_id: str, temperature: float, max_tokens: int) -> ChatOpenRouter:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Copy .env.example to .env and paste the key from exercise 2."
        )
    return ChatOpenRouter(
        model=model_id,
        api_key=api_key,
        temperature=min(1.0, max(0.0, float(temperature))),
        max_tokens=max(256, int(max_tokens)),
        timeout=180_000,
        streaming=True,
        app_url="http://localhost:8000",
        app_title="Next-Air-Assistant",
    )


def _find_ci(hay: str, needles: tuple[str, ...]) -> tuple[int | None, int]:
    low = hay.lower()
    best: int | None = None
    length = 0
    for needle in needles:
        idx = low.find(needle)
        if idx != -1 and (best is None or idx < best):
            best = idx
            length = len(needle)
    return best, length


class ThinkFilter:
    """Hold back incomplete tags; drop think/reasoning blocks."""

    def __init__(self) -> None:
        self.buf = ""
        self.inside = False
        self.visible: list[str] = []

    def feed(self, chunk: str) -> str:
        if not chunk:
            return ""
        self.buf += chunk
        out: list[str] = []
        while True:
            if self.inside:
                idx, nlen = _find_ci(self.buf, _CLOSE_TAGS)
                if idx is None:
                    if len(self.buf) > _HOLD:
                        self.buf = self.buf[-_HOLD:]
                    break
                self.buf = self.buf[idx + nlen :]
                self.inside = False
                continue
            idx, nlen = _find_ci(self.buf, _OPEN_TAGS)
            if idx is None:
                if len(self.buf) > _HOLD:
                    out.append(self.buf[:-_HOLD])
                    self.buf = self.buf[-_HOLD:]
                break
            out.append(self.buf[:idx])
            self.buf = self.buf[idx + nlen :]
            self.inside = True
        piece = "".join(out)
        if piece:
            self.visible.append(piece)
        return piece

    def flush(self) -> str:
        if self.inside:
            self.buf = ""
            return ""
        piece = self.buf
        self.buf = ""
        if piece:
            self.visible.append(piece)
        return piece

    def text(self) -> str:
        return "".join(self.visible).strip()


def _tool_event_name(event: dict[str, Any]) -> str:
    name = event.get("name") or ""
    if name:
        return str(name)
    data = event.get("data") or {}
    inp = data.get("input")
    if isinstance(inp, dict):
        return str(inp.get("name") or inp.get("tool") or "tool")
    return "tool"


def _tool_event_args(event: dict[str, Any]) -> dict:
    data = event.get("data") or {}
    inp = data.get("input")
    if isinstance(inp, dict):
        if isinstance(inp.get("input"), dict):
            return dict(inp["input"])
        skip = {"name", "tool", "type", "id", "tool_call_id"}
        return {k: v for k, v in inp.items() if k not in skip}
    return {}


def _message_text(msg: Any) -> str:
    if msg is None:
        return ""
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text") or "")
        return "".join(parts)
    return ""


def _tool_event_output(event: dict[str, Any]) -> str:
    data = event.get("data") or {}
    out = data.get("output")
    if out is None:
        return ""
    if hasattr(out, "content"):
        out = out.content
    return str(out)


def _history_messages(history: list[dict[str, Any]], user_text: str) -> list:
    messages: list = []
    for m in history:
        role = m.get("role")
        content = m.get("content") or ""
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "system":
            messages.append(SystemMessage(content=content))
    messages.append(HumanMessage(content=user_text))
    return messages


async def _emit(on_token, piece: str) -> None:
    if piece and on_token:
        await on_token(piece)


async def run_turn(
    *,
    system: str,
    history: list[dict[str, Any]],
    user_text: str,
    model: str | None,
    on_token: Callable[[str], Awaitable[None]] | None = None,
    on_tool_start: Callable[[str, str, dict], Awaitable[None]] | None = None,
    on_tool_end: Callable[[str, str, str, bool, float], Awaitable[None]] | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> str:
    chosen = (model or os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()
    llm = _openrouter_model(chosen, temperature, max_tokens)
    run_limit = max(8, MAX_ITERATIONS * 2)
    agent = create_agent(
        model=llm,
        tools=list(TOOLS),
        system_prompt=system,
        middleware=[
            ToolCallLimitMiddleware(run_limit=run_limit, exit_behavior="continue"),
        ],
    )
    messages = _history_messages(history, user_text)
    config = {"recursion_limit": max(40, run_limit * 2 + 4)}
    filt = ThinkFilter()
    tool_started_at: dict[str, float] = {}
    run_to_call: dict[str, str] = {}
    hit_step_limit = False

    try:
        async for event in agent.astream_events(
            {"messages": messages},
            config=config,
            version="v2",
        ):
            kind = event.get("event")
            run_id = str(event.get("run_id") or "")

            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk is None:
                    continue
                content = getattr(chunk, "content", None)
                if isinstance(content, str) and content:
                    await _emit(on_token, filt.feed(content))
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text") or ""
                            if text:
                                await _emit(on_token, filt.feed(text))
                        elif isinstance(block, str) and block:
                            await _emit(on_token, filt.feed(block))

            elif kind == "on_chat_model_end" and not filt.text():
                output = (event.get("data") or {}).get("output")
                if output and not getattr(output, "tool_calls", None):
                    fallback = _message_text(output)
                    if fallback:
                        await _emit(on_token, filt.feed(fallback))

            elif kind == "on_tool_start" and on_tool_start:
                call_id = uuid.uuid4().hex
                if run_id:
                    run_to_call[run_id] = call_id
                tool_started_at[call_id] = time.perf_counter()
                await on_tool_start(call_id, _tool_event_name(event), _tool_event_args(event))

            elif kind == "on_tool_end" and on_tool_end:
                call_id = run_to_call.pop(run_id, None) or uuid.uuid4().hex
                started = tool_started_at.pop(call_id, time.perf_counter())
                dur_ms = (time.perf_counter() - started) * 1000.0
                await on_tool_end(
                    call_id,
                    _tool_event_name(event),
                    _tool_event_output(event),
                    True,
                    dur_ms,
                )

            elif kind == "on_tool_error" and on_tool_end:
                call_id = run_to_call.pop(run_id, None) or uuid.uuid4().hex
                started = tool_started_at.pop(call_id, time.perf_counter())
                dur_ms = (time.perf_counter() - started) * 1000.0
                err = (event.get("data") or {}).get("error")
                await on_tool_end(
                    call_id,
                    _tool_event_name(event),
                    str(err or "tool error"),
                    False,
                    dur_ms,
                )
    except Exception as stream_err:
        err_name = type(stream_err).__name__
        if "Recursion" in err_name or "recursion" in str(stream_err).lower():
            hit_step_limit = True
        else:
            try:
                result = await agent.ainvoke({"messages": messages}, config=config)
                final_msgs = result.get("messages") or []
                for msg in reversed(final_msgs):
                    if (
                        isinstance(msg, AIMessage)
                        and msg.content
                        and not getattr(msg, "tool_calls", None)
                    ):
                        text = _message_text(msg)
                        await _emit(on_token, filt.feed(text))
                        break
            except Exception as invoke_err:
                if "Recursion" in type(invoke_err).__name__:
                    hit_step_limit = True
                else:
                    raise

    await _emit(on_token, filt.flush())
    text = filt.text()
    if hit_step_limit:
        if not text:
            await _emit(on_token, TOOL_STEP_LIMIT)
            return TOOL_STEP_LIMIT
        suffix = "\n\n" + TOOL_STEP_LIMIT
        await _emit(on_token, suffix)
        return text + suffix
    return text or "(empty reply)"
