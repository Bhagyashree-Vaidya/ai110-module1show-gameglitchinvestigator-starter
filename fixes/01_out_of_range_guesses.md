# Fix 1: Out-of-range guesses (like -30) were accepted

## Symptom
The game says "Guess a number between 1 and 100", but a guess of `-30` was accepted and used up an attempt.

## Root cause
- `parse_guess()` only checked that the input was a number. It never checked the range.
- The prompt text was hardcoded to `1 and 100`, even on Easy (1–20) and Hard (1–50).

## Fix
- **`logic_utils.py` → `parse_guess(raw, low, high)`** now takes the difficulty's range and returns
  `(False, None, "Your guess must be between {low} and {high}.")` for anything outside it.
  It also strips whitespace and catches `ValueError` instead of a bare `Exception`.
- **`app.py`** passes `low, high` into `parse_guess`, and the info box now shows the real range.
- An invalid guess (empty, not a number, out of range) **no longer uses up an attempt**.

## Tests
`test_negative_guess_rejected`, `test_guess_above_range_rejected`,
`test_guess_at_range_edges_accepted`, `test_non_number_rejected`, `test_empty_guess_rejected`
