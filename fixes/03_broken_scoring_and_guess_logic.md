# Fix 3: Broken guess logic and scoring (final score -60)

## Symptom
The final score could reach -60 on Easy (only 6 attempts). Guesses were compared incorrectly.

## Root cause
1. **The secret was turned into a string on every even attempt** (`secret = str(...)` in `app.py`).
   Comparing `int > str` raised `TypeError`, and the fallback compared *strings*, which sorts
   alphabetically (`"9" > "10"`). So every other guess was judged wrong.
2. **`update_score()` was inconsistent:** "Too High" *added* 5 points on even attempts and took 5 away on
   odd ones. A win used `attempt_number + 1`, which dropped the score by an extra 10.
3. **The score never reset on New Game**, so losses piled up across games. That is how you got to -60.

## Fix
- **`logic_utils.py` → `check_guess(guess, secret)`** always compares two ints. The string fallback is
  removed. `app.py` passes the real integer secret.
- **`logic_utils.py` → `update_score()`**: every wrong guess costs 5 points. A win scores
  `100 - 10 × (attempt − 1)`, so a first-try win = 100, with a minimum of 10.
- **`app.py`**: `start_new_game()` resets the score to 0 (see Fix 2). The worst possible loss on Easy is now -30.
- All four functions were moved out of `app.py` into `logic_utils.py`, and `app.py` imports them.

## Tests
`test_winning_guess`, `test_hint_compares_numbers_not_strings`, `test_first_try_win_scores_100`,
`test_win_score_has_floor`, `test_wrong_guesses_always_cost_points`, `test_worst_case_easy_loss_bounded`
