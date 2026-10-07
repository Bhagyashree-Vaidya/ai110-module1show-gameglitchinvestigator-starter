# Fix 2: Changing difficulty mid-game showed "Attempts left: -1"

## Symptom
Switching difficulty during a running game (e.g. Normal → Easy) made "Attempts left" negative, and the
secret could be outside the new range (e.g. a secret of 98 on Easy, which only goes to 20).

## Root cause
- The attempt limit was recalculated from the dropdown on every rerun, but `attempts` and `secret`
  stayed from the old game. 7 attempts used against Easy's limit of 6 = `-1`.
- `attempts` started at `1` instead of `0` (off by one).
- **New Game** only reset `attempts` and `secret`. It picked the secret from `1–100` no matter the
  difficulty, and never reset `score`, `status` or `history`.

## Fix (`app.py`)
- The current difficulty is saved in `st.session_state.difficulty`.
- **The Difficulty dropdown is disabled once you've made a guess**, with a 🔒 note telling you to finish
  or click New Game. It unlocks again when the game ends.
- Changing difficulty *before* the first guess starts a fresh game in the new range.
- A new `start_new_game(difficulty)` helper resets **all** state (secret from the right range,
  attempts = 0, score = 0, status, history, hint). Both first load and New Game use it.
- "Attempts left" is clamped with `max(0, ...)`, so it can never show a negative number.
- The attempt limits moved to `logic_utils.get_attempt_limit()`.
