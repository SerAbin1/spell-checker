import pytest

from spell_checker import find_correct_spelling, generate_edits, known


@pytest.fixture
def small_dict():
    # A toy dictionary with artificial frequencies
    return {
        "cat": 50,
        "bat": 30,
        "rat": 10,
        "dog": 100,
        "cot": 20,
    }


def test_generate_edits_basic():
    edits = generate_edits("cat")
    # Check presence of some known edits
    assert "at" in edits  # delete c
    assert "act" in edits  # swap c and a
    assert "bat" in edits  # replace c -> b
    assert "cata" in edits  # insert a at end
    # Make sure the original word is not included
    assert "cat" not in edits


def test_known_function(small_dict):
    candidates = {"cat", "qat", "cot"}
    result = known(candidates, small_dict)
    assert result == {"cat", "cot"}


def test_exact_match(small_dict):
    assert find_correct_spelling("dog", small_dict) == "dog"


def test_one_edit_match(small_dict):
    # "dat" -> "cat" (replace d->c) or "bat" (replace d->b)
    correction = find_correct_spelling("dat", small_dict)
    assert correction in {"cat", "bat"}
    # but "cat" has higher frequency
    assert correction == "cat"


def test_two_edits_match(small_dict):
    # "dqt" is two edits from "cat"
    correction = find_correct_spelling("dqt", small_dict)
    assert correction == "cat"


def test_no_match_returns_none(small_dict):
    assert find_correct_spelling("zzzz", small_dict) is None
