#!/usr/bin/env bash
# Claude Code + OpenRouter. The three-variable trick is Francesco Bardozzo's
# (University of Salerno). Adapted here so exercise 2 is true on that host:
# you pick a model without leaving Claude Code.
# No real API key is stored; the script prompts for yours.
set -euo pipefail

TARGET="$HOME/.openrouter-models.sh"
RCFILE="$HOME/.bashrc"
BEGIN="# >>> openrouter-models >>>"
END="# <<< openrouter-models <<<"

echo "Paste your OpenRouter API key (sk-or-v1-...)."
echo "Leave it blank and press ENTER to add it later by hand."
read -rp "Key: " OR_KEY_INPUT
[ -z "${OR_KEY_INPUT:-}" ] && OR_KEY_INPUT="sk-or-v1-YOUR-KEY"

cat > "$TARGET" <<'FUNCS'
# Claude Code + OpenRouter. Variables are set only for that claude call.
# ANTHROPIC_API_KEY must stay empty. ANTHROPIC_BASE_URL is /api, not /api/v1.
# Do not also set ANTHROPIC_MODEL in the project's settings.local.json.
# Free slugs rotate: https://openrouter.ai/collections/free-models

export OR_KEY="__OR_KEY__"
export OR_BASE="https://openrouter.ai/api"

# Working default for this pack (swap the slug to pick another :free model)
ccor() {
  ANTHROPIC_BASE_URL="$OR_BASE" ANTHROPIC_AUTH_TOKEN="$OR_KEY" ANTHROPIC_API_KEY="" \
  ANTHROPIC_MODEL="nvidia/nemotron-3.5-lightning:free" \
  ANTHROPIC_SMALL_FAST_MODEL="nvidia/nemotron-3.5-lightning:free" \
  claude "$@"
}
FUNCS

sed -i "s|__OR_KEY__|${OR_KEY_INPUT}|" "$TARGET"
chmod 600 "$TARGET"
echo "Functions written to: $TARGET (permissions 600)"

if [ -f "$RCFILE" ]; then
  cp "$RCFILE" "${RCFILE}.bak.$(date +%Y%m%d-%H%M%S)"
  echo ".bashrc backup created."
else
  touch "$RCFILE"
fi

if grep -qF "$BEGIN" "$RCFILE"; then
  echo ".bashrc already sources the functions: no change made."
else
  {
    printf '\n%s\n' "$BEGIN"
    printf 'source "%s"\n' "$TARGET"
    printf '%s\n' "$END"
  } >> "$RCFILE"
  echo "Source line added to $RCFILE"
fi

echo
echo "Done. Run:        source ~/.bashrc"
echo "Then, from the pack folder: ccor"
if [ "$OR_KEY_INPUT" = "sk-or-v1-YOUR-KEY" ]; then
  echo
  echo "You did not enter a key. Open the file and add it:  $TARGET"
fi
