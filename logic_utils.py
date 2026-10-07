import re

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    # FIX (Glitch 6): Hard gets the biggest range, so it has a few more attempts than before.
    "Hard": 7,
}

# Only plain ASCII digits with an optional sign, e.g. "42", "-30", "+7".
# Python's int() also accepts "1_0" and non-ASCII digits like "٥", which we don't want.
WHOLE_NUMBER = re.compile(r"[+-]?[0-9]+")
DECIMAL_NUMBER = re.compile(r"[+-]?([0-9]+\.[0-9]*|\.[0-9]+)")


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX (Glitch 6): Hard used to be 1-50, a smaller range than Normal.
        return 1, 200
    return 1, 100


def get_attempt_limit(difficulty: str):
    """Return how many guesses the player gets for a given difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, ATTEMPT_LIMITS["Normal"])


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    # FIX (Glitches 4 & 5): decimals used to be silently truncated ("50.9" -> 50),
    # and "1_0" / "٥" slipped through int(). Only whole ASCII numbers are accepted now.
    if DECIMAL_NUMBER.fullmatch(raw):
        return False, None, "Enter a whole number (no decimals)."
    if not WHOLE_NUMBER.fullmatch(raw):
        return False, None, "That is not a number."

    try:
        value = int(raw)
    except ValueError:
        # Python refuses to convert absurdly long digit strings (4300+ digits).
        return False, None, f"Your guess must be between {low} and {high}."

    # FIX (Issue 1): reject numbers outside the difficulty's range, e.g. -30.
    if value < low or value > high:
        return False, None, f"Your guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX (Issue 3/4): always compare ints, and point the hint the right way.
    # A guess that is too high means the player must go LOWER, and vice versa.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1 for the first guess. A first-try win is worth 100,
    each extra attempt costs 10 (minimum 10). Every wrong guess costs 5.
    A win always leaves you with at least 10 points in total.
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        # FIX (Glitch 3): a late win could end with a negative score (e.g. -5).
        return max(10, current_score + points)

    # FIX (Issue 3): "Too High" used to randomly *add* points on even attempts.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
