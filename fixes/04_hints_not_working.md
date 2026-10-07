# Fix 4: Hints didn't work

## Symptom
Guessing 21 when the secret was 98 said "Go LOWER!". Sometimes no hint appeared at all.

## Root cause
- **The messages were swapped** in `check_guess()`. When the guess was too high it said "Go HIGHER", and when it was too low it said "Go LOWER".
- On even attempts the string comparison (see Fix 3) gave wrong directions even with correct messages.
- The hint was only drawn during the run where you clicked Submit. Any rerun (like toggling
  "Show hint") made it disappear. The game-over check also called `st.stop()` *before* the hint
  code, so the last hint never showed.

## Fix
- **`logic_utils.py` → `check_guess()`**: "Too High" → `📉 Go LOWER!`, "Too Low" → `📈 Go HIGHER!`, always
  comparing integers.
- **`app.py`**: the latest hint is saved in `st.session_state.last_hint` and drawn on every rerun while the
  game is in progress. The "Show hint" checkbox now turns it on and off right away.
- Win/loss messages are drawn from `status` on every run, instead of `st.stop()` cutting the page short.

## Tests
`test_guess_too_high` and `test_guess_too_low` now also check the direction of the hint message.
