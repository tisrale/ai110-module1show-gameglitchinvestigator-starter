from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, update_score

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_numbers_compared_as_numbers_not_text():
    # Bug: as text, "9" > "50". As numbers, 9 is lower than 50.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_first_try_win_scores_100():
    # Bug: the off-by-one formula gave only 80 for a first-try win.
    assert update_score(0, "Win", 1) == 100


def test_win_points_drop_10_per_attempt():
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 5) == 60


def test_win_points_never_below_10():
    assert update_score(0, "Win", 10) == 10
    assert update_score(0, "Win", 20) == 10


def test_win_adds_to_existing_score():
    assert update_score(-10, "Win", 3) == 70


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_too_high_always_costs_5(attempt):
    # Bug: "Too High" on an even attempt used to ADD 5 points.
    assert update_score(20, "Too High", attempt) == 15


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_too_low_always_costs_5(attempt):
    assert update_score(20, "Too Low", attempt) == 15


# ---------------------------------------------------------------------------
# app.py: attempts and score during a real game
# ---------------------------------------------------------------------------

def start_app(secret=50):
    # The first run is slow while Streamlit loads, so allow more than the 3s default.
    at = AppTest.from_file(APP_PATH, default_timeout=15)
    at.run()
    at.session_state["secret"] = secret
    return at


def guess(at, value):
    at.text_input(key="guess_input_Normal").set_value(value)
    at.button[0].click()  # Submit Guess
    at.run()


def attempts_left_text(at):
    return at.info[0].value


def test_attempts_start_at_zero():
    # Bug: attempts started at 1, so a fresh game showed 7 of 8 attempts left.
    at = start_app()
    assert at.session_state["attempts"] == 0
    assert "Attempts left: 8" in attempts_left_text(at)


def test_valid_guess_uses_one_attempt():
    at = start_app()
    guess(at, "10")
    assert at.session_state["attempts"] == 1
    guess(at, "20")
    assert at.session_state["attempts"] == 2


def test_attempts_left_updates_right_after_guess():
    # Bug: the counter was drawn before the guess was processed, so it lagged by one.
    at = start_app()
    guess(at, "10")
    assert "Attempts left: 7" in attempts_left_text(at)


def test_invalid_guess_does_not_use_an_attempt():
    at = start_app()
    guess(at, "abc")
    assert at.session_state["attempts"] == 0
    assert "Attempts left: 8" in attempts_left_text(at)


def test_game_lost_after_attempt_limit():
    at = start_app(secret=50)
    for _ in range(8):
        guess(at, "10")
    assert at.session_state["attempts"] == 8
    assert at.session_state["status"] == "lost"


def test_correct_guess_on_even_attempt_wins():
    # Bug: on even attempts the secret became a string, so 50 != "50" and
    # a correct guess was not counted as a win.
    at = start_app(secret=50)
    guess(at, "10")
    guess(at, "50")
    assert at.session_state["status"] == "won"
    # -5 for the wrong guess, +90 for a win on attempt 2
    assert at.session_state["score"] == 85


def test_score_across_a_full_game():
    at = start_app(secret=50)
    guess(at, "60")  # Too High: -5
    guess(at, "70")  # Too High on an even attempt: still -5
    guess(at, "40")  # Too Low: -5
    guess(at, "50")  # Win on attempt 4: +70
    assert at.session_state["score"] == 55


def test_new_game_resets_score_and_state():
    # Bug: the score, status and history carried over into the next game.
    at = start_app(secret=50)
    guess(at, "50")
    assert at.session_state["status"] == "won"

    at.button[1].click()  # New Game
    at.run()

    assert at.session_state["attempts"] == 0
    assert at.session_state["score"] == 0
    assert at.session_state["status"] == "playing"
    assert at.session_state["history"] == []
