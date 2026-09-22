# Thresholds (orientation, not a certificate)

Numbers for this plugin live here. Do not copy them into skills or adapters. Personal health notes belong in `preconditions.md`, not here.

Outdoor air from this plugin is **CAMS via Open-Meteo**: a model grid, not a monitor in the street.

## European AQI (CAMS `european_aqi`)

Bands as commonly used with the European index on this feed. Treat as orientation.

| Index | Band |
|------:|------|
| 0–20 | Good |
| 21–40 | Fair |
| 41–60 | Moderate |
| 61–80 | Poor |
| 81–100 | Very poor |
| >100 | Extremely poor |

## WHO global air quality guidelines (2021) - 24-hour, µg/m³

Use when the user pastes a concentration or when CAMS returns µg/m³. These are health guidelines, not EU law.

| Pollutant | 24-hour guideline |
|-----------|-------------------|
| PM2.5 | 15 µg/m³ |
| PM10 | 45 µg/m³ |
| NO2 | 25 µg/m³ |
| O3 (8-hour) | 100 µg/m³ |

Source: WHO global air quality guidelines, 2021.

## Heat (outdoor forecast)

Not a legal limit. Orientation for a school or office without claiming EPBD compliance.

| Daily max (outdoor) | Note |
|---------------------|------|
| ≥ 32 °C | Heat is already a classroom problem in much of southern Europe; ask about cooling and afternoon use. |
| ≥ 35 °C | Strong caution: shorten outdoor time, shade, water; do not pretend indoor air is known unless they paste a reading. |

## Indoor paste (optional)

If they paste a room reading, this is enough for v0. Skip missing parameters. Keep the time they stated next to the value. Do not line it up with current outdoor CAMS as if both were taken together.

| Parameter | Orientation |
|-----------|-------------|
| CO2 | Around 1000 ppm: air is stale; ventilate if outdoor air is cleaner and cooler. Not a WELL audit. |
| PM2.5 | Compare to the WHO 24-hour line above. If outdoor CAMS is worse than indoor, closing windows may help. |

## Provenance one-liners

- CAMS / Open-Meteo: modeled outdoor, snapped to a grid cell (coordinates in the response may not match the address). Timestamps belong to the `timezone` field on that same payload (IANA name, with `utc_offset_seconds`). Without `timezone=auto`, air quality is GMT and the weather forecast is already local; do not mix those two clocks.
- Tavily: headlines, if the user is signed in. Not a concentration. Cite URLs. If unauthorized, say news unavailable.
- A pasted indoor number: their sensor or their word; you did not read a building API. It is valid at the time they gave, not automatically at the CAMS `current.time`.
- WAQI / OpenAQ: not configured in v0. Do not fetch them unless the user added that MCP.
- Preconditions: optional; only filled Active rows in `preconditions.md`. Extra caution, not a diagnosis.
