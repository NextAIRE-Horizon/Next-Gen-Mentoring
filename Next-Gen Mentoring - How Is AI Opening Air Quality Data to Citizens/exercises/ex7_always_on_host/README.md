# Exercise 7 - A host that stays on

| Piece | In this exercise |
|-------|------------------|
| **Host** | Hermes Agent on your computer, desktop app first. Not an IDE, not n8n Cloud, not a vendor chat site. |
| **Harness** | Whatever Hermes ships (chat, tools, later skills and MCP). Next-Air-Assistant is **not** wired here yet. |
| **Model** | OpenRouter, the same key as exercise 2. Local models can wait. |

This exercise is optional and for the brave. The first job is only this: run a **non-commercial** desktop agent, on your machine, with a model you already pay for or get free through OpenRouter. That is the point. Cursor, Claude, ChatGPT, and Grok are commercial hosts you do not own. Hermes is MIT, Nous Research. Docs: `https://hermes-agent.nousresearch.com/`.

## Step 1 - Install the desktop app

Download Hermes Desktop for your system (Windows, macOS, or Linux) from their site and install it like any other application. Their own quickstart calls that installer the recommended path: `https://hermes-agent.nousresearch.com/docs/getting-started/quickstart`.

Do not start with `curl | bash`, a VPS, Telegram, or a paid portal. Those exist. They are a second session, after a local chat works.

## Step 2 - One model, one conversation

In Hermes, choose OpenRouter and paste the key from exercise 2. Send a short message. If it replies, you are done with this exercise as a first look.

Hermes can talk to a local endpoint later (Ollama, LM Studio, and similar). Do not do that on day one. Their docs also ask for a large context window (on the order of 64k tokens). Get OpenRouter working first.

## The plugin comes after

We have **not** yet checked that Next-Air-Assistant, Open-Meteo, Tavily, the n8n note, or openair MCP load cleanly inside Hermes. Do not spend the workshop reverse-engineering that. If you already know Agent Skills and MCP in Hermes, you may point it at `../ex3_next_air_assistant/next-air-assistant/` on your own. Treat anything that works as a bonus.

The honest sequence is: desktop app, OpenRouter, a chat that answers. Skills, MCP, always-on gateway, and our indoor-air plugin are the next investigation, not this page.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
