"""HTTP tools wrapped for LangChain. No MCP, no vendor sensor API."""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx
from langchain_core.tools import tool

from plugin_paths import require_plugin

OPEN_METEO_GEO = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_AQ = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPEN_METEO_WX = "https://api.open-meteo.com/v1/forecast"
TAVILY_SEARCH = "https://api.tavily.com/search"
CHRONOS = "https://miguel-escribano-chronos-co2-forecast.hf.space/gradio_api/call/predict"

AQ_CURRENT = "european_aqi,pm2_5,pm10,nitrogen_dioxide,ozone"


async def _get(url: str, params: dict) -> Any:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()


def _stamp_clock(data: dict, *, kind: str) -> dict:
    """Open-Meteo already converted times; we only label the clock it used."""
    tz = data.get("timezone") or "GMT"
    offset = data.get("utc_offset_seconds")
    if isinstance(offset, (int, float)):
        hours = offset / 3600
        utc_label = f"UTC{hours:+g}"
    else:
        utc_label = "UTC offset unknown"
    when = (data.get("current") or {}).get("time")
    data["_clock"] = {
        "iana": tz,
        "abbreviation": data.get("timezone_abbreviation"),
        "utc_offset_seconds": offset,
        "as_utc": utc_label,
        "current_time": when,
        "note": (
            f"{kind} timestamps are already in {tz} ({utc_label}). "
            "Quote this clock. Do not convert them again, and do not mix them with another payload."
        ),
    }
    return data


def _active_table_text() -> str:
    """Filled rows of knowledge/preconditions.md ## Active. Empty table means unused."""
    path = require_plugin() / "knowledge" / "preconditions.md"
    try:
        markdown = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    start = markdown.find("## Active")
    if start == -1:
        return ""
    rest = markdown[start + len("## Active") :]
    nxt = rest.find("\n## ")
    section = rest if nxt == -1 else rest[:nxt]
    lines: list[str] = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        joined = " ".join(cells).strip()
        if not joined or set(joined.replace(" ", "")) <= set("-:"):
            continue
        header = joined.lower()
        if header.startswith("who ") or "what it changes" in header:
            continue
        if not any(cells):
            continue
        lines.append(joined)
    return " ".join(lines)


def pollen_fields_from_active() -> list[str]:
    """G3: only pollen names that appear in filled Active rows, never from chat."""
    blob = _active_table_text().lower()
    if not blob.strip():
        return []
    mapping = (
        ("alder_pollen", ("alder",)),
        ("birch_pollen", ("birch",)),
        ("grass_pollen", ("grass",)),
        ("mugwort_pollen", ("mugwort",)),
        ("olive_pollen", ("olive",)),
        ("ragweed_pollen", ("ragweed",)),
    )
    return [field for field, keys in mapping if any(key in blob for key in keys)]


@tool
async def geocode_place(name: str, country: str | None = None) -> str:
    """Look up a place name. Pick the high-population city, not a lookalike.

    Args:
        name: Place name to look up.
        country: Optional ISO-2 or country name to disambiguate.
    """
    params: dict[str, Any] = {"name": name, "count": 3, "language": "en"}
    if country:
        params["country"] = country
    data = await _get(OPEN_METEO_GEO, params)
    return json.dumps(data, ensure_ascii=False)


@tool
async def get_cams_air(latitude: float, longitude: float) -> str:
    """Open-Meteo air quality (modelled CAMS). Not a street station.

    Pollen fields are added only when the plugin Active table names them.
    Do not pass a pollen flag.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
    """
    pollen = pollen_fields_from_active()
    current = AQ_CURRENT + (("," + ",".join(pollen)) if pollen else "")
    data = await _get(
        OPEN_METEO_AQ,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": current,
            "domains": "auto",
            "timezone": "auto",
        },
    )
    _stamp_clock(data, kind="CAMS air")
    extra = (
        f" Active pollen fields: {', '.join(pollen)}."
        if pollen
        else " Active table named no pollen; none requested."
    )
    data["_note"] = (
        "CAMS via Open-Meteo, modelled outdoor air, not a station. "
        + data["_clock"]["note"]
        + extra
    )
    data["_pollen_fields"] = pollen
    return json.dumps(data, ensure_ascii=False)


@tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """Open-Meteo weather now plus 7 daily max/min and rain.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
    """
    data = await _get(
        OPEN_METEO_WX,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 7,
            "timezone": "auto",
        },
    )
    _stamp_clock(data, kind="Weather")
    data["_note"] = (
        "Weather data by Open-Meteo.com (CC BY 4.0). " + data["_clock"]["note"]
    )
    return json.dumps(data, ensure_ascii=False)


