# Fix 6: Guessing the same number again used up an attempt

## Symptom
Submitting 50 twice used up 2 attempts and took 10 points. History showed `[50, 50, 74]`.

## Root cause
`app.py` never checked whether a guess was already in `st.session_state.history`.

## Fix (`app.py`)
If the guess is already in history, show "You already guessed 50. Try a different number." and
don't count it: no attempt used, no points lost, nothing added to history.

## Verified
In the running app: guessed 50, then submitted 50 again. Attempts stayed at 1, the score stayed at -5,
and history stayed `[50]`.
