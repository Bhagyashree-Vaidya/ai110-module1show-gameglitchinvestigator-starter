import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def add_numbers(a, b):
    return a + b


def start_new_game(difficulty: str):
    """Reset every piece of game state for a fresh round at this difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

if "secret" not in st.session_state:
    start_new_game("Normal")

# FIX (Issue 2): lock the difficulty once a game is in progress, so the
# attempt limit and range can't change underneath a running game.
game_in_progress = (
    st.session_state.status == "playing" and st.session_state.attempts > 0
)

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    key="difficulty_select",
    index=["Easy", "Normal", "Hard"].index(st.session_state.difficulty),
    disabled=game_in_progress,
)

if game_in_progress:
    st.sidebar.caption("🔒 Finish the game or click New Game to change difficulty.")
elif difficulty != st.session_state.difficulty:
    # No guesses made yet, so switching just starts a fresh game in the new range.
    start_new_game(difficulty)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")

attempts_left = max(0, attempt_limit - st.session_state.attempts)
st.info(f"Guess a number between {low} and {high}. Attempts left: {attempts_left}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.rerun()

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # Invalid input doesn't use up an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)
        st.session_state.last_hint = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

        # Rerun so the lock, attempts counter and messages reflect the new state.
        st.rerun()

# FIX (Issue 4): the hint is stored in session state, so it survives reruns
# and follows the checkbox instead of only flashing on the submit run.
if show_hint and st.session_state.last_hint and st.session_state.status == "playing":
    st.warning(st.session_state.last_hint)

if st.session_state.status == "won":
    st.success(
        f"🎉 You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Click New Game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Click New Game to try again."
    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
