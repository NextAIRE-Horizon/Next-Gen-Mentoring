---
name: open-close-filter-stay
description: "Recommend open, close, filter, or stay for a room from outdoor CAMS, optional news, and an optional indoor paste. Use when the user asks about windows, school tomorrow, heatwave, wildfire smoke, or whether to stay indoors."
---

# Open, close, filter, or stay

This skill turns a number, an outdoor envelope, and an optional news event into one room decision. It is not fire science. Follow guardrails G1–G5 in `../../agents/next-air-assistant.md`. Read `../../knowledge/thresholds.md` and `../../knowledge/preconditions.md` before you classify anything.

If the person has not given a city or a lat/lon, ask once and stop.

## Phase 1. Observe and orient (findings, then pause)

1. Geocode, and pick the real high-population city, not a namesake.
2. Fetch current CAMS air quality and the seven-day heat, wind, and rain forecast (the same tools as assess).
3. Include an indoor paste or CSV only if they offered it. Do not invent indoor values (G1).
4. Search news with Tavily (`tavily_search`): at most two queries, and cite URLs. If Tavily is missing or unauthorized, write that news is unavailable and continue. Do not invent headlines (G1, G2).
5. Read filled Active rows in `preconditions.md`. Add a pollen field only when that table names that pollen (G3).

Attribute CAMS and Open-Meteo (G2). If a headline and the model disagree, show both; do not draw a smoke plume (G5). Map values to bands in `thresholds.md` only. Do not claim EPBD or WELL. If Active preconditions exist, fold them in as extra caution, not as a diagnosis (G5). Ignore empty rows and the Examples table.

Present findings as a table plus two sentences. Then stop (G4).

Ask, in a full sentence, what a sensor cannot see that is still open, after you have recapped occupancy, windows, filter, who is sensitive (chat or Active), and when they will use the space. Invite them to correct the recap. Do not tell them they may skip the pause. Wait for their next message before Phase 2.

## Phase 2. Decide and act

After they answer, give one screen:

| Option | Meaning |
|--------|---------|
| **Open** | Outdoor looks cleaner or cooler than staying shut; ventilate. |
| **Close** | Outdoor heat or pollution is the problem; keep windows shut if they can. |
| **Filter** | Only if they have a portable filter or HVAC recirculation; do not invent hardware they did not mention. |
| **Stay** | Limit outdoor time. Indoor air is still unknown unless they pasted a reading. |

Recommend one option, say how confident you are, and say what would change the call. Suggest a re-check window (this evening, or tomorrow morning).
