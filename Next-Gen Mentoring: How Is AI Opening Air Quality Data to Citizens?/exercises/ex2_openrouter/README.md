# Exercise 2 - Choose a model (OPTIONAL)

| Piece | In this exercise |
|-------|------------------|
| **Host** | The same IDE you opened in exercise 1. You do not switch hosts. |
| **Harness** | Unchanged. Still the product default. |
| **Model** | One you pick on OpenRouter. A `:free` model is enough. The same key is used again in n8n. |

The model is swappable. The host stays the same.

Create an OpenRouter account so the same key can drive free models in your host and, later, the n8n workflow. You can stay on the free tier, or add credit if you want to try paid models.

1. Sign up at <https://openrouter.ai>.
2. Open <https://openrouter.ai/keys> and create a key (`sk-or-v1-...`).
3. Keep the key on your machine only. Do not commit it.
4. Free models rotate. The live list is <https://openrouter.ai/collections/free-models>. Pick a `:free` model that supports tools if you will use n8n agents. A working default today is `nvidia/nemotron-3.5-lightning:free`. `openai/gpt-oss-20b:free` is no longer free.

Put that key into the host you opened in exercise 1. Cursor, Antigravity, and Visual Studio Code take an OpenAI-compatible endpoint. Claude Code does not: it talks to the Anthropic API shape. OpenRouter exposes that shape as well, so you still change the model without leaving Claude Code. Francesco Bardozzo wrote that wiring. This folder is the copy for this pack.

**Cursor.** Settings → Models. Add OpenRouter, or add an OpenAI-compatible provider with base URL `https://openrouter.ai/api/v1` and your OpenRouter key. OpenRouter’s own notes: <https://openrouter.ai/docs/guides/community/cursor>. Pick a `:free` model and send a short message to check that it replies.

**Antigravity.** Add an OpenAI-compatible provider with the same base URL and key. Choose a free model and send a short message.

**Visual Studio Code and Codex.** Codex already talks to OpenAI. You only need OpenRouter here if you want the same free models as in n8n. Use an OpenAI-compatible extension or provider with `https://openrouter.ai/api/v1`.

**Claude Code.** Stay in the pack folder you opened in exercise 1. Claude Code reads these variables:

| Variable | Value | Why |
|----------|-------|-----|
| `ANTHROPIC_BASE_URL` | `https://openrouter.ai/api` | Send requests to OpenRouter. The path is `/api`, not `/api/v1`. |
| `ANTHROPIC_AUTH_TOKEN` | your `sk-or-v1-...` key | This is where the OpenRouter key goes. |
| `ANTHROPIC_API_KEY` | empty | If this is set, Claude Code calls Anthropic and ignores OpenRouter. |
| `ANTHROPIC_MODEL` | e.g. `nvidia/nemotron-3.5-lightning:free` | The model you pick. Change this slug to swap models. |

Use one of the two methods below, not both. If you set `ANTHROPIC_MODEL` in the project file and in a shortcut, they fight.

Copy `ex2_openrouter/settings.local.json.example` to `.claude/settings.local.json` in the pack root (the folder that contains `ex1_workspace`). Paste your key. Leave `ANTHROPIC_API_KEY` as an empty string. Launch `claude` from that folder. That file stays on your machine; this pack gitignores `.claude/`.

If you prefer to set the variables only for one launch, do it in the same terminal before `claude`. On Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL="https://openrouter.ai/api"
$env:ANTHROPIC_AUTH_TOKEN="sk-or-v1-..."
$env:ANTHROPIC_API_KEY=""
$env:ANTHROPIC_MODEL="nvidia/nemotron-3.5-lightning:free"
claude
```

On macOS, Linux, or WSL, `install-openrouter-models.sh` in this folder writes a `ccor` shortcut that does the same thing. Run `bash install-openrouter-models.sh`, then `source ~/.bashrc`, then `ccor` from the pack folder. Do not also fill `ANTHROPIC_MODEL` in `.claude/settings.local.json` if you use that shortcut.

Three mistakes that break the wiring: the base URL ends in `/api/v1`; `ANTHROPIC_API_KEY` is filled; the model is set twice.

When a free model answers in the host (or you have a key ready for n8n), continue with exercise 3.

---

*Next-Air-Assistant: citizen IAQ assistant*  
*Miguel Escribano Hierro (inBiot) · NextAIRE webinar, 22 September 2026: How Is AI Opening Air Quality Data to Citizens?*  
*`https://nextaire.eu/` · HORIZON-WIDERA 101217310*