@tool
async def search_news(query: str) -> str:
    """Tavily web search for headlines. At most two calls per turn. Cite URLs.

    Args:
        query: Search query.
    """
    key = os.getenv("TAVILY_API_KEY", "").strip()
    if not key:
        return json.dumps({"unavailable": True, "reason": "TAVILY_API_KEY not set"})
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            TAVILY_SEARCH,
            json={
                "api_key": key,
                "query": query,
                "search_depth": "basic",
                "max_results": 5,
            },
        )
        if r.status_code >= 400:
            return json.dumps({"unavailable": True, "status": r.status_code, "body": r.text[:500]})
        return json.dumps(r.json(), ensure_ascii=False)


def _classroom_example_path():
    return (
        require_plugin()
        / "skills"
        / "forecast-co2"
        / "examples"
        / "classroom_co2_24h.csv"
    )


def _parse_classroom_csv(text: str) -> dict[str, Any]:
    stamps: list[str] = []
    ppm: list[float] = []
    for raw in text.splitlines()[1:]:
        line = raw.strip()
        if not line or line.startswith("timestamp"):
            continue
        ts, val = line.split(",", 1)
        stamps.append(ts.strip())
        ppm.append(float(val.strip()))
    return {
        "path": "classroom_co2_24h.csv",
        "synthetic": True,
        "n_points": len(ppm),
        "first_timestamp": stamps[0] if stamps else None,
        "last_timestamp": stamps[-1] if stamps else None,
        "last_co2_ppm": ppm[-1] if ppm else None,
        "occupied_peak_ppm": max(ppm) if ppm else None,
        "co2_ppm": ppm,
        "csv": text,
        "note": (
            "Synthetic 10-minute classroom series. Chronos continues from last_timestamp. "
            "If that clock is after class, the next two hours are not a lesson. "
            "occupied_peak_ppm is a different interval in the same file."
        ),
    }


@tool
def read_classroom_co2_example() -> str:
    """Read the labelled synthetic 24-hour classroom CO2 CSV.

    Returns every ppm plus last_timestamp. To forecast that file, call
    forecast_co2_chronos with use_labelled_example true. Do not copy only
    the last hour of numbers.
    """
    parsed = _parse_classroom_csv(_classroom_example_path().read_text(encoding="utf-8"))
    return json.dumps(parsed)


@tool
async def forecast_co2_chronos(
    co2_ppm: list[float] | None = None,
    prediction_length: int = 12,
    use_labelled_example: bool = False,
) -> str:
    """Chronos-2 CO2 forecast. Chronos continues from the last point.

    For the bundled classroom example set use_labelled_example true so this host
    sends the full file. Otherwise pass an oldest-first ppm list of at least 6
    points. Space may sleep; this tool retries.

    Args:
        co2_ppm: Oldest-first ppm list. Ignored when use_labelled_example is true.
        prediction_length: 1=10min, 6=1h, 12=2h default, 24=4h.
        use_labelled_example: If true, read the bundled classroom CSV in full.
    """
    series_meta = None
    if use_labelled_example:
        series_meta = _parse_classroom_csv(
            _classroom_example_path().read_text(encoding="utf-8")
        )
        series = series_meta["co2_ppm"][-144:]
    else:
        series = list(co2_ppm or [])[-144:]
        if len(series) < 6:
            return json.dumps(
                {
                    "error": (
                        "Need at least 6 points at 10-minute spacing, or set "
                        "use_labelled_example true for the bundled file. Do not invent."
                    )
                }
            )
    inner = json.dumps(
        {
            "inputs": series,
            "parameters": {
                "prediction_length": int(prediction_length or 12),
                "quantile_levels": [0.1, 0.5, 0.9],
            },
        }
    )
    extra = {
        "context_points": len(series),
        "note": "Chronos-2-small Hugging Face Space. First call may wake a cold Space.",
    }
    if series_meta:
        extra.update(
            {
                "synthetic": True,
                "last_timestamp": series_meta["last_timestamp"],
                "last_co2_ppm": series_meta["last_co2_ppm"],
                "occupied_peak_ppm": series_meta["occupied_peak_ppm"],
                "clock_note": series_meta["note"],
            }
        )
    async with httpx.AsyncClient(timeout=45.0) as client:
        last_err = "unknown"
        for attempt in range(8):
            try:
                r = await client.post(CHRONOS, json={"data": [inner]})
                r.raise_for_status()
                event_id = r.json().get("event_id")
                if not event_id:
                    last_err = r.text[:400]
                    await asyncio.sleep(20)
                    continue
                r2 = await client.get(f"{CHRONOS}/{event_id}")
                r2.raise_for_status()
                return json.dumps(
                    {
                        "attempt": attempt + 1,
                        "raw": r2.text[:8000],
                        **extra,
                    }
                )
            except Exception as exc:
                last_err = str(exc)
                await asyncio.sleep(20)
        return json.dumps(
            {
                "unavailable": True,
                "reason": "Chronos Space did not wake",
                "last_error": last_err,
            }
        )


TOOLS = [
    geocode_place,
    get_cams_air,
    get_forecast,
    search_news,
    read_classroom_co2_example,
    forecast_co2_chronos,
]
