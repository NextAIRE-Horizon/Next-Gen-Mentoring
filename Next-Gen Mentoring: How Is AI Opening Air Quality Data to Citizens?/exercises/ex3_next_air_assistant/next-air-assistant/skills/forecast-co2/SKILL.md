---
name: forecast-co2
description: "Indoor CO2 forecast for the next 10 min to 4 h with Chronos-2. Use when the user asks where indoor CO2 is heading, whether the room will go stale, or to run Chronos on a 10-minute CO2 series or the labelled classroom example."
---

# Forecast indoor CO2

Follow guardrails G1–G5 in `../../agents/next-air-assistant.md`. Read `../../knowledge/thresholds.md`, and read filled Active rows in `../../knowledge/preconditions.md` before the pause in Phase 3. This skill does not use MCP. You call the public Chronos-2 Space yourself over HTTP. There is no API key.

`https://miguel-escribano-chronos-co2-forecast.hf.space`

Do not invent CO2 values (G1). Do not call a building API this plugin does not have (G5). Do not add a Python file; follow the snippets below.

## Phase 0 - Ask for a series (mandatory before any HTTP call)

Stop and show this. Then wait.

Indoor CO2 forecast needs a time series at **10-minute** intervals, oldest first.

| | Points | Window |
|--|--------:|--------|
| Ideal | 144 | 24 hours |
| Minimum | 6 | 1 hour |

Fewer than 24 hours is a toy run. A single pasted reading is not enough.

CSV header:

```text
timestamp,co2_ppm
```

Template (two rows only; the user adds the rest): `examples/TEMPLATE.csv`

Labelled classroom example (synthetic, not a sensor): `examples/classroom_co2_24h.csv`

Ask the user to pick one:

1. Use the bundled classroom example.
2. Attach or point to their own CSV with the same header.
3. Paste a column of ppm values if they already have at least six numbers (still 10-minute spacing).

If they already chose the bundled example in this message, do not wait. If they have fewer than six points, stop. Do not pad, interpolate, or invent.

## Phase 1 - Observe

Read the CSV (or the pasted column). Take every `co2_ppm` value, oldest first, up to 144 points (24 hours). Do not drop the daytime hours and keep only the evening tail. The bundled classroom file is a full school day that **ends at 23:50**, after the room emptied; Chronos still starts from that last clock.

On a host that offers `use_labelled_example` (the Chainlit exercise), set that flag so the host reads the file. Do not type twelve night-time ppm values by hand.

Horizons:

| Horizon | `prediction_length` |
|---------|--------------------:|
| 10min | 1 |
| 1h | 6 |
| 2h (default) | 12 |
| 4h | 24 |

POST the **same** body every time, including retries. Inner payload, then wrap it as a Gradio `data` string:

```json
{
  "inputs": [430, 431, 432],
  "parameters": {
    "prediction_length": 12,
    "quantile_levels": [0.1, 0.5, 0.9]
  }
}
```

```bash
curl -sS -X POST "https://miguel-escribano-chronos-co2-forecast.hf.space/gradio_api/call/predict" \
  -H "Content-Type: application/json" \
  -d '{"data":["<INNER_JSON_AS_STRING>"]}'
```

The response is `{"event_id":"..."}`. Then:

```bash
curl -sS "https://miguel-escribano-chronos-co2-forecast.hf.space/gradio_api/call/predict/<EVENT_ID>"
```

Parse the SSE `data:` line as JSON. You want `quantiles` `0.1`, `0.5`, `0.9`.

The Space is a free Hugging Face app: it sleeps, and the **first** call often fails while it boots. That is expected. Tell the user the Space is waking. Wait about 20 seconds. POST the **same** inner JSON again. Repeat until you get quantiles, for up to about three minutes. Do not treat the first HTTP error as a failed forecast. Do not change the series between retries. If it still fails after that wait, say the Space did not wake and offer one more identical call.

Attribute: Chronos-2-small on Hugging Face; method as in Garcia-Pinilla et al., 2026 (`https://doi.org/10.3390/forecasting8010026`). If they used the bundled CSV, say it is a synthetic classroom series.

## Phase 2 - Orient

Present the last ppm **and its timestamp** (G2). Then median / p10 / p90 for the horizon, in a small table. Compare the median to the CO2 line in `thresholds.md`. If they asked about a lesson (or another occupied use) and the last timestamp is not during that use, say so in a full sentence before you interpret stale or not. You may name the occupied-hour peak in the same file as a **different** interval. No open / close / filter / stay yet.

## Phase 3 - Decide + Act

Same pause as `open-close-filter-stay` (G4): recap occupancy, windows, who is sensitive, and when; invite a correction; wait for their next message. Then one line: open / close / filter / stay, with the forecast uncertainty you already showed.
