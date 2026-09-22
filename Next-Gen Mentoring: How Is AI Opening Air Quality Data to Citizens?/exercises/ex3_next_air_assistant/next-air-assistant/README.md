# Next-Air-Assistant

A public indoor-air assistant and consultant for a home, school, office, or clinic. Give it a place and a country, what the room is for, what you can actually do, and who is in the space. It looks up modeled outdoor air quality and heat, optional news headlines, and an indoor reading if you paste one. It then pauses, asks for context a sensor cannot see, and recommends whether to **open**, **close**, **filter**, or **stay**.

It is a citizen helper, not a certification audit, not a fire model, and not a doctor. Outdoor numbers come from CAMS (Copernicus / ECMWF) through Open-Meteo: a forecast grid, not a monitor on your street. Say that every time you quote them.

This folder is an **initiation**: enough architecture to see how an assistant is wired. It is not production. It does not include expert-reviewed guardrails, evals, or cost control. Those remain open problems.

Author: Miguel Escribano (`mescribano@inbiot.es`). License: MIT.

## Install this folder

This directory is the plugin. Install **this folder** in the host you already use. Skills and MCP load that way. Opening the parent project is not enough: the servers in `mcp.json` are picked up when the plugin is installed. You do not need Node on the default path.

| Host | What to do |
|------|------------|
| Claude Code | From this folder: `claude --plugin-dir .`. Then `/mcp` if you want news. |
| Cursor | Customize → plugins. Install from this folder. Enable MCP when asked. |
| Visual Studio Code | Enable MCP from `.vscode/mcp.json`. |
| Codex | Install this folder as a plugin (`plugin.json` and `mcp.json` are here). |
| Antigravity | Install this folder as a plugin. Enable MCP when asked. |
| Grok | Open this folder so it reads `AGENTS.md` and `agents/next-air-assistant.md`. |

Plugin id: `next-air-assistant`. Slash commands, if the host has them: `/next-air-assistant:help`, `/next-air-assistant:assess`, `/next-air-assistant:open-close-filter-stay`, `/next-air-assistant:forecast-co2`.

If you arrived through the NextAIRE exercise pack, customise first (`knowledge/thresholds.md`, optional `knowledge/preconditions.md`, and `agents/next-air-assistant.md`), then install. The workshop steps live in `../README.md`.

## Try this

Give a place, a country, the room, what you can change, and who is there.

> I teach about twenty-five children in a primary classroom in Seville, Spain. We have no indoor sensor and no mechanical cooling, but we can open the windows. One child is sensitive to heat. I need to plan next week’s afternoons.

> I am at home in a flat in Porto, Portugal. There is wildfire smoke outside. I can close the windows and I have a portable particle filter. I have asthma, which I have not copied into the Active table. Should I close and filter?

> This open-plan office in Lyon, France, just read 1400 ppm of CO2 at about 11:00 local time on a handheld meter. Twelve people are here. The windows can open. Nobody is listed in Active. What should we do with the windows?

> Please forecast indoor CO2 using the labelled classroom example series (synthetic, not a real sensor). The room is in Valencia, Spain. We can open the windows. The file is a 24-hour school day. Forecast the next two hours from the last point, name that clock, and say whether those two hours are a lesson. If they are not, still tell me what the same series did during class hours.

## What it uses

| Piece | Role |
|-------|------|
| `agents/next-air-assistant.md` | Persona, five guardrails (G1–G5), OODA with a human pause, MCP tools, skill routing |
| `knowledge/thresholds.md` | The only file that should hold numbers |
| `knowledge/preconditions.md` | Optional Active table: asthma, pollen allergy, heat or blood-pressure notes. Extra caution, not a diagnosis. Empty means unused |
| `help` | What this helper does |
| `assess` | Snapshot of outdoor air and heat |
| `open-close-filter-stay` | One room decision after the pause |
| `forecast-co2` | Indoor CO2 horizon from a 10-minute series (HTTP, not MCP) |

Open-Meteo MCP (no account): `https://open-meteo.caseyjhand.com/mcp`. If MCP is down, the agent may GET the same Open-Meteo HTTP APIs. Weather data by Open-Meteo.com (CC BY 4.0). Air quality: CAMS.

Tavily MCP (news, not concentrations): `https://mcp.tavily.com/mcp/`. No key in this repo. Approve OAuth in the host, or keep a Researcher key from `https://app.tavily.com` on your machine. If news is unavailable, the rest of the helper still runs.

Indoor CO2 forecast: Chronos-2-small on `https://miguel-escribano-chronos-co2-forecast.hf.space`. The Space sleeps; the first call often fails while it wakes. Retry the same payload. Method: Garcia-Pinilla et al., 2026 (`https://doi.org/10.3390/forecasting8010026`). The bundled classroom CSV is synthetic.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
