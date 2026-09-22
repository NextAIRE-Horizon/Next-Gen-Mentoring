# Exercise 3 - Load the plugin in that host

| Piece | In this exercise |
|-------|------------------|
| **Host** | Still the IDE from exercise 1. The plugin runs *inside* that runtime. |
| **Harness** | The host already has one: chat, tools, context, permissions, the loop. Next-Air-Assistant is a plugin. It joins that harness and augments it (agent, skills, knowledge, Open-Meteo and Tavily as MCP). The pause in Decide exists because this host is interactive. |
| **Model** | OpenRouter from exercise 2, or the host's own model if you skipped that wiring. |

You join that host's harness and augment it, inside someone else's runtime. Same outdoor numbers will feel different in n8n (exercise 4), where there is no pause.

This folder is the exercise. The plugin itself is the subfolder `next-air-assistant/` (its own README is there).

Next-Air-Assistant looks up outdoor air quality and heat, optional news, and an indoor reading if you paste one. It then recommends whether to open, close, filter, or stay.

Stay in the unzipped pack. Do not create another project. Edit the plugin first, then install **that subfolder** in the host you already have open. Do not install a second Next-Air-Assistant from a marketplace.

## Customise the knowledge base

Open `next-air-assistant/knowledge/thresholds.md`. That file is the only place numbers should live. Change a band, add a line that matters for your room (a school that will not open windows above a certain outdoor temperature, a pollen note, a CO2 value you actually use), and leave the rest. Skills should keep reading this file rather than duplicating figures.

Optional: open `next-air-assistant/knowledge/preconditions.md`. The Active table is empty on purpose. Copy an example row up if someone in the room has asthma, a named pollen allergy, or heat or blood-pressure sensitivity. Empty means unused. The assistant treats filled rows as extra caution, not a diagnosis.

## Edit the agent file

Open `next-air-assistant/agents/next-air-assistant.md`. That file is the control layer: who the assistant is, five guardrails written in full sentences (G1–G5), the OODA loop with the human pause, which MCP tools it may call, and how intents map to skills.

You can change the voice, rewrite a guardrail, tighten the gate question, or forbid a topic you do not want it to answer. Keep new rules in the same table, as complete sentences, so skills can still point here instead of inventing policy. An extra row might look like this:

```text
| G6 | Do not recommend opening windows in a nursery after 16:00. Ask the teacher to confirm occupancy first. |
```

Leave the plugin id as `next-air-assistant` (`name` in the YAML at the top of this file, and in `plugin.json`). Slash commands are `/next-air-assistant:help` and the same prefix for the others. Renaming the plugin means editing those files together, or the host will not find the commands. You may still change the display line (“You are **Next-Air-Assistant**…”) to another public name without touching the id.

## Add a skill (optional)

The plugin ships `help`, `assess`, `open-close-filter-stay`, and `forecast-co2`. `forecast-co2` asks for a CO2 series (or the labelled classroom CSV) and calls Chronos-2 over HTTP, not MCP. If you want another behaviour, add a folder and tell the agent when to use it.

1. Create `next-air-assistant/skills/<name>/SKILL.md` with YAML frontmatter (`name` and `description`). The description is how the host decides to call it.
2. Add a row to the routing table in `next-air-assistant/agents/next-air-assistant.md`.
3. Optional, only if you want a Claude Code slash command: add `next-air-assistant/commands/<name>.md` so you get `/next-air-assistant:<name>`.
4. If the skill needs Open-Meteo fields that the agent file does not already list, add those variable names to the tool list in `agents/next-air-assistant.md`. Guardrail G3 treats that list as the allowlist. The pollen example below needs that step.

A minimal skill looks like this:

```markdown
---
name: pollen
description: "Hay fever and outdoor pollen. Use when the user asks about birch, grass, weeds, or whether to air a room because of allergies."
---

# Pollen

Read `../../agents/next-air-assistant.md`, `../../knowledge/thresholds.md`, and `../../knowledge/preconditions.md`.

Use Open-Meteo air quality. Ask for pollen on `openmeteo_get_air_quality` (for example `birch_pollen`, `grass_pollen`, `olive_pollen`). If a field is null, say it is unavailable. Do not invent indoor readings. Findings first, then the same pause as `open-close-filter-stay` before you recommend open / close / filter / stay.
```

In `next-air-assistant/agents/next-air-assistant.md`, add those pollen names to `current_variables` on `openmeteo_get_air_quality`. G3 only allows fields that are listed there (or named in a filled Active row of `preconditions.md`). If you want pollen on by default, copy an example row into Active as well.

Routing row:

```text
| hay fever, birch, grass, pollen, allergies | `skills/pollen/SKILL.md` |
```

Command file, if you want the slash command:

```markdown
---
description: Outdoor pollen and whether to air the room.
---

Run the `pollen` skill. Follow `skills/pollen/SKILL.md`.
```

You can skip this whole section and keep the skills that already exist.

## Install the plugin

Install the `next-air-assistant/` folder in the host. Open-Meteo needs no key (`https://open-meteo.caseyjhand.com/mcp`). For Tavily (`https://mcp.tavily.com/mcp/`), approve the prompt or keep a key from <https://app.tavily.com> on your machine only.

| Host | What to do |
|------|------------|
| Claude Code | From the pack root: `claude --plugin-dir ./ex3_next_air_assistant/next-air-assistant`. Then `/mcp` for Tavily. |
| Cursor | Customize → plugins. Install from `ex3_next_air_assistant/next-air-assistant`. Enable MCP when asked. |
| Visual Studio Code | Install or enable MCP from `next-air-assistant/.vscode/mcp.json`. |
| Codex | Install the `next-air-assistant/` folder as a plugin (`plugin.json` and `mcp.json` are there). |
| Antigravity | Install the `next-air-assistant/` folder as a plugin. Enable MCP when asked. |
| Grok | Install or open `next-air-assistant/` so it reads that folder’s `AGENTS.md` and `agents/next-air-assistant.md`. |

Then try the prompts below. Slash commands, if the host has them: `/next-air-assistant:help`, `/next-air-assistant:assess`, `/next-air-assistant:open-close-filter-stay`, `/next-air-assistant:forecast-co2`.

## Try this

Give the helper a place, a country, what the room is for, what you can actually do, and who is in it. Short city-only prompts starve situational intelligence.

> I teach about twenty-five children in a primary classroom in Seville, Spain. We have no indoor sensor and no mechanical cooling, but we can open the windows. One child is sensitive to heat. I need to plan next week’s afternoons.

Then:

> I am at home in a flat in Porto, Portugal. There is wildfire smoke outside. I can close the windows and I have a portable particle filter. I have asthma, which I have not copied into the Active table. Should I close and filter?

> This open-plan office in Lyon, France, just read 1400 ppm of CO2 at about 11:00 local time on a handheld meter. Twelve people are here. The windows can open. Nobody is listed in Active. What should we do with the windows?

> Please forecast indoor CO2 using the labelled classroom example series (synthetic, not a real sensor). The room is in Valencia, Spain. We can open the windows. The file is a 24-hour school day. Forecast the next two hours from the last point, name that clock, and say whether those two hours are a lesson. If they are not, still tell me what the same series did during class hours.

If you added a pollen skill, or you copied a grass-pollen row into Active, ask something that should catch that field.

## License

The plugin is MIT. Weather data by Open-Meteo.com (CC BY 4.0). Air quality: CAMS.

Continue with exercise 4.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
