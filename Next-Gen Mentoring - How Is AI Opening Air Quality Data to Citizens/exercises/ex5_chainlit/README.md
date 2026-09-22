# Exercise 5 - A runtime you write

| Piece | In this exercise |
|-------|------------------|
| **Host** | This small Chainlit app. It runs on your machine and opens in the browser. You own the runtime. |
| **Harness** | LangChain `create_agent` wraps the model (chat, tools, context, the pause). Next-Air-Assistant from exercise 3 is loaded from markdown (`agents/`, `skills/`, `knowledge/`) and augments that wrap. |
| **Model** | OpenRouter. Same key as exercise 2. The sidebar lists `:free` models first, then paid slugs if you add credit. |

n8n (exercise 4) is a workflow: the canvas already chose the steps. This is a **chat**: you say what you want. Same outdoor feed, different host.

For inspiration, look at VayuBuddy (IIT Gandhinagar, 2024): a chatbot where a citizen asks in plain language, the model writes and runs Python over India's public government sensor data, and the answer comes back in plain language or as a plot. Paper: `https://arxiv.org/abs/2411.12760`. Live demo: `https://huggingface.co/spaces/SustainabilityLabIITGN/VayuBuddy`. It is the same shape as this exercise (question, code and tools, answer), with public outdoor data there and your room here. Once the app runs, you can grow it in that direction.

This exercise is advanced. You need Python 3.11 or newer on the machine. An IDE is useful for the terminal; it is not required. You do not install the plugin into Cursor for this step. The app reads the plugin folder itself.

## What you will see

A local page at `http://localhost:8000`. The left column is chat settings (the model list, then temperature and max output tokens) and new chat. Those two sliders belong to this host: they change how OpenRouter samples, not the assistant’s personality in the markdown. Tool calls show as steps so you can see Open-Meteo working. After the tools, the answer text streams into the bubble (hidden think tags stay off-screen). Starter chips are full situational prompts (place, room, what you can do, who is there), not one-line city names. Slash commands match the skills: help, assess, open-close-filter-stay, forecast-co2.

Pollen fields are not a switch the model can flip. This host reads the Active table in the plugin and only then adds named pollen to the CAMS call. Chat history lives in RAM for this run of the app. There is no login, no voice, no vendor sensor API, and no database. Restart the window and the thread is gone. This pack is an initiation: it does not include abuse screens, evals, or cost control.

This chat is tables and prose from the tools. If you ask for a dashboard or an HTML sparkline, a small model will often draw something that does not match the numbers. Charts that encode the data belong in exercise 6.

The loop is LangChain's `create_agent`. That call compiles a LangGraph. You do not write the nodes. If you want the pause in Decide to become a real graph interrupt, that is the next step, not this exercise.

## Run it (Windows)

Double-click `Start Next-Air-Assistant.bat` in this folder. The first time it creates `.venv`, installs packages, and copies `.env.example` to `.env`. Paste `OPENROUTER_API_KEY` from exercise 2 into `.env`, save, and double-click again. The black window is the heartbeat: the first load often takes 20 to 40 seconds. A browser tab opens when the page answers, not at four seconds. Leave that window open until you are done.

The bat file uses the folder it lives in (`%~dp0`). You can unzip the pack anywhere.

## Run it (macOS or Linux)

```bash
chmod +x run.sh
./run.sh
```

Put the OpenRouter key in `.env` first (copy `.env.example`). Then open `http://localhost:8000`.

## Optional

Tavily news: put `TAVILY_API_KEY` in `.env`. If it is missing, the assistant should say news is unavailable and continue.

Free model slugs rotate. If a sidebar model fails, edit `models.py` or `OPENROUTER_MODEL` in `.env`. Paid slugs (`openai/gpt-4o-mini`, `google/gemini-2.5-flash`, `anthropic/claude-sonnet-5`, and the non-`:free` Nemotron) need OpenRouter credit. Without credit they return a payment error. Close `Start Next-Air-Assistant.bat` and start it again after you change the model list.

Continue with exercise 6 if you can host an MCP plot server.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
