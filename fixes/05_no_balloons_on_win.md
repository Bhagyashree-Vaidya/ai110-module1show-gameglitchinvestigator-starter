# Fix 5: No balloons when you win

## Symptom
Winning showed "You won! … Final score: 70", but the balloons never appeared.

## Root cause
This was introduced by Fix 2/4. After a guess, `app.py` calls `st.rerun()` so the page redraws with the
new state. `st.balloons()` ran just before that rerun, and the rerun cleared the page before
the animation could play. A Streamlit `AppTest` run of the old code showed **0** balloons elements after a win.

## Fix (`app.py`)
- On a win, set `st.session_state.celebrate = True` instead of calling `st.balloons()` directly.
- On the next run, if `celebrate` is set, call `st.balloons()` once and clear the flag.
- `start_new_game()` resets `celebrate` to `False`.

## Verified
`AppTest`: the new code sends **1** balloons element after a win and **0** on later reruns, so they play
once and don't repeat.
