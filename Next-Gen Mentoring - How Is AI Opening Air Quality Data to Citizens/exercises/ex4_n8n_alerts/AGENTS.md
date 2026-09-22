# Exercise 4

Import `daily-open-meteo-alert.json` into n8n. Collect outdoor air (Open-Meteo / CAMS) and official European weather warnings (Meteoalarm country Atom), then add situational intelligence from the user's place, setting, and preconditions plus optional Tavily tools. Mail (and optional Telegram) is that interpretation, not a dump of the API. Another outdoor service or a user's own sensor API could replace the two Open-Meteo boxes.

- OpenRouter from exercise 2. Not OpenAI. The JSON ships `nvidia/nemotron-3.5-lightning:free` so a first run works. Switching **OpenRouter Chat Model** to a paid Sonnet (`anthropic/claude-sonnet-5`) and back is part of the exercise: same collected numbers, different note. Prefer the paid slug for a daily mail you will read. Free models can take several minutes or time out.
- CAMS is modelled outdoor air, not a station. `domains=auto`. Pollen `0` is a reading; `null` is unavailable (usual outside Europe).
- **Get official alerts** is Meteoalarm for `Set Place.country` (Spain to spain). Collection, not a tool. Compact alerts keeps a short list. Outside Europe the feed fails; say unavailable, not "no warning today". Do not invent a warning.
- Calendar day from **Set Date** (`$now` in the place timezone), not from the model.
- **Set Place** includes country. Search web weather is `Weather in place, country?` (advanced, today). Tools must not replace CAMS numbers. If a tool is missing, say unavailable.
- Chat in the editor must not send Gmail or Telegram.
- Preconditions are user-stated notes, not a diagnosis. Do not invent a condition.
- Fill weather copies Open-Meteo into ☀️ only if no Weather header is present (🌦️ already counts), appends the ℹ️ Note if skipped, and rewrites **Change this if** when that threshold is already true.
- After a run, open **Executions**: **Get CAMS air**, **Compact alerts**, then **AI Agent**.
- Do not put API keys, a bot token, or a chat ID in files in this folder. `YOUR_CHAT_ID` and `you@example.com` are placeholders.

Do not invent Open-Meteo, CAMS, Meteoalarm warnings, news, indoor readings, or a calendar date.
Do not name commercial indoor monitors, a vendor product line, or a private consultant. This pack has no private sensor API.
