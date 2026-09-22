# Preconditions (optional)

Personal notes for this assistant. Not a medical record and not a diagnosis. Leave the Active table empty if you do not want health notes used. The assistant may treat filled Active rows as extra caution when it recommends open, close, filter, or stay. It must not prescribe treatment or invent a condition you did not write.

You can also say the same kind of thing in chat (“I have asthma”, “one child is sensitive to heat”). That spoken note is context for the pause. Only a filled Active row can add extra Open-Meteo fields such as a named pollen. If you want grass pollen on every run, copy the example row into Active. If you only mention it once in conversation, the helper should ask, not quietly widen the tool call.

Skills should read this file. They must not copy these rows into `thresholds.md`.

## Active

Only this table counts. Empty rows do not count.

| Who | Note | What it changes |
|-----|------|-----------------|
| | | |

## Examples (copy up only if they apply)

These rows are **not** in force. Copy a line into Active if you mean it.

| Who | Note | What it changes |
|-----|------|-----------------|
| Me | Asthma | Prefer close or filter when outdoor PM or smoke is the story. |
| Me | Grass pollen allergy | Request `grass_pollen` from Open-Meteo if that field exists; lean close or stay on high grass days. |
| Occupant | High blood pressure | Heat is extra caution. Still not medical advice. |
| Occupant | Low blood pressure | Same: heat is extra caution. Still not medical advice. |
| Child in this classroom | Heat-sensitive | Afternoon outdoor max at or above the heat lines in `thresholds.md` is a stronger stay. |

Open-Meteo pollen names this plugin may add to the air-quality call when an Active row names them: `alder_pollen`, `birch_pollen`, `grass_pollen`, `mugwort_pollen`, `olive_pollen`, `ragweed_pollen`. If the field is null, say it is unavailable.
