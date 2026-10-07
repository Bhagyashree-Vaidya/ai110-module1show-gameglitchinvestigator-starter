# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game it looked finished: a title, a difficulty dropdown, a guess box, and Submit / New Game buttons. But it was almost impossible to play correctly. The prompt said to pick a number between 1 and 100, yet it happily accepted `-30`. The hints pointed the wrong way: I guessed 21 when the secret was 98 and it told me "Go LOWER!". Switching the difficulty during a game made "Attempts left" go negative (-1), and after one lost game on Easy my score was -60, even though Easy only has 6 attempts.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| `-30` on Normal (range 1–100) | Rejected with a "must be between 1 and 100" message; no attempt used | Accepted as a guess, used an attempt, and showed "Go LOWER!" | None, failed silently |
| `21` on Easy, secret 98 (from Debug Info) | Hint "Go HIGHER!" | Hint "Go LOWER!", then "Out of attempts! The secret was 98. Score: -60" | None. The secret 98 was outside Easy's 1–20 range |
| Switch difficulty Normal → Easy mid-game | Not allowed, or a fresh game in the new range | "Attempts left: -1"; secret stayed from the old range | None |
| "Show hint" checked, then submit / rerun | Correct hint stays visible | Hint wrong on alternate guesses, gone after any rerun | None. Root cause: `secret` turned into a `str` on even attempts, so it compared strings (`"9" > "10"`) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code (in the Claude desktop app) as my AI coding assistant. <!-- TODO: add any other tools you used, e.g. ChatGPT for the Streamlit state question -->
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude found that the real cause of the "wrong hint" bug wasn't just swapped messages. On every even attempt the app turned the secret into a string, so Python compared `"21"` and `"98"` alphabetically. It suggested always comparing integers in `check_guess()` and moving that function into `logic_utils.py`. I verified it with a pytest case (`check_guess(9, 10)` must be "Too Low", which fails with string comparison) and by playing the game: guessing 50 against a secret of 74 correctly said "Go HIGHER!".
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

<!-- TODO (your own experience): describe one AI suggestion you changed or didn't accept as written, and why. Some candidates from this project, if any apply to you:
  - Claude rewrote the starter tests in tests/test_game_logic.py (they compared check_guess's tuple to a plain string). Did you agree with changing the tests rather than the function's return value?
  - Claude disabled the Difficulty dropdown mid-game. Would you have preferred asking for confirmation, or auto-restarting?
  - Anything in the diff you reviewed that felt over-engineered or harder to read.
Say what it suggested, what you did instead (or why you kept it after review), and how you checked your version. -->

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed only when two things were true: a pytest test that targets it passed, and I could no longer reproduce it by playing the app. For example, `test_negative_guess_rejected` checks that `parse_guess("-30", 1, 100)` returns an error mentioning "between 1 and 100". In the running app, entering -30 showed that message and "Attempts left" stayed at 8. Running `pytest` at the end showed all 13 tests passing. Yes, AI helped: Claude noticed the starter tests could never pass because they compared the `(outcome, message)` tuple to a plain string. It also added edge-case tests, like the range edges 1 and 20, and a worst-case Easy loss that has to be -30, not -60. <!-- TODO: add what *you* learned from reading those tests -->

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type in a box, Streamlit reruns your whole Python script from top to bottom, like refreshing the page. Normal variables are created fresh on every rerun, so they "forget" everything. `st.session_state` is a small dictionary that survives reruns, so anything the game must remember (the secret number, attempts, score, the last hint) has to live there. Several of this game's bugs were state bugs: New Game reset only part of `session_state`, and the hint was a temporary message instead of saved state, so it disappeared on the next rerun. <!-- TODO: rewrite in your own words -->

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

<!-- TODO (your own answers):
  - One habit to reuse (e.g. reproducing each bug and writing a test for it before fixing, reviewing every diff, or committing once tests pass)
  - One thing you'd do differently with AI next time
  - How this project changed your view of AI-generated code -->
