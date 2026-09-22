# Next-Air-Assistant - exercises

**Talk by:** Miguel Escribano Hierro (inBiot, Spain)
**Webinar:** How Is AI Opening Air Quality Data to Citizens? · 22 September 2026
**Project:** NextAIRE (HORIZON-WIDERA 101217310) · `https://nextaire.eu/`

Hands-on exercises for a public indoor-air assistant. Unzip this pack and open **this folder** in your host. It is the project. `AGENTS.md` here is the workshop file (Claude Code loads it through `CLAUDE.md`). Each exercise folder has the same pair. The air-quality persona lives in `ex3_next_air_assistant/next-air-assistant/agents/next-air-assistant.md`. Work through the exercise folders in order.

> No API keys are stored in these files. You add your own on the machine. The labelled classroom CO2 series is **synthetic**, invented for the exercises. Outdoor numbers come from live Open-Meteo / CAMS when you run the plugin.

## This pack is an initiation

These exercises are a first look at how a generative-AI helper is put together: an agent, skills, a small knowledge folder, a model, and a couple of public tools. They are not a production system.

They do not include robust guardrails reviewed by experts, a serious evaluation suite (evals), or cost control. Those are the next problems. Keep investigating them. At inBiot we are working them in one way; that stack is not in this zip. The field is early. Some of these questions do not yet have a settled answer.

The pack starts a conversation. It does not finish one.

## Host, harness, and model

A **host** is the runtime: the application where the agent actually runs. Cursor, Claude Code, Claude Desktop, ChatGPT, Antigravity, Grok, and n8n are hosts. Each host ships its own window, rules, and way of calling tools.

A **harness** is what that host already wraps around the model: skills, tools, an MCP client, the chat or canvas, context, permissions, and whether a person can pause before a decision. Commercial apps sell host and harness together. A plugin such as Next-Air-Assistant does not replace that harness. It joins it and augments it: persona, skills, a small knowledge folder, extra tools. This pack lets you see the three parts apart.

A **model** is the language model. Here that is often a free one through OpenRouter. The same model can feel different in two hosts because the harness changed. Each exercise names all three at the top.

## The exercises, in order

| # | Folder | Concept |
|---|--------|---------|
| 1 | `ex1_workspace` | Choosing a host (AI app or IDE) |
| 2 | `ex2_openrouter` | Enabling OpenRouter to use free LLMs |
| 3 | `ex3_next_air_assistant` | Customizing your agent: Next-Air-Assistant as a plugin |
| 4 | `ex4_n8n_alerts` | Building the agent with n8n: situational intelligence in your inbox |
| 5 | `ex5_chainlit` | Building with Chainlit: a local chat |
| 6 | `ex6_openair` | Adding openair tools: an MCP for deterministic chart analysis |
| 7 | `ex7_always_on_host` | Installing Hermes: an agent that grows with you |

## Getting your keys

OpenRouter (exercise 2) is how you reach free models; you can add credit later if you want. In Cursor, Antigravity, and Visual Studio Code that is an OpenAI-compatible provider. In Claude Code it is Francesco Bardozzo’s wiring: the OpenRouter Anthropic endpoint and three environment variables, in this pack as `ex2_openrouter/settings.local.json.example`. For exercises 3, 4, and 5 you may also want a Tavily key from <https://app.tavily.com>. In Claude Code, sign in with `/mcp`; otherwise set `TAVILY_API_KEY` on your machine. For exercise 4 you need n8n, an email account, and the OpenRouter credential from exercise 2. On that canvas, try a paid OpenRouter slug and the free one with the same profile; the difference is the exercise. Tavily on **Search news** and **Search web weather** is optional (same Header Auth). Open-Meteo does not require a key.

After you have edited `ex3_next_air_assistant/next-air-assistant`, install that folder as a plugin in the host. Claude Code:

```bash
claude --plugin-dir ./ex3_next_air_assistant/next-air-assistant
```

Cursor, Codex, and the others: install from this same folder. Do not add a second Next-Air-Assistant from a marketplace.

## Related work

Other people have built air-quality assistants before you. These are the ones we checked; they are paths, not templates.

- VayuBuddy (IIT Gandhinagar, 2024): a citizen asks in plain language, the model writes and runs Python over India's public sensor data, the answer comes back as text or a plot. `https://arxiv.org/abs/2411.12760` · demo `https://huggingface.co/spaces/SustainabilityLabIITGN/VayuBuddy`
- VayuChat (IIT Gandhinagar, 2025): the same idea with demographics and funding records, code returned with every answer, and a benchmark. Its rule is worth copying: never hand the model the table; make it write code. `https://arxiv.org/abs/2511.01046`
- AMI, an LLM-enhanced air monitoring interface via MCP (2025): live sensors exposed as MCP tools, so the model only touches numbers through them. `https://arxiv.org/abs/2511.03706`
- HIAPLLM (2026): a Raspberry Pi fetches Open-Meteo, a local model under Ollama answers, nothing leaves the network. The closest cousin of exercises 3 to 5. `https://github.com/ParthaPRay/Air_Pollution_LLM_Advisor`
- PLAM, Plovdiv Air Monitoring (2026): planning agents and language agents sharing the work over a city's sensors. For when you want more than one agent. `https://doi.org/10.3390/fi18020078`
- Crew Air Analyzer: a small open-source multi-agent analysis of indoor files with CrewAI. Static data, no standards, but a clean example of roles. `https://github.com/rooneyrulz/crew-air-analyzer`
- AirGPT (2025) and Emission-GPT (2025): assistants that read a curated literature base instead of remembering it. `https://doi.org/10.1038/s41612-025-01070-4` · `https://arxiv.org/abs/2510.02359`

## Reference links

**The webinar and the project**

- NextAIRE · `https://nextaire.eu/`
- CORDIS 101217310 · `https://cordis.europa.eu/project/id/101217310`

**Tools used in the pack**

- OpenRouter · `https://openrouter.ai` · keys: `https://openrouter.ai/keys`
- Tavily · `https://app.tavily.com`
- Open-Meteo (weather CC BY 4.0; air quality CAMS) · `https://open-meteo.com/`
- Meteoalarm (official European weather warnings, country Atom) · `https://feeds.meteoalarm.org/`
- Claude Code plugins · `https://code.claude.com/docs/en/plugins`
- n8n · `https://n8n.io/`
- Chainlit · `https://docs.chainlit.io/`
- openair-ai-kit · `https://github.com/miguel-escribano/openair-ai-kit`
- Hermes Agent (example for exercise 7) · `https://hermes-agent.nousresearch.com/`

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
