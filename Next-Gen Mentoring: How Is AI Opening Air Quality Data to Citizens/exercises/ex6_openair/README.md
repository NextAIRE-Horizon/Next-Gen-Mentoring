# Exercise 6 - A tool, not a new host

| Piece | In this exercise |
|-------|------------------|
| **Host** | One you already used. Default: the IDE from exercise 1. Optional: the local chat app from exercise 5, or n8n only if it runs on this machine. |
| **Harness** | Unchanged. You add an MCP *server* of plot tools. You do not install a second assistant. |
| **Model** | Whatever that host is already using. |

This exercise is optional and advanced. If you cannot run Git, Python, and R, stop here. Exercises 1 to 5 already showed host, model, plugin, another host, and a runtime you write.

openair is a trusted R package for air-quality charts. The kit wraps it as an MCP server so a host can ask for a plot instead of you opening RStudio. The kit is not affiliated with openair-project. Landing page: `https://github.com/miguel-escribano/openair-ai-kit`.

## What you do

Follow the kit README to start the server on your machine. Then connect that server to **one** host, not all of them.

**The IDE from exercise 1** is the path we expect. Cursor, Claude Code, Codex, and Antigravity already know how to load an MCP server from a plugin or a config file. If the IDE and R share a machine, use local stdio. If the server is elsewhere, R stays on that machine and the IDE is the client.

**The local chat app from exercise 5** is optional. Attach the same MCP there only if you completed that exercise. The chat app must still start without R; openair is an extra, not a requirement.

**n8n** is a footnote, not a recipe. n8n Cloud cannot see an R process on your laptop. Self-hosted n8n on the same computer might reach a local URL. We do not ship that wiring. Skip n8n unless you already know how to add an MCP or HTTP tool on a self-hosted instance.

## When it is connected

In that host, try:

```
Use tests/fixtures/felisa_munarriz.json in the plugin repo.
Prepare hourly Europe/Madrid, then time_plot all pollutants. MCP tools only.
Do not search for data/felisa.xlsx or other server paths.
```

An air-quality figure is work for a library that already encodes the data, not for a sketch the model invents. openair is one such library. A host with its own chart widgets would be another. The chart should come from the tool. Exercise 5 can show the same numbers in a table; it is not the place to ask the model to invent a dashboard.

Continue with exercise 7 if you want an always-on host.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
