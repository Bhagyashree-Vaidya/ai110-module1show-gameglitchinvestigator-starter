# Fix 7: You could win with a negative score

## Symptom
Winning on the 8th guess on Normal gave a final score of **-5**. That's 7 wrong guesses × -5, then a win worth 30.

## Root cause
This was introduced by Fix 3. Wrong guesses cost 5 points each *and* the win bonus also shrinks by 10 per
attempt, so a late win was penalised twice and could end below zero.

## Fix (`logic_utils.py` → `update_score()`)
A win now returns `max(10, current_score + points)`, so winning always leaves you with at least 10.
Early wins are unchanged. For example, a win on guess 2 is still -5 + 90 = 85.

## Tests
`test_late_win_never_negative`, `test_early_win_unaffected_by_floor`
