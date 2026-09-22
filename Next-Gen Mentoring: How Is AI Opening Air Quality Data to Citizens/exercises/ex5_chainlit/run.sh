#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not on PATH."
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
elif ! .venv/bin/python -c "import langchain" >/dev/null 2>&1; then
  echo "Updating packages for LangChain ..."
  .venv/bin/python -m pip install -r requirements.txt
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Put OPENROUTER_API_KEY from exercise 2 in that file, then run again."
  exit 1
fi

echo "Starting Next-Air-Assistant on http://localhost:8000"
echo "The first load often takes 20 to 40 seconds. That is Python waking up, not a crash."
echo "Keep this terminal open. A browser tab opens when the page answers, not before."

(
  for i in $(seq 1 90); do
    sleep 1
    if curl -sf -o /dev/null --max-time 2 "http://127.0.0.1:8000"; then
      if command -v open >/dev/null 2>&1; then
        open "http://localhost:8000"
      elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:8000"
      fi
      break
    fi
  done
) &

.venv/bin/python -m chainlit run app.py -h --port 8000
