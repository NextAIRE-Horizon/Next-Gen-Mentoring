# Next-Air-Assistant

Read **[agents/next-air-assistant.md](agents/next-air-assistant.md)** for persona, OODA, MCP tools, and skill routing. Adapters in this folder only point. They do not restate thresholds or preconditions.

## MCP

Default MCPs (no Node): Open-Meteo `https://open-meteo.caseyjhand.com/mcp` (CAMS, no account) and Tavily `https://mcp.tavily.com/mcp/` (news; OAuth or a key the user adds locally, never a key in this repo). Config: [mcp.json](mcp.json).

## Skills

See the routing table in `agents/next-air-assistant.md`. The pack ships `help`, `assess`, `open-close-filter-stay`, and `forecast-co2`. If you add a skill, add a row there.
