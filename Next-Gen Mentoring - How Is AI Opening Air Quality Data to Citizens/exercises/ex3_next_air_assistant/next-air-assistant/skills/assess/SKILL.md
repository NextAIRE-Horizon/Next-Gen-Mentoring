---
name: assess
description: "Snapshot of outdoor air quality and heat for a place (European AQI, PM2.5, PM10, NO2, O3, 7-day temperature). Use when the user asks how the air is, AQI now, forecast this week, or wants numbers without a full stay-or-go decision."
---

# Assess

This skill is a snapshot, not a stay-or-go campaign. Follow guardrails G1–G5 in `../../agents/next-air-assistant.md`. Read `../../knowledge/thresholds.md` and `../../knowledge/preconditions.md` before you classify anything.

If the person has not given a city or a lat/lon, ask once and stop.

## Phase 1. Observe and orient (findings, then pause)

Prefer the Open-Meteo MCP. If MCP is down, use the HTTP fallback listed in the agent file.

1. Call `openmeteo_search_locations` when you have a name. Pick the high-population city, not a lookalike village or airport.
2. Call `openmeteo_get_air_quality` with current `european_aqi`, `pm2_5`, `pm10`, `nitrogen_dioxide`, and `ozone`.
3. Call `openmeteo_get_forecast` for now plus seven daily maximums, minimums, and rain.
4. If they pasted indoor numbers, put those rows in the table, including the time they stated. Do not invent any (G1). Do not present a morning paste as the indoor air at the outdoor `current.time` (G2).
5. Read filled Active rows in `preconditions.md`. Add a pollen field to the air-quality call only when that table names that pollen (G3). Chat is not a substitute for a filled row.

Classify outdoor AQI and heat using `thresholds.md` only. Label CAMS as modeled (G2). When you quote a value, name the tool, the place, and the clock. If Active preconditions exist, mention them as extra caution, not as a diagnosis (G5).

Present:

#### Outdoor snapshot: [place]

**Source:** Open-Meteo / CAMS (modeled, not a station) | **Time:** [current.time plus the IANA timezone from that payload]

| What | Value | Unit | Band / note |
|------|-------|------|-------------|
| European AQI | | | |
| PM2.5 | | µg/m³ | |
| PM10 | | µg/m³ | |
| NO2 | | µg/m³ | |
| O3 | | µg/m³ | |
| Now temperature | | °C | |
| Next days max | | °C | from the daily series |

Add indoor rows only when they were pasted.

Under **Gaps**, say whether pollen, stations, or news were not fetched.

Then stop (G4). Recap, in a full sentence, the room, occupancy, windows or filter, who is sensitive, and when they will use the space, including anything they only said in chat. Invite them to correct that recap. Ask for whatever a sensor cannot see that is still missing. If Active preconditions exist, name them. Do not tell them they may skip the pause. Wait for their next message before Phase 2.

## Phase 2. Decide and act

Wait until they answer. Keep this smaller than `open-close-filter-stay`: one or two sentences, not a campaign. If they actually asked whether to open the windows, or whether school should run tomorrow, switch to `../open-close-filter-stay/SKILL.md`.
