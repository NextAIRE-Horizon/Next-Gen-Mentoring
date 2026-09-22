# Next-Air-Assistant exercises

You are helping the user work through this workshop pack. Follow `README.md` in order. Keep **host**, **harness**, and **model** distinct: the host is the runtime (the app where the agent runs); the harness is what that app wraps around the model; the model is the LLM. Exercise 1 opens a host. Exercise 2 chooses a model in the same host. Exercise 3 loads the plugin (the portable harness) there. Exercise 4 is another host (n8n). Exercise 5 is a runtime they write: the local Chainlit app in `ex5_chainlit/`, loading the exercise 3 plugin. Exercise 6 is optional: host the openair MCP and attach it to one host they already used (IDE default; local chat if they ran 5; n8n only if self-hosted on this machine). It is a tool server, not a new host. Exercise 7 is optional and for the brave: install Hermes Desktop, chat with OpenRouter from exercise 2. Do not treat plugin/MCP wiring as done.

This unzipped folder is the project. Do not create a second workspace. After they customise `ex3_next_air_assistant/next-air-assistant`, they install that folder as a plugin in the host. Do not install a second Next-Air-Assistant from a marketplace. If they treat the pack as a finished production system, correct them: it is an initiation. Guardrails reviewed by experts, evals, and cost control are not in this zip.

When they ask about indoor air, outdoor CAMS, heat, news, or whether to open, close, filter, or stay, follow `ex3_next_air_assistant/next-air-assistant/agents/next-air-assistant.md`. That file is the air-quality agent. This file is not. Optional health notes live in `ex3_next_air_assistant/next-air-assistant/knowledge/preconditions.md` (Active table only).

Do not invent Open-Meteo, CAMS, news, or indoor readings.
Do not name commercial indoor monitors, a vendor product line, or a private consultant. This pack has no private sensor API.
Do not put API keys in files in this folder.
