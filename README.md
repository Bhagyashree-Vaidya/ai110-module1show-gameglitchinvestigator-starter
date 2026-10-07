# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game purpose

A Streamlit number-guessing game. The app picks a secret number in a range set by the difficulty
(Easy 1–20 with 6 attempts, Normal 1–100 with 8, Hard 1–200 with 7). After each guess you get a
"Go HIGHER / Go LOWER" hint. You win by finding the number before your attempts run out, and you
score more points for winning in fewer guesses.

### Bugs found

| # | Bug | Root cause |
|---|-----|------------|
| 1 | Out-of-range guesses like `-30` were accepted | `parse_guess()` never checked the range, and the prompt always said "1 and 100" |
| 2 | Changing difficulty mid-game showed "Attempts left: -1" | The attempt limit changed but attempts and secret didn't. Attempts started at 1 instead of 0, and New Game reset only part of the state |
| 3 | Guess logic and scoring broken (final score of -60) | On even attempts the secret became a string, so guesses were compared alphabetically. "Too High" sometimes *added* points, and the score never reset between games |
| 4 | Hints were wrong or missing | The "Go HIGHER" and "Go LOWER" messages were swapped, and the hint disappeared on any rerun |
| 5 | No balloons on a win | `st.balloons()` ran right before `st.rerun()`, which cleared the page before the animation played |
| 6 | Guessing the same number again used up an attempt | Guesses were never checked against the history |
| 7 | A late win could end with a negative score (e.g. -5) | Wrong guesses and the shrinking win bonus both penalised extra attempts |
| 8 | `50.9` was silently cut to 50; `1_0` and `٥` were accepted | `int(float(...))` dropped decimals, and Python's `int()` accepts more formats than a game should |
| 9 | "Hard" (1–50) had a smaller range than "Normal" (1–100) | The difficulty settings didn't scale |

### Fixes applied

1. **Range validation:** `parse_guess(raw, low, high)` rejects numbers outside the difficulty's range.
   Invalid guesses no longer use up an attempt, and the prompt shows the real range.
2. **Difficulty lock:** the Difficulty dropdown is disabled once you make a guess and unlocks when
   the game ends. A `start_new_game()` helper resets every part of the game state and picks the
   secret from the correct range. "Attempts left" can't go below 0.
3. **Correct comparisons and scoring:** `check_guess()` always compares integers. Each wrong guess
   costs 5 points. A win scores `100 - 10 × (attempt − 1)`, with a minimum of 10.
4. **Working hints:** the messages point the right way, and the latest hint is saved in session
   state so it stays visible. The "Show hint" checkbox turns it on and off.
5. **Balloons:** a win sets a `celebrate` flag, and the balloons play on the next run, after the rerun.
6. **Repeated guesses:** you get "You already guessed 50" and no attempt or points are used.
7. **Score floor:** a win always leaves you with at least 10 points.
8. **Strict input:** only whole numbers made of plain digits are accepted. Decimals get "Enter a whole number".
9. **Hard difficulty:** now 1–200 with 7 attempts.
10. **Refactor:** all game logic moved from `app.py` into `logic_utils.py`, and `app.py` imports it.

Detailed write-ups for each fix are in the [`fixes/`](fixes/) folder.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open http://localhost:8501. The game starts on Normal (1–100, 8 attempts).
2. Pick a difficulty in the sidebar before guessing. The range, the attempt count and the prompt update to match.
3. Enter `-30` and click **Submit Guess**. The game shows "Your guess must be between 1 and 100." and the attempt count doesn't change.
4. Enter `50.9`. The game says "Enter a whole number (no decimals)." and no attempt is used.
5. Enter `50`. A correct hint appears (e.g. "📈 Go HIGHER!" when the secret is 74), attempts left drops by one, and the Difficulty dropdown locks 🔒.
6. Submit `50` again. The game says "You already guessed 50" and no attempt is used.
7. Keep guessing using the hints. A win shows balloons and your final score. Running out of attempts shows the secret and your score.
8. Click **New Game** to reset the score, attempts and history. The difficulty unlocks again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ .venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
collected 22 items

tests/test_game_logic.py ......................                           [100%]

============================== 22 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
