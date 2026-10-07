# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code in agent mode. My first prompt listed four bugs with screenshots (negative guesses accepted,
"Attempts left: -1" after changing difficulty, a final score of -60, and broken hints). I asked it to make a file for
each resolution and to move `check_guess` / `parse_guess` into `logic_utils.py`, fix them, and update the
import in `app.py`. Later prompts: "can you find more glitches?", then "fix all of them".

**What did the agent do?**

Files modified: `logic_utils.py`, `app.py`, `tests/test_game_logic.py`, `README.md`, `reflection.md`, and new
`fixes/01`–`09` write-ups.

1. Read `app.py`, `logic_utils.py` and the starter tests, and traced each symptom to its code cause.
2. Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` into `logic_utils.py`
   and fixed them. `app.py` now imports them.
3. Added a new **difficulty lock** feature: the Difficulty dropdown is disabled once a game is in progress, and
   a `start_new_game()` helper resets all game state. It also added **repeat-guess detection**, so guessing a
   number already in history doesn't cost an attempt.
4. Rewrote the starter tests (they compared a tuple to a string, so they could never pass) and added edge-case
   tests. It ran `pytest` after each round of fixes.
5. Played the game in the built-in browser to confirm the fixes: -30 rejected, correct "Go HIGHER!" hint,
   dropdown locked, win and New Game.
6. On "find more glitches", it found 6 more. Two were bugs it had introduced itself: missing win balloons and a
   negative win score. It fixed them all and confirmed the balloons fix with Streamlit's `AppTest`.

**What did you have to verify or fix manually?**

- I reviewed every diff before committing.
- The agent's first scoring fix let a late win end at -5, and its `st.rerun()` change stopped the balloons from
  showing. Both were caught in the "find more glitches" review and revised (fixes 5 and 7).
- During testing, my running Streamlit server kept the old `logic_utils.py` loaded, because Streamlit only reloads
  `app.py`. I had to restart it to see the new behaviour.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`-30`) | "It ask to pick number from 1 to 100 but accepts number in negatives example -30 … Can you make file for each of the resolution ?" | `test_negative_guess_rejected` | Yes | This was the exact input from my bug report, so it proves that bug is fixed |
| Range edges (`1` and `20` on Easy, `21` just above) | Same prompt as above | `test_guess_at_range_edges_accepted`, `test_guess_above_range_rejected` | Yes | Off-by-one mistakes happen at the edges. The limits must be accepted and one past them rejected |
| Empty / whitespace input (`"  "`) | Same prompt as above | `test_empty_guess_rejected` | Yes | Clicking Submit with an empty box is the most common accidental input |
| Non-numeric string (`abc`) | Same prompt as above | `test_non_number_rejected` | Yes | Typing letters must give a clear error, not a crash |
| String vs number comparison (`9` vs `10`) | "The hint does not work at all." | `test_hint_compares_numbers_not_strings` | Yes | The starter code compared strings on even attempts, and `"9" > "10"` as strings. This case fails if that bug comes back |
| Decimal (`50.9`, `100.0`) | "can you find more glitches?" → "fix all of them" | `test_decimal_rejected_not_truncated`, `test_trailing_dot_decimal_rejected` | Yes | `50.9` used to be silently cut to 50. The player should be told instead |
| Python-only number formats (`1_0`, `٥`, `1e2`, `0x10`) | "fix all of them" | `test_python_only_number_formats_rejected` | Yes | Python's `int()` accepts these, but a guessing game shouldn't |
| Huge number (5000 digits) | "fix all of them" | `test_huge_number_does_not_crash` | Yes | Python refuses to convert more than 4300 digits. This makes sure the game shows an error instead of crashing |
| Late win score (win on the 8th guess) | "fix all of them" | `test_late_win_never_negative` | Yes | Catches the AI's own earlier scoring bug, where a win could end at -5 |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
