# Exercise 4 - Another host: n8n

| Piece | In this exercise |
|-------|------------------|
| **Host** | n8n (Cloud or self-hosted). Every run is stored under **Executions**. |
| **Harness** | This canvas: collect outdoor numbers, then an agent with tools. The 07:00 schedule has no human pause. Chat in the editor does not send mail. |
| **Model** | OpenRouter, same key as exercise 2. The JSON ships `nvidia/nemotron-3.5-lightning:free` so a first run works. Switching that node to a more reliable model (and back) is part of the exercise. |

Import a ready-made canvas. It collects outdoor air from a public service and official European weather warnings from Meteoalarm, then an agent adds situational intelligence (your profile, a news check, a web check) and emails one call: **open**, **close**, **filter**, or **stay**. Telegram is optional. This is an initiation, not a production alert.

## What's in the folder

```
daily-open-meteo-alert.json   <- import this into n8n
README.md
AGENTS.md
```

Yellow notes on the canvas repeat the same points. Read those if you get lost.

## Architecture in one line

```
schedule or chat → profile → Open-Meteo (CAMS + forecast) → Meteoalarm (country) → agent (+ news, web check) → Gmail / Telegram
```

Chat skips Gmail and Telegram. Open-Meteo / CAMS is the air feed here (no key). Meteoalarm is the official-warning feed for Europe (country Atom, no key). You could swap the Open-Meteo boxes for another outdoor API, or add indoor readings from a sensor API you already have. The agent's job stays the same: interpret the data you collected in the context you configured.

## How to use

1. Open n8n. Cloud is enough: `https://app.n8n.cloud/`. Docs: `https://docs.n8n.io/`. Self-host: `https://docs.n8n.io/hosting/`.
2. **Import from File** → `daily-open-meteo-alert.json` from this folder. Do not paste keys into the file.
3. Edit the profile boxes (defaults are Seville, a classroom, grass pollen, `Europe/Madrid`). Put your address on **Gmail** `sendTo` (`you@example.com` is a placeholder).
4. Attach credentials (next section). Red marks on a box usually mean a key is missing.
5. **Test workflow**. You should get a mail (and Telegram if you set it). On the free model this can take several minutes, and it may time out; wait before you assume it hung.
6. Open **Executions**, click that run. Open **Get CAMS air** (`european_aqi`, `pm2_5`), **Compact alerts** (official warnings), then **AI Agent** (the note and any tool calls). If the mail feels wrong, look here before you rewrite the prompt. Docs: `https://docs.n8n.io/workflows/executions/`
7. **Change the model and run again.** On **OpenRouter Chat Model**, if the key has credit, set `anthropic/claude-sonnet-5` and Test workflow with the same profile. Then put the free slug back and run once more. Same CAMS numbers, different note. That contrast is the exercise: a paid model is what you want for a daily mail you will actually read; the free one shows the limit of a `:free` slug. Free-model list: `https://openrouter.ai/collections/free-models`.
8. Then turn **Active** (07:00). Open **Chat** in the editor to ask the same agent a question without sending mail.

| Node | What to type | Default |
|------|----------------|---------|
| **Set Place** | name, country, latitude, longitude | Seville, Spain, 37.38283, -5.97317 |
| **Set Occupant** | who the note is for | classroom, no indoor sensor |
| **Set Preconditions** | asthma, a named pollen, blood pressure, heat, or `none` | grass pollen note |
| **Set Date** | timezone for "today" | Europe/Madrid |
| **OpenRouter Chat Model** | model slug | `nvidia/nemotron-3.5-lightning:free` (try `anthropic/claude-sonnet-5` if you have credit) |
| **Gmail** | your address in **sendTo** | `you@example.com` |

If you move **Set Place**, change **Set Date** to that timezone. Country stops a namesake city (Seville, Ohio) from entering the news search, and it selects the Meteoalarm feed (`Spain` to `spain`).

## Keys

**Required for email**

1. **OpenRouter Chat Model** — key from exercise 2 (`https://openrouter.ai/keys`). The imported model is `nvidia/nemotron-3.5-lightning:free`. If that key has credit, switch the node to `anthropic/claude-sonnet-5` for a readable note, then try the free slug again so you see the difference yourself.
2. **Gmail** — connect your Google account. Put your real address on the node.

**Optional.** Skip any of these; the mail can still send.

3. **Telegram** — bot token from `@BotFather`, chat ID from `@userinfobot`. `YOUR_CHAT_ID` is a placeholder.
4. **Search news** and **Search web weather** — one Header Auth named Tavily (`Authorization: Bearer` plus a key from `https://app.tavily.com`). These are HTTP Request Tools on the agent, not a community Tavily node (n8n Cloud cannot load those as tools). If you skip them, those lines should say unavailable.

Open-Meteo and Meteoalarm do not need a key. Meteoalarm covers Europe (and a few neighbours) by country; outside that the GET fails and the note should say unavailable. Tools add context. They do not replace the collected CAMS numbers or invent an official warning.

## The mistakes that waste a run

1. Putting keys or a chat ID in the JSON.
2. Expecting **Chat** to send Gmail or Telegram. It will not.
3. Changing the place and leaving `Europe/Madrid` on **Set Date**.
4. Treating CAMS as a street station. It is modelled outdoor air.
5. Reading pollen `0` as missing. `0` is a real reading. `null` means CAMS does not publish pollen there (usual outside Europe).
6. A **Change this if** line that is already true (do not say change if PM2.5 exceeds 35 when it is already 77).
7. Treating a Tavily headline as an official warning. Official warnings come from **Get official alerts** (Meteoalarm).
8. Writing "no official warning today" when Compact alerts says the feed is unavailable (usual outside Europe). That line should say unavailable.
9. Judging the canvas from one free-model mail. Change the OpenRouter slug and compare in **Executions**.
10. Expecting the free model to finish in seconds. Give it several minutes, or switch to a paid slug.

## What the note looks like

Headers, in this order: Date and place, Outdoor air, Weather, Official alert, Pollen, What this means, News, Web check, What to do, Note.

**What to do** is one word (open, close, filter, or stay), one sentence, then what would change the call. The **Note** is copied verbatim: not a diagnosis, modelled CAMS via Open-Meteo, official warnings from Meteoalarm when listed, check a national meteorological service, talk to a doctor if someone feels unwell.

Email-and-pollen shape: Ange Russell, n8n template 3699 (`https://n8n.io/workflows/3699-daily-personalized-air-and-pollen-health-alerts-with-ambee-api-and-ai-via-email/`), with Open-Meteo instead of Ambee.

Continue with exercise 5.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
