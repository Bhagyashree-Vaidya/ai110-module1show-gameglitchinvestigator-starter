from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- check_guess (Issues 3 & 4) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_hint_compares_numbers_not_strings():
    # As strings, "21" < "98" but "9" > "10" — numeric compare must be used.
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"


# --- parse_guess (Issue 1) ---

def test_negative_guess_rejected():
    ok, value, err = parse_guess("-30", 1, 100)
    assert not ok and value is None
    assert "between 1 and 100" in err

def test_guess_above_range_rejected():
    ok, _, _ = parse_guess("21", 1, 20)
    assert not ok

def test_guess_at_range_edges_accepted():
    assert parse_guess("1", 1, 20) == (True, 1, None)
    assert parse_guess("20", 1, 20) == (True, 20, None)

def test_non_number_rejected():
    ok, _, err = parse_guess("abc", 1, 100)
    assert not ok and err == "That is not a number."

def test_empty_guess_rejected():
    ok, _, err = parse_guess("  ", 1, 100)
    assert not ok and err == "Enter a guess."


# --- update_score (Issue 3) ---

def test_first_try_win_scores_100():
    assert update_score(0, "Win", 1) == 100

def test_win_score_has_floor():
    assert update_score(0, "Win", 20) == 10

def test_wrong_guesses_always_cost_points():
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
    assert update_score(0, "Too Low", 2) == -5

def test_worst_case_easy_loss_bounded():
    # 6 wrong guesses on Easy can't produce the -60 seen in the bug report.
    score = 0
    for attempt in range(1, get_attempt_limit("Easy") + 1):
        score = update_score(score, "Too Low", attempt)
    assert score == -30


# --- Glitch 3: a win never ends with a negative score ---

def test_late_win_never_negative():
    # 7 wrong guesses on Normal (-35), then a win on the 8th used to give -5.
    score = 0
    for attempt in range(1, 8):
        score = update_score(score, "Too Low", attempt)
    assert update_score(score, "Win", 8) == 10

def test_early_win_unaffected_by_floor():
    assert update_score(-5, "Win", 2) == 85


# --- Glitches 4 & 5: only whole ASCII numbers are accepted ---

def test_decimal_rejected_not_truncated():
    ok, value, err = parse_guess("50.9", 1, 100)
    assert not ok and value is None
    assert "whole number" in err

def test_trailing_dot_decimal_rejected():
    assert parse_guess("100.0", 1, 100)[2] == "Enter a whole number (no decimals)."

def test_python_only_number_formats_rejected():
    for raw in ["1_0", "٥", "1e2", "0x10"]:
        ok, _, err = parse_guess(raw, 1, 100)
        assert not ok, raw
        assert err == "That is not a number.", raw

def test_huge_number_does_not_crash():
    ok, _, err = parse_guess("9" * 5000, 1, 100)
    assert not ok and "between 1 and 100" in err

def test_plus_sign_still_accepted():
    assert parse_guess("+5", 1, 100) == (True, 5, None)


# --- Glitch 6: difficulty actually gets harder ---

def test_ranges_grow_with_difficulty():
    sizes = [get_range_for_difficulty(d)[1] for d in ("Easy", "Normal", "Hard")]
    assert sizes == sorted(sizes) and len(set(sizes)) == 3

def test_hard_settings():
    assert get_range_for_difficulty("Hard") == (1, 200)
    assert get_attempt_limit("Hard") == 7
