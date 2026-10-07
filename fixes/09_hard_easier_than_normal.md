# Fix 9: "Hard" had a smaller range than "Normal"

## Symptom
Hard was 1–50 and Normal was 1–100. Hard was only harder because it had 3 fewer attempts.

## Fix (`logic_utils.py`)
- Hard is now **1–200 with 7 attempts**.
- With a perfect halving strategy, 1–200 can take 8 guesses, so 7 attempts makes Hard actually
  hard. Normal (1–100, 8 attempts) can always be won with perfect play.

| Difficulty | Range | Attempts |
|------------|-------|----------|
| Easy | 1–20 | 6 |
| Normal | 1–100 | 8 |
| Hard | 1–200 | 7 |

## Tests
`test_ranges_grow_with_difficulty`, `test_hard_settings`
